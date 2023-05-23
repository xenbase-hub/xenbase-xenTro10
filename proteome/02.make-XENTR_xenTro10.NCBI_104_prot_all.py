#!/usr/bin/env python3
import sys
import gzip

filename_base = 'XENTR_xenTro10.NCBI_104'

# Source URL: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/latest_assembly_versions/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz

filename_gff = 'raw/GCF_000004195.4_UCB_Xtro_10.0_genomic.gff.gz'

# NC_030680.2	BestRefSeq	CDS	15937067	15937514	.	+	0	ID=cds-NP_001001190.1;Parent=rna-NM_001001190.1;Dbxref=GeneID:407851,Genbank:NP_001001190.1,Xenbase:XB-GENE-5809007;Name=NP_001001190.1;gbkey=CDS;gene=tmem178.2;product=transmembrane protein 178B precursor;protein_id=NP_001001190.1

# Source URL: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/vertebrate_other/Xenopus_tropicalis/latest_assembly_versions/GCF_000004195.4_UCB_Xtro_10.0/GCF_000004195.4_UCB_Xtro_10.0_protein.faa.gz

filename_fa = 'raw/GCF_000004195.4_UCB_Xtro_10.0_protein.faa.gz'

# >NP_001001190.1 transmembrane protein 178B precursor [Xenopus tropicalis]
# MRLLAGAGLCLALAALALLAVALSTDHWYETDARRHRDRCRKPGGKRNDPGYMYTPGQHLPLRGEPPSSRIRSPRGGEPG
# GVRMISRAEDLGVRGLRERPTGARDLPLSRPYLATDPHCSRRFNSTVSGLWRKCHRDGFDKDTEELILKGIVERCTSVRY

prot_info = dict()

f_gff = gzip.open(filename_gff, 'rt')
for line in f_gff:
    if line.startswith('#'):
        continue
    tokens = line.strip().split("\t")
    tmp_type = tokens[2]
    if tmp_type != 'CDS':
        continue

    tx_id = 'NA'
    prot_id = 'NA'
    xb_gene_id = 'NA'
    ncbi_gene_id = 'NA'
    gene_name = 'NA'
    for tmp in tokens[8].split(';'):
        if tmp.startswith('Parent='):
            tx_id = tmp.split('=')[1].replace('rna-', '')
        if tmp.startswith('protein_id='):
            prot_id = tmp.split('=')[1]
        if tmp.startswith('gene='):
            gene_name = tmp.split('=')[1]
        if tmp.startswith('Dbxref='):
            for tmp2 in tmp.split('=')[1].split(','):
                if tmp2.startswith('GeneID:'):
                    ncbi_gene_id = tmp2.split(':')[1]
                if tmp2.startswith('Xenbase:'):
                    xb_gene_id = tmp2.split(':')[1]

    if prot_id not in prot_info:
        prot_info[prot_id] = {'name': gene_name, 'tx_id': tx_id,
                              'xb_gene_id': xb_gene_id,
                              'ncbi_gene_id': ncbi_gene_id}
f_gff.close()

is_log = -1

f_fa = gzip.open(filename_fa, 'rt')
f_out = open('%s.prot_all.fa' % filename_base, 'w')
f_log = open('%s.prot_all.log' % filename_base, 'w')
for line in f_fa:
    if line.startswith('>'):
        tmp_id = line.strip().split()[0].lstrip('>')

        # stop if there is no protein_id in the GFF3 file
        if tmp_id not in prot_info:
            sys.stderr.write('No_ID: %s\n' % tmp_id)
            sys.exit(1)
        else:
            tmp_p = prot_info[tmp_id]
            tmp_h = '%s|%s|%s|GeneID:%s xb_gene_id=%s' %\
                    (tmp_p['name'], tmp_id, tmp_p['tx_id'],
                     tmp_p['ncbi_gene_id'], tmp_p['xb_gene_id'])

            if tmp_p['tx_id'].find('_') < 0:
                is_log = 1
                sys.stderr.write('tx_id error: %s\n' % tmp_h)
                f_log.write('tx_id error: >%s\n' % tmp_h)
                f_out.write('>%s\n' % tmp_h)
            elif tmp_p['ncbi_gene_id'] == 'NA':
                is_log = 1
                sys.stderr.write('ncbi_gene_id error: %s\n' % tmp_h)
                f_log.write('ncbi_gene_id error: >%s\n' % tmp_h)
                f_out.write('>%s\n' % tmp_h)
            else:
                is_log = -1
                f_out.write('>%s\n' % tmp_h)
    else:
        # if is_log > 0:
        #    f_log.write('%s\n' % line.strip())

        f_out.write('%s\n' % line.strip())
f_fa.close()
f_log.close()
f_out.close()
