#!/usr/bin/env python3
"""Read-only byte-integrity check of this reviewer's allowlist and private inventory."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent

def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe_path(relative):
    p = BASE / relative
    if p.is_symlink() or not p.resolve().is_relative_to(BASE) or not p.is_file():
        raise ValueError('Unsafe/missing path: ' + relative)
    return p

def main():
    seal = json.loads((BASE / 'FINAL_SEAL.json').read_text())
    public = json.loads((BASE / 'PUBLIC_FILES.json').read_text())['files']
    if len(public) != len(set(public)):
        raise ValueError('Duplicate allowlist entry')
    if any(p.startswith('private_sources/') or '..' in Path(p).parts for p in public):
        raise ValueError('Foreign source or escaping path in public allowlist')
    expected = set(public) - {'FINAL_SEAL.json'}
    if set(seal['public_payload']) != expected:
        raise ValueError('Public payload/allowlist mismatch')
    for relative, wanted in seal['public_payload'].items():
        if digest(safe_path(relative)) != wanted:
            raise ValueError('Public digest mismatch: ' + relative)
    inventory = json.loads((BASE / 'receipts/PRIVATE_SOURCE_INVENTORY.json').read_text())
    actual_private = {str(p.relative_to(BASE)) for p in (BASE / 'private_sources').rglob('*') if p.is_file()}
    if actual_private != set(inventory['files']):
        raise ValueError('Private source inventory incomplete')
    for relative, wanted in inventory['files'].items():
        if digest(safe_path(relative)) != wanted:
            raise ValueError('Private digest mismatch: ' + relative)
    own_files = {str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(BASE / 'private_sources') and '__pycache__' not in p.parts}
    if own_files != set(public):
        raise ValueError('Own files not completely positively allowlisted')
    verdict = json.loads((BASE / 'VERDICT.json').read_text())
    for key in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']:
        if type(verdict[key]) is not int or verdict[key] < 0:
            raise ValueError('Finding must be a nonnegative typed integer: ' + key)
        if verdict[key] != len(verdict[key + '_details']):
            raise ValueError('Count/detail mismatch: ' + key)
    checkpoint = json.loads((BASE / 'receipts/INITIAL_PRIORITY_SEAL.json').read_text())
    if digest(BASE / 'INITIAL_PRIORITY.md')['sha256'] != checkpoint['sha256']:
        raise ValueError('Independent initial checkpoint changed')
    return {
        'integrity_verified': True,
        'public_file_count': len(public),
        'private_file_count': len(actual_private),
        'final_seal_sha256': digest(BASE / 'FINAL_SEAL.json')['sha256'],
        'scope': 'Byte integrity and schema only; no mathematical acceptance, priority approval, or status mutation',
    }

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
