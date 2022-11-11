from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

import iso639
from langdetect import detect


from .utils.translate import detect_and_translate
from .utils.keywordExtractor import keyword_extractor
from .utils.getTitleTextSummary import getTitleTextSummary
from .utils.getDomainTopics import getDomainTopics
from .utils.scrapeURL import getTextFromURL

from .models import Document, Topic

# Create your views here.

class ClassifyAnalyseView(generics.GenericAPIView):

    def post(self, request):

        url = request.data.get('url')

        rawText = getTextFromURL(url)
        original_lang = iso639.to_name(detect(rawText))
        rawText = detect_and_translate(rawText, target_lang='en')
        

        title, mainText, extractive_summary = getTitleTextSummary(url)

        # Save in DB to build topic graph
        domain, topics = getDomainTopics(mainText) # rawText gives noisy output
        keywords = keyword_extractor(extractive_summary)
        
        title_len = len(title.split())
        mainText_len = len(mainText.split())
        extractive_summary_len = len(extractive_summary.split())
        rawText_len = len(rawText.split())

        #----------------DOMAIN---------------#

        obj = Topic.nodes.get_or_none(name=domain[0])
        if obj:
            obj.level = 0
            urls = obj.urls
            if url not in urls:
                urls.append(url)
                obj.urls = urls
            obj.save()
        else:
            obj = Topic(name=domain[0], level=0, weight=float(domain[1]), urls=[url])
            obj.save()

        #----------------TOPICS---------------#
        
        for i in range(len(topics[0])):
            topic_obj = Topic.nodes.get_or_none(name=topics[0][i])
            if not topic_obj:
                topic_obj = Topic(name=topics[0][i], level=1, weight=topics[1][i], urls=[url])
                topic_obj.save()
            else:
                urls = topic_obj.urls
                if url not in urls:
                    urls.append(url)
                    topic_obj.urls = urls
                    topic_obj.save()
            obj.hasTopic.connect(topic_obj)

        # Storing document information
        doc = Document.nodes.get_or_none(url = url)
        if not doc:
            doc = Document(url=url, mainText=mainText, extractiveSummary=extractive_summary, domain=domain[0], 
            topics=topics[0], keywords=keywords)
            doc.save()
            
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
                            "domain": domain[0],
                            "topics": topics[0],
                            "keywords": keywords,
                            "original_lang": original_lang
                        }, status=status.HTTP_201_CREATED)




class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)