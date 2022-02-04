import os
import pandas as pd
import spacy
from tqdm import tqdm 
import json

NAMED_ENTITY_SET = {'ORG', 'LOC', 'GEO', 'GPE'}

if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/complete_raw_data_unique'
    nlp = spacy.load("en_core_web_sm")
    print(nlp.pipe_names)

    list_files = [f'LexisNexis_BostonMedia_NewsArticles_unique_{i}.csv' for i in range(20)]
    
    for filename in list_files:
        try:
            print(filename)
            csv_path = os.path.join(data_path, filename)
            df = pd.read_csv(csv_path, error_bad_lines=False,  encoding='utf8', engine='python')

            json_result = {'data':[], 'errors':[]}        
            doc_ids = df['DOC-ID'].values
            for id in doc_ids:
                json_result['data'].append({'doc_id': str(id), 'ORG':[], 'LOC':[], 'GEO':[], 'GPE':[]})

            i = 0
            batch_text_raw = df['lede'].values
            batch_text = [str(item) for item in batch_text_raw]	
            for doc in tqdm(nlp.pipe(batch_text, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]), total=len(doc_ids)):
                try:
                    for ent in doc.ents:
                        text = str(ent.text)
                        if ((ent.label_ in NAMED_ENTITY_SET) and (text not in json_result['data'][i][ent.label_])):
                            json_result['data'][i][ent.label_].append(text)
                except Exception as e:
                    with open('result_NER/errors.txt', 'w') as f:
                        print(filename, str(e))
                        f.write(filename + " " + str(e))
                i+=1
            
            i = 0
            batch_text_raw = df['body'].values
            batch_text = [str(item) for item in batch_text_raw]
            for doc in tqdm(nlp.pipe(batch_text, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]), total=len(doc_ids)):
                try:
                    for ent in doc.ents:
                        text = str(ent.text)
                        if ((ent.label_ in NAMED_ENTITY_SET) and (text not in json_result['data'][i][ent.label_])):
                            json_result['data'][i][ent.label_].append(text)
                except Exception as e:
                    with open('result_NER/errors.txt', 'w') as f:
                        print(filename, str(e))
                        f.write(filename + " " + str(e))
                i+=1

            output_json_file = open(f'result_NER/NER_{filename[:-4]}.json', 'w')
            json.dump(json_result, output_json_file, indent=4)
            output_json_file.close()
            
        except Exception as e:
            with open('result_NER/errors.txt', 'w') as f:
                print(filename, str(e))
                f.write(filename + " " + str(e))

        
