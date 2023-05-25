#!/bin/bash

for FA in $(ls *NCBI*.prot_all.fa)
do
  DATA_NAME=${FA/.prot_all.fa/}
  OUT_FILE=$DATA_NAME".gene_id_list.csv"
  echo "Make $OUT_FILE"
  grep '>' $FA | awk -F"|" '{print $4}' | awk '{print $1","$2}' | sed 's/xb_gene_id=//' | sort -u > $OUT_FILE
done
