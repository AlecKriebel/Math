#!/usr/bin/env python3
"""Check the standalone audit inventory, and optionally reject six mutations."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import tempfile

EXPECTED={'AUDIT_REPORT.md','README.md','audit_result.json','author_replay.json',
          'dataset_metadata_check.json','independent_results.json','source_byte_checks.json',
          'source_review.json','verify_audit_manifest.py','verify_independent.py'}

def check(root):
    root=Path(root)
    if not root.is_dir() or root.is_symlink(): raise ValueError('invalid root')
    if {p.name for p in root.iterdir()} != EXPECTED|{'manifest.json'}: raise ValueError('path set mismatch')
    if any(p.is_symlink() or not p.is_file() for p in root.iterdir()): raise ValueError('nonregular member')
    entries=json.loads((root/'manifest.json').read_text())['files']
    names=[e['path'] for e in entries]
    if len(names)!=len(EXPECTED) or set(names)!=EXPECTED: raise ValueError('manifest inventory mismatch')
    for e in entries:
        b=(root/e['path']).read_bytes()
        if len(b)!=e['bytes'] or sha256(b).hexdigest()!=e['sha256']: raise ValueError('content mismatch')
    return len(entries)

def mutations(root):
    cases=('edit','omit','extra','symlink','duplicate','traversal')
    for case in cases:
        with tempfile.TemporaryDirectory() as tmp:
            dst=Path(tmp)/'packet';shutil.copytree(root,dst)
            p=dst/'AUDIT_REPORT.md'
            if case=='edit': p.write_bytes(p.read_bytes()+b'altered')
            elif case=='omit': p.unlink()
            elif case=='extra': (dst/'unexpected.txt').write_text('extra')
            elif case=='symlink': p.unlink();p.symlink_to(root/'AUDIT_REPORT.md')
            else:
                f=dst/'manifest.json';m=json.loads(f.read_text())
                if case=='duplicate':m['files'].append(m['files'][0])
                else:m['files'][0]['path']='../outside'
                f.write_text(json.dumps(m))
            try:check(dst)
            except (ValueError,KeyError,TypeError):pass
            else:raise ValueError('mutation accepted: '+case)
    return len(cases)

def main():
    p=argparse.ArgumentParser();p.add_argument('--selftest',action='store_true');a=p.parse_args()
    root=Path(__file__).resolve().parent
    result={'status':'PASS_AUDIT_INTEGRITY','bound_files':check(root)}
    if a.selftest:result['rejected_mutations']=mutations(root)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
