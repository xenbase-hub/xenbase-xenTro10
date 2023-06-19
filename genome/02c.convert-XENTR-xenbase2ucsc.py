#!/usr/bin/env python3
import sys
import os

filename_in = sys.argv[1]

filename_alias = 'raw/GCF_000004195.4_UCB_Xtro_10.0_assembly_report.txt'
dirname_base = os.path.dirname(os.path.realpath(__file__))

chr_alias = dict()
f_alias = open(os.path.join(dirname_base, filename_alias), 'r')
# Sequence-Name Sequence-Role   Assigned-Molecule       Assigned-Molecule-Location/Type GenBank-Accn    Relationship   RefSeq-Accn      Assembly-Unit   Sequence-Length UCSC-style-name
# Chr1    assembled-molecule      1       Chromosome      CM004443.2      =       NC_030677.2     Primary Assembly       217471166        chr1

for line in f_alias:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    xb_id = tokens[0]
    chr_id = tokens[9]
    chr_alias[xb_id] = chr_id
f_alias.close()

# 1       ensembl gene    26787   30692   .       +       .       ID=gene:ENSXETG00000046667;biotype=protein_coding;gene_id=ENSXETG00000046667;logic_name=ensembl;version=1
# AAMC04000166.1  ensembl gene    1       512     .       -       .       ID=gene:ENSXETG00000043539;Name=efna3;biotype=protein_coding;description=ephrin A3 [Source:Xenbase%3BAcc:XB-GENE-5720826];gene_id=ENSXETG00000043539;logic_name=ensembl;version=1


f_in = open(filename_in, 'r')
if filename_in.endswith('.gz'):
    import gzip
    f_in = gzip.open(filename_in, 'rt')

f_out = open('%s.ucsc_style' % filename_in, 'w')
for line in f_in:
    if line.startswith('#'):
        f_out.write("%s\n" % line.strip())
    else:
        tokens = line.strip().split("\t")
        tokens[0] = chr_alias[tokens[0]]
        f_out.write("%s\n" % "\t".join(tokens))
f_in.close()
