#!/usr/bin/env python3
"""Root receipt of sealed evidence; not a publication/disposition gate.

No source or reviewer-file writes. Explicit guards remain active under -O.
Root's complete report/code reading is separately recorded in the receipt.
"""
import ast
import datetime
import hashlib
import json
from pathlib import Path

CASE = Path(__file__).resolve().parent
HEAD = '87a39f7b4e5ef81aacf98464f86586cc95684d7f'


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def load(relative):
    return json.loads((CASE / relative).read_text())


def identity(value, reviewer=None):
    require(type(value.get('pr')) is int and value['pr'] == 458, 'PR identity')
    require(value.get('problem_id') == '20000693', 'problem identity')
    require(value.get('frozen_head') == HEAD, 'head identity')
    if reviewer is not None:
        require(value.get('reviewer') == '/root/pr458_' + reviewer, 'reviewer identity')


def manifest(reviewer):
    folder = CASE / 'reviews' / reviewer
    value = json.loads((folder / 'PUBLIC_FILES.json').read_text())
    identity(value, reviewer)
    seen = set()
    records = []
    excluded = {'private_sources', 'private_cases', 'venv', '.venv', '__pycache__',
                '.secrets', '.zenodo-state', 'mutation_fixtures'}
    for record in value['files']:
        rel = Path(record['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'manifest topology')
        require(not excluded.intersection(rel.parts) and rel.suffix != '.pyc', 'private file')
        require(str(rel) not in seen and str(rel) != 'PUBLIC_FILES.json', 'manifest duplicate/self')
        path = folder / rel
        require(path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(folder), 'payload topology')
        actual = digest(path)
        require(actual == {'bytes': record['bytes'], 'sha256': record['sha256']}, 'payload binding')
        seen.add(str(rel))
        records.append({'case_relative_path': str(path.relative_to(CASE)), **actual})
        if rel.suffix == '.json':
            json.loads(path.read_text())  # Entire JSON parsed, no abbreviated metadata acceptance.
    return {'payloads': records, 'public_manifest': digest(folder / 'PUBLIC_FILES.json')}


def main():
    sealed = {name: manifest(name) for name in ('euler_adversary', 'reproduction')}
    receipt = load('SOURCE_RECEIPT.json')
    require(receipt['head_sha'] == HEAD and len(receipt['files']) == 27, 'source inventory')
    for record in receipt['files']:
        path = CASE / 'source_snapshot' / record['path']
        require(digest(path) == {'bytes': record['bytes'], 'sha256': record['sha256']}, 'frozen source changed')
    results = {name: load('reviews/' + name + '/RESULT.json') for name in sealed}
    for name, result in results.items():
        identity(result, name)
        require(type(result['blocking_issues']) is int and result['blocking_issues'] == 1, 'raw blockers')
        require(type(result['unresolved_mathematical_gaps']) is int and result['unresolved_mathematical_gaps'] == 0, 'raw math scope')
        require(result['asymptotic_proved'] is False, 'unproved asymptotic')
    require(results['euler_adversary']['required_repairs'] == 1, 'Euler raw repair')
    require(results['reproduction']['required_repairs'] == 3, 'reproduction raw repairs')
    e = [load('reviews/euler_adversary/CHECKS_' + mode + '.json') for mode in ('NORMAL', 'OPTIMIZED')]
    for i, value in enumerate(e):
        require(value['status'] == 'PASS' and value['check_count'] == 18078, 'Euler guard count')
        require(value['runtime_optimization'] == i, 'Euler mode')
        negatives = value['negative_controls']
        require(len(negatives) == 12 and len({r['name'] for r in negatives}) == 12, 'Euler controls')
        require(all(r['returncode'] == 1 and r['guard_rejected'] is True for r in negatives), 'Euler rejection')
    left, right = [dict(v) for v in e]
    left.pop('runtime_optimization'); right.pop('runtime_optimization')
    require(left == right, 'Euler mode semantic mismatch')
    baselines = load('reviews/reproduction/HISTORICAL_REPLAYS.json')
    identity(baselines, 'reproduction')
    require(len(baselines['records']) == 8 and all(r['returncode'] == 0 for r in baselines['records']), 'historical baselines')
    require(all(r.get('generated_exactly_frozen', True) and r.get('stdout_exactly_frozen', True) for r in baselines['records']), 'historical byte replay')
    invalid = load('reviews/reproduction/HISTORICAL_NEGATIVE_CONTROLS.json')
    identity(invalid, 'reproduction')
    require(len(invalid['records']) == 38 and invalid['cases_per_mode'] == 19, 'invalid execution count')
    historical_controls = []
    for mode in ('normal', 'optimized'):
        rows = [r for r in invalid['records'] if r['mode'] == mode]
        require(len(rows) == 19 and len({r['case'] for r in rows}) == 19, 'invalid case coverage')
        for r in rows:
            if mode == 'normal':
                require(r['returncode'] == 1 and r['stdout_bytes'] == 0 and 'AssertionError' in r['stderr'], 'normal intended assertion rejection')
            else:
                require(r['returncode'] == 0 and r['emitted_status'] == 'PASS' and r['inherited_PYTHONOPTIMIZE'] == '1', 'optimized false acceptance')
            historical_controls.append({k: r[k] for k in ('case', 'mode', 'returncode', 'stdout_bytes')})
        comparator = next(r for r in rows if r['case'] == 'publication_replay_generated_report_mismatch')
        if mode == 'normal':
            require('author/verify.py: replay report differs' in comparator['stderr'], 'actual replay comparator')
    require(sum(r.get('stdout_exactly_original_pass_report', False) for r in invalid['records']) == 8, 'invalid mathematical PASS bytes')
    fresh = load('reviews/reproduction/INDEPENDENT_CONTROL_RESULTS.json')
    identity(fresh, 'reproduction')
    require(len(fresh['records']) == 20 and fresh['negative_cases_per_mode'] == 9, 'fresh control count')
    fresh_controls = []
    for row in fresh['records']:
        if row['positive_baseline']:
            require(row['returncode'] == 0 and row['total_cases'] == 673, 'fresh baseline')
        else:
            require(row['returncode'] == 1 and row['stdout_bytes'] == 0 and 'RuntimeError: independent audit rejected:' in row['stderr'], 'fresh intended guard rejection')
        fresh_controls.append({k: row[k] for k in ('case', 'mode', 'returncode', 'stdout_bytes')})
    n = CASE / 'reviews/reproduction/INDEPENDENT_CHECKS_NORMAL.json'
    o = CASE / 'reviews/reproduction/INDEPENDENT_CHECKS_OPTIMIZED.json'
    require(n.read_bytes() == o.read_bytes() and len(n.read_bytes()) == 40017, 'fresh byte-stable modes')
    for name, scripts in {'euler_adversary': ['check_euler.py'], 'reproduction': ['verify_independent.py', 'run_independent_controls.py', 'replay_historical.py', 'test_historical_negative_controls.py']}.items():
        for script in scripts:
            tree = ast.parse((CASE / 'reviews' / name / script).read_text())
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), 'fresh scripts assert-based')
    report = {
        'recorded_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'pr': 458, 'problem_id': '20000693', 'frozen_head': HEAD,
        'status': 'SEALED_EVIDENCE_READBACK_WITH_RAW_FINDINGS_RETAINED',
        'sealed_families': sealed, 'frozen_source_files_verified_unchanged': 27,
        'root_entire_reports_results_manifests_and_five_control_scripts_read': True,
        'root_entire_euler_reconstruction_and_repair_read': True,
        'raw_counts': {name: {k: result[k] for k in ('blocking_issues', 'required_repairs', 'unresolved_mathematical_gaps')} for name, result in results.items()},
        'euler_guard_checks_per_mode': 18078, 'euler_controls_per_mode': 12,
        'historical_baselines': 8, 'historical_invalid_cases_per_mode': 19,
        'historical_normal_rejections': 19, 'historical_optimized_false_PASS': 19,
        'historical_invalid_math_scripts_same_PASS_bytes': 8,
        'historical_controls': historical_controls, 'fresh_reproduction_controls': fresh_controls,
        'fresh_reproduction_cases_per_mode': 673, 'fresh_reproduction_negatives_per_mode': 9,
        'fresh_reproduction_json': digest(n),
        'context_caveat': 'Both original families inherited full chat context; separately authored/tool-sequence evidence is not fully unprimed context.',
        'primary_range_correction': 'Sealed Euler X>2/excluded-endpoint label is incorrect; actual Sahay Theorem1.3 says X>=2. H1 and its correction remain valid.',
        'interpretation_only_source_repair_applied': False,
        'publication_package_approved': False, 'priority_approved': False,
        'operations_approved': False, 'new_original_proof_attempts': 0,
        'remaining_gap': 'Fresh whole and no-history mathematical rereviews, then deep priority; raw H1/V1/P2/C3 remain publication repairs if publication proceeds.'
    }
    (CASE / 'MATHEMATICAL_FAMILIES_READBACK.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'raw_counts', 'frozen_source_files_verified_unchanged', 'historical_optimized_false_PASS')}, indent=2))


if __name__ == '__main__':
    main()
