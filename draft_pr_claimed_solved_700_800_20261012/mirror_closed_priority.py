"""Record only one closed claimed-solved candidate's verified prior-result outcome.

The shared checkout stays on main and untouched. Fresh remote-parent commits
preserve every unrelated JSON member and CSV/queue row byte for byte.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile

from finalize_native_acceptance import REPO, NATIVE, run, encode, replace_root_member, replace_array_record


def append_event(raw, event):
    return raw + ('' if not raw or raw.endswith('\n') else '\n') + json.dumps(event, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audit', type=Path)
    args = parser.parse_args()
    audit = args.audit.resolve()
    audit.relative_to(Path(__file__).resolve().parent)
    disposition_path = audit / 'DISPOSITION.json'
    disposition = json.loads(disposition_path.read_text())
    if disposition['result'] != 'closed_without_merge_prior_full_result' or not disposition['fresh_priority_adversary_confirmed']:
        raise ValueError('Verified final disposition required')
    if run('git', 'branch', '--show-current').strip() != 'main':
        raise ValueError('Shared checkout must remain on main')
    number, problem, head = disposition['pr'], disposition['problem'], disposition['reviewed_head']
    pr = json.loads(run('gh', 'api', f'repos/AlecKriebel/Math/pulls/{number}'))
    if pr['state'] != 'closed' or pr['merged'] or pr['head']['sha'] != head:
        raise ValueError('Exact eligible head must already be closed without merge')
    original_row = json.loads((audit / 'SNAPSHOT.json').read_text())['queue_row'].split('|')
    if original_row[8].strip() != 'claimed_solved':
        raise ValueError('Original eligibility is not exactly claimed_solved')
    used, limit = map(int, original_row[9].strip().split('/'))
    prior = disposition['prior_full_result']
    doi = prior['doi']
    sidecar = f'{NATIVE}/attempts/{problem}/PR{number}_PRIOR_RESULT.json'
    with tempfile.TemporaryDirectory(prefix='closed-pr-priority-index-') as temp:
        env = os.environ.copy(); env['GIT_INDEX_FILE'] = str(Path(temp) / 'index')
        for attempt in range(3):
            parent = run('gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main', '--jq', '.object.sha').strip()
            exists = subprocess.run(['git', 'cat-file', '-e', parent + '^{commit}'], cwd=REPO, capture_output=True)
            if exists.returncode:
                run('git', 'fetch', '--no-write-fetch-head', 'origin', parent)
            names = ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'ranking.csv',
                     'assessments.json', 'assessment_history.jsonl']
            raw = {name: run('git', 'show', f'{parent}:{NATIVE}/{name}') for name in names}
            rows = [line for line in raw['QUEUE.md'].splitlines(keepends=True)
                    if line.startswith('| ') and f' {problem} / ' in line]
            if len(rows) != 1:
                raise ValueError('Unique current target row required')
            old_row = rows[0]; cells = old_row.split('|')
            if len(cells) != 14 or cells[8].strip() not in ['queued', 'claimed_solved']:
                raise ValueError('Current native status changed; reconcile without overwriting')
            if cells[12].strip():
                raise ValueError('Unexpected existing DOI; preserve and reconcile')
            catalog = json.loads(raw['catalog.json'])
            target = [entry for entry in catalog if entry['id'] == problem]
            if len(target) != 1:
                raise ValueError('Unique catalog target required')
            current = target[0]
            if current['statement_hash'] != disposition['statement_hash'] or current['review_hash'] != disposition['review_hash']:
                raise ValueError('Source hashes changed after disposition')
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            sidecar_raw = encode({**disposition, 'native_mirror_at': now})
            evidence = {'disposition': {'path': disposition_path.relative_to(REPO).as_posix(),
                        'sha256': hashlib.sha256(disposition_path.read_bytes()).hexdigest()},
                        'native_resolution': {'path': sidecar, 'sha256': hashlib.sha256(sidecar_raw.encode()).hexdigest()},
                        'reviewed_head': head, 'prior_result_doi': doi,
                        'original_explicit_budget': original_row[9].strip(),
                        'historical_lifecycle_reconstructed': False, 'earliest_global_priority_certified': False}
            note = (f'PR#{number} closed without merge: the internally verified candidate is a rediscovery '
                    f'of {prior["author"]}, {prior["publication_date"]}, DOI {doi}. '
                    'Same full infinite conclusion and permutation-equivalent counterexample; no proof failure or plagiarism claim.')
            event = {'at': now, 'id': problem, 'status': 'already_solved',
                     'event': 'priority_audit_rediscovery', 'note': note, 'pr': number,
                     'prior_result_doi': doi, 'statement_hash': current['statement_hash'],
                     'review_hash': current['review_hash'], 'turns_used': used, 'turn_limit': limit,
                     'evidence': evidence}
            event['event_id'] = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()
            state = json.loads(raw['state.json'])
            state_target = {**state.get(problem, {}), **event}
            assessments = json.loads(raw['assessments.json'])
            assessment = {**assessments.get(problem, {}), 'reviewed_at': now,
                          'statement_hash': current['statement_hash'], 'review_hash': current['review_hash'],
                          'resolution': 'already_solved', 'decision': 'exclude', 'p_valid_open': 0,
                          'note': note, 'rationale': note,
                          'remaining_gap': 'No mathematical gap found; a full earlier published proof is independently verified. Earliest global priority and external editorial acceptance are not certified.',
                          'first_experiment': 'Completed exact prior-proof and permutation-action comparison; preserve this outcome and skip future research under the claimed-solved-only policy.'}
            assessment['sources'] = list(dict.fromkeys(assessment.get('sources', []) + ['https://doi.org/' + doi]))
            cells[8] = ' already_solved '; cells[9] = f' {used}/{limit} '
            cells[11] = cells[11].rstrip() + f' {now} — {note} '
            changed_queue = raw['QUEUE.md'].replace(old_row, '|'.join(cells), 1)
            current.update(local_status='already_solved', eligible=False, rank=None, turns_used=used,
                           p_valid_open=0, ev=0, ev_low=0, ev_high=0, desk_decision='exclude', desk_note=note)
            current['holds'] = list(dict.fromkeys(current.get('holds', []) + ['known_resolution']))
            csv_lines = raw['ranking.csv'].splitlines(keepends=True)
            header = next(csv.reader([csv_lines[0]])); found = 0
            for i, line in enumerate(csv_lines[1:], 1):
                row = next(csv.reader([line]))
                if row[header.index('id')] != problem:
                    continue
                found += 1
                for key, value in [('rank', ''), ('local_status', 'already_solved'), ('eligible', 'False'),
                                   ('turns_used', str(used)), ('p_valid_open', '0'), ('ev', '0'), ('ev_low', '0'),
                                   ('ev_high', '0'), ('desk_decision', 'exclude'), ('desk_note', note),
                                   ('holds', '; '.join(current['holds']))]:
                    if key in header:
                        row[header.index(key)] = value
                stream = io.StringIO(newline=''); csv.writer(stream).writerow(row); csv_lines[i] = stream.getvalue()
            if found != 1:
                raise ValueError('Unique ranking target required')
            updates = {f'{NATIVE}/QUEUE.md': changed_queue,
                       f'{NATIVE}/state.json': replace_root_member(raw['state.json'], problem, state_target),
                       f'{NATIVE}/history.jsonl': append_event(raw['history.jsonl'], event),
                       f'{NATIVE}/catalog.json': replace_array_record(raw['catalog.json'], problem, current),
                       f'{NATIVE}/ranking.csv': ''.join(csv_lines),
                       f'{NATIVE}/assessments.json': replace_root_member(raw['assessments.json'], problem, assessment),
                       f'{NATIVE}/assessment_history.jsonl': append_event(raw['assessment_history.jsonl'], {'id': problem, **assessment}),
                       sidecar: sidecar_raw}
            exists = subprocess.run(['git', 'cat-file', '-e', parent + ':' + sidecar], cwd=REPO, capture_output=True)
            if exists.returncode == 0:
                raise ValueError('Existing resolution sidecar must not be overwritten')
            run('git', 'read-tree', parent, env=env)
            for path, content in updates.items():
                blob = run('git', 'hash-object', '-w', '--stdin', raw=content).strip()
                run('git', 'update-index', '--add', '--cacheinfo', '100644', blob, path, env=env)
            changed = run('git', 'diff', '--cached', '--name-only', parent, env=env).splitlines()
            if set(changed) != set(updates):
                raise ValueError('Unexpected paths changed')
            tree = run('git', 'write-tree', env=env).strip()
            commit = run('git', 'commit-tree', tree, '-p', parent,
                         raw=f'PR{number}: record independently confirmed prior full solution\n').strip()
            pushed = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'], cwd=REPO,
                                    capture_output=True, text=True)
            if pushed.returncode:
                ref_race = re.search(
                    r"cannot lock ref 'refs/heads/main': is at [0-9a-f]{40} but expected [0-9a-f]{40}",
                    pushed.stderr)
                if 'fetch first' in pushed.stderr or 'non-fast-forward' in pushed.stderr or ref_race:
                    continue
                raise RuntimeError(pushed.stderr)
            for path, expected in updates.items():
                if run('git', 'show', commit + ':' + path) != expected:
                    raise ValueError('Committed resolution differs from intended bytes')
            receipt = {'completed_utc': now, 'result': 'PASS', 'commit': commit, 'parent': parent,
                       'pr': number, 'problem': problem, 'prior_result_doi': doi, 'status': 'already_solved',
                       'paths': list(updates), 'unrelated_entries_and_shared_checkout_preserved': True,
                       'file_hashes': {path: hashlib.sha256(content.encode()).hexdigest() for path, content in updates.items()}}
            (audit / 'NATIVE_PRIORITY_MIRROR_RECEIPT.json').write_text(encode(receipt))
            print(json.dumps({k: v for k, v in receipt.items() if k not in ['paths', 'file_hashes']}))
            return
        raise RuntimeError('Remote main advanced on all three attempts')


if __name__ == '__main__':
    main()
