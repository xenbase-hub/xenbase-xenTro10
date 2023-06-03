#!/usr/bin/env python3
import sys

filename_1 = sys.argv[1]
filename_2 = sys.argv[2]

dataname_1 = filename_1.split('.')[0].replace('XENTR_', '')
dataname_2 = filename_2.split('.')[0].replace('XENTR_', '')

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

seq_1 = read_fasta(filename_1)
seq_2 = read_fasta(filename_2)

seq2h_1 = dict()
seq2h_2 = dict()

count_same = 0
h_list_same = []
for tmp_h1, tmp_list1 in seq_1.items():
    tmp_seq_1 = ''.join(tmp_list1)
    if tmp_h1 in seq_2:
        tmp_seq_2 = ''.join(seq_2[tmp_h1])
        if tmp_seq_1 == tmp_seq_2:
            h_list_same.append(tmp_h1)
            count_same += 1
        else:
            ## critical error. same header with different sequences.
            sys.stderr.write("SameID;DiffSeq\t%s" % tmp_h1)
            sys.exit(1)
    else:
        seq2h_1[tmp_seq_1] = tmp_h1

count_new_seq1 = 0
count_new_seq2 = 0

count_diff_symbol = 0
count_diff_type = 0

f_out = open('%s-%s.compare.txt' % (dataname_1, dataname_2), 'w')
for tmp_h2, tmp_list2 in seq_2.items():
    if tmp_h2 in h_list_same:
        continue

    tmp_seq_2 = ''.join(seq_2[tmp_h2])
    seq2h_2[tmp_seq_2] = tmp_h2
    if tmp_seq_2 not in seq2h_1:
        count_new_seq2 += 1
    else:
        tmp_h1 = seq2h_1[tmp_seq_2]
        tmp_acc_1 = tmp_h1.split()[0].split('|')[1]
        tmp_acc_2 = tmp_h2.split()[0].split('|')[1]
        if tmp_acc_1 != tmp_acc_2:
            sys.stderr.write("SameSeq;DiffAcc\t%s\t%s\n" % (tmp_h1, tmp_h2))
            f_out.write("SameSeq;DiffAcc\t%s\t%s\n" % (tmp_h1, tmp_h2))

        tmp_symbol_1 = tmp_h1.split()[0].split('|')[0]
        tmp_symbol_2 = tmp_h2.split()[0].split('|')[0]
        #sys.stderr.write("DiffHeader\t%s\t%s\n" % (tmp_h2, seq2h_1[tmp_seq_2]))
        tmp_type_1 = tmp_h1.split()[1]
        tmp_type_2 = tmp_h2.split()[1]
        if tmp_symbol_1 != tmp_symbol_2:
            count_diff_symbol += 1
            if tmp_type_1 != tmp_type_2:
                f_out.write("DiffSymbol;DdiffType\t%s\t%s\n" % (tmp_h1, tmp_h2))
            else:
                f_out.write("DiffSymbol\t%s\t%s\n" % (tmp_h1, tmp_h2))
        elif tmp_type_1 != tmp_type_2:
            count_diff_type += 1
            f_out.write("DiffType\t%s\t%s\n" % (tmp_h1, tmp_h2))

for tmp_seq_1, tmp_h1 in seq2h_1.items():
    if tmp_seq_1 not in seq2h_2:
        count_new_seq1 += 1

f_out.close()

sys.stderr.write("%s sequences: %d\n" % (dataname_1, len(seq_1)))
sys.stderr.write("%s sequences: %d\n" % (dataname_2, len(seq_2)))
sys.stderr.write("\n")
sys.stderr.write("Identical seqs: %d\n" % (count_same))
sys.stderr.write("  Diff seqs in %s: %d\n" % (dataname_1, len(seq2h_1)))
sys.stderr.write("  Diff seqs in %s: %d\n" % (dataname_2, len(seq2h_2)))
sys.stderr.write("\n")
sys.stderr.write("Change symbols: %d\n" % count_diff_symbol)
sys.stderr.write("Change types (sp/tr, main/additional): %d\n" % count_diff_type)

