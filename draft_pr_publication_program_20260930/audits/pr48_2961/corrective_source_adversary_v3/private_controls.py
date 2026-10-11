"""Independent private specification models. Candidate/ROOT code is never imported or run."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;R=F.parents[3];START=dt.datetime.now(dt.timezone.utc).isoformat();RESULTS=[]
def need(v):
 if not v:raise ValueError('Independent typed custody predicate refuses')
def sha(b):return hashlib.sha256(b).hexdigest()
def directory(p,expected):
 need(type(expected) is int and expected in (0o700,0o755) and p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents));need(stat.S_IMODE(p.stat().st_mode)==expected);return dict(path=p.name,full_mode=expected)
def source(p,expected):
 need(type(expected) is int and p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected);b=p.read_bytes();return dict(path=p.name,bytes=len(b),sha256=sha(b),full_mode=expected)
def test(label,fn,wanted):
 try:got=fn()
 except (ValueError,TypeError,KeyError):got=False
 need(got is wanted);RESULTS.append(dict(label=label,expected_acceptance=wanted,observed_acceptance=got))
base=F/'private_fixtures';base.mkdir(exist_ok=False);base.chmod(0o755);outer=base/'outer';outer.mkdir(mode=0o700);runtime=base/'runtime';runtime.mkdir(mode=0o755);(runtime/'MARKER.txt').write_bytes(b'own runtime directory remains0755\n')
original=R/'draft_pr_publication_program_20260930/audits/pr45_9900007/capture_root_command.py';body=original.read_bytes();need(sha(body)=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec')
live=base/'capture_root_command.py';snapshot=outer/'prelaunch_operator.py';live.write_bytes(body);snapshot.write_bytes(body);live.chmod(0o644);snapshot.chmod(0o644)
genuine=original.parent/'root_pr57_priority_source_closure_actual_capture';need(stat.S_IMODE(genuine.stat().st_mode)==0o700)
test('actual genuine c1ae ROOT directory0700 accepted read-only',lambda:directory(genuine,0o700)['full_mode']==0o700,True)
test('actual genuine c1ae ROOT directory0700 rejected by old755 premise',lambda:directory(genuine,0o755)['full_mode']==0o755,False)
ROLES=['verified operator binding','epoch author outer','phase caller outer','complete inspector outer']
for role in ROLES:
 outer.chmod(0o700);test(role+' private0700 accepted',lambda:directory(outer,0o700)['full_mode']==0o700,True)
 for mode in [0o755,0o1700,0o2700,0o4700,0o7700]:
  outer.chmod(mode);test(role+' private chmod '+oct(mode)+' rejected',lambda:directory(outer,0o700)['full_mode']==0o700,False)
outer.chmod(0o700)
test('own runtime755 accepted',lambda:directory(runtime,0o755)['full_mode']==0o755,True)
for mode in [0o700,0o1755,0o2755,0o4755,0o7755]:
 runtime.chmod(mode);test('own runtime chmod '+oct(mode)+' rejected',lambda:directory(runtime,0o755)['full_mode']==0o755,False)
runtime.chmod(0o755)
for value in [True,False,448.0,493.0,None,'0700',0o1700]:test('typed expected '+repr(value)+' rejected',lambda v=value:directory(outer,v)['full_mode']==v,False)
def v3_observation():
 # The V3 outer boundary contains only the retained prelaunch operator and directory.
 return dict(outer_operator=source(snapshot,0o644),directories=[directory(outer,0o700)],runtime_directory=directory(base,0o755))
before=v3_observation();counterexamples=[]
for mode in [0o600,0o2644,0o4644]:
 live.chmod(mode);after=v3_observation();same=after==before and live.read_bytes()==body and snapshot.read_bytes()==body
 test('M3 live chmod '+oct(mode)+' leaves V3 snapshot context identical',lambda s=same:s,True)
 test('M3 live chmod '+oct(mode)+' rejected by required actual-live source0644',lambda:source(live,0o644)['full_mode']==0o644,False)
 test('M3 live chmod '+oct(mode)+' leaves c1ae body-only operator_unchanged true',lambda:live.read_bytes()==body,True)
 counterexamples.append(dict(live_full_mode=stat.S_IMODE(live.stat().st_mode),snapshot_full_mode=stat.S_IMODE(snapshot.stat().st_mode),outer_full_mode=stat.S_IMODE(outer.stat().st_mode),live_complete_body_sha256=sha(live.read_bytes()),snapshot_complete_body_sha256=sha(snapshot.read_bytes()),V3_mode_context_unchanged=same,required_live0644_predicate_accepts=False,c1ae_body_only_unchanged_predicate_accepts=True))
live.chmod(0o644);test('required live0644 source restored accepted',lambda:source(live,0o644)['full_mode']==0o644,True)
need(body==live.read_bytes()==snapshot.read_bytes());outer.chmod(0o755)
print(json.dumps(dict(schema='pr48-v3-independent-private-directory-and-live-operator-controls/v1',status='PASS_CONTROLS_WITH_M3_COUNTEREXAMPLES',actual_private_pid=os.getpid(),started_utc=START,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=len(RESULTS),controls=RESULTS,M3_actual_private_chmod_counterexamples=counterexamples,original_or_actual_ROOT_capture_modes_changed=False,production_or_candidate_or_ROOT_operator_import_compile_execution=False,private_fixture_dirs_restored0755=True),indent=2))
