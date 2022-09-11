"""
This script contains scrapper for famous notes delivering website
`https://www.rgpvnotes.in/`, that was created by students of
IIST-Indore as a college project, and now it is helping lakhs of students
throughout the state.

These notes have helped me a lot during my college years and still
provides some amazing content.
However, I always find that using big websites is a tedious task
specially when you need to quickly access an information and go back to your work
as soon as possible (last moment studies before the exams :P).

Aim of this scrapper is to automate the process of searching the notes
and include the notes searching feature in my future projects as well
including the `college information chatbot` that I created for helping
the students of my college.
"""
import csv
import re
import time

import requests
from bs4 import BeautifulSoup


class RgpvNotesScrapper:

    @staticmethod
    def save_data_to_csv(file_name: str, data: list):
        """
        this is a generic method that saves data into a csv file
        `<file_name>.csv`
        :param file_name: name of output file
        :type: str
        :param data: data to be saved
        :type: list of dicts
        """
        print("Inside RgpvNotesScrapper.save_data_to_csv..")

        try:
            with open(file_name, 'w', newline='', encoding='utf8') as csv_file:
                fc = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                fc.writeheader()
                fc.writerows(data)
            print(f"`{file_name}` Saved Successfully.")
        except Exception as e:
            print(f"Error while Saving the File.\n{e}")


    @staticmethod
    def get_page_source(url: str) -> str:
        """
        this function returns page source of any url
        :param url: page to be fetched
        :type: str
        :return: page source of the url
        :type: str
        """
        print(f"inside RgpvNotesScrapper.get_page_source")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36'}
        resp = requests.get(url=url, headers=headers)
        if resp.status_code == 200:
            return resp.text
        return ""

    @staticmethod
    def get_year_wise_url(branch: str, year: int) -> str:
        """
        this method returns the url of a particular year of a branch
        this will help in scrapping that particular page only

        :param branch: branch to be searched
        :type: str

        :param year: year to be searched
        :type: int

        :return: url of that page
        :type: str
        """
        cse_notes_url = {
            2: 'https://www.rgpvnotes.in/btech/grading-system-old/notes/p/computer-science-2nd-year',
            3: 'https://www.rgpvnotes.in/btech/grading-system-old/notes/p/computer-science-3rd-year',
            4: 'https://www.rgpvnotes.in/be/cbgs/notes/p/computer-science-4th-year'
        }

        if branch == 'cse':
            return cse_notes_url[year]

    @staticmethod
    def rgpv_notes_search_branch_year(branch: str, year: int) -> list:
        """
        this method returns data of all the notes for a particular year and a particular branch
        :param branch: branch to be searched
        :type: str

        :param year: year to be searched
        :type: int

        :return: notes information (title and urls)
        :type: list of dicts | similar to json | helpful if we need to store the data in csv or other format
        """
        print(f"inside RgpvNotesScrapper.rgpv_notes_search_branch_year")
        start = time.time()

        # getting the `units` page for 4th yr

        rgpv_notes_search_url = RgpvNotesScrapper.get_year_wise_url(branch=branch, year=year)
        page_source = RgpvNotesScrapper.get_page_source(url=rgpv_notes_search_url)

        if len(page_source) == 0:
            end = time.time()
            print(f"Elapsed Time: {round(end - start, 2)}")
            return []

        soup = BeautifulSoup(page_source, 'html.parser')
        unit_boxes = soup.find_all('div', attrs={'class': 'unitbox'})

        subject_urls = []

        # fetching all the urls for all the subjects

        for unit_box in unit_boxes:
            subject_urls.append(f'https://www.rgpvnotes.in/be/cbgs/notes{unit_box.findChild("a")["href"][2:]}')

        # now scraping pages of all the subjects one by one for notes urls
        print()

        notes = []
        for subject_url in subject_urls:
            page_source = RgpvNotesScrapper.get_page_source(url=subject_url)
            soup = BeautifulSoup(page_source, 'html.parser')
            try:
                title = soup.find('h5', attrs={'class': 'tc-title tc-title-center'}).contents[0].strip('\n')
            except:
                # broken urls will generate errors
                # so ignore them
                continue
            units = soup.find('div', attrs={'class': 'separator'}).findChildren('ul', attrs={'class': 'text-left'})
            if len(units) <= 1:
                continue

            # accessing all the units one-by-one

            units = units[1]
            li = units.findChild('li')

            all_unit_tags = []

            unit_number = 1
            while unit_number <= 5:
                all_unit_tags.append(li)
                li = li.findNextSibling('li')
                unit_number += 1

            for unit in all_unit_tags:
                unit_no = unit.findChild('span', attrs={
                    'class': 'text-uppercase-maybe h5'}).findChild('b').contents[0][-1]
                links = unit.findChildren('span', attrs={'class': 'Tooltip-box'})[1].find_all('a')

                for link in links:
                    data = {'subject': title,
                            'unit': int(unit_no),
                            'url': link['href'],
                            'description': link.contents[0]}

                    notes.append(data)

        end = time.time()
        print(f"Returning {len(notes)} results.")
        print(f"Elapsed Time: {round(end - start, 2)}")
        return notes


if __name__ == '__main__':
    notes_data = RgpvNotesScrapper.rgpv_notes_search_branch_year(branch='cse', year=4)
    RgpvNotesScrapper.save_data_to_csv(file_name='4th_year_subjects_links_rgpv_notes.csv', data=notes_data)

# error ! working only for cse-4th year need to make it dynamic
