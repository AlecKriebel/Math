#!/usr/bin/env python3
"""Strict byte/scope verifier, not a mathematical theorem checker."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

EXPECTED = {
    'README.md','PROOF.md','APPROACH_LOG.md','SOURCE_STATUS.md',
    'source_verification.json','verify_examples.py','example_results.json',
    'verify_packet.py'
}


def verify(root, replay=True):
    root=Path(root)
    entries={p.name for p in root.iterdir()}
    if entries != EXPECTED | {'MANIFEST.json'}:
        raise ValueError('Top-level path set differs from the exact allowlist')
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file():
            raise ValueError('Symlink or non-file entry: '+p.name)
    m=json.loads((root/'MANIFEST.json').read_text())
    if set(m) != {'schema','problem_id','status','files'}:
        raise ValueError('Manifest schema mismatch')
    if m['schema'] != 1 or m['problem_id'] != '30001678' or m['status'] != 'unresolved_scoped_partials':
        raise ValueError('Manifest identity or status mismatch')
    if set(m['files']) != EXPECTED:
        raise ValueError('Manifest file set mismatch')
    for name,rec in m['files'].items():
        if Path(name).name != name or name in ('.','..'):
            raise ValueError('Unsafe relative name')
        if set(rec) != {'bytes','sha256'}:
            raise ValueError('File entry schema mismatch')
        b=(root/name).read_bytes()
        if len(b) != rec['bytes'] or hashlib.sha256(b).hexdigest() != rec['sha256']:
            raise ValueError('Size or SHA-256 mismatch: '+name)
    if replay:
        result=subprocess.run([sys.executable,'-B',str(root/'verify_examples.py')],
                              cwd=root,capture_output=True,check=True)
        if result.stderr or result.stdout != (root/'example_results.json').read_bytes():
            raise ValueError('Example replay differs from stored exact stdout')
    return m


def self_test(root):
    cases=('changed','missing','extra','nested_extra','symlink','traversal','manifest_omission')
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='perfect-product-packet-') as tmp:
            copy=Path(tmp)/'packet'
            shutil.copytree(root,copy)
            if case=='changed':
                with (copy/'PROOF.md').open('ab') as f: f.write(b'\nchanged\n')
            elif case=='missing': (copy/'PROOF.md').unlink()
            elif case=='extra': (copy/'unlisted.txt').write_text('unlisted')
            elif case=='nested_extra':
                (copy/'unlisted').mkdir(); (copy/'unlisted'/'record.txt').write_text('unlisted')
            elif case=='symlink':
                (copy/'README.md').unlink(); (copy/'README.md').symlink_to('PROOF.md')
            else:
                p=copy/'MANIFEST.json';m=json.loads(p.read_text())
                rec=m['files'].pop('README.md')
                if case=='traversal': m['files']['../README.md']=rec
                p.write_text(json.dumps(m))
            try: verify(copy,replay=False)
            except (ValueError,OSError,KeyError,json.JSONDecodeError): pass
            else: raise AssertionError('Negative control was accepted: '+case)
    return list(cases)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    verify(root)
    rejected=self_test(root) if args.self_test else []
    print(json.dumps({
        'result':'PASS_PACKET_INTEGRITY_AND_EXAMPLE_REPLAY',
        'hashed_payload_files':len(EXPECTED),
        'total_packet_files':len(EXPECTED)+1,
        'exact_example_assertions':json.loads((root/'example_results.json').read_text())['total_assertions'],
        'rejected_mutations':rejected,
        'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest(),
        'qualification':'Integrity and example controls only; no independent mathematical audit or source resolution implied.'
    },indent=2,sort_keys=True))

if __name__=='__main__': main()
