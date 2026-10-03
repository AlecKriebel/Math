"""Read-only final own-family and exact current packet check before ROOT closes."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,os,stat
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];C=A/'reviewed_candidate';sha=lambda b:hashlib.sha256(b).hexdigest()
def parse(b):
 def unique(xs):
  o={}
  for k,v in xs:assert k not in o;o[k]=v
  return o
 def floating(s):f=float(s);assert math.isfinite(f);return f
 return json.loads(b,object_pairs_hook=unique,parse_float=floating,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def raw(p):assert p.is_file()and not p.is_symlink()and all(not q.is_symlink()for q in p.parents);return p.read_bytes()
def topology(root):
 fs=set();ds=set()
 for p in root.rglob('*'):
  assert not p.is_symlink();n=p.relative_to(root).as_posix();assert not set(PurePosixPath(n).parts)&{'.','..','.git','__pycache__'}
  if p.is_file():fs.add(n)
  else:assert stat.S_ISDIR(p.stat().st_mode);ds.add(n)
 assert ds=={q.as_posix()for n in fs for q in PurePosixPath(n).parents if str(q)!='.'};return fs,ds
assert not (F/'MANIFEST.json').exists();fs,ds=topology(F);own=[]
for n in sorted(fs):
 p=F/n;b=raw(p)
 if n.endswith('.json'):parse(b)
 own.append(dict(path=n,bytes=len(b),sha256=sha(b),full_mode_before_ROOT_closure=stat.S_IMODE(p.stat().st_mode)))
v=parse(raw(F/'VERDICT.json'));assert v['report_sha256']==sha(raw(F/'AUDIT.md'))and v['future_acceptance_approved']is False and v['mandatory_mathematical_corrections']==v['mandatory_source_or_packet_corrections']==[]
assert parse(raw(F/'FINAL_EVIDENCE_CONTROL_RESULT_V2.json'))['original_true_closing_capture']['pid']==87065
captures=[]
for cp in sorted(F.rglob('CAPTURE.json')):
 c=parse(raw(cp));assert c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and type(c['exit_code'])is int;assert c['stdin_supplied']is False
 pre=parse(raw(cp.parent/'PRELAUNCH.json'));assert pre['argv']==c['argv']and pre['cwd']==c['cwd']and pre['operator_pid']==c['operator_pid']
 for k in ['stdout','stderr']:
  r=c[k];b=raw(cp.parent/r['path']);assert len(b)==r['bytes']and sha(b)==r['sha256']
 if 'operator_sha256'in c:assert sha(raw(cp.parent/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']
 if c.get('source_sha256')is not None:assert sha(raw(cp.parent/'PRELAUNCH_SOURCE.py'))==c['source_sha256']
 captures.append(dict(path=str(cp.relative_to(F)),actual_pid=c['pid'],exit_code=c['exit_code']))
# This running capture has only prelaunch and streams. Its completion is not invented.
assert not (F/'captures/final_preclosure_v2/CAPTURE.json').exists();assert raw(F/'captures/final_preclosure_v2/PRELAUNCH_SOURCE.py')==raw(Path(__file__))
m=parse(raw(C/'MANIFEST.json'));assert sha(raw(C/'MANIFEST.json'))==v['candidate_manifest_sha256'];ns,dds=topology(C);assert len(m['files'])==1946 and ns=={r['path']for r in m['files']}|{'MANIFEST.json'}and len(dds)==365
for r in m['files']:
 p=C/r['path'];b=raw(p);assert len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE(p.stat().st_mode)==0o444
assert stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444
D=parse(raw(C/'CURRENT_DEPENDENCIES.json'));native4={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl']}|{'draft_pr_publication_program_20260930/inventory.json'};stable=[r for r in D['current_native13']if r['path']not in native4];assert len(stable)==9
for r in stable:
 p=R/r['path'];b=raw(p);assert len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
result=dict(status='PASS_FINAL_PRECLOSURE_OWN_COMPLETE_EVIDENCE_AND_CURRENT_PACKET',actual_pid=os.getpid(),UTC=dt.datetime.now(dt.timezone.utc).isoformat(),whole1946_payload_self365_topology_full0444=True,stable9_live=True,own_complete_files_before_this_result=len(own),own_relative_directories=len(ds),full_own_read_bindings=own,complete_previous_capture_outcomes=captures,current_running_capture_not_read_as_complete=True,current_running_capture_completion_will_be_written_only_by_outer_after_exit=True,report_sha256=v['report_sha256'],ROOT_closure_not_executed=True,future_acceptance_approved=False)
(F/'FINAL_PRECLOSURE_RESULT_V2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:x for k,x in result.items()if k not in {'full_own_read_bindings','complete_previous_capture_outcomes'}},indent=2))
