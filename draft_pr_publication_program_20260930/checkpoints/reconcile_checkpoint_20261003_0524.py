#!/usr/bin/env python3
"""Reconcile the completed stage capture; its own stream was an honest live prefix."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
P=Path(__file__).absolute().parent
R=P.parents[1]
A=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
cp=P/'CHECKPOINT_20261003_0524.json'
c=json.loads(cp.read_bytes())

def sha(b):
    return hashlib.sha256(b).hexdigest()

def git(*argv):
    return subprocess.check_output(['git',*argv],cwd=R)

assert git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==c['main_before']
names={r['path'] for r in c['owned_files']}|{cp.relative_to(R).as_posix()}
before={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert before<=names
changed=[]
for r in c['owned_files']:
    p=R/r['path']; b=p.read_bytes()
    assert stat.S_IMODE(p.stat().st_mode)==r['observed_full_mode']
    if len(b)!=r['bytes'] or sha(b)!=r['sha256']: changed.append(r['path'])
stream=(A/'root_checkpoint_0524_v2_actual_capture/stdout.bin').relative_to(R).as_posix()
assert changed==[stream]
capdir=A/'root_checkpoint_0524_v2_actual_capture'
cap=json.loads((capdir/'CAPTURE.json').read_bytes())
assert cap['actual_execution'] is True and cap['completed'] is True and cap['pid']==93564 and type(cap['exit_code']) is int and cap['exit_code']==0
for k in ('stdout','stderr'):
    b=(capdir/cap[k]['path']).read_bytes()
    assert len(b)==cap[k]['bytes'] and sha(b)==cap[k]['sha256']
phase=json.loads((capdir/'stdout.bin').read_bytes())
assert phase['foreign_staged']==0 and phase['active_families_staged'] is False
for p in capdir.iterdir():
    assert p.is_file() and not p.is_symlink(); names.add(p.relative_to(R).as_posix())
names.add(Path(__file__).relative_to(R).as_posix())
record=P/'CHECKPOINT_20261003_0524_POST_STAGE_QUALIFICATION.json'
with record.open('x') as h:
    json.dump(dict(schema='ROOT_checkpoint_completed_stage_reconciliation/v1',utc=dt.datetime.now(dt.timezone.utc).isoformat(),pid=os.getpid(),
        original_dated_preexit_checkpoint_sha256=sha(cp.read_bytes()),original_dated_checkpoint_future_authority=False,
        changed_since_dated_listing=changed,reason='Only the actual live outer stdout prefix grew after the stage child completed; the old listing remains dated first-party preexit evidence, not a completed receipt. The full actual completed CAPTURE and stdout are now reconciled before commit.',
        complete_stage_capture=cap,complete_stage_result=phase,final_publication_native_or_future_merge_authority=False,
        other_owned_members_unchanged=True,foreign_or_active_agent_members_staged=False),h,indent=2); h.write('\n')
names.add(record.relative_to(R).as_posix())
subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=b''.join(n.encode()+b'\0' for n in sorted(names)),check=True)
staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0') if n}
assert staged<=names and not staged&{r['path'] for r in c['foreign_dirty_before']}
entries={}
for line in git('ls-files','--stage','-z').decode().split('\0'):
    if line:
        info,n=line.split('\t'); mode,oid,stage=info.split()
        if n in staged:
            assert stage=='0' and mode in {'100644','100755'}; entries[n]=oid
ordered=sorted(staged)
child=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
data,err=child.communicate(b''.join((entries[n]+'\n').encode() for n in ordered))
assert child.returncode==0 and not err
offset=0
for n in ordered:
    end=data.index(b'\n',offset); oid,kind,size=data[offset:end].decode().split()
    count=int(size); start=end+1
    assert oid==entries[n] and kind=='blob' and data[start:start+count]==(R/n).read_bytes() and data[start+count:start+count+1]==b'\n'
    offset=start+count+1
assert offset==len(data) and git('rev-parse','HEAD').decode().strip()==c['main_before']
print(json.dumps(dict(status='PASS_COMPLETED_STAGE_FULL_STREAM_RECONCILIATION',pid=os.getpid(),main_before=c['main_before'],staged=len(staged),foreign_staged=0,active_agent_members_staged=False,full_staged_bytes_verified=True,live_stage_stdout_prefix_reconciled=True)))
