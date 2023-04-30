#!/bin/bash
DATE_VER="2023_04"

## NCBI orthology

OUT_NAME="./raw/gene_orthologs.ncbi."$DATE_VER".gz"
curl -o $OUT_NAME https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_orthologs.gz

## HGNC complete set
HGNC_VER=${DATE_VER/_/-}"-01"
OUT_NAME="./raw/hgnc_complete_set."$DATE_VER".txt"

curl -o $OUT_NAME https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/tsv/hgnc_complete_set_2023-04-01.txt
gzip $OUT_NAME
