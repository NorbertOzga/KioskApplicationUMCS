from bs4 import BeautifulSoup
import json
from flask import Response
from requests import get
from ..extensions import cache


def get_color(string):
    colors = {
        'student': '#4bbe9d',
        'lublin': '#dc462d',
        'tv umcs': '#f38200',
        'biznes': '#6b08ff',
        'pracownik': '#337b93',
        'absolwent': '#60baf6',
        'kandydat': '#ff6600',
    }
    try:
        picked = colors[string.lower()]
        return picked
    except:
        return '#9399a5'


class Events:
    def __init__(self, cache_module=cache):
        self.cache_module = cache_module

    def subscrape(self, url):
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        everything = soup.find('div', class_='paginate-content')

        return everything

    def subscrape_fixed(self, url):
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        everything = soup.find('div', class_='paginate-content')
        intro_text = everything.find('p')
        intro_text = intro_text.text.replace('\n', '').strip()

        if intro_text == "":
            intro_text = everything.find('div', class_='jRelatedPhotos').find('p')
            intro_text = intro_text.text.replace('\n', '').strip()

        return intro_text

    def get_events(self):
        url = 'http://www.umcs.pl'
        response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_events = soup.find_all('a', class_='box-news')

        fail_flag = False
        item_list = []

        for item in all_events:
            event_name = item.find('h4', class_='title')
            event_name = event_name.text.replace('\n', '').strip()
                    
            date = item.find('div', class_='label-meta')
            date = date.text.replace('\n', '').strip()
            
            event_type = item.find('em', class_='label-area-A')
            event_type = event_type.text.replace('\n', '').strip()

            photo_link = item.find('img', class_='img')['src']

            color = get_color(event_type)

            sub_url = item['href']
            sub_url = url + sub_url
            raw = str(self.subscrape(sub_url))
            fixed = self.subscrape_fixed(sub_url)

            # check for fails in scraping
            if (
                    (event_name == "")
                    or (date == "")
                    or (event_type == "")
                    or (color == "")
            ):
                fail_flag = True

            # serialize data to JSON format
            if not fail_flag:
                item_list.append({
                    'name': event_name,
                    'date': date,
                    'type': event_type,
                    'color': color,
                    'photo_link': photo_link,
                    'text': fixed
                })

        data = {
            'payload': item_list
        }

        self.cache_module.set("events", str(data))
