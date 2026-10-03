"""Root actual merge tree and full prepush receipt inspection."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr40_2814';K='unsolved_math_prioritization/attempts/2814/'
def H(b):return hashlib.sha256(b).hexdigest()
def J(p):return json.loads(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
p=J(A/'integration_prepush.json');cap=J(A/'root_integration_prepush_actual_capture/CAPTURE.json');overlay=J(A/'integration_check.json')
assert cap['status']=='PASS' and cap['exit_code']==0 and cap['outer_errors']==[] and cap['fresh_native13_before']==cap['fresh_native13_after']
for field in ['stdout','stderr']:
    z=cap[field];b=(A/'root_integration_prepush_actual_capture'/z['path']).read_bytes();assert len(b)==z['bytes'] and H(b)==z['sha256']
assert p['merge_commit']==git('rev-parse','HEAD').decode().strip()
assert p['merge_parents']==git('show','-s','--format=%P','HEAD').decode().strip().split()==['f56477f54beb48eae1dc828da06eb195d07a0b3a','163e34d566d6cbaee3a2a8fdc6394fbb9e49a539']
assert p['merge_tree']==git('show','-s','--format=%T','HEAD').decode().strip()
rows=overlay['canonical_overlay_files'];actual=set()
for item in rows:
    n=K+item['path'];actual.add(n);raw=git('show','HEAD:'+n)
    assert len(raw)==item['bytes'] and H(raw)==item['sha256'] and raw==(R/n).read_bytes()
    entry=git('ls-tree','-z','HEAD','--',n);assert entry.startswith(b'100644 blob ') and entry.endswith(('\t'+n+'\0').encode())
assert set(git('diff','--name-only',p['merge_parents'][0],'HEAD').decode().splitlines())==actual|{'unsolved_math_prioritization/QUEUE.md'}
assert H((R/'unsolved_math_prioritization/QUEUE.md').read_bytes())==overlay['whole_queue_after_sha256']
assert not git('diff','--cached','--name-only').strip()
receipt=dict(status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_prepush_pid=cap['pid'],whole_prepared_overlay_members=len(rows),merge_commit=p['merge_commit'],merge_tree=p['merge_tree'],exact_two_parents=p['merge_parents'],complete_tree_payloads_modes_verified=True,entire_prepush_object=p,full_native13_and_captured_streams_unchanged=True)
with (A/'ROOT_ACTUAL_PREPUSH_INSPECTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',merge_commit=p['merge_commit'],canonical_members=len(rows))))
