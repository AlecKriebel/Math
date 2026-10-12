"""Root reproduction and complete immutable reviewer02 evidence verification."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, sys

A=Path(__file__).resolve().parent
N=A/'preprint_review_02'
PY='/opt/homebrew/bin/python3.11'
phase=sys.argv[1]
assert phase in ('pre','post') and __debug__
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def inventory():
    rows={}
    for p in sorted(N.rglob('*')):
        assert not p.is_symlink() and (p.is_dir() or p.is_file())
        row={'type':'file' if p.is_file() else 'directory','mode':stat.S_IMODE(p.stat().st_mode)}
        if p.is_file():
            b=p.read_bytes();row.update(bytes=len(b),sha256=sha(b))
        rows[p.relative_to(N).as_posix()]=row
    return rows

out=A/('ROOT_PREPRINT02_PRECLOSURE_REPLAY.json' if phase=='pre' else 'ROOT_PREPRINT_REVIEW02_VERIFICATION.json')
assert not out.exists()
D=A/'root_replay_private'/('preprint_review02_'+phase+'_001')
D.mkdir(parents=True,exist_ok=False)
before=inventory()
(D/'whole_namespace_before.json').write_text(json.dumps(before,indent=2)+'\n')
plan=load(N/'closure_plan.json')
plan_sha=sha((N/'closure_plan.json').read_bytes())
assert plan_sha=='a84e819ca189b172781ec1e6a368c9183afa5f08702a79f8e709950b07260913'
for path,pin in plan['files'].items():
    if phase=='post' and path=='research_log.md': continue
    row=before[path]
    assert (row['bytes'],row['sha256'],oct(row['mode']))==(pin['bytes'],pin['sha256'],pin['mode']),path
pins=[{'path':name,**pin} for name,pin in load(A/'ROOT_PREPRINT_PACKAGE_VERIFICATION.json')['files'].items()]
for e in pins:
    b=(A/'preprint'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256']
for label,relative in [('default','preprint_draft002/integrity.stdout'),('full','preprint_draft001/full.stdout')]:
    assert (N/'native_runs'/(label+'.stdout')).read_bytes()==(A/'root_replay_private'/relative).read_bytes()
    assert (N/'native_runs'/(label+'.stderr')).read_bytes()==b''
runs=[]
def run(label,args,expected,mode=None):
    prep={'utc':utc(),'argv':args,'orchestrator_sha256':sha(Path(__file__).read_bytes()),
          'program_sha256':sha(Path(args[2]).read_bytes()),'expected_whole_stdout_bytes':len(expected),
          'expected_whole_stdout_sha256':sha(expected),'mode':mode}
    (D/(label+'.preexecution.json')).write_text(json.dumps(prep,indent=2)+'\n')
    z=subprocess.run(args,cwd=A,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    for k,b in [('stdout',z.stdout),('stderr',z.stderr)]: (D/(label+'.'+k)).write_bytes(b)
    r={**prep,'finished_utc':utc(),'exit_code':z.returncode,'stdout_path':str(D/(label+'.stdout')),
       'stderr_path':str(D/(label+'.stderr')),'stdout_bytes':len(z.stdout),'stdout_sha256':sha(z.stdout),
       'stderr_bytes':len(z.stderr),'whole_expected_output_compared':z.stdout==expected}
    (D/(label+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');runs.append(r)
    assert z.returncode==0 and z.stderr==b'' and z.stdout==expected,(label,z.stderr)
if phase=='pre':
    assert not (N/'CLOSURE_SEAL.json').exists()
    assert {p for p,v in before.items() if v['type']=='file'}==set(plan['files'])|{'closure_plan.json'}
    run('own_controls',[PY,'-B',str(N/'own_controls.py')],(N/'native_runs/own.stdout').read_bytes())
for mode in ('public','full'):
    obj=load(N/'terminal_expected'/(mode+'.stdout'))
    if phase=='post': obj['state']='SEALED_ONCE'
    if mode=='full': obj['external_bindings']=27
    expected=(json.dumps(obj,indent=2)+'\n').encode()
    args=[PY,'-B',str(N/'public/verify_review.py'),'--root',str(N),'--mode',mode]
    if phase=='pre': args+=['--proposal',str(N/'closure_plan.json')]
    if mode=='full': args+=['--include-external-sources']
    run(mode,args,expected,mode)
assert inventory()==before
for e in pins:
    b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
r={'utc':utc(),'status':'PASS_WHOLE_SECOND_FRESH_PREPRINT_REVIEW_'+phase.upper(),
   'mandatory_findings':0,'all_mandatory_submission_findings_resolved':True,
   'whole_verifier_output_compared':True,'closed_namespace_unchanged':phase=='post',
   'sealed_submission_files':pins,'native_runs':runs,'captures':runs,'whole_namespace':before,
   'package_full_and_default_outputs_equal_root':True,'closure_plan_sha256':plan_sha,
   'scope':'Root full concrete report/code/source comparison read; independently reproduced reviewer02 literal controls before closure. Exact whole public/private streams and all namespace paths/bodies/modes checked. Bounded priority; no global novelty or external human peer-review certificate.'}
if phase=='pre':
    (D/'research_log.before.md').write_bytes((N/'research_log.md').read_bytes())
else:
    old=load(A/'ROOT_PREPRINT02_PRECLOSURE_REPLAY.json')['whole_namespace']
    extra_files={p for p,v in before.items() if v['type']=='file'}-{p for p,v in old.items() if v['type']=='file'}
    assert extra_files==set(plan['final_records'])|set(plan['terminal_capture_allowlist'])
    assert not set(old)-set(before)
    for path,pin in old.items():
        if path!='research_log.md': assert before[path]==pin,path
    seal=load(N/'CLOSURE_SEAL.json')
    prior=(A/'root_replay_private/preprint_review02_pre_001/research_log.before.md').read_bytes()
    assert (N/'research_log.md').read_bytes()==prior+seal['research_log_append'].encode()
    assert before['research_log.md']['mode']==old['research_log.md']['mode']
    assert set(before)-set(old)==extra_files|{'terminal_verifier'}
    r.update(review_seal_path='CLOSURE_SEAL.json',review_seal_sha256=sha((N/'CLOSURE_SEAL.json').read_bytes()),
             closure_authorization_sha256=sha((A/'ROOT_PREPRINT02_CLOSURE_AUTHORIZATION.json').read_bytes()))
    r['package_native_streams']={label:{'stdout_path':str(N/'native_runs'/(label+'.stdout')),
          'stderr_path':str(N/'native_runs'/(label+'.stderr')),'bytes':(N/'native_runs'/(label+'.stdout')).stat().st_size,
          'sha256':sha((N/'native_runs'/(label+'.stdout')).read_bytes()),
          'exit_code':load(N/'native_runs'/(label+'.after.json'))['exit_code']} for label in ('default','full')}
out.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ('whole_namespace','captures')},indent=2))
