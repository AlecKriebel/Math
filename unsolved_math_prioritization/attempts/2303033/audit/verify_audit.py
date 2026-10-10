#!/usr/bin/env python3
"""Replay pinned authored packages in isolation; no source corpus or network needed."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

BASE = Path(__file__).resolve().parent
PINS = {
    'B_REGULAR_2303033_AUTHOR_SAFE_FREEZE.zip': (11463, 'b440a4b7dfca3b37e477cf121b1bd04938d22c1c42b861c58c84be94903263c3'),
    'B_REGULAR_2303033_AUTHOR_EXTERNAL_MANIFEST.json': (2027, '4affbaf482d62671ea8dbb6931b2cfb1fb39d6a8ec6fa09b7e4cd1044dd6b20d'),
    'B_REGULAR_2303033_DIAGNOSTIC_CORRECTED_EXTERNAL_MANIFEST.json': (2050, '5a78caafba2fb23c32acf2afd92512c3ff0b0810ce6806d13709ac192a2ec7b6'),
    'B_REGULAR_2303033_DIAGNOSTIC_CORRECTED_SAFE.zip': (11631, '1beeeffdb1bc0c1d0665df8c348d833b3a002ddd8148116117a50d933fb4fc04'),
}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def checked_members(archive_name, manifest_name):
    archive, manifest = BASE / archive_name, BASE / manifest_name
    metadata = json.loads(manifest.read_text())
    require(pin(archive.read_bytes()) == {'bytes': metadata['archive_bytes'], 'sha256': metadata['archive_sha256']}, 'Archive manifest pin')
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'CRC')
        names = z.namelist()
        require(len(names) == len(set(names)) == 9, 'Unique nine members')
        require(set(names) == set(metadata['members']), 'Exact allowlist')
        require(all('/' not in n and '\\' not in n for n in names), 'Flat member paths')
        members = {n: z.read(n) for n in names}
    for name, info in metadata['members'].items():
        require(pin(members[name]) == info, 'External member pin: ' + name)
    internal = json.loads(members['MANIFEST.json'])['members']
    require(set(internal) == set(members) - {'MANIFEST.json'}, 'Internal allowlist')
    for name, info in internal.items():
        require(pin(members[name]) == info, 'Internal member pin: ' + name)
    return members

def run_case(members, label, variant, expected_success):
    results = []
    with tempfile.TemporaryDirectory(prefix='b_regular_replay_') as directory:
        root = Path(directory)
        files = root / 'relocated'
        files.mkdir()
        for name, content in members.items():
            (files / name).write_bytes(content)
        if variant:
            variant(files)
        for optimized in (False, True):
            command = [sys.executable] + (['-O'] if optimized else []) + [str(files / 'verify.py')]
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=30)
            expected = expected_success[optimized]
            require((result.returncode == 0) == expected, label + ': exit expectation')
            if expected:
                require(json.loads(result.stdout) == json.loads(members['VERIFICATION.json']), label + ': exact stored output')
            results.append({'case': label, 'optimized': optimized, 'exit_code': result.returncode, 'expected_success': expected, 'expectation_met': True})
    return results

def status_mutation(field, value):
    def mutate(root):
        p = root / 'STATUS.json'
        data = json.loads(p.read_text())
        data[field] = value
        p.write_text(json.dumps(data))
    return mutate

def script_mutation(old, new):
    def mutate(root):
        p = root / 'verify.py'
        code = p.read_text()
        require(old in code, 'Mutation target found')
        p.write_text(code.replace(old, new))
    return mutate

def main():
    for name, (size, sha) in PINS.items():
        require(pin((BASE / name).read_bytes()) == {'bytes': size, 'sha256': sha}, 'Trusted input pin: ' + name)
    author = checked_members('B_REGULAR_2303033_AUTHOR_SAFE_FREEZE.zip', 'B_REGULAR_2303033_AUTHOR_EXTERNAL_MANIFEST.json')
    corrected = checked_members('B_REGULAR_2303033_DIAGNOSTIC_CORRECTED_SAFE.zip', 'B_REGULAR_2303033_DIAGNOSTIC_CORRECTED_EXTERNAL_MANIFEST.json')
    changed = sorted(n for n in author if author[n] != corrected[n])
    require(changed == ['MANIFEST.json', 'verify.py'], 'Minimal correction scope')
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(corrected['verify.py']))), 'No optimized-away assertions')
    records = []
    records += run_case(author, 'author_original', None, {False: True, True: True})
    records += run_case(author, 'author_status_full_solution_true', status_mutation('full_solution', True), {False: False, True: True})
    records += run_case(author, 'author_false_assertion', script_mutation('assert abs(F(0.5) - 1j) < 1e-13', 'assert False'), {False: False, True: True})
    records += run_case(corrected, 'corrected_original', None, {False: True, True: True})
    for field, value in [('full_solution', True), ('novelty_claim', True), ('turns_used', 3), ('turn_limit', 6), ('current_literature_status', 'verified')]:
        records += run_case(corrected, 'corrected_status_' + field, status_mutation(field, value), {False: False, True: False})
    records += run_case(corrected, 'corrected_wrong_rotation', script_mutation('ROT = cmath.exp(-2j * math.pi / 3)', 'ROT = cmath.exp(2j * math.pi / 3)'), {False: False, True: False})
    records += run_case(corrected, 'corrected_wrong_exponent', script_mutation('p, beta = Fraction(5, 4), Fraction(1, 2)', 'p, beta = Fraction(7, 4), Fraction(1, 2)'), {False: False, True: False})
    records += run_case(corrected, 'corrected_wrong_density_factor', script_mutation('return (3 * math.sqrt(3) / (2 * math.pi))', 'return (6 * math.sqrt(3) / (2 * math.pi))'), {False: False, True: False})
    records += run_case(corrected, 'corrected_failed_runtime_check', script_mutation('require(abs(F(0.5) - 1j) < 1e-13,', 'require(False,'), {False: False, True: False})
    return {'result': 'pass', 'scope': 'Exact artifact pins and isolated executable replay only; mathematical acceptance is in MATHEMATICAL_AUDIT.md.', 'cases': records, 'cases_count': len(records), 'source_corpus_required': False, 'network_used': False, 'original_optimized_fail_open_reproduced': True, 'corrected_optimized_checks_active': True, 'changed_members': changed}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
