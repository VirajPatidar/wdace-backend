import string
import re
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

with open('./saved_files/topics.pickle', 'rb') as f:
    topics_model = pickle.load(f)

with open('./saved_files/dictionary.pickle', 'rb') as f:
    dictionary = pickle.load(f)

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

def text_to_bow(cleaned_inp_text):
	cleaned_inp_text = clean_text(inp_text)
	lemmatizer = WordNetLemmatizer()
	lemmatized_words = []
	for word in cleaned_inp_text.split():
		if("reuter" not in word):
			lemmatized_word = lemmatizer.lemmatize(word)
			if(len(lemmatized_word) > 2 and lemmatized_word not in stopwords.words('english')):
				lemmatized_words.append(lemmatized_word)
	bow_text = dictionary.doc2bow(lemmatized_words)
	return bow_text

def get_class(bow_text):
	classes = {0: "World", 1: "Sports", 2: "Science & Tech", 3: "Business"}
	vector = topics_model[bow_text]
	maxi = 0; maxs = 0
	for i, s in vector:	# index, score
		print(str(i) + "\t" + str(s))
		if s > maxs:
			maxs = s; maxi = i
	return classes[maxi]

def predict(text):
	cleaned_text = clean_text(text)
	bow_text = text_to_bow(cleaned_text)
	text_class = get_class(bow_text)
	return text_class

# inp_text = '''Amazon has announced that it will be hiring 75,000 new employees across its fulfillment and transportation networks in the United States and Canada. The new hires will work in various roles, including pickers, packers, and drivers, and will receive an average starting wage of $17 per hour, along with signing bonuses of up to $1,000. This move comes as the company continues to experience high demand for its products and services, and seeks to improve its delivery times and customer experience. Amazon has been one of the few companies to experience growth during the pandemic, and this hiring spree is a sign that the company is committed to continuing that trend. The new hires will join Amazon's existing workforce of more than 800,000 employees in North America.'''
inp_text = '''Amazon has been one of the few companies to experience growth during the pandemic, and this hiring spree is a sign that the company is committed to continuing that trend. The new hires will join Amazon's existing workforce of more than 800,000 employees in North America.'''

print(predict(inp_text))
