#!/usr/bin/env python3
"""Independent read-only original/Git/full-corpus/native provenance reproduction.

Called only by the root-owned collector, against its exact private hierarchy.
It imports only the pinned queue module and calls its pure score function.
It never calls sync/rank/status/turn or creates a historical worker transcript.
"""
import argparse
from collections import Counter
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sqlite3
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--pins', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert not sys.flags.optimize
    sys.dont_write_bytecode = True
    repo = args.repo.resolve()
    pins = json.loads(args.pins.read_bytes())
    audit = repo/pins['audit_relative_path']
    source, native = audit/'source_snapshot', repo/'unsolved_math_prioritization'
    sha = lambda data: hashlib.sha256(data).hexdigest()
    load = lambda path: json.loads(path.read_bytes())
    git = lambda *parts: subprocess.check_output(['git', *parts], cwd=repo)
    assert git('branch', '--show-current').strip() == b'main'
    manifest = load(audit/'snapshot_manifest.json')
    assert manifest['head'] == pins['head'] and manifest['base'] == pins['base']
    assert len(manifest['files']) == 16 and len(manifest['changed_paths']) == 17
    tree_rows = []
    for record in manifest['files']:
        path = 'unsolved_math_prioritization/attempts/2765/'+record['path']
        data = (source/record['path']).read_bytes()
        assert len(data) == record['size'] and sha(data) == record['sha256']
        assert git('show', pins['head']+':'+path) == data
        tree = git('ls-tree', pins['head'], '--', path).decode().strip()
        assert tree == record['mode']+' blob '+record['git_blob']+'\t'+path
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == record['git_blob']
        tree_rows.append({'path': path, 'mode': record['mode'], 'git_blob': record['git_blob'],
                          'size': len(data), 'sha256': sha(data)})
        if record['path'].endswith('.json'):
            json.loads(data)
    assert git('diff', '--name-only', pins['base'], pins['head']).decode().splitlines() == manifest['changed_paths']
    assert git('diff', pins['base'], pins['head']) == (audit/'pr_input/diff.patch').read_bytes()
    historical_queue = git('show', pins['head']+':unsolved_math_prioritization/QUEUE.md')
    historical_rows = [line for line in historical_queue.decode().splitlines() if '| 2765 / KP-2.17 |' in line]
    assert len(historical_rows) == 1 and '| unsolved | 2/5 |' in historical_rows[0]

    upstream = load(native/'manifest.json')
    assert upstream == pins['corpus']
    raw = {}
    for name, record in upstream['files'].items():
        data = (native/'cache'/name).read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256']
        raw[name] = json.loads(data)
    assert sum(record['bytes'] for record in upstream['files'].values()) == 149266659
    problems, reports = raw['problems.json'], raw['research_results.json']
    assert len(problems) == 15458 and len(reports) == 6701
    ids = [str(problem['id']) for problem in problems]
    assert len(set(ids)) == len(ids)
    counts = Counter(problem['problem_number'] for problem in problems)
    selected = [problem for problem in problems if problem['id'] == 2765]
    assert len(selected) == 1
    problem = selected[0]
    assert problem == load(source/'source_record.json') and counts['KP-2.17'] == 1
    assert 'KP-2.17' not in reports and (source/'prior_report.json').read_bytes() == b'null\n'
    assert load(source/'prior_report.json') is None
    imported_prior = reports.get('KP-2.17', {})
    assert imported_prior == {} and sha(json.dumps(imported_prior, sort_keys=True).encode()) != sha(b'null')

    code = (native/'queue.py').read_text()
    importer_definitions = ["counts=collections.Counter(p['problem_number'] for p in problems)",
                            "if counts[p['problem_number']]>1 and p['problem_number'] in reports: p['_ambiguous_report']=True",
                            "json.dumps({} if p.get('_ambiguous_report') else reports.get(p['problem_number'],{}))"]
    assert all(fragment in code for fragment in importer_definitions), 'Importer schema drift requires root review'
    expected = {}
    for item in problems:
        payload = copy.deepcopy(item)
        if counts[payload['problem_number']] > 1 and payload['problem_number'] in reports:
            payload['_ambiguous_report'] = True
        prior = {} if payload.get('_ambiguous_report') else reports.get(payload['problem_number'], {})
        expected[str(payload['id'])] = (payload, prior)
    database = native/'cache/catalog.sqlite'
    connection = sqlite3.connect(database.as_uri()+'?mode=ro&immutable=1', uri=True)
    connection.execute('PRAGMA query_only=ON')
    assert connection.execute('SELECT revision FROM metadata').fetchall() == [(upstream['revision'],)]
    seen = set()
    for key, payload, prior in connection.execute('SELECT key,payload,report FROM records ORDER BY key'):
        assert key not in seen and key in expected
        assert (json.loads(payload), json.loads(prior)) == expected[key], key
        seen.add(key)
    assert seen == set(expected) and len(seen) == 15458
    connection.close()
    spec = importlib.util.spec_from_file_location('root_pinned_pr38_pure_queue', native/'queue.py')
    queue = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(queue)
    score = queue.score(problem, imported_prior, load(native/'policy.json'))
    assert score['statement_hash'] == sha(problem['statement'].encode())
    assert score['review_hash'] == sha(json.dumps([problem, imported_prior], sort_keys=True).encode())
    assert score == load(audit/'primary_scope_family/raw_importer_pin.json')['pure_queue_score']

    attempt, turns, review = load(source/'attempt.json'), load(source/'turns.json'), load(source/'review/review_summary.json')
    assert attempt['id'] == '2765' and attempt['problem_number'] == 'KP-2.17'
    assert attempt['substantive_attempts_used'] == len(turns) == 2
    assert attempt['substantive_attempt_limit'] == 5 and [x['turn'] for x in turns] == [1, 2]
    assert not attempt['full_closed_surface_resolution_claimed'] and not attempt['novel_result_claimed']
    assert attempt['results_sha256'] == review['author_sha256'] == sha((source/'RESULTS.md').read_bytes())
    for name, digest in review['files'].items():
        assert sha((source/'review'/name).read_bytes()) == digest
    state = load(native/'state.json')
    catalog = [row for row in load(native/'catalog.json') if row['id'] == '2765']
    history = [json.loads(line) for line in (native/'history.jsonl').read_text().splitlines()
               if line and str(json.loads(line).get('id')) == '2765']
    queue_rows = [line for line in (native/'QUEUE.md').read_text().splitlines() if '| 2765 / KP-2.17 |' in line]
    assert '2765' not in state and history == []
    assert len(catalog) == 1 and catalog[0]['local_status'] == 'queued' and catalog[0]['turns_used'] == 0
    assert len(queue_rows) == 1 and '| queued | 0/5 |' in queue_rows[0]
    result = {'status': 'PASS_READONLY_PROVENANCE_REPRODUCTION', 'head': pins['head'], 'base': pins['base'],
              'runtime_python_version': sys.version, 'runtime_actual_executable': sys.executable,
              'original_git_files': tree_rows, 'changed_diff_paths': manifest['changed_paths'],
              'historical_head_queue_sha256': sha(historical_queue), 'historical_head_queue_target_row': historical_rows[0],
              'raw_corpus_bytes': 149266659, 'problem_count': 15458, 'research_report_count': 6701,
              'full_raw_and_SQL_importer_join_checked': True, 'SQL_mode': 'ro, immutable, query_only',
              'SQL_revision': upstream['revision'], 'importer_source_fragments': importer_definitions,
              'complete_flat_problem': problem, 'prior_raw_key_present': False, 'original_prior_literal': None,
              'raw_and_SQL_full_problem_equal_snapshot': True, 'complete_flat_source_record_preserved': True,
              'native_importer_prior_fallback': imported_prior, 'pure_queue_score': score,
              'prior_qualification': 'Missing raw research key; original null records absence. Native importer {} is a fallback, with different serialized value and status semantics. Neither is a retrieved report.',
              'authored_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
              'current_native_target': {'state': None, 'history_events': history, 'catalog': catalog[0], 'queue_row': queue_rows[0]},
              'historical_worker_transcript': pins['historical_worker_transcript_status'],
              'scope': 'Source/Git/accounting/importer/full-corpus provenance only. No hidden-turn inference, imported-primary reading claim, mathematical verdict or novelty claim.'}
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
