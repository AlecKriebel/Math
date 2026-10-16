from pathlib import Path
import json,hashlib,datetime,urllib.request,subprocess
OWN=Path(__file__).resolve().parent;OUT=OWN/'external_reading';OUT.mkdir(exist_ok=True)
old=OWN.parent.parent/'initial_review_20261013'
items=[
('KMv1','https://arxiv.org/pdf/1907.02744v1',old/'source_pde_adversary_02/private_reading/kunisch-meinlschmidt-v1.pdf',[8,9,19,20,21,25,26,27,35,36,37,38]),
('OWR','https://publications.mfo.de/bitstream/handle/mfo/3850/OWR_2021_09.pdf',old/'source_pde_adversary_02/private_reading/owr2021-09.pdf',[20,21,22]),
('KMauthor','https://hannes.meinlschmidt.eu/preprint/KunischMeinlschmidt2020.pdf',old/'source_pde_adversary_02/private_reading/author-version.pdf',[8,19,20,26,35]),
('BWfinal','https://jnsao.episciences.org/14959/pdf',old/'priority_classical_adversary_01/private_reading/BW2024.pdf',[3,4,12,13,34,35]),
('CHW','https://www.numdam.org/item/10.1051/cocv/2015048.pdf',old/'priority_classical_adversary_01/private_reading/CHW2017.pdf',[1,22,30,31,32,33]),
('CTsurvey','https://www.mathematik.de/images/DMV/Jahresberichte/Jahresberichte_Archiv/2015.117Heft1.pdf',old/'priority_classical_adversary_01/private_reading/CT2015survey.pdf',[25,26])]
ledger=[]
for name,url,local,pages in items:
 p=OUT/(name+'.pdf');row={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'existing_primary_copy':str(local),'complete_pages_to_read':pages}
 expected=local.read_bytes();row['existing_bytes']=len(expected);row['existing_sha256']=hashlib.sha256(expected).hexdigest()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source audit'})
  with urllib.request.urlopen(req,timeout=30) as response: data=response.read();row['response_url']=response.url;row['http_status']=response.status
  assert data.startswith(b'%PDF'),data[:100]
  p.write_bytes(data);row.update({'fresh_bytes':len(data),'fresh_sha256':hashlib.sha256(data).hexdigest(),'fresh_equals_existing_primary':data==expected,'fresh_retrieval':True})
 except Exception as e:
  row.update({'fresh_retrieval':False,'retrieval_error':str(e),'fallback_to_local_primary':True});p.write_bytes(expected)
 print(name,row.get('fresh_equals_existing_primary',False),row.get('retrieval_error',''),flush=True)
 for page in pages:
  text=OUT/(name+'-p'+str(page)+'.txt')
  subprocess.run(['pdftotext','-layout','-f',str(page),'-l',str(page),str(p),str(text)],check=True)
 row['local_reading_copy_excluded_from_public_manifest']=str(p.relative_to(OWN));ledger.append(row)
(OWN/'SOURCE_VERSION_LEDGER.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':ledger,'external_whole_reading_copies_publicly_excluded':True,'publisher_KM_final_body_not_inspected':True,'KM_final_identification_not_silently_inferred_from_preprints':True},indent=2)+'\n')
