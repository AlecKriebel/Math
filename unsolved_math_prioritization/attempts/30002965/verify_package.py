#!/usr/bin/env python3
"""Offline byte-integrity validator; not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
FILES={'EDITORIAL_DELTA.md','INDEPENDENT_REVIEW.md','SOURCE_GATE.md','PUBLIC_VERIFICATION.json','README.md','PROVENANCE.json','MANIFEST.json','verify_package.py'}
SOURCE_HASHES=json.loads('{"SOURCE_GATE.md": {"source_name": "AUTHOR_GATE.md", "original": {"bytes": 4119, "sha256": "f6c9b8cf9fe92e5f71431cf1f78f9b2291de8deb75db2889100a613e0992e97a"}, "frozen": {"bytes": 4345, "sha256": "c8c84f54b449b27f1e7524af51aa56840d8cae968b8cb39bf5c3f3696bb11457"}, "editorial_changes": [["Proposition 2.6 gives vol(Cut(suspension G))", "The unnumbered covariance-map identity following Definition 2.5 (Section 2, PDF page 5) gives vol(Cut(suspension G))"], ["subject to independent mathematical audit.", "accepted by the accompanying independent mathematical audit."], ["Thus both the significant-improvement and nontrivial-lower-bound requests are met.", "Thus the asymptotic significant-improvement and nontrivial-lower-bound alternatives are met. The new upper bound is weaker at n=2,3,4; use min(Q_n, U_n), where U_n=2^(-r-d)V_(n+1), for a uniformly no-worse upper bound."]]}, "INDEPENDENT_REVIEW.md": {"source_name": "INDEPENDENT_MATHEMATICAL_AUDIT.md", "original": {"bytes": 6840, "sha256": "d48a6c48e14b87ed5ac04e788608b3b0ec7daf2b4a0d3dd794578e3dacd429dc"}, "frozen": {"bytes": 6840, "sha256": "d48a6c48e14b87ed5ac04e788608b3b0ec7daf2b4a0d3dd794578e3dacd429dc"}, "editorial_changes": []}, "PUBLIC_VERIFICATION.json": {"source_name": "public_metadata.json", "original": {"bytes": 1510, "sha256": "c20759c7e47cd28d3a32c6f29f61e7aa024d1c6d8c52a2dfa0e7b4bd74227f3a"}, "frozen": {"bytes": 1578, "sha256": "69a9a68ff94442f9f4de31a3d73ba1d1b1c3190f61f1c6c3cc248d5598ce803f"}, "editorial_changes": [["Proposition 2.6, elliptope recurrence", "unnumbered covariance-map identity following Definition 2.5 (Section 2, PDF page 5), elliptope recurrence"]]}}')

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
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1883,30002965,'already_solved'):fail('target or status mismatch')
    if set(manifest['files'])!=FILES-{'MANIFEST.json'}:fail('manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        if rec(read_regular(root/name))!=wanted:fail('content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    if provenance['source_artifacts']!=SOURCE_HASHES:fail('provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        data=read_regular(root/name)
        if rec(data)!=wanted['frozen']:fail('frozen source mismatch: '+name)
        for before,after in reversed(wanted['editorial_changes']):
            if data.count(after.encode())!=1:fail('editorial inverse ambiguity: '+name)
            data=data.replace(after.encode(),before.encode())
        if rec(data)!=wanted['original']:fail('exact original provenance mismatch: '+name)
    if receipt['row']!=1883 or receipt['problem_id']!=30002965:fail('receipt target mismatch')
    print('PASS: exact source provenance, external anchors, recursive inventory, and all payload hashes; analytic mathematics only; good-bounds alternative already_solved/1; exact general volume not claimed.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
