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
from .utils.currentURLStatus import currentURLStatus
from .utils.getLbl2VecDomain import getDomain


from .models import Document, Topic
from neomodel import db




# Create your views here.

class ClassifyAnalyseView(generics.GenericAPIView):

    def post(self, request):

        url = request.data.get('url')
        current_status = currentURLStatus(url)
        # LbLDomain = getDomain()
        rawOriginalText = getTextFromURL(url)
        original_lang = iso639.to_name(detect(rawOriginalText))

        rawText=""
        if original_lang != 'English':
            rawText = detect_and_translate(rawOriginalText, target_lang='en')
        else:
            rawText = rawOriginalText
        

        title, mainText, extractive_summary = getTitleTextSummary(url)
        lbl_domain, similarityScore = getDomain(title, mainText)

        # Save in DB to build topic graph
        domain, topics = getDomainTopics(rawText)
        keywords = keyword_extractor(extractive_summary)
        
        title_len = len(title.split())
        mainText_len = len(mainText.split())
        extractive_summary_len = len(extractive_summary.split())
        rawOriginalText_len = len(rawOriginalText.split())
        rawText_len = len(rawText.split())


        #---------------SIMILAR DOCUMENTS-----------------#
        similar_urls = []
        #---------------DOMAIN-----------------#
        obj = Topic.nodes.get_or_none(name=domain)
        if obj:
            obj.level = 0
            urls = obj.urls
            if url not in urls:
                urls.append(url)
                obj.urls = urls
            #Getting similar documents
            for u in urls:
                if(u != url and u not in similar_urls):
                    similar_urls.append(u)
            obj.save()
        else:
            obj = Topic(name=domain, level=0, urls=[url])
            obj.save()


        #----------------TOPICS---------------#
        for i in range(len(topics)):
            topic_obj = Topic.nodes.get_or_none(name=topics[i])
            if not topic_obj:
                topic_obj = Topic(name=topics[i], level=1, urls=[url])
                topic_obj.save()
            else:
                urls = topic_obj.urls
                if url not in urls:
                    urls.append(url)
                    topic_obj.urls = urls

                #Getting similar documents
                for u in urls:
                    if(u != url and u not in similar_urls):
                        similar_urls.append(u)
                
                topic_obj.save()

            if(obj.name != topic_obj.name):
                if(not topic_obj.hasTopic.is_connected(obj)):
                    obj.hasTopic.connect(topic_obj)


        #---------------------SPECIALIZED TO GENERALIZED--------------------#
        #----------CHILDREN NODES-----------#
        children = {}
        traversal = []
        traversal.append(obj)

        for node in traversal:
            childNodes = node.hasTopic.search(level = 0)
            if childNodes:
                children[node.name] = []
                for c in childNodes:
                    children[node.name].append(c.name)
                    if c not in traversal:
                        traversal.append(c)

        #------------PARENT NODES------------#
        parents = {}
        traversal = []
        traversal.append(obj)
        
        for node in traversal:
            query = r"MATCH (t1:Topic {name: '" + node.name + r"'})<-[:HAS_TOPIC]-(t2:Topic {level: 0}) RETURN t2"
            results, _ = db.cypher_query(query)
            parent_topics = [Topic.inflate(row[0]) for row in results]
            if parent_topics:
                parents[node.name] = []
                for p in parent_topics:
                    if p not in traversal:
                        parents[node.name].append(p.name)
                        traversal.append(p)


        #Storing document information
        doc = Document.nodes.get_or_none(url = url)
        if not doc:
            doc = Document(url=url, mainText=mainText, extractiveSummary=extractive_summary, domain=domain, 
            topics=topics, keywords=keywords)
            doc.save()

        
            
        return Response(
                        {
                            "LbLDomain": lbl_domain,
							'similarityScore': similarityScore,
                            "domain": domain,
                            "topics": topics,
                            "keywords": keywords,
                            "original_lang": original_lang,
                            "similar_urls": similar_urls,
                            "children_nodes": children,
                            "parent_nodes": parents,
                            "current_status": current_status,
                            "len": {
                                "title_len": title_len, 
                                "mainText_len": mainText_len, 
                                "extractive_summary_len": extractive_summary_len, 
                                "rawText_len": rawText_len, 
                                "rawOriginalText_len": rawOriginalText_len
                            },
                            "textual_data": {
                                "title": title,
                                "mainText": mainText,
                                "extractive_summary": extractive_summary,
                                "rawOriginalText": rawOriginalText,
                                "rawText": rawText,
                            }
                        }, status=status.HTTP_201_CREATED)




class TestView(generics.GenericAPIView):

    def get(self, request):
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)