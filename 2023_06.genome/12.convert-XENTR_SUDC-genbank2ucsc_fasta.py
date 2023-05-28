#!/usr/bin/env python3
import sys
import os

filename_alias = 'raw/GCA_013368275.1_ASM1336827v1_assembly_report.txt'
filename_fa_in = 'raw/GCA_013368275.1_ASM1336827v1_genomic.fna.gz'

dirname_base = os.path.dirname(os.path.realpath(__file__))

chr_alias = dict()
f_alias = open(os.path.join(dirname_base, filename_alias), 'r')

for line in f_alias:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    gb_id = tokens[4]
    chr_id = tokens[0].replace('Chr0', 'chr')
    chr_alias[gb_id] = chr_id
f_alias.close()

f_fa_in = open(filename_fa_in, 'r')
if filename_fa_in.endswith('.gz'):
    import gzip
    f_fa_in = gzip.open(filename_fa_in, 'rt')

f_fa_out = open('%s.ucsc_style' % filename_fa_in, 'w')
for line in f_fa_in:
    if line.startswith('>'):
        tmp_id = line.strip().lstrip('>').split()[0]
        if tmp_id.startswith('CM'):
            new_id = chr_alias[tmp_id]
            sys.stderr.write('%s -> %s\n' % (line.strip(), new_id))
            f_fa_out.write('>%s|SUDC %s\n' % (new_id, tmp_id))
        else:
            new_id = 'chrUn_%s' % tmp_id.replace('.', 'v')
            sys.stderr.write('%s -> %s\n' % (line.strip(), new_id))
            f_fa_out.write('>%s|SUDC %s\n' % (new_id, tmp_id))
    else:
        f_fa_out.write('%s\n' % line.strip())
f_fa_in.close()
