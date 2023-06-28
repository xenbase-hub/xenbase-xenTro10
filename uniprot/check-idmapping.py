#!/usr/bin/env python3

import sys
import gzip

filename_map = 'raw/2023_02.UP000008143_8364.idmapping.gz'
filename_prot = '../XENTR_prot_id_list.active.csv'

id2map = dict()
f_map = gzip.open(filename_map, 'rt')
for line in f_map:
    tokens = line.strip().split("\t")
    q_id = tokens[0]
    source_type = tokens[1]
    source_id = tokens[2]

    if q_id not in id2map:
        id2map[q_id] = {'GeneID': 'NA', 'RefSeq': 'NA', 'Xenbase': 'NA', 'RefSeq_NT': 'NA'}

    if source_type == 'GeneID':
        id2map[q_id]['GeneID'] = 'GeneID:%s' % source_id
    if source_type == 'RefSeq':
        id2map[q_id]['RefSeq'] = source_id
    if source_type == 'RefSeq_NT':
        id2map[q_id]['RefSeq_NT'] = source_id
    if source_type == 'Xenbase':
        id2map[q_id]['Xenbase'] = source_id
f_map.close()

change_refseq = 0
change_refseq_nt = 0
change_ncbi_gene = 0
change_xb_gene = 0

f_list = open('../XENTR_prot_id_list.active.csv', 'r')
for line in f_list:
    if line.startswith('#'):
        continue
    tokens = line.strip().split(",")
    up_acc = tokens[0]
    refseq_prot = tokens[1]
    refseq_tx = tokens[2]
    ncbi_gene = tokens[3]
    xb_gene = tokens[4]

    if up_acc not in id2map:
        print("NEW\t%s" % line.strip())
    else:
        up_refseq = id2map[up_acc]['RefSeq']
        up_refseq_nt = id2map[up_acc]['RefSeq_NT']
        up_gene = id2map[up_acc]['GeneID']
        up_xb = id2map[up_acc]['Xenbase']

        old_line = "%s,%s,%s,%s,%s" % (up_acc,up_refseq,up_refseq_nt, up_gene, up_xb)

        tag_list = []
        if up_refseq != refseq_prot:
            tag_list.append('RefSeq')
            change_refseq += 1

        if up_refseq_nt != refseq_tx:
            tag_list.append('RefSeq_NT')
            change_refseq_nt += 1

        if up_gene != ncbi_gene:
            tag_list.append('GeneID')
            change_ncbi_gene += 1

        if up_xb != xb_gene:
            tag_list.append('Xenbase')
            change_xb_gene += 1

        if len(tag_list) > 0:
            print("OldLine\t%s\t%s" % (old_line, ",".join(tag_list)) )
            print("NewLine\t%s" % line.strip())
f_list.close()

sys.stderr.write('RefSeq change: %d\n' % change_refseq)
sys.stderr.write('Refseq_NT change: %dd\n' % change_refseq_nt)
sys.stderr.write('GeneID change: %d\n' % change_ncbi_gene)
sys.stderr.write('Xenbase Gene ID change: %d\n' % change_xb_gene)
