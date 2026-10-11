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
TERMINAL = {'unsolved', 'already_solved', 'preprint_published', 'duplicate'}
MIRROR_EVENTS = {'acceptance_mirror_import', 'acceptance_duplicate_mirror_import'}


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
        elif kind == 'json_number_turns':
            require(obj['used'] == used and obj['limit'] == limit, 'Original budget mismatch')
            require([x['number'] for x in obj['turns']] == list(range(1, used + 1)), 'Ambiguous numbered attempt list')
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


def package_bindings(repo, manifest_binding, audit):
    """Check the accepted canonical package, with each actual file independently bound."""
    data = bound(repo, manifest_binding)
    require(audit.get('canonical_manifest_sha256') == sha(data), 'Audit/canonical manifest mismatch')
    manifest = json.loads(data)
    parent = Path(manifest_binding['path']).parent
    bindings = []
    paths = []
    for item in manifest['files']:
        child = Path(item['path'])
        require(not child.is_absolute() and '..' not in child.parts, 'Unsafe canonical manifest path')
        binding = {'path': str(parent / child), 'sha256': item['sha256']}
        payload = bound(repo, binding)
        require(len(payload) == item['bytes'], 'Canonical manifest byte count mismatch')
        paths.append(binding['path'])
        bindings.append(binding)
    require(len(paths) == len(set(paths)), 'Duplicate canonical manifest path')
    return bindings


