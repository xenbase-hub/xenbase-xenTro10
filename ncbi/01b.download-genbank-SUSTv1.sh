#!/bin/bash

curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_013368275.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_013368275.1.zip" -H "Accept: application/zip"

curl -output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/368/275/GCA_013368275.1_ASM1336827v1/GCA_013368275.1_ASM1336827v1_assembly_report.txt
curl -output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/013/368/275/GCA_013368275.1_ASM1336827v1/GCA_013368275.1_ASM1336827v1_genomic.fna.gz
