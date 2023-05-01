#!/usr/bin/env python3
import gzip

filename_hgnc_raw = 'raw/hgnc_complete_set.2023_04.txt.gz'
filename_out = 'XENTR_xenTro10.gene_names_raw.XB2023_04.csv'

hgnc_info = dict()
gene_symbols = dict()
alias_list = dict()

hs_id2name = dict()

f_out = open(filename_out, 'w')
f_out.write("remark,rep_symbol,gene_id,tx_id,prot_id,uniprot_id,ncbi_symbol,")
f_out.write("uniprot_symbol,xb_symbol,xb_id,")
f_out.write("diopt_hs1_name, diopt_hs1_id, diopt_hs1_score,")
f_out.write("diopt_hs2_name, diopt_hs2_id, diopt_hs2_score\n")

f_hgnc = gzip.open(filename_hgnc_raw, 'rt')
h_hgnc = f_hgnc.readline().split("\t")
for line in f_hgnc:
    tokens = line.strip().split("\t")
    tmp_symbol = tokens[1]
    tmp_name = tokens[2]
    tmp_type = tokens[3].replace(' ', '_')
    tmp_alias_symbols = tokens[8]
    tmp_alias_name = tokens[9]
    tmp_prev_symbols = tokens[10]
    tmp_prev_name = tokens[11]
    alias_list[tmp_symbol] = []

    tmp_entrez_id = 'NA'
    if len(tokens) >= 19:
        tmp_entrez_id = tokens[18]
        hs_id2name[tmp_entrez_id] = tmp_symbol

    gene_symbols[tmp_symbol] = tmp_symbol
    hgnc_info[tmp_symbol] = {'name': tmp_name, 'type': tmp_type}

    for tmp in tmp_alias_symbols.strip().split('|'):
        tmp = tmp.replace('"', '')
        if tmp != '':
            gene_symbols[tmp] = tmp_symbol
            alias_list[tmp_symbol].append(tmp)
    for tmp in tmp_prev_symbols.strip().split('|'):
        tmp = tmp.replace('"', '')
        if tmp != '':
            gene_symbols[tmp] = tmp_symbol
            alias_list[tmp_symbol].append(tmp)

    tmp_alias_str = 'NA'
    if len(alias_list[tmp_symbol]) > 0:
        tmp_alias_str = '|'.join(sorted(alias_list[tmp_symbol]))

f_hgnc.close()

ortho_xt2hs = dict()
filename_diopt = 'DIOPT.Foley2023_04_28/DIOPT2023_04.Hsap_Xtrop_7Tools.tsv.gz'
f_diopt = gzip.open(filename_diopt, 'rt')
f_diopt.readline()
# HSAP	XTROP	FO	IP	OF	PO	SO	SP	PDB	TOTAL
# 15	100497589	1	1	1	1	1	1	1	7
# 16	100492308	1	1	1	1	1	1	1	7
for line in f_diopt:
    tokens = line.strip().split("\t")
    hs_id = tokens[0]
    xt_id = tokens[1]
    tmp_sum = int(tokens[-1].strip())
    if xt_id not in ortho_xt2hs:
        ortho_xt2hs[xt_id] = dict()
    ortho_xt2hs[xt_id][hs_id] = tmp_sum
f_diopt.close()

xb_names = dict()
f_xb = open('XENTR_xenTro10.XB_export.Arshinoff-2023_04_26.csv', 'r')
f_xb.readline()
for line in f_xb:
    tokens = line.strip().split(',')
    ncbi_gene_id = tokens[1]
    xb_gene_id = tokens[2]
    xb_gene_symbol = tokens[6]
    xb_names[ncbi_gene_id] = {'symbol': xb_gene_symbol, 'xb_id': xb_gene_id}
f_xb.close()

filename_raw = 'XENTR_xenTro10.prot_uniprot_ncbi.raw.2023_04.csv'
f_list = open(filename_raw, 'r')
# GeneID:100491944,XM_004915148.3,XP_004915205.1,runx1t1,A0A5S6MBM4,runx1t1
# GeneID:100487513,XM_002937850.5,XP_002937896.1,ano10,A0A6I8Q0X6,ano10

