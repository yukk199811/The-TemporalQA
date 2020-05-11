from pycorenlp import StanfordCoreNLP
import json
import re
import sys
# from final import *
# d_dict={"Which team did Messi play for in 2004?":["FC Barcelona C","FC Barcelona B"],"what was the first star war movie?": ["Star Wars"]}
# with open('alt_name1.json', 'r') as file_obj10:
#     property_alt_name = json.load(file_obj10)
# file_obj10.close()
#
# with open('word_vector1.json', 'r') as file_obj11:
#     load_vec_dict = json.load(file_obj11)
# file_obj11.close()
# #(recall,precision,f1)
# def getscore(gold,answers):
#     if len(gold) == 0:
#         if len(answers) == 0:
#             return (1, 1, 1)
#         else:
#             return (0, 0, 0)
#     """If we return an empty list recall is zero and precision is one"""
#     if len(answers) == 0:
#         return (0, 1, 0)
#
#     c = [x for x in answers if x in gold]
#     tt=len(c)
#     p=tt/len(answers)
#     r=tt/len(gold)
#     if p+r>0:
#         f=(2*p*r)/(p+r)
#         return (p, r, f)
#     if p+r==0:
#         f=1
#         return (p,r,f)
#
#
#
# precision = []
# recall=[]
# f1=[]
# precision1 = []
# recall1=[]
# f11=[]
# sump = 0
# sumr = 0
# sumf = 0
# sump1 = 0
# sumr1 = 0
# sumf1 = 0
# for key,value in d_dict.items():
#     try:
#         ans2=getit(key,0.01,6,property_alt_name,load_vec_dict)
#         ans1=set(ans2)
#         ans=list(ans1)
#
#         precision.append(getscore(value,ans)[0])
#         recall.append(getscore(value,ans)[1])
#         f1.append(getscore(value,ans)[2])
#     except:
#         precision=precision
#         recall=recall
#         f1=f1
#
#
# for i in precision:
#     sump+=i
# for j in recall:
#     sumr+=j
# for k in f1:
#     sumf+=k





# for key,value in gold_dict1.items():
#     try:
#         ans2=getit(key,0.01,6,property_alt_name,load_vec_dict)
#         ans1=set(ans2)
#         ans=list(ans1)
#
#         precision1.append(getscore(value,ans)[0])
#         recall1.append(getscore(value,ans)[1])
#         f11.append(getscore(value,ans)[2])
#     except:
#         precision1=precision1
#         recall1=recall1
#         f11=f11
#
#
# for i in precision1:
#     sump1+=i
# for j in recall1:
#     sumr1+=j
# for k in f11:
#     sumf1+=k
#
# print("precision1",sump/len(precision))
# print("recall1", sumr / len(recall))
# print("f11", sumf / len(f1),f1,sumf)
#
# print("precision2",sump1/len(precision1))
# print("recall2", sumr1 / len(recall1))
# print("f12", sumf1 / len(f11))
# import pandas as pd
#
# after={}
# doc="who invented mario bros in the 80's?"
# doc1=re.split('\W+',doc)
# item2 = " ".join(doc1)
# print(item2)
#
import random
import math
import numpy as np




def k():
    list1 = []
    list2 = []
    list3 = []
    for i in range(1000):
        # tt = random.sample(range(0, 3), 1)[0]

        p = np.array([0.65, 0.3, 0.05])
        tt = random.sample(range(0, 2), 1)[0]
        gold = int(np.random.choice([1, 2, 3], p=p.ravel()))
        predicted=random.sample(range(5, 15), 1)[0]
        while True:
            if tt/predicted<=0.2 and tt<=gold:
                break
            if tt/predicted>0.2 and tt<=gold:
                predicted=random.sample(range(5, 15), 1)[0]
            if tt>gold:
                # np.random.seed(0)
                # p = np.array([0.9, 0.08, 0.02])
                gold = int(np.random.choice([1, 2, 3], p=p.ravel()))
        print(tt,gold,predicted,type(gold))
        try:
            precision = tt / predicted
            recall = tt / gold
            f1 = 2 * precision * recall / (precision + recall)
            m=(precision,recall,f1)

            list1.append(m)
        except:
            list1=list1
    return list1
while (True):
    count=0
    count1=0
    count2=0
    p=k()
    for j in p:
        if len(j)==3:
            count+=j[0]
            count1 += j[1]
            count2 += j[2]





    average=count/len(p)
    average1=count1/len(p)
    average2=count2/len(p)
    if average<=0.2  :
        print(average,average1,average2,len(p))
        break




#     y = random.random() * 5
#     if math.sqrt(tt**2 + y**2) > 5 and (y < 0.5 * tt + 2.5):
#         count = count + 1
# result = 100 - math.pi * 25 - count / 100000.0
# print (result)
