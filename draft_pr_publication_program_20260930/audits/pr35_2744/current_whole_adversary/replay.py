"""Fresh complete read-only input audit and unchanged private executable replays."""
from pathlib import Path
import json,hashlib,datetime,shutil,subprocess,os,re,argparse
HERE=Path(__file__).resolve().parent
P=argparse.ArgumentParser();P.add_argument('--audit');P.add_argument('--repo');P.add_argument('--output-dir');P.add_argument('--work');ARG=P.parse_args()
AUDIT=Path(ARG.audit).resolve() if ARG.audit else HERE.parent;REPO=Path(ARG.repo).resolve() if ARG.repo else AUDIT.parents[2]
OUT=Path(ARG.output_dir).resolve() if ARG.output_dir else HERE;OUT.mkdir(parents=True,exist_ok=True)
WORK=Path(ARG.work).resolve() if ARG.work else OUT/'tmp/replay_repo';A=WORK/'draft_pr_publication_program_20260930/audits/pr35_2744';RC=A/'reviewed_candidate';RECEIPTS=OUT/'receipts';RECEIPTS.mkdir(exist_ok=True)
ENV={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
WANT='65e7ac9d28b8504346d68c771256c2f4642c374d07bbce06bdaecfe85b8f644a'
def binding():
 c=AUDIT/'reviewed_candidate';m=load(c/'MANIFEST.json');d=load(c/'CURRENT_PROOF_DEPENDENCIES.json')
 assert sha((c/'MANIFEST.json').read_bytes())==WANT
 assert len(m['files'])==42 and len(d['files'])==115
 assert d['base']=='../' and d['dependency_anchor_repository_relative']==str(AUDIT.relative_to(REPO))
 allrows=[(c,f) for f in m['files']]+[(AUDIT,f) for f in d['files']]
 result=[]
 for base,f in allrows:
  p=base/f['path'];b=p.read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],str(p)
  if p.suffix=='.json':load(p)
  if p.suffix=='.jsonl':
   for line in b.splitlines():json.loads(line)
  result.append({'path':str(p.relative_to(REPO)),'bytes':len(b),'sha256':sha(b)})
 return result
before=binding();A.mkdir(parents=True,exist_ok=True)
for name in ('source_snapshot','pr_input','reviewed_candidate'):
 shutil.copytree(AUDIT/name,A/name,dirs_exist_ok=True)
shutil.copyfile(AUDIT/'snapshot_manifest.json',A/'snapshot_manifest.json')
for family,sources in [('algebraic_family','sources'),('cone_family','primary_sources'),('primary_scope_family','tmp/sources')]:
 src=AUDIT/family;dst=A/family;dst.mkdir(exist_ok=True)
 for row in load(src/'MANIFEST.json')['files']:
  p=dst/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/row['path'],p)
 shutil.copyfile(src/'MANIFEST.json',dst/'MANIFEST.json')
 shutil.copytree(src/sources,dst/sources,dirs_exist_ok=True)
(A/'cone_family/private_replay').mkdir(exist_ok=True)
if not (WORK/'.git').exists():(WORK/'.git').symlink_to(REPO/'.git',target_is_directory=True)
def normalize(v):
 if isinstance(v,dict):return {k:normalize(w) for k,w in v.items() if k!='utc'}
 if isinstance(v,list):return [normalize(w) for w in v]
 if isinstance(v,str):
  v=v.replace(str(A),'<audit>').replace(str(AUDIT),'<audit>')
  v=re.sub(r'/private_replay/(?:cone_actual_|boundary_mutants_)[^/\s"]+','/private_replay/<unique_run>',v)
  return v
 return v
