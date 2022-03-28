import os
import pandas as pd
import spacy
from tqdm import tqdm 
import json
import sys
import gc
import glob
import numpy as np

NAMED_ENTITY_SET = {'ORG', 'LOC', 'GEO', 'GPE'}

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    list_files = glob.glob(f'/projectnb/multilm/yusuf/racial_bias/LexisNexis/output/data/*/*.csv')
    list_files = np.sort(list_files)
    for filename in tqdm(list_files):
        df_chunk = pd.read_csv(filename, error_bad_lines=False,  encoding='utf8', engine='python')
        try:
            list_json_result = []
            doc_ids = df_chunk['DOC-ID'].values

            i = 0
            for id in doc_ids:
                list_json_result.append({'doc_id': str(id), 'ORG':[], 'LOC':[], 'GEO':[], 'GPE':[]})
                i += 1

            i = 0
            batch_text_raw = df_chunk['lede'].values
            batch_text = [str(item) for item in batch_text_raw]
            for doc in nlp.pipe(batch_text, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
                try:
                    for ent in doc.ents:
                        text = str(ent.text)
                        if ((ent.label_ in NAMED_ENTITY_SET) and (text not in list_json_result[i][ent.label_])):
                            list_json_result[i][ent.label_].append(text)
                except Exception as e:
                    with open('result_NER_doc_complete/errors_all.txt', 'a') as f:
                        print(str(e))
                        f.write(str(list_id_from_name_extraction[i]) + " " + str(e) + '\n')
                i+=1

            with open('result_NER_doc_complete/NER_all.jsonl', mode='a+', encoding='utf-8') as f:
                for res in list_json_result:
                    json.dump(res, f)
                    f.write('\n')

            del df_chunk
            gc.collect()

        except Exception as e:
            with open('result_NER_doc_complete/errors_all.txt', 'a') as f:
                print(str(e))
                f.write(str(e) + '\n')    
