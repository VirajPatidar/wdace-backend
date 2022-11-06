import yake
import string
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy



def getDomainTopics(text):
    
    # PREPROCESSING
    # 1. Remove punctuation
    # 2. Remove digits
    # 3. Convert to lowercase
    # 4. Remove stop words


    def remove_punctuation(text):
        punctuationfree="".join([i for i in text if i not in string.punctuation])
        return punctuationfree

    text=remove_punctuation(text)
    text = text.lower()
    text = ''.join([i for i in text if not i.isdigit()])
    text=" ".join(text.split())





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


    for kw, v in keywords:
        if(100-v > 99.999):
          words = kw.split()
          keyw = " ".join(sorted(set(words), key=words.index))
          print("Keyphrase: ",keyw, ": score", 100-v)


    domain = keywords[0]
    topics = list(map(list, zip(*keywords[1:])))

    return domain, topics

