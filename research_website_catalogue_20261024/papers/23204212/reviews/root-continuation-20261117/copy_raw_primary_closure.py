from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;S=R.parent/'adversarial-continuation-20261117';D=R/'primary'
assert not D.exists()
manifest=S/'FINAL_MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='7f98849c904df24dffdb92f021670d68fd54f110c8801e5b01a4cb8084efd7c2'
entries=json.loads(manifest.read_text())['entries']
chosen=[e for e in entries if e['kind']=='file' and e['path'].startswith('primary/') and (e['path'].endswith('.pdf') or (e['path'].startswith('primary/lean/') and e['path'].endswith('.lean')))]
assert len(chosen)==75 and sum(e['path'].endswith('.lean') for e in chosen)==68
D.mkdir();rows=[];commands=[]
for e in chosen:
 n=e['path'];f=S/n;b=f.read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
 out=R/n;out.parent.mkdir(exist_ok=True);out.write_bytes(b);out.chmod(0o444)
 rows.append({'path':n,'bytes':len(b),'SHA256':e['sha256'],'source':str(f)})
 if n.endswith('.pdf'):
  argv=['pdftotext','-layout',str(out),str(out)+'.txt'];p=subprocess.run(argv,capture_output=True,check=False)
  (Path(str(out)+'.pdftotext.stdout.bin')).write_bytes(p.stdout);(Path(str(out)+'.pdftotext.stderr.bin')).write_bytes(p.stderr)
  commands.append({'argv':argv,'exit':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)})
  (R/'PRIMARY_COPY_EXECUTIONS.json').write_text(json.dumps(commands,indent=2)+'\n');assert p.returncode==0
 assert f.read_bytes()==b
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'RAW_PRIMARY_COPY_AUTHENTICATED','files':rows,'Lean_files':68,'PDFs':7,'root_has_not_opened_current_peer_mathematical_reports':True,'proof_reading_not_inferred_from_copy':True,'root_scientific_or_Lean_program_execution':False,'source_raw_primary_files_unchanged':True,'third_party_rights':'Private source reading copies only; excluded from public checkpoint payloads'}
(R/'PRIMARY_COPY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'files':75,'data_exits':[r['exit'] for r in commands]}))
