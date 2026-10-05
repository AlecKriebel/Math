#!/usr/bin/env python3
"""Verify audit bytes, bound candidate bytes, and independent finite controls.
Usage: python verify_audit.py PATH_TO_FROZEN_CANDIDATE_DIRECTORY
No source PDFs, private records or network access are required.
This verifier does not mechanically prove the mathematical assertions.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def check_files(root, items, excluded=()):
    names = {item['path'] for item in items}
    actual = {p.name for p in root.iterdir() if p.name not in excluded}
    assert names == actual, (names, actual)
    for item in items:
        assert item['path'] == Path(item['path']).name
        p = root/item['path']
        assert p.is_file() and not p.is_symlink()
        data=p.read_bytes()
        assert len(data)==item['bytes'], item['path']
        assert sha256(data)==item['sha256'], item['path']


def main():
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python verify_audit.py PATH_TO_FROZEN_CANDIDATE_DIRECTORY')
    root=Path(__file__).resolve().parent
    candidate=Path(sys.argv[1]).resolve()
    audit_manifest=json.loads((root/'MANIFEST.json').read_text())
    check_files(root,audit_manifest['files'],excluded=('MANIFEST.json',))
    binding=json.loads((root/'BINDING.json').read_text())
    check_files(candidate,binding['candidate_all_files'])
    result=subprocess.run([sys.executable,str(root/'independent_controls.py')],
                          text=True,capture_output=True,check=True)
    assert json.loads(result.stdout)==json.loads((root/'INDEPENDENT_RESULTS.json').read_text())
    candidate_result=subprocess.run([sys.executable,str(candidate/'verify_packet.py')],
                                    text=True,capture_output=True,check=True)
    assert json.loads(candidate_result.stdout)==binding['candidate_verifier_result']
    check_files(candidate,binding['candidate_all_files'])
    print(json.dumps({'status':'PASS','candidate_files_verified':len(binding['candidate_all_files']),
                      'candidate_payload_bytes':binding['candidate_payload_bytes'],
                      'audit_payload_files_verified':len(audit_manifest['files']),
                      'independent_graphs_checked':1100,
                      'formal_proof_checker':False,
                      'external_theorem_reproved':False},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
