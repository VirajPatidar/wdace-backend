import re
from langdetect import detect
from googletrans import Translator


def preProcessForTranslation(text):
    # removing english words
    txt_list = list(text.split(" "))
    txt = list(filter(lambda ele: re.search("[a-zA-Z\s]+", ele) is None, txt_list))
    text = ' '.join([str(elem) for elem in txt])

    return str(text.strip())



def detect_and_translate(text, target_lang):
    
    result_lang = detect(text)
    # print(result_lang)
    
    if result_lang == target_lang:
        return text 
    
    else:
        translator= Translator()
        text = preProcessForTranslation(text)
        translation = translator.translate(text, src=result_lang, dest=target_lang)
        return translation.text