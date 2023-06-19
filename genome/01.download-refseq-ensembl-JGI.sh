#!/bin/bash

## EnsEMBL
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/release-109/gff3/xenopus_tropicalis/Xenopus_tropicalis.UCB_Xtro_10.0.109.gff3.gz

## RefSeq
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_assembly_report.txt

## JGI
curl --output-dir ./raw -O https://download.xenbase.org/xenbase/Genomics/JGI/Xentr10.0/Berkeley/XENTR_10.0_UCB_gene.gff3.gz

## Xenbase
curl --output-dir ./raw -O https://download.xenbase.org/xenbase/Genomics/JGI/Xentr10.0/XENTR_10.0_Xenbase.gff3.gz
