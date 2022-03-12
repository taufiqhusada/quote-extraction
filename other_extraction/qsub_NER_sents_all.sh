#!/bin/bash -l

#$ -P multilm
#$ -l h_rt=99:00:00   # Specify the hard time limit for the job
#$ -pe omp 24
#$ -N NER_sents_all
#$ -j y               # Merge the error and output streams into a single file
#$ -V
#$ -m e

python NER_extraction_sents_all.py
