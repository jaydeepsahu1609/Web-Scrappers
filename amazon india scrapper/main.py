"""
A simple web-scrapper for `amazon.in`.
You just need to pass the search string to the method
and it will return all the required data in a list
"""

from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests


def get_page_source(url: str) -> str:
    """
    this method returns the page source after sending a get request
    :param url: url to be fetched
    :type: str
    :return: page source
    :type: str
    """
    print(f"Inside get_page_source(url='{url}')")

    # you need to pass headers when sending a get request using a python script
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        return response.text

    return ""


def search_amazon_in(query: str) -> list:
    """
    this method takes user's search string and returns a list of responses of product
    using amazon-india
    :param query: search string of user
    :type: str
    :return: list of dicts that contains product information
    :type: list
    """
    # ########################################
    # STEP-1 | GET THE PAGE SOURCE
    # ########################################
    print(f"Inside amazon_in(query='{query}')")
    amazon_in_url = "https://www.amazon.in/s?k="  # url of amazon india

    # we need to parse (i.e,url-encoding) the user query to fit it into url as query parameter
    query = quote_plus(query)

    # final url
    url = amazon_in_url + query
    # print(url)

    # now fetch page source by sending a get request
    response = get_page_source(url=url)

    if response == "":
        return []

    # ########################################
    # STEP-2 | PARSE THE PAGE SOURCE
    # ########################################

    # use BeautifulSoup to parse the page source
    soup = BeautifulSoup(response, 'html.parser')
    # print(soup)

    # ########################################
    # STEP-3 | SCRAP THE DESIRED DATA
    # ########################################

    # using browser's inspect tool, locate the tag that contains the results
    rows = soup.find_all('div', attrs={'class': 's-result-item s-asin sg-col sg-col-12-of-12 s-widget-spacing-small'})

    result = []

    for row in rows:
        card_row = row.find('div', attrs={"class": "sg-row"})

        image_url = card_row.find('img', attrs={"class": "s-image"})
        title_span = card_row.find('span', attrs={"class": "a-size-small a-color-base a-text-normal"})
        product_url = card_row.find('a', attrs={"title": "product-detail", "class": "a-link-normal s-faceout-link a-text-normal"})
        price_span = card_row.find('span', attrs={"class": "a-price-whole"})

        data = {
            "image_url": image_url['src'],
            "product_title": title_span.contents[0],
            "product_url": f"https://www.amazon.in/{product_url['href']}",
            "price": f"{price_span.contents[0]}"
        }
        result.append(data)

    print(f"Returning {len(result)} results.")
    return result


if __name__ == '__main__':
    result = search_amazon_in(query="lenovo ideapad slim3i")
    for product in result:
        print(product)
        print()
