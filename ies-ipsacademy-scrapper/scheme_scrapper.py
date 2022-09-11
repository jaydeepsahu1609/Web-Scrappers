from imports import *
# --------------------------------------------------------------


def get_div(branch: str):
    branch = branch.strip()
    if len(branch.strip()) == 0:
        return None
    try:
        url = scheme_links[branch]
    except KeyError as ke:
        print("Branch Not Found.")
        return None

    html = to_soup.get_html(url)
    soup = to_soup.get_soup(html)
    main = soup.find('main', attrs={"id": "main"})
    div = main.findChild("article").findChild("div")
    return div


# --------------------------------------------------------------


def get_schemes_cse_csit():
    div = get_div("cse")

    if div is None:
        return None

    p = div.findChildren("p")[-1]
    uls = div.findChildren("ul")

    urls = {}
    for ul in uls:
        lis = ul.findChildren("li")
        for li in lis:
            a = li.findChild("a")
            if a is not None:
                title = a.text
                link = a.get('href')
                urls[title] = link

    a_s = p.findChildren('a')
    for a in a_s:
        if a is not None:
            title = a.text
            link = a.get('href')
            urls[title] = link

    print(f"Returning {len(urls)} urls.")
    # for u in urls.items():
    #     print(u)
    return urls


def get_schemes_mechanical():
    div = get_div("mechanical")

    if div is None:
        return None

    paras = div.findChildren("p")

    urls = {}
    for p in paras:
        a_s = p.findChildren('a')
        for a in a_s:
            title = a.text
            link = a.get('href')
            urls[title] = link

    print(f"Returning {len(urls)} urls.")
    # for u in urls.items():
    #     print(u)
    return urls


def get_schemes_chemical():
    div = get_div("chemical")

    if div is None:
        return None

    paras = div.findChildren("p")
    urls = {}
    for p in paras:
        a_s = p.findChildren('a')
        for a in a_s:
            if a is not None:
                title = a.text
                link = a.get('href')
                urls[title] = link

    # for u in urls.items():
    #     print(u)
    return urls


def get_schemes_general():
    div = get_div("general")

    if div is None:
        return None

    paras = div.findChildren("p")
    urls = {}

    for p in paras:
        a_s = p.findChildren('a')
        for a in a_s:
            title = p.text
            link = a.get('href')
            urls[title] = link

    print(f"Returning {len(urls)} urls.")
    for u in urls.items():
        print(u)
    return urls


# --------------------------------------------------------------


def get_schemes(branch: str):
    branch = branch.strip()

    if len(branch) == 0:
        return None

    if branch == "cse":
        return get_schemes_cse_csit()

    if branch == "cm":
        return get_schemes_chemical()
    if branch == "mechanical":
        return get_schemes_mechanical()
    if branch == "general":
        return get_schemes_general()

    # FOR ELECTRICAL | ELECTRONICS | FT
    div = get_div(branch)
    if div is None:
        return None

    paras = div.findChildren("p")
    urls = {}

    for p in paras:
        a_s = p.findChildren('a')
        for a in a_s:
            title = a.text
            link = a.get('href')
            urls[title] = link

    print(f"Returning {len(urls)} urls.")
    # for u in urls.items():
    #     print(u)
    return urls


# --------------------------------------------------------------


if __name__ == '__main__':
    branch = "cse"
    urls = get_schemes(branch)
    print(urls)

# --------------------------------------------------------------
