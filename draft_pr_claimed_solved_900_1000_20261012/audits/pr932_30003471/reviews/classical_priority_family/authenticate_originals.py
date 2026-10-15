#!/usr/bin/env python3
"""Read-only immutable-Git/disk authentication; writes only this review."""
import datetime, hashlib, json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
AUDIT = HERE.parent.parent
HEAD = 'c09ef9df8b1f4642be0396ba6343344be8fa25b0'
PREFIX = 'unsolved_math_prioritization/attempts/30003471'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)
def sha(data): return hashlib.sha256(data).hexdigest()
rows = []
for line in git('ls-tree', '-r', HEAD, '--', PREFIX).decode().splitlines():
    meta, path = line.split('\t', 1)
    mode, typ, blob = meta.split()
    raw = git('cat-file', 'blob', blob)
    disk = AUDIT / 'original' / path
    rows.append(dict(path=path, mode=mode, type=typ, git_blob=blob,
                     git_sha256=sha(raw), disk_sha256=sha(disk.read_bytes()),
                     bytes=len(raw), matches=disk.read_bytes()==raw))
proof = next(r for r in rows if r['path'].endswith('/public/PROOF.md'))
outer = next(r for r in rows if r['path'].endswith('/PUBLICATION_MANIFEST.json'))
out = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           immutable_head=HEAD, actual_git_prefix=PREFIX,
           current_shared_head=git('rev-parse','HEAD').decode().strip(),
           current_branch=git('branch','--show-current').decode().strip(),
           original_count=len(rows), all_originals_match=all(r['matches'] for r in rows),
           proof_expected_sha256='6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415',
           proof_sha256=proof['disk_sha256'],
           outer_manifest_expected_sha256='d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd',
           outer_manifest_sha256=outer['disk_sha256'], files=rows,
           mutations='None to original, Git index, HEAD, branch, remote or service')
assert len(rows)==29 and out['all_originals_match']
assert out['proof_sha256']==out['proof_expected_sha256']
assert out['outer_manifest_sha256']==out['outer_manifest_expected_sha256']
assert sys.argv[1] in ('START','END')
(HERE / ('ORIGINAL_AUTH_'+sys.argv[1]+'.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='files'},indent=2))
