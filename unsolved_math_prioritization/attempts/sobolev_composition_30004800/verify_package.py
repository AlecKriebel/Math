#!/usr/bin/env python3
"""Offline artifact-integrity checker, not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
def deny_network(event,args):
    if event.startswith("socket."): raise RuntimeError("Network prohibited")
sys.addaudithook(deny_network)
FILES={'MANIFEST.json', 'SOURCE_GATE.md', 'README.md', 'INDEPENDENT_REVIEW.md', 'RETRIEVAL_MANIFEST.json', 'verify_package.py', 'PROVENANCE.json', 'ACCEPTANCE_REPORT.md'}
SOURCE_HASHES={'ACCEPTANCE_REPORT.md': {'source_name': 'authored/ACCEPTANCE_REPORT.md', 'original': {'bytes': 6345, 'sha256': '1b99d41be2f468d5cf15171c40b1480f918e46d4a09837955219156956824263'}, 'frozen': {'bytes': 6345, 'sha256': '1b99d41be2f468d5cf15171c40b1480f918e46d4a09837955219156956824263'}, 'editorial_changes': []}, 'INDEPENDENT_REVIEW.md': {'source_name': 'authored/INDEPENDENT_REVIEW.md', 'original': {'bytes': 8581, 'sha256': '4e267057c584b575e87a266ef9ee9bae5e690220f92738be3da5822743d2db66'}, 'frozen': {'bytes': 8581, 'sha256': '4e267057c584b575e87a266ef9ee9bae5e690220f92738be3da5822743d2db66'}, 'editorial_changes': []}, 'SOURCE_GATE.md': {'source_name': 'SOURCE_GATE.md', 'original': {'bytes': 3897, 'sha256': 'ea9362b149f7794609338d62807ad84bd7ceaeff090bcf9ea840fe7097d3ce4e'}, 'frozen': {'bytes': 2966, 'sha256': '32ee523c0aec6fc85c3de3ab71783b81d05c9f792db8c15a2357f61536228362'}, 'editorial_changes': ['Removed the entire duplicate and review boundary section, including repository search and private-corpus findings and internal next-action instructions.']}, 'RETRIEVAL_MANIFEST.json': {'source_name': 'RETRIEVAL_MANIFEST.json', 'original': {'bytes': 1702, 'sha256': '0716444344228f17755cbbb0099c6e153a5f4c1177b7b054b6637095c1cebda6'}, 'frozen': {'bytes': 1702, 'sha256': '0716444344228f17755cbbb0099c6e153a5f4c1177b7b054b6637095c1cebda6'}, 'editorial_changes': []}}

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
    if receipt_path.resolve().is_relative_to(root.resolve()):fail('receipt must be external')
    receipt=json.loads(read_regular(receipt_path))
    manifest_bytes=read_regular(root/'MANIFEST.json')
    if rec(manifest_bytes)!=receipt['manifest']:fail('external manifest anchor mismatch')
    if rec(read_regular(root/'verify_package.py'))!=receipt['validator']:fail('external validator anchor mismatch')
    manifest=json.loads(manifest_bytes)
    if set(manifest)!= {'row','problem_id','status','files'}:fail('manifest schema mismatch')
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1888,30004800,'already_solved'):fail('target or status mismatch')
    if set(manifest['files'])!=FILES-{'MANIFEST.json'}:fail('manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        if rec(read_regular(root/name))!=wanted:fail('content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    if provenance['source_artifacts']!=SOURCE_HASHES:fail('source provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        if rec(read_regular(root/name))!=wanted['frozen']:fail('frozen source mismatch: '+name)
    if receipt['row']!=1888 or receipt['problem_id']!=30004800:fail('receipt target mismatch')
    print('PASS: exact inventory, source provenance and external hash anchors. already_solved/1; attributed unrefereed prior solution within full-Fourier real-input scope. Analytic proof-audit integrity, NOT a mathematical certificate.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
