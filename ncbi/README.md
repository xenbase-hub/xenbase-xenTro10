# NCBI resources for *Xenopus tropicalis*

## Processed files
* https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/ (ID: amphibase  PW: ribbit)
  * [XENTR_xenTro10.refseq104.prot_all.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.refseq104.prot_all.fa.gz): All proteins
    * 45,093 sequences [XENTR_xenTro10.refseq104.prot_all.headers](./XENTR_xenTro10.refseq104.prot_all.headers)
  * [XENTR_xenTro10.refseq104.prot_all.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.refseq104.prot_all.fa_NR.gz): Non redundant proteins
    * 37,591 sequences [XENTR_xenTro10.refseq104.prot_all_NR.headers](./XENTR_xenTro10.refseq104.prot_all.headers)
  * [XENTR_xenTro10.refseq104.tx_all.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.refseq104.tx_all.fa.gz): All transcripts
    * 50,533 sequences [XENTR_xenTro10.refseq104.tx_all_NR.headers](./XENTR_xenTro10.refseq104.tx_all.headers)
  * [XENTR_xenTro10.refseq104.cds_all.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.refseq104.cds_all.fa.gz): All CDS sequences
    * 45,093 sequences [XENTR_xenTro10.refseq104.cds_all.headers](./XENTR_xenTro10.refseq104.cds_all.headers)

## Procedures

* Download required files from NCBI
  ```
  ./01.download-refseq-stable.sh
  ```
  * [List of files for downloading](./FILES.xenTro10_refseq104)

* Change the header format of protein sequences.
  ```
  ./02.reformat-ncbi_prot_fasta.py <faa file> <gff file> <output name> 
  ```

  Original header of protein FASTA file looks like:
  ```
  >NP_001116955.1 DNA-binding protein RFX2 [Xenopus tropicalis]
  ```

  New header of protein FASTA file looks like (all other associated IDs are from GFF3):
  ```
  >rfx2|NP_001116955.1|NM_001123483.1|GeneID:100144734 xb_gene_id=XB-GENE-991774
  ```

  * All mitochondrial proteins do not have proper rna IDs. See [the log file](./XENTR_xenTro10.refseq104.prot_all.log).

* Change the header format of rna sequences (similar to protein sequences).
  ```
  ./03.reformat-ncbi_rna_fasta.py <fna file> <gff file> <output name>
  ```
  
  Original header of protein FASTA file looks like:
  ```
  >NM_001123483.1 Xenopus tropicalis regulatory factor X2 (rfx2), mRNA
  ```

  New header of protein FASTA file looks like (all other associated IDs are from GFF3):
  ```
  >rfx2|NM_001123483.1|GeneID:100144734 xb_gene_id=XB-GENE-991774 type=mRNA
  ```

  * All sequences annotated as a 'guide_RNA' were discarded.

* Change the header format of CDS sequences. It reports the sequences matched to protein sequences.
  ```
  ./04.reformat-ncbi_cds_fasta.py <cds fna file> <protein faa file (processed .prot_all.fa)>
  ```
  
  * 72 genes (mostly related to immune system) do not have protein IDs. See [the log file](./XENTR_xenTro10.refseq104.cds_all.log)
  * The following 6 genes have split CDS sequences (need further investigations). 
    * LOC100216185|GeneID:100216185|NP_001135626.1 : NC_030685.2, NW_022279350.1
    * slc25a34|GeneID:100216146|NP_001135591.1 : NW_022279421.1, NW_022279431.1
    * slc31a1|GeneID:407919|NP_001001238.1 : NC_030684.2, NW_022279440.1
    * otud5|GeneID:448134|NP_001004849.1 : NC_030684.2, NW_022279442.1
    * prpf4|GeneID:394655|NP_989058.1 : NC_030684.2, NW_022279444.1
    * efna3|GeneID:496827|NP_001011360.1 : NC_030684.2, NW_022279502.1

* Make a non-redundant protein sequence file (collapse identical sequences).
  ```
  ./05.make-refseq-non_redundant_fasta.py <protein faa file (processed .prot_all.fa)>
  ```
  * 45,093 all protein sequences --> 37,591 non-redundant protein sequences.
    * 7,209 sequences were represented by a sequence of same gene (gene symbol and Gene ID are matched).
    * 293 sequences were represented by a sequence of different gene (gene symbol and GeneID are not matched).
    * See [the log file](./XENTR_xenTro10.refseq104.prot_all_NR.log) for more details. 

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


