"""Dated retained three-old-row repair receipts; no fresh service/CRC/proof claims."""
from pathlib import Path
import hashlib,json,sys,re,lzma
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
W=R/'audits/final_reconciliation_new_independent_adversary01'
p=W/'independent_checks.py';b=p.read_bytes();assert hashlib.sha256(b).hexdigest()=='63f9f0d1cd4d8e8d87b3c087ce8db2535ef526db3f359e2df7f4c13ce550aa8a'
n={'__name__':'_readonly_three_old_repairs','__file__':str(p)};exec(compile(b,str(p),'exec'),n)
pins={
248:('797a3a08c714f837a07d8fc5de6f24ff74953dd7e7c6425b3f9cb81e2948608d',10911,'6e9915c4f2a1a991b5b0e7e6daa60309478aee265d6a6b97550a9228da275a73',4802,23358014,87,'30004630'),
254:('736a860e30ab8a36336feeec4a1fbf7f782a947aa99d9d7d1e854dbfb31aa222',8025,'e32e9dfee1969d0b7f289d864bbadba6f754ae3287ae825b236a63efba1f7170',4048,23334001,79,'5100020'),
256:('091883fb12214cc87ff60ce6d90acb230786226c9e9a785e0aad293b0768ddb6',6799,'a110f61bf864fba05f587717fa689becba08c38cbaaa44aa1c39ddbb8048dcb3',4417,23331331,69,'5100017')}
j=n['frozen_join']()['baseline']()
ins=n['strict'](lzma.decompress((n['J']/'private/LOCAL_ORIGINAL_INPUTS.json.xz').read_bytes()))
sheetpin=next(p for p in ins['external_pins']if p['path'].endswith('/AFTER_COMPLETE_SHEET.json'))
sheet=n['objpin'](sheetpin);n['strict_sheet'](sheet)
out=[]
for pr,(ps,pb,rs,rb,record,row,pid)in pins.items():
 pp={'path':str(R/f'PR{pr:04}_PUBLICATION_VERIFICATION.json'),'bytes':pb,'sha256':ps}
 rp={'path':str(R/f'PR{pr:04}_LEDGER_REPAIR.json'),'bytes':rb,'sha256':rs}
 pub=n['objpin'](pp);repair=n['objpin'](rp);doi='10.5281/zenodo.'+str(record)
 assert pub['doi']==repair['doi']==doi and pub['record']==repair['record']==record and pub['ledger_row']==repair['row']==row
 assert pub['published']is True and pub['doi_resolution']=={'status':200,'final_url':'https://zenodo.org/records/'+str(record)}
 assert repair['pr']==pr and repair['status']=='verified'and repair['updated']is True and repair['new_publication']is False and repair['new_row']is False
 assert repair['rows_before']==repair['rows_after']==173 and repair['unique_primary_doi_count']==1 and repair['observed_changes']==[{'columns':[4],'row':row}]
 assert repair['new_notes'].startswith(repair['old_notes'])and repair['new_notes']!=repair['old_notes']and pid in repair['new_notes']and 'https://github.com/AlecKriebel/Math/pull/'+str(pr)in repair['new_notes']
 assert repair['final_row'][3]==repair['new_notes']and n['typed'](sheet['values'][row-1][:4],repair['final_row'])
 response=repair['find_replace_response']
 assert response['spreadsheetId']==n['BOOK']and response['replies']==[{'findReplace':{'occurrencesChanged':1,'rowsChanged':1,'sheetsChanged':1,'valuesChanged':1}}]
 c=next(x for x in j['rows']if x['pr']==pr)['coverage'];assert c['doi']==doi and c['row']==row
 files=pub['files'];assert len(files)==2 and sum(f['name'].endswith('.pdf')for f in files)==sum(f['name'].endswith('.zip')for f in files)==1
 reported=[]
 for f in files:
  assert f['download_verified']is True and type(f['size'])is int and f['size']>0 and re.fullmatch('[0-9a-f]{64}',f['sha256'])and re.fullmatch('md5:[0-9a-f]{32}',f['checksum'])
  if f['name'].endswith('.zip'):assert f['zip_crc_ok']is True and type(f['members'])is list and bool(f['members'])and len(f['members'])==len(set(f['members']))
  reported.append({k:f[k]for k in['name','size','sha256','checksum','download_verified']}|({'reported_zip_crc_ok':True,'reported_member_count':len(f['members'])}if f['name'].endswith('.zip')else{}))
 out.append({'pr':pr,'DOI':doi,'existing_row':row,'literal_four_cells_sha256':n['H'](n['C'](repair['final_row'])),'original_note_preserved_prefix':True,'receipt_pins':[pp,rp],'reported_files':reported})
print(json.dumps({'status':'PASS_DATED_THREE_EXISTING_ROW_REPAIR_AND_REPORTED_PAYLOAD_RECEIPTS','new_papers':0,'new_rows':0,'old_rows_repaired':3,'reported_PDFs':3,'reported_supporting_ZIPs':3,'rows':out,'dated252snapshot':sheetpin,'limitation':'Exact retained receipt consistency and existing252readback. Original receipts report download/CRC/DOI success; no fresh download, underlying transport replay, CRC rerun, proof or novelty audit is claimed here.','services':0,'final_clearance':False},sort_keys=True,indent=2))
