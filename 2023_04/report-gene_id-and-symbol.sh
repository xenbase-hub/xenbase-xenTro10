#!/bin/bash

FILE_CSV="XENTR_xenTro10.gene_symbols.XB2023_04.csv"
COUNT_ALL=$(awk -F"," '{print $3}' $FILE_CSV | grep -v gene_id | wc -l)
COUNT_ID=$(awk -F"," '{print $3}' $FILE_CSV | grep -v gene_id | sort -u | wc -l)
COUNT_SYMBOL=$(awk -F"," '{print $2}' $FILE_CSV | grep -v rep_symbol | sort -u | wc -l)

echo "FILE: "$FILE_CSV
echo "Number of records: " $COUNT_ALL
echo "Number of gene ID: " $COUNT_ID
echo "Number of gene symbols: " $COUNT_SYMBOL

