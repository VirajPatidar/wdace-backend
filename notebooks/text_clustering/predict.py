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
	classes = {0: "Science & Tech", 1: "World", 2: "Sports", 3: "Business"}
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

# inp_text = '''Amazon has been one of the few companies to experience growth during the pandemic, and this hiring spree is a sign that the company is committed to continuing that trend. The new hires will join Amazon's existing workforce of more than 800,000 employees in North America.'''

# inp_text = '''
# In a highly anticipated football match, the two teams clashed on the pitch in front of a packed stadium. The game got off to a tense start, with both sides evenly matched and determined to take control of the ball.

# As the first half progressed, the home team began to find their rhythm, dominating possession and creating several dangerous opportunities. However, the visiting team's defense held strong, thwarting their opponents' attempts to score.

# In the second half, the away team started to push forward more aggressively, launching several counterattacks and putting the home team under pressure. But the home team's defense remained solid, and they managed to weather the storm.

# Finally, in the dying minutes of the game, the home team broke through the visiting team's defense with a well-placed shot that found the back of the net. The crowd erupted in cheers as the home team celebrated their hard-fought victory.

# Overall, it was a thrilling match that showcased the skill and determination of both teams. But in the end, it was the home team who emerged victorious, much to the delight of their fans.
# '''

# inp_text = '''
# India, one of the world's largest democracies, is currently undergoing significant reforms in its political landscape. The country has seen major changes in recent years, ranging from the introduction of new policies to the emergence of new political parties and leaders.

# One of the most significant reforms has been the implementation of the Goods and Services Tax (GST), which has streamlined the country's complex tax system and created a common market for goods and services. The government has also introduced reforms in the agricultural sector, including the passage of new laws aimed at modernizing the industry and providing greater market access for farmers.

# The Indian political scene has also seen the rise of new political parties and leaders, with the Aam Aadmi Party (AAP) gaining significant support in recent years. The party has focused on anti-corruption measures and public service delivery, and has been successful in winning several state elections.

# In addition, there have been efforts to increase the representation of women in politics, with the government introducing a bill to reserve 33% of seats in parliament and state assemblies for women.

# Overall, these reforms are aimed at modernizing India's political system, promoting economic growth, and ensuring greater accountability and transparency in governance. While there are still challenges and obstacles to be overcome, the country's political landscape is evolving rapidly, offering hope for a brighter future.
# '''

inp_text = '''
starting likehangs headthe justin timberlake song rock body like first sounded boring redundantbut make want dancei know whyyyyyyyi wanna dance hear choreograph something maybe kind subliminal msg like songdance really hormonal right nowi feel like like celeb guy like hotanyway yeah guy happen bump justin timberlake send
'''

print(predict(inp_text))


# other_texts = [
#     ['computer', 'time', 'graph', 'microsoft', 'system', 'technology'],
#     ['game', 'point', 'year', 'coach', 'season', 'team'],
#     ['president', 'government', 'computer', 'leader', 'world', 'country'],
#     ['company', 'stock', 'target', 'million', 'billion']
# ]

# '''
# 0 - science and tech
# 1 - world
# 2 - sports
# 3 - business
# '''

# other_corpus = [dictionary.doc2bow(text) for text in other_texts]

# unseen_doc = other_corpus[0]
# vector = topics_model[unseen_doc]  # get topic probability distribution for a document
# print(vector)

# unseen_doc = other_corpus[1]
# vector = topics_model[unseen_doc]  # get topic probability distribution for a document
# print(vector)

# unseen_doc = other_corpus[2]
# vector = topics_model[unseen_doc]  # get topic probability distribution for a document
# print(vector)

# unseen_doc = other_corpus[3]
# vector = topics_model[unseen_doc]  # get topic probability distribution for a document
# print(vector)
