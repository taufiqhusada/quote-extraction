import os

if __name__ == "__main__":
    data_path = '/projectnb/multilm/thdaryan/racial_bias/quote-extraction/regex_pipeline/list_year_gun_violence'
    list_files = []
    with open('list_csv_files.txt') as temp_file:
        for filename in temp_file.readlines():
            list_files.append(filename.strip())
    print(len(list_files))

    dict_cnt_year = {}

    for filename in list_files:
        print(filename)
        with open(os.path.join(data_path, f'list_year_gun_violence_{filename[:-4]}.txt')) as temp_file:
            for pair_year_cnt in temp_file.readlines():
                year = int(pair_year_cnt.split()[0])
                cnt = int(pair_year_cnt.split()[1])
                if (year in dict_cnt_year):
                    dict_cnt_year[year] += cnt
                else:
                    dict_cnt_year[year] = cnt

    print(dict_cnt_year)
    output_file = f'summary_year_cnt.csv'
    with open(output_file, 'w') as temp_file:
        temp_file.write("year" + "," + "cnt" + '\n')
        for year in sorted(dict_cnt_year):
            temp_file.write(str(year) + "," + str(dict_cnt_year[year]) + '\n')

  
        

