#!/usr/bin/env python3
"""Full postexit original inner/outer and current packet readback by ROOT."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
A=Path(__file__).absolute().parent
R=A.parents[2]
C=A/'reviewed_candidate'
O=A/'tmp/root_pr46_current_v2_outer_20261003T051557.465033Z'
I=A/'tmp/root_pr46_current_v2_build_20261003T051557.532485Z'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    assert stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()

def obj(p):
    return json.loads(read(p))

def row(p):
    b=read(p)
    return dict(path=p.relative_to(A).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))

def canonical(n):
    assert type(n) is str and n and n != '.'
    p=PurePosixPath(n)
    assert not p.is_absolute() and str(p)==n and not set(p.parts).intersection({'.','..','.git','__pycache__'}) and '\\' not in n and '\0' not in n

def clock(s):
    t=dt.datetime.fromisoformat(s)
    assert t.utcoffset()==dt.timedelta(0)
    return t

assert R==Path('/Users/alec/Documents/Math')
cap=obj(O/'CAPTURE.json')
assert sha(read(O/'CAPTURE.json'))=='4d708706dd03e0e21325e01c1cf3a0e14e9814bb803156d0cb52264ab93cc311'
assert cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0
assert cap['operator_pid']==85727 and cap['pid']==85728 and cap['builder_unchanged_after_child'] is True and cap['operator_unchanged_after_child'] is True
assert clock(cap['finished_utc']) < dt.datetime.now(dt.timezone.utc)
assert cap['current_whole_verdict'] is None and cap['new_whole_current_gate']=='PENDING'
pre=obj(O/'OPERATION_PRELAUNCH.json')
assert pre['argv']==cap['argv'] and pre['operator_pid']==cap['operator_pid']
assert sha(read(O/'PRELAUNCH_BUILDER_SOURCE.py'))==cap['builder_sha256']==sha(read(A/'current_preparation_family_v2/prepare_current_packet.py'))
assert sha(read(O/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256']==sha(read(A/'current_preparation_family_v2/capture_root_builder_operation.py'))
for key in ('stdout','stderr'):
    b=read(O/cap[key]['path'])
    assert len(b)==cap[key]['bytes'] and sha(b)==cap[key]['sha256']
assert not read(O/'stderr.bin')
output=obj(O/'stdout.bin')
assert output['status']=='ACTUAL_CURRENT_FREEZE_NEW_WHOLE_GATE_PENDING' and output['current_whole_verdict'] is None
mf=obj(C/'MANIFEST.json')
assert sha(read(C/'MANIFEST.json'))=='66239699390b279235c4064208e63134049a5804884818de9176d377476a189d'
assert output['manifest_sha256']==sha(read(C/'MANIFEST.json')) and mf['self_excluded']==['MANIFEST.json']
assert type(mf['files_count']) is int and mf['files_count']==len(mf['files'])
names=set()
for r in mf['files']:
    assert type(r) is dict and set(r)=={'path','bytes','sha256'}
    canonical(r['path']); assert r['path'] not in names and type(r['bytes']) is int
    names.add(r['path']); p=C/r['path']; b=read(p)
    assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
files=set(); dirs=set()
for p in C.rglob('*'):
    assert not p.is_symlink()
    n=p.relative_to(C).as_posix()
    if stat.S_ISREG(p.stat().st_mode): files.add(n)
    else: assert stat.S_ISDIR(p.stat().st_mode); dirs.add(n)
assert files==names|{'MANIFEST.json'} and stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444
assert dirs=={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'}
commands=obj(I/'GIT_COMMANDS.json')
assert type(commands) is list and len(commands)==45
full_streams=[]
for index,c in enumerate(commands):
    assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0
    assert c['cwd']==str(R) and c['stdin_supplied'] is False
    assert clock(cap['started_utc'])<=clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(cap['finished_utc'])
    assert c['argv'][0]=='git' and c['argv'][1] in {'branch','show','ls-tree','rev-parse','diff'}
    for key in ('stdout','stderr'):
        p=I/c[key]['path']; b=read(p)
        assert len(b)==c[key]['bytes'] and sha(b)==c[key]['sha256']
        full_streams.append(row(p))
        if key=='stderr': assert not b
    b=read(I/c['stdout']['path'])
    if c['argv'][1]=='branch': assert b==b'main\n'
    elif c['argv'][1]=='show':
        ref,path=c['argv'][2].split(':',1)
        if ref=='a39d178b10f75fb127058b08e0d0002b3ae97f8a':
            n=path.removeprefix('unsolved_math_prioritization/attempts/30004438/')
            assert b==read(A/'source_snapshot'/n)==read(C/'original_archive'/n)
        else:
            assert ref=='8f2b03b15902069ac24c1de59de1bf32b9c22f84'
            assert b==read(C/'native4_proposal/preimage'/path.replace('/','__'))
    elif c['argv'][1]=='diff' and '--binary' in c['argv']:
        assert b==read(A/'original_diff.patch')==read(C/'original_diff.patch')
prefix=obj(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
assert prefix==commands[:len(prefix)] and len(prefix)<len(commands)
dependencies=obj(C/'CURRENT_DEPENDENCIES.json')
for r in dependencies['files']:
    canonical(r['path']); b=read(A/r['path'])
    assert len(b)==r['bytes'] and sha(b)==r['sha256']
native4={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
for r in dependencies['current_native13']:
    if r['path'] not in native4:
        p=R/r['path']; b=read(p)
        assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
q=read(C/'queue_proposal/QUEUE_PREIMAGE.md')
p=read(C/'queue_proposal/QUEUE_PROSPECTIVE.md')
ql=q.splitlines(keepends=True); pl=p.splitlines(keepends=True)
assert len(ql)==len(pl)
changed=[(l,r) for l,r in zip(ql,pl) if l!=r]
assert len(changed)==1
left,right=[b.decode().split('|') for b in changed[0]]
assert left[2].strip()==right[2].strip()=='30004438 / OWR-17475-003'
assert len(left)==len(right)==14
assert {i for i,(l,r) in enumerate(zip(left,right)) if l!=r} <= {8,9,11}
assert left[8].strip()=='queued' and right[8].strip()=='already_solved' and left[9].strip()==right[9].strip()=='0/5'
for path in native4:
    name=path.replace('/','__')
    before=read(C/'native4_proposal/preimage'/name)
    after=read(C/'native4_proposal/prospective'/name)
    assert after==(p if path.endswith('/QUEUE.md') else before)
record=dict(schema='pr46-root-complete-actual-current-freeze-readback/v2',utc=dt.datetime.now(dt.timezone.utc).isoformat(),verification_pid=os.getpid(),
    status='PASS_COMPLETED_ORIGINAL_INNER_OUTER_FULL_READBACK',packet_manifest=row(C/'MANIFEST.json'),packet_files_count=mf['files_count'],packet_directories=len(dirs),
    complete_actual_outer_capture=cap,complete_final_original_inner_commands=commands,complete_stream_members=full_streams,
    frozen_inner_prefix_commands=len(prefix),final_original_inner_commands=len(commands),all_dependency_members_read=len(dependencies['files']),
    all_packet_member_bytes_full_modes_read=True,stable9_live_match=True,queue_only_allowed_named_cells_changed=True,state_history_inventory_prospective_unchanged=True,
    original_science_immutable=True,full_proof_reading_reference='ROOT_MATHEMATICAL_REVIEW.md',ROOT_full_command_record_and_outer_streams_personally_read=True,
    old_PASS_transferred=False,new_whole_current_gate='PENDING',future_acceptance_approved=False,
    limitations='Complete body/typed/hash readback is structural evidence. ROOT mathematical and scoped primary-text reasoning is separately recorded. Frozen native4/main is dated, and a newfresh13 is needed for future acceptance.')
with (A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json').open('xb') as h:
    h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode())
print(json.dumps({k:record[k] for k in ['status','utc','verification_pid','packet_files_count','packet_directories','frozen_inner_prefix_commands','final_original_inner_commands','all_dependency_members_read','new_whole_current_gate','future_acceptance_approved']},sort_keys=True))
