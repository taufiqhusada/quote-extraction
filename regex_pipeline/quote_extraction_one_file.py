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
def run_one(text, model_name='en_core_web_sm', debug=True):
    nlp = spacy.load(model_name)
    results = extract_quotes_and_sentence_speaker(text, nlp, debug)
    return results

def write_jsonl(data, path):
    import srsly
    srsly.write_jsonl(path, [d.to_dict() for d in data])
    logging.info(f"Output witten to {output_path}")
    
if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/complete_raw_data_unique'
    
    filename = sys.argv[1]
    cnt_quotes = 0
    print(filename)

    csv_path = join(data_path, filename)
    try:
        inp = pd.read_csv(csv_path, error_bad_lines=False,  encoding='utf8', engine='python')
        print(inp.head(1))
        doc_ids = inp['DOC-ID'].values
    except:
        inp = pd.read_csv(csv_path, error_bad_lines=False,  encoding='utf8', engine='python', names=['hl1','author','lede','body','DOC-ID','pubDay','pubMonth','pubYear','pubName','filename','Unique_Id'])
        print(inp.head(1))
        doc_ids = inp['DOC-ID'].values

    inps_body = inp['body'].values
    jsonl_output_file = open(f'result_json/quote_extraction_{filename}.jsonl', mode='a+', encoding='utf-8')
    for i in tqdm(range(len(inps_body))):
        try:
            text = get_text_from_input(str(inps_body[i]))

            output, sentences = run_one(text, debug=False)
            if (len(output) != 0 and len(sentences) != 0):
                cnt_quotes += 1
                
                output = [d.to_dict() for d in output]
                for item in output:

                    item['DOC-ID'] = str(doc_ids[i])
                
                    # print(string_item)
                    json.dump(item, jsonl_output_file)
                    jsonl_output_file.write('\n')

        except Exception as e: 
            print(filename, i, e)

    jsonl_output_file.close()
    print(cnt_quotes)
        
