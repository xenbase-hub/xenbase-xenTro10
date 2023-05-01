#!/usr/bin/env python3
import sys

filename_review = 'XENTR_xenTro10.gene_names_reviewed.XB2023_04.csv'
filename_out = 'XENTR_xenTro10.gene_names.XB2023_04.csv'

symbol2id = dict()
id2symbol = dict()
id2ncbi = dict()

f_raw = open(filename_review, 'r')
h_raw = f_raw.readline().strip()
for line in f_raw:
    tokens = line.strip().split(",")
    tmp_symbol = tokens[1]
    tmp_gene_id = tokens[2]
    if tmp_symbol not in symbol2id:
        symbol2id[tmp_symbol] = []
    symbol2id[tmp_symbol].append(tmp_gene_id)

    if tmp_gene_id not in symbol2id:
        id2symbol[tmp_gene_id] = []
    id2symbol[tmp_gene_id].append(tmp_symbol)

    id2ncbi[tmp_gene_id] = tokens[6]
f_raw.close()

sys.stderr.write("# Genes: %d\n" % len(id2symbol))
sys.stderr.write("# Symbols: %d\n" % len(symbol2id))

for tmp_id in id2symbol.keys():
    if len(id2symbol[tmp_id]) > 1:
        sys.stderr.write("MultiSymbol: %s\n" % tmp_id)

revert_ids = dict()
for tmp_symbol in symbol2id.keys():
    tmp_id_list = list(set(symbol2id[tmp_symbol]))
    if len(tmp_id_list) > 1:
        for tmp_id in tmp_id_list:
            sys.stderr.write("MultiID: %s %s %s\n" %
                             (tmp_symbol, tmp_id, id2ncbi[tmp_id]))
            revert_ids[tmp_id] = id2ncbi[tmp_id]

f_raw = open(filename_review, 'r')
h_raw = f_raw.readline().strip()

f_out = open(filename_out, 'w')
f_out.write("%s\n" % h_raw)
for line in f_raw:
    tokens = line.strip().split(",")
    tmp_symbol = tokens[1]
    tmp_gene_id = tokens[2]
    if tmp_gene_id in revert_ids:
        tokens[0] += ';Reverted'
        tokens[1] = revert_ids[tmp_gene_id]
    f_out.write("%s\n" % ",".join(tokens))
f_out.close()
