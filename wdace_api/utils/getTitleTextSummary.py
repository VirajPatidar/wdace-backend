import re
import string
from readability import Document
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
import iso639
from langdetect import detect


from .extractiveSummariser import extractive_summariser
from .translate import detect_and_translate



# Disable displaying SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})



def getTitleTextSummary(url):
    
    response = requests.get(url, headers=HEADERS)

    doc = Document(response.text)

    title = doc.title()
    raw_html = doc.summary()

    original_lang = iso639.to_name(detect(raw_html))


    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 
    cleantext = re.sub(CLEANR, '', raw_html)
    cleantext2 = re.sub('\n', ' ', cleantext)
    mainText = re.sub(' +', ' ', cleantext2)
    mainText = mainText[:-1]
    mainText.strip()


    if original_lang != 'English':
        title = detect_and_translate(title, target_lang='en')
        mainText = detect_and_translate(mainText, target_lang='en')

    extractive_summary = extractive_summariser(mainText)

    return title, mainText, extractive_summary