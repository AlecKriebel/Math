#!/usr/bin/env python3
"""Validate a pinned packet manifest and ZIP, not mathematical correctness.

Usage: python verify_packet.py PACKET.zip EXTERNAL_MANIFEST.json
The manifest must come from a trusted, separately pinned source.
"""
import hashlib
import json
import re
import stat
import sys
from pathlib import Path
from zipfile import ZipFile

EXPECTED = {
    'README.md', 'MATHEMATICAL_REPORT.md', 'APPROACH_LOG.md',
    'STATUS.json', 'SOURCE_AUDIT.json', 'PROVENANCE.json',
    'verify_packet.py', 'INTEGRITY_TESTS.json',
}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def parse_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def validate(zip_path, manifest_path):
    raw = Path(zip_path).read_bytes()
    require(len(raw) <= 2_000_000, 'oversized archive')
    m = parse_json(Path(manifest_path).read_text())
    require(set(m) == {'schema', 'problem_id', 'archive', 'files', 'claims'}, 'manifest keys')
    require(m['schema'] == 'stable-pseudoisotopy-2950-v1', 'schema mismatch')
    require(type(m['problem_id']) is int and m['problem_id'] == 2950, 'identity mismatch')
    a = m['archive']
    require(set(a) == {'name', 'bytes', 'sha256'}, 'archive metadata keys')
    require(a['name'] == Path(zip_path).name, 'archive name mismatch')
    require(type(a['bytes']) is int and a['bytes'] == len(raw), 'archive byte mismatch')
    require(a['sha256'] == sha(raw), 'archive hash mismatch')
    require(m['claims'] == {'mathematics': 'unsolved_scoped_partial', 'approaches': 4,
                             'formal_proof_check': False, 'source_contents_included': False}, 'claim mismatch')
    require(type(m['files']) is list and len(m['files']) == len(EXPECTED), 'inventory length')
    inventory = {}
    for item in m['files']:
        require(set(item) == {'name', 'bytes', 'sha256'}, 'file metadata keys')
        name = item['name']
        require(type(name) is str and name in EXPECTED and name not in inventory, 'file identity')
        require(type(item['bytes']) is int and 0 < item['bytes'] < 1_000_000, 'file byte bound')
        require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']), 'file hash syntax')
        inventory[name] = item
    require(set(inventory) == EXPECTED, 'manifest inventory mismatch')
    with ZipFile(zip_path) as z:
        names = z.namelist()
        require(len(names) == len(EXPECTED) and set(names) == EXPECTED, 'ZIP inventory mismatch')
        contents = {}
        for info in z.infolist():
            mode = info.external_attr >> 16
            require(not info.is_dir() and not stat.S_ISLNK(mode), 'nonregular archive member')
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), 'nonregular file mode')
            item = inventory[info.filename]
            require(info.file_size == item['bytes'], 'member byte mismatch')
            require(info.flag_bits & 1 == 0, 'encrypted archive member')
            payload = z.read(info.filename)
            require(sha(payload) == item['sha256'], 'member hash mismatch')
            payload.decode('utf-8')
            contents[info.filename] = payload
    status = parse_json(contents['STATUS.json'])
    require(status.get('id') == 2950 and status.get('problem_number') == 'KP-4.74', 'status identity')
    require(status.get('status') == 'unsolved' and status.get('approaches_used') == 4,
            'status disposition')
    require(status.get('full_solution_claim') is False and status.get('novelty_claim') is False,
            'unsupported solution or novelty claim')
    require(status.get('geometric_counterexample_constructed') is False, 'unsupported construction')
    return {'result': 'PASS', 'files': len(EXPECTED), 'scope': 'archive_integrity_only'}

if __name__ == '__main__':
    try:
        require(len(sys.argv) == 3, 'usage: verify_packet.py PACKET.zip EXTERNAL_MANIFEST.json')
        print(json.dumps(validate(sys.argv[1], sys.argv[2]), sort_keys=True))
    except Exception as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
