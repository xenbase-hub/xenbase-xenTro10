#!/usr/bin/env python3
import sys

filename_gene_info = '../XENTR_gene_info.active.tsv'
# NCBI_GENE	XB_GENE	GENE_SYMBOL	GENE_NAME
# GeneID:100036770	XB-GENE-1007455	cyp2a6.9.L	cytochrome P450 family 2 subfamily A member 6 gene 9 L homeolog
# GeneID:100036776	XB-GENE-17332265	mpst.S	mercaptopyruvate sulfurtransferase S homeolog

count_genes = 0
count_ncbi_NA = 0
count_xb_NA = 0
count_symbol_NA = 0

ncbi_genes = dict()
xb_genes = dict()
gene_symbols = dict()
f_gene = open(filename_gene_info, 'r')
for line in f_gene:
    if line.startswith('#'):
        continue

    count_genes += 1
    tokens = line.strip().split("\t")
    tmp_symbol = tokens[0]
    tmp_ncbi_id = tokens[1]
    tmp_xb_id = tokens[2]
    tmp_name = tokens[3]

    if tmp_ncbi_id == 'NA':
        count_ncbi_NA += 1

    elif tmp_ncbi_id not in ncbi_genes:
        ncbi_genes[tmp_ncbi_id] = {'xb': tmp_xb_id, 'symbol': tmp_symbol, 
                                   'name': tmp_name, 'lines': [] }
        ncbi_genes[tmp_ncbi_id]['lines'].append(line.strip())
    else:
        ncbi_genes[tmp_ncbi_id]['lines'].append(line.strip())

    if tmp_xb_id == 'NA':
        count_xb_NA += 1
    elif tmp_xb_id not in xb_genes:
        xb_genes[tmp_xb_id] = {'ncbi': tmp_ncbi_id, 'symbol': tmp_symbol,
                               'name': tmp_name, 'lines': []}
        xb_genes[tmp_xb_id]['lines'].append(line.strip())
    else:
        xb_genes[tmp_xb_id]['lines'].append(line.strip())
    
    if tmp_symbol == 'NA':
        count_symbol_NA += 1
        sys.stderr.write("No symbol: %s\n" % line.strip())
    elif tmp_symbol not in gene_symbols:
        gene_symbols[tmp_symbol] = {'ncbi': tmp_ncbi_id, 'xb': tmp_xb_id, 
                                    'name': tmp_name, 'lines': []}
        gene_symbols[tmp_symbol]['lines'].append(line.strip())
    else:
        gene_symbols[tmp_symbol]['lines'].append(line.strip())
f_gene.close()

sys.stderr.write("\nTotal gene counts (gene_info): %d\n" % count_genes)
sys.stderr.write("Genes with NA in NCBI: %d\n" % count_ncbi_NA)
sys.stderr.write("Genes with NA in XB: %d\n\n" % count_xb_NA)

for tmp_ncbi_id, tmp in ncbi_genes.items():
    if len(tmp['lines']) > 1:
        sys.stderr.write("MultiNCBIGene: %s\n" % tmp_ncbi_id)
        sys.stderr.write("%s\n\n" % ("\n".join(tmp['lines'])))

for tmp_xb_id, tmp in xb_genes.items():
    if len(tmp['lines']) > 1:
        sys.stderr.write("MultiXBGene: %s\n" % tmp_xb_id)
        sys.stderr.write("%s\n\n" % ("\n".join(tmp['lines'])))

for tmp_symbol, tmp in gene_symbols.items():
    if len(tmp['lines']) > 1:
        sys.stderr.write("MultiSymbol: %s\n" % tmp_symbol)
        sys.stderr.write("%s\n\n" % ("\n".join(tmp['lines'])))

