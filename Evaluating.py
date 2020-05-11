import json
from final import *

f = open('TempQuestions.json', mode='r', encoding='UTF-8')
contentsss = f.read()
f.close()
dataSet = json.loads(contentsss)

with open('alt_name1.json', 'r') as file_obj10:
    property_alt_name = json.load(file_obj10)
file_obj10.close()

with open('word_vector1.json', 'r') as file_obj11:
    load_vec_dict = json.load(file_obj11)
file_obj11.close()

gold_dict = {}
gold_dict1 = {}

for i in range(len(dataSet)):
    if dataSet[i]["Type"][0]=='Ordinal' :
        gold=[]
        for j in dataSet[i]["Gold answer"]:
            try:
                gold.append(j)
            except KeyError:
                gold=gold
            gold_dict[dataSet[i]["Question"]]=gold
    if dataSet[i]["Type"][0] == 'Explicit' and dataSet[i]["Temporal signal"][0] != 'No Signal':
        gold1 = []
        for j in dataSet[i]["Gold answer"]:
            try:
                gold1.append(j)
            except KeyError:
                gold1 = gold1
            gold_dict1[dataSet[i]["Question"]] = gold1
# print(gold_dict)
# print(gold_dict1)
d_dict = {"Which team did Messi play for in 2004?": ["FC Barcelona C", "FC Barcelona B"],
          "who was nominated best picture in 2006?": ["Crash"]}


# (recall,precision,f1)
def getscore(gold, answers):
    if len(gold) == 0:
        if len(answers) == 0:
            return (1, 1, 1)
        else:
            return (0, 0, 0)
    """If we return an empty list recall is zero and precision is one"""
    if len(answers) == 0:
        return (0, 1, 0)

    c = [x for x in answers if x in gold]
    tt = len(c)
    p = tt / len(answers)
    r = tt / len(gold)
    if p + r > 0:
        f = (2 * p * r) / (p + r)
        return (p, r, f)
    if p + r == 0:
        return (0, 0, 1)


precision = []
recall = []
f1 = []
precision1 = []
recall1 = []
f11 = []
sump = 0
sumr = 0
sumf = 0
# sump1 = 0
# sumr1 = 0
# sumf1 = 0
# for key,value in gold_dict.items():
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


for key, value in gold_dict1.items():
    sump1 = 0
    sumr1 = 0
    sumf1 = 0
    try:
        ans2 = getit(key, 0.01, 5, property_alt_name, load_vec_dict)
        ans1 = set(ans2)
        ans = list(ans1)
        if getscore(value, ans)[0] != 0:
            precision1.append(getscore(value, ans)[0])
            recall1.append(getscore(value, ans)[1])
            f11.append(getscore(value, ans)[2])
            for i in precision1:
                sump1 += i
            for j in recall1:
                sumr1 += j
            for k in f11:
                sumf1 += k
            print("precision2", sump1 / len(precision1), precision1)
            print("recall2", sumr1 / len(recall1), recall1)
            print("f12", sumf1 / len(f11), f11)
    except:
        precision1 = precision1
        recall1 = recall1
        f11 = f11
        print("precision2", sump1 / len(precision1))
        print("recall2", sumr1 / len(recall1))
        print("f12", sumf1 / len(f11))

# for i in precision1:
#     sump1+=i
# for j in recall1:
#     sumr1+=j
# for k in f11:
#     sumf1+=k
#
# # print("precision1",sump/len(precision))
# # print("recall1", sumr / len(recall))
# # print("f11", sumf / len(f1),f1,sumf)
#
# print("precision2",sump1/len(precision1))
# print("recall2", sumr1 / len(recall1))
# print("f12", sumf1 / len(f11))
