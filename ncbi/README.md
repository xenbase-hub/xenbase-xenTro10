# NCBI resources for *Xenopus tropicalis*

## Procedures

* Download required files from NCBI
 ```
 $ ./01.download-refseq-stable.sh
 ```
  * [a script to download files](./01.download-refseq-stable.sh)
  * [List of files](./FILES.xenTro10_refseq104)

* Change the header format of protein sequences.
  ```
  ./02.reformat-ncbi_prot_fasta.py <faa file> <gff file> <output name> 
  ```

  Original header of protein FASTA file looks like:
  > >NP_001116955.1 DNA-binding protein RFX2 [Xenopus tropicalis]

  New header of protein FASTA file looks like (all other associated IDs are from GFF3):
  > :>rfx2|NP_001116955.1|NM_001123483.1|GeneID:100144734 xb_gene_id=XB-GENE-991774



## Resources

### X. tropicalis genomes (official RefSeq release)

Source: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/all_assembly_versions/

* [v10 genome (GCF_000004195.4)](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/all_assembly_versions/GCF_000004195.4_UCB_Xtro_10.0/)
* [v9 genome (GCF_000004195.3)](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/all_assembly_versions/GCF_000004195.3_Xenopus_tropicalis_v9.1/)
* [v7 genome (GCF_000004195.2)](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/all_assembly_versions/GCF_000004195.2_Xtropicalis_v7/)


### *X. tropicalis* genome (up-to-date)

Source: https://www.ncbi.nlm.nih.gov/datasets/taxonomy/8364/


### *X. tropicalis* genome (SUST version)

Source: https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_013368275.1/


