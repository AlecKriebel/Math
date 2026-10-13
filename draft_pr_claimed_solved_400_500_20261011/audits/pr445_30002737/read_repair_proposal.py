#!/usr/bin/env python3
"""Read back complete proposed repair without declaring independent approval."""
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
from read_initial_families import HERE, HEAD, digest, need, read


def main():
    root = HERE / 'verification_repair'
    manifest = read(root / 'PUBLIC_FILES.json')
    result = read(root / 'RESULT.json')
    need(len(manifest['files']) == 116 and len({r['path'] for r in manifest['files']}) == 116, 'Complete unique payloads')
    need(result['pr'] == 445 and result['problem_id'] == 30002737 and result['frozen_head'] == HEAD, 'Repair identity')
    need(result['reviewer'] == '/root/pr445_verification_repair', 'Repair author')
    need(result['proposed_repair_acceptance']['independently_accepted'] is False, 'Self-test not approval')
    need([result[k] for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']] == [1, 1, 0], 'Original raw counts')
    payloads = []
    for item in manifest['files']:
        relative = Path(item['path'])
        need(not relative.is_absolute() and not {'..', 'private', 'private_sources', 'private_cases', '__pycache__', '.venv', 'venv'}.intersection(relative.parts), 'Unsafe/private payload')
        file = root / relative
        need(file.is_file() and not file.is_symlink(), 'Missing/indirect payload')
        need(digest(file) == {k: item[k] for k in ['bytes', 'sha256']}, 'Repair payload binding')
        if file.suffix == '.json':
            read(file)
        if file.suffix == '.py' and 'frozen_history' not in relative.parts:
            need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(file.read_text()))), 'Supported assertion found')
        payloads.append({'path': item['path'], **digest(file)})
    source = read(HERE / 'SOURCE_RECEIPT.json')
    for item in source['files']:
        rel = Path(item['path']).relative_to('unsolved_math_prioritization/attempts/30002737')
        wanted = {k: item[k] for k in ['bytes', 'sha256']}
        need(digest(root / 'frozen_history' / rel) == wanted, 'Frozen-history copy changed')
        need(digest(HERE / 'source_snapshot' / item['path']) == wanted, 'Frozen original changed')
    for item in read(root / 'ATTRIBUTION.json')['inputs']:
        need(digest(HERE / item['case_relative_path']) == {k: item[k] for k in ['bytes', 'sha256']}, 'Attribution input binding')
    inspected = []
    for name, outer in [('matrix_01', 0), ('matrix_02_optimized_outer', 1)]:
        directory = root / 'records' / name
        summary = read(directory / 'SUMMARY.json')
        need(summary['suite_runtime']['optimization'] == outer, 'Outer suite mode')
        need(summary['baseline_runs'] == 2 and summary['actual_negative_runs'] == 42, 'Actual matrix counts')
        need(len(summary['run_records']) == len(set(summary['run_records'])) == 44, 'Matrix record count')
        baselines = []
        counts = {'mathematical': 0, 'semantic': 0, 'integrity': 0}
        actual = []
        for name in summary['run_records']:
            record = read(directory / name)
            need(name == record['name'] + '.json' and record['expectation_met'] is True, 'Run identity')
            need(record['sys_executable_pinned'] is True and record['command'][0] == summary['suite_runtime']['executable'], 'Pinned child')
            need(record['inherited_PYTHONOPTIMIZE'] == ('1' if record['name'].endswith('_optimized') else None), 'Child mode')
            need(' ' in record['cwd'] and ' ' in record['command'][1], 'Relocated spaces/cwd')
            if record['expected_rejection']:
                need(record['returncode'] == 1 and record['stdout'] == '', 'Actual negative failed')
                need(record['expected_error_substring'] in record['stderr'] and 'VERIFICATION_FAILED:' in record['stderr'], 'Wrong rejection guard')
                kind = 'integrity' if record['name'].startswith('integrity_') else 'semantic' if record['name'].startswith('fault_saved_') else 'mathematical'
                counts[kind] += 1
            else:
                value = json.loads(record['stdout'])
                need(record['returncode'] == 0 and record['stderr'] == '' and value['status'] == 'PASS', 'Actual positive failed')
                need(value['runtime']['executable'] == summary['suite_runtime']['executable'], 'Actual interpreter differs')
                need(value['runtime']['optimization'] == int(record['name'].endswith('_optimized')), 'Actual runtime mode')
                baselines.append(value)
            actual.append({'name': record['name'], 'returncode': record['returncode'], 'mode': record['inherited_PYTHONOPTIMIZE'], 'error': record['expected_error_substring']})
        need(counts == {'mathematical': 16, 'semantic': 4, 'integrity': 22}, 'Negative classes')
        need(read(directory / 'FINITE_RESULTS.json') == baselines[0], 'Finite result not actual stdout')
        for baseline in baselines:
            del baseline['runtime']
        need(baselines[0] == baselines[1], 'Positive finite outputs differ by mode')
        inspected.append({'matrix': directory.name, 'outer_optimization': outer, 'negative_classes': counts, 'actual_records': actual})
    replay = read(HERE / 'ROOT_REPAIR_REPLAY.json')
    need(replay['status'] == 'ROOT_REPLAY_EXPECTATIONS_MET' and replay['actual_baselines'] == 2 and replay['actual_negatives'] == 6, 'Root replay')
    for name, binding in replay['code_bindings'].items():
        need(digest(root / name) == binding, 'Root read/replay code not sealed proposal')
    outcome = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pr': 445, 'problem_id': '30002737', 'frozen_head': HEAD, 'status': 'COMPLETE_PROPOSAL_READBACK_PASS_NOT_INDEPENDENT_APPROVAL', 'payloads': payloads, 'matrix_readbacks': inspected, 'actual_author_baselines': 4, 'actual_author_negative_rejections': 84, 'root_additional_baselines': 2, 'root_additional_negative_rejections': 6, 'original_frozen_files_and_proposal_copies_match': 12, 'attribution_inputs_checked': 6, 'original_raw_counts_preserved': [1, 1, 0], 'fresh_whole_adversary_acceptance_pending': True, 'limit': 'Root read complete code/docs/report/result and parsed every raw matrix record, independently replayed exact core; publication/priority/whole-package approval remains separate.'}
    (HERE / 'REPAIR_PROPOSAL_READBACK.json').write_text(json.dumps(outcome, indent=2) + '\n')
    print(json.dumps({k: v for k, v in outcome.items() if k not in ['payloads', 'matrix_readbacks']}, indent=2))


if __name__ == '__main__':
    main()
