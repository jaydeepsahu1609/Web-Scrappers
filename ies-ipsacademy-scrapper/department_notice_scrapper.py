from imports import *

# --------------------------------------------------------------


def get_articles(soup):
    nb = soup.find('main', attrs={"id": "main", "class": "site-main"})
    # print(nbc)
    articles = nb.findChildren('article')
    print(f"Fetched {len(articles)} Articles")
    print(f"Returning {len(articles)} Articles")
    return articles


def get_notice_from_articles(articles):
    notices = []
    for article in articles:
        notice = article.findChildren('div')[1].findChild('header').find('h2').find('a')
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


def get_department_notice(branch: str):
    print(f"inside get_department_notice: {branch}")
    url = department_notice_url[branch]
    start_time = time.time()

    html = to_soup.get_html(url)
    soup = to_soup.get_soup(html)

    articles = get_articles(soup)
    notices = get_notice_from_articles(articles)
    formatted_notices = format_notices(notices)

    end_time = time.time()
    print("Time Elapsed: {:.3f}s".format(end_time - start_time))
    return formatted_notices


def get_formatted_dept_notice_for_alert(branch):
    print(f"get_formatted_dept_notice_for_alert: {branch}")
    url = department_notice_url[branch]
    start_time = time.time()

    html = to_soup.get_html(url)
    soup = to_soup.get_soup(html)

    articles = get_articles(soup)
    notices = get_notice_from_articles(articles)
    formatted_notices = format_notices(notices)

    end_time = time.time()
    print("Time Elapsed: {:.3f}s".format(end_time - start_time))
    pairs = []
    for fn in formatted_notices:
        pairs.append(({branch.upper(): fn['Link']}))
        break
    return pairs

# --------------------------------------------------------------

if __name__ == '__main__':
    print(get_department_notice('ft'))

# --------------------------------------------------------------
