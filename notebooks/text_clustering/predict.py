import string
import re
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def remove_punctuation_digits(text):
	punctuationfree = "".join([i for i in text if i not in string.punctuation and not i.isdigit()])
	return punctuationfree

def remove_stopwords(text):
	text = " ".join([i for i in text.split() if len(i) > 2 and i not in stopwords.words('english')])
	return text

def clean_text(text):
	text = text.replace("/", " ")
	text = text.replace("\\", " ")
	text = remove_stopwords(text)
	text = remove_punctuation_digits(text)
	text = text.lower()
	text = re.sub(' +', ' ', text)
	return text


with open('./saved_files/topics.pickle', 'rb') as f:
    topics_model = pickle.load(f)

with open('./saved_files/dictionary.pickle', 'rb') as f:
    dictionary = pickle.load(f)

other_texts = [
    ['computer', 'time', 'graph', 'microsoft', 'system', 'technology'],
    ['game', 'point', 'year', 'coach', 'season', 'team'],
    ['president', 'government', 'computer', 'leader', 'world', 'country'],
    ['company', 'stock', 'target', 'million', 'billion']
]

other_corpus = [dictionary.doc2bow(text) for text in other_texts]
unseen_doc = other_corpus[1]
print(unseen_doc)
vector = topics_model[unseen_doc]  # get topic probability distribution for a document
print(vector)
