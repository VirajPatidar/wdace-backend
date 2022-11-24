import pickle
import pandas as pd
from gensim.utils import simple_preprocess
from gensim.models.doc2vec import TaggedDocument
from gensim.parsing.preprocessing import strip_tags

# Open the file in binary mode
with open('./wdace_api/utils/lbl2vec_model.pkl', 'rb') as f:
	lbl2vec_model = pickle.load(f)

def tokenize(doc):
    return simple_preprocess(strip_tags(doc), deacc=True, min_len=2, max_len=15)

# 'https://www.ibm.com/cloud/learn/convolutional-neural-networks'
def getDomain(title, mainText):
	tagged_doc = TaggedDocument(tokenize(title + '. ' + mainText), [str('0')])

	lbl2vec_similarity = lbl2vec_model.predict_new_docs(tagged_docs=pd.Series([tagged_doc]))

	return str(lbl2vec_similarity['most_similar_label'][0]), float(lbl2vec_similarity['highest_similarity_score'][0])
