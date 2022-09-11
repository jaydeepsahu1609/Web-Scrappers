import csv
import datetime
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class YTScrapper:

    # general purpose methods

    @staticmethod
    def get_channel_name_from_url(channel_link: str) -> str:
        """
        this method returns channel name from its url

        :param channel_link: url of channel
        :type: str

        :return: channel name
        :type: str
        """
        page_source = YTScrapper.get_page_source(url=channel_link)
        soup = BeautifulSoup(page_source, 'html.parser')
        channel_name = soup.find('div',
                                 attrs={'id': 'text-container', 'class': 'style-scope ytd-channel-name'}).findChild(
            'yt-formatted-string',
            attrs={'class': 'style-scope ytd-channel-name', 'id': 'text'}).contents[0]

        return str(channel_name)

    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this method will return all the html of a YouTube channel using selenium

        :param: url: URL to be scrapped
        :type: str

        :return: html page
        :type: str
        """
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
        scroll_pause_time = 0.8  # we need to wait for the page to load completely after scrolling

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
    def save_channel_data_to_csv(file_name: str, channel_data: list):
        """
        this is a generic method that saves data into a csv file
        `<file_name>.csv`

        :param file_name: name of channel to which the data belongs
        :type: str

        :param channel_data: data to be saved
        :type: list of dicts
        """
        print("Inside save_channel_data_to_csv..")

        # name of the output file
        # removing special characters and whitespaces
        file_name = re.sub(r'[^a-zA-Z0-9 _]', '', file_name)
        filename = file_name.replace(' ', '_') + ".csv"

        try:
            with open(filename, 'w', newline='', encoding='utf8') as csv_file:
                fc = csv.DictWriter(csv_file, fieldnames=channel_data[0].keys())
                fc.writeheader()
                fc.writerows(channel_data)
            print(f"`{filename}` Saved Successfully.")
        except Exception as e:
            print(f"Error while Saving the File.\n{e}")

    # methods for scrapping of videos

    @staticmethod
    def get_page_source_videos(channel_link: str) -> str:
        """
        this method will return the html page of videos section of any YouTube channel

        :param channel_link: link of channel
        :return: html of '/videos' page
        """
        # url of channel's videos page
        videos_page_url = f'{channel_link}/videos'
        return YTScrapper.get_page_source(url=videos_page_url)

    @staticmethod
    def extract_video_title_url(page_source: str) -> list:
        """
        this method scraps title and url of all the videos

        :param page_source: page source as obtained from selenium driver
        :type: str

        :return: list of dicts {'title':'', 'url': '', 'views': '', 'uploaded_on': '', 'scrapped_on':''}
        containing video data
        :type: list
        """
        soup = BeautifulSoup(page_source, 'html.parser')

        current_time = datetime.datetime.now()
        items_div = soup.find('div', attrs={'class': 'style-scope ytd-grid-renderer', 'id': 'items'})
        videos = items_div.findChildren('ytd-grid-video-renderer', attrs={'class': 'style-scope ytd-grid-renderer'})
        print(f"{len(videos)} videos found.")

        videos_data = []
        for video in videos:
            title_a = video.findChild('a', attrs={'id': 'video-title'})
            views_upload = video.findChild('div', attrs={'id': 'metadata-line',
                                                         'class': 'style-scope ytd-grid-video-renderer'}).findChildren(
                'span')
            views = views_upload[0].contents[0]
            upload = views_upload[1].contents[0]
            data = {
                'video_title': title_a['title'],
                'video_url': f"https://www.youtube.com{title_a['href']}",
                'video_views': views,
                'video_uploaded_on': upload,
                'scrapped_on': f'{current_time}'
            }
            videos_data.append(data)

        return videos_data

    # methods for scraping of playlists

    @staticmethod
    def get_page_source_playlist(channel_link: str) -> str:
        """
        this method will return the html page of playlist section of any YouTube channel

        :param channel_link: link of channel
        :return: html of '/playlist' page
        """
        # url of channel's playlist page
        videos_page_url = f'{channel_link}/playlists'
        return YTScrapper.get_page_source(url=videos_page_url)

    @staticmethod
    def extract_playlist_title_url(page_source: str) -> list:
        """
        this method scraps title and url of all the playlists

        :param page_source: page source as obtained from selenium driver
        :type: str

        :return: list of dicts {'title':'', 'url': ''}
        containing playlist data

        :type: list
        """
        print("inside extract_playlist_title_url")
        soup = BeautifulSoup(page_source, 'html.parser')

        # access 'Created Playlists' Section
        items_div = soup.find('div',
                              attrs={'id': 'contents', 'class': 'style-scope ytd-section-list-renderer'}).findChild(
            'ytd-item-section-renderer',
            attrs={'class': 'style-scope ytd-section-list-renderer'}).findChild('div', attrs={'id': 'contents',
                                                                                              'class': 'style-scope '
                                                                                                       'ytd-item-section-renderer'}).find(
            'div', attrs={'id': 'items', 'class': 'style-scope ytd-grid-renderer'})

        # access all the playlists
        playlists = items_div.findChildren('ytd-grid-playlist-renderer')
        # print(f"{len(playlists)} playlist found.")

        playlist_data = []
        for playlist in playlists:
            title_a = playlist.findChild('a', attrs={'id': 'video-title'})
            url_a = playlist.findChild('yt-formatted-string', id='view-more').findChild('a')
            data = {
                'title': title_a['title'],
                'url': f"https://www.youtube.com{url_a['href']}",
            }
            playlist_data.append(data)

        return playlist_data

    @staticmethod
    def get_playlist_videos(playlist_url: str, playlist_title: str) -> list:
        """
        this method returns data of all the videos in a playlist

        :param playlist_url: url of playlist to be accessed
        :type: str

        :param playlist_title: title of playlist being accessed
        :type: str

        :return: data of videos in a playlist
        :type: list
        """

        # get html at `playlist_url`
        page_source = YTScrapper.get_page_source(url=playlist_url)

        # scrapping all the videos
        soup = BeautifulSoup(page_source, 'html.parser')

        videos_a = soup.find_all('a', attrs={'id': 'video-title'})

        final_video_data = []

        for video_a in videos_a:
            video = {
                'playlist_title': playlist_title,
                'video_title': video_a['title'],
                'video_url': f"https://www.youtube.com{video_a['href']}"
            }
            final_video_data.append(video)
        # print(final_video_data)

        return final_video_data

    # final high level methods

    @staticmethod
    def scrap_youtube_videos(channel_link: str):
        """
        This method scraps all the videos' data of any channel
        and save it to a csv file
        named `<channel_name>_videos.csv`

        :param channel_link: link of channel
        :type: str
        """
        print("inside scrap_youtube_videos")
        start = time.time()
        channel_link = channel_link.strip('/')

        # get channel name
        channel_name = YTScrapper.get_channel_name_from_url(channel_link=channel_link)
        file_name = channel_name + "_Videos"

        # scrap videos data
        page_source = YTScrapper.get_page_source_videos(channel_link=channel_link)
        videos_data = YTScrapper.extract_video_title_url(page_source=page_source)

        # save in the csv file
        YTScrapper.save_channel_data_to_csv(file_name=file_name, channel_data=videos_data)

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")

    @staticmethod
    def scrap_youtube_playlists(channel_link: str):
        """
        This method scraps all the playlist data of any channel
        and save it to a csv file
        named `<channel_name>_playlists.csv`

        :param channel_link: link of channel
        :type: str
        """
        print("inside scrap_youtube_playlist")
        start = time.time()
        channel_link = channel_link.strip('/')

        # get channel name
        channel_name = YTScrapper.get_channel_name_from_url(channel_link=channel_link)
        file_name = channel_name + "_playlists"

        # scrap playlist data
        page_source = YTScrapper.get_page_source_playlist(channel_link=channel_link)
        playlist_data = YTScrapper.extract_playlist_title_url(page_source=page_source)

        # scrap all the videos from individual playlists
        detailed_playlist_data = []

        for playlist in playlist_data:
            videos_data = YTScrapper.get_playlist_videos(playlist_url=playlist['url'], playlist_title=playlist['title'])
            detailed_playlist_data.extend(videos_data)

        # save in the csv file
        YTScrapper.save_channel_data_to_csv(file_name=file_name, channel_data=detailed_playlist_data)

        end = time.time()
        print(f"Time Elapsed: {round(end - start, 2)}s")


if __name__ == '__main__':
    # use this to scrap videos
    print("------- SCRAPPING VIDEO DATA ----")
    YTScrapper.scrap_youtube_videos(channel_link='https://www.youtube.com/channel/UCItJsxqZNWUyxFn-A2tzizQ')

    # use this to scrap playlists
    print("\n------- SCRAPPING PLAYLIST DATA ----")
    YTScrapper.scrap_youtube_playlists(
        channel_link='https://www.youtube.com/channel/UCItJsxqZNWUyxFn-A2tzizQ')
