import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class FinologyScrapper:
    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this method will return all the html of a webpage using selenium

        :param: url: URL to be scrapped
        :type: str

        :return: html page
        :type: str
        """
        print(f"Inside get_page_source -> {url}")

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
    def scrap_finology_blogs():
        """
        this method scraps legal blogs from `https://blog.finology.in/Legal-news`
        and saves following data to a csv file
        - Title of blog
        - link of image
        - link of article
        """
        print("Inside scrap_finology_blogs")

        start = time.time()

        # contains all blog cards
        blog_grids = []

        page = 1
        while page:
            # url of finology blog site pages
            url = f'https://blog.finology.in/Legal-news/page/{page}'
            page += 1

            # get page source
            page_source = FinologyScrapper.get_page_source(url=url)
            soup = BeautifulSoup(page_source, 'html.parser')

            blogs = soup.find_all('div', attrs={'class': 'grid'})
            if blogs is not None and len(blogs) != 0:
                blog_grids.extend(blogs)
            else:
                break

        blogs_data = []
        for blog in blog_grids:
            img_a = blog.findChild('img')
            data = {
                'blog_title': img_a['alt'],
                'blog_url': f'https://blog.finology.in{img_a.findParent()["href"]}',
                'image_url': img_a['src']
            }
            blogs_data.append(data)

        # save data to csv
        FinologyScrapper.save_data_to_csv('finology_blogs.csv', data=blogs_data)

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")


if __name__ == '__main__':
    FinologyScrapper.scrap_finology_blogs()
