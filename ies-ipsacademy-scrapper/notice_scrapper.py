from imports import *

# --------------------------------------------------------------

def get_notice_articles(soup):
    nb = soup.find('main', attrs={"id": "main"})
    # print(nb)
    articles = nb.findChildren('article')
    # print(f"Fetched {len(articles)} Articles")
    print(f"Returning {len(articles)} Articles")
    return articles


def get_notices(articles):
    notices = []
    for article in articles:
        notice = article.findChildren('div')[1].findChild('header').findChild('h2').find('a')
        # print(notice)
        notices.append(notice)
    return notices


def format_notices(notices):
    formatted_notices = []
    for notice in notices:
        data = {
            "Notice": notice.text,
            "Link": notice.get('href')
        }
        formatted_notices.append(data)
    return formatted_notices


# --------------------------------------------------------------


def get_formatted_notice():
    start_time = time.time()

    html = to_soup.get_html(nb_url)
    soup = to_soup.get_soup(html)

    articles = get_notice_articles(soup)
    notices = get_notices(articles)
    formatted_notices = format_notices(notices)

    end_time = time.time()
    print("Time Elapsed: {:.3f}s".format(end_time - start_time))
    return formatted_notices

def get_formatted_notice_for_alert():
    start_time = time.time()

    html = to_soup.get_html(nb_url)
    soup = to_soup.get_soup(html)

    articles = get_notice_articles(soup)
    notices = get_notices(articles)
    formatted_notices = format_notices(notices)

    end_time = time.time()
    print("Time Elapsed: {:.3f}s".format(end_time - start_time))
    pairs = []
    for fn in formatted_notices:
        pairs.append({'COLLEGE': fn['Link']})
        break
    return pairs

def set_notice():
    # no need
    formatted_notices = get_formatted_notice()
    msg = ''
    for formatted_notice in formatted_notices:
        result1 = str(formatted_notice['Notice'])
        result2 = str(formatted_notice['Link'])
        msg = msg + result1 + '\n' + result2 + '\n\n'
    return msg


# --------------------------------------------------------------

if __name__ == '__main__':
    formatted_notices = get_formatted_notice()
    print(formatted_notices)

# --------------------------------------------------------------
