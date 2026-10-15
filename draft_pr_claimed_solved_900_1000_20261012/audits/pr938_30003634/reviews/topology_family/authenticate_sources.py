#!/usr/bin/env python3
"""Read-only authentication of all 44 immutable attempt blobs; JSON to stdout."""
import datetime,hashlib,json,subprocess,sys
from pathlib import Path
OWN=Path(__file__).resolve().parent
ROOT=OWN.parent.parent
COMMIT='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
PREFIX='unsolved_math_prioritization/attempts/30003634'
PINS={PREFIX+'/original/PROOF.md':'0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b',PREFIX+'/PUBLICATION_MANIFEST.json':'149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30',PREFIX+'/original/MANIFEST.json':'d1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a'}
REPO=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def run(stage):
 inventory=json.loads((ROOT/'ORIGINAL_SNAPSHOT.json').read_text())['files']
 paths=git('ls-tree','-r','--name-only',COMMIT,'--',PREFIX).decode().splitlines()
 diskpaths=sorted(str(p.relative_to(ROOT/'original')) for p in (ROOT/'original'/PREFIX).rglob('*') if p.is_file())
 rows=[]
 for name in paths:
  blob=git('show',COMMIT+':'+name)
  disk=(ROOT/'original'/name).read_bytes()
  bh=hashlib.sha256(blob).hexdigest();dh=hashlib.sha256(disk).hexdigest()
  rows.append(dict(path=name,bytes=len(blob),git_blob_sha256=bh,disk_sha256=dh,inventory_sha256=inventory.get(name),pass_all=bh==dh==inventory.get(name)))
 out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage=stage,source_commit=COMMIT,current_shared_head=git('rev-parse','HEAD').decode().strip(),branch=git('branch','--show-current').decode().strip(),selected_count=len(rows),actual_git_tree_count=len(paths),closed_inventory_matches=len(paths)==44 and sorted(paths)==sorted(inventory)==diskpaths,pinned_digests_pass=all(next(r for r in rows if r['path']==p)['git_blob_sha256']==h for p,h in PINS.items()),rows=rows)
 out['all_pass']=out['closed_inventory_matches'] and out['pinned_digests_pass'] and all(r['pass_all'] for r in rows)
 if not out['all_pass']:
  raise RuntimeError('immutable source authentication failed')
 return out
if __name__=='__main__':
 print(json.dumps(run(sys.argv[1] if len(sys.argv)>1 else 'replay'),indent=2))
