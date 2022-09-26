from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

import iso639
from langdetect import detect


from .utils.translate import detect_and_translate
from .utils.extractive_summariser import extractive_summariser
from .utils.keyword_extractor import keyword_extractor
from .utils.scrape_url import getTextFromURL

# Create your views here.


class ClassifyAnalyseView(generics.GenericAPIView):

    def post(self, request):

        url = request.data.get('url')
        text = getTextFromURL(url)

        original_lang = iso639.to_name(detect(text))
        translated_text = detect_and_translate(text, target_lang='en')
        
        keywords = []

        if(translated_text == ""):
            extractive_summary = extractive_summariser(text)
            keywords = keyword_extractor(text)
            translated_text_len = 0
        else:
            extractive_summary = extractive_summariser(translated_text)
            keywords = keyword_extractor(translated_text)
            translated_text_len = len(translated_text.split())


        text_len = len(text.split())
        extractive_summary_len = len(extractive_summary.split())


        return Response(
                        {
                            "len": {
                                "text_len": text_len,
                                "translated_text_len": translated_text_len,
                                "extractive_summary_len": extractive_summary_len,
                            },
                            "text": {
                                "text": text,
                                "translated_text": translated_text,
                                "extractive_summary": extractive_summary,
                            },
                            "keywords": keywords,
                            "original_lang": original_lang
                        }, status=status.HTTP_201_CREATED)




class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)