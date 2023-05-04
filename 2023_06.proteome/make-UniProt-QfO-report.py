#!/usr/bin/env python3 
import sys
import gzip

up2ens = dict()
up2ncbi = dict()

filename_ens = 'raw/UP000008143_8364.gene2acc.gz'
filename_map = 'raw/UP000008143_8364.idmapping.gz'
filename_ref_all = '../2023_04.proteome/XENTR_xenTro10.XB2023_04.prot_nr_all.fa'
filename_ref_rep = '../2023_04.proteome/XENTR_xenTro10.XB2023_04.prot_nr_rep.fa'
filename_out = 'UP000008143_8364.2023_02.Xenbase_QfO_report.csv'

f_ens = gzip.open(filename_ens, 'rt')
for line in f_ens:
    tokens = line.strip().split("\t")
    up2ens[tokens[1]] = tokens[2]
f_ens.close()
sys.stderr.write('Accessions with EnsEMBL GeneID: %d\n' % len(up2ens))

f_map = gzip.open(filename_map, 'rt')
for line in f_map:
    tokens = line.strip().split("\t")
    tmp_acc = tokens[0]
    if tmp_acc not in up2ncbi:
        up2ncbi[tmp_acc] = {'gene': [], 'prot': [], 'tx': [], 'symbol': [], 'xenbase': []}

    if tokens[1] == 'GeneID':
        up2ncbi[tmp_acc]['gene'].append(tokens[2])
    elif tokens[1] == 'RefSeq':
        up2ncbi[tmp_acc]['prot'].append(tokens[2])
    elif tokens[1] == 'RefSeq_NT':
        up2ncbi[tmp_acc]['tx'].append(tokens[2])
    elif tokens[1] == 'Gene_Name':
        up2ncbi[tmp_acc]['symbol'].append(tokens[2])
    elif tokens[1] == 'Xenbase':
        up2ncbi[tmp_acc]['xenbase'].append(tokens[2])
f_map.close()

sys.stderr.write('Accessions with NCBI GeneID: %d\n' % len(up2ncbi))

rep_list =  []
f_rep = open(filename_ref_rep, 'r')
for line in f_rep:
    if line.startswith('>'):
        tmp_id = line.split()[2].replace('uniprot=', '')
        rep_list.append(tmp_id)
f_rep.close()

count_GeneSymbol = 0
count_RefSeqGeneID = 0
count_RefSeqTx = 0
count_RefSeqProt = 0
count_XbGeneID = 0
count_OK = 0
count_total = 0

f_fa = open(filename_ref_all, 'r')
f_out = open(filename_out, 'w')
f_out.write('#Remarks,IsRep,UniProtAcc,GeneSymbol,RefSeqGeneID,RefSeqTx,RefSeqProt,XbGeneID,UP_GeneSymbol,UP_RefSeqGeneID,UP_RefSeqTx,UP_RefSeqProt,UP_XbGeneID\n')
#>runx1t1|XP_004915205.1|XM_004915148.3|GeneID:100491944 xb_gene_id=XB-GENE-481238 uniprot=A0A5S6MBM4
for line in f_fa:
    if line.startswith('>'):
        count_total += 1
        tokens = line.strip().split()
        xb_id = tokens[1].replace('xb_gene_id=', '')
        uniprot_acc = tokens[2].replace('uniprot=', '')
        ncbi_tokens = tokens[0].lstrip('>').split('|')
        gene_symbol = ncbi_tokens[0]
        prot_id = ncbi_tokens[1]
        tx_id = ncbi_tokens[2]
        gene_id = ncbi_tokens[3]
        gene_id_bare = gene_id.split(':')[1]
        remark_list = []
        
        up_gene_symbol = 'NA'
        up_gene_id = 'NA'
        up_tx_id = 'NA'
        up_prot_id = 'NA'
        up_xb_id = 'NA'
        if uniprot_acc in up2ncbi:
            tmp_up2ncbi = up2ncbi[uniprot_acc]
            if len(tmp_up2ncbi['gene']) > 0:
                up_gene_id = ';'.join(sorted(list(set(tmp_up2ncbi['gene']))))
                if gene_id_bare not in tmp_up2ncbi['gene']:
                    remark_list.append('UpdateGeneID')
                    count_RefSeqGeneID += 1
            else:
                remark_list.append('UpdateGeneID')
                count_RefSeqGeneID += 1

            if len(tmp_up2ncbi['symbol']) > 0:
                up_gene_symbol = ';'.join(sorted(list(set(tmp_up2ncbi['symbol']))))
                if gene_symbol not in tmp_up2ncbi['symbol']:
                    remark_list.append('UpdateGeneSymbol')
                    count_GeneSymbol += 1
            else:
                remark_list.append('UpdateGeneSymbol')
                count_GeneSymbol += 1
            
            if len(tmp_up2ncbi['tx']) > 0:
                up_tx_id = ';'.join(sorted(list(set(tmp_up2ncbi['tx']))))
                if tx_id not in tmp_up2ncbi['tx']:
                    remark_list.append('UpdateRefSeqTx')
                    count_RefSeqTx += 1
            else:
                remark_list.append('UpdateRefSeqTx')
                count_RefSeqTx += 1
            
            if len(tmp_up2ncbi['prot']) > 0:
                up_prot_id = ';'.join(sorted(list(set(tmp_up2ncbi['prot']))))
                if prot_id not in tmp_up2ncbi['prot']:
                    remark_list.append('UpdateRefSeqProt')
                    count_RefSeqProt += 1
            else:
                remark_list.append('UpdateRefSeqProt')
                count_RefSeqProt += 1
            
            if len(tmp_up2ncbi['xenbase']) > 0:
                up_xb_id = ';'.join(sorted(list(set(tmp_up2ncbi['xenbase']))))
                if xb_id not in tmp_up2ncbi['xenbase']:
                    remark_list.append('UpdateXenbaseID')
                    count_XbGeneID += 1
            else:
                remark_list.append('UpdateXenbaseID')
                count_XbGeneID += 1

        else:
            remark_list.append('NoUniprotAcc')

        tmp_remark = 'OK'
        if len(remark_list) > 0:
            tmp_remark = ';'.join(sorted(list(set(remark_list))))
        else:
            count_OK += 1

        is_rep = 'N'
        if uniprot_acc in rep_list:
            is_rep = 'Y'

        f_out.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %
                    (tmp_remark, is_rep, uniprot_acc, gene_symbol, gene_id, tx_id, prot_id, xb_id, 
                     up_gene_symbol, up_gene_id, up_tx_id, up_prot_id, up_xb_id))
f_fa.close()

sys.stderr.write('Total proteins: %d\n' % count_total)
sys.stderr.write('OK: %d\n' % count_OK)
sys.stderr.write('UpdateGeneSymbol: %d\n' % count_GeneSymbol)
sys.stderr.write('UpdateRefSeqGeneID: %d\n' % count_RefSeqGeneID)
sys.stderr.write('UpdateRefSeqTx: %d\n' % count_RefSeqTx)
sys.stderr.write('UpdateRefSeqProt: %d\n' % count_RefSeqProt)
sys.stderr.write('UpdateXenbaseID: %d\n' % count_XbGeneID)
