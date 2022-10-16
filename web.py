from os import mkdir
import os
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import csv
import cssutils  # type: ignore
import sys


channel = sys.argv[1]
post_no = sys.argv[2]

def get_data(channel, post_no):
    url = f'https://t.me/{channel}/{post_no}?embed=1&mode=tme'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for_img = soup.find_all(
        'a', {'class': 'tgme_widget_message_photo_wrap'})

    vid_link = soup.find_all('video', {'class': 'tgme_widget_message_video'})

    content = soup.find(
        'div', class_='tgme_widget_message_text js-message_text')

    content = content if content else 'No content'

    productslist = []
    img_list = []
    vid_list = []
    tag = []

    mkdir('media') if not os.path.exists('media') else None
    os.chdir('media')
    os.mkdir(f'img_{post_no}') if not os.path.exists(f'img_{post_no}') else None
    os.chdir(f'img_{post_no}')

    if len(for_img) > 0:
        for item in for_img:
            img = item['style']
            style = cssutils.parseStyle(img)
            imglist = style['background-image']
            imglist = imglist.replace('url(', '').replace(')', '')
            for i in range(len(img_list)):
                img = requests.get(img_list[i])
                with open(f'img{post_no}_{i}.jpg', 'wb') as f:
                    f.write(img.content)
            img_list.append(imglist)
        img_list = ', \n'.join(img_list)
    else:
        img_list = 'No image'

    os.chdir('..')
    os.mkdir(f'vid_{post_no}') if not os.path.exists(f'vid_{post_no}') else None
   
    os.chdir(f'vid_{post_no}')


    if len(vid_link) > 0:
        for item in vid_link:
            vid = item['src']
            for i in range(len(vid_list)):
                vid = requests.get(vid_list[i])
                with open(f'vid{post_no}_{i}.mp4', 'wb') as f:
                    f.write(vid.content)
            vid_list.append(vid)
        vid_list = ', \n'.join(vid_list)
    else:
        vid_list = 'No video'

    os.chdir('..')

    title = content.get_text('\n')  # type: ignore

    print()

    if title.find('#') != -1:
        n = title.find('#')
        tag = title[n:]

    for i in range(len(title)):
        if title[i] == '#':
            for j in range(len(title[i:])):
                if title[i+j] == '\n':
                    tag = title[i:i+j]
                    break

            break
        else:
            tag = 'No tag'

    if tag != 'No tag':
        tittle1 = content.get_text('\n').split('\n')[1]  # type: ignore
    else:
        tittle1 = content.get_text('\n').split('\n')[0]  # type: ignore

    posted_on = soup.find('time', class_='datetime')
    posted_on = posted_on.get_text('\n') # type: ignore
    views_no = soup.find('span', class_='tgme_widget_message_views')
    views_no = views_no.get_text('\n')  # type: ignore

    product = {
        'TAG': tag.join(" \n"),  # type: ignore
        'title': tittle1.join(" \n"),
        'content': content.get_text('\n').join(" \n"),  # type: ignore
        'link': img_list.join(" \n"),
        'vid': vid_list.join(" \n"),
        'posted_on': posted_on.join(" \n"),
        'views': views_no.join(" \n"),
    }

    productslist.append(product)
    os.chdir('..')
    return productslist


def output(productslist):
    with open('output.csv', 'a') as csvfile:
        fieldnames = ['TAG', 'title', 'content',
                     'link', 'vid', 'posted_on', 'views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(productslist)
        print('Saved to txt file')


old_string = ['""']


def inplace_change(filename, old_string, new_string):
    with open(filename) as f:
        d = f.read()
    
    # Safely write the changed content, if found in the file
    for old_string in old_string:
        with open(filename, 'w') as f:
            d = d.replace(old_string, new_string)
            f.write(d)


try:
    soup1 = get_data(channel, post_no)
    output(soup1)
    inplace_change('output.csv', old_string, '"')
except KeyboardInterrupt:
    print('No internet connection')