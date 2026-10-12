"""Handwritten models only; neither candidate nor c1ae operator is executed."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent
R=Path('/Users/alec/Documents/Math')
START=dt.datetime.now(dt.timezone.utc).isoformat()
ROWS=[]
def need(v):
    if not v:raise ValueError('Private specification refusal')
def source(p,expected):
    need(type(expected) is int and p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected)
    b=p.read_bytes();return dict(path=p.relative_to(F).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=expected)
def directory(p,expected):
    need(type(expected) is int and p.is_dir() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_IMODE(p.stat().st_mode)==expected);return dict(path=p.relative_to(F).as_posix(),full_mode=expected)
def test(label,fn,want):
    try:got=fn()
    except (ValueError,TypeError,KeyError):got=False
    need(got is want);ROWS.append(dict(label=label,expected_acceptance=want,observed_acceptance=got))
def main():
    os.umask(0o022);base=F/'private_fixtures';base.mkdir();selected=base/'selected_A48';selected.mkdir();other=base/'other_A45';other.mkdir();outer=other/'actual_outer';outer.mkdir(mode=0o700)
    body=(R/'draft_pr_publication_program_20260930/audits/pr45_9900007/capture_root_command.py').read_bytes();sha=hashlib.sha256(body).hexdigest();need(len(body)==2593 and sha=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec')
    live=selected/'capture_root_command.py';actual=other/'capture_root_command.py';snapshot=outer/'prelaunch_operator.py'
    for p in [live,actual,snapshot]:p.write_bytes(body);p.chmod(0o644)
    def v4_context():
        # V4's literal selected A48 descriptor and arbitrary input outer snapshot.
        z=source(live,0o644);s=source(snapshot,0o644);need(z['sha256']==sha and live.read_bytes()==snapshot.read_bytes())
        return dict(actual_live_ROOT_operator=dict(source=z,parent=directory(selected,0o755)),outer_operator=s,outer_directory=directory(outer,0o700))
    def required_actual_identity():
        need(outer.parent==selected);return v4_context()
    before=v4_context();test('typed selected literal live644 c1ae body=snapshot descriptor accepts',lambda:bool(v4_context()),True)
    for mode in [0o600,0o2644,0o4644]:
        live.chmod(mode);test('M3 selected live mode '+oct(mode)+' is now rejected',lambda:bool(v4_context()),False)
    live.chmod(0o644)
    for mode in [0o700,0o2755]:
        selected.chmod(mode);test('selected actual-live parent '+oct(mode)+' rejected',lambda:bool(v4_context()),False)
    selected.chmod(0o755)
    for mode in [0o755,0o2700]:
        outer.chmod(mode);test('genuine outer700 role rejects '+oct(mode),lambda:bool(v4_context()),False)
    outer.chmod(0o700)
    for value in [True,420.0,None,'0644']:
        test('typed source expected '+repr(value)+' rejected',lambda v=value:bool(source(live,v)),False)
    snapshot.write_bytes(body+b'changed');test('entire snapshot substitution rejected',lambda:bool(v4_context()),False);snapshot.write_bytes(body);snapshot.chmod(0o644)
    counter=[]
    for mode in [0o600,0o2644,0o4644]:
        actual.chmod(mode)
        test('M4 actual other-parent live chmod '+oct(mode)+' leaves entire V4 selected context unchanged',lambda:v4_context()==before,True)
        test('M4 actual other-parent source '+oct(mode)+' fails required actual644',lambda:bool(source(actual,0o644)),False)
        test('M4 concrete same-parent identity requirement refuses other-parent outer',lambda:bool(required_actual_identity()),False)
        counter.append(dict(actual_operator_path=actual.relative_to(F).as_posix(),selected_operator_path=live.relative_to(F).as_posix(),outer_directory=outer.relative_to(F).as_posix(),actual_operator_full_mode=stat.S_IMODE(actual.stat().st_mode),selected_operator_full_mode=stat.S_IMODE(live.stat().st_mode),snapshot_full_mode=stat.S_IMODE(snapshot.stat().st_mode),V4_context_unchanged=v4_context()==before,whole_actual_selected_snapshot_body_sha256=sha,actual_outer_parent_equals_selected_operator_parent=False))
    actual.chmod(0o644);outer.chmod(0o755)
    need(all(p.read_bytes()==body and stat.S_IMODE(p.stat().st_mode)==0o644 for p in [live,actual,snapshot]))
    result=dict(schema='pr48-v4-independent-selected-live-and-actual-outer-identity-controls/v1',status='PASS_PRIVATE_CONTROLS_WITH_OTHER_PARENT_COUNTEREXAMPLES',actual_private_pid=os.getpid(),started_utc=START,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),checks=len(ROWS),controls=ROWS,other_parent_counterexamples=counter,candidate_or_ROOT_operator_imported_compiled_executed=False,actual_native_Git_remote_ROOT_mutation=False,all_private_sources_restored0644=True,all_private_directories_restored0755=True)
    print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__':main()
