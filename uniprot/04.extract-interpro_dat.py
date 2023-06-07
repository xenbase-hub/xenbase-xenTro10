#!/usr/bin/env python3
import sys
import gzip

filename_csv = sys.argv[1]
# F6V1J6,NP_001001190.1,NM_001001190.1,GeneID:407851,XB-GENE-5809007

filename_ipr = 'protein2ipr.dat.gz'
# A0A060A0J8      IPR000974       Glycoside hydrolase, family 22, lysozyme        PR00137 21      39

up_list = dict()
f_csv = open(filename_csv, 'r')
for line in f_csv:
    up_id = line.strip().split(",")[0]
    up_list[up_id] = 1
f_csv.close()


f_ipr = gzip.open(filename_ipr, 'rt')
for line in f_ipr:
    tmp_prot_id = line.strip().split("\t")[0]
    if tmp_prot_id in up_list:
        print(line.strip())
f_ipr.close()
