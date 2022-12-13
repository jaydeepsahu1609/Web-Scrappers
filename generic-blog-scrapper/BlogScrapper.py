import json
import re
import time

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# #################################################################################


class BlogScrapper:
    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this method will return all the html of a webpage using selenium
        :param: url: URL to be scrapped
        :type: str
        :return: html page
        :rtype: str
        """
        print("Inside get_page_source | this may take longer in case of infinite scrolling page")

        option = Options()
        option.headless = True
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        option.add_argument("--window-size=1920,1080")
        option.add_argument("user-agent=Chrome/80.0.3987.132")

        # installing driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=option)

        # sending the request
        driver.get(url=url)

        # all the blogs will only appear when we have scrolled
        # down till the end -- infinite scrolling pages
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        scroll_pause_time = 2  # we need to wait for the page to load completely after scrolling

        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # scrolling is done
        page_source = driver.page_source
        driver.quit()

        return page_source

    @staticmethod
    def get_parent_tag_in_blog_page(page_source: str) -> Tag:
        """
        this function tries to find the tag that holds the blog-text in
        any html page

        :param page_source: html text of the scraped page
        :type: str

        :return: Tag that holds the whole content of blog
        :rtype: bs4.Tag
        """
        soup = BeautifulSoup(page_source, 'html.parser')
        # print(soup.prettify())

        p_s = soup.find_all('p')
        max_text_p = None
        max_text_length = 0

        for p in p_s:
            p_text_length = len(p.text)
            if max_text_p is None or p_text_length > max_text_length:
                max_text_p = p
                max_text_length = p_text_length

        parent_tag = max_text_p.findParent()  # -- container of blog
        # print(parent_tag)

        return parent_tag

    @staticmethod
    def word_counter(data: str) -> int:
        """
        this method counts the number of words in a given text

        :param data: text we need to count words of
        :type: str

        :return: number of words in the given data
        :rtype: int
        """
        word_count = 0

        print("inside word_counter")

        # split the sentences
        sentences = data.split('\n')

        # now count the number of words in each sentence
        for sentence in sentences:
            # remove trailing whitespaces
            sentence = sentence.strip()

            # remove punctuations from sentences
            sentence = re.sub(r'[^\w\s]', '', sentence)
            # print(sentence)

            # now; count the words in the sentence
            words = sentence.split()

            # print(words)
            # print(len(words))
            word_count += len(words)

        return word_count

    @staticmethod
    def get_word_count_from_blog_url(blog_url: str) -> int:
        """
        this method scraps blog from given url
        and returns the number of words in that blog

        :param blog_url: url of the blog to be scraped
        :type: str

        :return: word-count of the blog
        :rtype: int
        """
        print("Inside scrap_blog")

        start = time.time()

        # get page source
        page_source = BlogScrapper.get_page_source(url=blog_url)

        parent_tag = BlogScrapper.get_parent_tag_in_blog_page(page_source=page_source)

        # now extract the text of blog
        content = parent_tag.get_text(separator=' ')
        # print(content)

        # now, get the count of words in that article
        word_count = BlogScrapper.word_counter(data=content)

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")

        return word_count

    @staticmethod
    def get_headings_sub_headings_from_blog_url(blog_url: str) -> list:
        """
        this method scraps all the headings and sub-headings of blog from given url

        :param blog_url: url of the blog to be scraped
        :type: str

        :return : all the heading and subheadings within the blog
        :rtype: list of dict
        """
        print("Inside scrap_blog")

        start = time.time()

        # get page source
        page_source = BlogScrapper.get_page_source(url=blog_url)

        # get parent tag that contains all the content of the blog
        parent_tag = BlogScrapper.get_parent_tag_in_blog_page(page_source=page_source)

        # find all heading tags within the blog
        h_s = parent_tag.find_all(['h1', 'h2', 'h3', 'h4'])
        # print(h_s)

        # will hold all the heading tags : we will return this list
        heading_tags = []

        for tag in h_s:
            if tag.name == 'h1':
                heading_tags.append({
                    'heading': tag.text,
                    'subheadings': []
                })
            elif tag.name == 'h2':
                if len(heading_tags) == 0:
                    heading_tags.append({
                        'heading': "",
                        'subheadings': []
                    })
                heading_tags[-1]['subheadings'].append({
                    'heading': tag.text,
                    'subheadings': []
                })
            elif tag.name == 'h3':
                if len(heading_tags[-1]['subheadings']) == 0:
                    heading_tags[-1]['subheadings'].append({
                        'heading': "",
                        'subheadings': []
                    })
                heading_tags[-1]['subheadings'][-1]['subheadings'].append({
                    'heading': tag.text,
                    'subheadings': []
                })
            elif tag.name == 'h4':
                if len(heading_tags[-1]['subheadings'][-1]['subheadings']) == 0:
                    heading_tags[-1]['subheadings'][-1]['subheadings'].append({
                        'heading': "",
                        'subheadings': []
                    })
                heading_tags[-1]['subheadings'][-1]['subheadings'][-1]['subheadings'].append({
                    'heading': tag.text,
                    'subheadings': []
                })

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")

        return heading_tags


# #################################################################################

if __name__ == '__main__':
    urls = [
        'https://blog.ipleaders.in/gst-amendment-act/',
        'https://blog.finology.in/Legal-news/road-safety-laws',
        'https://www.cars24.com/blog/how-to-drive-a-car-manual-automatic/',
        'https://www.vidhikarya.com/legal-blog/online-business-difficulty-with-consumers-compliance-and-fake-jobs'
    ]

    urls = [
        'https://www.vidhikarya.com/legal-blog/online-business-difficulty-with-consumers-compliance-and-fake-jobs'
    ]
    for url in urls:
        blog_word_count = BlogScrapper.get_word_count_from_blog_url(blog_url=url)
        print(blog_word_count)

        headings = BlogScrapper.get_headings_sub_headings_from_blog_url(blog_url=url)
        print(json.dumps(headings, indent=4))

# #################################################################################
