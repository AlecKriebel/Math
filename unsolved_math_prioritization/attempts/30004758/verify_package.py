#!/usr/bin/env python3
"""Offline integrity checker, not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
FILES={'MANIFEST.json', 'README.md', 'verify_package.py', 'AUDIT_AND_FIVE_APPROACHES.md', 'INDEPENDENT_ACCEPTANCE.json', 'SOURCE_GATE.md', 'PUBLIC_SOURCE_MANIFEST.json', 'PROVENANCE.json'}
SOURCE_HASHES={'AUDIT_AND_FIVE_APPROACHES.md': {'source_name': 'AUDIT_AND_FIVE_APPROACHES.md', 'original': {'bytes': 14105, 'sha256': 'acd7597cc351e15516db0e30a6c6b9525160e7a6c9a81d567c23ada3e4079519'}, 'frozen': {'bytes': 14105, 'sha256': 'acd7597cc351e15516db0e30a6c6b9525160e7a6c9a81d567c23ada3e4079519'}, 'editorial_changes': []}, 'INDEPENDENT_ACCEPTANCE.json': {'source_name': 'INDEPENDENT_ACCEPTANCE.json', 'original': {'bytes': 10489, 'sha256': '6a550114050e55c7ba473b402a77622700a289dafb3db9258c08d0db283e2981'}, 'frozen': {'bytes': 10489, 'sha256': '6a550114050e55c7ba473b402a77622700a289dafb3db9258c08d0db283e2981'}, 'editorial_changes': []}, 'SOURCE_GATE.md': {'source_name': 'SOURCE_GATE.md', 'original': {'bytes': 4243, 'sha256': 'd736ca7d7460c59730a7c703b336c9b11007b8fd02f0176f2d6e6c17deb0fbbd'}, 'frozen': {'bytes': 3490, 'sha256': 'efc34b3b99936fbf07dbd29b328853a1642b84a423fb1672cf1c3a5df0e0810b'}, 'editorial_changes': ['Removed the quoted original problem sentence; retained authored scope paraphrase and citations.', 'Removed the entire duplicate/repository checks section, including private-corpus and coordination findings.']}, 'PUBLIC_SOURCE_MANIFEST.json': {'source_name': 'PUBLIC_SOURCE_MANIFEST.json', 'original': {'bytes': 783, 'sha256': '3ae9d61141e4a1f6db404aa29474a75ee4a6ca2efaa407af29a52c972f6389df'}, 'frozen': {'bytes': 783, 'sha256': '3ae9d61141e4a1f6db404aa29474a75ee4a6ca2efaa407af29a52c972f6389df'}, 'editorial_changes': []}}

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
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1887,30004758,'partial'):fail('target or status mismatch')
    if set(manifest['files'])!=FILES-{'MANIFEST.json'}:fail('manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        if rec(read_regular(root/name))!=wanted:fail('content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    if provenance['source_artifacts']!=SOURCE_HASHES:fail('source provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        if rec(read_regular(root/name))!=wanted['frozen']:fail('frozen source mismatch: '+name)
    acceptance=json.loads(read_regular(root/'INDEPENDENT_ACCEPTANCE.json'))
    reviewed=acceptance['reviewed_report']
    if {'bytes':reviewed['bytes'],'sha256':reviewed['sha256']}!=SOURCE_HASHES['AUDIT_AND_FIVE_APPROACHES.md']['original']:fail('acceptance binding mismatch')
    if acceptance['decision']!='ACCEPTED_AS_PARTIAL_RESULT':fail('acceptance scope mismatch')
    for flag in ('broad_problem_resolved','novelty_certified','theorem_1_5_refuted'):
        if acceptance['scope'][flag] is not False:fail('invalid scope flag')
    if receipt['row']!=1887 or receipt['problem_id']!=30004758:fail('receipt target mismatch')
    print('PASS: exact inventory, source provenance, acceptance binding and external hash anchors. Five PARTIAL approaches; analytic acceptance integrity, NOT a mathematical certificate; no novelty/full-resolution/theorem-refutation claim.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
