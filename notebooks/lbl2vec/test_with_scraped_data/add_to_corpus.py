import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning 
import os
import pandas as pd

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
				'br', 'input', 'script', 'wbr', 'video', 'param', 'hr']
				
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
		title = soup.title.string

		text_from_html = ''

		visible_texts = filter(tag_visible, text)  
		text_from_html = " ".join(t.strip() for t in visible_texts)

		text_from_html = text_from_html.strip()

		text_from_html = re.sub('\n', ' ', text_from_html)
		res = re.sub(' +', ' ', text_from_html)

		return (title, res)

	except Exception as e:
		print(e)
		return(str(e))

# os.chdir("scraped_articles")



urls = [
	# whats DL
	# (3, "https://www.ibm.com/in-en/cloud/learn/deep-learning"),
	# (3, "https://machinelearningmastery.com/what-is-deep-learning/"),
	# (3, "https://www.analyticsvidhya.com/blog/2018/10/introduction-neural-networks-deep-learning/"),
	# CNN LSTM
	(3, "https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53"),
	(3, "https://www.ibm.com/cloud/learn/convolutional-neural-networks"),
	(3, "https://machinelearningmastery.com/gentle-introduction-long-short-term-memory-networks-experts/"),
	# # applications
	# (3, "https://www.analyticssteps.com/blogs/8-applications-neural-networks"),
	# (3, "https://www.tutorialspoint.com/artificial_neural_network/artificial_neural_network_applications.htm"),
]



class_index = []
title = []
text = []

for url in urls:
	class_index.append(url[0])
	fin = getTextFromURL(url[1])
	title.append(fin[0])
	text.append(fin[1])

# print(getTextFromURL("https://medium.com/analytics-vidhya/topic-modelling-using-lda-aa11ec9bec13"))
df = pd.DataFrame({
	'class': class_index,
	'title': title,
	'text': text
})

os.chdir("data")
print(f"Current directory: {os.getcwd()}")

if not os.path.isfile('scraped_urls_corpus.csv'):
	df.to_csv('scraped_urls_corpus.csv', header=False, index=False)
else:
	old_df = pd.read_csv('scraped_urls_corpus.csv', names=['class', 'title', 'text'], header=None)
	new_df = pd.concat([old_df, df], ignore_index=True)
	new_df.reset_index()
	new_df.to_csv('scraped_urls_corpus.csv', header=False, index=False)
