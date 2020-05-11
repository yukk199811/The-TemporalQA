from collections import defaultdict
import json
from numpy import *
import os
import numpy as np
import re
import codecs

import datetime
from usingVector import *



# print(get_high_similarity(5))


# obtaining the wiki predicates with high similarity, the qualifier of which are stattime，endtime，point in time。
def final_process(dict):
    my_dict = {}
    for key, value in dict.items():
        for i in value[2:]:
            my_dict1 = {}
            for m in i:
                if len(m) == 3:
                    if m[2] == 'start time':
                        my_dict1['start time'] = m[1]
                        my_dict1['ps'] = m[0]
                        my_dict1['similarity']=value[0]
                        my_dict[key] = my_dict1
                    if m[2] == 'end time':
                        my_dict1['end time'] = m[1]
                        my_dict1['ps'] = m[0]
                        my_dict1['similarity']=value[0]
                        my_dict[key] = my_dict1
                    if m[2] == 'point in time':
                        my_dict1['point in time'] = m[1]
                        my_dict1['ps'] = m[0]
                        my_dict1['similarity']=value[0]
                        my_dict[key] = my_dict1
                    else:
                        my_dict1['ps'] = m[0]
                        my_dict1['similarity']=value[0]
                        my_dict[key] = my_dict1
                else:
                    my_dict1['ps'] = m[0]
                    my_dict1['similarity'] = value[0]
                    my_dict[key] = my_dict1
    return my_dict


# dict={'position played on team / speciality': {'similarity':0.8}, 'member of sports team': {'similarity':0.9,'start time': 'P580', 'end time': 'P582'}}
# wiki_id=get_wikiid(objs, ids),'Q801'
# time1={1:'during',2:'before'}
# time2=['2011']

