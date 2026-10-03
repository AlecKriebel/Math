"""Final preparation-only readback; ROOT closer/reader remain unexecuted SOURCE."""
from pathlib import Path
import ast,datetime,hashlib,json,stat
F=Path(__file__).resolve().parent
checks=0
def ck(v):
 global checks;assert v;checks+=1
def sha(b):return hashlib.sha256(b).hexdigest()
for p in sorted(F.rglob('*')):
 st=p.lstat();ck(not p.is_symlink() and (stat.S_ISREG(st.st_mode) or stat.S_ISDIR(st.st_mode)))
 if p.is_file():
  b=p.read_bytes();ck(len(b)==st.st_size)
  if p.suffix=='.py':ast.parse(b,filename=str(p));checks+=1
ck(not (F/'SELF_MANIFEST.json').exists() and not (F/'INDEX.json').exists() and not (F/'READY.json').exists())
readback=json.loads((F/'PREPARATION_READBACK.json').read_bytes());ck(readback['status']=='PASS_PREPARATION_AUTHENTICATION_AND_LITERAL_REPLAY_ONLY');ck(readback['original_science_file_count']==19 and readback['original_science_bytes']==79731 and readback['full_diff_bytes']==88749)
capnames=[]
for d in sorted((F/'captures').iterdir()):
 if d.name=='final_source_ready_check':ck((d/'PRELAUNCH.json').exists() and not (d/'COMPLETE.json').exists());continue
 c=json.loads((d/'COMPLETE.json').read_bytes());ck(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int)
 for n in ['STDOUT.bin','STDERR.bin']:
  b=(d/n).read_bytes();ck(len(b)==c[n]['bytes'] and sha(b)==c[n]['sha256'])
 op=(d/'OPERATOR_PRELAUNCH.py').read_bytes();ck(len(op)==c['operator']['bytes'] and sha(op)==c['operator']['sha256']);ck(op==(F/'capture_private.py').read_bytes())
 for x in c['sources']:
  for r in [x['original'],x['saved']]:
   b=Path(r['path']).read_bytes();ck(len(b)==r['bytes'] and sha(b)==r['sha256'])
 if d.name=='existing_original_git':ck(c['exit_code']==128 and c['status']=='FAIL')
 elif d.name=='preparation_readback':ck(c['exit_code']==1 and c['status']=='FAIL')
 else:ck(c['exit_code']==0 and c['status']=='PASS')
 capnames.append(d.name)
ck('preparation_readback_v2' in capnames and len(capnames)==13)
refs=json.loads((F/'REFERENCE_BINDINGS.json').read_bytes());seen=set()
for cat in ['fixed_upstream_and_stable_reference_rows','dated_derived_cache_rows','dated_mutable_native_rows']:
 for r in refs[cat]:
  ck(set(r)=={'path','bytes','sha256','mode'} and type(r['bytes']) is int and type(r['mode']) is int);ck(r['path'] not in seen);seen.add(r['path'])
  if cat=='fixed_upstream_and_stable_reference_rows':
   p=Path(r['path']);b=p.read_bytes();ck(len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.lstat().st_mode)==r['mode'])
auth=json.loads((F/'ORIGINAL_AUTHENTICATION.json').read_bytes());ck(len(auth['primary_science_files'])==19)
for r in auth['primary_science_files']:
 b=Path(r['local_identity']['path']).read_bytes();ck(len(b)==r['local_identity']['bytes'] and sha(b)==r['local_identity']['sha256']);ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha1'])
source=Path(__file__).read_bytes();record={'schema':'pr52-final-preparation-source-readback/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_preparation_check_pid':__import__('os').getpid(),'status':'PASS_PREPARATION_ONLY','checks':checks,'completed_prior_capture_count':13,'completed_prior_capture_names':capnames,'currently_running_wrapper_excluded':'final_source_ready_check','source_sha256':sha(source),'root_closer_and_reader_executed':False,'self_manifest_present':False,'root_personal_read_attestation':False,'independent_new_mathematical_verdict':False,'native_and_remote_authority':False}
(F/'FINAL_SOURCE_READY_READBACK.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':record['status'],'checks':checks,'completed_prior_capture_count':13,'root_or_production_authority':False},sort_keys=True))