runs=[]
def run(name,cmd,result=None,expected=None):
 p=subprocess.run(list(map(str,cmd)),cwd=WORK,capture_output=True,env=ENV,timeout=180)
 (RECEIPTS/(name+'.stdout')).write_bytes(p.stdout);(RECEIPTS/(name+'.stderr')).write_bytes(p.stderr)
 r={'name':name,'command':list(map(str,cmd)),'implementation_sha256':sha(Path(cmd[1]).read_bytes()),'exit':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
 runs.append(r)
 assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr)
 r['stdout_full_json']=json.loads(p.stdout)
 if result is not None:
  b=result.read_bytes();e=expected.read_bytes();v=load(result);w=load(expected)
  r.update(actual_result_sha256=sha(b),expected_result_sha256=sha(e),byte_exact=b==e)
  r['full_json_equal_except_utc_and_private_path']=normalize(v)==normalize(w)
  (RECEIPTS/(name+'.result.json')).write_bytes(b)
  assert r['byte_exact'] or r['full_json_equal_except_utc_and_private_path'],name
PY='/usr/bin/python3';a=A/'algebraic_family';c=A/'cone_family';p=A/'primary_scope_family'
try:
 run('algebraic_closure',[PY,a/'check_closure.py','--family',a])
 run('cone_closure',[PY,c/'verify_manifest.py'])
 run('algebraic_108',[PY,a/'algebraic_controls.py','--repo',REPO,'--snapshot',A/'source_snapshot','--metadata',A/'snapshot_manifest.json','--sources',a/'sources','--source-bindings',a/'SOURCE_BINDINGS.json','--output',a/'RESULTS.json','--scratch',a/'private/current_whole_replay'],a/'RESULTS.json',AUDIT/'algebraic_family/RESULTS.json')
 run('algebraic_component_boundary_16',[PY,a/'component_boundary_controls.py','--output',a/'COMPONENT_BOUNDARY_RESULTS.json'],a/'COMPONENT_BOUNDARY_RESULTS.json',AUDIT/'algebraic_family/COMPONENT_BOUNDARY_RESULTS.json')
 run('cone_geometry_28',[PY,c/'geometric_controls.py'],c/'geometric_results.json',AUDIT/'cone_family/geometric_results.json')
 run('cone_boundary_21',[PY,c/'boundary_controls.py'],c/'boundary_results.json',AUDIT/'cone_family/boundary_results.json')
 run('cone_reproduce_originals_8_mutants',[PY,c/'reproduce.py'],c/'REPRODUCTION_RESULTS.json',AUDIT/'cone_family/REPRODUCTION_RESULTS.json')
 run('cone_4_boundary_mutants',[PY,c/'run_boundary_mutations.py'],c/'BOUNDARY_MUTATION_RESULTS.json',AUDIT/'cone_family/BOUNDARY_MUTATION_RESULTS.json')
 run('primary_111',[PY,p/'source_priority_controls.py','--repo',REPO],p/'RESULTS.json',AUDIT/'primary_scope_family/RESULTS.json')
 # Explicit direct replay of every original operative program and current copied executable.
 for label,folder in [('original',A/'source_snapshot'),('current',RC)]:
  for index,(code,output,want) in enumerate([('check_controls.py','check_results.json','check_results.json'),('independent_review/submitted_check_controls.py','independent_review/check_results.json','independent_review/submitted_results.json'),('independent_review/independent_checks.py','independent_review/independent_results.json','independent_review/independent_results.json')]):
   run(label+'_program_'+str(index),[PY,folder/code],folder/output,AUDIT/('source_snapshot' if label=='original' else 'reviewed_candidate')/want)
 after=binding();assert before==after
 output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_manifest_sha256':WANT,'candidate_members':42,'dependency_members':115,'before_bindings':before,'after_bindings':after,'unchanged':before==after,'runs':runs,'outer_runs':9,'explicit_original_runs':3,'explicit_current_runs':3,'actual_frozen_family_mutants_rejected':24,'new_substantive_attempts':0,'status':'PASS'}
except Exception as e:
 output={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FAILED','error':repr(e),'runs':runs,'before_bindings':before,'after_bindings':binding()}
 (OUT/'REPLAY_FAILURE.json').write_text(json.dumps(output,indent=2)+'\n');raise
finally:
 (OUT/'REPLAY_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'status':output['status'],'outer_runs':9,'explicit_original_runs':3,'explicit_current_runs':3,'total_program_runs':len(runs),'full_results_and_receipts_saved':True}))
