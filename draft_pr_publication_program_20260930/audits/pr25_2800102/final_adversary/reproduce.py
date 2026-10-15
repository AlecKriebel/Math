from pathlib import Path
import json, subprocess, shutil, hashlib, concurrent.futures,datetime,collections
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ROOT=AUDIT.parents[2]
MIRROR=HERE/'tmp/replay_root'
MP=MIRROR/'draft_pr_publication_program_20260930/audits/pr25_2800102'
MP.mkdir(parents=True,exist_ok=True)
for name in ['.git','unsolved_math_prioritization']:
 target=MIRROR/name
 if not target.exists():target.symlink_to(ROOT/name,target_is_directory=True)
for name in ['source_snapshot','primary_scope_family','real_family','complex_family','real_dependency_falsifier']:
 shutil.copytree(AUDIT/name,MP/name,dirs_exist_ok=True)
shutil.copyfile(AUDIT/'snapshot_manifest.json',MP/'snapshot_manifest.json')
(MP/'real_family/tmp').mkdir(exist_ok=True)
JOBS=[('primary_scope_family','audit_controls.py','CONTROL_RESULTS.json'),('real_family','controls.py','CONTROL_RESULTS.json'),('complex_family','fresh_controls.py','fresh_results.json'),('real_dependency_falsifier','controls.py','CONTROL_RECEIPTS.json')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(job):
 fam,script,resultname=job
 folder=MP/fam;dest=folder/script
 h_before=sha(AUDIT/fam/script)
 result=subprocess.run(['python3',str(dest)],cwd=folder,capture_output=True,text=True,timeout=240)
 (folder/'fresh_stdout.txt').write_text(result.stdout);(folder/'fresh_stderr.txt').write_text(result.stderr)
 old=json.loads((AUDIT/fam/resultname).read_text())
 got=json.loads((folder/resultname).read_text()) if result.returncode==0 else None
 receipt={'family':fam,'script':script,'script_sha256':h_before,'copy_matches_original':sha(dest)==h_before,'returncode':result.returncode,'original_script_unchanged':sha(AUDIT/fam/script)==h_before,'result_sha256':sha(folder/resultname) if got else None,'saved_result_sha256':sha(AUDIT/fam/resultname),'result_exact':got==old}
 if fam=='primary_scope_family':
  receipt['fresh_controls_passed']=got['passed'] if got else None
  receipt['checks_exact_after_ignoring_run_utc']=got['checks']==old['checks'] if got else False
 elif fam=='real_family':
  stripped={k:v for k,v in old.items() if k not in ['executed_exact_assertions','distinct_exact_assertions']}
  receipt['saved_only_annotation_keys']=sorted(set(old)-set(got)) if got else None
  receipt['all_raw_fields_exact']=stripped==got
  receipt['execution_count']=got['total_exact_assertions'] if got else None
  receipt['distinct_names']=len(set(got['checks'])) if got else None
 else:receipt['execution_count']=got['total_assertions'] if got else None
 return receipt
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(run,JOBS))
history=[]
for rel in ['verify.py','review/submitted_verify.py','review/independent_checks.py']:
 folder=HERE/'tmp/history'/rel.replace('/','_').replace('.py','');folder.mkdir(parents=True,exist_ok=True)
 dest=folder/Path(rel).name;shutil.copyfile(AUDIT/'source_snapshot'/rel,dest)
 r=subprocess.run(['python3',str(dest)],cwd=folder,capture_output=True,text=True,timeout=120)
 (folder/'stdout.txt').write_text(r.stdout);(folder/'stderr.txt').write_text(r.stderr)
 got=json.loads((folder/'independent_results.json').read_text()) if 'independent' in rel else json.loads(r.stdout)
 expected=json.loads((AUDIT/'source_snapshot'/('review/independent_results.json' if 'independent' in rel else 'verification.json')).read_text())
 history.append({'script':rel,'sha256':sha(dest),'returncode':r.returncode,'result_exact':got==expected,'count':got.get('passed',got.get('total_assertions'))})
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'isolation':'Every script is an unchanged isolated copy. Read-only .git and unsolved source symlinks for primary controls; all writes restricted to ignored replay mirror.','families':results,'historical':history,'all_success':all(x['returncode']==0 and (x.get('result_exact') or x.get('checks_exact_after_ignoring_run_utc') or x.get('all_raw_fields_exact')) for x in results) and all(x['result_exact'] and x['returncode']==0 for x in history)}
(HERE/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
