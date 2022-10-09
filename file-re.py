from re import I
from bs4 import BeautifulSoup
import requests
import pandas as pd

post_no = "74185"   
channel = 'tikvahethiopia'
# 74058

def get_data():
    productslist = []
    imglist = []
    url = f'https://t.me/{channel}/{post_no}?embed=1&mode=tme'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    content = soup.find(
        'div', class_='tgme_widget_message_text js-message_text')
    imgfil = soup.find(
        'div', class_="tgme_widget_message_grouped_layer js-message_grouped_layer")
    for img in imgfil.find_all('a'): # type: ignore
        imglist += img['href'] + '\n'

    product = {
                'content': content.text, # type: ignore
                'imgurl': imglist,
             }
    productslist.append(product)
    return productslist


def output(productslist):
    productsdf = pd.DataFrame(productslist)
    productsdf.to_csv('outputfile.txt', index=False)
    print('Saved to txt file')

old_string = [",", "'", " "]

def inplace_change(filename, old_string, new_string):
    with open(filename) as f:
        s = f.read()

    # Safely write the changed content, if found in the file
    for old_string in old_string:
        with open(filename, 'w') as f:
            s = s.replace(old_string, new_string)
            f.write(s)


soup = get_data()
output(soup)
inplace_change('outputfile.txt', old_string , '')