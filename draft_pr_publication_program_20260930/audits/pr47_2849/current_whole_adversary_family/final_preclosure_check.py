"""Read-only check before READY; excludes only this own still-running capture."""
from pathlib import Path, PurePosixPath
import datetime as dt,hashlib,json,os,stat,sys
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2]
assert __debug__ and not sys.flags.optimize
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_bytes())
def stream(root,row):
 b=(root/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'];return b
verdict=obj(F/'VERDICT.json');assert sha((F/'AUDIT.md').read_bytes())==verdict['report_sha256']
assert verdict['mandatory_corrections']==[] and verdict['future_acceptance_approved'] is False and verdict['status']=='unsolved'
assert sha((A/'reviewed_candidate/MANIFEST.json').read_bytes())==verdict['candidate_manifest_sha256']
assert not (F/'MANIFEST.json').exists()
fs=set();ds=set()
for p in F.rglob('*'):
 assert not p.is_symlink();n=p.relative_to(F).as_posix()
 assert not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts)
 if stat.S_ISREG(p.stat().st_mode):fs.add(n);p.read_bytes()
 else:assert stat.S_ISDIR(p.stat().st_mode);ds.add(n)
assert ds=={str(q) for n in fs for q in PurePosixPath(n).parents if str(q)!='.'}
records=[]
for d in sorted((F/'captures').iterdir()):
 if d.name=='final_preclosure':assert not (d/'CAPTURE.json').exists();continue
 c=obj(d/'CAPTURE.json');assert c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int
 assert c['source_unchanged_after_child'] is True and c['operator_unchanged_after_child'] is True
 assert sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256']
 stream(d,c['stdout']);stream(d,c['stderr']);records.append({'directory':d.name,'entire_capture':c})
assert len(records)==9 and sum(c['entire_capture']['exit_code']!=0 for c in records)==4
for root in [F/'private_git',F/'private_literal_replay',F/'private_literal_replay_v2',F/'private_literal_replay_v3']:
 for d in root.iterdir():
  c=obj(d/'CAPTURE.json');assert c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0
  assert stream(F,c['stderr'])==b'';stream(F,c['stdout'])
stable=['unsolved_math_prioritization/'+n for n in ['catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]
fresh=obj(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')
for row in fresh['files']:
 if row['path'] in stable:
  stream(R,row);assert stat.S_IMODE((R/row['path']).stat().st_mode)==row['full_mode']
result={'schema':'pr47-whole-independent-final-preclosure-check/v1','pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','complete_prior_own_captures':records,'failed_own_inspections_preserved':4,'stable9_match':True,'report_sha256':verdict['report_sha256'],'sole_future_self_manifest_absent':True,'currently_running_own_outer_completion_claimed':False,'future_acceptance_approved':False}
(F/'FINAL_PRECLOSURE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','pid','failed_own_inspections_preserved','report_sha256','future_acceptance_approved']}))
