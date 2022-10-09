import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import csv

# https://t.me/tikvahethiopia/74224

post_no = "74224"
channel = 'tikvahethiopia'
productslist = []


def get_data():
    url = f'https://t.me/{channel}/{post_no}?embed=1&mode=tme'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for_img_vid = soup.find_all(
        'div', {'class': 'tgme_widget_message_grouped_layer js-message_grouped_layer'})
    
    content = soup.find(
        'div', class_='tgme_widget_message_text js-message_text')

    content = content if content else 'No content'

    img_list = []
    vid_list = []
    tag = []

    for item in for_img_vid:

        img = item.find(
            'a', {'class': 'tgme_widget_message_photo_wrap'})['href']
        vid = item.find(
            'a', {'class': 'tgme_widget_message_video_player'})

        img_list = img + '\n'
        vid_list = vid['href'] + '\n' if vid else ''

        if img == None:  # if these are none just skip them.
            print('No image')
            continue
        if vid == None:
            vid_list = 'No video'
            print('No video')
            continue

    title = content.get_text('\n')  # type: ignore
    
    ''''
    this print the title unitl it finds a new line
    '''
    for i in range(len(title)):
        if title[i] == '#':
            for j in range(len(title[i:])):
                if title[i+j] == '\n':
                    tag = title[i:i+j] + ' '
                    break
            break
    
    

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

    product = {
        'TAG': tag,
        'title': title,  # type: ignore
        'content': content.get_text('\n'),  # type: ignore
        'link': img_list,
        'vid': vid_list,
    }

    productslist.append(product)
    return productslist


def output(productslist):
    with open('output.txt', 'w') as csvfile:
        fieldnames = ['TAG', 'title', 'content', 'link', 'vid']
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
