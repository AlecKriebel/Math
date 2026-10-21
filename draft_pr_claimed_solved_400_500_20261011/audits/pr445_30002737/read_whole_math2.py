#!/usr/bin/env python3
"""Parent readback of the genuine second whole review; never runs peer code."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json

CASE = Path(__file__).resolve().parent
REVIEW = CASE / 'reviews/whole_math_adversary2'
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
PINS = {
    'REPORT.md': '88587dbbf3ea641a232ee2c9714335b75fd76608e9decf141c662399dcbc6bd4',
    'RESULT.json': 'bebb5f4a5dd57cd1b3fcf5b5c2ebe288ef022fa930df6b0b47c1e67bbe4dd70d',
    'PUBLIC_FILES.json': '2009d518639b2bfbacaea7389172bf86da680406c5fbb727b021f57a09ecd37e',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def binding(root, row):
    rel = Path(row['path'])
    require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe bound path')
    path = root / rel
    require(path.is_file() and not path.is_symlink(), 'Missing/unsafe ' + str(rel))
    data = path.read_bytes()
    require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
            'Binding mismatch: ' + str(rel))
    return path


def raw_interpretations(value, label, rows):
    if isinstance(value, dict):
        if all(key in value for key in ('returncode', 'stdout', 'stderr')):
            out = value['stdout']
            parsed = None
            if isinstance(out, str) and out.strip():
                try:
                    parsed = json.loads(out)
                except json.JSONDecodeError:
                    parsed = {'not_one_JSON_value': True}
            rows.append({
                'input': label,
                'name': value.get('name', value.get('case', value.get('mutant'))),
                'returncode': value['returncode'],
                'optimization': value.get('inherited_PYTHONOPTIMIZE', value.get('optimized')),
                'stdout_status': parsed.get('status', parsed.get('verdict')) if isinstance(parsed, dict) else None,
                'stdout_bytes': len(out.encode()) if isinstance(out, str) else None,
                'stdout_sha256': hashlib.sha256(out.encode()).hexdigest() if isinstance(out, str) else None,
                'stderr': value['stderr'],
                'expected_rejection': value.get('expected_rejection'),
                'command': value.get('command'),
                'expected_error': value.get('expected_error_substring', value.get('expected_error')),
            })
        for key, child in value.items():
            if key not in ('stdout', 'stderr'):
                raw_interpretations(child, label + '/' + key, rows)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            raw_interpretations(child, label + '/' + str(index), rows)


def main():
    output = CASE / 'WHOLE_MATH2_READBACK.json'
    require(not output.exists(), 'Preserve previous parent readback')
    for name, digest in PINS.items():
        require(hashlib.sha256((REVIEW / name).read_bytes()).hexdigest() == digest, 'Sealed pin changed')
    index = load(REVIEW / 'PUBLIC_FILES.json')
    result = load(REVIEW / 'RESULT.json')
    keys = ('blocking_findings', 'required_repairs', 'central_mathematical_gaps')
    require(index['pr'] == result['pr'] == 445 and result['problem_id'] == 30002737
            and result['frozen_head'] == HEAD, 'Review identity mismatch')
    require(all(type(result[key]) is int and result[key] == 0 for key in keys), 'Current verdict mismatch')
    require([result['historical_original_R1_RR1'][key] for key in keys] == [1, 1, 0], 'History relabeled')
    require(len(index['files']) == 64 and len({r['path'] for r in index['files']}) == 64, 'Payload inventory')
    own_runs = []
    code = []
    for row in index['files']:
        path = binding(REVIEW, row)
        require(not any(p in ('private', 'private_sources', 'raw_original', '__pycache__')
                        for p in Path(row['path']).parts), 'Private payload selected')
        if path.suffix == '.py':
            count = sum(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text())))
            if row['path'] == 'controls/independent_whole_controls.py':
                require(count > 0 and row['classification'].startswith('preserved_normal_only'), 'Historical mode boundary')
            else:
                require(count == 0, 'Fresh controlling assert')
            code.append({'path': row['path'], 'sha256': row['sha256'], 'assertions': count})
        if path.suffix == '.json':
            value = load(path)
            if row['path'].startswith('records/interface_review/') and row['path'] != 'records/interface_review/SUMMARY.json':
                own_runs.append(value)
    exposed = load(REVIEW / 'EXPOSED_INPUT_BINDINGS.json')
    require(len(exposed['records']) == 212 and len(exposed['raw_subprocess_interpretation']) == 159, 'Exposed counts')
    foreign_runs = []
    for row in exposed['records']:
        path = binding(CASE, row)
        if path.suffix == '.json' and path.name != 'PUBLIC_FILES.json':
            raw_interpretations(load(path), row['path'], foreign_runs)
    require(foreign_runs == exposed['raw_subprocess_interpretation'], 'Foreign raw interpretation mismatch')
    require(len(own_runs) == 42 and len({row['name'] for row in own_runs}) == 42, 'Actual own records')
    source = CASE / 'source_snapshot/unsolved_math_prioritization/attempts/30002737/author/checks/verify_counterexample.py'
    original_mutant = source.read_text().replace('E = (F(1, 10), F(1, 10))', 'E = (F(1, 6), F(0))')
    old_digest = hashlib.sha256(original_mutant.encode()).hexdigest()
    current_digest = result['exact_current_package']['trust_anchor_sha256']
    guarded_digest = result['own_pre_exposure_normal_only_diagnostic']['separate_guarded_code_sha256']
    runtime = load(REVIEW / 'records/interface_review/SUMMARY.json')['python_executable']
    require(Path(runtime).is_absolute(), 'Nonabsolute runtime')
    baselines = []
    outcome_rows = []
    current_rejects = own_rejects = historical_false = 0
    for row in own_runs:
        name = row['name']
        optimized = name.endswith('_optimized')
        require(row['inherited_PYTHONOPTIMIZE'] == ('1' if optimized else None), 'Runtime mode mismatch')
        expected_digest = old_digest if name.startswith('original_') else guarded_digest if name.startswith('own_') else current_digest
        require(row['executed_sha256'] == expected_digest, 'Executed source mismatch: ' + name)
        require(type(row['returncode']) is int and row['command'][0] == runtime, 'Actual process record')
        if name.startswith(('baseline_', 'own_baseline_')):
            require(row['returncode'] == 0 and not row['stderr'], 'Baseline failed')
            parsed = json.loads(row['stdout'])
            require(parsed.get('status', parsed.get('verdict')) in ('pass', 'PASS'), 'Baseline status')
            if name.startswith('baseline_'):
                del parsed['runtime']
                baselines.append(parsed)
            else:
                require(parsed['flow_partition_cases'] == 4680 and parsed['source_substitution_sites'] == 65536
                        and sum(r['physical_displacements'] for r in parsed['actual_crop_records']) == 1625,
                        'Owned finite count mismatch')
        elif name == 'original_bad_marker_optimized':
            require(row['returncode'] == 0 and row['expected_historical_false_success']
                    and json.loads(row['stdout'])['status'] == 'pass', 'Historical false pass lost')
            historical_false += 1
        else:
            require(row['returncode'] != 0 and not row['stdout'] and row['expected_error'] in row['stderr'],
                    'Raw rejection mismatch: ' + name)
            if name.startswith('own_'):
                own_rejects += 1
            elif not name.startswith('original_'):
                current_rejects += 1
        outcome_rows.append({'name': name, 'optimized': optimized, 'returncode': row['returncode'],
                             'executed_sha256': expected_digest, 'stdout_empty': not bool(row['stdout']),
                             'intended_error_present': bool(row['expected_error']) and row['expected_error'] in row['stderr']})
    require(baselines[0] == baselines[1] and (current_rejects, own_rejects, historical_false) == (30, 6, 1), 'Outcome totals')
    record = {
        'utc': datetime.now(timezone.utc).isoformat(), 'pr': 445, 'problem_id': 30002737,
        'frozen_head': HEAD, 'parent': '/root', 'sealed_pins': PINS,
        'positive_payloads_verified': 64, 'exposed_bindings_verified': 212,
        'foreign_raw_interpretations_reconstructed': 159, 'actual_own_records_verified': 42,
        'current_complete_review_counts': [0, 0, 0], 'original_historical_counts': [1, 1, 0],
        'supported_invalid_rejections': 30, 'own_guarded_invalid_rejections': 6,
        'historical_optimized_false_successes_preserved': 1,
        'fresh_controlling_code': code, 'actual_outcomes': outcome_rows,
        'parent_full_report_result_code_read': True,
        'parent_reader_preseal_correction': 'First readback incorrectly required runtime filename python3; actual sys.executable is versioned. Corrected to equality with sealed summary runtime before writing any success record. Candidate/review bytes unchanged.',
        'scope': 'Exact frozen planar theorem and exact supported replacement interface accepted. Priority, a future paper/package, and live action gates remain outstanding. No peer scripts executed by this reader; no proof attempt or external mutation.',
    }
    output.write_text(json.dumps(record, indent=2) + '\n')
    require(load(output) == record, 'Parent write/read mismatch')
    print(json.dumps({k: v for k, v in record.items() if k not in ('actual_outcomes', 'fresh_controlling_code')}, indent=2))


if __name__ == '__main__':
    main()
