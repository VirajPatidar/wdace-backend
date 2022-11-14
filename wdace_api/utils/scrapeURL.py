import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning 

from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Comment

import numpy as np
import re
import string

# Disable displaying SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})



# Helper function to filter out futile HTML tags
def tag_visible(element):
    blacklist = ['style', 'label', '[document]', 'embed', 'img', 'object',
              'noscript', 'header', 'html', 'iframe', 'audio', 'picture',
              'meta', 'title', 'aside', 'footer', 'svg', 'base', 'figure',
              'form', 'nav', 'head', 'link', 'button', 'source', 'canvas',
              'br', 'input', 'script', 'wbr', 'video', 'param', 'hr', 'li', 'ol', 'ul', 'table', 'th', 'tr', 'td', 'a', 'button', 'span']
                
    if element.parent.name in blacklist:
        return False
    if isinstance(element, Comment):
        return False
    return True



def getTextFromURL(url):
    try:
        page = requests.get(url, headers=HEADERS)          #to extract page from website
        html_code = page.content                           #to extract html code from page

        soup = BeautifulSoup(html_code, 'html.parser')     #Parse html code
        text = soup.findAll(text=True)                     #find all text

        text_from_html = ''

        visible_texts = filter(tag_visible, text)  
        text_from_html = " ".join(t.strip() for t in visible_texts)

        text_from_html = text_from_html.strip()

        text_from_html = re.sub('\n', ' ', text_from_html)
        res = re.sub(' +', ' ', text_from_html)

        return res

    except Exception as e:
        print(e)
        return(str(e))

