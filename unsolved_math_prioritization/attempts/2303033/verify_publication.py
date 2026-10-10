#!/usr/bin/env python3
"""Fail-closed, offline verification of the accepted immutable partial-result packet."""
import argparse
import ast
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

BASE = Path(__file__).resolve().parent
ARCHIVES = {
    'AUTHOR': ('B_REGULAR_2303033_AUTHOR_SAFE_FREEZE.zip', 11463, 'b440a4b7dfca3b37e477cf121b1bd04938d22c1c42b861c58c84be94903263c3'),
    'DIAGNOSTIC_CORRECTED': ('B_REGULAR_2303033_DIAGNOSTIC_CORRECTED_SAFE.zip', 11631, '1beeeffdb1bc0c1d0665df8c348d833b3a002ddd8148116117a50d933fb4fc04'),
    'INDEPENDENT_AUDIT': ('B_REGULAR_2303033_INDEPENDENT_AUDIT_SAFE.zip', 39949, '9ec756875baf22c76245b02af887d706f13c53b15a81ee5a69da0036db9c945e'),
}
MANIFEST_PINS = {
    'AUTHOR': (2027, '4affbaf482d62671ea8dbb6931b2cfb1fb39d6a8ec6fa09b7e4cd1044dd6b20d'),
    'DIAGNOSTIC_CORRECTED': (2050, '5a78caafba2fb23c32acf2afd92512c3ff0b0810ce6806d13709ac192a2ec7b6'),
    'INDEPENDENT_AUDIT': (2588, '14f90d065663cc520e1e6713892b9f1e3a0ee14c877ebac6f2d974b02ad51172'),
}

def require(value, message):
    if not value:
        raise RuntimeError(message)

def pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def exact_pin(data, size, sha, label):
    require(pin(data) == {'bytes': size, 'sha256': sha}, label)

def read_archive(data, metadata, count):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        require(z.testzip() is None, 'ZIP CRC')
        require(len(names) == len(set(names)) == count, 'Unique exact member count')
        require(set(names) == set(metadata['members']), 'Archive allowlist')
        require(all('/' not in n and '\\' not in n and n not in ('.', '..') for n in names), 'Flat archive names')
        require(all((x.external_attr >> 16) & 0o170000 != 0o120000 for x in z.infolist()), 'No archive symlinks')
        members = {n: z.read(n) for n in names}
    for n, info in metadata['members'].items():
        require(pin(members[n]) == info, 'Archive member pin: ' + n)
    if 'MANIFEST.json' in members:
        inner = json.loads(members['MANIFEST.json'])['members']
        require(set(inner) == set(members) - {'MANIFEST.json'}, 'Internal manifest allowlist')
        for n, info in inner.items():
            require(pin(members[n]) == info, 'Internal manifest pin: ' + n)
    return members

