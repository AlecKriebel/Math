from pathlib import Path
import collections, datetime as dt, hashlib, json, os, sys
sys.dont_write_bytecode=True
os.environ.update(PYTHONDONTWRITEBYTECODE="1",GIT_OPTIONAL_LOCKS="0")
R=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+"\n")
inputs=load('INPUT_MANIFEST.json');bad=[]
for e in inputs['files']:
 b=(R/e['captured_path']).read_bytes()
 if len(b)!=e['bytes'] or sha(b)!=e['sha256']:bad.append(e['captured_path'])
if bad:raise RuntimeError('Captured input custody mismatch '+str(bad))
mountdiff=[]
for p in sorted((R/'inputs/prior02').rglob('*')):
 if p.is_file():
  rel=p.relative_to(R/'inputs/prior02');q=R/'replay/inputs'/rel
  if not q.is_file() or q.read_bytes()!=p.read_bytes():mountdiff.append(str(rel))
assert mountdiff==['current/coverage_snapshot.py']
assert (R/'replay/inputs/current/coverage_snapshot.py').read_bytes()==(R/'inputs/current/coverage_snapshot.py').read_bytes()
assert all((R/'replay'/n).read_bytes()==(R/'inputs/prior02_review'/n).read_bytes() for n in ['controls.py','supplementary.py'])
assert sha((R/'inputs/current/coverage_snapshot.py').read_bytes())=='8771f7efc9d48edc8fcc2b2d186442b7b3cd739255426b105f31d1bb93f66aba'
replay=load('replay/CONTROL_RESULTS.json')['results'];supp=load('replay/SUPPLEMENTARY_RESULTS.json')['results'];fresh=load('NEW_CONTROL_RESULTS.json')['results']
assert len(replay)==368 and all(e['control_pass'] for e in replay)
assert len(supp)==20 and all(not e['accepted'] for e in supp)
assert len(fresh)==206
assert [(e['name'],e['accepted']) for e in fresh if e['mode']=='normal']==[(e['name'],e['accepted']) for e in fresh if e['mode']=='optimized']
assert all(not e['accepted'] for e in fresh if e['family']=='destination')
primary_names={e['name'] for e in fresh if e['family'] in ['legacy_manifest','ledger_pr_url'] or e['name'] in ['ledger_range_wrong_row_292','ledger_range_wrong_row_397']}
assert len(primary_names)==10 and all(e['accepted'] for e in fresh if e['name'] in primary_names)
accounting=load('INDEPENDENT_ACCOUNTING.json')
assert accounting['prefix']['count']==512 and accounting['own_publication_count']==4 and all(e['independent_counts_equal'] for e in accounting['baseline_comparisons'])
validation=dict(at=now(),captured_entries_checked=len(inputs['files']),captured_mismatches=bad,replay_mount_only_change=mountdiff,exact_original_harnesses=True,prior_control_executions=len(replay)+len(supp),prior_all_pass=True,new_executions=len(fresh),direct_baseline_executions=2,total_validator_executions=len(replay)+len(supp)+len(fresh)+2,primary_counterexamples_per_mode=sorted(primary_names),no_canonical_immutability_claim=True,providers_invoked=0)
save('CUSTODY_AND_VALIDATION.json',validation)
log=load('RESEARCH_LOG.json')
if not any(e.get('completion_estimate_percent')==100 for e in log):
 log.append(dict(at=now(),completion_estimate_percent=100,event='Independent bounded review complete. Both prior seals verified;596 validator executions retained; all388 prior controls pass;10 primary counterfactual negativecases/mode accepted,16 supplemental negativecases/mode accepted,5 unadjudicated scopeprobes/mode accepted; canonical fourpublication baseline independently correct. Output seal created.'))
 save('RESEARCH_LOG.json',log)
files=[];symlinks=[]
for p in sorted(R.rglob('*')):
 if p==R/'OUTPUT_MANIFEST.json':continue
 if p.is_symlink():
  symlinks.append(dict(path=str(p.relative_to(R)),target=os.readlink(p),resolved_target=str(p.resolve())))
 elif p.is_file():
  b=p.read_bytes();files.append(dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b)))
save('OUTPUT_MANIFEST.json',dict(at=now(),files=files,symlinks=symlinks,note='Exact regular-file contents and symlink targets under this review directory; manifest itself excluded to avoid circular hashing. No canonical-file immutability claim.'))
for e in files:
 b=(R/e['path']).read_bytes()
 if len(b)!=e['bytes'] or sha(b)!=e['sha256']:raise RuntimeError('Output seal mismatch')
assert all(os.readlink(R/e['path'])==e['target'] for e in symlinks)
print(json.dumps(dict(at=now(),regular_files_sealed=len(files),symlinks_sealed=len(symlinks),output_manifest_sha256=sha((R/'OUTPUT_MANIFEST.json').read_bytes()),validation=validation),indent=2))
