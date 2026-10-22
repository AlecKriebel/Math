#!/usr/bin/env python3
"""Source-free integrity and arithmetic replay, not analytic/formal proof verification."""
from pathlib import Path, PurePosixPath
from fractions import Fraction
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import sympy as s
import mpmath

ROOT = Path(__file__).resolve().parent
AUTHOR = 'theta_twisted_volumes_30004711/authored'
CUSP = 'theta_cusp_growth_audit/authored'
CURRENT = 'theta_current_recursion_audit/authored'
LINE = 'theta_line_comparison_audit/authored'


def pin(path, expected):
    b = path.read_bytes()
    assert len(b) == expected['bytes'], f'Byte count mismatch: {path.name}'
    assert hashlib.sha256(b).hexdigest() == expected['sha256'], f'Hash mismatch: {path.name}'


def verify_inventory():
    m = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text())
    assert m['schema'] == 'theta-volume-30004711-publication-v1'
    assert m['problem_id'] == 30004711 and m['status'] == 'unsolved' and m['turns'] == '5/5'
    allowed = {e['path'] for e in m['files']}
    assert len(allowed) == len(m['files']), 'Duplicate manifest entry'
    assert 'PUBLIC_MANIFEST.json' not in allowed
    actual = set()
    for p in ROOT.rglob('*'):
        assert not p.is_symlink(), 'Symlinks are excluded'
        if p.is_file():
            actual.add(p.relative_to(ROOT).as_posix())
    assert actual == allowed | {'PUBLIC_MANIFEST.json'}, f'Allowlist mismatch: {actual ^ (allowed | {"PUBLIC_MANIFEST.json"})}'
    for e in m['files']:
        p = PurePosixPath(e['path'])
        assert not p.is_absolute() and '..' not in p.parts
        assert p.suffix in {'.md', '.json', '.py'}, p
        assert 'private_sources' not in p.parts
        pin(ROOT / e['path'], e)
    assert m['original_preserved_file_count'] == 48
    assert sum(e['preserved_original'] for e in m['files']) == 48
    for e in json.loads((ROOT / AUTHOR / 'DELIVERABLE_MANIFEST.json').read_text())['files']:
        pin(ROOT / AUTHOR / e['name'], e)
    assert (ROOT / AUTHOR / 'CORRECTIVE_ADDENDUM.md').is_file()
    assert (ROOT / AUTHOR / 'SOURCE_SCOPED_IMPLICATION_REPORT.md').is_file()
    assert (ROOT / AUTHOR / 'APPROACH_2_CONVENTION_CLARIFICATION.md').read_bytes() == (ROOT / LINE / 'APPROACH_2_CONVENTION_CLARIFICATION.md').read_bytes()
    ca = json.loads((ROOT / CUSP / 'PINNED_CUSP_CORRECTION_ACCEPTANCE.json').read_text())
    for e in [ca['frozen_candidate'], *ca['other_inspected_authored_inputs']]:
        pin(ROOT / AUTHOR / e['filename'], e)
    pin(ROOT / CUSP / ca['audit_report']['filename'], ca['audit_report'])
    ac = json.loads((ROOT / CURRENT / 'PINNED_CURRENT_RECURSION_ACCEPTANCE.json').read_text())
    for e in ac['frozen_targets']:
        pin(ROOT / AUTHOR / e['file'], e)
    for e in ac['accepted_dependency_artifacts']:
        folder = AUTHOR if e['file'].startswith('AUTHOR_') else CUSP
        pin(ROOT / folder / e['file'], e)
    for e in ac['audit_artifacts']:
        pin(ROOT / CURRENT / e['file'], e)
    return m