def getting_my_answer(dict, wiki_id, time1, time2):
    just_a_list = defaultdict(list)
    ans=[]
    str1 = '-01-01'
    str2 = '-12-31'
    answer_with_label = {}
    # rank 0 signal word with two date
    if (0 in time1.keys()) and len(time2) == 2:
        for key, value in dict.items():
            # 有qualifier
            if len(dict[key]) >= 3:
                # 模板0-1-1
                if ('start time' in dict[key]) and ('end time' in dict[key]):
                    try:
                        time_2 = time2[1] + str2

                        url = 'https://query.wikidata.org/sparql'
                        query = """
                        SELECT ?answer ?answerLabel ?starttime ?endtime
                        WHERE
                        {
                             wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                           pq:""" + dict[key]['start time'] + """  ?starttime;
                                           pq:""" + dict[key]['end time'] + """ ?endtime;
                                          ].
                             FILTER('""" + time_2 + """'^^xsd:dateTime <= ?endtime && ?starttime <= '""" + time_2 + """'^^xsd:dateTime).
                             SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                        }
                        ORDER BY ?starttime
                    	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.1.1', dict[key]['similarity'],graph[i]['answerLabel']['value'],'1', graph[i]['answer']['value'],graph[i]['starttime']['value'],
                                     graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.1.1'])
                        # print data

                    except:
                        print("Http Error1.1.1:")

                # template 0-1-2
                if 'point in time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        time_2 = time2[1] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                       SELECT ?answer ?answerLabel ?pointintime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['point in time'] + """  ?pointintime;
                                         ].
                            FILTER('""" + time_1 + """'^^xsd:dateTime <= ?pointintime && ?pointintime <= '""" + time_2 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?pointintime
                                       	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.1.2', dict[key]['similarity'],graph[i]['answerLabel']['value'],'1', graph[i]['answer']['value'],graph[i]['pointintime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.1.2'])
                        # print data

                    except :
                        print("Http Error1.1.2:")

                # template 2-1
                if ('point in time' not in dict[key]) and ('start time' in dict[key]) and ('end time' not in dict[key]):
                    try:
                        # print "Link is ",link
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                      SELECT ?answer ?answerLabel ?starttime
                      WHERE
                      {
                           wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                         pq:""" + dict[key]['start time'] + """  ?starttime;
                                        ].
                           FILTER('""" + time_2 + """'^^xsd:dateTime >= ?starttime ).
                           SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                      }
                      ORDER BY ?starttime
                                                          	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.1.3',dict[key]['similarity'], graph[i]['answerLabel']['value'],'2', graph[i]['answer']['value'],graph[i]['starttime']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.1.3'])
                        # print data

                    except:
                        print("Http Error1.1.3:")

                # template 2-2
                if ('point in time' not in dict[key]) and ('start time' not in dict[key]) and ('end time' in dict[key]):
                    try:
                        # print "Link is ",link
                        time_2 = time2[1] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                      SELECT ?answer ?answerLabel ?endtime
                      WHERE
                      {
                           wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                         pq:""" + dict[key]['end time'] + """  ?endtime;
                                        ].
                           FILTER( ?endtime >= '""" + time_2 + """'^^xsd:dateTime).
                           SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                      }
                      ORDER BY ?endtime
                                                          	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.1.4',dict[key]['similarity'], graph[i]['answerLabel']['value'],'2', graph[i]['answer']['value'],graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.1.4'])
                        # print data

                    except:
                        print("Http Error1.1.4:")

            # no qualifier
            else:
                # 模板3
                try:
                    # print "Link is ",link
                    url = 'https://query.wikidata.org/sparql'
                    query = """
                   SELECT ?answer ?answerLabel 
                   WHERE
                   {
                        wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                     ].
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                   }
                                                           	    """

                    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                    answer = r.json()
                    graph = answer['results']['bindings']
                    if len(graph):
                        for i in range(len(graph)):
                            just_a_list[key].append(['1.1.5',dict[key]['similarity'], graph[i]['answerLabel']['value'],'3',graph[i]['answer']['value']])
                            ans.append(graph[i]['answerLabel']['value'])
                    else:
                        just_a_list[key].append(['1.1.5'])
                    # print data

                except:
                    print("Http Error1.1.5:")


    # 1.2 rank 0 siganl word with one date
    if (0 in time1.keys()) and len(time2) == 1:
        for key, value in dict.items():
            # 有qualifier
            if len(dict[key]) >= 3:
                # 模板0-2-1
                if ('start time' in dict[key]) and ('end time' in dict[key]):
                    try:
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                       SELECT ?answer ?answerLabel ?starttime ?endtime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['start time'] + """  ?starttime;
                                          pq:""" + dict[key]['end time'] + """ ?endtime;
                                         ].
                            FILTER('""" + time_2 + """'^^xsd:dateTime >= ?starttime && ?endtime >= '""" + time_2 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?starttime
                                           	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.2.1',dict[key]['similarity'], graph[i]['answerLabel']['value'], '1',graph[i]['answer']['value'],graph[i]['starttime']['value'],
                                     graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.2.1'])
                        # print data

                    except :
                        print("Http Error1.2.1:")

                # template 0-2-2
                if 'point in time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """SELECT ?answer ?answerLabel ?pointintime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['point in time'] + """  ?pointintime;
                                         ].
                            FILTER('""" + time_1 + """'^^xsd:dateTime <= ?pointintime && ?pointintime <= '""" + time_2 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?pointintime
                                                                              	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.2.2',dict[key]['similarity'], graph[i]['answerLabel']['value'], '1',graph[i]['answer']['value'],graph[i]['pointintime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.2.2'])
                        # print data

                    except :
                        print("Http Error1.2.2:")

                # 模板2-1
                if ('point in time' not in dict[key]) and ('start time' in dict[key]) and ('end time' not in dict[key]):
                    try:
                        # print "Link is ",link
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                     SELECT ?answer ?answerLabel ?starttime
                     WHERE
                     {
                          wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                        pq:""" + dict[key]['start time'] + """  ?starttime;
                                       ].
                          FILTER('""" + time_2 + """'^^xsd:dateTime >= ?starttime).
                          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                     }
                     ORDER BY ?starttime
                                                                             	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.2.3' ,dict[key]['similarity'],graph[i]['answerLabel']['value'],'2', graph[i]['answer']['value'],graph[i]['starttime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.2.3'])
                        # print data

                    except :
                        print("Http Error1.2.3:")

                # 模板2-2
                if ('point in time' not in dict[key]) and ('start time' not in dict[key]) and ('end time' in dict[key]):
                    try:
                        # print "Link is ",link
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                         SELECT ?answer ?answerLabel ?endtime
                         WHERE
                         {
                              wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                            pq:""" + dict[key]['end time'] + """  ?endtime;
                                           ].
                              FILTER( ?endtime >= '""" + time_2 + """'^^xsd:dateTime).
                              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                         }
                         ORDER BY ?endtime
                                                                             	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['1.2.4',dict[key]['similarity'], graph[i]['answerLabel']['value'],'2', graph[i]['answer']['value'],graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['1.2.4'])
                        # print data

                    except :
                        print("Http Error1.2.4:")

            # no qualifier
            else:
                # 模板3
                try:
                    # print "Link is ",link
                    url = 'https://query.wikidata.org/sparql'
                    query = """
                   SELECT ?answer ?answerLabel 
                   WHERE
                   {
                        wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                     ].
                        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                   }
                                                                                """

                    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                    answer = r.json()
                    graph = answer['results']['bindings']
                    if len(graph):
                        for i in range(len(graph)):
                            just_a_list[key].append(['1.2.5',dict[key]['similarity'], graph[i]['answerLabel']['value'],'3',graph[i]['answer']['value']])
                            ans.append(graph[i]['answerLabel']['value'])
                    else:
                        just_a_list[key].append(['1.2.5'])
                    # print data

                except :
                    print("Http Error1.2.5:")


    # rank 1 signal words with one date
    if ((1 in time1.keys()) and (0 not in time1.keys()) and len(time2) != 0) or (len(time2) != 0 and (3 not in time1.keys()) and (2 not in time1.keys()) and (1 not in time1.keys()) and (
            0 not in time1.keys()) and (4 not in time1.keys())):
        for key, value in dict.items():
            # qualifier exists
            if len(dict[key]) >= 3:
                # template 0-2-1
                if ('start time' in dict[key]) and ('end time' in dict[key]):
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                       SELECT ?answer ?answerLabel ?starttime ?endtime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['start time'] + """  ?starttime;
                                          pq:""" + dict[key]['end time'] + """ ?endtime;
                                         ].
                            FILTER('""" + time_1 + """'^^xsd:dateTime >= ?starttime && ?endtime >= '""" + time_1 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?starttime
                                                               	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['2.1.1',dict[key]['similarity'], graph[i]['answerLabel']['value'],'1', graph[i]['answer']['value'],graph[i]['starttime']['value'],
                                     graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['2.1.1'])
                        # print data

                    except :
                        print("Http Error2.1.1:")
                # template 0-2-2
                if 'point in time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """SELECT ?answer ?answerLabel ?pointintime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['point in time'] + """  ?pointintime;
                                         ].
                            FILTER('""" + time_1 + """'^^xsd:dateTime <= ?pointintime && ?pointintime <= '""" + time_2 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?pointintime
                                                                                                  	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['2.1.2',dict[key]['similarity'], graph[i]['answerLabel']['value'], '1',graph[i]['answer']['value'],graph[i]['pointintime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['2.1.2'])
                        # print data

                    except:
                        print("Http Error2.1.2:")
                # template 2-1
                if ('point in time' not in dict[key]) and ('start time' in dict[key]) and ('end time' not in dict[key]):
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                        SELECT ?answer ?answerLabel ?starttime
                        WHERE
                        {
                             wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                           pq:""" + dict[key]['start time'] + """  ?starttime;
                                          ].
                             FILTER('""" + time_1 + """'^^xsd:dateTime >= ?starttime).
                             SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                        }
                        ORDER BY ?starttime
                                                                                                	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['2.1.3',dict[key]['similarity'], graph[i]['answerLabel']['value'],'2',graph[i]['answer']['value'], graph[i]['starttime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['2.1.3'])
                        # print data

                    except :
                        print("Http Error2.1.3:")

                # template 2-2
                if ('point in time' not in dict[key]) and ('start time' not in dict[key]) and ('end time' in dict[key]):
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                        SELECT ?answer ?answerLabel ?endtime
                        WHERE
                        {
                             wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                           pq:""" + dict[key]['end time'] + """  ?endtime;
                                          ].
                             FILTER( ?endtime >= '""" + time_1 + """'^^xsd:dateTime).
                             SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                        }
                        ORDER BY ?endtime
                                                                                                	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['2.1.4',dict[key]['similarity'], graph[i]['answerLabel']['value'], '2',graph[i]['answer']['value'],graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['2.1.4'])
                        # print data

                    except :
                        print("Http Error2.1.4:")

            # no qualifier
            else:
                # 模板3
                try:
                    url = 'https://query.wikidata.org/sparql'
                    query = """
                    SELECT ?answer ?answerLabel 
                    WHERE
                    {
                         wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                      ].
                         SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                    }
                                                                                            	    """

                    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                    answer = r.json()
                    graph = answer['results']['bindings']
                    if len(graph):
                        for i in range(len(graph)):
                            just_a_list[key].append(['2.1.5',dict[key]['similarity'], graph[i]['answerLabel']['value'],'3',graph[i]['answer']['value']])
                            ans.append(graph[i]['answerLabel']['value'])
                    else:
                        just_a_list[key].append(['2.1.5'])
                    # print data

                except :
                    print("Http Error2.1.5:", )

    # 3. single date with rank 2 signal words
    if (2 in time1.keys()) and (0 not in time1.keys()) and (1 not in time1.keys()) and len(time2) != 0:
        for key, value in dict.items():
            #  qualifier exists
            if len(dict[key]) >= 3:

                if 'end time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                       SELECT ?answer ?answerLabel ?endtime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['end time'] + """  ?endtime;
                                         ].
                            FILTER( ?endtime <= '""" + time_1 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?endtime
                                                                                                                   	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['3.1.1',dict[key]['similarity'], graph[i]['answerLabel']['value'],'2', graph[i]['answer']['value'],graph[i]['endtime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['3.1.1'])
                        # print data

                    except :
                        print("Http Error3.1.1:")

                # template 2-1
                if 'point in time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_1 = time2[0] + str1
                        url = 'https://query.wikidata.org/sparql'
                        query = """SELECT ?answer ?answerLabel ?pointintime
                       WHERE
                       {
                            wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                          pq:""" + dict[key]['point in time'] + """  ?pointintime;
                                         ].
                            FILTER(?pointintime <= '""" + time_1 + """'^^xsd:dateTime).
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                       }
                       ORDER BY ?pointintime
                                                                                                                      	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['3.1.2',dict[key]['similarity'], graph[i]['answerLabel']['value'],'1', graph[i]['answer']['value'],graph[i]['pointintime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['3.1.2'])
                        # print data

                    except :
                        print("Http Error3.1.2:")

            # no qualifier
            else:
                # 模板3
                try:
                    url = 'https://query.wikidata.org/sparql'
                    query = """
                    SELECT ?answer ?answerLabel 
                    WHERE
                    {
                         wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                      ].
                         SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                    }
                                                                                                            	    """

                    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                    answer = r.json()
                    graph = answer['results']['bindings']
                    if len(graph):
                        for i in range(len(graph)):
                            just_a_list[key].append(['3.1.3',dict[key]['similarity'], graph[i]['answerLabel']['value'],'3',graph[i]['answer']['value']])
                            ans.append(graph[i]['answerLabel']['value'])
                    else:
                        just_a_list[key].append(['3.1.3'])

                except :
                    print("Http Error3.1.3:")

    # 4. single date with rank 3 signal word
    if (3 in time1.keys()) and (0 not in time1.keys()) and (2 not in time1.keys()) and (1 not in time1.keys()) and len(
            time2) != 0:
        for key, value in dict.items():
            # 有qualifier
            if len(dict[key]) >= 3:
                # 模板2-2
                if 'start time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """
                        SELECT ?answer ?answerLabel ?starttime
                        WHERE
                        {
                             wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                           pq:""" + dict[key]['start time'] + """  ?starttime;
                                          ].
                             FILTER( '""" + time_2 + """'^^xsd:dateTime <= ?starttime ).
                             SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                        }
                        ORDER BY ?starttime
                                                                                                	    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['4.1.1',dict[key]['similarity'], graph[i]['answerLabel']['value'], '2',graph[i]['answer']['value'],graph[i]['starttime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['4.1.1'])

                    except :
                        print("Http Error4.1.1:")

                # template 2-2
                if 'point in time' in dict[key]:
                    try:
                        # print "Link is ",link
                        time_2 = time2[0] + str2
                        url = 'https://query.wikidata.org/sparql'
                        query = """SELECT ?answer ?answerLabel ?pointintime
                              WHERE
                              {
                                   wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                                 pq:""" + dict[key]['point in time'] + """  ?pointintime;
                                                ].
                                   FILTER( '""" + time_2 + """'^^xsd:dateTime <= ?pointintime).
                                   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                              }
                              ORDER BY ?pointintime
                                                                                                                                    """

                        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                        answer = r.json()
                        graph = answer['results']['bindings']
                        if len(graph):
                            for i in range(len(graph)):
                                just_a_list[key].append(
                                    ['4.1.2',dict[key]['similarity'], graph[i]['answerLabel']['value'],'1',graph[i]['answer']['value'], graph[i]['pointintime']['value']])
                                ans.append(graph[i]['answerLabel']['value'])
                        else:
                            just_a_list[key].append(['4.1.2'])
                        # print data

                    except :
                        print("Http Error4.1.2:")

            # no qualifier
            else:
                # 模板3
                try:
                    url = 'https://query.wikidata.org/sparql'
                    query = """
                    SELECT ?answer ?answerLabel 
                    WHERE
                    {
                         wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                      ].
                         SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                    }
                                                                                                            	    """

                    r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                    answer = r.json()
                    graph = answer['results']['bindings']
                    if len(graph):
                        for i in range(len(graph)):
                            just_a_list[key].append(['4.1.3',dict[key]['similarity'], graph[i]['answerLabel']['value'],'3',graph[i]['answer']['value']])
                            ans.append(graph[i]['answerLabel']['value'])
                    else:
                        just_a_list[key].append(['4.1.3'])

                except :
                    print("Http Error4.1.3:")


    # ORDINAL word(1)
    if (len(time2) == 0) and (3 not in time1.keys()) and (2 not in time1.keys()) and (1 not in time1.keys()) and (
            0 not in time1.keys()) and (4 in time1.keys()):
        for key, value in dict.items():
            try:
                # print "Link is ",link
                url = 'https://query.wikidata.org/sparql'
                query = """
               SELECT ?answer ?answerLabel
               WHERE
               {
                    wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                 ].
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
               }
                                                                            """

                r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                answer = r.json()
                graph = answer['results']['bindings']
                if len(graph):
                    for i in range(len(graph)):
                        just_a_list[key].append(['5.1.1',dict[key]['similarity'], graph[time1[4]-1]['answerLabel']['value'],'1',graph[i]['answer']['value']])
                        ans.append(graph[i]['answerLabel']['value'])
                else:
                    just_a_list[key].append(['5.1.1'])

            except :
                print("Http Error5.1.1:")


    else:
        for key, value in dict.items():
            try:
                # print "Link is ",link
                url = 'https://query.wikidata.org/sparql'
                query = """
               SELECT ?answer ?answerLabel
               WHERE
               {
                    wd:""" + wiki_id + """ p:""" + dict[key]['ps'] + """ [ps:""" + dict[key]['ps'] + """ ?answer;
                                 ].
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
               }
                                                                            """

                r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
                answer = r.json()
                graph = answer['results']['bindings']
                if len(graph):
                    for i in range(len(graph)):
                        just_a_list[key].append(['6.1.1', dict[key]['similarity'], graph[i]['answerLabel']['value'], '3',graph[i]['answer']['value']])
                        ans.append(graph[i]['answerLabel']['value'])
                else:
                    just_a_list[key].append(['6.1.1'])

            except :
                print("Http Error6.1.1:")
                print(wiki_id,dict[key]['ps'])
    return just_a_list,ans


# dic = get_high_similarity(7, sim)
# start1 = datetime.datetime.now()
# answer = getting_my_answer(final_process(dic), wiki_id, time_IN, time_CD)
# end1 = datetime.datetime.now()
# print('time cost:',end1-start1)

#calculate confidence of the final answers
def my_answer_with_possibility(ans,rhos):
    penalty={'1':1.0,'2':0.85,'3':0.75}
    ans_with_possibility=defaultdict(list)
    for key,value in ans.items():
        if len(value[0])>=5:
            #penalty is the punish coefficient，rho is the confidence of the subject word
            possibility=(0.4*rhos+0.6*value[0][1])*penalty[value[0][3]]
            # #相似度阈值为0.5
            # if possibility>=0.4:
            ans_with_possibility[value[0][2]].append([possibility,value[0][4]])
    res = sorted(ans_with_possibility.items(),key=lambda d:d[1],reverse=True)

    return res

#print the final answer list
# print(my_answer_with_possibility(answer,rho))
