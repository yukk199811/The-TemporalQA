import requests
import time
import json
from functools import lru_cache
import operator
import sys



# doc="Which team did Messi play for in 2004?"

"""entity linking"""


def get_response(ques,Wiki_Threshold):
    tagme_ent = {}
    after_response={}
    tagme_ent['spot'] = []
    after_response1 = []

    req_string = 'https://tagme.d4science.org/tagme/tag?lang=en&include_abstract=true&include_categories=true&gcube-token=9dc5f6c0-3040-411b-9687-75ca53249072-843339462&text=' + ques  # .encode('utf-8')

    try:
        r = requests.get(req_string)
        wiki = r.json()
        # print wiki
        annotations = wiki['annotations']
        # print "Annotations ",wiki,annotations
        flag = 0
        file_name = 'entity_linking.json'
        with open(file_name, 'w') as file_obj:
            json.dump(annotations, file_obj)
        file_obj.close()
        for doc in annotations:
            if doc['rho'] >= Wiki_Threshold:
                tagme_ent['spot'].append((doc['spot'], doc['title'], doc['rho'], doc['id']))
                # print "Wiki added ",doc['rho'],doc['spot'], doc['dbpedia_categories']

        for i in range(len(tagme_ent['spot'])):
            after_response[tagme_ent['spot'][i][1]] = [tagme_ent['spot'][i][2],tagme_ent['spot'][i][3]]
        #sorting
        after_response1 = sorted(after_response.items(),key=lambda x:x[1],reverse=True)

        file_name = 'afterResponse.json'
        with open(file_name, 'w') as file_obj:
            after_responses = json.dumps(after_response1)
            json.dump(after_responses, file_obj)
        file_obj.close()

    except:
        print("TAGME Problem ", ques)
    finally:
        return after_response1




"""getting wikidata subgraph"""

@lru_cache()
def get_wikidata_id_aida(wiki_id):
    try:
        # print "Link is ",link

        url = 'https://query.wikidata.org/sparql'
        query = """
        SELECT distinct ?subject ?subjectLabel ?p ?wdLabel ?statement ?statementLabel ?ps ?ps_object ?ps_objectLabel 
        ?pq ?wdpqLabel ?pq_object ?pq_objectLabel {
          VALUES(?subject){(wd:"""+wiki_id+""")}
          ?subject ?p ?statement.
          ?statement ?ps ?ps_object.
          ?wd wikibase:claim ?p.
          ?wd wikibase:statementProperty ?ps.
          OPTIONAL {?statement ?pq ?pq_object .
                  ?wdpq wikibase:qualifier ?pq .}
          SERVICE wikibase:label {bd:serviceParam wikibase:language 'en'}}
        ORDER BY ?statement ?ps ?ps_object
    	    """

        r = requests.get(url, params={'format': 'json', 'query': query}, timeout=1000)
        datas = r.json()
        file_name = 'knowledgeGraph.json'
        with open(file_name, 'w') as file_obj:
            json.dump(datas, file_obj)
        file_obj.close()
        # print data
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    finally:
        return datas
#getting wiki id of the named-entity
@lru_cache()
def get_wikiid(obj,id):
    try:
        data=''
        try:

            url = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles='+obj+'&format=json'
            r = requests.get(url, params={'format': 'json'}, timeout=1000)
            data = r.json()['query']['pages'][str(id)]['pageprops']['wikibase_item']
        except KeyError:
            url = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search='+obj+'&language=en&limit=20&format=json'
            r = requests.get(url, params={'format': 'json'}, timeout=1000)
            data = r.json()['search'][0]['id']


    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    finally:
        return data













