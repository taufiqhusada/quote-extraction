import sys
import logging
import json
import spacy
from os import listdir
from os.path import isfile, join
import pandas as pd
from tqdm import tqdm
from utils.transform_quotes import transform_all_quotes_to_straight_double_quotes

from utils.quote_extraction import extract_quotes_and_sentence_speaker

# Utility functions
def check_if_fname_exists(fname):
    import os
    return os.path.exists(fname)


def load_file(fname):
    with open(fname, 'rt') as fin:
        return fin.read()


# def get_text_from_input(input_):
#     """ Get text from `input` provided.
#         Check if input provided is a file name. If so, load and return contents.
#         Else: Assume input provided is the input text.
#         Returns: text to be processed:str """
#     if check_if_fname_exists(input_):
#         return load_file(input_)
#     else:
#         return input_

def get_text_from_input(input_):
    return transform_all_quotes_to_straight_double_quotes(input_)


# Quote extraction
def run_one(text, model_name='en_core_web_trf', debug=True):
    nlp = spacy.load(model_name)
    results = extract_quotes_and_sentence_speaker(text, nlp, debug)
    return results

def write_jsonl(data, path):
    import srsly
    srsly.write_jsonl(path, [d.to_dict() for d in data])
    logging.info(f"Output witten to {output_path}")

LIST_COL = ['doc_id','quote_text','speaker','quote_text_optional_second_part','QUOTE_TYPE','additional_cue','quote_text_optional_third_part']
    
if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/raw_data/data/145223'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    for filename in onlyfiles:
        inp = pd.read_csv(join(data_path, filename), encoding="utf8")
        if (len(inp) > 10000):
             print("more than 10000")
             continue
        inps_hl1 = inp['hl1'].values
        inps_lede = inp['lede'].values
        inps_body = inp['body'].values
        doc_ids = inp['DOC-ID'].values
        output_tsv_file = open(f'results_tsv/result_{filename[:-4]}.tsv', 'w')
        output_tsv_file.write('doc_id\tquote_text\tspeaker\tquote_text_optional_second_part\tQUOTE_TYPE\tadditional_cue\tquote_text_optional_third_part\n')
        for i in tqdm(range(len(inps_body))):
            try:
                text = get_text_from_input(str(inps_hl1[i]) + " " + str(inps_lede[i]) + " " + str(inps_body[i]))
                # if (i==0):
                   #  print(text)
                output, sentences = run_one(text, debug=False)
                if (len(output) != 0 and len(sentences) != 0):
                    print(i)
                    print(i, output)
                    output = [d.to_dict() for d in output]
                    for item in output:
                      
                        item['doc_id'] = doc_ids[i]
                        string_item = ""
                        for col in LIST_COL:
                              if (col in item and item[col]!=None):
                                    string_item += str(item[col]) + "\t"
                              else:
                                    string_item += "\t"
                        
                        
                        # print(string_item)
                        output_tsv_file.write(string_item[:-1] + '\n')
                              
            except Exception as e: 
                print(filename, i, e)
                              
        output_tsv_file.close()
        
            
        
