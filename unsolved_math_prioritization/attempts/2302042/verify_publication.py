#!/usr/bin/env python3
"""Portable integrity/replay checks, not a formal proof certificate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent


def need(ok, label):
    if not ok:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key: ' + k)
        d[k] = v
    return d


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def inventory(root, manifest_name):
    m = read_json(root / manifest_name)
    expected = {}
    for row in m['files']:
        name = row['path']
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and name == p.as_posix(), 'unsafe path')
        need(name not in expected, 'duplicate manifest path')
        expected[name] = row
    need(not any(p.is_symlink() for p in root.rglob('*')), 'symlink in packet')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual == set(expected) | {manifest_name}, 'strict inventory mismatch')
    for name, row in expected.items():
        data = (root / name).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'content mismatch: ' + name)
    return len(expected)


def frozen_archive(folder, filename, bytes_expected, hash_expected, manifest_hash, member_count):
    archive = folder / filename
    data = archive.read_bytes()
    need(len(data) == bytes_expected and sha(data) == hash_expected, 'frozen ZIP identity')
    packet = folder / ('safe_output' if folder.name == 'freeze' else 'safe_audit')
    need(sha((packet / 'MANIFEST.json').read_bytes()) == manifest_hash, 'frozen manifest identity')
    inventory(packet, 'MANIFEST.json')
    expected = {p.relative_to(packet).as_posix() for p in packet.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        need(len(names) == len(set(names)) == member_count and set(names) == expected, 'ZIP inventory')
        need(z.testzip() is None, 'ZIP CRC')
        for name in names:
            need(z.read(name) == (packet / name).read_bytes(), 'ZIP member mismatch: ' + name)


def main():
    files = inventory(ROOT, 'PUBLICATION_MANIFEST.json')
    frozen_archive(ROOT / 'freeze', 'asymptotic_ratio_2302042_NEW_FREEZE_20261005.zip',
                   13409, 'f55af0a7d0d909ec90a41158620f8e5304d74646032ef6e1465613f7518f0902',
                   '9a16d1058ebccac239eee2faf033b61437eeeffe83ae178409e2903ae6914320', 8)
    frozen_archive(ROOT / 'independent_audit', 'asymptotic_ratio_2302042_INDEPENDENT_AUDIT_20261005.zip',
                   13309, '6ec84bc419bd972acd7c088c1d08d989158d0ca6c78ed8bb673b223bb613582b',
                   'd1d075ea69ab4f1e03c2ed2acc2b1b1236faecfde0a1ccd9979bf1e50bde6244', 7)
    outputs = []
    for flags in ([], ['-O']):
        run = subprocess.run([sys.executable, *flags,
                              str(ROOT / 'independent_audit/safe_audit/audit_replay.py'),
                              str(ROOT / 'freeze')], capture_output=True, text=True, check=True)
        result = json.loads(run.stdout, object_pairs_hook=unique_object)
        need(result['result'] == 'PASS', 'audit replay')
        need(result == read_json(ROOT / 'independent_audit/safe_audit/REPLAY_RESULTS.json'),
             'frozen replay result reproduction')
        outputs.append(result)
    need(outputs[0] == outputs[1], 'Python mode mismatch')
    print(json.dumps({'result': 'PASS', 'files_verified': files,
                      'strict_inventory': True, 'frozen_archives_verified': 2,
                      'frozen_archive_members_verified': 15,
                      'audit_replay_normal_and_optimized': 'PASS',
                      'exact_checks_per_mode': 2480, 'scope_mutants_per_mode': 8,
                      'additional_scope_checks': 9, 'exact_flux_checks': 2000,
                      'manifest_mutant_types_per_mode': 4,
                      'numeric_results_preserved_not_rerun': True,
                      'original_barsegyan_proof_verified': False,
                      'original_dataset_bytes_verified': False,
                      'analytic_proof_formalized': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
