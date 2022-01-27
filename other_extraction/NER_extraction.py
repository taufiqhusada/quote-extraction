import os
import pandas as pd
import spacy
from tqdm import tqdm 
import json

NAMED_ENTITY_SET = {'ORG', 'LOC', 'GEO', 'GPE'}

def NER_from_df(hl1, lede, body, doc_id, nlp):
    dict_result = {'doc_id': doc_id, 'ORG':[], 'LOC':[], 'GEO':[], 'GPE':[]}

    if (hl1):
        doc = nlp(str(hl1))
        for ent in doc.ents:
            if ((ent.label_ in NAMED_ENTITY_SET) and (ent.text not in dict_result[ent.label_])):
                dict_result[ent.label_].append(ent.text)
    if (lede):
        doc = nlp(str(lede))
        for ent in doc.ents:
            if ((ent.label_ in NAMED_ENTITY_SET) and (ent.text not in dict_result[ent.label_])):            
                dict_result[ent.label_].append(ent.text)

    if (body):
        doc = nlp(str(body))
        for ent in doc.ents:
            if ((ent.label_ in NAMED_ENTITY_SET) and (ent.text not in dict_result[ent.label_])):            
                dict_result[ent.label_].append(ent.text)
    
    return dict_result


if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/raw_data/data/145223'
    nlp = spacy.load("en_core_web_trf")

    list_files = []
    with open('../regex_pipeline/list_csv_files.txt') as temp_file:
        for filename in temp_file.readlines():
            list_files.append(filename.strip())
    
    for filename in list_files:
        print(filename)
        csv_path = os.path.join(data_path, filename)
        df = pd.read_csv(csv_path, error_bad_lines=False,  encoding='utf8', engine='python')

        inps_hl1 = df['hl1'].values
        inps_lede = df['lede'].values
        inps_body = df['body'].values
        doc_ids = df['DOC-ID'].values

        json_result = {'data':[], 'errors':[]}
        
        for i in tqdm(range(len(inps_body))):
            try:
                result_this_id = NER_from_df(inps_hl1[i], inps_lede[i], inps_body[i], doc_ids[i], nlp)
                json_result['data'].append(result_this_id)
            except Exception as e: 
                print(filename, i, e)
                json_result['errors'].append(str(e))

        output_json_file = open(f'results_NER/NER_{filename[:-4]}.json', 'w')
        json.dump(json_result, output_json_file, indent=4)
        output_json_file.close()
        print('len', str(len(json_result['data'])))
