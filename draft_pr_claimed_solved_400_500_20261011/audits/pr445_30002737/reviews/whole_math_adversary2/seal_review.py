#!/usr/bin/env python3
"""Seal only the positive owned allowlist, keeping foreign fixture bytes private.

This publication index is custody evidence; it cannot bless changed trusted code.
The original normal-only diagnostic remains explicit, immutable historical evidence.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'
PINS = {
    'INITIAL_RECONSTRUCTION.md': '81ec5bf6eded3a9fc117a23bc8c5ae0b8fd1d350eb3dc8a06b948c4850d325b3',
    'controls/independent_whole_controls.py': '7e2229db5fc79b13d3f2ce897a7b9b7c1307a00bbaccbb77582ebbdc729a91c3',
    'controls/independent_whole_controls_guarded.py': 'dac860e3fb7fb31be30eb76ba83783a5532cb54ff2e71483136f415e75f032d4',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_bytes())


def main():
    for rel, expected in PINS.items():
        require(digest(HERE / rel) == expected, 'Protected checkpoint changed: ' + rel)
    result = load(HERE / 'RESULT.json')
    require(result['pr'] == 445 and result['problem_id'] == 30002737 and result['frozen_head'] == HEAD,
            'Identity mismatch')
    counts = ('blocking_findings', 'required_repairs', 'central_mathematical_gaps')
    require(all(type(result[key]) is int and result[key] == 0 for key in counts),
            'Current whole-review count mismatch')
    history = result['historical_original_R1_RR1']
    require([history[key] for key in counts] == [1, 1, 0], 'Historical counts relabeled')
    require(not history['original_scripts_safe_under_optimization'] and not history['original_scripts_repaired'],
            'Original safety history relabeled')
    bindings = load(HERE / 'EXPOSED_INPUT_BINDINGS.json')
    require(len(bindings['records']) == 212 and len(bindings['raw_subprocess_interpretation']) == 159,
            'Exposed evidence count mismatch')
    for row in bindings['records']:
        rel = Path(row['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe bound path')
        path = CASE / rel
        require(path.is_file() and not path.is_symlink(), 'Missing bound file: ' + str(rel))
        require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                'Reviewed exposed bytes changed: ' + str(rel))

    payloads = [
        'REPORT.md', 'RESULT.json', 'RESEARCH_LOG.md',
        'INITIAL_RECONSTRUCTION.md', 'INITIAL_RECONSTRUCTION_BINDING.json',
        'FROZEN_READ_RECEIPT.json', 'PRIMARY_SOURCES.json', 'EXPOSED_INPUT_BINDINGS.json',
        'bind_exposed_inputs.py', 'run_repair_review.py', 'seal_review.py',
        'controls/independent_whole_controls.py',
        'controls/independent_whole_controls_results.json',
        'controls/make_guarded_controls.py',
        'controls/independent_whole_controls_guarded.py',
        'controls/independent_whole_controls_guarded_results.json',
        'controls/ORIGINAL_REPLAY.json',
        'controls/original_verify_counterexample.stdout.txt',
        'controls/original_verify_counterexample.stderr.txt',
        'controls/original_independent_controls.stdout.txt',
        'controls/original_independent_controls.stderr.txt',
        'records/interface_review/SUMMARY.json',
    ]
    mathematical = ('marker', 'correlation', 'normalization', 'flow', 'cocycle', 'rs',
                    'physical_pairs', 'subdivision', 'saved_author_semantic', 'saved_independent_semantic')
    integrity = ('same_length_proof', 'missing_result', 'extra_source', 'resealed_wrong_result', 'code_byte')
    actual = []
    for mode in ('normal', 'optimized'):
        actual.append('baseline_' + mode)
        actual.extend(fault + '_' + mode for fault in mathematical + integrity)
        actual.append('original_bad_marker_' + mode)
        actual.append('own_baseline_' + mode)
        actual.extend('own_' + fault + '_' + mode for fault in ('marker', 'physical_pairs', 'section'))
    require(len(actual) == 42 and len(set(actual)) == 42, 'Raw record inventory mistake')
    payloads.extend('records/interface_review/' + name + '.json' for name in actual)
    require(len(payloads) == len(set(payloads)), 'Duplicate public selection')
    summary = load(HERE / 'records/interface_review/SUMMARY.json')
    require(summary['raw_record_count'] == 42 and summary['actual_current_negatives'] == 30,
            'Raw summary mismatch')
    current_baselines = []
    for name in actual:
        row = load(HERE / 'records/interface_review' / (name + '.json'))
        require(type(row['returncode']) is int and row['name'] == name, 'Bad actual run record')
        mode = 'optimized' if name.endswith('_optimized') else 'normal'
        require(row['inherited_PYTHONOPTIMIZE'] == ('1' if mode == 'optimized' else None),
                'Actual run-mode mismatch')
        if name.startswith('baseline_') or name.startswith('own_baseline_'):
            require(row['returncode'] == 0 and not row['stderr'], 'Failed actual baseline')
            output = json.loads(row['stdout'])
            require(output.get('status', output.get('verdict')) in ('pass', 'PASS'), 'Missing baseline success')
            if name.startswith('baseline_'):
                del output['runtime']
                current_baselines.append(output)
        elif name == 'original_bad_marker_optimized':
            require(row['returncode'] == 0 and row['expected_historical_false_success'],
                    'Historical false success relabeled')
            require(json.loads(row['stdout'])['status'] == 'pass', 'Historical raw false success absent')
        else:
            require(row['returncode'] != 0 and not row['stdout'] and row['expected_error'] in row['stderr'],
                    'Actual rejecting record mismatch: ' + name)
    require(current_baselines[0] == current_baselines[1], 'Finite baseline mismatch')

    files = []
    for rel in payloads:
        relative = Path(rel)
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe public path')
        require(not any(part in ('private', 'private_sources', 'raw_original', '__pycache__') for part in relative.parts),
                'Foreign/private bytes selected')
        path = HERE / rel
        require(path.is_file() and not path.is_symlink(), 'Public payload missing/unsafe: ' + rel)
        classification = 'positive_owned_payload'
        if rel in ('controls/independent_whole_controls.py', 'controls/independent_whole_controls_results.json'):
            classification = 'preserved_normal_only_historical_diagnostic_not_supported_optimized'
        if rel.startswith('records/interface_review/original_bad_marker_'):
            classification = 'owned_actual_historical_failure_replay_not_current_acceptance'
        if rel.endswith('.py') and rel != 'controls/independent_whole_controls.py':
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text()))),
                    'Essential own assertion: ' + rel)
        if rel.endswith('.json'):
            load(path)
        files.append({'path': rel, 'bytes': path.stat().st_size, 'sha256': digest(path),
                      'classification': classification})
    public = {'schema_version': 1, 'pr': 445, 'problem_id': 30002737, 'frozen_head': HEAD,
              'reviewer': '/root/pr445_whole_math_adversary2',
              'utc': datetime.now(timezone.utc).isoformat(),
              'policy': 'Positive complete owned allowlist with all authored controlling code, results and actual raw records. Normal-only original own diagnostic is explicitly historical. No self-hash or foreign PDF/extract/render/copied original/repair/mutant fixture/cache/environment bytes. Input bindings are owned custody and structured interpretation metadata.',
              'files': files}
    (HERE / 'PUBLIC_FILES.json').write_text(json.dumps(public, indent=2) + '\n')
    reread = load(HERE / 'PUBLIC_FILES.json')
    require(len(reread['files']) == len(files), 'Public write/read mismatch')
    for row in reread['files']:
        path = HERE / row['path']
        require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'], 'Public readback failed')
    print(json.dumps({'payloads': len(files), 'current_counts': [result[key] for key in counts],
                      'historical_counts': [history[key] for key in counts],
                      'report_sha256': digest(HERE / 'REPORT.md'), 'result_sha256': digest(HERE / 'RESULT.json'),
                      'public_index_sha256': digest(HERE / 'PUBLIC_FILES.json'),
                      'all_payloads_readback': True, 'exposed_input_hashes_unchanged': True}, indent=2))


if __name__ == '__main__':
    main()
