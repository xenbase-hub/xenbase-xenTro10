#!/usr/bin/env python3
import gzip

filename_hgnc_raw = 'raw/hgnc_complete_set.2023_04.txt.gz'
filename_csv = 'XENTR_xenTro10.gene_symbols.XB2023_04.csv'
filename_out = 'XENTR_xenTro10.gene_symbols_vs_HGNC.XB2023_04.csv'

hgnc_info = dict()
gene_symbols = dict()
alias_list = dict()

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


f_csv = open(filename_csv, 'r')
f_csv.readline()
out_lines = []
for line in f_csv:
    tokens = line.strip().split(",")
    tmp_rep_symbol = tokens[1]
    tmp_rep_hs_symbol = tmp_rep_symbol.upper()
    tmp_gene_id = tokens[2]

    if tmp_rep_hs_symbol in gene_symbols:
        if tmp_rep_hs_symbol == gene_symbols[tmp_rep_hs_symbol]:
            out_lines.append("MATCH,%s,%s,%s" % (tmp_gene_id, tmp_rep_symbol, tmp_rep_hs_symbol)) 
        else:
            out_lines.append("ALIAS_MATCH,%s,%s,%s" % (tmp_gene_id, tmp_rep_symbol, gene_symbols[tmp_rep_hs_symbol])) 
    else:
        tmp_rep_hs_stripped = tmp_rep_hs_symbol.split('.')[0]
        if tmp_rep_hs_stripped in gene_symbols:
            if tmp_rep_hs_stripped == gene_symbols[tmp_rep_hs_stripped]:
                out_lines.append("STRIP_MATCH,%s,%s,%s" % (tmp_gene_id, tmp_rep_symbol, tmp_rep_hs_stripped))
            else:
                out_lines.append("STRIP_ALIAS_MATCH,%s,%s,%s" % (tmp_gene_id, tmp_rep_symbol, gene_symbols[tmp_rep_hs_stripped]))
        else:
            out_lines.append("NO_MATCH,%s,%s,NA" % (tmp_gene_id, tmp_rep_symbol))
f_csv.close()

f_out = open(filename_out, 'w')
for tmp_line in sorted(list(set(out_lines))):
    f_out.write("%s\n" % tmp_line)
f_out.close()
