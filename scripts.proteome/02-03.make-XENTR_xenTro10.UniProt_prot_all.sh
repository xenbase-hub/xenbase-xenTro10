#!/bin/bash
DIR_RAW="UP.2023_02"

REL_VER=$(head -n 1 $DIR_RAW/relnotes.txt | awk '{print $3}')
OUT_FILE="XENTR_xenTro10.UniProt_"$REL_VER".prot_all.fa"

./02a.uniprot-cleanup-proteome.py $DIR_RAW/UP000008143_8364.fasta.gz > $OUT_FILE
./02a.uniprot-cleanup-proteome.py $DIR_RAW/UP000008143_8364_additional.fasta.gz >> $OUT_FILE
./03.make-non_redundant_fasta.py $OUT_FILE