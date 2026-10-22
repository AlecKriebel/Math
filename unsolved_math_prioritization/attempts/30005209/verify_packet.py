#!/usr/bin/env python3
"""Source-free packet integrity checks; optional floating-point formula replay.

This does not prove the mathematics, recheck external theorems, retrieve sources,
or establish novelty. Run with Python 3.10+; --sanity additionally needs SciPy.
No retained packet file is modified. Optional replay runs a copy in a temp folder.
"""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
ORIGINAL_MANIFEST = 'fa8b800b4df4a938a72256b6b97a106cf9555a4ccd323003255e30b9320a1516'
AUDIT = '3d094bbc985f6f48f1fa3679382d6414b730127f261a968ab0f29d011e79b8af'
PATCH = '46b92198186437ead57ebdff5f6bd536078bcb41d617d75823d8ca47ec1a5f0d'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_file(base, name):
    candidate = base / name
    require(not candidate.is_symlink(), f'Symlink is outside packet contract: {name}')
    path = candidate.resolve()
    require(path.is_relative_to(base.resolve()), f'Unsafe manifest path: {name}')
    require(path.is_file(), f'Missing file: {name}')
    return path


def check_pin(path, pin):
    data = path.read_bytes()
    require(len(data) == pin['bytes'], f'Byte count mismatch: {path.name}')
    require(digest(data) == pin['sha256'], f'SHA-256 mismatch: {path.name}')


def integrity():
    packet = read_json(ROOT / 'PACKET_MANIFEST.json')
    expected = {entry['file'] for entry in packet['files']}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual == expected | {'PACKET_MANIFEST.json'}, 'Packet file allowlist differs')
    for entry in packet['files']:
        check_pin(safe_file(ROOT, entry['file']), entry)
    authored = ROOT / 'authored'
    manifest_bytes = (authored / 'AUTHORED_MANIFEST.json').read_bytes()
    require(digest(manifest_bytes) == ORIGINAL_MANIFEST, 'Original manifest anchor differs')
    original = json.loads(manifest_bytes)
    require(len(original['files']) == 11, 'Expected 11 frozen authored files')
    for entry in original['files']:
        check_pin(safe_file(authored, entry['file']), entry)
    review = ROOT / 'review'
    acceptance = read_json(review / 'ACCEPTANCE.json')
    require(acceptance['decision'] == 'ACCEPT_PARTIAL_RESULTS', 'Acceptance scope differs')
    require(acceptance['classification_status'] == 'UNRESOLVED', 'Classification scope differs')
    require(not acceptance['novelty_claimed'], 'Unexpected novelty claim')
    require(not acceptance['full_classification_accepted'], 'Unexpected full solution claim')
    require(acceptance['accepted_original_files'] == original['files'], 'Acceptance file pins differ')
    check_pin(authored / 'AUTHORED_MANIFEST.json', acceptance['accepted_original_manifest'])
    check_pin(review / 'AUDIT_REPORT.md', acceptance['audit_report'])
    require(digest((review / 'AUDIT_REPORT.md').read_bytes()) == AUDIT, 'Audit anchor differs')
    typography = read_json(review / 'TYPOGRAPHY_MANIFEST.json')
    require(typography['files'] == acceptance['accepted_reading_copies'], 'Reading acceptance pins differ')
    check_pin(review / 'TYPOGRAPHY_ONLY.patch', acceptance['typography']['patch'])
    check_pin(review / 'TYPOGRAPHY_MANIFEST.json', acceptance['typography']['manifest'])
    require(digest((review / 'TYPOGRAPHY_ONLY.patch').read_bytes()) == PATCH, 'Patch anchor differs')
    corrected = read_json(review / 'readable/CORRECTED_COPY_MANIFEST.json')
    require(corrected['original_manifest_sha256'] == ORIGINAL_MANIFEST, 'Corrected anchor differs')
    require(corrected['patch_sha256'] == PATCH, 'Corrected patch anchor differs')
    require(corrected['files'] == [dict(file=e['file'], bytes=e['reading_copy_bytes'],
                                      sha256=e['reading_copy_sha256']) for e in typography['files']],
            'Separate corrected-copy manifest differs')
    generated_patch = ''
    total_insertions = 0
    for entry in typography['files']:
        old_path = safe_file(authored, entry['file'])
        new_path = safe_file(review / 'readable', entry['file'])
        check_pin(old_path, dict(bytes=entry['original_bytes'], sha256=entry['original_sha256']))
        check_pin(new_path, dict(bytes=entry['reading_copy_bytes'], sha256=entry['reading_copy_sha256']))
        old, new = old_path.read_bytes(), new_path.read_bytes()
        inserted = 0
        for op, i, j, k, l in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
            if op == 'equal':
                continue
            require(op == 'insert' and new[k:l] == b'\\' * (l-k), 'Non-typographic byte edit')
            inserted += l-k
        require(inserted == entry['backslashes_inserted'], 'Insertion count differs')
        total_insertions += inserted
        generated_patch += ''.join(difflib.unified_diff(
            old.decode('utf-8').splitlines(True), new.decode('utf-8').splitlines(True),
            fromfile='a/' + entry['file'], tofile='b/' + entry['file']))
    require(total_insertions == typography['total_backslashes_inserted'] == 171, 'Expected 171 insertions')
    require(generated_patch.encode('utf-8') == (review / 'TYPOGRAPHY_ONLY.patch').read_bytes(),
            'Patch does not reproduce exactly from original and corrected bytes')
    return dict(status='passed', pinned_files=len(packet['files']), frozen_authored_files=11,
                corrected_reading_copies=8, inserted_backslashes=total_insertions,
                source_retrieval_or_reinspection_performed=False,
                scope='Byte integrity and typography only; not mathematical or formal verification')


def sanity():
    # The unchanged authored script's assertions are always enabled in this child.
    with tempfile.TemporaryDirectory(prefix='crystalline-wulff-') as temporary:
        target = Path(temporary) / 'verify_formulas.py'
        shutil.copyfile(ROOT / 'authored/verify_formulas.py', target)
        import os
        environment = dict(os.environ)
        environment.pop('PYTHONOPTIMIZE', None)
        run = subprocess.run([sys.executable, str(target)], cwd=temporary,
                             env=environment, capture_output=True, text=True)
        require(run.returncode == 0, 'Sanity replay failed: ' + run.stderr)
        result_bytes = target.with_name('verification_results.json').read_bytes()
    expected_bytes = (ROOT / 'authored/verification_results.json').read_bytes()
    generated, expected = json.loads(result_bytes), json.loads(expected_bytes)
    groups = [('parallelogram_checks', 12), ('square_hessian_checks', 4), ('thin_triangle_checks', 3)]
    import math
    def close(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
        if isinstance(a, list) and isinstance(b, list):
            return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10)
        return a == b
    require(close(generated, expected), 'Replay differs beyond reported floating-point tolerance')
    for group, count in groups:
        require(len(generated[group]) == count, 'Sanity case count differs')
    return dict(status='passed', checks=19, byte_identical_to_retained_output=result_bytes == expected_bytes,
                json_comparison_relative_tolerance=1e-10, json_comparison_absolute_tolerance=1e-10,
                replay_sha256=digest(result_bytes), retained_sha256=digest(expected_bytes),
                scope='Floating-point sanity checks, not exact proof certificates; analytic arguments and cited theorems carry the proofs')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sanity', action='store_true', help='Also replay 19 floating-point checks; requires SciPy')
    args = parser.parse_args()
    result = dict(integrity=integrity(), classification_status='UNRESOLVED', full_solution_claimed=False)
    if args.sanity:
        result['sanity'] = sanity()
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
