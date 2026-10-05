"""Fetch full original sources before candidate proof or code is opened."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,urllib.request
A=Path(__file__).resolve().parent;D=A/'root_primary_private';D.mkdir(exist_ok=True)
sources=[('hayman_lingham_2018','https://arxiv.org/pdf/1809.07200',1706228,'8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0'),('carleson_1976','https://www.acadsci.fi/mathematica/Vol02/vol02pp035-039.pdf',3653618,'4f4d183b2bdb68752b9c46d7bd866748a25615d2ab2d8b3b7a2644d28cc29aae')];receipts=[]
for name,url,size,pin in sources:
 start=datetime.now(timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=60) as response:b=response.read();resolved=response.url;headers=dict(response.headers.items())
 end=datetime.now(timezone.utc).isoformat();p=D/(name+'.pdf');p.write_bytes(b)
 assert len(b)==size and hashlib.sha256(b).hexdigest()==pin
 z=subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],capture_output=True)
 (D/(name+'.extract.stdout')).write_bytes(z.stdout);(D/(name+'.extract.stderr')).write_bytes(z.stderr);assert z.returncode==0 and not z.stderr
 receipts.append({'name':name,'requested_url':url,'resolved_url':resolved,'start_utc':start,'end_utc':end,'response_headers':headers,'bytes':size,'sha256':pin,'pdf_path':str(p),'text_sha256':hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest(),'extraction_exit':z.returncode,'extraction_stdout_bytes':len(z.stdout),'extraction_stderr_bytes':len(z.stderr)})
(A/'ROOT_PRIMARY_RECEIPTS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'candidate_proof_code_historical_reviews_not_read':True,'prior_routing_only':'Original PR title/bodymetadata/filenames, SOURCE_MANIFEST and SOURCE_NORMALIZATION read; source-first baseline will describe that disclosure','sources':receipts},indent=2)+'\n')
print(json.dumps({'status':'BOTH_COMPLETE_PRIMARY_DOWNLOADS_EXACT','sources':[{'name':e['name'],'bytes':e['bytes'],'sha256':e['sha256']} for e in receipts]},indent=2))
