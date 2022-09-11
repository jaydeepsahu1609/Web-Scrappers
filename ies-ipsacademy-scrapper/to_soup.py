import requests
from bs4 import BeautifulSoup

# --------------------------------------------------------------


def get_html(url: str = None):
    """request for the given url and then return the response in text or None"""
    # print("\nInside get_html")
    if url is None:
        print("No url passed")
        return None

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

    response = requests.get(url, headers=header)
    if response.status_code != 200:
        print("Response: ", response.status_code)
        return None
    return response.text


def get_soup(html: str = None):
    """receives html and return BeautifulSoup Object"""
    # print("\nInside get_soup")
    if html is None:
        print("HTML not received")
        return None
    soup = BeautifulSoup(html, "html.parser")
    return soup

# --------------------------------------------------------------
