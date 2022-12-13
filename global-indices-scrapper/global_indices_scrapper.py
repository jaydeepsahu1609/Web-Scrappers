import requests
from bs4 import BeautifulSoup
import csv
import time

def get_html(url: str = None):
    """request for the given url and then return the response in text or None"""
    print("\nInside get_html")
    if url is None:
        print("No url passed")
        return None

    # The web server detects the python script as a bot and hence blocks it.
    # By using headers you can prevent it
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}

    print("sending a GET request to the given url")
    response = requests.get(url, headers=header)
    print(f"Recieved: {response}")
    if response.status_code != 200:
        print("Response: ", response.status_code)
        return None
    print("Returning response.text")
    # print(response.text)
    return response.text


def get_soup(html: str = None):
    """receives html and return BeautifulSoup Object"""
    print("\nInside get_soup")
    if html is None:
        print("HTML not received")
        return None
    soup = BeautifulSoup(html, "html.parser")
    print("BeautifulSoup object created")
    # print(soup)
    print("Returning BeautifulSoup Object")
    return soup


def get_price(soup: BeautifulSoup = None):
    """Returns tuple of (Name, Last, High, Low, Chg%, Chg, Time) for the given name"""
    print("\ninside get_price")
    if soup is None:
        print("Received None")
        return None

    section = soup.find('section', {"class": "instrument js-section-content"})
    table = section.findChildren('table')[0]

    trs = table.find_all('tr', attrs={"class": "common-table-item"})

    price_data = []
    for tr in trs:
        rows = []
        td_names = tr.findChildren('td', {"class": "col-name"})
        for td_name in td_names:
            name = td_name.findChild('a').text
            rows.append(name)

        td_lasts = tr.findChildren('td', {"class": "col-last"})
        for td_last in td_lasts:
            last = td_last.findChild('span').text
            rows.append(last)

        td_highs = tr.findChildren('td', {"class": "col-high"})
        for td_high in td_highs:
            high = td_high.findChild('span').text
            rows.append(high)

        td_lows = tr.findChildren('td', {"class": "col-low"})
        for td_low in td_lows:
            low = td_low.findChild('span').text
            rows.append(low)

        td_chg_pcts = tr.findChildren('td', {"class": "col-chg_pct"})
        for td_chg_pct in td_chg_pcts:
            chg_pct = td_chg_pct.findChild('span').text
            rows.append(chg_pct)

        td_chgs = tr.findChildren('td', {"class": "col-chg"})
        for td_chg in td_chgs:
            chg = td_chg.findChild('span').text
            rows.append(chg)

        td_times = tr.findChildren('td', {"class": "col-time"})
        for td_time in td_times:
            time = td_time.findChild('time').text
            rows.append(time)

        # print(rows)
        price_data.append(rows)

    print(f"Returning {len(price_data)} rows")
    return price_data


def get_performance(soup: BeautifulSoup = None):
    """Returns tuple of (day, week, month, ytd, year, 3year) for the given name"""
    print("\ninside get_performance")
    if soup is None:
        print("Received None")
        return None

    section = soup.find('section', {"class": "instrument js-section-content"})
    table = section.findChildren('table')[0]

    trs = table.find_all('tr', attrs={"class": "common-table-item"})

    performance_data = []
    for tr in trs:
        rows = []
        td_days = tr.findChildren('td', {"class": "col-performance_day"})
        for td_day in td_days:
            day = td_day.findChild('span').text
            rows.append(day)

        td_weeks = tr.findChildren('td', {"class": "col-performance_week"})
        for td_week in td_weeks:
            week = td_week.findChild('span').text
            rows.append(week)

        td_months = tr.findChildren('td', {"class": "col-performance_month"})
        for td_month in td_months:
            month = td_month.findChild('span').text
            rows.append(month)

        td_ytds = tr.findChildren('td', {"class": "col-performance_ytd"})
        for td_ytd in td_ytds:
            ytd = td_ytd.findChild('span').text
            rows.append(ytd)

        td_years = tr.findChildren('td', {"class": "col-performance_year"})
        for td_year in td_years:
            year = td_year.findChild('span').text
            rows.append(year)

        td_3years = tr.findChildren('td', {"class": "col-performance_3year"})
        for td_3year in td_3years:
            t_year = td_3year.findChild('span').text
            rows.append(t_year)

        performance_data.append(rows)

    print(f"Returning {len(performance_data)} rows")
    return performance_data


