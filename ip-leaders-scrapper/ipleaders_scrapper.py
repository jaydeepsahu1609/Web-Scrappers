import csv
import time

from bs4 import BeautifulSoup
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class IPleaderScrapper:
    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this method will return all the html of a webpage using selenium

        :param: url: URL to be scrapped
        :type: str

        :return: html page
        :type: str
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

        # all the videos will only appear when we have scrolled
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
    def save_data_to_csv(file_name: str, data: list):
        """
        this is a generic method that saves data into a csv file
        `<file_name>.csv`

        :param file_name: name of csv file
        :type: str

        :param data: data to be saved
        :type: list of dict
        """
        print("Inside save_data_to_csv..")

        try:
            with open(file_name, 'w', newline='', encoding='utf8') as csv_file:
                fc = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                fc.writeheader()
                fc.writerows(data)
            print(f"`{file_name}` Saved Successfully.")
        except Exception as e:
            print(f"Error while Saving the File.\n{e}")

    @staticmethod
    def scrap_ipleaders_blogs():
        """
        this methods scraps url from `https://blog.ipleaders.in/blog/`
        and saves following data to a csv file
        - Title of blog
        - link of image
        - Creation Date
        - link of article
        """
        print("Inside scrap_ipleaders_blogs")

        start = time.time()

        # url of ipleaders site
        url = 'https://blog.ipleaders.in/blog/'

        # get page source
        page_source = IPleaderScrapper.get_page_source(url=url)
        soup = BeautifulSoup(page_source, 'html.parser')

        # get all blogs
        blogs = soup.find_all('div', attrs={'class': 'td_module_3 td_module_wrap td-animation-stack'})
        print(f"{len(blogs)} blogs found.")

        # get all relevant data
        blogs_data = []
        for blog in blogs:
            image_a = blog.findChild('div', attrs={'class': 'td-module-image'}).findChild(
                'div', attrs={'class': 'td-module-thumb'}).findChild('img')

            title_url_a = blog.findChild('h3').findChild('a')

            creation_date = blog.findChild('div', attrs={'class': 'td-module-meta-info'}).findChild(
                'span', attrs={'class': 'td-post-date'}).findChild('time')

            data = {
                'blog_title': title_url_a['title'],
                'blog_url': title_url_a['href'],
                'image_url': image_a['src'],
                'date': parser.parse(creation_date['datetime']).date()
            }
            blogs_data.append(data)

        # save data to csv
        IPleaderScrapper.save_data_to_csv('ipleaders_blogs.csv', data=blogs_data)

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")


if __name__ == '__main__':
    IPleaderScrapper.scrap_ipleaders_blogs()
