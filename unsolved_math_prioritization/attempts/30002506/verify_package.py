#!/usr/bin/env python3
"""Offline byte-integrity validator; not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
FILES={'RESEARCH_ATTEMPT.md','INDEPENDENT_REVIEW.md','SOURCE_GATE.md','PUBLIC_VERIFICATION.json','README.md','PROVENANCE.json','MANIFEST.json','verify_package.py'}
SOURCE_HASHES={'RESEARCH_ATTEMPT.md': {'bytes': 11844, 'sha256': 'b2a6f3676810818eeded0d9e1af68415512cbd61dc43ab3ee676b21f037dbdaf'}, 'INDEPENDENT_REVIEW.md': {'bytes': 6348, 'sha256': 'd0565fd917f36f47df358045192f899757a2c72f67b6ccd162d6fb0460d089fe'}, 'SOURCE_GATE.md': {'bytes': 3651, 'sha256': 'a01fd80aed2d0ac6d27bd89a90a229f4f16d74901ffccbcaf8c1db5eee3004d0'}, 'PUBLIC_VERIFICATION.json': {'bytes': 1748, 'sha256': '35cd3132f329d73c0ccce93978e8d1163a94d0f1a85a0c93508932251550c836'}}

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
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1882,30002506,'UNSOLVED'):fail('target or status mismatch')
    if set(manifest['files'])!=FILES-{'MANIFEST.json'}:fail('manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        if rec(read_regular(root/name))!=wanted:fail('content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    if provenance['source_artifacts']!=SOURCE_HASHES:fail('provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        if rec(read_regular(root/name))!=wanted:fail('exact source mismatch: '+name)
    if receipt['row']!=1882 or receipt['problem_id']!=30002506:fail('receipt target mismatch')
    print('PASS: exact source provenance, external anchors, recursive inventory, and all payload hashes; analytic mathematics only; general UNSOLVED.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
