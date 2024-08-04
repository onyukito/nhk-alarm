from pyPodcastParser.Podcast import Podcast
import requests
import os
import time
from datetime import datetime


def get_list():
    while True:
        try:
            response = requests.get(
                'https://www.nhk.or.jp/s-media/news/podcast/list/v1/all.xml')
            podcast = Podcast(response.content)
            break
        except:
            print('failed to get podcast info, retry in 5 mins...')
            time.sleep(60)
    
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
            os.system('ffplay nhk.mp3')

if __name__ == "__main__":
    while True:
        curr_time = datetime.now().strftime("%H:%M")
        print('Current time: ', curr_time)
        if curr_time == '07:10':
            main()
        time.sleep(60)