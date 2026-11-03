#!/usr/bin/env python3
"""Offline byte-integrity validator; not a mathematical certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
FILES={'PUBLIC_SOURCES.json', 'PROVENANCE.json', 'RECOVERY_PUBLIC.md', 'ACCEPTANCE.md', 'README.md', 'INPUT_HASHES.json', 'MANIFEST.json', 'verify_package.py', 'ACCEPTANCE.json'}
SOURCE_HASHES={'ACCEPTANCE.md': {'source_name': 'INDEPENDENT_ACCEPTANCE.md', 'original': {'bytes': 7762, 'sha256': 'e679c47d9509cd7ded47469a3740203d4365ba3a89be608eb5b931d520fb176d'}, 'frozen': {'bytes': 7762, 'sha256': 'e679c47d9509cd7ded47469a3740203d4365ba3a89be608eb5b931d520fb176d'}, 'editorial_changes': []}, 'ACCEPTANCE.json': {'source_name': 'ACCEPTANCE.json', 'original': {'bytes': 1088, 'sha256': '8a9af954857a521de79ab99dc779d4578bd062a15a28b473ec64f622361ced17'}, 'frozen': {'bytes': 1088, 'sha256': '8a9af954857a521de79ab99dc779d4578bd062a15a28b473ec64f622361ced17'}, 'editorial_changes': []}, 'INPUT_HASHES.json': {'source_name': 'INPUT_HASHES.json', 'original': {'bytes': 685, 'sha256': 'cb747656f5909ad41134ba3a9e35a92af884a46adb91e06049b737ebb5cdd036'}, 'frozen': {'bytes': 685, 'sha256': 'cb747656f5909ad41134ba3a9e35a92af884a46adb91e06049b737ebb5cdd036'}, 'editorial_changes': []}, 'RECOVERY_PUBLIC.md': {'source_name': 'SOURCE_GATE.md', 'original': {'bytes': 3332, 'sha256': '0875fb595ab5509cc07ce1fc29218dd458fc0cdc3fb1017588f5fff27fe4db57'}, 'frozen': {'bytes': 3446, 'sha256': 'cfe382dc591d07cde6918912291f7420f6abd9470bcfd9091b44c935c8848eca'}, 'editorial_changes': [['Already solved at the original existential scope; zero new proof attempts (0/5).', 'Already solved at the original existential scope; standard workflow disposition already_solved, Turns 1. This supersedes the recovery bookkeeping value 0/5, not a claim of one new proof attempt.']]}, 'PUBLIC_SOURCES.json': {'source_name': 'SOURCE_METADATA.json', 'original': {'bytes': 981, 'sha256': '18e8476753363c77c5d504806c00d904132aca239db73da112f5112b52d23ff4'}, 'frozen': {'bytes': 977, 'sha256': '06415ece50f43f9a88f28f6383ed48e7fb910f837251582100d446e65cad01f1'}, 'editorial_changes': [['"turns": "0/5"', '"turns": 1']]}}
INPUT_RECEIPTS={'INDEPENDENT_ACCEPTANCE.md': {'bytes': 7762, 'sha256': 'e679c47d9509cd7ded47469a3740203d4365ba3a89be608eb5b931d520fb176d'}, 'ACCEPTANCE.json': {'bytes': 1088, 'sha256': '8a9af954857a521de79ab99dc779d4578bd062a15a28b473ec64f622361ced17'}, 'INPUT_HASHES.json': {'bytes': 685, 'sha256': 'cb747656f5909ad41134ba3a9e35a92af884a46adb91e06049b737ebb5cdd036'}, 'SOURCE_GATE.md': {'bytes': 3332, 'sha256': '0875fb595ab5509cc07ce1fc29218dd458fc0cdc3fb1017588f5fff27fe4db57'}, 'SOURCE_METADATA.json': {'bytes': 981, 'sha256': '18e8476753363c77c5d504806c00d904132aca239db73da112f5112b52d23ff4'}}

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
    if (manifest['row'],manifest['problem_id'],manifest['status'])!=(1886,11000031,'already_solved'):fail('target or status mismatch')
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
    if receipt['row']!=1886 or receipt['problem_id']!=11000031:fail('receipt target mismatch')
    print('PASS: exact source provenance, external anchors, recursive inventory, and all payload hashes; ALREADY SOLVED (credited prior result), workflow Turns 1; analytic dependency audit acceptance, not a mathematical certificate.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
