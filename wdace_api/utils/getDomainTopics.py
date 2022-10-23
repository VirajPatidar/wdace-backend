import yake


def getDomainTopics(text):
    
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

    # for kw, v in keywords:
    #     print("Keyphrase: ",kw, ": score", v)

    domain = keywords[0]
    topics = list(map(list, zip(*keywords[1:])))

    return domain, topics

