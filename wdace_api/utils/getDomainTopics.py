import yake
import string
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import spacy
import lemminflect
from itertools import combinations

nlp = spacy.load("en_core_web_md")

def pre_process(titles):
    """
    Pre-processes titles by removing stopwords and lemmatizing text.
    :param titles: list of strings, contains target titles,.
    :return: preprocessed_title_docs, list containing pre-processed titles.
    """

    # Preprocess all the titles
    title_docs = [nlp(x) for x in titles]
    preprocessed_title_docs = []
    lemmatized_tokens = []
    for title_doc in title_docs:
        for token in title_doc:
            if not token.is_stop:
                lemmatized_tokens.append(token.lemma_)
        preprocessed_title_docs.append(" ".join(lemmatized_tokens))
        del lemmatized_tokens[
            :
            ]  # empty the lemmatized tokens list as the code moves onto a new title

    return preprocessed_title_docs

def similarity_filter(titles):
    """
    Recursively check if titles pass a similarity filter.
    :param titles: list of strings, contains titles.
    If the function finds titles that fail the similarity test, the above param will be the function output.
    :return: this method upon itself unless there are no similar titles; in that case the feed that was passed
    in is returned.
    """

    # Preprocess titles
    preprocessed_title_docs = pre_process(titles)
    # print(preprocessed_title_docs)
    # Remove similar titles
    all_summary_pairs = list(combinations(preprocessed_title_docs, 2))
    similar_titles = []
    for pair in all_summary_pairs:
        title1 = nlp(pair[0])
        title2 = nlp(pair[1])
        similarity = title1.similarity(title2)
        if similarity > 0.8:
            similar_titles.append(pair)

    titles_to_remove = []
    for a_title in similar_titles:
        # Get the index of the first title in the pair
        index_for_removal = preprocessed_title_docs.index(a_title[1])
        titles_to_remove.append(index_for_removal)

    # Get indices of similar titles and remove them
    similar_title_counts = set(titles_to_remove)
    similar_titles = [
        x[1] for x in enumerate(titles) if x[0] in similar_title_counts
    ]

    # Exit the recursion if there are no longer any similar titles
    if len(similar_title_counts) == 0:
        return titles

    # Continue the recursion if there are still titles to remove
    else:
        # Remove similar titles from the next input
        for title in similar_titles:
            idx = titles.index(title)
            titles.pop(idx)
            
        return similarity_filter(titles)


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