for line in f_list:
    tokens = line.strip().split(",")
    gene_id = tokens[0].replace('GeneID:', '')
    tx_id = tokens[1]
    prot_id = tokens[2]
    ncbi_symbol = tokens[3]
    uniprot_id = tokens[4]
    uniprot_symbol = tokens[5]

    xb_symbol = 'NA'
    xb_id = 'NA'
    if gene_id in xb_names:
        if xb_names[gene_id]['symbol'] != '':
            xb_symbol = xb_names[gene_id]['symbol']
            xb_id = 'XB-GENE-%s' % xb_names[gene_id]['xb_id']

    ortho_hs1_id = 'NA'
    ortho_hs1_name = 'NA'
    ortho_hs1_score = -1
    ortho_hs2_id = 'NA'
    ortho_hs2_name = 'NA'
    ortho_hs2_score = -1
    if gene_id in ortho_xt2hs:
        sorted_hs_list = sorted(ortho_xt2hs[gene_id].keys(),
                                key=ortho_xt2hs[gene_id].get, reverse=True)
        ortho_hs1_id = sorted_hs_list[0]
        if ortho_hs1_id in hs_id2name:
            ortho_hs1_name = hs_id2name[ortho_hs1_id]
        ortho_hs1_score = ortho_xt2hs[gene_id][ortho_hs1_id]

        if len(sorted_hs_list) > 1:
            ortho_hs2_id = sorted_hs_list[1]
            if ortho_hs2_id in hs_id2name:
                ortho_hs2_name = hs_id2name[ortho_hs2_id]
            ortho_hs2_score = ortho_xt2hs[gene_id][ortho_hs2_id]

    hs_name_lower = ortho_hs1_name.lower()

    tmp_tag = 'NA'
    rep_symbol = 'NA'
    if ncbi_symbol == hs_name_lower or \
       ncbi_symbol.split('.')[0] == hs_name_lower:
        rep_symbol = ncbi_symbol

        if ncbi_symbol == xb_symbol:
            tmp_tag = 'GOOD'
            if ncbi_symbol == uniprot_symbol:
                tmp_tag = 'PERFECT'
            else:
                tmp_tag = 'GOOD;CheckUniProt'
        elif ncbi_symbol == uniprot_symbol:
            tmp_tag = 'GOOD;CheckXenbase'
        else:
            tmp_tag = 'REVIEW-NCBI'

    elif xb_symbol == hs_name_lower or \
            xb_symbol.split('.')[0] == hs_name_lower:

        rep_symbol = xb_symbol
        if xb_symbol == uniprot_symbol:
            tmp_tag = 'GOOD;CheckNCBI'
        else:
            tmp_tag = 'REVIEW-Xenbase'

    elif uniprot_symbol == hs_name_lower or \
            uniprot_symbol.split('.')[0] == hs_name_lower:
        rep_symbol = uniprot_symbol
        if uniprot_symbol == xb_symbol:
            tmp_tag = 'GOOD;CheckNCBI'
        elif uniprot_symbol == ncbi_symbol:
            tmp_tag = 'GOOD;CheckXenbase'
        else:
            tmp_tag = 'REVIEW-UniProt'
    else:
        if ncbi_symbol == xb_symbol:
            rep_symbol = ncbi_symbol
            if ncbi_symbol == uniprot_symbol:
                tmp_tag = 'PERFECT;CheckHuman'
            else:
                tmp_tag = 'GOOD;CheckHuman;CheckUniProt'
        elif ncbi_symbol == uniprot_symbol:
            rep_symbol = ncbi_symbol
            tmp_tag = 'GOOD;CheckHuman;CheckXenbase'
        elif xb_symbol == uniprot_symbol:
            rep_symbol = xb_symbol
            tmp_tag = 'GOOD;CheckHuman;CheckNCBI'
        else:
            rep_symbol = 'NA'
            tmp_tag = 'REVIEW'

    if rep_symbol == 'NA':
        rep_symbol = ncbi_symbol

    f_out.write("%s,%s,GeneID:%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d,%s,%s,%d\n" %
                (tmp_tag, rep_symbol, gene_id, tx_id, prot_id, uniprot_id,
                 ncbi_symbol, uniprot_symbol, xb_symbol, xb_id,
                 ortho_hs1_name, ortho_hs1_id, ortho_hs1_score,
                 ortho_hs2_name, ortho_hs2_id, ortho_hs2_score))
f_out.close()