def apply_exact_patch(original, patch):
    lines = patch.splitlines(keepends=True)
    require(lines[:2] == ['--- author/verify.py\n', '+++ corrected/verify.py\n'], 'Exact patch paths')
    source = original.splitlines(keepends=True)
    output, cursor, at = [], 0, 2
    while at < len(lines):
        match = re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n', lines[at])
        require(match is not None, 'Patch hunk header')
        old_start, old_count, new_start, new_count = map(int, match.groups())
        require(old_start - 1 >= cursor, 'Patch monotonic source offsets')
        output.extend(source[cursor:old_start - 1]); cursor = old_start - 1
        require(len(output) == new_start - 1, 'Patch destination offset')
        consumed = produced = 0; at += 1
        while at < len(lines) and not lines[at].startswith('@@ '):
            line = lines[at]; require(line[:1] in (' ', '+', '-'), 'Patch line marker')
            if line[:1] in (' ', '-'):
                require(cursor < len(source) and source[cursor] == line[1:], 'Exact patch context')
                cursor += 1; consumed += 1
            if line[:1] in (' ', '+'):
                output.append(line[1:]); produced += 1
            at += 1
        require((consumed, produced) == (old_count, new_count), 'Patch hunk lengths')
    output.extend(source[cursor:])
    return ''.join(output)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.manifest_sha256) is not None, 'Explicit manifest pin required')
    manifest_bytes = (BASE / 'PUBLICATION_MANIFEST.json').read_bytes()
    require(hashlib.sha256(manifest_bytes).hexdigest() == args.manifest_sha256, 'Publication manifest pin')
    manifest = json.loads(manifest_bytes)
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    paths = list(BASE.rglob('*'))
    require(not any(p.is_symlink() for p in paths), 'No publication symlinks')
    actual = {p.relative_to(BASE).as_posix() for p in paths if p.is_file()}
    require(actual == expected, 'Exact publication inventory')
    require(all(p.is_file() or p.is_dir() for p in paths), 'Only ordinary files/directories')
    for n, info in manifest['files'].items():
        require(pin((BASE / n).read_bytes()) == info, 'Publication file pin: ' + n)
    require(not any(isinstance(x, ast.Assert) for x in ast.walk(ast.parse(Path(__file__).read_text()))), 'Wrapper has no assertions')
    raw, packages = {}, {}
    folders = {'AUTHOR': 'author', 'DIAGNOSTIC_CORRECTED': 'corrected', 'INDEPENDENT_AUDIT': 'audit'}
    for tag, (name, size, sha) in ARCHIVES.items():
        encoded = (BASE / 'frozen_archives' / (name + '.b64')).read_bytes()
        data = base64.b64decode(encoded.rstrip(b'\n'), validate=True)
        require(encoded == base64.b64encode(data) + b'\n', 'Canonical archive base64')
        exact_pin(data, size, sha, 'Immutable ZIP pin: ' + tag)
        mname = 'B_REGULAR_2303033_' + tag + '_EXTERNAL_MANIFEST.json'
        mb = (BASE / 'manifests' / mname).read_bytes()
        exact_pin(mb, *MANIFEST_PINS[tag], 'Immutable external manifest: ' + tag)
        metadata = json.loads(mb)
        require(metadata['archive_filename'] == name, 'Manifest archive identity')
        require(pin(data) == {'bytes': metadata['archive_bytes'], 'sha256': metadata['archive_sha256']}, 'External archive pin')
        raw[name] = data
        members = read_archive(data, metadata, 11 if tag == 'INDEPENDENT_AUDIT' else 9)
        packages[tag] = members
        for n, content in members.items():
            if n.endswith('.zip'):
                require(n in raw and content == raw[n], 'Nested archive exact bytes')
            else:
                require((BASE / folders[tag] / n).read_bytes() == content, 'Readable member exact bytes: ' + n)
    original, corrected, audit = (packages[t] for t in ('AUTHOR', 'DIAGNOSTIC_CORRECTED', 'INDEPENDENT_AUDIT'))
    require(sorted(n for n in original if original[n] != corrected[n]) == ['MANIFEST.json', 'verify.py'], 'Minimal derivative changes')
    patched = apply_exact_patch(original['verify.py'].decode(), audit['DIAGNOSTIC_CORRECTION.patch'].decode()).encode()
    require(patched == corrected['verify.py'], 'Actual patch creates accepted diagnostic')
    updated = json.loads(original['MANIFEST.json'])
    updated['members']['verify.py'] = pin(patched)
    require((json.dumps(updated, indent=2) + '\n').encode() == corrected['MANIFEST.json'], 'Deterministic manifest update creates accepted bytes')
    old_ast = ast.parse(original['verify.py']); new_ast = ast.parse(patched)
    require(sum(isinstance(x, ast.Assert) for x in ast.walk(old_ast)) == 13, '13 historical assertions')
    require(not any(isinstance(x, ast.Assert) for x in ast.walk(new_ast)), 'Corrected checks survive optimization')
    require(sum(isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == 'require' for x in ast.walk(new_ast)) == 13, '13 explicit diagnostic checks')
    require(not any(isinstance(x, ast.Assert) for x in ast.walk(ast.parse(audit['verify_audit.py']))), 'Audit checks survive optimization')
    receipt = json.loads((BASE / 'INDEPENDENT_AUDIT_RECEIPT.json').read_bytes())
    for key, member in [('acceptance', 'ACCEPTANCE.json'), ('mathematical_audit', 'MATHEMATICAL_AUDIT.md')]:
        require(pin(audit[member]) == {k: receipt[key][k] for k in ('bytes', 'sha256')}, 'Exact receipt: ' + key)
    acceptance = json.loads(audit['ACCEPTANCE.json'])
    require(acceptance['problem_id'] == 2303033 and acceptance['rank'] == 901, 'Accepted identity')
    disposition = acceptance['disposition']
    require(disposition['status'] == 'stalled_partial' and disposition['turns_used'] == 2 and disposition['turn_limit'] == 5, 'Accepted partial disposition')
    require(disposition['full_solution'] is False and disposition['counterexample_to_original_problem'] is False and disposition['novelty_claim'] is False, 'No promoted claims')
    require(disposition['current_literature_status'] == 'unverified', 'Unverified literature retained')
    require(hashlib.sha256(original['PROOF.md']).hexdigest() == acceptance['proof_sha256'], 'Accepted proof unchanged')
    outputs = []
    with tempfile.TemporaryDirectory(prefix='b_regular_publication_') as temporary:
        directory = Path(temporary); relocated = directory / 'audit'; relocated.mkdir()
        for n, content in audit.items():
            (relocated / n).write_bytes(content)
        for optimized in (False, True):
            command = [sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(relocated / 'verify_audit.py')]
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True, timeout=180)
            require(result.returncode == 0, 'Isolated audit replay failed: ' + result.stderr)
            parsed = json.loads(result.stdout)
            require(parsed == json.loads(audit['REPLAY_RESULTS.json']), 'Exact frozen replay output')
            require(parsed['cases_count'] == 26 and all(c['expectation_met'] for c in parsed['cases']), '26 expected outcomes')
            outputs.append(parsed)
    require(outputs[0] == outputs[1], 'Normal and optimized audit outputs equal')
    return {'result': 'pass', 'problem_id': 2303033, 'archive_count': 3, 'archive_member_counts': [9, 9, 11], 'publication_files': len(actual), 'actual_patch_replayed': True, 'deterministic_manifest_update_matches': True, 'proof_unchanged': True, 'historical_assertions': 13, 'corrected_runtime_checks': 13, 'audit_replay_modes': ['normal', 'optimized'], 'cases_per_replay': 26, 'expected_successes_per_replay': 6, 'expected_rejections_per_replay': 20, 'original_optimized_false_passes_per_replay': 2, 'all_expected_outcomes_met': True, 'network_used': False, 'external_provenance_replay': 'NOT_RUN_EXTERNAL_INPUTS_REQUIRED', 'mathematical_scope': 'Accepted partial only; no localization counterexample, full solution, or novelty claim; current literature unverified.'}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
