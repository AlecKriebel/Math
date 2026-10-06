#!/usr/bin/env python3
"""Check the exact safe packet against its separately supplied integrity manifest.
This does not verify mathematical claims or establish manifest authenticity.
"""
import hashlib
import json
import pathlib
import stat
import sys
import zipfile

EXPECTED = {'README.md', 'PROOF.md', 'REPORT.md', 'research_log.json',
            'sources.json', 'status.json', 'verification_metadata.json',
            'verify_packet.py'}
MAX_BYTES = 2_000_000

def fail(message):
    raise ValueError(message)

def check(condition, message):
    if not condition:
        fail(message)

def unique(pairs):
    result = {}
    for key, value in pairs:
        check(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result

def parse(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=lambda value: fail('Nonfinite JSON constant'))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    check(__debug__, 'Optimized Python execution is unsupported; run without -O or -OO.')
    check(len(sys.argv) == 3, 'Usage: verify_packet.py DIRECTORY_OR_ZIP EXTERNAL_MANIFEST')
    target, manifest_path = map(pathlib.Path, sys.argv[1:])
    check(not manifest_path.is_symlink(), 'Manifest must not be a symlink')
    mb = manifest_path.read_bytes()
    check(len(mb) <= MAX_BYTES, 'Manifest too large')
    manifest = parse(mb)
    check(manifest.get('schema_version') == 1, 'Manifest schema mismatch')
    check(manifest.get('problem_id') == 2931 and manifest.get('problem_number') == 'KP-4.55', 'Wrong problem')
    check(manifest.get('artifact_scope') == 'authored_analysis_and_public_verification_metadata', 'Unexpected scope')
    entries = manifest.get('files')
    check(isinstance(entries, list), 'Missing manifest entries')
    check(len(entries) == len(EXPECTED), 'Wrong manifest entry count')
    names = [entry.get('path') for entry in entries]
    check(set(names) == EXPECTED and len(set(names)) == len(names), 'Wrong or duplicate paths')
    check(not target.is_symlink(), 'Target must not be a symlink')
    data = {}
    if target.is_dir():
        children = list(target.iterdir())
        check({p.name for p in children} == EXPECTED, 'Unexpected directory contents')
        for child in children:
            check(child.is_file() and not child.is_symlink(), 'Nonregular packet member')
            check(child.stat().st_size <= MAX_BYTES, 'Oversized member')
            data[child.name] = child.read_bytes()
    else:
        blob = target.read_bytes()
        check(len(blob) <= MAX_BYTES, 'Oversized ZIP')
        archive = manifest.get('archive', {})
        check(archive.get('bytes') == len(blob) and archive.get('sha256') == digest(blob), 'ZIP fingerprint mismatch')
        with zipfile.ZipFile(target) as z:
            members = z.infolist()
            check(len(members) == len(EXPECTED), 'Wrong ZIP member count')
            check({m.filename for m in members} == EXPECTED, 'Unexpected ZIP paths')
            check(len({m.filename for m in members}) == len(members), 'Duplicate ZIP path')
            for member in members:
                check(not member.is_dir(), 'ZIP directories not allowed')
                check(member.file_size <= MAX_BYTES, 'Oversized uncompressed member')
                check(not stat.S_ISLNK(member.external_attr >> 16), 'ZIP symlink not allowed')
                check(not (member.flag_bits & 1), 'Encrypted ZIP not allowed')
                data[member.filename] = z.read(member)
    for entry in entries:
        name = entry['path']
        b = data[name]
        check(type(entry.get('bytes')) is int and entry['bytes'] == len(b), 'Byte count mismatch: ' + name)
        check(entry.get('sha256') == digest(b), 'Digest mismatch: ' + name)
        b.decode('utf-8')
    status = parse(data['status.json'])
    check(status.get('id') == 2931 and status.get('problem_number') == 'KP-4.55', 'Status identity mismatch')
    check(status.get('status') == 'stalled_partial', 'Wrong status')
    check(status.get('turns_used') == 5 and status.get('turn_limit') == 5, 'Approach budget mismatch')
    for field in ('full_solution', 'counterexample', 'new_classification_theorem'):
        check(status.get(field) is False, 'Claim boundary changed: ' + field)
    log = parse(data['research_log.json'])
    check(log.get('id') == 2931 and log.get('novelty_claim') is False, 'Research log mismatch')
    check(log.get('mathematical_computation_performed') is False, 'Computation claim changed')
    approaches = log.get('approaches', [])
    check(len(approaches) == 5 and [a.get('turn') for a in approaches] == [1, 2, 3, 4, 5], 'Approach log mismatch')
    metadata = parse(data['verification_metadata.json'])
    check(metadata.get('id') == 2931 and metadata.get('exact_id_unique') is True, 'Verification identity mismatch')
    check(metadata.get('inherited_gate_result') == 'passed_literature_only', 'Gate result mismatch')
    for field in ('source_text_included', 'dataset_contents_included', 'private_material_included'):
        check(metadata.get(field) is False, 'Public scope flag changed: ' + field)
    check(metadata.get('statement_sha256') == '8be9730755fec5ea406c5f1d9c5cd3d50ca13f5d40e307baa2c1cd74e3752263', 'Statement hash mismatch')
    check(metadata.get('record_report_pair_sha256') == '74978e4c1d87ebc102f6be15c3991950f15f85dc1f991004324b483743c1855e', 'Pair hash mismatch')
    datasets = metadata.get('datasets', [])
    expected_ds = [('catalog.json',21735099,'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'),
                   ('problems.json',68931837,'04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf'),
                   ('research_results.json',80334822,'8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b')]
    check(len(datasets) == 3, 'Dataset metadata count mismatch')
    for actual, (label, size, hash_value) in zip(datasets, expected_ds):
        check(actual == {'dataset':label,'bytes':size,'sha256':hash_value,'matched':True}, 'Dataset fingerprint mismatch')
    sources = parse(data['sources.json']).get('sources', [])
    check({s.get('key') for s in sources} == {'K3','KPR','KNR','HH','HN','HU','KNV','KP','HKPR','P'}, 'Source inventory mismatch')
    check(len(sources) == 10, 'Duplicate source entries')
    for source in sources:
        check(source.get('url', '').startswith('https://'), 'Nonpublic source URL')
        n, h = source.get('pdf_bytes'), source.get('pdf_sha256')
        check((n is None and h is None) or (type(n) is int and n > 0 and isinstance(h,str) and len(h) == 64 and all(c in '0123456789abcdef' for c in h)), 'Invalid PDF fingerprint')
    for name, b in data.items():
        if name != 'verify_packet.py':
            for forbidden in (b'/workspace/', b'private_sources/', b'chatgpt.com/c/', b'codex://', b'"background":', b'"created_at":'):
                check(forbidden not in b, 'Disallowed private/corpus marker in ' + name)
    print('INTEGRITY_AND_SCHEMA_PASS: 8 exact members; stalled_partial; no mathematical validation claimed.')

if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, UnicodeError) as error:
        print('REJECTED: ' + str(error), file=sys.stderr)
        sys.exit(2)
