#!/usr/bin/env python3
import sys

filename_out = 'XENTR_xenTro10.gene_symbols_reviewed.XB2023_04.csv'
filename_raw = 'XENTR_xenTro10.gene_symbols_raw.XB2023_04.csv'
# remark,rep_symbol,gene_id,tx_id,prot_id,uniprot_id,ncbi_symbol,uniprot_symbol,xb_symbol,xb_id,diopt_hs1_name, diopt_hs1_id, diopt_hs1_score,diopt_hs2_name, diopt_hs2_id, diopt_hs2_score
# PERFECT,runx1t1,GeneID:100491944,XM_004915148.3,XP_004915205.1,A0A5S6MBM4,runx1t1,runx1t1,runx1t1,XB-GENE-481238,RUNX1T1,862,4,NA,NA,-1

filename_review = 'XENTR_xenTro10.gene_symbols_from_reviewers.XB2023_04.csv'
# NCBI_GeneID,XB_GeneID,GeneSymbol,XB_Symbol,USE_THIS_SYMBOL,QC:curators initials
# GeneID:100489955,XB-GENE-1219042,avpr2.2,avpr2c,avpr2c,cjz

c_orf_list = dict()
f_c_orf = open('C-ORF.2023_04.txt', 'r')
for line in f_c_orf:
    tokens = line.strip().split("\t")
    c_orf_list[tokens[0]] = tokens[1]
f_c_orf.close()

reviewed = dict()
f_review = open(filename_review, 'r')
f_review.readline()
for line in f_review:
    tokens = line.strip().split(",")
    if len(tokens) == 0:
        continue
    gene_id = tokens[0]
    gene_symbol = tokens[4]
    sys.stderr.write("%s %s\n" % (gene_id, gene_symbol))
    reviewed[gene_id] = gene_symbol
f_review.close()

f_raw = open(filename_raw, 'r')
f_out = open(filename_out, 'w')
f_out.write(f_raw.readline())
for line in f_raw:
    tokens = line.strip().split(",")
    rep_symbol = tokens[1]
    gene_id = tokens[2]
    if gene_id in reviewed:
        tokens[1] = reviewed[gene_id]
        tokens[0] += ';Reviewed'
    elif rep_symbol in c_orf_list:
        tokens[1] = c_orf_list[rep_symbol]
        tokens[0] += ';Reviewed_C_ORF'

    f_out.write("%s\n" % ",".join(tokens))
f_out.close()

