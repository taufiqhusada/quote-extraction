import csv
import pandas as pd
import os
from tqdm import tqdm

def partial_search_in_string(s):
    s = str(s)
    candidates = ['gun', 'firearm', 'nra', '2nd amendment', 'second amendment', 'shooting', 'ar15', 'assault weapon', 'rifle', 'brady act', 'brady bill']

    splitted_s = s.lower().split()
    len_splitted_s = len(splitted_s)
    for i in range(len_splitted_s):
        for c in candidates:
            target = splitted_s[i]
            if (i < len_splitted_s - 1 and len(c.split())==2):
                target += " " + splitted_s[i+1]
            # print(target)
            len_c = len(c)
            if (len(target) < len_c):
                continue

            if (c == target[:len_c]):
                # print(c, target[:len_c])
                return True
    return False

def partial_search_in_row_csv(row):
    col_to_look = ['hl1', 'lede', 'body']
    for col in col_to_look:
        if partial_search_in_string(row[col]):
            return True

    return False

# print(partial_search_in_string('gun violence'))
# print(partial_search_in_string('guns violence'))
# print(partial_search_in_string('assault weapon'))
# print(partial_search_in_string('agun 2nd amendment'))

if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/raw_data/data/145223'
    list_files = []
    with open('list_csv_files.txt') as temp_file:
        for filename in temp_file.readlines():
            list_files.append(filename.strip())
    print(len(list_files))
    for filename in list_files:
        print(filename)
        inp = os.path.join(data_path, filename)
        df = pd.read_csv(inp, error_bad_lines=False,  encoding='utf8', engine='python')

        list_doc_id_gun_violence = []
        dict_cnt_year = {}
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            if (partial_search_in_row_csv(row)):
                print(row['DOC-ID'], row['pubYear'])
                list_doc_id_gun_violence.append(row['DOC-ID'])

                pub_year = int(row['pubYear'])
                if (pub_year in dict_cnt_year):
                    dict_cnt_year[pub_year] += 1
                else:
                    dict_cnt_year[pub_year] = 1

        #print(list_doc_id_gun_violence)
        print(len(list_doc_id_gun_violence))
        #print(dict_cnt_year)

        output_file = f'list_id_gun_violence/list_id_gun_violence_{filename[:-4]}.txt'
        with open(output_file, 'w') as temp_file:
            for id in list_doc_id_gun_violence:
                temp_file.write(str(id) + '\n')

        output_file = f'list_year_gun_violence/list_year_gun_violence_{filename[:-4]}.txt'
        with open(output_file, 'w') as temp_file:
            for year in dict_cnt_year:
                temp_file.write(str(year) + " " + str(dict_cnt_year[year]) + '\n')
        