def get_technical(soup: BeautifulSoup = None):
    """Returns tuple of (day, hour, week, month) for the given name"""
    print("\ninside get_performance")
    if soup is None:
        print("Received None")
        return None

    section = soup.find('section', {"class": "instrument js-section-content"})
    table = section.findChildren('table')[0]

    trs = table.find_all('tr', attrs={"class": "common-table-item"})

    technical_data = []
    for tr in trs:
        rows = []

        td_days = tr.findChildren('td', {"class": "col-technical_day"})
        for td_day in td_days:
            day = td_day.findChild('span').text
            rows.append(day)

        td_hours = tr.findChildren('td', {"class": "col-technical_hour"})
        for td_hour in td_hours:
            hour = td_hour.findChild('span').text
            rows.append(hour)

        td_weeks = tr.findChildren('td', {"class": "col-technical_week"})
        for td_week in td_weeks:
            week = td_week.findChild('span').text
            rows.append(week)

        td_months = tr.findChildren('td', {"class": "col-technical_month"})
        for td_month in td_months:
            month = td_month.findChild('span').text
            rows.append(month)

        technical_data.append(rows)

    print(f"Returning {len(technical_data)} rows")
    return technical_data


def get_price_data():
    """Return data from price section by calling all the aforementioned methods"""
    print("\ninside get_price_data")
    price_url = 'https://in.investing.com/indices/global-indices?c_id%5B%5D=all&majorIndices=on&r_id%5B%5D=1&r_id%5B%5D=2&r_id%5B%5D=3&r_id%5B%5D=4&r_id%5B%5D=5'

    html = get_html(price_url)
    soup = get_soup(html)
    price_data = get_price(soup)

    return price_data


def get_performance_data():
    """Return data from performance section by calling all the aforementioned methods"""
    print("\n\ninside get_performance_data")
    performance_url = 'https://in.investing.com/indices/global-indices/performance?c_id%5B%5D=all&majorIndices=on&r_id%5B%5D=1&r_id%5B%5D=2&r_id%5B%5D=3&r_id%5B%5D=4&r_id%5B%5D=5'
    html = get_html(performance_url)
    soup = get_soup(html)
    performance_data = get_performance(soup)

    return performance_data


def get_technical_data():
    """Return data from technical section by calling all the aforementioned methods"""
    print("\n\ninside get_technical_data")
    technical_url = 'https://in.investing.com/indices/global-indices/technical?c_id%5B%5D=all&majorIndices=on&r_id%5B%5D=1&r_id%5B%5D=2&r_id%5B%5D=3&r_id%5B%5D=4&r_id%5B%5D=5'
    html = get_html(technical_url)
    soup = get_soup(html)
    technical_data = get_technical(soup)

    return technical_data


def combine_data(price_data, performance_data, technical_data):
    """combines all the data in the form of list of tuples"""
    print("\ninside combine_data")

    combined_data = []
    count = len(price_data)

    for row in range(count):
        data = tuple(price_data[row] + performance_data[row] + technical_data[row])
        combined_data.append(data)

    # print(combined_data)
    return combined_data


def create_csv(data, filename: str = "global_indices.csv"):
    """Create csv file for the combined data"""
    print("\nInside create_csv")
    try:
        fileptr = open(filename, 'w')

        header = ("Name", "Last", "High", "Low", "chg_pct", "chg", "Time", "Day", "Week", "Month", "Ytd", "Year", "3Year", "Day", "Hour", "Week", "Month")

        # create the csv writer
        writer = csv.writer(fileptr)

        # write heading
        writer.writerow(header)

        for row in data:
            # write  row to the csv file
            writer.writerow(row)

        # close the file
        fileptr.close()

        print(f"CSV Created Successfully. \nFile Name: {filename}")
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    start_time = time.time()
    price_data = get_price_data()
    performance_data = get_performance_data()
    technical_data = get_technical_data()
    combined = combine_data(price_data, performance_data, technical_data)
    create_csv(combined, "global_indices.csv")
    end_time = time.time()
    print("Time Elapsed: {:.3f}s".format(end_time - start_time))

