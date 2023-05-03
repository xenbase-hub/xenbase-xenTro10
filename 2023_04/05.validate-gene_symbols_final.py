#!/usr/bin/env python3

# remark,rep_symbol,gene_id,tx_id,prot_id,uniprot_id,ncbi_symbol,uniprot_symbol,xb_symbol,xb_id,diopt_hs1_name, diopt_hs1_id, diopt_hs1_score,diopt_hs2_name, diopt_hs2_id, diopt_hs2_score
# PERFECT,runx1t1,GeneID:100491944,XM_004915148.3,XP_004915205.1,A0A5S6MBM4,runx1t1,runx1t1,runx1t1,XB-GENE-481238,RUNX1T1,862,4,NA,NA,-1

gene_id2name = dict()

filename_csv = 'XENTR_xenTro10.gene_symbols.XB2023_04.csv'

count_diff = 0
f_csv = open(filename_csv, 'r')
for line in f_csv:
    tokens = line.strip().split(",")
    tmp_symbol = tokens[1]
    tmp_gene_id = tokens[2]
    if tmp_gene_id not in gene_id2name:
        gene_id2name[tmp_gene_id] = tmp_symbol
    elif gene_id2name[tmp_gene_id] != tmp_symbol:
        count_diff += 1
        print("Diff_symbol: %s %s %s" % (tmp_gene_id, gene_id2name[tmp_gene_id], tmp_symbol))
f_csv.close()

if count_diff == 0:
    print("Hooray! Good to go!")
