#!/usr/bin/env python3
"""ROOT reads the completed actual outer and original final inner evidence."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

A=Path(__file__).absolute().parent;R=A.parents[2];C=A/'reviewed_candidate'
O=A/'tmp/root_pr47_current_outer_20261003T063156.236399Z'
I=A/'tmp/root_pr47_current_build_20261003T063156.293697Z'
assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def obj(p):return json.loads(read(p))
def row(p):
    b=read(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def canonical(n):
    assert type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n
    p=PurePosixPath(n);assert not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts)
def clock(v):
    t=dt.datetime.fromisoformat(v);assert t.utcoffset()==dt.timedelta(0);return t
assert R==Path('/Users/alec/Documents/Math')
cap=obj(O/'CAPTURE.json')
assert sha(read(O/'CAPTURE.json'))=='43cef6efd729ed5c7c3aed280421ba80821ee8fb49abefb54ea5bded698a7c1a'
assert cap['schema']=='PR47_ROOT_ACTUAL_BUILDER_OPERATION_v1'
assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0
assert cap['operator_pid']==53866 and cap['pid']==53867 and cap['builder_unchanged_after_child'] is True and cap['operator_unchanged_after_child'] is True
assert clock(cap['finished_utc'])<dt.datetime.now(dt.timezone.utc)
assert cap['current_whole_verdict'] is None and cap['new_whole_current_gate']=='PENDING'
pre=obj(O/'OPERATION_PRELAUNCH.json')
assert pre['argv']==cap['argv'] and pre['operator_pid']==cap['operator_pid']
for name,key,source in [('PRELAUNCH_BUILDER_SOURCE.py','builder_sha256','prepare_current_packet.py'),('PRELAUNCH_OPERATOR.py','operator_sha256','capture_root_builder_operation.py')]:
    assert sha(read(O/name))==cap[key]==sha(read(A/'current_preparation_family_v2'/source))
for ch in ['stdout','stderr']:
    b=read(O/cap[ch]['path']);assert len(b)==cap[ch]['bytes'] and sha(b)==cap[ch]['sha256']
assert not read(O/'stderr.bin')
output=obj(O/'stdout.bin');assert output['current_whole_verdict'] is None and output['full_problem_solved'] is False
mf=obj(C/'MANIFEST.json');msha=sha(read(C/'MANIFEST.json'))
assert msha=='a7d1acc9dbbf8cd5435d0bebd8f6b1a540ecb0f2aea8d0c616c46bc5bf6b4ea5'==output['manifest_sha256']
assert mf['schema']=='PR47_STRICT_CURRENT_PACKET_v1' and mf['self_excluded']==['MANIFEST.json'] and mf['files_count']==len(mf['files'])==1328
names=set()
for r in mf['files']:
    assert set(r)=={'path','bytes','sha256'} and type(r['bytes']) is int
    canonical(r['path']);assert r['path'] not in names;names.add(r['path'])
    p=C/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
actual=set();dirs=set()
for p in C.rglob('*'):
    assert not p.is_symlink();n=p.relative_to(C).as_posix()
    if p.is_file():actual.add(n)
    else:assert stat.S_ISDIR(p.stat().st_mode);dirs.add(n)
assert actual==names|{'MANIFEST.json'} and dirs==set(mf['directories'])
assert dirs=={p.as_posix() for n in actual for p in PurePosixPath(n).parents if p.as_posix()!='.'}
assert stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444
commands=obj(I/'GIT_COMMANDS.json');assert type(commands) is list and len(commands)==49
streams=[];children=set()
main=obj(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['current_head']
for c in commands:
    assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and c['pid'] not in children;children.add(c['pid'])
    assert type(c['exit_code']) is int and c['exit_code']==0 and c['cwd']==str(R) and c['stdin_supplied'] is False
    assert clock(cap['started_utc'])<=clock(c['started_utc'])<clock(c['finished_utc'])<=clock(cap['finished_utc'])
    assert c['argv'][0]=='git' and c['argv'][1] in {'branch','show','ls-tree','rev-parse','diff'}
    for ch in ['stdout','stderr']:
        canonical(c[ch]['path']);p=I/c[ch]['path'];b=read(p)
        assert len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256'];streams.append(row(p))
        if ch=='stderr':assert not b
    b=read(I/c['stdout']['path'])
    if c['argv'][1]=='branch':assert b==b'main\n'
    elif c['argv'][1]=='show':
        ref,path=c['argv'][2].split(':',1)
        if ref=='487327b2412c436ae69e8c52bf353a9a1fb7594e':
            prefix='unsolved_math_prioritization/attempts/2849/';assert path.startswith(prefix)
            n=path[len(prefix):];assert b==read(A/'source_snapshot'/n)==read(C/'original_archive'/n)
        else:assert ref==main and b==read(C/'native4_proposal/preimage'/path.replace('/','__'))
    elif c['argv'][1]=='diff' and '--binary' in c['argv']:assert b==read(A/'original_diff.patch')==read(C/'original_diff.patch')
prefix=obj(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
assert prefix==commands[:len(prefix)] and len(prefix)==47<len(commands)
deps=obj(C/'CURRENT_DEPENDENCIES.json');assert deps['anchor']=='repository_root' and len(deps['files'])==1422
for r in deps['files']:
    canonical(r['path']);p=R/r['path'];b=read(p)
    assert len(b)==r['bytes'] and sha(b)==r['sha256']
    if 'full_mode' in r:assert stat.S_IMODE(p.stat().st_mode)==r['full_mode']
native4={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
for r in deps['current_native13']:
    if r['path'] not in native4:
        p=R/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
q=read(C/'native4_proposal/preimage/unsolved_math_prioritization__QUEUE.md')
p=read(C/'native4_proposal/prospective/unsolved_math_prioritization__QUEUE.md')
before=q.splitlines(keepends=True);after=p.splitlines(keepends=True);assert len(before)==len(after)
changed=[(a,b) for a,b in zip(before,after) if a!=b];assert len(changed)==1
left,right=[v.decode().split('|') for v in changed[0]]
assert len(left)==len(right)==14 and left[2].strip()==right[2].strip()=='2849 / KP-3.51'
assert {i for i,(a,b) in enumerate(zip(left,right)) if a!=b}<={8,9,11}
assert left[8].strip()=='queued' and right[8].strip()=='unsolved' and left[9].strip()=='0/5' and right[9].strip()=='1/5'
for n in native4:
    name=n.replace('/','__');b=read(C/'native4_proposal/preimage'/name);a=read(C/'native4_proposal/prospective'/name)
    assert a==(p if n.endswith('/QUEUE.md') else b)
record={'schema':'pr47-root-complete-actual-current-freeze-readback/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'verification_pid':os.getpid(),'status':'PASS_COMPLETED_ORIGINAL_INNER_OUTER_FULL_READBACK','packet_manifest':row(C/'MANIFEST.json'),'packet_files_count':mf['files_count'],'packet_directories':len(dirs),'complete_actual_outer_capture':cap,'complete_outer_stdout_value':output,'complete_final_original_inner_commands':commands,'complete_stream_members':streams,'frozen_inner_prefix_commands':len(prefix),'final_original_inner_commands':len(commands),'all_dependency_members_read':len(deps['files']),'all_packet_member_bytes_full_modes_read':True,'stable9_live_match':True,'queue_only_allowed_named_cells_changed':True,'state_history_inventory_prospective_unchanged':True,'all16_original_archive_bytes_immutable':True,'full_proof_reading_reference':'ROOT_MATHEMATICAL_REVIEW.md','ROOT_full_command_record_and_outer_streams_personally_read':True,'old_PASS_transferred':False,'new_whole_current_gate':'PENDING','future_acceptance_approved':False,'limitations':'Full structural evidence reading accompanies separately recorded mathematical/primary-text reasoning. Native4/main are dated; new fresh13 authority is required before eventual acceptance.'}
with (A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json').open('xb') as h:h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
print(json.dumps({k:record[k] for k in ['status','utc','verification_pid','packet_files_count','packet_directories','frozen_inner_prefix_commands','final_original_inner_commands','all_dependency_members_read','new_whole_current_gate','future_acceptance_approved']},sort_keys=True))
