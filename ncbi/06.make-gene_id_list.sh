#!/bin/bash

FILE_HEADER="XENTR_xenTro10.refseq104.prot_all.headers"
OUT_FILE=${FILE_HEADER/.prot_all.headers/}".gene_id_list.csv"
echo "Make $OUT_FILE"

grep '>' $FILE_HEADER | awk -F"|" '{print $4}' | awk '{print $1","$2}' | sed 's/xb_gene_id=//' | sort -u > $OUT_FILE
