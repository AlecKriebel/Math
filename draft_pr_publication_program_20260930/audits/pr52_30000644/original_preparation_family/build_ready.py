"""Finalize a bounded source-only preparation inventory; READY is written last."""
from pathlib import Path
import datetime,hashlib,json,os,stat
F=Path(__file__).resolve().parent
assert not any((F/x).exists() for x in ['INDEX.json','READY.json','SELF_MANIFEST.json'])
final=json.loads((F/'captures/final_source_ready_check/COMPLETE.json').read_bytes());assert final['actual_execution'] is True and final['completed'] is True and final['exit_code']==0 and final['status']=='PASS'
for p in [F]+list(F.rglob('*')):
 st=p.lstat();assert not p.is_symlink() and (stat.S_ISREG(st.st_mode) or stat.S_ISDIR(st.st_mode));p.chmod(0o444 if stat.S_ISREG(st.st_mode) else 0o755)
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':stat.S_IMODE(p.lstat().st_mode)}
rows=sorted([identity(p) for p in F.rglob('*') if p.is_file()],key=lambda x:x['path']);dirs=sorted([{'path':str(p),'mode':stat.S_IMODE(p.lstat().st_mode)} for p in [F]+list(F.rglob('*')) if p.is_dir()],key=lambda x:x['path'])
assert 100<=len(rows)+2<=200 and all(r['mode']==0o444 for r in rows) and all(r['mode']==0o755 for r in dirs)
now=datetime.datetime.now(datetime.timezone.utc).isoformat();index={'schema':'pr52-original-source-payload-index/v1','created_utc':now,'payload_files':rows,'directories':dirs,'self_exclusions':['INDEX.json','READY.json','SELF_MANIFEST.json'],'full_modes_included':True,'source_only':True}
ip=F/'INDEX.json'
with ip.open('xb') as f:f.write((json.dumps(index,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
ip.chmod(0o444);h=hashlib.sha256(ip.read_bytes()).hexdigest()
ready={'schema':'pr52-original-source-ready/v1','created_utc':now,'index_sha256':h,'payload_file_count':len(rows),'complete_prepared_file_count':len(rows)+2,'directory_count_including_root':len(dirs),'payload_total_bytes':sum(x['bytes'] for x in rows),'self_manifest_present_at_preparer_handoff':False,'root_personal_read_attestation':False,'native_acceptance_authority':False,'remote_action_authority':False,'independent_new_mathematical_verdict':False,'source_preparation_completion_percent':100,'new_discovery_credit_percent':0,'original_status':'already_solved','original_substantive_search_attempts':0,'original_substantive_attempt_limit':5,'original_known_theorem_validation_activities':1,'full_journal_proof_certified':False,'close_source_sha256':hashlib.sha256((F/'close_family.py').read_bytes()).hexdigest(),'reader_source_sha256':hashlib.sha256((F/'read_closed_family.py').read_bytes()).hexdigest(),'common_source_sha256':hashlib.sha256((F/'closure_common.py').read_bytes()).hexdigest(),'closer_reader_executed_by_preparer':False,'root_closure_required_after_preparer_exit':True,'native_actual_acceptance_and_mathematical_reconciliation_remain_pending':True,'final_preparer_build_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'preparer_build_pid':os.getpid(),'build_process_completion_not_claimed_here':True}
rp=F/'READY.json';fd=os.open(str(rp),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
with os.fdopen(fd,'wb') as f:f.write((json.dumps(ready,indent=2,sort_keys=True)+'\n').encode());f.flush();os.fsync(f.fileno())
assert stat.S_IMODE(rp.stat().st_mode)==0o444
print(json.dumps({'status':'READY_SOURCE_ONLY','files':len(rows)+2,'directories':len(dirs),'index_sha256':h,'ready_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'self_manifest_present':False,'no_post_ready_writes':True},sort_keys=True))
