import random
import pickle
import pandas as pd
from gensim.utils import simple_preprocess
from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import strip_tags
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from bs4.element import Comment
import re

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

# Open the file in binary mode
with open('lbl2vec_model.pkl', 'rb') as f:
	lbl2vec_model = pickle.load(f)

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

		return title, res

	except Exception as e:
		print(e)
		return(str(e))

def tokenize(doc):
    return simple_preprocess(strip_tags(doc), deacc=True, min_len=2, max_len=15)

# 'https://www.ibm.com/cloud/learn/convolutional-neural-networks'
def getDomain(url):

	title, desc = getTextFromURL(url)

	tagged_doc = TaggedDocument(tokenize(title + '. ' + desc), [str('0')])

	lbl2vec_similarity = lbl2vec_model.predict_new_docs(tagged_docs=pd.Series([tagged_doc]))

	return str(lbl2vec_similarity['most_similar_label']), float(lbl2vec_similarity['highest_similarity_score'])
