#!/usr/bin/env python3
import sys

filename_ncbi = './XENTR_xenTro10.NCBI_104.prot_all_NR.fa'
filename_up = './XENTR_xenTro10.UniProt_2023_01.prot_all_NR.fa'

filename_base = 'XENTR_xenTro10.XB2023_04'


def read_fasta(tmp_filename):
    rv = dict()
    f = open(tmp_filename, 'r')
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


seq_up = read_fasta(filename_up)
seq_ncbi = read_fasta(filename_ncbi)

seq2h_up = seq2h(seq_up)
seq2h_ncbi = seq2h(seq_ncbi)

sys.stderr.write('Seqs in UniProt: %d\n' % len(seq2h_up))
sys.stderr.write('Seqs in NCBI: %d\n' % len(seq2h_ncbi))

f_out = open('%s.raw.prot_combined.fa' % filename_base, 'w')
# f_diff_name = open('%s.raw.prot_diff_name.fa' % filename_base, 'w')
f_log = open('%s.raw.prot_combined.log' % filename_base, 'w')
f_ncbi = open('%s.raw.prot_NCBI_only.fa' % filename_base, 'w')
f_up = open('%s.raw.prot_UniProt_only.fa' % filename_base, 'w')

good_seq_list = []

count_refseq_only = 0
count_uniprot_only = 0

for tmp_seq in seq2h_up.keys():
    tmp_name_up = seq2h_up[tmp_seq][0].split('|')[0]
    if len(seq2h_up[tmp_seq]) > 1:
        sys.sterr.write("MulitHeadder.NCBI: %s\n" %
                        ";;".join(seq2h_up[tmp_seq]))

    tmp_up_h = seq2h_up[tmp_seq][0]
    if tmp_seq in seq2h_ncbi:
        tmp_ncbi_h = seq2h_ncbi[tmp_seq][0]
        good_seq_list.append(tmp_seq)
        tmp_name_ncbi = seq2h_ncbi[tmp_seq][0].split('|')[0]

        if tmp_name_up != tmp_name_ncbi:
            f_log.write('DiffName\t%s\t%s\n' %
                        (seq2h_up[tmp_seq][0], seq2h_ncbi[tmp_seq][0]))
            # f_diff_name.write('>%s uniprot=%s\n%s\n' %
            #                   (seq2h_ncbi[tmp_seq][0],
            #                    seq2h_up[tmp_seq][0], tmp_seq))
        # else:
        f_out.write('>%s uniprot=%s\n%s\n' %
                    (seq2h_ncbi[tmp_seq][0], seq2h_up[tmp_seq][0],
                     "\n".join(seq_ncbi[tmp_ncbi_h])))
    else:
        f_log.write('UniProtOnly\t%s\n' % tmp_up_h)
        f_up.write('>%s\n%s\n' % (tmp_up_h, "\n".join(seq_up[tmp_up_h])))
        count_uniprot_only += 1

for tmp_seq in seq2h_ncbi.keys():
    if len(seq2h_ncbi[tmp_seq]) > 1:
        sys.sterr.write("MulitHeadder.NCBI: %s\n" %
                        ";;".join(seq2h_ncbi[tmp_seq]))
    if tmp_seq not in seq2h_up:
        tmp_ncbi_h = seq2h_ncbi[tmp_seq][0]
        f_log.write('RefSeqOnly\t%s\n' % tmp_ncbi_h)
        f_ncbi.write('>%s\n%s\n' %
                     (tmp_ncbi_h, "\n".join(seq_ncbi[tmp_ncbi_h])))
        count_refseq_only += 1

sys.stderr.write('Matched seq: %d\n' % len(good_seq_list))
sys.stderr.write('RefSeq only: %d\n' % count_refseq_only)
sys.stderr.write('UniProt only: %d\n' % count_uniprot_only)

f_log.close()
f_out.close()
f_up.close()
f_ncbi.close()
