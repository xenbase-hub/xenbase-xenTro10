#!/bin/bash
curl --output-dir ./raw -o "ensembl.current_README" https://ftp.ensembl.org/pub/current_README
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_fasta/xenopus_tropicalis/cds/Xenopus_tropicalis.UCB_Xtro_10.0.cds.all.fa.gz
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_fasta/xenopus_tropicalis/cdna/Xenopus_tropicalis.UCB_Xtro_10.0.cdna.all.fa.gz
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_fasta/xenopus_tropicalis/ncrna/Xenopus_tropicalis.UCB_Xtro_10.0.ncrna.fa.gz
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_fasta/xenopus_tropicalis/pep/Xenopus_tropicalis.UCB_Xtro_10.0.pep.all.fa.gz
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_gff3/xenopus_tropicalis/Xenopus_tropicalis.UCB_Xtro_10.0.109.gff3.gz
curl --output-dir ./raw -O https://ftp.ensembl.org/pub/current_gtf/xenopus_tropicalis/Xenopus_tropicalis.UCB_Xtro_10.0.109.gtf.gz
