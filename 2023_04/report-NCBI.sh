#!/bin/bash

FILENAME_CSV="XENTR_xenTro10.gene_symbols.XB2023_04.csv"
OUT_SYMBOL="ToNCBI-ChangeSymbol-"$FILENAME_CSV

#remark,rep_symbol,gene_id,tx_id,prot_id,uniprot_id,ncbi_symbol,uniprot_symbol,xb_symbol,xb_id,diopt_hs1_name, diopt_hs1_id, diopt_hs1_score,diopt_hs2_name, diopt_hs2_id, diopt_hs2_score
#PERFECT,runx1t1,GeneID:100491944,XM_004915148.3,XP_004915205.1,A0A5S6MBM4,runx1t1,runx1t1,runx1t1,XB-GENE-481238,RUNX1T1,862,4,NA,NA,-1

cat $FILENAME_CSV | awk -F"," '{ if ($2 != $7) print $3","$2","$7","$5}' > $OUT_SYMBOL
