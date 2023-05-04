#!/bin/bash

## UniProt
UNIPROT_URL="https://ftp.uniprot.org/pub/databases/uniprot/current_release/"

curl --output-dir ./raw -O "$UNIPROT_URL/relnotes.txt"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364.fasta.gz"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364_additional.fasta.gz"

## RefSeq

curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_protein.faa.gz
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_rna.fna.gz
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/README_Xenopus_tropicalis_annotation_release_104
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/README.txt
curl --output-dir ./raw -O https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/representative/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_assembly_report.txt
