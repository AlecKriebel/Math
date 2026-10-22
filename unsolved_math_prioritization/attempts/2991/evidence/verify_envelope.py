#!/usr/bin/env python3
"""Verify the complete packet against an externally obtained envelope SHA-256.

Usage: python verify_envelope.py PACKET_DIRECTORY EXPECTED_ENVELOPE_SHA256
Read-only; all checks remain active under -O and -OO.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet',type=Path)
    parser.add_argument('expected_sha256')
    args=parser.parse_args()
    root=args.packet.resolve()
    need(re.fullmatch('[0-9a-f]{64}',args.expected_sha256) is not None, 'invalid trusted digest')
    envelope=root/'PUBLICATION_ENVELOPE.json'
    need(envelope.is_file() and not envelope.is_symlink(),'missing or symlinked envelope')
    raw=envelope.read_bytes()
    need(digest(raw)==args.expected_sha256,'trusted envelope digest mismatch')
    manifest=json.loads(raw)
    files=manifest['files']
    names=[entry['path'] for entry in files]
    need(len(names)==len(set(names)),'duplicate manifest path')
    for p in root.rglob('*'):
        need(not p.is_symlink(),'packet contains a symlink')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual==set(names)|{'PUBLICATION_ENVELOPE.json'},'packet member set mismatch')
    for entry in files:
        p=(root/entry['path']).resolve()
        need(p.is_relative_to(root) and p.is_file(),'invalid packet member path')
        raw=p.read_bytes()
        need(len(raw)==entry['bytes'] and digest(raw)==entry['sha256'],
             'packet member binding mismatch: '+entry['path'])
    print(json.dumps({'status':'pass','files_bound':len(files),'envelope_sha256':args.expected_sha256,
                      'optimization':sys.flags.optimize,'read_only':True},sort_keys=True))

if __name__=='__main__':
    main()
