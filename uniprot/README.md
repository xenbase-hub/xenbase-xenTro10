# UniProt resources for *Xenopus tropicalis*.

* https://www.uniprot.org/taxonomy/8364
* https://www.uniprot.org/proteomes/UP000008143
* https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000008143/


## Processed files
* https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/ (ID: amphibase  PW: ribbit)
  * [XENTR_xenTro10.uniprot2023_02.prot_all.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.uniprot2023_02.prot_all.fa.gz): All proteins
    * 37,774 sequences [XENTR_xenTro10.uniprot2023_02.prot_all.headers](./XENTR_xenTro10.refseq104.prot_all.headers)
  * [XENTR_xenTro10.uniprot2023_02.prot_all_NR.fa.gz](https://pub.amphibase.org/annotation/legacy/Xenopus_tropicalis/XENTR_xenTro10.uniprot2023_02.prot_all_NR.fa.gz): Non redundant proteins
    * 37,651 sequences [XENTR_xenTro10.uniprot2023_02.prot_all_NR.headers](./XENTR_xenTro10.refseq104.prot_all.headers)


## Procedures
* Download required files from UniProt.

  ``` ./01.download-uniprot.sh ```

  * [List of files for downloading](./FILES.UP000008143)

* Change the header format of protein sequences.

  ``` ./02.reformat-uniprot_prot_fasta.py <faa file> > <output filename>```

  ``` 
  [Original header]
  >sp|B1WAV2|RFX2_XENTR DNA-binding protein RFX2 OS=Xenopus tropicalis OX=8364 GN=rfx2 PE=2 SV=1
  
  [New header]
  >rfx2|B1WAV2 type=main;sp
  ```

* Make a non-redundant protein sequence file (collapse identical sequences).

  ``` ./03.make-uniprot-non_redundant_fasta.py <protein faa file (processed .prot_all.fa)> ```

  * 37,774 all protein sequences --> 37,651 non-redundant protein sequences.
    * 109 sequences were represented by a sequence with same gene name (Duplicate)
    * 14 sequences were represented by a sequence with different gene name (MultiName)
    * See [the log file](./XENTR_uniprot2023_02.prot_all_NR.log) for more details. 
  

## 2023_02 version
* Total 37,774 protein sequences
  * 22,227 reference proteins (UP000008143_8364)
  * 15,547 additional proteins (UP000008143_8364_additional)

* Vs. 2023_01 (see [a log file](uniprot2023_01-uniprot2023_02.compare.txt) for changes).
  * 37,055 sequences are identical.
  * No sequence is added.
  * 488 sequences changed symbols
  * 108 sequences changed types

## 2023_01 version
* Total 37,774 protein sequences
  * 22,282 reference proteins (UP000008143_8364)
  * 15,492 additional proteins (UP000008143_8364_additional)
