#!/usr/bin/env python3
"""Offline byte-integrity validator; not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
FILES={'LITERATURE_DISPROOF.md', 'ACCEPTANCE.md', 'verify_package.py', 'README.md', 'PUBLIC_SOURCES.json', 'PROVENANCE.json', 'MANIFEST.json'}
SOURCE_HASHES=json.loads('{"ACCEPTANCE.md": {"source_name": "ACCEPTANCE.md", "original": {"bytes": 3942, "sha256": "9bbca4856cf3565d72446135e6ebb1dfa40eb73601976606f7e1bb9961123af6"}, "frozen": {"bytes": 3942, "sha256": "9bbca4856cf3565d72446135e6ebb1dfa40eb73601976606f7e1bb9961123af6"}, "editorial_changes": []}}')
INPUT_RECEIPTS=json.loads('{"ACCEPTANCE.md": {"bytes": 3942, "sha256": "9bbca4856cf3565d72446135e6ebb1dfa40eb73601976606f7e1bb9961123af6"}, "GATE.md": {"bytes": 4217, "sha256": "39c388a7306fb6ba6c3237c3c6ae643908b0d803a0a4908fc36a43e758921236"}, "SOURCE_METADATA.json": {"bytes": 2378, "sha256": "6c9ecdbba4da15469c723e590f44b6627135e86553a337a5985ed122989ed6a3"}}')

def fail(message):
    raise ValueError(message)

def inventory(root):
    if not stat.S_ISDIR(root.lstat().st_mode): fail('root is not a real directory')
    found=set(); bad=[]
    def walk(directory,prefix=''):
        with os.scandir(directory) as it:
            entries=sorted(it,key=lambda e:e.name)
        for entry in entries:
            relative=prefix+entry.name; st=entry.stat(follow_symlinks=False)
            found.add(relative)
            if stat.S_ISDIR(st.st_mode):
                bad.append(relative+': directory prohibited')
                walk(Path(directory)/entry.name,relative+'/')
            elif not stat.S_ISREG(st.st_mode) or st.st_nlink!=1:
                bad.append(relative+': nonregular, symlink, or hardlink prohibited')
    walk(root)
    if bad or found!=FILES: fail('inventory rejected: '+repr({'unsafe':bad,'extra':sorted(found-FILES),'missing':sorted(FILES-found)}))

def read_regular(path):
    # No following symlinks at the final component; recheck type after open.
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        st=os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1:fail('unsafe read target')
        with os.fdopen(fd,'rb',closefd=False) as stream:return stream.read()
    finally:os.close(fd)

def rec(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def validate(root,receipt_path):
    inventory(root) # Complete recursive inventory before all package payload reads.
    if receipt_path.absolute().is_relative_to(root.absolute()):fail('receipt must be external')
    receipt=json.loads(read_regular(receipt_path))
    manifest_bytes=read_regular(root/'MANIFEST.json')
    if rec(manifest_bytes)!=receipt['manifest']:fail('external manifest anchor mismatch')
    if rec(read_regular(root/'verify_package.py'))!=receipt['validator']:fail('external validator anchor mismatch')
    manifest=json.loads(manifest_bytes)
    if set(manifest)!= {'row','problem_id','status','files'}:fail('manifest schema mismatch')
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1884,10400211,'already_solved'):fail('target or status mismatch')
    if set(manifest['files'])!=FILES-{'MANIFEST.json'}:fail('manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        if rec(read_regular(root/name))!=wanted:fail('content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    if provenance['source_artifacts']!=SOURCE_HASHES:fail('provenance mismatch')
    if provenance['input_receipts']!=INPUT_RECEIPTS:fail('input provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        data=read_regular(root/name)
        if rec(data)!=wanted['frozen']:fail('frozen source mismatch: '+name)
        for before,after in reversed(wanted['editorial_changes']):
            if data.count(after.encode())!=1:fail('editorial inverse ambiguity: '+name)
            data=data.replace(after.encode(),before.encode())
        if rec(data)!=wanted['original']:fail('exact original provenance mismatch: '+name)
    if receipt['row']!=1884 or receipt['problem_id']!=10400211:fail('receipt target mismatch')
    print('PASS: exact source provenance, external anchors, recursive inventory, and all payload hashes; literature disproof already_solved/1; analytic/source acceptance, not an executable mathematical proof.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
