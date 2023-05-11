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
    refseq_id = tokens[6]
    chr_id = tokens[9]
    chr_alias[refseq_id] = chr_id
f_alias.close()


# ==> XENTR.ncbi104.gene.gff3 <==
# NC_030677.2	Gnomon	gene	43856	87766	.	+	.	ID=gene-LOC101732307;Dbxref=GeneID:101732307;Name=LOC101732307;gbkey=Gene;gene=LOC101732307;gene_biotype=protein_coding

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
