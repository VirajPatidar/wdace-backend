import yake
import string
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import lemminflect



def getDomainTopics(text):
    
    # PREPROCESSING
    # 1. Remove punctuation
    # 2. Remove digits
    # 3. Convert to lowercase
    # 4. Remove stop words
    # 5. Lemmatization


    def remove_punctuation(text):
        punctuationfree="".join([i for i in text if i not in string.punctuation])
        return punctuationfree

    text=remove_punctuation(text)
    text = text.lower()
    text = ''.join([i for i in text if not i.isdigit()])
    text=" ".join(text.split())


    # filtered_list = []
    # stop_words = nltk.corpus.stopwords.words('english')
    # words = word_tokenize(text)
    # for w in words:
    #     if w.lower() not in stop_words:
    #         filtered_list.append(w)
            
    # text = " ".join(filtered_list)


    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    lemmatised=[]

    for item in doc:
        item = item._.lemma()
        lemmatised.append(item)

    text=" ".join(lemmatised)


    # YAKE
    # optimise parameters to get best results
    language = "en"
    max_ngram_size = 2
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 10

    kw_extractor = yake.KeywordExtractor(lan=language, 
                                        n=max_ngram_size, 
                                        dedupLim=deduplication_thresold, 
                                        dedupFunc=deduplication_algo, 
                                        windowsSize=windowSize, 
                                        top=numOfKeywords)
                                                

    keywords = kw_extractor.extract_keywords(text)

    topics = []

    for kw, v in keywords:
        if(100-v > 99.999):
          words = kw.split()
          keyw = " ".join(sorted(set(words), key=words.index))
          topics.append(keyw)
        #   print("Keyphrase: ",keyw, ": score", 100-v)


    domain = keywords[0][0]
    topics = topics[1:]

    return domain, topics

