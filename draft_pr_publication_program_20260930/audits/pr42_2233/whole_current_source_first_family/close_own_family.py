"""Close only this independent audit family, with self-only exclusion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
root=Path(__file__).resolve().parent
started=datetime.now(timezone.utc).isoformat()
manifest=root/'OWN_CLOSED_MANIFEST.json'
if manifest.exists():raise RuntimeError('Never overwrite closed family')
files=[]
for p in sorted(root.rglob('*')):
 if p.is_symlink():raise RuntimeError('Symlink not allowed')
 if not p.is_file():continue
 b=p.read_bytes();p.chmod(0o444)
 files.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'permission_mode':'0o444','classification':'own authored or actual own generated capture'})
foreign=json.loads((root/'FOREIGN_INPUT_ROWS.json').read_text())['files']
record={'schema':'PR42_NEW_WHOLE_CURRENT_ADVERSARY_CLOSED_FAMILY_v1','root':str(root),'closure_pid':os.getpid(),'closure_started_utc':started,'closure_finished_utc':datetime.now(timezone.utc).isoformat(),'status':'CLOSED_PASS_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY','self_excluded':['OWN_CLOSED_MANIFEST.json'],'files_count':len(files),'files':files,'foreign_files_individually_pinned_and_excluded':foreign,'foreign_copies_inside_family':[],'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'candidate_manifest_sha256':'09ac3a27edc2113da9574e57a13e7a0c99baa194fa50efb07548ec47fa7493de','scope':'new whole current qualified partial review only; ROOT publication decision separate','all_own_files_mode':'stat.S_IMODE0444','current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'historic_runtime_certified':False}
manifest.write_text(json.dumps(record,indent=2)+'\n');manifest.chmod(0o444)
for r in files:
 p=root/r['path'];b=p.read_bytes()
 if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256'] or stat.S_IMODE(p.stat().st_mode)!=0o444:raise RuntimeError('Closure verification failed')
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual!={r['path'] for r in files}|{'OWN_CLOSED_MANIFEST.json'}:raise RuntimeError('Exact closure failed')
print(json.dumps({'status':record['status'],'manifest':str(manifest),'sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'first_party_files_excluding_self':len(files),'foreign_individual_rows':len(foreign),'actual_closure_pid':os.getpid()}))
