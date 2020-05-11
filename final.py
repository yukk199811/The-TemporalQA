from gettingAnswer import *
import sys



def getit(doc,rho,predicate_num,prop,vec):

    try:
        using_first_function = get_response(doc, rho)
        # Calling for wikidata id
        objs = using_first_function[0][0]
        ids = using_first_function[0][1][1]
        rho1 = using_first_function[0][1][0]
        wiki_id = get_wikiid(objs, ids)
        # getting subgraph
        graph = get_wikidata_id_aida(wiki_id)
        after1 = get_question_pos(doc,rho)[0]
        annot_doc1 = get_question_pos(doc,rho)[1]
        filtered = get_question_pos(doc,rho)[2]
        time_IN = get_question_pos(doc,rho)[3]
        time_CD = get_question_pos(doc,rho)[4]
        ps_wdlabel = get_p(graph)
        # with open('alt_name1.json', 'r') as file_obj10:
        #     property_alt_name = json.load(file_obj10)
        # file_obj10.close()
        #
        # with open('word_vector1.json', 'r') as file_obj11:
        #     load_vec_dict = json.load(file_obj11)
        # file_obj11.close()

        sim=calculation(ps_wdlabel,vec, filtered,prop)[0]
        # num=calculation(ps_wdlabel,load_vec_dict, filtered,property_alt_name)[1]
        dic = get_high_similarity(predicate_num, sim)
        answer = getting_my_answer(final_process(dic), wiki_id, time_IN, time_CD)[0]
        # calculate confidence of the final answers

        # print the final answer list
        return my_answer_with_possibility(answer,rho1)
    except IndexError as errm:
        print('Entity recognizing failure:', errm)

# root = os.getcwd()
# name1 = "alt_name1.json"
# name2 = "word_vector1.json"
# with open(os.path.join(root, name1), 'r') as file_obj10:
#     property_alt_name = json.load(file_obj10)
# file_obj10.close()
#
# with open(os.path.join(root, name2), 'r') as file_obj11:
#     load_vec_dict = json.load(file_obj11)
# file_obj11.close()
# doc='which team did messi plays for in 2004'
# rho=0.1
# predicate_num=6
# prop=property_alt_name
# vec=load_vec_dict
# print(getit(doc,rho,predicate_num,prop,vec))
if __name__ == '__main__':
    root = os.getcwd()
    name1 = "alt_name1.json"
    name2="word_vector1.json"
    with open(os.path.join(root, name1), 'r') as file_obj10:
        property_alt_name = json.load(file_obj10)
    file_obj10.close()

    with open(os.path.join(root, name2), 'r') as file_obj11:
        load_vec_dict = json.load(file_obj11)
    file_obj11.close()

    # doc = "what was the first star war movie?"
    doc = ' '.join(sys.argv[3:])
    rho = float(sys.argv[1])
    predicate_num = int(sys.argv[2])
    # print(getit(doc,rho,predicate_num,property_alt_name,load_vec_dict))

    print(getit(doc,0.1,7,property_alt_name,load_vec_dict))