from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

import iso639
from langdetect import detect


from .utils.translate import detect_and_translate
from .utils.keywordExtractor import keyword_extractor
from .utils.getTitleTextSummary import getTitleTextSummary
from .utils.scrapeURL import getTextFromURL

# Create your views here.


class ClassifyAnalyseView(generics.GenericAPIView):

    def post(self, request):

        url = request.data.get('url')

        rawText = getTextFromURL(url)
        original_lang = iso639.to_name(detect(rawText))
        rawText = detect_and_translate(rawText, target_lang='en')
        

        title, mainText, extractive_summary = getTitleTextSummary(url)

        
        keywords = keyword_extractor(extractive_summary)


        title_len = len(title.split())
        mainText_len = len(mainText.split())
        extractive_summary_len = len(extractive_summary.split())
        rawText_len = len(rawText.split())



        return Response(
                        {
                            "len": {
                                "title_len": title_len, 
                                "mainText_len": mainText_len, 
                                "extractive_summary_len": extractive_summary_len, 
                                "rawText_len": rawText_len, 
                            },
                            "textual_data": {
                                "title": title,
                                "mainText": mainText,
                                "extractive_summary": extractive_summary,
                                "rawText": rawText,
                            },
                            "keywords": keywords,
                            "original_lang": original_lang
                        }, status=status.HTTP_201_CREATED)




class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)