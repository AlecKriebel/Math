#!/usr/bin/env python3
"""ROOT's actual complete immutable original inspection and unchanged replay."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

A=Path(__file__).absolute().parent;R=A.parents[2];D=A/'root_original_actual_reproduction'
H='036a5ed59bee5ed79f08349290481584610f1456'
BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def obj(p):return json.loads(read(p))
def dump(p,o):
    with p.open('xb') as f:f.write((json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
def typed(v):
    if type(v) is dict:return ('dict',[(k,typed(x)) for k,x in sorted(v.items())])
    if type(v) is list:return ('list',[typed(x) for x in v])
    return (type(v).__name__,v)
def row(p):
    b=read(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
D.mkdir(exist_ok=False);SOURCE=read(Path(__file__));(D/'PRELAUNCH_ROOT_OPERATOR.py').write_bytes(SOURCE)
captures=[]
def command(label,argv,source=None):
    cdir=D/label;cdir.mkdir(exist_ok=False)
    (cdir/'PRELAUNCH_OPERATOR.py').write_bytes(SOURCE)
    sr=None
    if source is not None:
        sr=row(source);(cdir/'PRELAUNCH_TARGET.py').write_bytes(read(source))
    pre={'schema':'pr49-root-operation-prelaunch/v1','argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'started_utc':utc(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'source':sr,'source_unchanged':None,'operator_sha256':sha(SOURCE),'stdin_supplied':False}
    dump(cdir/'PRELAUNCH.json',pre);c=dict(pre)
    with (cdir/'stdout.bin').open('xb') as out,(cdir/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
        c.update(actual_execution=True,pid=child.pid)
        try:c['exit_code']=child.wait(timeout=60);c['completed']=True
        except BaseException:child.kill();c['exit_code']=child.wait();raise
    c.update(schema='pr49-root-actual-unchanged-helper/v1' if source is not None else 'pr49-root-actual-readonly-git/v1',finished_utc=utc(),operator_unchanged=read(Path(__file__))==SOURCE,source_unchanged=(read(source)==read(cdir/'PRELAUNCH_TARGET.py')) if source is not None else None)
    for ch in ['stdout','stderr']:c[ch]=row(cdir/(ch+'.bin'))
    dump(cdir/'CAPTURE.json',c);captures.append(c)
    assert c['exit_code']==0 and c['operator_unchanged'] is True and not read(cdir/'stderr.bin')
    if source is not None:assert c['source_unchanged'] is True
    return read(cdir/'stdout.bin')

mf=obj(A/'ORIGINAL_PREPARATION_MANIFEST.json')
assert sha(read(A/'ORIGINAL_PREPARATION_MANIFEST.json'))=='2eecad772938f3b220936c3317f1266d9a98de0f9d9750a6efa725c665f63b4c'
assert mf['files_count']==len(mf['files'])==350 and mf['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json']
for r in mf['files']:
    p=A/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode']==0o444
snap=obj(A/'snapshot_manifest.json');original={}
assert snap['original_files']==len(snap['files'])==16 and snap['head']==H and snap['merge_base']==snap['github_base']==BASE
for index,r in enumerate(snap['files']):
    n=r['relative_path'];b=read(A/'source_snapshot'/n)
    assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE((A/'source_snapshot'/n).stat().st_mode)==0o444
    assert command('git_body_'+str(index),['git','show',H+':'+r['path']])==b
    assert command('git_tree_'+str(index),['git','ls-tree',H,'--',r['path']]).decode().strip()=='100644 blob '+r['git_object']+'\t'+r['path']
    original[n]=b
diff=command('git_complete_diff',['git','diff','--no-ext-diff','--no-textconv','--binary',BASE,H,'--'])
assert diff==read(A/'original_diff.patch') and len(diff)==52829 and sha(diff)=='9aafdb42b2983020e919d6ff66b03720e1d858eebd98b4e46fa6b3909923fb50'
turns=json.loads(original['turns.json']);assert type(turns['id']) is int and turns['id']==30000703 and type(turns['count']) is int and turns['count']==0 and turns['substantive_attempts']==[]
assert original['prior_report.json']==b'null\n' and original['verify.py']==original['review/submitted_verify.py'] and original['verification.json']==original['review/verification.json']
results={}
for label,name,receipt,expected in [('author','verify.py','verification.json',69),('identical_submitted','review/submitted_verify.py','review/verification.json',69),('historical_independent','review/independent_checks.py','review/independent_results.json',187)]:
    folder=D/('private_'+label);folder.mkdir();helper=folder/Path(name).name;helper.write_bytes(original[name])
    output=command(label+'_actual_capture',['/usr/bin/python3','-B',str(helper)],helper)
    saved=read(folder/Path(receipt).name);assert saved==original[receipt]
    full=json.loads(saved);assert typed(full)==typed(json.loads(original[receipt])) and type(full['passed']) is int and full['passed']==expected and full['failed']==0 and full['sympy_version']=='1.14.0' and len(full['checks'])==expected and set(full['checks'].values())=={'PASS'}
    assert typed(json.loads(output))==typed({k:v for k,v in full.items() if k!='checks'})
    results[label]=full
assert len(captures)==36
result={'schema':'pr49-root-original-complete-reproduction/v1','status':'PASS_ROOT_EXACT_ORIGINAL_AND_LITERAL_UNCHANGED_REPRODUCTION','created_utc':utc(),'actual_operator_pid':os.getpid(),'original_head':H,'github_base':BASE,'actual_merge_base':BASE,'original_files':16,'whole_original_diff_bytes':len(diff),'whole_original_diff_sha256':sha(diff),'original_manifest':row(A/'ORIGINAL_PREPARATION_MANIFEST.json'),'all350_original_payloads_read_in_full_with_full_modes':True,'complete_original_JSON_values':{n:json.loads(b) for n,b in original.items() if n.endswith('.json')},'entire_original_turns':turns,'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'complete_actual_Git_captures':captures[:33],'complete_actual_helper_captures':captures[33:],'entire_replayed_results':results,'identical_submitted_counted_independent':False,'prior_absence_vs_null_qualification':'Original literal null is an administrative marker; full raw audit must separately establish absent key and literal SQLite {}.','raw_SQL_independently_reaudited_by_ROOT':'PENDING','mathematical_notes':'ROOT_MATHEMATICAL_REVIEW.md','known_credited_result_only':True,'project_solved':False,'novelty_claimed':False,'future_acceptance_approved':False,'foreign_native_raw_SQL_PDF_OCR_pixel_bodies_copied':False}
dump(D/'ROOT_REPRODUCTION_RESULT.json',result)
print(json.dumps({'status':result['status'],'actual_operator_pid':os.getpid(),'actual_readonly_Git_children':33,'actual_unchanged_helper_children':3,'helper_pass_counts':[69,69,187],'all350_original_members_full_read':True,'future_acceptance_approved':False},indent=2))
