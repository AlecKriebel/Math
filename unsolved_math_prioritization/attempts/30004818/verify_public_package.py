#!/usr/bin/env python3
"""Source-free public integrity, patch and finite-arithmetic checks only.

This is a new checker, not a replacement or rebinding of the frozen acceptance.
It never reads or retrieves raw scholarly source documents. It is not a proof
checker and does not certify geometric arguments, Floer arguments or novelty.
Run with Python 3 using its standard library only.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def verify_pin(path, record):
    require(path.is_file() and not path.is_symlink(), f'Missing or unsafe file: {path}')
    data = path.read_bytes()
    require(len(data) == record['bytes'], f'Byte count mismatch: {path}')
    require(hashlib.sha256(data).hexdigest() == record['sha256'], f'Hash mismatch: {path}')


def apply_exact_patch(text):
    """Apply the retained, ordinary unified diff in memory, with no offsets/fuzz."""
    lines = text.splitlines(keepends=True)
    i = 0
    outputs = {}
    while i < len(lines):
        require(lines[i].startswith('--- a/'), 'Expected source-file patch header')
        old_name = lines[i][6:].rstrip('\n')
        i += 1
        require(i < len(lines) and lines[i].startswith('+++ b/'), 'Expected target-file patch header')
        new_name = lines[i][6:].rstrip('\n')
        require(old_name == new_name, 'Unexpected renamed patch target')
        require(old_name in {
            'local_knot_genus_30004818/authored/SOURCE_AND_SCOPE_REPORT.md',
            'local_knot_genus_30004818/authored/APPROACH_05_COBORDISM_NORM_AND_FLOER_BOUNDS.md',
        }, 'Patch target is outside the authorized two-file set')
        require(old_name not in outputs, 'Duplicate patch target')
        original = (ROOT / old_name).read_text(encoding='utf-8').splitlines(keepends=True)
        out = []
        cursor = 0
        i += 1
        while i < len(lines) and lines[i].startswith('@@ '):
            m = re.fullmatch(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@[^\n]*\n', lines[i])
            require(m is not None, 'Malformed hunk header')
            old_start, old_count, new_start, new_count = (
                int(m.group(1)), int(m.group(2) or '1'),
                int(m.group(3)), int(m.group(4) or '1'))
            require(old_start - 1 >= cursor, 'Overlapping or reordered hunk')
            out.extend(original[cursor:old_start - 1])
            cursor = old_start - 1
            require(len(out) == new_start - 1, 'New hunk line position mismatch')
            i += 1
            removed = added = 0
            while i < len(lines) and not lines[i].startswith(('@@ ', '--- a/')):
                line = lines[i]
                require(line[:1] in (' ', '-', '+'), 'Unsupported diff record')
                if line[0] in (' ', '-'):
                    require(cursor < len(original) and original[cursor] == line[1:], 'Exact hunk context mismatch')
                    cursor += 1
                    removed += 1
                if line[0] in (' ', '+'):
                    out.append(line[1:])
                    added += 1
                i += 1
            require((removed, added) == (old_count, new_count), 'Hunk length mismatch')
        out.extend(original[cursor:])
        outputs[old_name] = ''.join(out).encode('utf-8')
    require(len(outputs) == 2, 'Expected exactly two patched outputs')
    return outputs


def main():
    manifest = read_json(ROOT / 'PUBLICATION_MANIFEST.json')
    require(manifest['full_resolution'] is False, 'Invalid current scope')
    declared = {r['path']: r for r in manifest['files']}
    require(len(declared) == len(manifest['files']), 'Duplicate inventory path')
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    require(actual == set(declared) | {'PUBLICATION_MANIFEST.json'}, 'Public inventory differs from exact allowlist')
    for name, record in declared.items():
        require(not Path(name).is_absolute() and '..' not in Path(name).parts, 'Unsafe manifest path')
        require(Path(name).suffix not in {'.pdf', '.png', '.jpg', '.txt'}, 'Unexpected raw-source file type')
        verify_pin(ROOT / name, record)

    base = ROOT / 'local_knot_genus_30004818'
    audit = ROOT / 'local_knot_genus_audit'
    original = read_json(base / 'verification/AUTHORED_MANIFEST.json')
    require(len(original['authored_files']) == 7, 'Expected seven frozen author files')
    for row in original['authored_files']:
        verify_pin(base / row['file'], row)
    for row in read_json(audit / 'input_pins.json'):
        verify_pin(base / row['file'], row)
    audit_manifest = read_json(audit / 'AUDIT_MANIFEST.json')
    for row in audit_manifest['authored_artifact_allowlist']:
        verify_pin(audit / row['file'], row)
    require(hashlib.sha256((audit / 'ACCEPTANCE_REPORT.md').read_bytes()).hexdigest()
            == '6972cbca8d53737613854c6d4bb3d55caad2ba3958dd2cdcb54ebf11b71bd2a1',
            'Original acceptance anchor mismatch')

    patched = apply_exact_patch((audit / 'OPTIONAL_CLARIFICATIONS.diff').read_text(encoding='utf-8'))
    for row in read_json(audit / 'patch_dry_run.json')['patched_copy_pins']:
        target = ROOT / 'clarified' / row['file']
        verify_pin(target, row)
        require(target.read_bytes() == patched[row['file']], 'Clarified copy differs from exact patch output')

    checks = {'finite_cover_cases': 0}
    for degree in range(1, 31):
        for genus in range(21):
            if genus == 0 and degree != 1:
                continue
            upstairs = 1 + degree * (genus - 1)
            require(upstairs >= 0, 'Negative admissible genus')
            require(2 - 2 * upstairs - degree == degree * (1 - 2 * genus), 'Cover Euler identity')
            require(degree * (1 - 2 * genus) - (degree - 1) == 1 - 2 * degree * genus, 'Band Euler identity')
            checks['finite_cover_cases'] += 1
    checks['equivariant_records'] = 0
    for row in read_json(base / 'verification/APPROACH_03_CHECKS.json')['equivariant_genus_one_arithmetic']:
        require(2 - 2 * row['upstairs_genus'] - row['upstairs_boundary'] == row['degree'] * row['quotient_chi'], 'Equivariant cover identity')
        require(row['quotient_chi'] == 1 - 2 * row['quotient_genus'], 'Quotient genus identity')
        checks['equivariant_records'] += 1
    checks['smoothing_cases'] = 0
    for intersections in range(1001):
        require(-1 - 2 * intersections == 1 - 2 * (1 + intersections), 'Smoothing Euler identity')
        checks['smoothing_cases'] += 1
    q = lambda n: (abs(n) + 1) // 2
    checks['norm_triangle_inequalities'] = 0
    for a in range(-100, 101):
        require(q(a) == q(-a) and ((q(a) == 0) == (a == 0)), 'Norm symmetry or zero set')
        for b in range(-100, 101):
            require(q(a + b) <= q(a) + q(b), 'Norm triangle inequality')
            checks['norm_triangle_inequalities'] += 1
    checks['disk_bundle_determinants'] = 0
    for p in range(-1000, 1001):
        require(p * 0 - 1 * 1 == -1, 'Disk bundle determinant')
        checks['disk_bundle_determinants'] += 1
    checks['status'] = 'PASS'
    checks['scope'] = 'Finite arithmetic checks only. Geometric and Floer claims are assessed in the mathematical audit, not certified by this file.'
    require(checks == read_json(audit / 'independent_checks.json'), 'Historical arithmetic counts differ')
    result = {
        'checker': 'verify_public_package.py',
        'status': 'PASS',
        'inventory_files_hashed': len(declared),
        'frozen_author_files': 7,
        'frozen_audit_allowlist_files': len(audit_manifest['authored_artifact_allowlist']),
        'exact_patch_outputs': len(patched),
        'arithmetic': checks,
        'raw_source_checks_replayed': False,
        'mathematical_proof_certified': False,
        'scope': 'Public file integrity, exact editorial patch reconstruction and finite arithmetic only. No source retrieval, source-text verification or geometric/Floer proof certification.',
    }
    require(result == read_json(ROOT / 'PORTABLE_CHECK_RESULTS.json'), 'Portable result differs from declared record')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
