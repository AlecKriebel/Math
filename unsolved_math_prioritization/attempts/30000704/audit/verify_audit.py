#!/usr/bin/env python3
"""Verify portable audit inventory and its exact frozen-author binding."""
import hashlib,json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent
def digest(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check_tree(folder,expected,excluded=()):
    for p in folder.rglob('*'):
        if p.is_symlink(): raise SystemExit('Symlink rejected: '+str(p.relative_to(folder)))
    actual={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}-set(excluded)
    if actual!=set(expected): raise SystemExit('File inventory mismatch')
    for rel,want in expected.items():
        q=pathlib.PurePosixPath(rel)
        if q.is_absolute() or '..' in q.parts: raise SystemExit('Unsafe manifest path')
        if digest(folder/rel)!=want: raise SystemExit('Digest mismatch: '+rel)
manifest=json.loads((root/'SHA256SUMS.json').read_text())
check_tree(root,manifest['files'],['SHA256SUMS.json'])
if len(sys.argv)!=2: raise SystemExit('Usage: python3 verify_audit.py ORIGINAL_SAFE_DIRECTORY')
author=pathlib.Path(sys.argv[1]).resolve()
binding=json.loads((root/'BINDING.json').read_text())
m=binding['original_manifest']
if digest(author/m['filename'])!={k:m[k] for k in ['bytes','sha256']}: raise SystemExit('Wrong original manifest')
if json.loads((author/m['filename']).read_text())['files']!=binding['original_files']: raise SystemExit('Original manifest content mismatch')
check_tree(author,binding['original_files'],[m['filename']])
for command,expected,count in [([sys.executable,str(author/'controls/verify.py')],root/'AUTHOR_CONTROL_REPLAY.json',22),([sys.executable,str(root/'controls/adversarial.py')],root/'ADVERSARIAL_RESULTS.json',27)]:
    output=subprocess.check_output(command)
    if output!=expected.read_bytes(): raise SystemExit('Control output changed: '+expected.name)
    data=json.loads(output)
    if data['count']!=count or not all(c['passed'] for c in data['checks']): raise SystemExit('Failed controls')
if (root/'AUTHOR_CONTROL_REPLAY.json').read_bytes()!=(author/'CONTROL_RESULTS.json').read_bytes(): raise SystemExit('Author replay mismatch')
print(json.dumps({'status':'PASS','original_files_checked':len(binding['original_files']),'audit_files_checked':len(manifest['files']),'original_controls':22,'independent_controls':27,'originals_unchanged':True},sort_keys=True))
