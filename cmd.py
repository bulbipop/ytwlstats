from bs4 import BeautifulSoup as bs
from datetime import timedelta
import requests
import browser_cookie3

import db

def req(url, cookie_jar):
    print('Downloading ' + url)
    return requests.get(url, cookies=cookie_jar)

def calcLength(length, speeds=[1, 1.5, 2, 3]):
    ''' Generator to calculate length at different speeds '''
    for speed in speeds:
        new_len = length / speed
        ms = new_len.microseconds
        new_len -= timedelta(microseconds=ms) # rounds to second
        yield new_len, speed

def getLengthfromPage():
    ''' return number of videos and sum of all lengths '''
    root = 'https://www.youtube.com'
    cj = browser_cookie3.chrome(domain_name='youtube.com')
    url =  root + '/playlist?list=WL'
    html = req(url, cj).text
    button = bs(html, 'html.parser').find(class_='load-more-button')

    while button:
        url = root + button['data-uix-load-more-href']
        ajax = req(url, cj).json()
        html += ajax['content_html']
        button = bs(ajax['load_more_widget_html'], 'html.parser').button
    # if polymer:                       # first result is blank
    #length = bs(html, 'html.parser').find_all(id='length')[1:]
    length = bs(html, 'html.parser').find_all(class_='timestamp')

    total = timedelta()
    for time in length:
        *h, m, s = list(map(int, time.text.split(':')))
        total += timedelta(hours=next(iter(h), 0), minutes=m, seconds=s)
    print('Finished')
    return len(length), total

def main():
    nb_videos, length = getLengthfromPage()
    db.insertDB(nb_videos, length)
    return nb_videos, length


if __name__ == '__main__':
    nb_videos, length = main()
    print('{} videos for a total length of:'.format(nb_videos))
    for new_len, speed in calcLength(length):
        print('{} at {}x'.format(new_len, speed))
