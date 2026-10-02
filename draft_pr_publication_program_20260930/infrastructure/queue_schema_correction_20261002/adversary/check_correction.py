#!/usr/bin/env python3
"""Independent, nonmutating named-column queue correction checks.

Reads immutable baseline evidence, proposed or applied queue, accepted package
bindings and source-bound mirror inputs. Writes no files and calls no writers.
"""
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
ROOT = HERE.parent
IDS = ('10000062', '2800102', '10400115', '30003713', '7000019',
       '30004186', '30003955', '10000043')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(test, message):
    if not test:
        raise ValueError(message)


def parse(data):
    lines = data.decode().splitlines(keepends=True)
    headers = [line for line in lines if line.startswith('| Rank | ID / code |')]
    require(len(headers) == 1, 'Ambiguous or missing literal header')
    names = tuple(x.strip() for x in headers[0].strip().strip('|').split('|'))
    require(len(names) == 12 and len(set(names)) == 12, 'Duplicate/missing header column')
    require(set(('ID / code', 'Chat', 'Findings', 'Status', 'Turns', 'DOI')) <= set(names),
            'Required named field missing')
    rows = {}
    identity_position = 1 + names.index('ID / code')
    for n, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        cells = line.rstrip('\n').split('|')
        if len(cells) <= identity_position:
            continue
        identity = cells[identity_position].strip().split('/')[0].strip()
        if identity.isdecimal():
            rows.setdefault(identity, []).append((n, cells))
    return lines, names, rows


def correction(before, after):
    old_lines, old_names, old_rows = parse(before)
    new_lines, new_names, new_rows = parse(after)
    require(old_names == new_names, 'Literal header changed')
    require(len(old_lines) == len(new_lines), 'Line count changed')
    require(old_rows.keys() == new_rows.keys(), 'Numeric row identities changed')
    changed = {n for n, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b}
    selected = set()
    chat = 1 + old_names.index('Chat')
    findings = 1 + old_names.index('Findings')
    observations = []
    for identity in IDS:
        require(len(old_rows.get(identity, [])) == len(new_rows.get(identity, [])) == 1,
                'Selected identity absent or duplicated: ' + identity)
        old_n, old = old_rows[identity][0]
        new_n, new = new_rows[identity][0]
        require(old_n == new_n and len(old) == len(new) == len(old_names) + 2,
                'Selected row moved or malformed: ' + identity)
        selected.add(old_n)
        require(old[chat].strip() and not old[findings].strip(), 'Unexpected selected preimage')
        require(new[findings] == old[chat] and new[chat] == old[findings],
                'Exact named Chat/Findings move failed: ' + identity)
        require(all(a == b for k, (a, b) in enumerate(zip(old, new))
                    if k not in (chat, findings)),
                'Protected selected field changed: ' + identity)
        observations.append({'id': identity, 'changed_named_columns': ['Chat', 'Findings'],
                             'status': new[1 + old_names.index('Status')].strip(),
                             'turns': new[1 + old_names.index('Turns')].strip(),
                             'DOI': new[1 + old_names.index('DOI')].strip(),
                             'findings_sha256': sha(new[findings].encode())})
    require(changed == selected, 'Unrelated row/text changed or selected row unrepaired')
    return observations


def mutate(data, identity, field, value):
    lines, names, rows = parse(data)
    n, cells = rows[identity][0]
    cells = cells.copy()
    cells[1 + names.index(field)] = ' ' + value + ' '
    lines[n] = '|'.join(cells) + ('\n' if lines[n].endswith('\n') else '')
    return ''.join(lines).encode()


def protected_bindings():
    baseline = json.loads((HERE / 'PROTECTED_BINDINGS_BASELINE.json').read_text())
    for binding in baseline['checks']:
        data = (REPO / binding['path']).read_bytes()
        require(sha(data) == binding['expected_sha256'] and len(data) == binding['bytes'],
                'Protected accepted artifact/state/history changed: ' + binding['path'])
    return len(baseline['checks'])


