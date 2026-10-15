#!/usr/bin/env python3
"""Read-only exact-head binding; writes only into this review directory."""
import hashlib,json,pathlib,subprocess
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parent
REPO=ROOT.parents[2]
manifest=json.loads((ROOT/'snapshot_manifest.json').read_text())
assert manifest['head']=='967e8e489aa4599f712d5ddcde62e591827f7e38'
assert len(manifest['files'])==49
rows=[]
for rec in manifest['files']:
 data=(ROOT/'snapshot'/rec['path']).read_bytes()
 blob=subprocess.check_output(['git','show',f"{manifest['head']}:{rec['path']}"],cwd=REPO)
 assert data==blob,rec['path']
 assert len(data)==rec['bytes'],rec['path']
 assert hashlib.sha256(data).hexdigest()==rec['sha256'],rec['path']
 rows.append({'path':rec['path'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'git_exact_head_equal':True})
assert sum(r['path'].startswith('unsolved_math_prioritization/attempts/30004047/') for r in rows)==48
result={'status':'PASS','head':manifest['head'],'files_checked':len(rows),'target_files_checked':48,'queue_files_checked':1,'snapshot_manifest_sha256':hashlib.sha256((ROOT/'snapshot_manifest.json').read_bytes()).hexdigest(),'files':rows}
(HERE/'SNAPSHOT_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','head':manifest['head'],'files_checked':len(rows),'target_files_checked':48,'queue_files_checked':1},indent=2))
