#!/usr/bin/env python3
"""Evidence-bound acceptance mirror proposal; never writes live queue metadata.

Default command emits a dry-run JSON plan. Sandbox replay is restricted to this
helper's ignored tmp directory. No Git, network, ranking or publication calls.
"""
import argparse
import copy
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
TERMINAL = {'unsolved', 'already_solved', 'preprint_published'}


class Rejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def load(path):
    return json.loads(Path(path).read_text())


def bound(repo, binding):
    path = (repo / binding['path']).resolve()
    require(path.is_relative_to(repo.resolve()), 'Evidence escapes repository')
    require(path.is_file(), 'Missing evidence: ' + binding['path'])
    data = path.read_bytes()
    require(sha(data) == binding['sha256'], 'Stale/mismatched evidence: ' + binding['path'])
    return data


def table_rows(text):
    """Strict selected-row parsing. Malformed unrelated rows do not confer a budget."""
    header = next((x for x in text.splitlines() if x.startswith('| Rank | ID / code |')), None)
    require(header is not None, 'Unknown current queue table layout')
    columns = [x.strip() for x in header.strip('|').split('|')]
    require(all(x in columns for x in ['ID / code', 'Status', 'Turns', 'DOI']), 'Required queue columns absent')
    rows = {}
    doi_owners = {}
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) < 2:
            continue
        identity = cells[1].split('/')[0].strip()
        for doi in set(re.findall(r'10\.5281/zenodo\.[0-9]+', line)):
            doi_owners.setdefault(doi, set()).add(identity)
        if not re.fullmatch(r'[0-9]+', identity):
            continue
        # Never silently choose one duplicate selected row or displaced budget.
        rows.setdefault(identity, []).append(dict(zip(columns, cells)) if len(cells) == len(columns) else None)
    return rows, doi_owners


def ledger_budget(data, kind, used, limit):
    if kind == 'jsonl_turns':
        records = [json.loads(x) for x in data.decode().splitlines() if x.strip()]
        numbers = [x['turn'] for x in records]
        require(numbers == list(range(1, used + 1)), 'Ambiguous/gapped/duplicate attempt ledger')
    else:
        obj = json.loads(data)
        if kind == 'json_turn_list':
            require([x['turn'] for x in obj] == list(range(1, used + 1)), 'Ambiguous attempt list')
        elif kind == 'json_turns':
            require(obj['used'] == used and obj['limit'] == limit, 'Original budget mismatch')
            require([x['turn'] for x in obj['turns']] == list(range(1, used + 1)), 'Ambiguous attempt list')
        elif kind == 'json_attempt':
            require(obj['substantive_attempts_used'] == used and obj['substantive_attempt_limit'] == limit, 'Original budget mismatch')
        elif kind == 'json_target_ledger':
            require(obj['substantive_attempts_used'] == used and obj['maximum_substantive_attempts'] == limit, 'Original budget mismatch')
            require([x['number'] for x in obj['attempts']] == list(range(1, used + 1)), 'Ambiguous attempt list')
        else:
            raise Rejected('Unsupported ledger schema; no budget inference')


def source_hashes(repo, identity):
    """Read-only check against actual pinned source, not only stale catalog fields."""
    db_path = repo / 'unsolved_math_prioritization/cache/catalog.sqlite'
    with closing(sqlite3.connect(db_path.as_uri() + '?mode=ro', uri=True)) as db:
        raw = db.execute('SELECT payload,report FROM records WHERE key=?', (identity,)).fetchone()
        require(raw is not None, 'Unknown pinned source ID')
        problem, report = map(json.loads, raw)
        require(str(problem['id']) == identity, 'Pinned source identity mismatch')
    return {'review_hash': sha(json.dumps([problem, report], sort_keys=True).encode()),
            'statement_hash': sha((problem.get('statement') or '').encode()),
            'source_record_hash': sha(json.dumps(problem, sort_keys=True).encode()),
            'source_report_hash': sha(json.dumps(report, sort_keys=True).encode())}


