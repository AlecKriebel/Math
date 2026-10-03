"""Root full automatic queue and exact original head/index inspection."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
Q='unsolved_math_prioritization/QUEUE.md';M='f56477f54beb48eae1dc828da06eb195d07a0b3a';H='163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('rev-parse','HEAD').decode().strip()==M and git('rev-parse','MERGE_HEAD').decode().strip()==H
assert git('diff','--name-only','--diff-filter=U').decode().splitlines()==[Q]
assert git('show',':2:'+Q)==(A/'integration_queue_before.md').read_bytes()
assert git('show',':3:'+Q)==git('show',H+':'+Q)
assert git('show',':1:'+Q)==git('show',git('merge-base',M,H).decode().strip()+':'+Q)
rows=json.loads((A/'snapshot_manifest.json').read_bytes())['files'];prefix='unsolved_math_prioritization/attempts/2814/'
expected={prefix+z['path'] for z in rows}|{Q}
assert set(git('diff','--cached','--name-only').decode().splitlines())==expected
for z in rows:
    p=R/prefix/z['path'];b=p.read_bytes();assert len(b)==z['size'] and sha(b)==z['sha256'] and not p.is_symlink()
    assert b==(A/'source_snapshot'/z['path']).read_bytes()
    assert git('ls-files','--stage','-z','--',prefix+z['path']).decode().split('\0')[:-1]==[z['mode']+' '+z['git_blob']+' 0\t'+prefix+z['path']]
raw=(R/Q).read_bytes();assert b'<<<<<<<' in raw and b'>>>>>>>' in raw
receipt=dict(status='PASS',approved_by_root=True,utc=dt.datetime.now(dt.timezone.utc).isoformat(),head=M,merge_head=H,whole_queue_sha256=sha(raw),complete_stage1_2_3_bytes_compared=True,original13_scientific_files_exact=True,staged_paths=sorted(expected),only_conflict=Q)
with (A/'ROOT_AUTOMATIC_MERGE_INSPECTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',reviewed_automatic_merge_sha256=sha((A/'ROOT_AUTOMATIC_MERGE_INSPECTION.json').read_bytes()),whole_queue_sha256=sha(raw))))
