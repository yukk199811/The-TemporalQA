from pycorenlp import StanfordCoreNLP
from functools import lru_cache
import json
import usingWiki
import sys

sys.path.append("..")
from usingWiki import *
import pandas as pd
from functools import lru_cache
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')
stop_word = set(stopwords.words('english'))


# doc is the temporal question
@lru_cache()
def get_question_pos(doc,rho):
    after = {}
    # Storing candidate attributes
    filtered = []
    # Storing time preposition or ORDINAL
    time_IN = {}
    # Storing DATE entity
    time_CD1 = []
    time_CD=[]
    time_CD2=[]
    nlp_wrapper = StanfordCoreNLP('http://localhost:9000')
    print('Temporal questions:', doc)
    annot_doc = nlp_wrapper.annotate(doc,
                                     properties={
                                         'annotators': 'lemma,pos,ner',
                                         'outputFormat': 'json',
                                         'timeout': 1000,
                                     })
    resul=annot_doc['sentences'][0]
    for i in range(len(resul['tokens'])):
        after[i] = [annot_doc['sentences'][0]['tokens'][i]['lemma'], annot_doc['sentences'][0]['tokens'][i]['pos'],
                    annot_doc['sentences'][0]['tokens'][i]['ner']]

    IN_list = ['during', 'in', 'at', 'between', 'before', 'until', 'after', 'then', 'next']
    ORDINAL_dic = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8,
                   'ninth': 9,
                   'tenth': 10, 'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14, 'fifteenth': 15,
                   'sixteenth': 16,
                   'seventeenth': 17, 'eighteenth': 18, 'nineteenth': 19,'twentieth':20,'thirtieth':30,'fortieth':40,
                   'fiftieth':50,'sixtieth':60,'seventieth':70,'eightieth':80,'ninetieth':90,'last':-1
                   }
    for m in range(len(after)):
        # rank 0 of signal word
        if after[m][0] == 'during' or after[m][0] == 'between':
            time_IN[0] = after[m][0]
        # rank 1 of signal word
        if after[m][0] == 'in' or after[m][0] == 'at' or after[m][0] == 'of':
            time_IN[1] = after[m][0]
        # rank 2 of signal word
        if after[m][0] == 'before' or after[m][0] == 'until' :
            time_IN[2] = after[m][0]
        # rank 3 of signal word
        if after[m][0] == 'after' or after[m][0] == 'then' or after[m][0] == 'next':
            time_IN[3] = after[m][0]
        # rank 4 of signal word
        if after[m][1] == 'ORDINAL':
            time_IN[4] = ORDINAL_dic[after[m][0]]


        #storing the date entity
        if after[m][2] == 'DATE':
            time_CD1.append(after[m][0])

    for i in time_CD1:
        if i.isdigit() and len(i)==4:
            i = int(i)
            time_CD2.append(i)

    time_CD2.sort()
    time_CD.append(''.join(str(item) for item in time_CD2))



    # lemmatization
    for i in range(len(after)):
        if (after[i][1] == 'VBZ' or after[i][1] == 'VB' or after[i][1] == 'VBD' or after[i][1] == 'VBG' or after[i][
            1] == 'VBN' or after[i][1] == 'VBP') and after[i][0] not in stop_word:
            filtered.append(after[i][0])


    objs = usingWiki.get_response(doc,rho)
    if filtered == []:
        for i in range(len(objs)):
            if objs[i][0] not in stop_word:
                filtered.append(objs[i][0])
        filtered.pop(0)
        for i in range(len(filtered)):
            filtered[i] = filtered[i].lower()
    return after, annot_doc, filtered, time_IN, time_CD


# after = get_question_pos(doc)[0]
# annot_doc = get_question_pos(doc)[1]
# filtered = get_question_pos(doc)[2]
# time_IN = get_question_pos(doc)[3]
# time_CD = get_question_pos(doc)[4]
#
# # 将lemma和pos存储在lemma_and_pos.json中
# file_name1 = 'lemma_and_pos.json'
# with open(file_name1, 'w') as file_obj1:
#     json.dump(after, file_obj1)
# file_obj1.close()
# file_name = 'afterStanford.json'
# with open(file_name, 'w') as file_obj:
#     json.dump(annot_doc, file_obj)
# file_obj.close()
