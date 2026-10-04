"""Root full overlay/index verification; stages only individually reviewed paths."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr40_2814';K=R/'unsolved_math_prioritization/attempts/2814'
def H(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def J(p):return json.loads(p.read_bytes())
z=J(A/'integration_check.json');rows=z['canonical_overlay_files'];names=[]
for item in rows:
    n=item['path'];assert n not in names;names.append(n);p=K/n;assert p.is_file() and not p.is_symlink();b=p.read_bytes();assert len(b)==item['bytes'] and H(b)==item['sha256']
assert {p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()}==set(names)
assert H((R/'unsolved_math_prioritization/QUEUE.md').read_bytes())==z['whole_queue_after_sha256']
snapshot=J(A/'snapshot_manifest.json')
for item in snapshot['files']:
    assert (K/'original_archive'/item['path']).read_bytes()==(A/'source_snapshot'/item['path']).read_bytes()
assert (K/'SOURCE_STATUS.md').read_bytes()==(A/'source_snapshot/SOURCE_STATUS.md').read_bytes()
assert (K/'turns.json').read_bytes()==(A/'source_snapshot/turns.json').read_bytes()
assert not git('diff','--name-only','--diff-filter=U').strip()
assert git('rev-parse','MERGE_HEAD').decode().strip()=='163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'
owned={'unsolved_math_prioritization/attempts/2814/'+n for n in names}|{'unsolved_math_prioritization/QUEUE.md'}
for i in range(0,len(owned),100):git('add','-f','--',*sorted(owned)[i:i+100])
staged=set(git('diff','--cached','--name-only').decode().splitlines());assert staged==owned
for entry in git('ls-files','--stage','-z').split(b'\0'):
    if not entry:continue
    meta,n=entry.split(b'\t',1);name=n.decode()
    if name not in owned:continue
    mode,oid,stage=meta.split();assert mode==b'100644' and stage==b'0';b=(R/name).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()
for item in J(A/'integration_preflight.json')['foreign_logs']:
    b=(R/item['path']).read_bytes();assert len(b)==item['bytes'] and H(b)==item['sha256']
receipt=dict(status='PASS',utc=dt.datetime.now(dt.timezone.utc).isoformat(),canonical_members=len(rows),all_canonical_bytes_exact=True,original13_archive_exact=True,original_SOURCE_STATUS_and_zero_ledger_exact=True,complete_named_queue_verified=True,all_exact_staged_index_bytes_modes=True,foreign_logs_excluded_preserved=True,staged_paths=sorted(owned))
with (A/'ROOT_ACTUAL_OVERLAY_AND_INDEX_INSPECTION.json').open('x') as f:json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',canonical_members=len(rows),staged_members=len(staged))))
