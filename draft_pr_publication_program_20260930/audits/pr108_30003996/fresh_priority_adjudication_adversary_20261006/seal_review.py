import json,hashlib,os,sys
from pathlib import Path
from datetime import datetime,timezone
W=Path(__file__).resolve().parent
utc=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def pin(p):
 b=p.read_bytes();return {'relative_path':str(p.relative_to(W)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def put(n,d):(W/n).write_text(json.dumps(d,indent=2)+'\n')
put('SEAL_EXECUTION_RECEIPT.json',{'UTC_start':utc(),'operator_pid':os.getpid(),'argv':[sys.executable,*sys.argv],'source':pin(Path(__file__).resolve()),'meaning':'Actual seal operator entry receipt; completion UTC and result are in SEAL.json and returned tool output. No stdout hash is invented.'})
private=[pin(p) for p in sorted((W/'private').rglob('*')) if p.is_file()]
put('PRIVATE_CUSTODY_MANIFEST.json',{'UTC':utc(),'files':private,'custody':'Private ignored raw source/extraction/search result and diagnostic execution bodies; metadata only, no redistributed source content.'})
exclude={'PUBLIC_MANIFEST.json','SEAL.json','SHA256SUMS'}
public=[pin(p) for p in sorted(W.iterdir()) if p.is_file() and p.name not in exclude]
put('PUBLIC_MANIFEST.json',{'UTC':utc(),'files':public,'self_and_outer_seal_excluded':sorted(exclude),'private_custody_manifest':'PRIVATE_CUSTODY_MANIFEST.json','scope':'This bounded priority-disposition audit only; no publication package certified.'})
sha=[pin(p) for p in sorted(W.iterdir()) if p.is_file() and p.name not in {'SHA256SUMS','SEAL.json'}]
(W/'SHA256SUMS').write_text(''.join(p['sha256']+'  '+p['relative_path']+'\n' for p in sha))
allpublic=[pin(p) for p in sorted(W.iterdir()) if p.is_file() and p.name!='SEAL.json']
val=json.loads((W/'VALIDATION_RESULT.json').read_text())
assert val['status']=='PASS'
seal={'schema':'fresh-priority-disposition-seal/v1','UTC':utc(),'operator_pid':os.getpid(),'operator_argv':[sys.executable,*sys.argv],'scope':'Sealed bounded adversarial disposition. Not a first-in-history claim, publication waiver, or unseen-package certificate.','all_public_files_except_self':allpublic,'public_manifest':pin(W/'PUBLIC_MANIFEST.json'),'private_manifest':pin(W/'PRIVATE_CUSTODY_MANIFEST.json'),'validation':val,'criteria_frozen_sha256':'8714cd68a1e383963d4cad32477eef40f23fc48b295c0db2f235b82e0c051f8c','self_excluded':'SEAL.json'}
put('SEAL.json',seal)
print(json.dumps({'UTC':seal['UTC'],'public_files_bound':len(allpublic),'private_files_bound':len(private),'seal_sha256':hashlib.sha256((W/'SEAL.json').read_bytes()).hexdigest(),'status':'SEALED'}))
