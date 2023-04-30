#!/usr/bin/env python3
import gzip
import sys

filename_prot = 'DIOPT2023_04.XENTR-HUMAN.FastOrtho_prot_summary.tsv'
filename_gene = 'DIOPT2023_04.XENTR-HUMAN.FastOrtho_gene_summary.tsv'

xt_prot2gene = dict()
f_xt_genes = gzip.open('DIOPT2023_04.TropEntrez.txt.gz', 'rt')
f_xt_genes.readline()
for line in f_xt_genes:
    tokens = line.strip().split()
    xt_prot2gene[tokens[0]] = tokens[1]
f_xt_genes.close()

# Some proteins missed the gene IDs; added them from ncbi-uniprot mapping.
# No XT gene: XP_012821376.2
# No XT gene: NP_989218.1
# No XT gene: NP_001116949.1
# No XT gene: NP_001123816.1
f_genes = open('../XENTR_xenTro10.prot_uniprot_ncbi.raw.2023_04.csv', 'r')
for line in f_genes:
    tokens = line.strip().split(",")
    xt_prot2gene[tokens[2].split('.')[0]] = tokens[0].replace('GeneID:', '')
f_genes.close()

hs_prot2gene = dict()
f_hs_genes = gzip.open('DIOPT2023_04.HumanEntrez.txt.gz', 'rt')
f_hs_genes.readline()
for line in f_hs_genes:
    tokens = line.strip().split()
    hs_prot2gene[tokens[0]] = tokens[1]
f_hs_genes.close()

gene_summary = dict()

f_prot = open(filename_prot, 'w')
f_prot.write("#XT_prot\tXT_gene\tHS_prot\tHS_gene\tOrthoID\n")
f_list = gzip.open('DIOPT2023_04.FastOrtho_Hsap_Xtrop_RAW.tsv.gz', 'rt')
for line in f_list:
    tokens = line.strip().split("\t")
    ortho_id = tokens[0].split()[0]
    hs_id_list = []
    xt_id_list = []
    for tmp in tokens[1].split():
        if tmp.endswith('(XtropV10_Proteome)'):
            xt_id_list.append(tmp.replace('(XtropV10_Proteome)', ''))
        elif tmp.endswith('(H_sapiens_proteome_UP000005640_9606)'):
            hs_id_list.append(tmp.split('_')[2])

    for tmp_xt in xt_id_list:
        tmp_xt_q = tmp_xt.split('.')[0]

        tmp_xt_gene = 'NA'
        if tmp_xt_q in xt_prot2gene:
            tmp_xt_gene = xt_prot2gene[tmp_xt_q]
            if tmp_xt_gene not in gene_summary:
                gene_summary[tmp_xt_gene] = dict()
        else:
            sys.stderr.write("No XT gene: %s\n" % tmp_xt)

        if len(hs_id_list) > 0:
            for tmp_hs in hs_id_list:
                tmp_hs_gene = 'NA'
                if tmp_hs in hs_prot2gene:
                    tmp_hs_gene = hs_prot2gene[tmp_hs]

                if tmp_hs_gene not in gene_summary[tmp_xt_gene]:
                    gene_summary[tmp_xt_gene][tmp_hs_gene] = ortho_id
                elif gene_summary[tmp_xt_gene][tmp_hs_gene] != ortho_id:
                    sys.stderr.write('Different: %s - %s\n' %
                                     (tmp_xt_gene, tmp_hs_gene))

                f_prot.write('%s\t%s\t%s\t%s\t%s\n' %
                             (tmp_xt, tmp_xt_gene,
                              tmp_hs, tmp_hs_gene, ortho_id))
        else:
            f_prot.write('%s\t%s\tNA\tNA\t%s\n' %
                         (tmp_xt, tmp_xt_gene, ortho_id))

f_list.close()
f_prot.close()

f_gene = open(filename_gene, 'w')
f_gene.write("#XT_gene\tHS_gene\tOrthoID\n")
for tmp_xt_gene in sorted(gene_summary.keys()):
    for tmp_hs_gene in sorted(gene_summary[tmp_xt_gene].keys()):
        f_gene.write("%s\t%s\t%s\n" %
                     (tmp_xt_gene, tmp_hs_gene,
                      gene_summary[tmp_xt_gene][tmp_hs_gene]))
f_gene.close()
