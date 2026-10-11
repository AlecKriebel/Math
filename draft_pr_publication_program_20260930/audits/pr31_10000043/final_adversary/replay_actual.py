#!/usr/bin/env python3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import shutil,subprocess,sys,json,hashlib,datetime
HERE=Path(__file__).resolve().parent;A=HERE.parent;REPO=A.parents[2]
S=HERE/'sandbox'/'repo';T=S/'draft_pr_publication_program_20260930'/'audits'/'pr31_10000043'
T.mkdir(parents=True,exist_ok=True)
(S/'.git').symlink_to(REPO/'.git',target_is_directory=True)
(S/'unsolved_math_prioritization').symlink_to(REPO/'unsolved_math_prioritization',target_is_directory=True)
for n in ['source_snapshot','pr_input','coupling_family','infinite_volume_family','primary_scope_family','reviewed_candidate']:
 shutil.copytree(A/n,T/n,ignore=shutil.ignore_patterns('tmp','__pycache__','isolated_original'),dirs_exist_ok=True)
for n in ['snapshot_manifest.json','pr_input.json']:shutil.copy2(A/n,T/n)
(T/'primary_scope_family'/'sources').mkdir(exist_ok=True)
# Foreign source PDFs used only as inputs; actual fetch code retrieves its own copies next.
items=[]
def run(label,folder,script):
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 q=subprocess.run([sys.executable,script],cwd=folder,capture_output=True,text=True,timeout=500)
 (HERE/(label+'.stdout')).write_text(q.stdout);(HERE/(label+'.stderr')).write_text(q.stderr)
 item={'label':label,'script':str(Path(folder)/script),'script_sha256':hashlib.sha256((Path(folder)/script).read_bytes()).hexdigest(),'utc':started,'returncode':q.returncode,'stdout_file':label+'.stdout','stderr_file':label+'.stderr'}
 items.append(item);print(json.dumps(item),flush=True);return q.returncode
# Verifiers are executed before the replay creates extra output/caches.
for label,folder,script in [('volume_manifest',T/'infinite_volume_family','verify_family_manifest.py'),('primary_manifest',T/'primary_scope_family','verify_manifest.py')]:assert run(label,folder,script)==0
# Independent runs write to separate private directories.
jobs=[('original_author',T/'reviewed_candidate','check_coupling.py'),('original_review',T/'reviewed_candidate','review/independent_checks.py'),('coupling_current',T/'coupling_family','independent_adaptive_controls.py'),('coupling_archived_v1',T/'coupling_family'/'control_runs'/'v1','independent_adaptive_controls.py'),('volume_controls',T/'infinite_volume_family','infinite_volume_controls.py'),('coupling_replay_original',T/'coupling_family','replay_original.py'),('primary_fresh_fetch',T/'primary_scope_family','fresh_fetch.py')]
with ThreadPoolExecutor(max_workers=7) as pool:
 for status in pool.map(lambda j:run(*j),jobs):assert status==0
assert run('primary_control_audit',T/'primary_scope_family','control_audit.py')==0
# Compare byte-exact deterministic results; normalize ONLY telemetry fields for generated audit receipts.
comparisons=[]
for rel,ignore in [('reviewed_candidate/check_results.json',[]),('reviewed_candidate/review/independent_results.json',[]),('coupling_family/INDEPENDENT_CONTROLS_RECEIPT.json',['started_utc','finished_utc','python']),('coupling_family/control_runs/v1/INDEPENDENT_CONTROLS_RECEIPT.json',['started_utc','finished_utc','python']),('infinite_volume_family/infinite_volume_controls_results.json',['utc']),('infinite_volume_family/negative_controls.json',[]),('primary_scope_family/CONTROL_RESULTS.json',['at_utc'])]:
 old=json.loads((A/rel).read_text());new=json.loads((T/rel).read_text())
 if isinstance(old,dict):
  for k in ignore:old.pop(k,None);new.pop(k,None)
 identical=old==new
 comparisons.append({'path':rel,'content_equal_except_explicit_telemetry':identical,'excluded_telemetry':ignore})
 assert identical,rel
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'actual_unmodified_program_runs':items,'result_comparisons':comparisons,'limitations':'All original/family programs run unchanged only in isolated copies. Downloads/readonly Git/SQLite do not prove historical telemetry or mathematical truth. Cached stale generated results are accepted only after returncode0 and comparison.'}
(HERE/'ACTUAL_CODE_RECEIPTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
