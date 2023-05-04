#!/usr/bin/env python3
import sys

filename_csv = "../2023_04/XENTR_xenTro10.gene_symbols.XB2023_04.csv"
#remark,rep_symbol,gene_id,tx_id,prot_id,uniprot_id,ncbi_symbol,uniprot_symbol,xb_symbol,xb_id,diopt_hs1_name, diopt_hs1_id, diopt_hs1_score,diopt_hs2_name, diopt_hs2_id, diopt_hs2_score
#PERFECT,runx1t1,GeneID:100491944,XM_004915148.3,XP_004915205.1,A0A5S6MBM4,runx1t1,runx1t1,runx1t1,XB-GENE-481238,RUNX1T1,862,4,NA,NA,-1

update_symbols = dict()
update_xb_ids = dict()
f_csv = open(filename_csv, 'r')
h_csv = f_csv.readline().strip().split(',')
for line in f_csv:
    tokens = line.strip().split(",")
    gene_symbol = tokens[1]
    gene_id = tokens[2]
    update_symbols[gene_id] = gene_symbol
    update_xb_ids[gene_id] = tokens[9]
f_csv.close()

#>runx1t1|XP_004915205.1|XM_004915148.3|GeneID:100491944 xb_gene_id=XB-GENE-481238 uniprot=runx1t1|A0A5S6MBM4
#>ano10|XP_002937896.1|XM_002937850.5|GeneID:100487513 xb_gene_id=XB-GENE-955754 uniprot=ano10|A0A6I8Q0X6

filename_fa = 'XENTR_xenTro10.XB2023_04.raw.prot_combined.fa'
filename_all_out = 'XENTR_xenTro10.XB2023_04.prot_nr_all.fa'
filename_rep_out = 'XENTR_xenTro10.XB2023_04.prot_nr_rep.fa'

seq_len = dict()
seq_list = dict()
f_fa = open(filename_fa, 'r')
f_out = open(filename_all_out, 'w')
for line in f_fa:
    if line.startswith('>'):
        tokens = line.strip().lstrip('>').split()
        ncbi_tokens = tokens[0].split('|')
        uniprot_tokens = tokens[2].split('|')
        tmp_gene_id = ncbi_tokens[3]
        new_symbol = update_symbols[tmp_gene_id]
        new_xb_id = update_xb_ids[tmp_gene_id]
        tmp_ncbi_h = '%s|%s' % (new_symbol, '|'.join(ncbi_tokens[1:]))
        tmp_h = '%s xb_gene_id=%s uniprot=%s' % (tmp_ncbi_h, new_xb_id, uniprot_tokens[1])
        seq_list[tmp_h] = []
        if tmp_gene_id not in seq_len:
            seq_len[tmp_gene_id] = dict()
        seq_len[tmp_gene_id][tmp_h] = 0
        f_out.write('>%s\n' % tmp_h)
    else:
        seq_len[tmp_gene_id][tmp_h] += len(line.strip())
        f_out.write("%s\n" % line.strip())
        seq_list[tmp_h].append(line.strip())
f_fa.close()
f_out.close()

f_rep = open(filename_rep_out, 'w')
for tmp_gene, tmp in seq_len.items():
    tmp_h_list = sorted(tmp.keys(), key=tmp.get, reverse=True)
    rep_h = tmp_h_list[0]
  
    f_rep.write(">%s\n%s\n" % (rep_h, '\n'.join(seq_list[rep_h])))
f_rep.close()
