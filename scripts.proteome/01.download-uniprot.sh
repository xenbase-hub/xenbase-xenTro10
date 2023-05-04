#!/bin/bash

## UniProt
UNIPROT_URL="https://ftp.uniprot.org/pub/databases/uniprot/current_release/"

curl --output-dir ./raw -O "$UNIPROT_URL/relnotes.txt"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364.fasta.gz"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364_additional.fasta.gz"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364.idmapping.gz"
curl --output-dir ./raw -O "$UNIPROT_URL/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364.gene2acc.gz"
