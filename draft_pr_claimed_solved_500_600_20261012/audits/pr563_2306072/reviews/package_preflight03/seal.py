#!/usr/bin/env python3
"""Seal this review's authored top-level outputs, excluding raw/cache data."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
SEAL = ROOT / 'MANIFEST.json'


def inventory():
    result = {}
    for p in sorted(ROOT.iterdir()):
        if p.is_file() and p.name != SEAL.name and p.name != 'SEAL_CHECK.json':
            if p.is_symlink():
                raise RuntimeError('Unexpected authored symlink')
            result[p.name] = {'bytes': p.stat().st_size,
                              'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    return result


if '--verify' in sys.argv:
    seal = json.loads(SEAL.read_text())
    if seal['files'] != inventory():
        raise RuntimeError('Authored review seal mismatch')
    print(json.dumps({'status':'PASS', 'authored_outputs':len(seal['files']),
                      'manifest_sha256':hashlib.sha256(SEAL.read_bytes()).hexdigest()}))
else:
    SEAL.write_text(json.dumps({
        'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope':'Independent package_preflight03 authored outputs only',
        'files':inventory(),
        'exclusions':['MANIFEST.json self','SEAL_CHECK.json dynamic verification receipt',
                      '.cache/ raw renders/extractions/venvs/mutation copies/rebuilds','__pycache__/'],
        'limits':'Integrity is consistency, not formal proof, authenticity, human review, or priority.'
    },indent=2)+'\n')
    print(json.dumps({'status':'SEALED', 'authored_outputs':len(inventory())}))