def elementary_cusp_checks():
    # A separate source-free calculation. Does not execute or modify the
    # historical cusp checker, which requires excluded source PDF bytes.
    Y, y, T, A, r, t, k = s.symbols('Y y T A r t k', positive=True)
    collar = s.integrate(Y / s.pi * s.sin(s.pi * y / Y), (y, 0, Y))
    assert s.simplify(collar - 2 * Y**2 / s.pi**2) == 0
    assert s.simplify((T**s.Rational(3, 2) / s.sqrt(A))**s.Rational(2, 3) * A**s.Rational(1, 3) - T) == 0
    tail = s.integrate(y * s.exp(-2*s.pi*y), (y, Y, s.oo))
    assert s.simplify(tail - s.exp(-2*s.pi*Y)*(Y/(2*s.pi) + 1/(4*s.pi**2))) == 0
    assert s.limit((2*s.log(t) + s.log(s.log(t)))/t, t, s.oo) == 0
    assert s.limit((2*s.log(k*t) + s.log(s.log(k*t)))/t, t, s.oo) == 0
    primitive = -s.log(1/r)**2 / 2
    assert s.simplify(s.diff(primitive, r) - s.log(1/r)/r) == 0
    assert s.limit(primitive, r, 0, dir='+') == -s.oo
    assert s.simplify(s.diff(2*s.log(t)+s.sin(t**2), t) - (2/t+2*t*s.cos(t**2))) == 0
    assert Fraction(3, 2)*Fraction(1, 2)*Fraction(1, 24) == Fraction(1, 32)
    return {'scope': 'Elementary identities only; excludes source verification and geometric/analytic theorem applications', 'passed': True}


def main():
    m = verify_inventory()
    replays = []
    scripts = [e['path'] for e in m['files'] if e['preserved_original'] and e['path'].endswith('.py')]
    skip = CUSP + '/verify_cusp_audit.py'
    assert len(scripts) == 10 and skip in scripts
    before = {e['path']: (ROOT / e['path']).read_bytes() for e in m['files']}
    with tempfile.TemporaryDirectory(prefix='theta-volume-source-free-') as tmp:
        work = Path(tmp)
        for e in m['files']:
            if e['preserved_original']:
                dst = work / e['path']
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(before[e['path']])
        for name in scripts:
            if name == skip:
                continue
            p = subprocess.run([sys.executable, '-B', str(work / name)], cwd=work,
                               text=True, capture_output=True, timeout=300)
            assert p.returncode == 0, f'{name}: {p.stderr}'
            result = json.loads(p.stdout)
            replays.append({'script': name, 'returncode': p.returncode,
                            'stdout_is_json': isinstance(result, dict)})
        expected_paths = {e['path'] for e in m['files'] if e['preserved_original']}
        actual_paths = {p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file()}
        assert actual_paths == expected_paths, 'Replay produced unexpected files'
        for name in expected_paths:
            assert (work / name).read_bytes() == before[name], f'Replay output differs from preserved original: {name}'
    elementary = elementary_cusp_checks()
    for name, b in before.items():
        assert (ROOT / name).read_bytes() == b, f'Original modified by driver: {name}'
    print(json.dumps({
        'problem_id': 30004711, 'status': 'PASS',
        'scope': 'Source-free packet integrity and finite arithmetic/symbolic replay only',
        'versions': {'python': sys.version.split()[0], 'sympy': s.__version__, 'mpmath': mpmath.__version__},
        'preserved_original_files': 48, 'manifested_files': len(m['files']),
        'exact_allowlist_and_all_byte_pins_match': True,
        'author_inventory_and_acceptance_pins_match': True,
        'both_mandatory_addenda_present': True,
        'historical_checkers_replayed': replays,
        'all_replayed_outputs_byte_identical': True,
        'historical_checkers_skipped': [{'script': skip, 'reason': 'Requires excluded source PDFs; complete historical run not portable in this source-free packet'}],
        'separate_cusp_arithmetic': elementary,
        'source_PDF_hashes_reverified': False,
        'source_retrieval_or_inspection_replayed': False,
        'analytic_proofs_or_theorem_applications_formally_verified': False,
        'actual_torsion_identity_proved': False,
        'higher_rank_or_even_component_current_extension_proved': False,
    }, indent=2))


if __name__ == '__main__':
    main()
