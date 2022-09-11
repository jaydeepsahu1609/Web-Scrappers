"""
This script contains scrapper for famous pdf books delivering website
`https://pdfdrive.net`, that contains an amazing search engine and claims to provide
millions of pdf books.

These books have helped me a lot during my college years and still
provides some amazing content.

Aim of this scrapper is to automate the process of fetching the results
and include book searching features in my future projects as well
including the `college information chatbot` that I created for helping
the students of my college.

"""
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup


class PdfDriveScrapper:
    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this function returns page source of any url

        :param url: page to be fetched
        :type: str

        :return: page source of the url
        :type: str
        """
        print(f"inside PdfDriveScrapper.get_page_source")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return ""

    @staticmethod
    def pdf_drive_search(query: str, limit: int = 15) -> list:
        """
        this method returns books response from page

        :param query: query to be searched
        :type: str

        :param limit: number of results returned | defaults to 10
        :type: int

        :return: books information (name and urls)
        :type: list of dicts | similar to json | helpful if we need to store the data in csv or other format
        """
        print(f"inside PdfDriveScrapper.pdf_drive_search")
        start = time.time()

        pdf_drive_search_url = 'https://www.pdfdrive.com/search?q=' + (urllib.parse.quote(query))
        page_source = PdfDriveScrapper.get_page_source(url=pdf_drive_search_url)

        if len(page_source) == 0:
            end = time.time()
            print(f"Elapsed Time: {round(end - start, 2)}")
            return []

        print("Scrapping the content...")

        soup = BeautifulSoup(page_source, 'html.parser')
        books_a_s = soup.find('div', attrs={'class': 'files-new'}).findChild('ul').findChildren('li')

        books = []
        counter = 0

        for book_a in books_a_s:
            url = book_a.findChild('a')['href']
            title_thumb = book_a.findChild('img')
            title = title_thumb['alt']
            thumb = title_thumb['src']

            data = {
                'title': title,
                'thumbnail': thumb,
                'url': f'https://www.pdfdrive.com/{url}'
            }

            books.append(data)

            counter += 1
            if counter == limit:
                break

        end = time.time()
        print(f"Returning {len(books)} results.")
        print(f"Elapsed Time: {round(end-start, 2)}")
        return books


if __name__ == '__main__':
    books_data = PdfDriveScrapper.pdf_drive_search('big data')
    for book in books_data:
        print(book)
