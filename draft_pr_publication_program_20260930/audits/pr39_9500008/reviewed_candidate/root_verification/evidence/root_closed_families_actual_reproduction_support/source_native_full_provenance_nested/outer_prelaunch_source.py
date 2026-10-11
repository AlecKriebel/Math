#!/usr/bin/env python3
"""Read-only root PR39 provenance reproduction, never a mathematical verdict.

Root runs this only in the collector's private exact repository hierarchy.
Full raw records and every SQL row are checked before the actual selected
present report and pure queue.score pair are checked. No queue mutation runs.
"""
import argparse
from collections import Counter
import copy
import datetime
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
    prefix = 'unsolved_math_prioritization/attempts/9500008/'
    for record in manifest['files']:
        path = prefix+record['path']
        data = (source/record['path']).read_bytes()
        assert len(data) == record['size'] and sha(data) == record['sha256']
        assert record['mode'] == '100644'
        assert git('show', pins['head']+':'+path) == data
        assert git('ls-tree', pins['head'], '--', path).decode().strip() == record['mode']+' blob '+record['git_blob']+'\t'+path
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == record['git_blob']
        tree_rows.append({'path': path, 'mode': record['mode'], 'git_blob': record['git_blob'], 'size': len(data), 'sha256': sha(data)})
        if record['path'].endswith('.json'): json.loads(data)
    assert git('diff', '--name-only', pins['base'], pins['head']).decode().splitlines() == manifest['changed_paths']
    diff = git('diff', pins['base'], pins['head'])
    assert diff == (audit/'pr_input/diff.patch').read_bytes() and len(diff) == 49891
    assert sha(diff) == manifest['diff_sha256']

    historical = {}
    for label, revision, disposition in [('base', pins['base'], '| queued | 0/5 |'), ('head', pins['head'], '| unsolved | 2/5 |')]:
        text = git('show', revision+':unsolved_math_prioritization/QUEUE.md')
        rows = [line for line in text.decode().splitlines() if '| 9500008 / AMR-094-0008 |' in line]
        assert len(rows) == 1 and disposition in rows[0]
        state = json.loads(git('show', revision+':unsolved_math_prioritization/state.json'))
        events = [json.loads(line) for line in git('show', revision+':unsolved_math_prioritization/history.jsonl').decode().splitlines()
                  if line and str(json.loads(line).get('id')) == '9500008']
        assert '9500008' not in state and not events
        historical[label] = {'queue_sha256': sha(text), 'target_queue_row': rows[0], 'state': None, 'history_events': events}
    assert git('ls-tree', pins['base'], '--', prefix.rstrip('/')) == b''
    assert git('ls-tree', 'HEAD', '--', prefix.rstrip('/')) == b''
    assert not (native/'attempts/9500008').exists()

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
    assert len({str(problem['id']) for problem in problems}) == len(problems)
    counts = Counter(problem['problem_number'] for problem in problems)
    selected = [problem for problem in problems if problem['id'] == 9500008]
    assert len(selected) == 1
    problem = selected[0]
    assert counts['AMR-094-0008'] == 1 and problem == load(source/'source_record.json') == load(audit/'pinned_problem.json')
    assert 'AMR-094-0008' in reports
    prior = reports['AMR-094-0008']
    assert prior and prior == load(source/'prior_report.json') == load(audit/'pinned_prior_report.json')
    assert prior != {} and prior is not None

    code = (native/'queue.py').read_text()
    importer_definitions = ["counts=collections.Counter(p['problem_number'] for p in problems)",
                            "if counts[p['problem_number']]>1 and p['problem_number'] in reports: p['_ambiguous_report']=True",
                            "json.dumps({} if p.get('_ambiguous_report') else reports.get(p['problem_number'],{}))"]
    assert all(fragment in code for fragment in importer_definitions), 'Importer schema drift requires root review'
    expected = {}
    for item in problems:
        payload = copy.deepcopy(item)
        if counts[payload['problem_number']] > 1 and payload['problem_number'] in reports: payload['_ambiguous_report'] = True
        imported = {} if payload.get('_ambiguous_report') else reports.get(payload['problem_number'], {})
        expected[str(payload['id'])] = (payload, imported)
    database = native/'cache/catalog.sqlite'
    assert not Path(str(database)+'-wal').exists() and not Path(str(database)+'-shm').exists()
    connection = sqlite3.connect(database.as_uri()+'?mode=ro&immutable=1', uri=True)
    connection.execute('PRAGMA query_only=ON')
    assert connection.execute('SELECT revision FROM metadata').fetchall() == [(upstream['revision'],)]
    seen = set()
    for key, payload, report in connection.execute('SELECT key,payload,report FROM records ORDER BY key'):
        assert key not in seen and key in expected
        assert (json.loads(payload), json.loads(report)) == expected[key], key
        seen.add(key)
    assert seen == set(expected) and len(seen) == 15458
    sql_selected = connection.execute('SELECT payload,report FROM records WHERE key=?', ('9500008',)).fetchone()
    assert (json.loads(sql_selected[0]), json.loads(sql_selected[1])) == (problem, prior)
    connection.close()
    spec = importlib.util.spec_from_file_location('root_pinned_pr39_pure_queue', native/'queue.py')
    queue = importlib.util.module_from_spec(spec); spec.loader.exec_module(queue)
    score = queue.score(problem, prior, load(native/'policy.json'))
    assert score['statement_hash'] == sha(problem['statement'].encode())
    assert score['review_hash'] == sha(json.dumps([problem, prior], sort_keys=True).encode())
    assert score == pins['pure_queue_score']

    readiness, turns, verdict = load(source/'readiness.json'), load(source/'turns.json'), load(source/'review/verdict.json')
    budget = readiness['budget']
    assert readiness['id'] == turns['id'] == 9500008
    assert turns['count'] == len(turns['attempts']) == budget['used'] == 2
    assert budget['maximum_substantive_attempts'] == 5 and [x['number'] for x in turns['attempts']] == [1, 2]
    assert [x['outcome'] for x in turns['attempts']] == ['unresolved', 'partial']
    assert readiness['outcome'] == 'unresolved' and verdict['full_problem_solved'] is False
    assert readiness['statement_hash'] == score['statement_hash'] and readiness['review_hash'] == score['review_hash']
    assert turns['attempts'][1]['sha256'] == readiness['reviewed_artifact_sha256'] == verdict['artifact_sha256'] == sha((source/'PARTIAL.md').read_bytes())
    start, deadline = [datetime.datetime.fromisoformat(budget[key].replace('Z', '+00:00')) for key in ['start_utc', 'deadline_utc']]
    literature = datetime.datetime.fromisoformat(readiness['literature_checked_at'])
    assert (deadline-start).total_seconds() == 7200 and start < literature < deadline
    state = load(native/'state.json')
    catalog = [row for row in load(native/'catalog.json') if row['id'] == '9500008']
    history = [json.loads(line) for line in (native/'history.jsonl').read_text().splitlines()
               if line and str(json.loads(line).get('id')) == '9500008']
    queue_rows = [line for line in (native/'QUEUE.md').read_text().splitlines() if '| 9500008 / AMR-094-0008 |' in line]
    assert '9500008' not in state and history == []
    assert len(catalog) == 1 and catalog[0]['local_status'] == 'queued' and catalog[0]['turns_used'] == 0
    assert len(queue_rows) == 1 and '| queued | 0/5 |' in queue_rows[0]
    result = {'status': 'PASS_READONLY_PROVENANCE_REPRODUCTION', 'head': pins['head'], 'base': pins['base'],
              'runtime_python_version': sys.version, 'runtime_actual_executable': sys.executable,
              'original_git_files': tree_rows, 'changed_diff_paths': manifest['changed_paths'], 'full_diff_bytes': len(diff), 'full_diff_sha256': sha(diff),
              'historical_native_target': historical, 'target_attempt_absent_at_base_current_HEAD_and_private_native': True,
              'raw_corpus_bytes': 149266659, 'problem_count': 15458, 'research_report_count': 6701,
              'full_raw_and_SQL_importer_join_checked': True, 'SQL_mode': 'ro, immutable, query_only', 'SQL_revision': upstream['revision'],
              'importer_source_fragments': importer_definitions, 'complete_flat_problem': problem, 'complete_actual_prior_report': prior,
              'prior_raw_key_present': True, 'prior_fallback_used': False, 'raw_and_SQL_full_pair_equal_snapshot_and_root_pins': True,
              'pure_queue_score': score, 'prior_qualification': 'The actual nonempty AMR-094-0008 report is present; null and {} are not this selected prior. Scoped prior credit is not an exhaustive novelty certificate.',
              'authored_substantive_turns': 2, 'turn_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
              'current_native_target': {'state': None, 'history_events': history, 'catalog': catalog[0], 'queue_row': queue_rows[0]},
              'local_ledger_qualification': 'Authored local two-attempt packet is not a canonical queue.py turn-event ledger; native state/history remain absent.',
              'historical_worker_transcript': pins['historical_worker_transcript_status'],
              'scope': 'Source/Git/accounting/importer/full-corpus provenance only. No hidden-turn inference, primary reading attestation, Brownian-law proof, novelty claim or publication verdict.'}
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__': main()
