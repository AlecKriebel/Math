#!/usr/bin/env python3
"""Independent complete-stream replay of the immutable public archive."""
from pathlib import Path
import hashlib,json,os,re,stat,subprocess,time
N=Path(__file__).resolve().parent
P=N/'archive_replay'
R=N/'bound_replay_receipts'
R.mkdir(exist_ok=True)
SP='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr329_20000450/geometry/.runtime/bin/python'
STD='/opt/homebrew/bin/python3'
sha=lambda b:hashlib.sha256(b).hexdigest()
def utc():
    r=subprocess.run(['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],capture_output=True,check=True)
    return r.stdout.decode().strip()
def inventory():
    fs={};ds={'.':format(stat.S_IMODE(P.stat().st_mode),'04o')}
    for p in sorted(P.rglob('*')):
        assert not p.is_symlink(),p
        rel=str(p.relative_to(P));m=format(stat.S_IMODE(p.stat().st_mode),'04o')
        if p.is_file():
            b=p.read_bytes();fs[rel]={'bytes':len(b),'sha256':sha(b),'mode':m}
        elif p.is_dir():ds[rel]=m
    return fs,ds
before=inventory();manifest=json.loads((P/'MANIFEST.json').read_bytes())
assert set(before[0])==set(manifest['files'])|{'MANIFEST.json'}
assert {k:v for k,v in before[0].items() if k!='MANIFEST.json'}==manifest['files']
assert {k:v for k,v in before[1].items() if k!='.'}==manifest['directory_modes']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
results=[]
def run(label,argv,script,exit_code=0,expected=None,geometry=False,chord=False):
    assert not (R/(label+'.json')).exists(),label
    body=script.read_bytes();started=utc();tm=time.monotonic_ns()
    rec={'label':label,'argv':argv,'cwd':str(P),'clock_argv':['/bin/date','-u','+%Y-%m-%dT%H:%M:%SZ'],
         'utc_start':started,'executed_body':str(script),'executed_body_sha256_before':sha(body),
         'runner_body_sha256':sha(Path(__file__).read_bytes()),'expected_exit':exit_code,
         'stdout_file':label+'.stdout','stderr_file':label+'.stderr','state':'started'}
    (R/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    with (R/(label+'.stdout')).open('wb') as out,(R/(label+'.stderr')).open('wb') as err:
        proc=subprocess.run(argv,cwd=P,env=env,stdout=out,stderr=err,check=False,timeout=240)
    stdout=(R/(label+'.stdout')).read_bytes();stderr=(R/(label+'.stderr')).read_bytes()
    rec.update(utc_end=utc(),elapsed_monotonic_ns=time.monotonic_ns()-tm,actual_exit=proc.returncode,
               stdout_bytes=len(stdout),stdout_sha256=sha(stdout),stderr_bytes=len(stderr),stderr_sha256=sha(stderr),
               executed_body_sha256_after=sha(script.read_bytes()),state='completed')
    (R/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert rec['executed_body_sha256_before']==rec['executed_body_sha256_after']
    assert proc.returncode==exit_code,(label,proc.returncode,stderr)
    if expected is not None:
        assert not stderr,(label,stderr)
        if geometry:
            lines=[]
            for line in stdout.decode().splitlines():
                if re.fullmatch(r'native_utc(?:_start|_end)? \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',line):continue
                line=re.sub(r' native_utc \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00$','',line)
                lines.append(line)
            actual=('\n'.join(lines)+'\n').encode();wanted=expected.read_bytes()
            assert actual==wanted,label
        else:
            actual=json.loads(stdout)
            if chord:
                assert 'interpreter' in actual;del actual['interpreter']
            assert actual==json.loads(expected.read_bytes()),label
        rec['complete_mathematical_output_equal']=True
        rec['expected_body_sha256']=sha(expected.read_bytes())
        (R/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    results.append(rec);print(label,proc.returncode,rec['utc_start'],rec['utc_end'],flush=True)
names=['geometry_source','geometry_quotient','geometry','geometry_primitivity','division_chord','division_model','division_finite','division_quintic','candidate','priority','arithmetic']
for name in names:
    script=P/'programs'/(name+'.py');geom=name.startswith('geometry')
    run('positive_'+name,[SP,'-B',str(script)],script,expected=P/'expected'/(name+('.txt' if geom else '.json')),geometry=geom,chord=name=='division_chord')
for mutant in ['drop_twist','wrong_radical','wrong_cyclotomic','wrong_norm_degree']:
    script=P/'programs/arithmetic.py'
    run('mutant_'+mutant,[SP,'-B',str(script),'--mutant',mutant],script,1,P/'expected'/('mutant_'+mutant+'.json'))
for name in names:
    script=P/'programs'/(name+'.py')
    run('optimization_guard_'+name,[SP,'-O','-B',str(script)],script,1)
    assert (R/('optimization_guard_'+name+'.stderr')).read_bytes()==b'Verification refuses Python optimization (-O/-OO).\n'
for label,argv,script in [
    ('shipped_verify_all',[SP,'-B',str(P/'verify.py'),'--python',SP],P/'verify.py'),
    ('shipped_verify_arithmetic_std',[STD,'-B',str(P/'verify.py'),'--suite','arithmetic','--python',STD],P/'verify.py'),
    ('public_priority_verify',[STD,'-B',str(P/'priority_evidence/verify_public_package.py')],P/'priority_evidence/verify_public_package.py')]:
    run(label,argv,script)
    assert not (R/(label+'.stderr')).read_bytes()
    assert json.loads((R/(label+'.stdout')).read_bytes())['status']=='PASS'
assert inventory()==before,'Archive mutation'
summary={'status':'PASS','utc_end':utc(),'positive_programs':11,'negative_mutants':4,'optimization_guards':11,
         'shipped_full_and_stdlib_arithmetic_replay':True,'public_priority_replay':True,
         'all_archive_bodies_modes_directories_unchanged':True,'receipts':results}
(N/'BOUND_PACKET_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='receipts'},indent=2))
