"""Fresh primary-byte bindings only, before reading candidate proof/code."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;S=A/'snapshot/unsolved_math_prioritization/attempts/2303016'
D=A/'root_primary_private';D.mkdir(exist_ok=True)
rows=[]
for row in json.loads((S/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs']:
 start=datetime.now(timezone.utc).isoformat()
 r=subprocess.run(['curl','--location','--fail','--silent','--show-error','--connect-timeout','15','--max-time','60',row['url']],capture_output=True)
 (D/row['file']).write_bytes(r.stdout);(D/(row['file']+'.stderr')).write_bytes(r.stderr)
 actual={'file':row['file'],'url':row['url'],'bytes':len(r.stdout),'sha256':hashlib.sha256(r.stdout).hexdigest(),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stderr_bytes':len(r.stderr)}
 actual['matches_frozen_primary_binding']=actual['bytes']==row['bytes'] and actual['sha256']==row['sha256'];rows.append(actual)
 (A/'ROOT_PRIMARY_RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
 assert r.returncode==0 and r.stderr==b'' and actual['matches_frozen_primary_binding'],actual
 out=subprocess.run(['pdftotext','-layout',str(D/row['file']),str(D/(row['file']+'.txt'))],capture_output=True)
 assert out.returncode==0 and out.stderr==b''
print(json.dumps({'status':'FRESH_BOTH_PRIMARY_BYTES_PASS','sources':rows,'candidate_proof_or_code_read':False},indent=2))
