import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import csv
import cssutils # type: ignore

# https://t.me/tikvahethiopia/74220

post_no = "74176"
channel = 'tikvahethiopia'
productslist = []


def get_data():
    url = f'https://t.me/{channel}/{post_no}?embed=1&mode=tme'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    for_img_vid = soup.find_all(
        'a', {'class': 'tgme_widget_message_photo_wrap'})

    vid_link = soup.find_all('video', {'class': 'tgme_widget_message_video'})

    content = soup.find(
        'div', class_='tgme_widget_message_text js-message_text')

    content = content if content else 'No content'

    img_list = []
    vid_list = []
    tag = []


    if len(for_img_vid) > 0:
        for item in for_img_vid:
            img = item['style']
            style = cssutils.parseStyle(img)
            imglist = style['background-image']
            imglist = imglist.replace('url(', '').replace(')', '')
            img_list.append(imglist)
        img_list = ', \n'.join(img_list)
    else:
        img_list = 'No image'


    if len(vid_link) > 0:
        for item in vid_link:
            vid = item['src']
            vid_list.append(vid)
        vid_list = ', \n'.join(vid_list)
    else:
        vid_list = 'No video'


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
        tittle1 = content.get_text('\n').split('\n')[1]
    else:
        tittle1 = content.get_text('\n').split('\n')[0]

    posted_on = soup.find('time', class_='datetime')
    posted_on = posted_on.get_text('\n').join(' \n') # type: ignore
    views_no = soup.find('span', class_='tgme_widget_message_views')
    views_no = views_no.get_text('\n').join(' \n')  # type: ignore
    

    product = {
        'TAG': tag,
        'title': tittle1,
        'content': content.get_text('\n'),  # type: ignore
        'link': img_list,
        'vid': vid_list,
        'posted_on': posted_on,
        'views': views_no,
    }

    productslist.append(product)
    return productslist


def output(productslist):
    with open('output.csv', 'a') as csvfile:
        fieldnames = ['TAG', 'title', 'content', 'link', 'vid', 'posted_on', 'views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(productslist)
        print('Saved to txt file')


old_string = ['","', '",', ',"']


def inplace_change(filename, old_string, new_string):
    with open(filename) as f:
        s = f.read()

    # Safely write the changed content, if found in the file
    for old_string in old_string:
        with open(filename, 'w') as f:
            s = s.replace(old_string, new_string)
            f.write(s)


soup1 = get_data()
output(soup1)
inplace_change('output.txt', old_string, '\n \n')
