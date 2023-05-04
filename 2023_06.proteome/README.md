# Reference proteome of Xenopus tropicalis (2023_06).

## Review for Quest for Orthologs (QfO). 

* Download the _Xenopus tropicalis_ proteomes id mapping file from UniProt 2023_02 release.
  * https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000008143/UP000008143_8364.idmapping.gz
* Extract information with the following keywords: GeneID, RefSeq, RefSeq_NT, GeneName, Xenbase
* Compare it with the 2023_04 ID-symbol mapping table. 
  * ../2023_04/XENTR_xenTro10.gene_symbols.XB2023_04.csv

* Make a report: UP000008143_8364.2023_02.Xenbase_QfO_report.csv
  * Total proteins: 37416 (same as ID-symbol mapping table)
  * OK: 16129 (matched with current table)
  * UpdateGeneSymbol: 1847 (needs to update gene symbol)
  * UpdateRefSeqGeneID: 18445 (needs to update NCBI GeneID)
  * UpdateRefSeqTx: 312 (needs to update RefSeq_NT)
  * UpdateRefSeqProt: 74 (needs to update RefSeq)
  * UpdateXenbaseID: 16844 (needs to update Xenbase Gene ID)
