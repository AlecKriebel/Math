#!/usr/bin/env python3
"""Validate this public audit against a separately trusted external manifest.

This checks exact packaging, original acceptance pins and author verifier replay.
It neither proves the mathematics nor fetches or inspects scholarly sources.
Usage: python replay.py AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json
"""
import hashlib
import json
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

AUTHOR_ZIP = 'STABLE_PSEUDOISOTOPY_2950_AUTHOR_SAFE_FREEZE.zip'
AUTHOR_MANIFEST = 'STABLE_PSEUDOISOTOPY_2950_AUTHOR_EXTERNAL_MANIFEST.json'
AUTHOR_PINS = {
    AUTHOR_ZIP: (11204, 'c49cd7cd07b7691f1504c99cb6e8bfa03f27c00fe94171b0730e1051a718d556'),
    AUTHOR_MANIFEST: (1632, '8159de4db930160353ee17c2e01ecf82d51f75a7389e3b06d771a5d98f219198'),
}
EXPECTED = {AUTHOR_ZIP, AUTHOR_MANIFEST, 'README.md', 'AUDIT.md', 'ACCEPTANCE.json',
            'SOURCE_INSPECTION.json', 'SOURCE_RETRIEVAL.json', 'SOURCE_PIN_RESULTS.json',
            'HISTORY_REVIEW.json', 'verify_sources.py', 'replay.py', 'test_integrity.py',
            'INTEGRITY_TEST_RESULTS.json'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unique(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def parse(raw):
    return json.loads(raw, object_pairs_hook=unique)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def validate(zip_path, manifest_path):
    zpath, mpath = Path(zip_path), Path(manifest_path)
    require(zpath.is_file() and not zpath.is_symlink(), 'unsafe archive path')
    require(mpath.is_file() and not mpath.is_symlink(), 'unsafe manifest path')
    raw = zpath.read_bytes()
    require(0 < len(raw) < 2_000_000, 'archive bound')
    manifest = parse(mpath.read_bytes())
    require(set(manifest) == {'schema', 'problem_id', 'archive', 'files', 'claims'}, 'manifest fields')
    require(manifest['schema'] == 'stable-pseudoisotopy-2950-independent-audit-v1', 'schema')
    require(type(manifest['problem_id']) is int and manifest['problem_id'] == 2950, 'identity')
    require(manifest['claims'] == {'decision': 'ACCEPT_ORIGINAL_SCOPED_PARTIAL', 'approaches_used': 4,
            'full_solution': False, 'formal_proof_check': False, 'source_contents_included': False}, 'claims')
    archive = manifest['archive']
    require(set(archive) == {'name', 'bytes', 'sha256'}, 'archive fields')
    require(archive['name'] == zpath.name and type(archive['bytes']) is int and
            archive['bytes'] == len(raw) and archive['sha256'] == sha(raw), 'archive pin')
    require(type(manifest['files']) is list and len(manifest['files']) == len(EXPECTED), 'inventory length')
    inventory = {}
    for row in manifest['files']:
        require(set(row) == {'name', 'bytes', 'sha256'}, 'member fields')
        name = row['name']
        require(type(name) is str and name in EXPECTED and name not in inventory, 'member name')
        require(type(row['bytes']) is int and 0 < row['bytes'] < 1_000_000, 'member bound')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'member hash')
        inventory[name] = row
    require(set(inventory) == EXPECTED, 'inventory set')
    payloads = {}
    with ZipFile(zpath) as archive:
        require(len(archive.namelist()) == len(EXPECTED) and set(archive.namelist()) == EXPECTED, 'ZIP inventory')
        for info in archive.infolist():
            mode = info.external_attr >> 16
            require(not info.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG), 'nonregular member')
            require(not (info.flag_bits & 1), 'encrypted member')
            row = inventory[info.filename]
            require(info.file_size == row['bytes'], 'member size')
            data = archive.read(info)
            require(sha(data) == row['sha256'], 'member digest')
            if not info.filename.endswith('.zip'):
                data.decode('utf-8')
            if info.filename.endswith('.json'):
                parse(data)
            payloads[info.filename] = data
    for name, pin in AUTHOR_PINS.items():
        require((len(payloads[name]), sha(payloads[name])) == pin, 'original acceptance pin')
    acceptance = parse(payloads['ACCEPTANCE.json'])
    require(acceptance['decision'] == 'ACCEPT_ORIGINAL_SCOPED_PARTIAL' and
            acceptance['status'] == 'unsolved' and acceptance['problem_id'] == 2950 and
            acceptance['problem_number'] == 'KP-4.74' and acceptance['rank'] == 921, 'acceptance disposition')
    require(acceptance['approaches_used'] == 4 and acceptance['approach_limit'] == 5 and
            acceptance['full_solution_claim'] is False and acceptance['novelty_claim'] is False and
            acceptance['formal_proof_check'] is False and acceptance['repair_required'] is False and
            acceptance['original_members_unchanged'] is True, 'acceptance scope')
    for name, pin in AUTHOR_PINS.items():
        row = acceptance['accepted_inputs'][name]
        require((row['bytes'], row['sha256']) == pin, 'acceptance input record')
    with tempfile.TemporaryDirectory(prefix='stable-pseudoisotopy-replay-') as temp:
        root = Path(temp)
        for name in AUTHOR_PINS:
            (root / name).write_bytes(payloads[name])
        with ZipFile(root / AUTHOR_ZIP) as inner:
            checker = inner.read('verify_packet.py')
        require(sha(checker) == '2c4ad1cdce0521a486fa3548edc49668b71244bdf5e1bb6b846eb2c5d9bbd54d', 'author checker pin')
        (root / 'verify_packet.py').write_bytes(checker)
        command = [sys.executable] + (['-O'] if sys.flags.optimize else []) + [str(root / 'verify_packet.py'), str(root / AUTHOR_ZIP), str(root / AUTHOR_MANIFEST)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        require(result.returncode == 0, 'author replay failed: ' + result.stderr)
        require(parse(result.stdout) == {'result': 'PASS', 'files': 8, 'scope': 'archive_integrity_only'}, 'author replay output')
    return {'result': 'PASS', 'audit_members': len(EXPECTED), 'author_members': 8,
            'accepted_original_exact': True, 'optimized': bool(sys.flags.optimize),
            'scope': 'packaging_and_pinned_acceptance_only', 'mathematical_proof_check': False}

if __name__ == '__main__':
    try:
        require(len(sys.argv) == 3, 'usage: replay.py AUDIT.zip AUDIT_EXTERNAL_MANIFEST.json')
        print(json.dumps(validate(sys.argv[1], sys.argv[2]), sort_keys=True))
    except Exception as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