def accepted_statement(data, identity, current, annotations=()):
    """Find an explicit numeric-ID statement; never borrow a neighbor's formulation."""
    matches = []
    container = json.loads(data)
    require(set(annotations) <= {'statement_audit'}, 'Cannot strip source fields as annotations')
    if isinstance(container, dict) and container.get('catalog_at_start'):
        require(container['catalog_at_start'].get('review_hash') == current['review_hash'], 'Accepted source review context changed')
    def walk(obj):
        if isinstance(obj, dict):
            if str(obj.get('id', obj.get('numeric_id', ''))) == identity and isinstance(obj.get('statement'), str):
                original = {k: v for k, v in obj.items() if k not in annotations}
                require(sha(json.dumps(original, sort_keys=True).encode()) == current['source_record_hash'], 'Accepted/current full source record mismatch')
                matches.append(obj['statement'])
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    walk(container)
    if isinstance(container, dict) and str(container.get('problem_id')) == identity and isinstance(container.get('source_statement'), str):
        require(container.get('catalog_at_start', {}).get('review_hash') == current['review_hash'], 'Accepted source review context changed')
        matches.append(container['source_statement'])
    if isinstance(container, dict) and str(container.get('id')) == identity and container.get('upstream_statement_sha256'):
        require(container.get('upstream_statement_sha256') == current['statement_hash'] and container.get('review_hash') == current['review_hash'], 'Accepted source hash context changed')
        return current['statement_hash']
    if isinstance(container, dict) and 'prior_report' in container:
        # Recorded null and pinned {} both expressly mean no prior report.
        report = {} if container['prior_report'] is None else container['prior_report']
        require(sha(json.dumps(report, sort_keys=True).encode()) == current['source_report_hash'], 'Accepted prior-report context changed')
    require(len(matches) == 1, 'Accepted source statement absent/ambiguous; no hash rebinding')
    return sha(matches[0].encode())


