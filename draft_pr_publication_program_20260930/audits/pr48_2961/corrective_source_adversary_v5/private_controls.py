"""Independent handwritten filesystem predicates only; no candidate/operator run."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;R=Path('/Users/alec/Documents/Math');START=dt.datetime.now(dt.timezone.utc).isoformat();ROWS=[]
def need(v):
    if not v:raise ValueError('Independent private refusal')
def source(p,expected):
    need(type(expected) is int and p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected)
    b=p.read_bytes();return dict(path=p.relative_to(F).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=expected)
def directory(p,expected):
    need(type(expected) is int and p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected);return dict(path=p.relative_to(F).as_posix(),full_mode=expected)
def test(label,fn,want):
    try:got=fn()
    except (ValueError,TypeError,KeyError,FileNotFoundError):got=False
    need(got is want);ROWS.append(dict(label=label,expected_acceptance=want,observed_acceptance=got))
def main():
    os.umask(0o022);base=F/'private_fixtures';base.mkdir();selected=base/'selected_A48';other=base/'other_A45';selected.mkdir();other.mkdir();good=selected/'outer';bad=other/'outer';good.mkdir(mode=0o700);bad.mkdir(mode=0o700)
    body=(R/'draft_pr_publication_program_20260930/audits/pr45_9900007/capture_root_command.py').read_bytes();digest=hashlib.sha256(body).hexdigest();need(len(body)==2593 and digest=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec')
    live=selected/'capture_root_command.py';actual_other=other/'capture_root_command.py';snap=good/'prelaunch_operator.py'
    for p in [live,actual_other,snap,bad/'prelaunch_operator.py']:p.write_bytes(body);p.chmod(0o644)
    def context(outer):
        need(outer.is_absolute() and outer.parent==selected and outer.is_dir() and not outer.is_symlink() and all(not q.is_symlink() for q in outer.parents) and outer.resolve(strict=True)==outer and selected.resolve(strict=True)==selected)
        parent=directory(selected,0o755);s=source(outer/'prelaunch_operator.py',0o644);z=source(live,0o644);need(z['sha256']==digest and live.read_bytes()==(outer/'prelaunch_operator.py').read_bytes())
        return dict(live=z,parent=parent,snapshot=s,outer=directory(outer,0o700))
    for role in ['author','caller','inspector']:
        test(role+' exact same canonical parent/source/snapshot modes accepts',lambda:bool(context(good)),True)
        test(role+' other parent with healthy identical source rejects',lambda:bool(context(bad)),False)
    for mode in [0o600,0o2644,0o4644]:
        actual_other.chmod(mode);test('M4 other-parent actual source mode '+oct(mode)+' rejected by identity',lambda:bool(context(bad)),False)
    actual_other.chmod(0o644)
    for mode in [0o600,0o2644,0o4644]:
        live.chmod(mode);test('M3 same-parent live full mode '+oct(mode)+' rejects',lambda:bool(context(good)),False)
    live.chmod(0o644)
    for p,mode,restored,label in [(selected,0o2755,0o755,'actual parent special bits'),(good,0o2700,0o700,'outer special bits')]:
        p.chmod(mode);test(label+' rejected',lambda:bool(context(good)),False);p.chmod(restored)
    snap.write_bytes(body+b'changed');test('complete snapshot substitution rejects',lambda:bool(context(good)),False);snap.write_bytes(body);snap.chmod(0o644)
    test('lexical traversal refuses',lambda:bool(context(selected/'..'/'selected_A48'/'outer')),False)
    alias=selected/'linked_outer';alias.symlink_to(good,target_is_directory=True);test('symlink outer refuses',lambda:bool(context(alias)),False);alias.unlink()
    for expected in [True,420.0]:test('typed mode '+repr(expected)+' refuses',lambda v=expected:bool(source(live,v)),False)
    before=context(good);live.chmod(0o2644);test('after-boundary chmod drift refuses',lambda:context(good)==before,False);live.chmod(0o644);test('restored whole context accepts',lambda:context(good)==before,True)
    for p in [live,actual_other,snap,bad/'prelaunch_operator.py']:need(p.read_bytes()==body and stat.S_IMODE(p.stat().st_mode)==0o644)
    good.chmod(0o755);bad.chmod(0o755)
    print(json.dumps(dict(schema='pr48-v5-independent-actual-parent-live-mode-controls/v1',status='PASS_PRIVATE_MODELS_ONLY',actual_private_pid=os.getpid(),started_utc=START,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=len(ROWS),controls=ROWS,private_sources_restored0644=True,private_directories_restored0755=True,private_symlink_removed=True,candidate_or_ROOT_operator_imported_compiled_executed=False,actual_ROOT_operator_copy_native_Git_remote_mutation=False),indent=2))
if __name__=='__main__':main()
