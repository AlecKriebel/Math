"""Real OS failure branches of unchanged harness orchestration, with synthetic children.

This is not scientific evidence: child processes emit explicitly synthetic frozen
result fixtures. The actual scientific replay is retained in a separate directory.
All failure attempts and raw streams are retained. No candidate inputs are edited.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, contextlib, hashlib, importlib.util, io, json, runpy, shutil, subprocess, sys

O=Path(__file__).resolve().parent
V=O/'actual_zip_extraction/k303b_outer_center_pedal_product/verification'
OUT=O/'own_real_failure_controls';OUT.mkdir()
raw=(V/'run_checks.py').read_bytes();tree=ast.parse(raw)
cases=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='cases' for x in n.targets)))
lookup={Path(r[1]).name:r for r in cases}
real_run=subprocess.run
rows=[]
marker_out=b'OWN SYNTHETIC REAL CHILD stdout\x00\xff\n';marker_err=b'OWN SYNTHETIC REAL CHILD stderr\x00\xfe\n'
for mode in ['timeout','launch','nonzero','malformed','missing_result','after_integrity']:
    root=V
    if mode=='after_integrity':
        # Only this separately labelled disposable owned clone is faulted.
        clone=OUT/'faulted_owned_archive';shutil.copytree(V.parent,clone);root=clone/'verification'
    target=OUT/mode
    target_name='inherited' if mode=='malformed' else 'author' if mode=='timeout' else 'classical_bridge'
    invocations=[]
    def wrapper(command,**kw):
        case=lookup[Path(command[2]).name];name,script,copytree,outfile,expected,ignored=case
        invocations.append(name)
        child_mode=mode if name==target_name else 'success'
        if mode=='launch' and name==target_name:
            return real_run([str(OUT/'MISSING_EXECUTABLE_FOR_REAL_LAUNCH_FAILURE')],**kw)
        if mode=='after_integrity' and name==target_name:
            (root/'README.md').write_bytes((root/'README.md').read_bytes()+b'\nOWNED CLONE INPUT FAULT\n')
            child_mode='success'
        if outfile:
            output=Path(command[command.index('--output')+1]) if name=='physical' else Path(kw['cwd'])/outfile
        else:output='-'
        fixture=[sys.executable,'-B',str(O/'real_child_fixture.py'),child_mode,str(root/expected),str(output)]
        if mode=='timeout' and name==target_name:kw['timeout']=0.5
        return real_run(fixture,**kw)
    # runpy executes the exact unchanged harness source. Only its child API is
    # replaced with real fixture-process invocations; integrity remains actual.
    original_argv=sys.argv;original_path=list(sys.path);old_integrity=sys.modules.pop('integrity',None)
    subprocess.run=wrapper;sys.path.insert(0,str(root));sys.argv=[str(root/'run_checks.py'),'--output',str(target),'--jobs','3']
    console=io.StringIO();code=None
    try:
        with contextlib.redirect_stdout(console):
            try:runpy.run_path(str(root/'run_checks.py'),run_name='__main__')
            except SystemExit as e:code=e.code
    finally:
        subprocess.run=real_run;sys.argv=original_argv;sys.path[:]=original_path;sys.modules.pop('integrity',None)
        if old_integrity is not None:sys.modules['integrity']=old_integrity
    (target/'SYNTHETIC_ROLE.json').write_text(json.dumps(dict(mode=mode,role=__doc__,actual_science_executed=False),indent=2)+'\n')
    (target/'orchestration_stdout.txt').write_text(console.getvalue())
    receipt=json.loads((target/'REPRODUCTION.json').read_text());bad=[x for x in receipt['results'] if x['status']!='PASS']
    assert code==1 and receipt['status']=='FAIL' and len(receipt['results'])==8 and len(invocations)==8
    if mode=='after_integrity':assert len(bad)==0 and receipt['input_integrity_error'] is not None
    else:
        assert len(bad)==1 and bad[0]['name']==target_name and receipt['input_integrity_error'] is None
        failure=bad[0]
        if mode in ('timeout','nonzero'):
            assert (target/target_name/'stdout.txt').read_bytes()==marker_out
            assert (target/target_name/'stderr.txt').read_bytes()==marker_err
        if mode=='timeout':assert failure['execution_error']['kind']=='timeout' and failure['returncode'] is None
        if mode=='launch':assert failure['execution_error']['kind']=='launch_error'
        if mode=='nonzero':assert failure['returncode']==23
    rows.append(dict(mode=mode,exit=code,aggregate_status=receipt['status'],all_eight_outcomes_retained=True,failed_suites=len(bad),after_integrity_checked=receipt['input_integrity_error'] is not None or receipt['verification_files_after']==149))

guards=[]
for label,extra,program,target in [
    ('inside_archive',[],V/'run_checks.py',V.parent/'guard_output_must_not_exist'),
    ('inside_native_sibling',[],V/'run_checks.py',V.parent/'pr_update/5100015/guard_output_must_not_exist'),
    ('optimized_run',['-O'],V/'run_checks.py',OUT/'optimized_must_not_exist'),
    ('optimized_integrity',['-O'],V/'integrity.py',None)]:
    command=[sys.executable]+([] if extra is None else ['-B']+extra)+[str(program)]
    if target is not None:command+=['--output',str(target)]
    result=real_run(command,capture_output=True)
    (OUT/(label+'.stdout')).write_bytes(result.stdout);(OUT/(label+'.stderr')).write_bytes(result.stderr)
    assert result.returncode!=0 and (target is None or not target.exists())
    guards.append(dict(label=label,rejected=True,returncode=result.returncode))

# In-place check has no child scientific execution. Actual archive and candidate
# remain unchanged; faulted disposable clone paths are explicitly excluded.
integrity_result=real_run([sys.executable,'-B',str(V/'integrity.py')],capture_output=True)
assert integrity_result.returncode==0
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',tested_harness_sha256=hashlib.sha256(raw).hexdigest(),real_os_failure_modes=rows,guards=guards,original_archive_integrity=json.loads(integrity_result.stdout),role='Synthetic successful fixtures plus real OS timeout/launch/nonzero and input-fault failure checks; not scientific reproduction')
(O/'INDEPENDENT_HARNESS_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
