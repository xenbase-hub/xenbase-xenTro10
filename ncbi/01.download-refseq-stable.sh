#!/bin/bash

URL_NCBI_GENOME="https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/all_assembly_versions"
URL_NCBI_v10=$URL_NCBI_GENOME"/GCF_000004195.4_UCB_Xtro_10.0"
URL_NCBI_v9=$URL_NCBI_GENOME"/GCF_000004195.3_Xenopus_tropicalis_v9.1"
URL_NCBI_v7=$URL_NCBI_GENOME"/GCF_000004195.2_Xtropicalis_v7/"

for FILENAME in $(cat FILES.xenTro10_refseq104)
do
  FILENAME_OUT="./raw/"$FILENAME
  if [ -e $FILENAME_OUT ]; then
    echo "$FILENAME_OUT exists. Skip."
  else
    FILENAME_URL=$URL_NCBI_v10"/"$FILENAME
    echo "Download $FILENAME_URL"
    curl --output-dir ./raw -O $FILENAME_URL
  fi
done

for FILENAME in $(cat FILES.xenTro9_refseq103)
do
  FILENAME_OUT="./raw/"$FILENAME
  if [ -e $FILENAME_OUT ]; then
    echo "$FILENAME_OUT exists. Skip."
  else
    FILENAME_URL=$URL_NCBI_v9"/"$FILENAME
    echo "Download $FILENAME_URL"
    curl --output-dir ./raw -O $FILENAME_URL
  fi
done

for FILENAME in $(cat FILES.xenTro7_refseq)
do
  FILENAME_OUT="./raw/"$FILENAME
  if [ -e $FILENAME_OUT ]; then
    echo "$FILENAME_OUT exists. Skip."
  else
    FILENAME_URL=$URL_NCBI_v7"/"$FILENAME
    echo "Download $FILENAME_URL"
    curl --output-dir ./raw -O $FILENAME_URL
  fi
done
