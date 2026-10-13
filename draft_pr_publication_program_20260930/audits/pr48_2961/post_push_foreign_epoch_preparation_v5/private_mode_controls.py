"""Handwritten same/other-parent controls; no proposed source or operator execution."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
P=Path(__file__).absolute().parent;R=P.parents[3];START=dt.datetime.now(dt.timezone.utc).isoformat();ROWS=[]
def need(v):
 if not v:raise ValueError('Private model refusal')
def source(q):
 need(q.is_file() and not q.is_symlink() and all(not p.is_symlink() for p in q.parents) and stat.S_IMODE(q.stat().st_mode)==0o644);b=q.read_bytes();return dict(path=q.relative_to(P).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=0o644)
def directory(q,expected):need(q.is_dir() and not q.is_symlink() and all(not p.is_symlink() for p in q.parents) and stat.S_IMODE(q.stat().st_mode)==expected);return dict(path=q.relative_to(P).as_posix(),full_mode=expected)
def test(label,fn,want):
 try:got=fn()
 except (ValueError,TypeError,KeyError):got=False
 need(got is want);ROWS.append(dict(label=label,expected_acceptance=want,observed_acceptance=got))
def main():
 os.umask(0o022);base=P/'private_mode_fixtures';base.mkdir();selected=base/'selected_A48';other=base/'other_A45';selected.mkdir();other.mkdir();good=selected/'outer';bad=other/'outer';good.mkdir(mode=0o700);bad.mkdir(mode=0o700)
 body=(R/'draft_pr_publication_program_20260930/audits/pr45_9900007/capture_root_command.py').read_bytes();need(len(body)==2593 and hashlib.sha256(body).hexdigest()=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec')
 live=selected/'capture_root_command.py';actual_other=other/'capture_root_command.py'
 for q in [live,actual_other,good/'prelaunch_operator.py',bad/'prelaunch_operator.py']:q.write_bytes(body);q.chmod(0o644)
 def old_context(outer):
  z=source(live);snapshot=source(outer/'prelaunch_operator.py');need(live.read_bytes()==body==(outer/'prelaunch_operator.py').read_bytes());return dict(live=z,parent=directory(selected,0o755),snapshot=snapshot,outer=directory(outer,0o700))
 def repaired(outer):
  need(outer.is_absolute() and outer.parent==selected and outer.is_dir() and not outer.is_symlink() and all(not q.is_symlink() for q in outer.parents) and outer.resolve(strict=True)==outer and selected.resolve(strict=True)==selected);return old_context(outer)
 test('same canonical selected parent positive',lambda:bool(repaired(good)),True);test('other parent even with healthy operator negative',lambda:bool(repaired(bad)),False);before=old_context(bad)
 for mode in [0o600,0o2644,0o4644]:
  actual_other.chmod(mode);test('other actual live chmod '+oct(mode)+' omitted by old selected context',lambda:old_context(bad)==before,True);test('V5 exact parent refuses actual other live '+oct(mode),lambda:bool(repaired(bad)),False)
 actual_other.chmod(0o644)
 for mode in [0o600,0o2644,0o4644]:
  live.chmod(mode);test('same parent still rejects live mode '+oct(mode),lambda:bool(repaired(good)),False)
 live.chmod(0o644);snapshot=good/'prelaunch_operator.py';snapshot.write_bytes(body+b'changed');test('same parent snapshot substitution negative',lambda:bool(repaired(good)),False);snapshot.write_bytes(body);snapshot.chmod(0o644)
 selected.chmod(0o700);test('same parent0755 remains strict',lambda:bool(repaired(good)),False);selected.chmod(0o755);good.chmod(0o755);test('same-parent outer0700 remains strict',lambda:bool(repaired(good)),False);good.chmod(0o700)
 traversal=selected/'..'/'selected_A48'/'outer';test('lexical traversal to otherwise correct parent negative',lambda:bool(repaired(traversal)),False)
 alias=selected/'linked_outer';alias.symlink_to(good,target_is_directory=True);test('same-parent symlink outer negative',lambda:bool(repaired(alias)),False);alias.unlink()
 test('restored positive',lambda:bool(repaired(good)),True)
 for q in [live,actual_other,good/'prelaunch_operator.py',bad/'prelaunch_operator.py']:need(q.read_bytes()==body and stat.S_IMODE(q.stat().st_mode)==0o644)
 good.chmod(0o755);bad.chmod(0o755)
 result=dict(schema='pr48-first-party-private-actual-parent-controls/v5',status='PASS_PRIVATE_MODELS_ONLY',actual_private_control_pid=os.getpid(),started_utc=START,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),assertions=len(ROWS),controls=ROWS,all_private_source_bodies_restored_c1ae=True,private_sources_restored0644=True,private_directories_restored0755=True,private_symlink_removed_after_negative=True,candidate_or_ROOT_operator_imported_compiled_executed=False,actual_ROOT_operator_copy_or_capture_modified=False)
 with (P/'PRIVATE_MODE_CONTROL_RESULTS.json').open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
 print(json.dumps(dict(status=result['status'],actual_private_control_pid=result['actual_private_control_pid'],assertions=len(ROWS),candidate_executed=False)))
if __name__=='__main__':main()
