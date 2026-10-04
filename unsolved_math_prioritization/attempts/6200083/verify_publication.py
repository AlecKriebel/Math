#!/usr/bin/env python3
"""Strict publication manifest and unchanged author/audit replay."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys

AUTHOR_MANIFEST='91313d8e77bbd9b47d478beee9aef2b6507a80063920d3853265013848d6e31d'
AUDIT_MANIFEST='ed1376d3dd6971dab6a1d52ec751ad108f77283bdbeb1073f16222b9bc3d3e4c'

def require(ok,message):
    if not ok:
        raise AssertionError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    require(__debug__,'Optimization disables the author assertions; do not use -O.')
    root=Path(__file__).resolve().parent
    for p in root.rglob('*'):
        require(not p.is_symlink(),'symlink disallowed: '+p.relative_to(root).as_posix())
    manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
    rows=manifest['files']
    listed={r['path'] for r in rows}
    require(len(listed)==len(rows),'duplicate manifest paths')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==listed|{'PUBLICATION_MANIFEST.json'},'publication file-set mismatch')
    for row in rows:
        path=PurePosixPath(row['path'])
        require(not path.is_absolute() and '..' not in path.parts,'unsafe path')
        data=(root/row['path']).read_bytes()
        require(len(data)==row['bytes'],'byte-count mismatch: '+row['path'])
        require(digest(data)==row['sha256'],'hash mismatch: '+row['path'])
    frozen=(root/'FREEZE_MANIFEST.json').read_bytes()
    require(digest(frozen)==AUTHOR_MANIFEST,'author manifest changed')
    author=json.loads(frozen)
    require(len(author['files'])==8,'author count')
    for row in author['files']:
        data=(root/'packet'/row['path']).read_bytes()
        require(len(data)==row['bytes'] and digest(data)==row['sha256'],'author changed: '+row['path'])
    sums=''.join(r['sha256']+'  packet/'+r['path']+'\n' for r in author['files'])
    sums+=AUTHOR_MANIFEST+'  FREEZE_MANIFEST.json\n'
    require((root/'SHA256SUMS').read_text()==sums,'frozen checksum list changed')
    audit=root/'independent-audit'
    require(digest((audit/'AUDIT_MANIFEST.json').read_bytes())==AUDIT_MANIFEST,'audit manifest changed')
    require((audit/'AUDITED_INPUTS.json').read_bytes()==frozen,'audit input binding')
    proc=subprocess.run([sys.executable,'-I',str(audit/'verify_audit.py')],check=True,capture_output=True,text=True)
    result=json.loads(proc.stdout)
    require(result['status']=='PASS','audit replay')
    require(result['author_assertions']==5859 and result['independent_assertions']==13323,'control counts')
    direct=subprocess.run([sys.executable,'-I',str(root/'packet/verify.py')],check=True,capture_output=True,text=True)
    require(json.loads(direct.stdout)['assertions']==5859,'final-layout author replay')
    require(json.loads((root/'packet/result.json').read_text())['status']=='unsolved','target disposition')
    print(json.dumps({'status':'PASS','publication_files':len(actual),'author_assertions':5859,
                      'independent_assertions':13323,'publication_manifest_sha256':digest((root/'PUBLICATION_MANIFEST.json').read_bytes()),
                      'author_manifest_sha256':AUTHOR_MANIFEST,'audit_manifest_sha256':AUDIT_MANIFEST,
                      'target_status':'unsolved','scope':'Exact byte identity and finite controls; full mathematical target remains unresolved.'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
