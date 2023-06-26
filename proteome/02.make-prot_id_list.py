#!/usr/bin/env python3
import sys

filename_fa = sys.argv[1]

print("# UNIPROT_ACC,REFSEQ_PROT_ID,REFSEQ_RNA_ID,REFSEQ_GENE_ID,XB_GENE_ID")
f_fa = open(filename_fa, 'r')
for line in f_fa:
    if line.startswith('>'):
        tokens = line.strip().split()
        ncbi_tokens = tokens[0].split("|")
        xb_id = tokens[1].split('=')[1]

        uniprot_acc = 'NA'
        if len(tokens) >= 3:
            uniprot_acc = tokens[2].split('|')[-1]

        print("%s,%s,%s,%s,%s" % (uniprot_acc, ncbi_tokens[1],
                                  ncbi_tokens[2], ncbi_tokens[3], xb_id))
f_fa.close()