def build_plan(repo, spec, timestamp=None, source_reader=source_hashes):
    repo = Path(repo).resolve()
    timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    require(spec.get('authorization') == 'human_authorized_current_acceptance_mirror', 'Explicit current-mirror authorization missing')
    require(spec.get('revision') == 2, 'Explicit proposal revision2 required')
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
    events = {x['event_id']: x for x in history if x.get('event') in MIRROR_EVENTS}
    require(len(events) == sum(x.get('event') in MIRROR_EVENTS for x in history), 'Duplicate mirror history event')
    item_by_pr = {x['number']: x for x in inventory['items']}
    require(len(item_by_pr) == len(inventory['items']), 'Duplicate PR inventory entry')
    entries = spec['entries']
    require(len({x['id'] for x in entries}) == len(entries), 'Duplicate selected ID')
    require(len({x['pr'] for x in entries}) == len(entries), 'Duplicate selected PR')
    completed = {x['number'] for x in inventory['items'] if x.get('stage') == 'complete'}
    require(completed == set(spec['required_completed_prs']) == {x['pr'] for x in entries}, 'Completed-primary scope changed/ambiguous')
    duplicate_entries = spec.get('duplicate_mirrors', [])
    duplicate_by_id = {x['id']: x for x in duplicate_entries}
    require(len(duplicate_by_id) == len(duplicate_entries), 'Duplicate duplicate-mirror ID')
    require(not ({x['id'] for x in entries} & set(duplicate_by_id)), 'Primary/duplicate identity overlap')
    after = copy.deepcopy(state)
    appends, decisions = [], []
    bindings = [spec[k] for k in ['inventory', 'queue', 'catalog', 'policy']]
    if spec.get('historical_v1_seal'):
        seal = json.loads(bound(repo, spec['historical_v1_seal']))
        parent = (repo / spec['historical_v1_seal']['path']).parent
        for old in seal['files']:
            historical = {'path': str((parent / old['path']).resolve().relative_to(repo)), 'sha256': old['sha256']}
            require(len(bound(repo, historical)) == old['bytes'], 'Historical v1 byte count changed')
            bindings.append(historical)
        bindings.append(spec['historical_v1_seal'])
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
        require(status in TERMINAL - {'duplicate'}, 'Unsupported/unaccepted primary status')
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
        if entry.get('canonical_manifest'):
            audit = json.loads(bound(repo, entry['audit_acceptance']))
            require(str(audit.get('problem_id')) == identity and audit.get('pr') == pr, 'Audit acceptance identity mismatch')
            require(audit.get('merge_commit') == merge and audit.get('queue_status') == status and audit.get('original_head') == expected_head, 'Audit/canonical exact acceptance mismatch')
            bindings += package_bindings(repo, entry['canonical_manifest'], audit)
        duplicates = entry.get('duplicates', [])
        require(identity not in duplicates and len(set(duplicates)) == len(duplicates), 'Invalid selected duplicate group')
        for duplicate in duplicates:
            requested = duplicate_by_id.get(duplicate)
            require(duplicate in catalog, 'Duplicate source absent from catalog')
            if catalog[duplicate].get('eligible') is not False:
                require(requested is not None and requested.get('shared_budget_owner') == identity, 'Selected duplicate still research-eligible; explicit bound mirror needed')
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
        for key in ['artifact', 'publication', 'canonical_acceptance_text', 'duplicate_evidence', 'canonical_manifest', 'audit_acceptance']:
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
            require(prior.get('event') not in MIRROR_EVENTS, 'Existing acceptance mirror differs; explicit revision review required')
            appends.append(event)
        after[identity] = event
        decisions.append({'id': identity, 'pr': pr, 'status': status, 'turns_used': used,
                          'turn_limit': limit, 'doi': doi, 'event_id': event_id,
                          'state_changed': prior != event, 'history_append': existing is None})
        bindings += [entry[k] for k in ['acceptance', 'remote', 'accepted_source']]
        bindings += [budget['ledger']]
        bindings += [entry[k] for k in ['artifact', 'publication', 'canonical_acceptance_text', 'duplicate_evidence', 'canonical_manifest', 'audit_acceptance'] if k in entry]
    duplicate_decisions = []
    entry_by_id = {x['id']: x for x in entries}
    for duplicate in duplicate_entries:
        identity, owner = duplicate['id'], duplicate['shared_budget_owner']
        require(type(duplicate.get('additional_independent_proof_turns')) is int and duplicate['additional_independent_proof_turns'] == 0, 'Requested duplicate accounting must add zero proof turns')
        require(owner in entry_by_id and owner != identity, 'Shared budget owner absent/invalid')
        primary = entry_by_id[owner]
        require(identity in primary.get('duplicates', []), 'Duplicate not explicitly selected by primary')
        acceptance = json.loads(bound(repo, primary['acceptance']))
        require(str(acceptance.get('problem_id')) == owner and str(acceptance.get('duplicate_id')) == identity, 'Accepted duplicate/owner relation mismatch')
        require(acceptance.get('duplicate_queue_status') == 'duplicate', 'Duplicate disposition not accepted')
        require(type(acceptance.get('duplicate_additional_attempts_used')) is int and acceptance['duplicate_additional_attempts_used'] == 0, 'Duplicate has independent proof turn; explicit accounting repair needed')
        matches = rows.get(identity, [])
        require(len(matches) == 1 and matches[0] is not None, 'Duplicate queue row absent/ambiguous')
        row = matches[0]
        limit = primary['budget']['limit']
        require(row['Status'] == 'duplicate' and row['Turns'] == f'0/{limit}' and not row['DOI'], 'Duplicate queue disposition/budget/DOI mismatch')
        require(identity in catalog and catalog[identity].get('present') is True, 'Duplicate catalog source absent')
        require(type(catalog[identity].get('turns_used')) is int and catalog[identity]['turns_used'] == 0, 'Duplicate catalog records extra proof usage')
        current = source_reader(repo, identity)
        require(all(catalog[identity].get(k) == current[k] for k in ['statement_hash', 'review_hash']), 'Duplicate current source/catalog mismatch')
        statement_hash = accepted_statement(bound(repo, duplicate['accepted_source']), identity, current)
        require(statement_hash == current['statement_hash'], 'Accepted duplicate statement mismatch')
        provenance = json.loads(bound(repo, duplicate['relation_evidence']))
        require(str(provenance.get('problem_id')) == owner and str(provenance.get('duplicate_problem_id')) == identity, 'Duplicate relation provenance mismatch')
        require(provenance.get('duplicate_source_record_sha256') == duplicate['accepted_source']['sha256'], 'Accepted duplicate source hash mismatch')
        ledger = json.loads(bound(repo, primary['budget']['ledger']))
        require(str(ledger.get('shared_duplicate')) == identity, 'Original ledger does not share this duplicate')
        require(ledger['used'] == after[owner]['turns_used'] and ledger['limit'] == after[owner]['turn_limit'], 'Shared owner budget mismatch')
        prior = state.get(identity, {})
        require(type(prior.get('turns_used', 0)) is int and prior.get('turns_used', 0) == 0, 'Duplicate existing independent usage cannot be erased')
        evidence = {'canonical_acceptance': primary['acceptance'], 'remote_acceptance': primary['remote'],
                    'accepted_duplicate_source': duplicate['accepted_source'], 'duplicate_relation': duplicate['relation_evidence'],
                    'shared_original_ledger': primary['budget']['ledger'], 'canonical_acceptance_text': primary['canonical_acceptance_text'],
                    'merge_commit': after[owner]['evidence']['merge_commit'], 'reviewed_head': after[owner]['evidence']['reviewed_head'],
                    'authorization': spec['authorization'], 'import_is_present_day_mirror': True,
                    'historical_transitions_asserted': False, 'additional_independent_proof_turns': 0}
        core = {'id': identity, 'pr': primary['pr'], 'status': 'duplicate', 'turns_used': 0,
                'turn_limit': limit, 'independent_budget_allocated': False, 'shared_budget_owner': owner,
                'shared_turns_used': after[owner]['turns_used'], 'shared_turn_limit': limit,
                **current, 'doi': None, 'evidence': evidence}
        event_id = sha(encode(core))
        event = {**prior, **core, 'event': 'acceptance_duplicate_mirror_import', 'event_id': event_id,
                 'at': timestamp, 'note': 'Human-authorized current accepted duplicate mirror; zero additional proof turns; five-turn limit belongs to shared owner.'}
        existing = events.get(event_id)
        if existing:
            require(all(existing.get(k) == v for k, v in core.items()), 'Existing duplicate mirror conflict')
            event = existing
        else:
            require(prior.get('event') not in MIRROR_EVENTS, 'Existing duplicate mirror differs; explicit review required')
            appends.append(event)
        after[identity] = event
        decision = {'id': identity, 'pr': primary['pr'], 'status': 'duplicate', 'turns_used': 0, 'turn_limit': limit,
                    'shared_budget_owner': owner, 'independent_budget_allocated': False, 'doi': None,
                    'event_id': event_id, 'state_changed': prior != event, 'history_append': existing is None}
        decisions.append(decision)
        duplicate_decisions.append(decision)
        bindings += [duplicate['accepted_source'], duplicate['relation_evidence']]
    new_history = history_bytes + b''.join((json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n').encode() for x in appends)
    # Preserve original state bytes for a genuine no-op replay.
    after_bytes = state_bytes if after == state else encode(after)
    return {'schema': 'acceptance-mirror-plan/v2', 'created_at_utc': timestamp, 'proposal_spec': copy.deepcopy(spec), 'dry_run': True,
            'writes_authorized_to_live_repo': False, 'bindings': bindings,
            'preconditions': {'state_sha256': sha(state_bytes), 'history_sha256': sha(history_bytes),
                              'queue_sha256': sha(queue_data)},
            'decisions': decisions, 'state_after': after, 'history_append': appends,
            'primary_count': len(entries), 'duplicate_count': len(duplicate_decisions), 'duplicate_decisions': duplicate_decisions,
            'state_after_sha256': sha(after_bytes), 'history_after_sha256': sha(new_history),
            'state_after_bytes': after_bytes.decode(), 'history_append_bytes': new_history[len(history_bytes):].decode(),
            'protected': ['QUEUE.md', 'catalog.json', 'assessments.json', 'historical desk reviews', 'original v1 artifacts', 'unselected duplicate states', 'publication and tracker state'],
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
    require(plan.get('schema') == 'acceptance-mirror-plan/v2', 'Unknown plan schema')
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
        if event['status'] == 'duplicate':
            owner = plan['state_after'].get(event.get('shared_budget_owner'), {})
            require(owner.get('status') in TERMINAL - {'duplicate'} and event['turns_used'] == 0 and event.get('independent_budget_allocated') is False, 'Reviewed duplicate budget semantics invalid')
            require(owner.get('turns_used') == event.get('shared_turns_used') and owner.get('turn_limit') == event.get('shared_turn_limit'), 'Reviewed shared owner accounting mismatch')
    # A plan hash alone cannot prove that its bytes encode the accepted outcome.
    # Rebuild from the same current evidence, source records and import timestamp.
    expected = build_plan(repo, plan['proposal_spec'], plan['created_at_utc'])
    require(encode(expected) == encode(plan), 'Reviewed plan does not reproduce the exact accepted evidence/accounting')
    return {'preflight': 'PASS', 'targets': len(selected), 'bindings_verified': len(plan['bindings']), 'shared_files_changed': 0,
            'remote_check': 'Pinned saved receipt verification; fresh network acceptance check remains root-owned.'}


def replay_sandbox(plan, sandbox, fail_after_history=False):
    """Only own ignored sandbox; a durable intent receipt guards unknown outcomes."""
    sandbox = Path(sandbox).resolve()
    require(sandbox.is_relative_to(HERE / 'tmp'), 'Replay restricted to helper ignored tmp; live writes prohibited')
    require(plan.get('schema') == 'acceptance-mirror-plan/v2', 'Unknown plan schema')
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
