from usingStanfordnlp import *

from collections import defaultdict
from functools import lru_cache
import json
from numpy import *
import os
import numpy as np
import re
import codecs


after1=[]



def get_p(entity_graph):
    # getting predicate in subgraph
    graph1 = json.loads(json.dumps(entity_graph))
    graph2 = graph1['results']['bindings']
    ps_wdlabel = defaultdict(list)
    for i in range(len(graph2)):
        if 'wdpqLabel' in graph2[i]:
            ps_wdlabel[graph2[i]['wdLabel']['value'].lower()].append(
                [graph2[i]['p']['value'][29:], graph2[i]['pq']['value'][39:], graph2[i]['wdpqLabel']['value'].lower()])
        else:
            ps_wdlabel[graph2[i]['wdLabel']['value'].lower()].append([graph2[i]['p']['value'][29:]])
    return ps_wdlabel


# ps_wdlabel = get_p(graph)




# processing glove.6B.50d word vector
@lru_cache()
def read_glove_vecs(glove_file):
    with open(glove_file, mode='r', encoding='UTF-8') as f:
        words = set()
        word_to_vec_map = {}

        for line in f:
            line = line.strip().split()
            curr_word = line[0]
            words.add(curr_word)
            word_to_vec_map[curr_word] = line[1:]
    return words, word_to_vec_map, curr_word


# #
#
# try:
#     url = 'https://query.wikidata.org/sparql'
#     query = """
#     SELECT ?property ?propertyType ?propertyLabel ?propertyAltLabel WHERE{
#       ?property wikibase:propertyType ?propertyType .
#       SERVICE wikibase:label {bd:serviceParam wikibase:language 'en'}
#       }
# 	    """
#
#     r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
#     datass = r.json()
#
# except requests.exceptions.HTTPError as errh:
#     print("Http Error:", errh)
# except requests.exceptions.ConnectionError as errc:
#     print("Error Connecting:", errc)
# except requests.exceptions.Timeout as errt:
#     print("Timeout Error:", errt)
# except requests.exceptions.RequestException as err:
#     print("OOps: Something Else", err)
#
# #


# root = os.getcwd()
# name = "glove.6B.50d.txt"
# path=os.path.join(root, name)
# dicts=read_glove_vecs(path)[1]
# file_name6 = 'word_vector.json'
# with open(file_name6, 'w') as file_obj6:
#     json.dump(dicts, file_obj6)
#     file_obj6.close()

# print(list(dict_temp)[0])
# file_name4 = 'glove_words.txt'
# with open(file_name4, 'w',encoding="utf-8") as file_obj4:
#     for k in dict_temp:
#         file_obj4.write(k + '\n')
# file_obj4.close()


# root = os.getcwd()
# name = "glove.6B.50d.txt"
# path=os.path.join(root, name)
# dict_temp=read_glove_vecs(path)[1]
# file_name3 = 'vector.txt'
# with open(file_name3, 'w',encoding="utf-8") as file_obj3:
#     for k, v in dict_temp.items():
#         file_obj3.write(str(k) + ' ' + str(v) + '\n')
# file_obj3.close()


# with open('alt_name1.json', 'r') as file_obj6:
#     property_alt_name = json.load(file_obj6)
# file_obj6.close()
# #
# alt=datass['results']['bindings']
# #抽取属性别名
# for i in range(len(alt)):
#     if 'propertyAltLabel' in alt[i]:
#         property_alt_name[alt[i]['propertyLabel']['value']] = alt[i]['propertyAltLabel']['value'].split(',')
#     else:
#         property_alt_name[alt[i]['propertyLabel']['value']] = alt[i]['propertyLabel']['value'].split(',')
#
#
# for k in property_alt_name:
#     for i in range(len(property_alt_name[k])):
#         property_alt_name[k][i]=property_alt_name[k][i].strip()
# for k in property_alt_name:
#     for i in range(len(property_alt_name[k])):
#         property_alt_name[k][i]=property_alt_name[k][i].lower()
# new_dict={}
# for k,v in property_alt_name.items():
#     new_dict[k.lower()]=v
# print(new_dict)
#
#
#
# print(property_alt_name['head of government'])
# file_name10 = 'alt_name1.json'
# with open(file_name10, 'w') as file_obj10:
#     json.dump(new_dict, file_obj10)
#     file_obj10.close()
# #

# with open('word_vector1.json', 'r') as file_obj7:
#     load_vec_dict = json.load(file_obj7)
# file_obj7.close()



# def cut(string):


