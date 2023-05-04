#!/bin/bash
OUT_FILE="XENTR_xenTro10.UniProt_2023_01.prot_all.fa"
./02a.uniprot-cleanup-proteome.py raw/UP000008143_8364.fasta.gz > $OUT_FILE
./02a.uniprot-cleanup-proteome.py raw/UP000008143_8364_additional.fasta.gz >> $OUT_FILE
./03.make-non_redundant_fasta.py $OUT_FILE
