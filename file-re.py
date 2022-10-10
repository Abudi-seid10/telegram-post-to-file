from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import cssutils # type: ignore
import pandas as pd # type: ignore

post_no = "74202"   
channel = 'tikvahethiopia'
# 74058

def get_data():
    productslist = []
    imglist = []
    vidlist = []
    url = f'https://t.me/{channel}/{post_no}?embed=1&mode=tme'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    div = soup.find_all('div', {'class': 'tgme_widget_message_grouped_layer js-message_grouped_layer'})
    div_text = soup.find_all('div', {'class': 'tgme_widget_message_text js-message_text'})
    
    for item in div:
        if item.find('a', {'class': 'tgme_widget_message_photo_wrap'}):
            img = item.find('a', {'class': 'tgme_widget_message_photo_wrap'})['style']
            style = cssutils.parseStyle(img)
            imglist = style['background-image']
            imglist = imglist.replace('url(', '').replace(')', '')
            
        
        if item.find('video', {'class': 'tgme_widget_message_video'}):
            vid = item.find('video', {'class': 'tgme_widget_message_video'})['src']
            vidlist.append(vid).join(', ')
            
    
    
    
    
    
    # content = soup.find(
    #     'div', class_='tgme_widget_message_text js-message_text')
    # imgfil = soup.find(
    #     'div', class_="tgme_widget_message_grouped_layer js-message_grouped_layer")
    # for img in imgfil.find_all('a'): # type: ignore
    #     imglist += img['href'] + '\n'

    product = {
                #'content': content.text, # type: ignore
                'imgurl': imglist,
             }
    productslist.append(product)
    return productslist


def output(productslist):
    productsdf = pd.DataFrame(productslist)
    productsdf.to_csv('outputfilefile.txt', index=False)
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
# inplace_change('outputfile.txt', old_string , '')