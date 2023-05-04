#!/usr/bin/env python3

filename_out = 'XENTR_xenTro10.prot_uniprot_ncbi.raw.2023_04.csv'
#GeneID:100491944,XM_004915148.3,XP_004915205.1,runx1t1,A0A5S6MBM4,runx1t1
#GeneID:100487513,XM_002937850.5,XP_002937896.1,ano10,A0A6I8Q0X6,ano10

filename_fa = 'XENTR_xenTro10.XB2023_04.raw.prot_combined.fa'
# >knstrn|XP_017952403.1|XM_018096914.2|GeneID:100380161 xb_gene_id=XB-GENE-974812 uniprot=knstrn|A0A6I8PPC7
# >shc2|XP_002939812.3|XM_002939766.5|GeneID:100487416 xb_gene_id=XB-GENE-6073771 uniprot=shc2|A0A6I8PXN2

f_fa = open(filename_fa, 'r')
f_out = open(filename_out, 'w')
for line in f_fa:
    if line.startswith('>'):
        tokens = line.strip().lstrip('>').split()
        ncbi_tokens = tokens[0].split('|')
        ncbi_symbol = ncbi_tokens[0]
        ncbi_prot_id = ncbi_tokens[1]
        ncbi_tx_id = ncbi_tokens[2]
        ncbi_gene_id = ncbi_tokens[3]
        uniprot_tokens = tokens[2].replace('uniprot=', '').split('|')
        uniprot_symbol = uniprot_tokens[0]
        uniprot_acc = uniprot_tokens[1]
        f_out.write('%s,%s,%s,%s,%s,%s\n' %
                    (ncbi_gene_id, ncbi_tx_id, ncbi_prot_id, ncbi_symbol,
                     uniprot_acc, uniprot_symbol))
f_fa.close()
f_out.close()