def mirror_noop(before, after):
    path = REPO / 'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
    spec = importlib.util.spec_from_file_location('mirror_readonly', path)
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    original_ledger = mirror.ledger_budget
    original_bound = mirror.bound

    def zero_ledger(data, kind, used, limit):
        if kind != 'json_zero_source_triage':
            return original_ledger(data, kind, used, limit)
        obj = json.loads(data)
        mirror.require(str(obj.get('problem_id')) == '30002145', 'Wrong zero-triage owner')
        mirror.require(used == obj.get('used') == 0 and limit == obj.get('limit') == 5,
                       'Zero-triage ledger mismatch')
        mirror.require(obj.get('substantive_proof_attempts') == [] and
                       isinstance(obj.get('reason'), str) and obj['reason'],
                       'Unjustified zero-triage budget')

    mirror.ledger_budget = zero_ledger
    proposal = json.loads((REPO / 'draft_pr_publication_program_20260930/audits/pr31_10000043/state_mirror_bindings.json').read_text())
    queue_path = proposal['queue']['path']
    # Inventory stage may have advanced for pending PRs; complete accepted scope
    # remains checked by the actual source-bound builder, without old attestations.
    proposal['inventory']['sha256'] = sha((REPO / proposal['inventory']['path']).read_bytes())
    plans = []
    for data in (before, after):
        current = copy.deepcopy(proposal)
        current['queue']['sha256'] = sha(data)

        def bound(repo, binding, queue_bytes=data):
            if binding['path'] == queue_path:
                mirror.require(binding['sha256'] == sha(queue_bytes), 'Wrong in-memory queue binding')
                return queue_bytes
            return original_bound(repo, binding)

        mirror.bound = bound
        plan = mirror.build_plan(REPO, current, '2026-10-02T02:31:28.089410+00:00')
        preflight = mirror.validate_plan(REPO, plan)
        require(plan['primary_count'] == 21 and plan['duplicate_count'] == 1,
                'Accepted source-bound scope changed')
        require(plan['history_append'] == [], 'Unexpected accepted history append')
        require(plan['state_after_bytes'].encode() == (REPO / 'unsolved_math_prioritization/state.json').read_bytes(),
                'Mirror would change accepted state bytes')
        require(all(not x['state_changed'] and not x['history_append'] for x in plan['decisions']),
                'Mirror would change accepted state/decision')
        require(sum(x['turns_used'] for x in plan['state_after'].values()) == 26,
                'Original attempt count changed')
        plans.append((plan, preflight))
    require(plans[0][0]['decisions'] == plans[1][0]['decisions'], 'Acceptance decisions differ')
    require(plans[0][0]['state_after_bytes'] == plans[1][0]['state_after_bytes'], 'State bytes differ')
    require(plans[0][0]['history_after_sha256'] == plans[1][0]['history_after_sha256'], 'History hash differs')
    return {'both_actual_source_bound_preflights': [x[1] for x in plans],
            'state_sha256': plans[1][0]['state_after_sha256'],
            'history_sha256': plans[1][0]['history_after_sha256'],
            'history_appends': 0, 'primary_acceptances': 21, 'duplicate_acceptances': 1,
            'original_consumed_turns': 26,
            'scope': 'Actual builder and validator; only QUEUE bytes substituted in memory. No file writer called.'}


def main():
    before = (HERE / 'INITIAL_QUEUE_cab3546c2.md').read_bytes()
    after_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'QUEUE_CANDIDATE.md'
    after = after_path.read_bytes()
    observed = correction(before, after)
    plan = json.loads((ROOT / 'ROOT_CORRECTION_PLAN.json').read_text())
    require(sha(before) == plan['before_sha256'] and sha(after) == plan['candidate_sha256'],
            'Root candidate hash differs from independently checked bytes')
    prior = json.loads((HERE / 'PREMERGE_AND_MIRROR_INSPECTION.json').read_text())
    require({x['id'] for x in prior} == set(IDS) and all(not x['premerge']['Chat'] for x in prior),
            'Blank Chat is not supported by all actual premerge first parents')
    negatives = []
    fixtures = [('unrepaired old misplaced findings', before),
                ('selected Status alteration', mutate(after, IDS[0], 'Status', 'claimed_solved')),
                ('selected original attempt reset', mutate(after, IDS[0], 'Turns', '0/5')),
                ('selected invented DOI', mutate(after, IDS[0], 'DOI', '10.5281/zenodo.99999999')),
                ('selected lost findings prose', mutate(after, IDS[0], 'Findings', '')),
                ('selected retained prose in Chat', mutate(after, IDS[0], 'Chat', 'Accepted bad location')),
                ('unrelated published DOI alteration', mutate(after, '30005473', 'DOI', '10.5281/zenodo.99999998')),
                ('unrelated real Chat link alteration', mutate(after, '30000990', 'Chat', 'https://chatgpt.com/c/wrong')),
                ('unrelated queue header alteration', after.replace(b'| Impact (/10) |', b'| Impact |', 1)),
                ('extra malformed selected duplicate', after + b'| 39 | 10400115 / AMR-103-0115 | broken |\n')]
    for label, data in fixtures:
        try:
            correction(before, data)
        except (ValueError, KeyError) as error:
            negatives.append({'label': label, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Negative control accepted: ' + label)
    protected = protected_bindings()
    noop = mirror_noop(before, after)
    # Repeat all protected-byte checks after both genuine read-only builder runs.
    require(protected_bindings() == protected, 'Read-only validation changed protected evidence')
    print(json.dumps({'utc': datetime.now(timezone.utc).isoformat(), 'verdict': 'PASS',
                      'before_sha256': sha(before), 'after_sha256': sha(after),
                      'actual_header_derived_changes': observed,
                      'protected_actual_files_checked_before_and_after': protected,
                      'negative_controls': negatives, 'mirror_noop': noop,
                      'shared_files_written': 0, 'new_proof_turns': 0}, indent=2))


if __name__ == '__main__':
    main()
