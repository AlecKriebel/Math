#!/usr/bin/env python3
"""Read-only root validation of sealed PR445 families and actual run records.

This checks records and their preserved fixtures; it neither reruns them nor
turns a finite diagnostic into a proof or a publication approval.
"""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEAD = '3242c84e06db7e99012c7fe581adde5c3f89fc89'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def read(path):
    return json.loads(path.read_text())


def main():
    families = {}
    for name, count, verdict in [('geometry_scope', 8, [0, 0, 0]),
                                  ('spectral_adversary', 6, [0, 0, 0]),
                                  ('reproduction', 40, [1, 1, 0])]:
        root = HERE / 'reviews' / name
        index = read(root / 'PUBLIC_FILES.json')
        result = read(root / 'RESULT.json')
        need(index['pr'] == result['pr'] == 445, 'PR identity')
        need(str(index['problem_id']) == str(result['problem_id']) == '30002737', 'Problem identity')
        need(index['frozen_head'] == result['frozen_head'] == HEAD, 'Frozen identity')
        need(index['reviewer'] == result['reviewer'] == '/root/pr445_' + name, 'Reviewer identity')
        counts = [result[k] for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']]
        need(all(type(x) is int for x in counts) and counts == verdict, 'Raw verdict changed')
        entries = index['files']
        need(len(entries) == count, 'Payload count')
        seen = set()
        observed = []
        for item in entries:
            relative = item.get('review_relative_path', item['path'])
            rel = Path(relative)
            need(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path')
            need(not {'private', 'private_sources', 'private_cases', 'mutation_fixtures', '__pycache__', '.venv', 'venv'}.intersection(rel.parts), 'Private payload')
            path = root / rel
            need(path.is_file() and not path.is_symlink() and relative not in seen, 'Missing/indirect/duplicate payload')
            seen.add(relative)
            actual = digest(path)
            need(actual == {k: item[k] for k in actual}, 'Payload hash/length: ' + relative)
            if path.suffix == '.json':
                read(path)  # Parse every complete JSON payload, including each raw run.
            if path.suffix == '.py':
                need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(path.read_text()))), 'Fresh controlling assert')
            observed.append({'path': relative, **actual})
        families[name] = {'raw_counts': counts, 'manifest': digest(root / 'PUBLIC_FILES.json'), 'verified_payloads': observed}

    source_receipt = read(HERE / 'SOURCE_RECEIPT.json')
    source = HERE / 'source_snapshot/unsolved_math_prioritization/attempts/30002737'
    reproduction = HERE / 'reviews/reproduction'
    remote = read(reproduction / 'records/frozen_remote_provenance.json')
    need(remote['frozen_head'] == HEAD and remote['verified_count'] == 12 and remote['failed_count'] == 0, 'Remote counts')
    expected = {x['path']: x for x in source_receipt['files']}
    need(len(expected) == len(remote['files']) == 12, 'Remote unique count')
    for item in remote['files']:
        need(item['status'] == 'verified' and item['http_status'] == 200 and item['matches_receipt'] is True, 'Remote status')
        need(HEAD in item['requested_url'] and item['requested_url'].endswith(item['path']), 'Remote URL')
        want = {k: expected[item['path']][k] for k in ['bytes', 'sha256']}
        need({k: item[k] for k in want} == want, 'Remote metadata')
        need(digest(reproduction / 'private/frozen_remote' / item['path']) == want, 'Preserved remote blob')
        need(digest(HERE / 'source_snapshot' / item['path']) == want, 'Root frozen blob')

    raw = []
    for name in sorted((reproduction / 'records').glob('*.json')):
        record = read(name)
        if not isinstance(record, dict) or 'script' not in record:
            continue
        need(record['name'] == name.stem and type(record['returncode']) is int, 'Run identity/type')
        optimized = name.stem.endswith('_optimized')
        need(record['inherited_PYTHONOPTIMIZE'] == ('1' if optimized else None), 'Actual optimization mode')
        fixture = reproduction / 'private/replays' / name.stem
        script = fixture / record['script']
        need(script.is_file(), 'Executed script fixture absent')
        mutation = record.get('mutation')
        if isinstance(mutation, dict):
            original = (source / record['script']).read_text()
            need(original.count(mutation['old']) == 1, 'Mutation anchor not unique')
            need(script.read_text() == original.replace(mutation['old'], mutation['new']), 'Mutation fixture differs')
        if name.stem.startswith('baseline_'):
            need(record['returncode'] == 0 and record['stderr'] == '' and record['adjacent_output_byte_identical'] is True, 'Baseline status')
            output = 'author/checks/verification_results.json' if 'baseline_author_' in name.stem else 'audit/independent_controls_results.json'
            need((fixture / output).read_bytes() == (source / output).read_bytes(), 'Actual baseline output differs')
            need(record['stdout'] == (source / output).read_text(), 'Baseline stdout differs')
        else:
            need(record['expected_rejection'] is True, 'Missing negative intent')
            expected_rc = 1 if not optimized or mutation == 'missing_expected_results' else 0
            need(record['returncode'] == expected_rc, 'Raw rejection/false-success count')
            if expected_rc == 1:
                need(('FileNotFoundError' if mutation == 'missing_expected_results' else 'AssertionError') in record['stderr'], 'Unexpected failure guard')
            else:
                need(record['stderr'] == '', 'Unexpected false-success stderr')
                parsed = json.loads(record['stdout'])
                need(parsed.get('status') == 'pass' or parsed.get('verdict') == 'PASS', 'False success not PASS')
            if mutation == 'manifest_hash_mismatch':
                need(read(fixture / 'author/MANIFEST.json')['files']['checks/verify_counterexample.py']['sha256'] == '0' * 64, 'Hash mutant missing')
            elif mutation == 'replay_result_mismatch':
                saved = fixture / 'author/checks/verification_results.json'
                need(read(saved)['density'] == '300', 'Saved-result mutant missing')
                manifest = read(fixture / 'author/MANIFEST.json')['files']['checks/verification_results.json']
                need({k: manifest[k] for k in ['bytes', 'sha256']} == digest(saved), 'Saved-result re-signing missing')
            elif mutation == 'missing_expected_results':
                need(not (fixture / 'author/checks/verification_results.json').exists(), 'Missing-file mutant exists')
        if record['stdout_json'] is not None:
            need(record['stdout_json'] == json.loads(record['stdout']), 'Parsed stdout inconsistent')
        raw.append({'name': name.stem, 'optimized': optimized, 'returncode': record['returncode'], 'expected_rejection': record.get('expected_rejection', False), 'stderr_final_line': record['stderr'].splitlines()[-1] if record['stderr'] else None, 'executed_fixture': digest(script)})
    need(len(raw) == 24, 'Expected four original baselines and twenty negatives')
    new = read(reproduction / 'records/independent_exact_controls.json')
    need(len(new['runs']) == 12 and new['baseline_runs'] == 2 and new['negative_runs'] == new['negative_runs_rejected'] == 10, 'Fresh finite run counts')
    need(new['runs'][0]['stdout'] == new['runs'][1]['stdout'], 'New mode baseline mismatch')
    guards = {'marker': 'Marker is ambiguous', 'moments': 'Occupancy coefficient differs', 'normalization': 'normalization fails', 'flow': 'Floor-bin triangle fails', 'cocycle': 'Suspension action cocycle fails'}
    for i, run in enumerate(new['runs']):
        need(run['inherited_PYTHONOPTIMIZE'] == ('1' if i % 2 else None), 'New mode mismatch')
        if run['mutant'] is None:
            need(run['returncode'] == 0 and json.loads(run['stdout'])['status'] == 'pass' and run['stderr'] == '', 'New finite baseline')
        else:
            need(run['returncode'] == 1 and 'ValueError: ' in run['stderr'] and guards[run['mutant']] in run['stderr'], 'New finite negative wrong guard')

    geometry_root = HERE / 'reviews/geometry_scope'
    acquisition = read(geometry_root / 'SOURCE_ACQUISITION.json')
    for item in acquisition['source_pdfs'] + acquisition['renders']:
        need(digest(geometry_root / item['private_file']) == {k: item[k] for k in ['bytes', 'sha256']}, 'Geometry private input binding')
    provenance = read(reproduction / 'records/source_provenance.json')
    for item in provenance['sources']:
        need(item['http_status'] == 200 and item['matches_historical_hash'] is True, 'Primary acquisition status')
        need(digest(reproduction / 'private/sources' / (item['name'] + '.pdf')) == {k: item[k] for k in ['bytes', 'sha256']}, 'Reproduction primary binding')
    outcome = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pr': 445, 'problem_id': '30002737', 'frozen_head': HEAD, 'families': families, 'original_runs': raw, 'new_finite_runs': {'positive': 2, 'negative': 10, 'all_expected_outcomes_checked': True}, 'remote_frozen_bindings_checked': 12, 'geometry_private_pdf_render_bindings_checked': 12, 'reproduction_primary_pdf_bindings_checked': 3, 'claim_limit': 'Root readback of complete sealed artifacts and preserved run fixtures; no new subprocess replay, priority certificate, supported-integrity-interface approval, or infinite proof from finite tests. Original reproduction raw verdict remains 1/1/0.', 'status': 'READBACK_PASS'}
    (HERE / 'INITIAL_FAMILIES_READBACK.json').write_text(json.dumps(outcome, indent=2) + '\n')
    print(json.dumps({'status': outcome['status'], 'payloads_verified': 54, 'original_records_verified': 24, 'fresh_finite_records_verified': 12, 'original_optimized_false_passes': 9, 'original_raw_verdict': [1, 1, 0]}, indent=2))


if __name__ == '__main__':
    main()
