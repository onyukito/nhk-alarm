from pyPodcastParser.Podcast import Podcast
import requests
import pickle
import os
import time
from datetime import datetime
from playsound import playsound


LIST_FILE = "existing_list.pickle"


def get_list():
    while True:
        try:
            response = requests.get(
                'https://www.nhk.or.jp/s-media/news/podcast/list/v1/all.xml')
            podcast = Podcast(response.content)
            break
        except:
            print('failed to get podcast info, retry in 5 mins...')
            time.sleep(300)
    
    all_items = {}
    for item in podcast.items:
        all_items[item.title] = item.enclosure_url
    return all_items


def main():
    new_items = get_list()
    for title, link in new_items.items():
        if '午前７' in title:
            print(title)
            filename = os.path.basename(os.path.splitext(link)[0])
            cmd = "wget {0}".format(link)
            os.system(cmd)
            os.system("mv '{0}'.mp3 nhk.mp3".format(filename))
            playsound('nhk.mp3')

if __name__ == "__main__":
    while True:
        main()
        print('Current Time =', datetime.now().strftime("%H:%M:%S"))
        # print('Wait for 300\n')
        # time.sleep(300)