def build_plan(repo, spec, timestamp=None, source_reader=source_hashes):
    repo = Path(repo).resolve()
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    require(spec.get('authorization') == 'human_authorized_current_acceptance_mirror', 'Explicit current-mirror authorization missing')
    root = repo / 'unsolved_math_prioritization'
    inventory = json.loads(bound(repo, spec['inventory']))
    queue_data = bound(repo, spec['queue'])
    rows, doi_owners = table_rows(queue_data.decode())
    catalog = {str(x['id']): x for x in json.loads(bound(repo, spec['catalog']))}
    policy = json.loads(bound(repo, spec['policy']))
    state_bytes = (root / 'state.json').read_bytes()
    history_bytes = (root / 'history.jsonl').read_bytes()
    require(not history_bytes or history_bytes.endswith(b'\n'), 'History tail incomplete; unknown append outcome')
    state = json.loads(state_bytes)
    require(isinstance(state, dict), 'State must be an object')
    history = [json.loads(x) for x in history_bytes.decode().splitlines() if x.strip()]
    events = {x['event_id']: x for x in history if x.get('event') == 'acceptance_mirror_import'}
    require(len(events) == sum(x.get('event') == 'acceptance_mirror_import' for x in history), 'Duplicate mirror history event')
    item_by_pr = {x['number']: x for x in inventory['items']}
    require(len(item_by_pr) == len(inventory['items']), 'Duplicate PR inventory entry')
    entries = spec['entries']
    require(len({x['id'] for x in entries}) == len(entries), 'Duplicate selected ID')
    require(len({x['pr'] for x in entries}) == len(entries), 'Duplicate selected PR')
    after = copy.deepcopy(state)
    appends, decisions = [], []
    bindings = [spec[k] for k in ['inventory', 'queue', 'catalog', 'policy']]
    for entry in entries:
        identity, pr = str(entry['id']), entry['pr']
        item = item_by_pr.get(pr, {})
        require(item.get('stage') == 'complete', f'PR{pr}: unpublished/pending inventory stage')
        require(pr not in inventory.get('excluded_prs', []), 'Excluded PR')
        require(item.get('headRefName') == 'dot/math-' + identity, 'Selected source ID/branch mismatch')
        raw_accept = bound(repo, entry['acceptance'])
        acceptance = json.loads(raw_accept)
        if 'problem_id' in acceptance:
            require(str(acceptance['problem_id']) == identity, 'Acceptance ID mismatch')
        if 'pr' in acceptance:
            require(acceptance['pr'] == pr, 'Acceptance PR mismatch')
        require(entry['acceptance']['path'].startswith('unsolved_math_prioritization/attempts/' + identity + '/') or entry.get('canonical_acceptance_text'), 'Canonical acceptance pointer required')
        status = entry['status']
        require(status in TERMINAL, 'Unsupported/unaccepted status')
        # PR9 predates queue_status in the canonical receipt: exact published outcome only.
        accepted_status = acceptance.get('queue_status')
        if accepted_status is None:
            require(acceptance.get('outcome') == 'claimed_solved_accepted_and_published' and status == 'preprint_published', 'Acceptance status missing')
        else:
            require(accepted_status == status, 'Acceptance status mismatch')
        expected_head = item.get('audited_head') or item['headRefOid']
        heads = [acceptance[x] for x in ['source_head', 'original_head', 'audited_head', 'reviewed_head'] if x in acceptance]
        require(heads and all(x == expected_head for x in heads), 'Stale acceptance head')
        merge = acceptance.get('merge_commit')
        require(re.fullmatch(r'[a-f0-9]{40}', merge or '') is not None and merge == item.get('merge_commit'), 'Acceptance/inventory merge mismatch')
        remote_wrapper = json.loads(bound(repo, entry['remote']))
        remote = remote_wrapper.get('pull_request', remote_wrapper)
        require(remote.get('state') == 'MERGED' and remote.get('mergedAt'), 'Remote acceptance not verified MERGED')
        require(remote.get('isDraft') is not True, 'Draft remote PR')
        require(remote.get('headRefOid') == expected_head and remote.get('mergeCommit', {}).get('oid') == merge, 'Remote exact-head/merge mismatch')
        if 'number' in remote:
            require(remote['number'] == pr, 'Remote PR number mismatch')
        if 'url' in remote:
            require(remote['url'] == f'https://github.com/AlecKriebel/Math/pull/{pr}', 'Remote PR URL mismatch')
        require(remote['mergedAt'] == acceptance.get('merged_at'), 'Remote/canonical merge date mismatch')
        if item.get('merged_at'):
            require(item['merged_at'] == remote['mergedAt'], 'Remote/inventory merge date mismatch')
        matches = rows.get(identity, [])
        require(len(matches) == 1 and matches[0] is not None, 'Ambiguous/malformed selected queue row')
        row = matches[0]
        require(row['Status'] == status, 'Queue/acceptance status mismatch')
        budget = entry['budget']
        used, limit = budget['used'], budget['limit']
        require(type(used) is int and type(limit) is int and 0 <= used <= limit and limit > 0, 'Invalid budget')
        require(row['Turns'] == f'{used}/{limit}' and policy.get('turn_limit') == limit, 'Explicit queue/policy budget mismatch')
        ledger_budget(bound(repo, budget['ledger']), budget['kind'], used, limit)
        for key in ['original_attempts_used', 'attempts_used']:
            if key in acceptance:
                require(acceptance[key] == used, 'Canonical original budget mismatch')
        if 'turn_limit' in acceptance:
            require(acceptance['turn_limit'] == limit, 'Canonical original limit mismatch')
        current = source_reader(repo, identity)
        require(identity in catalog and catalog[identity].get('present') is True, 'Selected source absent from catalog')
        require(all(catalog[identity].get(k) == current[k] for k in ['statement_hash', 'review_hash']), 'Current source/catalog hash mismatch')
        statement_hash = accepted_statement(bound(repo, entry['accepted_source']), identity, current, entry['accepted_source'].get('source_annotations', []))
        require(statement_hash == current['statement_hash'], 'Accepted/current exact statement mismatch')
        artifact = entry.get('artifact')
        if artifact:
            bound(repo, artifact)
            require(acceptance.get(artifact['acceptance_hash_field']) == artifact['sha256'], 'Canonical accepted artifact hash mismatch')
        if entry.get('canonical_acceptance_text'):
            text = bound(repo, entry['canonical_acceptance_text']).decode()
            require(identity in text and status.upper() in text.upper(), 'Canonical acceptance text scope mismatch')
        duplicates = entry.get('duplicates', [])
        require(identity not in duplicates and len(set(duplicates)) == len(duplicates), 'Invalid selected duplicate group')
        for duplicate in duplicates:
            require(duplicate in catalog and catalog[duplicate].get('eligible') is False, 'Selected duplicate still research-eligible; separate audit needed')
        if duplicates:
            dtext = bound(repo, entry['duplicate_evidence']).decode()
            require(all(x in dtext for x in duplicates), 'Duplicate evidence mismatch')
        doi = acceptance.get('doi')
        if status == 'preprint_published':
            require(doi and doi == item.get('doi'), 'Published DOI missing/mismatched')
            require(doi_owners.get(doi) == {identity}, 'Duplicate/wrong-row DOI')
            require(doi in row['DOI'], 'Queue DOI missing')
            publication = json.loads(bound(repo, entry['publication']))
            observed = publication.get('doi') or publication.get('doi_url', '').removeprefix('https://doi.org/')
            require(observed == doi, 'Publication DOI mismatch')
            require(publication.get('published_state_verified_by_repository_tool') is True or publication.get('state') == 'public_record_and_downloads_verified', 'Publication not verified public')
        else:
            require(not doi and not item.get('doi') and not row['DOI'], 'Unpublished result has new DOI')
        prior = state.get(identity, {})
        require(prior.get('turns_used', 0) <= used, 'Would decrease existing budget usage')
        evidence = {'canonical_acceptance': entry['acceptance'], 'remote_acceptance': entry['remote'],
                    'accepted_source': entry['accepted_source'],
                    'original_budget_ledger': budget['ledger'], 'queue_explicit_budget': row['Turns'],
                    'merge_commit': merge, 'reviewed_head': expected_head, 'duplicate_ids': duplicates,
                    'authorization': spec['authorization'], 'import_is_present_day_mirror': True,
                    'historical_transitions_asserted': False}
        for key in ['artifact', 'publication', 'canonical_acceptance_text', 'duplicate_evidence']:
            if key in entry:
                evidence[key] = entry[key]
        core = {'id': identity, 'pr': pr, 'status': status, 'turns_used': used, 'turn_limit': limit,
                **current, 'doi': doi, 'evidence': evidence}
        event_id = sha(encode(core))
        event = {**prior, **core, 'event': 'acceptance_mirror_import', 'event_id': event_id,
                 'at': timestamp, 'note': 'Human-authorized current acceptance mirror; no historical readiness/candidate/verification transitions reconstructed.'}
        existing = events.get(event_id)
        if existing:
            require(all(existing.get(k) == v for k, v in core.items()), 'Existing mirror event conflict')
            event = existing
        else:
            require(prior.get('event') != 'acceptance_mirror_import', 'Existing acceptance mirror differs; explicit revision review required')
            appends.append(event)
        after[identity] = event
        decisions.append({'id': identity, 'pr': pr, 'status': status, 'turns_used': used,
                          'turn_limit': limit, 'doi': doi, 'event_id': event_id,
                          'state_changed': prior != event, 'history_append': existing is None})
        bindings += [entry[k] for k in ['acceptance', 'remote', 'accepted_source']]
        bindings += [budget['ledger']]
        bindings += [entry[k] for k in ['artifact', 'publication', 'canonical_acceptance_text', 'duplicate_evidence'] if k in entry]
    new_history = history_bytes + b''.join((json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n').encode() for x in appends)
    # Preserve original state bytes for a genuine no-op replay.
    after_bytes = state_bytes if after == state else encode(after)
    return {'schema': 'acceptance-mirror-plan/v1', 'created_at_utc': timestamp, 'dry_run': True,
            'writes_authorized_to_live_repo': False, 'bindings': bindings,
            'preconditions': {'state_sha256': sha(state_bytes), 'history_sha256': sha(history_bytes),
                              'queue_sha256': sha(queue_data)},
            'decisions': decisions, 'state_after': after, 'history_append': appends,
            'state_after_sha256': sha(after_bytes), 'history_after_sha256': sha(new_history),
            'state_after_bytes': after_bytes.decode(), 'history_append_bytes': new_history[len(history_bytes):].decode(),
            'protected': ['QUEUE.md', 'catalog.json', 'assessments.json', 'historical desk reviews', 'duplicate records', 'publication and tracker state'],
            'limitations': ['Does not prevent legacy rank from replacing manual QUEUE columns.',
                            'Does not prevent a deliberate legacy ready/in_progress command from reopening an accepted target.',
                            'Offline validates pinned existing remote receipts; does not authenticate GitHub or replace a fresh root remote check.']}


def atomic(path, data):
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('wb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)


def validate_plan(repo, plan):
    """Fresh read-only preflight for a reviewed proposal, before root-owned mutation."""
    repo = Path(repo).resolve()
    require(plan.get('schema') == 'acceptance-mirror-plan/v1', 'Unknown plan schema')
    for binding in plan['bindings']:
        bound(repo, binding)
    root = repo / 'unsolved_math_prioritization'
    state_bytes = (root / 'state.json').read_bytes()
    history_bytes = (root / 'history.jsonl').read_bytes()
    require(sha(state_bytes) == plan['preconditions']['state_sha256'] and sha(history_bytes) == plan['preconditions']['history_sha256'], 'Reviewed plan state/history precondition changed')
    require(sha(plan['state_after_bytes'].encode()) == plan['state_after_sha256'], 'Plan state content hash mismatch')
    require(json.loads(plan['state_after_bytes']) == plan['state_after'], 'Plan state representation mismatch')
    require(sha(history_bytes + plan['history_append_bytes'].encode()) == plan['history_after_sha256'], 'Plan history content hash mismatch')
    before = json.loads(state_bytes)
    selected = {x['id'] for x in plan['decisions']}
    require({k: v for k, v in before.items() if k not in selected} == {k: v for k, v in plan['state_after'].items() if k not in selected}, 'Plan touches unrelated state')
    for decision in plan['decisions']:
        event = plan['state_after'][decision['id']]
        current = source_hashes(repo, decision['id'])
        require(all(event.get(k) == v for k, v in current.items()), 'Reviewed plan source context changed')
        require(event['status'] in TERMINAL and event['turns_used'] == decision['turns_used'] and event['event_id'] == decision['event_id'], 'Reviewed plan decision mismatch')
    return {'preflight': 'PASS', 'targets': len(selected), 'bindings_verified': len(plan['bindings']), 'shared_files_changed': 0,
            'remote_check': 'Pinned saved receipt verification; fresh network acceptance check remains root-owned.'}


def replay_sandbox(plan, sandbox, fail_after_history=False):
    """Only own ignored sandbox; a durable intent receipt guards unknown outcomes."""
    sandbox = Path(sandbox).resolve()
    require(sandbox.is_relative_to(HERE / 'tmp'), 'Replay restricted to helper ignored tmp; live writes prohibited')
    require(plan.get('schema') == 'acceptance-mirror-plan/v1', 'Unknown plan schema')
    state_path, history_path = sandbox / 'state.json', sandbox / 'history.jsonl'
    receipt_path = sandbox / 'sync_intent_receipt.json'
    before = plan['preconditions']
    state_bytes, history_bytes = state_path.read_bytes(), history_path.read_bytes()
    state_hash, history_hash = sha(state_bytes), sha(history_bytes)
    plan_id = sha(encode(plan))
    if receipt_path.exists():
        receipt = load(receipt_path)
        require(receipt['plan_id'] == plan_id, 'Unknown outcome belongs to another plan; inspect receipt')
    else:
        require(state_hash == before['state_sha256'] and history_hash == before['history_sha256'], 'Precondition changed')
        receipt = {'plan_id': plan_id, 'status': 'PREPARED', 'before': before,
                   'state_after_sha256': plan['state_after_sha256'], 'history_after_sha256': plan['history_after_sha256']}
        atomic(receipt_path, encode(receipt))
    require(state_hash in {before['state_sha256'], plan['state_after_sha256']} and history_hash in {before['history_sha256'], plan['history_after_sha256']}, 'Unknown write outcome; no automatic retry')
    require(not (state_hash == plan['state_after_sha256'] and history_hash == before['history_sha256'] and before['history_sha256'] != plan['history_after_sha256']), 'Unexpected write order; inspect unknown outcome')
    if history_hash == before['history_sha256']:
        candidate = history_bytes + plan['history_append_bytes'].encode()
        require(sha(candidate) == plan['history_after_sha256'], 'History plan content hash mismatch')
        atomic(history_path, candidate)
    if fail_after_history:
        raise RuntimeError('Injected interruption after history write')
    if state_hash == before['state_sha256']:
        candidate = plan['state_after_bytes'].encode()
        require(sha(candidate) == plan['state_after_sha256'], 'State plan content hash mismatch')
        atomic(state_path, candidate)
    receipt['status'] = 'COMPLETED'
    atomic(receipt_path, encode(receipt))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--bindings', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-plan', type=Path)
    args = parser.parse_args()
    if args.check_plan:
        print(json.dumps(validate_plan(args.repo, load(args.check_plan))))
        return
    require(args.bindings is not None and args.output is not None, 'Dry run requires bindings and output')
    require(args.output.resolve().is_relative_to(HERE), 'Output restricted to dedicated proposal folder')
    plan = build_plan(args.repo, load(args.bindings))
    args.output.write_bytes(encode(plan))
    print(json.dumps({'dry_run': True, 'targets': len(plan['decisions']), 'history_appends': len(plan['history_append']), 'shared_files_changed': 0}))


if __name__ == '__main__':
    main()