# # 存储相似度
# sim = {}
# candidate predicate similarity calculation
def calculation(ps_wdlabel,load_vec_dict, filtered,property_alt_name):
    sim={}

    for key, value in ps_wdlabel.items():
        # candidate predicate is a word
        if filtered[0] in load_vec_dict:
            # the wikidata predicate is in the word vector set
            if key in load_vec_dict:
                # calculation similarity
                cos = np.dot(np.array(load_vec_dict[key]), np.array(load_vec_dict[filtered[0]])) / (
                            np.linalg.norm(np.array(load_vec_dict[key])) * np.linalg.norm(
                        np.array(load_vec_dict[filtered[0]])))
                sim[key] = [cos, 'information1:', value]
            # wikidata predicate is not in the word vector set
            else:
                # all of the alias have word vector
                try:
                    res = []
                    for alter_name in property_alt_name[key]:
                        res.append(load_vec_dict[alter_name])
                    res = np.array(res)
                    if res.shape[0] > 0:
                        vec_sum = np.sum(res, axis=0)
                        vec_average = vec_sum / res.shape[0]
                        cos1 = np.dot(vec_average, np.array(load_vec_dict[filtered[0]])) / (
                                    np.linalg.norm(vec_average) * np.linalg.norm(np.array(load_vec_dict[filtered[0]])))
                        sim[key] = [cos1, 'information2:', value]
                # some alias dont have word vector: splitting
                except KeyError as e:
                    nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
                    doc1 = re.split('\W+', key)
                    item2 = " ".join(doc1)
                    annot_doc3 = nlp_wrapper.annotate(item2,
                                                      properties={
                                                          'annotators': 'lemma,pos',
                                                          'outputFormat': 'json',
                                                          'timeout': 1000,
                                                      })
                    words_lemma = []
                    le = annot_doc3['sentences'][0]['tokens']
                    for i in le:
                        words_lemma.append(i['lemma'])
                    # all the word in phrase predicate has word vector
                    try:
                        ress = []
                        for i in words_lemma:
                            if i in load_vec_dict.keys():
                                ress.append(load_vec_dict[i])
                            else:
                                ress=ress
                        ress = np.array(ress)
                        if ress.shape[0] > 0:
                            vec_sum1 = np.sum(ress, axis=0)
                            vec_average1 = vec_sum1 / ress.shape[0]
                            cos2=np.dot(vec_average1, np.array(load_vec_dict[filtered[0]])) / (
                                        np.linalg.norm(vec_average1) * np.linalg.norm(
                                    np.array(load_vec_dict[filtered[0]])))
                            sim[key] = [cos2,'information3:',value]
                    # still no word vector
                    except KeyError:
                        sim[key] = [0.0, 'information:', value]
        # candidate predicate is a phrase
        else:
            nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
            doc1 = re.split('\W+', filtered[0])
            item2 = " ".join(doc1)
            annot_doc4 = nlp_wrapper.annotate(item2,
                                              properties={
                                                  'annotators': 'lemma,pos',
                                                  'outputFormat': 'json',
                                                  'timeout': 1000,
                                              })
            words_lemmas = []
            les = annot_doc4['sentences'][0]['tokens']
            for i in les:
                words_lemmas.append(i['lemma'])
            resss = []
            for i in words_lemmas:
                if i in load_vec_dict.keys():
                    resss.append(load_vec_dict[i])
                else:
                    resss = resss
            resss = np.array(resss)
            if resss.shape[0] > 0:
                vec_sum2 = np.sum(resss, axis=0)
                vec_average2 = vec_sum2 / resss.shape[0]
                if key in load_vec_dict:
                    # calculating similarity
                    cos = np.dot(np.array(load_vec_dict[key]), np.array(vec_average2)) / (
                            np.linalg.norm(np.array(load_vec_dict[key])) * np.linalg.norm(
                        np.array(vec_average2)))
                    sim[key] = [cos, 'information4:', value]
                #
                else:
                    # all alias are in the word vector set
                    try:
                        res = []
                        for alter_name in property_alt_name[key]:
                            res.append(load_vec_dict[alter_name])
                        res = np.array(res)
                        if res.shape[0] > 0:
                            vec_sum = np.sum(res, axis=0)
                            vec_average = vec_sum / res.shape[0]
                            cos1 = np.dot(vec_average, np.array(vec_average2)) / (
                                    np.linalg.norm(vec_average) * np.linalg.norm(np.array(vec_average2)))
                            sim[key] = [cos1, 'information5:', value]
                    # some alias dont have word vector: splitting the predicate
                    except KeyError as e:
                        nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
                        doc1 = re.split('\W+', key)
                        item2 = " ".join(doc1)
                        annot_doc3 = nlp_wrapper.annotate(item2,
                                                          properties={
                                                              'annotators': 'lemma,pos',
                                                              'outputFormat': 'json',
                                                              'timeout': 1000,
                                                          })
                        words_lemma = []
                        le = annot_doc3['sentences'][0]['tokens']
                        for i in le:
                            words_lemma.append(i['lemma'])
                        # the word in predicate have word vector
                        try:
                            ress = []

                            for i in words_lemma:
                                if i in load_vec_dict.keys():
                                    ress.append(load_vec_dict[i])
                                else:
                                    ress = ress
                            ress = np.array(ress)
                            if ress.shape[0] > 0:
                                vec_sum1 = np.sum(ress, axis=0)
                                vec_average1 = vec_sum1 / ress.shape[0]
                                cos2 = np.dot(vec_average1, np.array(vec_average2)) / (
                                        np.linalg.norm(vec_average1) * np.linalg.norm(
                                    np.array(vec_average2)))
                                sim[key] = [cos2, 'information6:', value]
                        # still no word vector
                        except KeyError:
                            sim[key] = [0.0, 'information7:', value]
    return sim,len(sim)

# sim=calculation(ps_wdlabel,load_vec_dict, filtered,property_alt_name)

# getting the wikidata predicate with n highest similarity
def get_high_similarity(n,similarity):
    # sorting the predicate according to similarity
    s = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    s = s[:n]
    dict = {}
    for i in s:
        dict[i[0]] = i[1]
    file_name = 'similarity.json'
    with open(file_name, 'w') as file_obj:
        json.dump(dict, file_obj)
        file_obj.close()
    return dict
