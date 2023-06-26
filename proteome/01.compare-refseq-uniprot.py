#!/usr/bin/env python3
import sys
import gzip

filename_1 = '../ncbi/XENTR_xenTro10.refseq104.prot_all_NR.fa.gz'
filename_2 = '../uniprot/XENTR_uniprot2023_02.prot_all_NR.fa.gz'

dataname_1 = "refseq104"
dataname_2 = "up2023_02"
filename_base = "XENTR_xenTro10_refseq104-up202302"


def read_fasta(tmp_filename):
    rv = dict()
    f = open(tmp_filename, 'r')
    if tmp_filename.endswith('.gz'):
        f = gzip.open(tmp_filename, 'rt')
    for line in f:
        if line.startswith('>'):
            tmp_h = line.strip().lstrip('>')
            rv[tmp_h] = []
        else:
            rv[tmp_h].append(line.strip())
    f.close()
    return rv


def seq2h(tmp_list):
    rv = dict()
    for tmp_h, tmp_seq_list in tmp_list.items():
        tmp_seq = ''.join(tmp_seq_list)
        if tmp_seq in rv:
            sys.stderr.write("Duplicate: %s, %s\n" %
                             (tmp_h, ','.join(rv[tmp_seq])))
            rv[tmp_seq].append(tmp_h)
        else:
            rv[tmp_seq] = [tmp_h]
    return rv


seq_1 = read_fasta(filename_1)
seq_2 = read_fasta(filename_2)

seq2h_1 = seq2h(seq_1)
seq2h_2 = seq2h(seq_2)

sys.stderr.write('Seqs in %s: %d\n' % (dataname_1, len(seq2h_1)))
sys.stderr.write('Seqs in %s: %d\n' % (dataname_2, len(seq2h_2)))

f_out = open('%s.raw.prot_combined.fa' % filename_base, 'w')

f_log = open('%s.raw.prot_combined.log' % filename_base, 'w')
f_1 = open('%s.raw.prot_%s_only.fa' % (filename_base, dataname_1), 'w')
f_2 = open('%s.raw.prot_%s_only.fa' % (filename_base, dataname_2), 'w')

good_seq_list = []

count_1_only = 0
count_2_only = 0

for tmp_seq in seq2h_1.keys():
    tmp_name_1 = seq2h_1[tmp_seq][0].split('|')[0]
    if len(seq2h_1[tmp_seq]) > 1:
        sys.sterr.write("MulitHeader.%s: %s\n" %
                        (dataname_1, 
                         ";;".join(seq2h_1[tmp_seq])))

    tmp_1_h = seq2h_1[tmp_seq][0]
    if tmp_seq in seq2h_2:
        tmp_2_h = seq2h_2[tmp_seq][0]
        good_seq_list.append(tmp_seq)
        tmp_name_2 = seq2h_2[tmp_seq][0].split('|')[0]

        if tmp_name_1 != tmp_name_2:
            f_log.write('DiffName\t%s\t%s\n' %
                        (seq2h_1[tmp_seq][0], seq2h_2[tmp_seq][0]))
            # f_diff_name.write('>%s uniprot=%s\n%s\n' %
            #                   (seq2h_2[tmp_seq][0],
            #                    seq2h_1[tmp_seq][0], tmp_seq))
        # else:
        f_out.write('>%s %s=%s\n%s\n' %
                    (seq2h_1[tmp_seq][0], dataname_2, seq2h_2[tmp_seq][0],
                     "\n".join(seq_2[tmp_2_h])))
    else:
        f_log.write('%s_only\t%s\n' % (dataname_1, tmp_1_h))
        f_1.write('>%s\n%s\n' % (tmp_1_h, "\n".join(seq_1[tmp_1_h])))
        count_1_only += 1

for tmp_seq in seq2h_2.keys():
    if len(seq2h_2[tmp_seq]) > 1:
        sys.sterr.write("MulitHeader.%s: %s\n" %
                        (dataname_2,
                        ";;".join(seq2h_2[tmp_seq])))
    if tmp_seq not in seq2h_1:
        tmp_2_h = seq2h_2[tmp_seq][0]
        f_log.write('%s_only\t%s\n' % (dataname_2, tmp_2_h))
        f_2.write('>%s\n%s\n' %
                     (tmp_2_h, "\n".join(seq_2[tmp_2_h])))
        count_2_only += 1

sys.stderr.write('Matched seq: %d\n' % len(good_seq_list))
sys.stderr.write('%s_only: %d\n' % (dataname_1, count_1_only))
sys.stderr.write('%s_only: %d\n' % (dataname_2, count_2_only))

f_log.close()
f_out.close()
f_1.close()
f_2.close()
