"""First-party reproduction orchestration; all foreign copies stay in ignored tmp."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,platform,shutil,subprocess,sys
OWN=Path(__file__).resolve().parent
ROOT=OWN.parent
TMP=OWN/'tmp'/'replays'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(x):
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k!='utc'}
 if isinstance(x,list):return [clean(v) for v in x]
 return x
jobs=[('original_author','source_snapshot',['check_small_planes.py'],['check_results.json']),('historical_reviewer','source_snapshot/review',['independent_checks.py'],['independent_checks.json']),('blocker','blocker_family',['fresh_affine_checks.py','dual_count_controls.py'],['fresh_checks.json','fresh_certificates.json','dual_count_results.json']),('probability','probability_family',['fresh_probability_controls.py'],['fresh_probability_results.json']),('source_container','source_container_family',['parameter_certificate.py'],['parameter_certificate.json'])]
def replay(job):
 name,src,scripts,outputs=job;dest=TMP/name;dest.mkdir(parents=True,exist_ok=True);before={}
 for s in scripts:shutil.copyfile(ROOT/src/s,dest/s);before[s]=sha(dest/s)
 runs=[]
 for s in scripts:
  r=subprocess.run([sys.executable,str(dest/s)],capture_output=True,text=True,timeout=180)
  runs.append({'script':s,'returncode':r.returncode,'stderr':r.stderr[-1500:]})
  if r.returncode:break
 compares=[]
 for x in outputs:
  p=dest/x;original=ROOT/src/x
  compares.append({'output':x,'exists':p.exists(),'bytes_match':p.exists() and p.read_bytes()==original.read_bytes(),'math_fields_match_ignoring_utc':p.exists() and clean(json.loads(p.read_text()))==clean(json.loads(original.read_text())),'stored_sha256':sha(original),'replayed_sha256':sha(p) if p.exists() else None})
 return {'job':name,'runs':runs,'comparisons':compares,'foreign_script_hashes':before,'scripts_unchanged':all(sha(dest/s)==before[s] for s in scripts)}
results=list(concurrent.futures.ThreadPoolExecutor(5).map(replay,jobs))
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'platform':platform.platform(),'results':results,'all_math_match':all(all(x['math_fields_match_ignoring_utc'] for x in r['comparisons']) and r['scripts_unchanged'] and all(x['returncode']==0 for x in r['runs']) for r in results),'foreign_copies':'ignored tmp/replays only','original_head':'f1053196b6405623d5f5d8611289939765918d72'}
(OWN/'REPRODUCTION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
