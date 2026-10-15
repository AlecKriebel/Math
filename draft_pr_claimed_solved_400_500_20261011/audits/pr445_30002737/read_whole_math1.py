#!/usr/bin/env python3
"""Root readback of the complete failed initial whole-package review."""
import ast
from datetime import datetime, timezone
import json
from pathlib import Path
from read_initial_families import HERE, HEAD, digest, need, read


def main():
    root = HERE / 'reviews/whole_math_adversary'
    index = read(root / 'PUBLIC_FILES.json')
    result = read(root / 'RESULT.json')
    need(result['pr'] == index['pr'] == 445 and result['frozen_head'] == index['frozen_head'] == HEAD, 'Identity')
    need(result['reviewer'] == index['reviewer'] == '/root/pr445_whole_math_adversary', 'Reviewer')
    need([result[k] for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']] == [1, 1, 0], 'Original failure history')
    need(result['publication_acceptance'] is False, 'Not a publication approval')
    need(len(index['files']) == 28 and len({x['path'] for x in index['files']}) == 28, 'Complete unique payloads')
    bindings = []
    for item in index['files']:
        rel = Path(item['path'])
        need(not rel.is_absolute() and not {'..', 'private', '__pycache__', '.venv', 'venv'}.intersection(rel.parts), 'Positive path')
        path = root / rel
        need(path.is_file() and not path.is_symlink(), 'Direct payload')
        need(digest(path) == {k: item[k] for k in ['bytes', 'sha256']}, 'Payload binding')
        if path.suffix == '.json':
            read(path)
        if path.suffix == '.py':
            need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(path.read_text()))), 'New essential assert')
        bindings.append({'path': item['path'], **digest(path)})
    exposed = read(root / 'INPUT_BINDINGS.json')
    need(len(exposed['records']) == 74 and exposed['all_originals_match_git'] == 12, 'Exposed counts')
    for item in exposed['records']:
        need(digest(HERE / item['path']) == {k: item[k] for k in ['bytes', 'sha256']}, 'Exposed record drift: ' + item['path'])
    initial = read(root / 'INITIAL_BINDINGS.json')
    need(len(initial['records']) == 14, 'Initial count')
    for item in initial['records']:
        need(digest(Path(item['path'])) == {k: item[k] for k in ['bytes', 'sha256']}, 'Initial input drift')
    initial_sha = '630b044983db4deb7a695037ce1ed49d2a193498cded21cf345b9054c95e3fa4'
    need(digest(root / 'INITIAL_RECONSTRUCTION.md')['sha256'] == initial_sha, 'Independent initial drift')
    records = []
    for file in sorted((root / 'records').glob('*.json')):
        item = read(file)
        if 'case' not in item:
            continue
        command = item['command']
        code = Path(command[-1])
        need(code.is_file() and str(code).startswith(str(root.resolve())), 'Actual fixture location')
        need(digest(code) == {'bytes': item['executed_bytes'], 'sha256': item['executed_sha256']}, 'Actual fixture hash')
        optimized = file.stem.endswith('_optimized')
        need(('-O' in command) == optimized, 'Actual command optimization')
        original_bad = file.stem.startswith('original_bad_')
        bad_fresh = file.stem.startswith('fresh_bad_')
        expected_rc = 1 if bad_fresh or (original_bad and not optimized) else 0
        need(item['returncode'] == expected_rc, 'Raw return code')
        if expected_rc == 1:
            need(item['stdout'] == '' and ('ValueError: marker collision' if bad_fresh else 'AssertionError') in item['stderr'], 'Wrong failure guard')
        else:
            parsed = json.loads(item['stdout'])
            need(parsed.get('status') in ['pass', 'PASS'] and item['stderr'] == '', 'PASS baseline/false success')
        records.append({'case': item['case'], 'optimized': optimized, 'returncode': item['returncode'], 'executed_sha256': item['executed_sha256'], 'stderr_final_line': item['stderr'].splitlines()[-1] if item['stderr'] else None})
    need(len(records) == 11, 'Eleven own raw records')
    peer = read(root / 'records/peer_proposal_replay.json')
    need(peer['original_publication_RR1_fully_repaired'] is False and len(peer['records']) == 12, 'Narrow finite proposal scope')
    need(peer['peer_code_sha256'] == digest(HERE / 'reviews/reproduction/exact_controls.py')['sha256'], 'Exact proposal version')
    need(peer['records'][0]['stdout'] == peer['records'][1]['stdout'], 'Proposal baseline equality')
    for i, run in enumerate(peer['records']):
        need(run['optimized'] == bool(i % 2), 'Proposal mode')
        if run['mutant'] is None:
            need(run['returncode'] == 0 and json.loads(run['stdout'])['status'] == 'pass' and run['stderr'] == '', 'Proposal baseline')
        else:
            need(run['returncode'] == 1 and run['stdout'] == '' and 'ValueError:' in run['stderr'], 'Proposal explicit negative')
    outcome = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pr': 445, 'problem_id': '30002737', 'frozen_head': HEAD, 'status': 'READBACK_PASS_ORIGINAL_FAILURE_PRESERVED', 'reviewer': result['reviewer'], 'raw_counts': [1, 1, 0], 'mathematical_claim_counts': [0, 0, 0], 'payloads': bindings, 'exposed_input_bindings': 74, 'initial_input_bindings': 14, 'own_subprocess_records': records, 'peer_proposal_replays': 12, 'future_integrated_verifier_reviewed': False, 'publication_acceptance': False, 'limit': 'Entire report and code read by root; byte and raw-record readback only, no additional subprocess replay or novelty certificate.'}
    (HERE / 'WHOLE_MATH1_READBACK.json').write_text(json.dumps(outcome, indent=2) + '\n')
    print(json.dumps({k: v for k, v in outcome.items() if k not in ['payloads', 'own_subprocess_records']}, indent=2))


if __name__ == '__main__':
    main()
