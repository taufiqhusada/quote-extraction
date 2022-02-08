#!/bin/bash -l

#$ -P multilm
#$ -l h_rt=200:00:00   # Specify the hard time limit for the job
#$ -pe omp 20
#$ -N quote_extraction
#$ -j y               # Merge the error and output streams into a single file
#$ -V
#$ -m e

python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_0.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_1.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_2.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_3.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_4.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_5.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_6.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_7.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_8.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_9.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_10.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_11.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_12.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_13.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_14.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_15.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_16.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_17.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_18.csv &
python quote_extraction_one_file.py LexisNexis_BostonMedia_NewsArticles_unique_19.csv &
wait
