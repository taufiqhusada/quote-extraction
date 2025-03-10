import os
import pandas as pd
import spacy
from tqdm import tqdm 
import json
import sys
import gc

NAMED_ENTITY_SET = {'ORG', 'LOC', 'GEO', 'GPE'}

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    filename = '/projectnb/multilm/yusuf/racial_bias/LexisNexis/extracted_final.csv'
    
    for df_chunk in tqdm(pd.read_csv(filename, chunksize=10**4, header=None,  error_bad_lines=False,  encoding='utf8', engine='python')):
        try:
            df_chunk.rename(columns={0: 'id_from_name_extraction', 1:'sent', 2:'names', 3:'start', 4:'end', 5:'source_type', 6:'DOC-ID'}, inplace=True)
            list_json_result = []
            doc_ids = df_chunk['DOC-ID'].values
            list_id_from_name_extraction = df_chunk['id_from_name_extraction'].values
            i = 0
            for id in doc_ids:
                list_json_result.append({'doc_id': str(id), 'id_from_name_extraction': str(list_id_from_name_extraction[i]), 'ORG':[], 'LOC':[], 'GEO':[], 'GPE':[]})
                i += 1

            i = 0
            batch_text_raw = df_chunk['sent'].values
            batch_text = [str(item) for item in batch_text_raw]
            for doc in nlp.pipe(batch_text, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
                try:
                    for ent in doc.ents:
                        text = str(ent.text)
                        if ((ent.label_ in NAMED_ENTITY_SET) and (text not in list_json_result[i][ent.label_])):
                            list_json_result[i][ent.label_].append(text)
                except Exception as e:
                    with open('result_alligned_NER/errors_all.txt', 'a') as f:
                        print(str(e))
                        f.write(str(list_id_from_name_extraction[i]) + " " + str(e) + '\n')
                i+=1

            with open('result_alligned_NER/NER_all.jsonl', mode='a+', encoding='utf-8') as f:
                for res in list_json_result:
                    json.dump(res, f)
                    f.write('\n')

            del df_chunk
            gc.collect()

        except Exception as e:
            with open('result_alligned_NER/errors_all.txt', 'a') as f:
                print(str(e))
                f.write(str(e) + '\n')    
