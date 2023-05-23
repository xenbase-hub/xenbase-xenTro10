#!/bin/bash

FILE_TSV="Xenbase_GPI.2023-05-16.raw.tsv"
NCBI_TAXON="NCBITaxon:8364"

DATE=$(echo $FILE_TSV | awk -F"." '{print $2}')
OUT_TSV="Xenbase_XENTR_gene_name."$DATE".tsv"

echo "Make $OUT_TSV ... done"
#grep ^"!" $FILE_TSV | awk -F"\t" '{if ($2 == "NCBITaxon:8364") print $2"\t"$1"\t"$3}'
grep -a -v ^"!" $FILE_TSV | awk -v TAX_ID="$NCBI_TAXON" -F"\t" '{if ($6 == TAX_ID) print $2"\t"$1"\t"$3}' > $OUT_TSV
