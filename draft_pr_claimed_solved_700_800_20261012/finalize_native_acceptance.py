"""Publish a scoped present-day acceptance mirror after verified publication and merge.

A scoped Git tree and fresh remote parent preserve the shared dirty checkout.
Only the named problem's entries and two new acceptance sidecars are changed.
Historical proof-attempt lifecycle events are never reconstructed.
"""
import argparse
import csv
import datetime
import hashlib
import io
import json
import re
from pathlib import Path
import subprocess
from scoped_tree import replace_paths

REPO = Path(__file__).resolve().parent.parent
NATIVE = 'unsolved_math_prioritization'


def run(*args, env=None, raw=None):
    result = subprocess.run(args, cwd=REPO, env=env,
                            input=None if raw is None else raw.encode('utf-8'),
                            capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8'))
    return result.stdout.decode('utf-8')


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def bind(path):
    return {'path': path.relative_to(REPO).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def skip_space(raw, pos):
    while pos < len(raw) and raw[pos] in ' \t\r\n':
        pos += 1
    return pos


def render_value(value, indent):
    lines = json.dumps(value, ensure_ascii=False, indent=2).splitlines()
    return lines[0] + ''.join('\n' + ' ' * indent + line for line in lines[1:])


def replace_root_member(raw, key, value):
    """Replace/append one root member, preserving every other member's exact bytes."""
    decoder = json.JSONDecoder()
    pos = skip_space(raw, 0)
    if raw[pos] != '{':
        raise ValueError('Expected a JSON object')
    opening = pos
    pos = skip_space(raw, pos + 1)
    found = []
    last_end = None
    keys = []
    while raw[pos] != '}':
        member_start = pos
        name, end = decoder.raw_decode(raw, pos)
        if not isinstance(name, str) or name in keys:
            raise ValueError('Invalid or repeated JSON member')
        keys.append(name)
        pos = skip_space(raw, end)
        if raw[pos] != ':':
            raise ValueError('Missing JSON colon')
        start = skip_space(raw, pos + 1)
        _, end = decoder.raw_decode(raw, start)
        if name == key:
            prefix = raw[raw.rfind('\n', 0, member_start) + 1:member_start]
            indent = len(prefix) if not prefix.strip() else 2
            found.append((start, end, indent))
        last_end = end
        pos = skip_space(raw, end)
        if raw[pos] == ',':
            pos = skip_space(raw, pos + 1)
        elif raw[pos] != '}':
            raise ValueError('Invalid JSON member delimiter')
    if found:
        start, end, indent = found[0]
        result = raw[:start] + render_value(value, indent) + raw[end:]
    else:
        insertion = '\n  ' + json.dumps(key) + ': ' + render_value(value, 2)
        if last_end is None:
            result = raw[:opening + 1] + insertion + raw[opening + 1:]
        else:
            result = raw[:last_end] + ',' + insertion + raw[last_end:]
    before, after = json.loads(raw), json.loads(result)
    if {k: v for k, v in before.items() if k != key} != {k: v for k, v in after.items() if k != key} or after[key] != value:
        raise ValueError('Unrelated JSON members changed')
    return result


def replace_array_record(raw, identifier, value):
    """Replace one array record while preserving every other record's exact bytes."""
    decoder = json.JSONDecoder()
    pos = skip_space(raw, 0)
    if raw[pos] != '[':
        raise ValueError('Expected a JSON array')
    pos = skip_space(raw, pos + 1)
    matches = []
    while raw[pos] != ']':
        start = pos
        item, end = decoder.raw_decode(raw, pos)
        if item['id'] == identifier:
            prefix = raw[raw.rfind('\n', 0, start) + 1:start]
            indent = len(prefix) if not prefix.strip() else 2
            matches.append((start, end, indent))
        pos = skip_space(raw, end)
        if raw[pos] == ',':
            pos = skip_space(raw, pos + 1)
        elif raw[pos] != ']':
            raise ValueError('Invalid JSON array delimiter')
    if len(matches) != 1:
        raise ValueError('Array record is not unique')
    start, end, indent = matches[0]
    result = raw[:start] + render_value(value, indent) + raw[end:]
    before, after = json.loads(raw), json.loads(result)
    if [v for v in before if v['id'] != identifier] != [v for v in after if v['id'] != identifier]:
        raise ValueError('Unrelated array records changed')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('audit', type=Path)
    parser.add_argument('problem')
    parser.add_argument('pr', type=int)
    parser.add_argument('head')
    args = parser.parse_args()
    if run('git', 'branch', '--show-current').strip() != 'main':
        raise ValueError('The shared checkout must remain on main')
    audit = args.audit.resolve()
    gate_path = audit / 'FINAL_READINESS.json'
    gate = json.loads(gate_path.read_text())
    publication_path = audit / 'publication/PUBLISH_RECEIPT.json'
    publication = json.loads(publication_path.read_text())
    tracker_path = audit / 'publication/SHEET_VERIFICATION.json'
    tracker = json.loads(tracker_path.read_text())
    if (gate['result'] != 'PASS' or publication['state'] != 'published'
            or tracker['result'] != 'PASS' or publication['doi'] != tracker['doi']):
        raise ValueError('Acceptance requires verified readiness, publication and tracker')
    inventory = json.loads((audit / 'preprint/PACKAGE_INVENTORY.json').read_text())
    if gate['publication_files'] != inventory['files']:
        raise ValueError('Publication inputs changed after the readiness gate')
    for item in inventory['files']:
        path = audit / 'preprint' / item['path']
        if path.stat().st_size != item['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError('Current package does not match the accepted inputs')
    pr = json.loads(run('gh', 'api', f'repos/AlecKriebel/Math/pulls/{args.pr}'))
    if not pr['merged'] or pr['head']['sha'] != args.head:
        raise ValueError('Exact reviewed PR head must be merged before acceptance mirroring')
    doi = publication['doi']
    native_acceptance = f'{NATIVE}/attempts/{args.problem}/acceptance.json'
    native_note = f'{NATIVE}/attempts/{args.problem}/PREPRINT_PUBLICATION.md'
    for attempt in range(3):
        parent = run('gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main',
                     '--jq', '.object.sha').strip()
        present = subprocess.run(['git', 'cat-file', '-e', parent + '^{commit}'],
                                 cwd=REPO, capture_output=True)
        if present.returncode:
            run('git', 'fetch', '--no-write-fetch-head', 'origin', parent)
        for sidecar in (native_acceptance, native_note):
            existing = subprocess.run(['git', 'cat-file', '-e', parent + ':' + sidecar],
                                      cwd=REPO, capture_output=True)
            if existing.returncode == 0:
                raise ValueError('An acceptance sidecar already exists; reconcile before writing')
        names = ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'ranking.csv']
        before = {name: run('git', 'show', f'{parent}:{NATIVE}/{name}') for name in names}
        queue = before['QUEUE.md']
        target_rows = [line for line in queue.splitlines(keepends=True)
                       if line.startswith('| ') and f' {args.problem} / ' in line]
        if len(target_rows) != 1:
            raise ValueError('Target queue row is not unique')
        old_line = target_rows[0]
        cells = old_line.split('|')
        if len(cells) != 14:
            raise ValueError('Unexpected queue schema')
        if cells[8].strip() == 'preprint_published' and cells[12].strip() in (doi, 'https://doi.org/' + doi):
            raise ValueError('Acceptance already recorded: inspect before repeating')
        if cells[8].strip() != 'claimed_solved' or cells[12].strip():
            raise ValueError('Only an unpublished claimed_solved target may be promoted')
        used, limit = map(int, cells[9].strip().split('/'))
        if not 1 <= used <= limit == 5:
            raise ValueError('Original explicit proof-attempt budget is invalid')
        state = json.loads(before['state.json'])
        catalog = json.loads(before['catalog.json'])
        target = [item for item in catalog if item['id'] == args.problem]
        if len(target) != 1:
            raise ValueError('Target catalog row is not unique')
        current = target[0]
        if current['statement_hash'] != gate['statement_hash'] or current['review_hash'] != gate['review_hash']:
            raise ValueError('The source hashes changed after final readiness')
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        acceptance = {'accepted_utc': now, 'problem': args.problem, 'pr': args.pr,
                      'reviewed_head': args.head, 'merge_commit': pr['merge_commit_sha'],
                      'result': 'accepted_full_resolution_unrefereed_preprint',
                      'doi': doi, 'record_url': publication['record_url'],
                      'statement_hash': current['statement_hash'], 'review_hash': current['review_hash'],
                      'final_readiness': bind(gate_path), 'publication': bind(publication_path),
                      'tracker': bind(tracker_path), 'publication_files': inventory['files'],
                      'historical_priority_certified': False, 'external_human_peer_review': False,
                      'formal_proof_verification': False, 'extensive_AI_use': True,
                      'historical_candidate_preserved': True, 'turns_used': used, 'turn_limit': limit}
        acceptance_raw = encode(acceptance)
        event = {'at': now, 'id': args.problem, 'status': 'preprint_published',
                 'event': 'acceptance_mirror_import', 'pr': args.pr, 'doi': doi,
                 'statement_hash': current['statement_hash'], 'review_hash': current['review_hash'],
                 'turns_used': used, 'turn_limit': limit,
                 'note': 'Present-day acceptance of the complete internally audited preprint; original candidate history preserved.',
                 'evidence': {'canonical_acceptance': {'path': native_acceptance,
                     'sha256': hashlib.sha256(acceptance_raw.encode()).hexdigest()},
                     'reviewed_head': args.head, 'merge_commit': pr['merge_commit_sha'],
                     'final_gate': bind(gate_path), 'publication': bind(publication_path),
                     'tracker': bind(tracker_path), 'queue_explicit_budget': cells[9].strip(),
                     'historical_transitions_asserted': False, 'historical_priority_certified': False}}
        event['event_id'] = hashlib.sha256(json.dumps(event, sort_keys=True).encode()).hexdigest()
        state[args.problem] = {**state.get(args.problem, {}), **event}
        current.update(local_status='preprint_published', turns_used=used, eligible=False, rank=None)
        cells[8] = ' preprint_published '
        cells[11] = cells[11].rstrip() + (
            f' {now} — ACCEPTED/PUBLISHED after fresh mathematical families, bounded priority '
            f'audit and successive whole-preprint adversarial reviews; research note and '
            f'source/verification package, DOI {doi}; PR#{args.pr} merged at '
            f'{pr["merge_commit_sha"]}; extensive AI use, unrefereed, no external human '
            'peer review or formal proof verification; first historical priority not certified. ')
        cells[12] = f' {doi} '
        changed_queue = queue.replace(old_line, '|'.join(cells), 1)
        csv_lines = before['ranking.csv'].splitlines(keepends=True)
        header = next(csv.reader([csv_lines[0]]))
        found = 0
        for i, line in enumerate(csv_lines[1:], 1):
            row = next(csv.reader([line]))
            if row[header.index('id')] != args.problem:
                continue
            found += 1
            for key, value in [('rank', ''), ('local_status', 'preprint_published'),
                               ('turns_used', str(used)), ('eligible', 'False')]:
                row[header.index(key)] = value
            out = io.StringIO(newline=''); csv.writer(out).writerow(row); csv_lines[i] = out.getvalue()
        if found != 1:
            raise ValueError('Target ranking row is not unique')
        audit_relative = audit.relative_to(REPO).as_posix()
        note = (f'# Accepted preprint for problem {args.problem}\n\n'
                f'[{publication["title"]}](https://doi.org/{doi}) by Alec Kriebel, '
                'ORCID 0009-0001-9320-500X, version 1.0. The accepted theorem is the '
                'full source target, with the hypotheses stated in the paper.\n\n'
                f'[Current audit and publication records](https://github.com/AlecKriebel/Math/tree/main/{audit_relative}) '
                f'bind the exact manuscript, PDF, support archive, fresh reviews, '
                f'publication receipt and tracker readback. PR#{args.pr} head `{args.head}` '
                f'was merged as `{pr["merge_commit_sha"]}`.\n\n'
                'AI tools were used extensively. This preprint is unrefereed; internal '
                'AI-assisted review is not external human peer review or formal proof '
                'verification. A bounded priority audit found no earlier full resolution; '
                'first historical priority is not certified. The original candidate files '
                'and historical adverse findings are retained unchanged. See acceptance.json '
                'for the present-day acceptance bindings.\n')
        updates = {f'{NATIVE}/QUEUE.md': changed_queue,
                   f'{NATIVE}/state.json': replace_root_member(before['state.json'], args.problem, state[args.problem]),
                   f'{NATIVE}/history.jsonl': before['history.jsonl'] +
                       ('' if not before['history.jsonl'] or before['history.jsonl'].endswith('\n') else '\n') +
                       json.dumps(event, ensure_ascii=False) + '\n',
                   f'{NATIVE}/catalog.json': replace_array_record(before['catalog.json'], args.problem, current),
                   f'{NATIVE}/ranking.csv': ''.join(csv_lines),
                   native_acceptance: acceptance_raw, native_note: note}
        # Frozen attempt files and unrelated entries retain their Git objects.
        object_updates = {}
        for path, raw in updates.items():
            blob = run('git', 'hash-object', '-w', '--stdin', raw=raw).strip()
            object_updates[path] = ('100644', blob)
        tree = replace_paths(REPO, parent, object_updates)
        changed = run('git', 'diff', '--name-only', parent, tree).splitlines()
        if set(changed) != set(updates):
            raise ValueError('Unexpected native acceptance changes')
        commit = run('git', 'commit-tree', tree, '-p', parent,
                     raw=f'Accept PR{args.pr} published preprint and synchronize its own queue mirrors\n').strip()
        push = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'],
                              cwd=REPO, capture_output=True, text=True)
        if push.returncode:
            ref_race = re.search(
                r"cannot lock ref 'refs/heads/main': is at [0-9a-f]{40} but expected [0-9a-f]{40}",
                push.stderr)
            if 'fetch first' in push.stderr or 'non-fast-forward' in push.stderr or ref_race:
                continue
            raise RuntimeError(push.stderr)
        receipts = {'completed_utc': now, 'result': 'PASS', 'commit': commit, 'parent': parent,
                    'doi': doi, 'pr': args.pr, 'reviewed_head': args.head,
                    'merge_commit': pr['merge_commit_sha'], 'paths': list(updates),
                    'shared_checkout_and_index_untouched': True,
                    'unrelated_entries_preserved': True,
                    'file_hashes': {path: hashlib.sha256(raw.encode()).hexdigest() for path, raw in updates.items()}}
        for path, expected in updates.items():
            if run('git', 'show', commit + ':' + path) != expected:
                raise ValueError('Committed native acceptance readback differs')
        (audit / 'publication/NATIVE_ACCEPTANCE_RECEIPT.json').write_text(encode(receipts))
        print(json.dumps({key: value for key, value in receipts.items() if key not in ['paths', 'file_hashes']}))
        return
    raise RuntimeError('Remote main advanced during all three attempts')


if __name__ == '__main__':
    main()
