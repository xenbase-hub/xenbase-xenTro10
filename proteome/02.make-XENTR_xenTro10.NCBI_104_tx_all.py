#!/usr/bin/env python3
import sys
import gzip

filename_base = 'XENTR_xenTro10.NCBI_104'

# Source URL: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/latest_assembly_versions/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz

filename_gff = 'raw/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz'

# NC_030680.2	BestRefSeq	CDS	15937067	15937514	.	+	0	ID=cds-NP_001001190.1;Parent=rna-NM_001001190.1;Dbxref=GeneID:407851,Genbank:NP_001001190.1,Xenbase:XB-GENE-5809007;Name=NP_001001190.1;gbkey=CDS;gene=tmem178.2;product=transmembrane protein 178B precursor;protein_id=NP_001001190.1

# Source URL: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/latest_assembly_versions/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_protein.faa.gz

filename_fa = 'raw/GCF_000004195.4_UCB_Xtro_10.0_rna.fna.gz'

# >NM_001001190.1 Xenopus tropicalis transmembrane protein 178, gene 2 (tmem178.2), mRNA
# CCCAGCGCAGCAGCAGCACCACCTCTGCTTAGGCCCCTCCCGGCCGCACCGCCGCACCGCAGCCAGCAGGGGGAGCCACC
# TCTCCGGTTATCAGTCAGCCCTCTCTCCGGCGCTATGAGGCTGCTGGCCGGTGCCGGTCTGTGCTTGGCCCTGGCCGCTC

tx_info = dict()

f_gff = gzip.open(filename_gff, 'rt')
for line in f_gff:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tmp_type = tokens[2]

    tx_id = 'NA'
    xb_gene_id = 'NA'
    ncbi_gene_id = 'NA'
    gene_name = 'NA'

    if not tokens[8].startswith('ID=rna-'):
        continue
    for tmp in tokens[8].split(';'):
        if tmp.startswith('ID=rna-'):
            tx_id = tmp.split('=')[1].replace('rna-', '')
        if tmp.startswith('gene='):
            gene_name = tmp.split('=')[1]
        if tmp.startswith('Dbxref='):
            for tmp2 in tmp.split('=')[1].split(','):
                if tmp2.startswith('GeneID:'):
                    ncbi_gene_id = tmp2.split(':')[1]
                if tmp2.startswith('Xenbase:'):
                    xb_gene_id = tmp2.split(':')[1]

    if tx_id not in tx_info:
        tx_info[tx_id] = {'name': gene_name, 
                          'xb_gene_id': xb_gene_id, 
                          'ncbi_gene_id': ncbi_gene_id}
f_gff.close()

is_log = -1

f_fa = gzip.open(filename_fa, 'rt')
f_out = open('%s.tx_all.fa' % filename_base, 'w')
f_log = open('%s.tx_all.log' % filename_base, 'w')
for line in f_fa:
    if line.startswith('>'):
        tmp_id = line.strip().split()[0].lstrip('>')

        # stop if there is no protein_id in the GFF3 file
        if tmp_id not in tx_info:
            sys.stderr.write('No_ID: %s\n' % tmp_id)
            sys.exit(1)
        else:
            tmp_t = tx_info[tmp_id]
            tmp_h = '%s|%s|GeneID:%s xb_gene_id=%s' %\
                    (tmp_t['name'], tmp_id, 
                     tmp_t['ncbi_gene_id'], tmp_t['xb_gene_id'])

            if tmp_t['ncbi_gene_id'] == 'NA':
                is_log = 1
                sys.stderr.write('ncbi_gene_id error: %s\n' % tmp_h)
                f_log.write('ncbi_gene_id error: >%s\n' % tmp_h)
                f_out.write('>%s\n' % tmp_h)
            else:
                is_log = -1
                f_out.write('>%s\n' % tmp_h)
    else:
        #if is_log > 0:
        #    f_log.write('%s\n' % line.strip())

        f_out.write('%s\n' % line.strip())
f_fa.close()
f_log.close()
f_out.close()
