#!/usr/bin/env python3
"""Read-only structural coverage of the resumable sweep; never proof/priority clearance."""
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def snapshot():
    state = json.loads((ROOT/'STATE.json').read_text())
    inventory = json.loads((ROOT/'rest_inventory.json').read_text())
    journal = [json.loads(line) for line in (ROOT/'dispositions.jsonl').read_text().splitlines() if line.strip()]
    numbers = [entry['pr'] for entry in journal]
    if numbers != list(range(state['start_pr'], state['next_pr'])):
        raise RuntimeError('Ordered journal is not the exact numerical prefix ending before next_pr')
    if state['last_completely_processed_pr'] != state['next_pr']-1 or state['completed_pr_count'] != len(numbers):
        raise RuntimeError('Cursor/count disagrees with ordered journal')
    known = {entry['number'] for entry in inventory['pull_requests']}
    if len(known) != inventory['in_scope_pr_count'] or max(known) != inventory['highest_pr']:
        raise RuntimeError('Inventory total/maximum mismatch')
    gaps = set(inventory['numeric_gaps'])
    if known | gaps != set(range(state['start_pr'], inventory['highest_pr']+1)) or known & gaps:
        raise RuntimeError('Inventory numbers/gap partition incomplete')
    if any(number not in known for number in numbers):
        raise RuntimeError('Journal contains a number absent from the actual PR inventory')
    for entry in journal:
        saved = json.loads((ROOT/('PR%04d_DISPOSITION.json' % entry['pr'])).read_text())
        if saved != entry:
            raise RuntimeError('Per-PR disposition differs from journal: '+str(entry['pr']))
    own = state.get('completed_publications', [])
    own_dois = [entry['doi'].removeprefix('https://doi.org/') for entry in own]
    if len(set(own_dois)) != len(own_dois):
        raise RuntimeError('Own completed publication list repeats a DOI')
    for entry in own:
        evidence = ROOT/entry['verification']
        if not evidence.is_file():
            raise RuntimeError('Own completed publication lacks its verification artifact')
    counts = dict(collections.Counter(entry['disposition'] for entry in journal))
    doi_prs = collections.defaultdict(list)
    for entry in journal:
        if entry.get('doi'):
            doi_prs[entry['doi'].removeprefix('https://doi.org/')].append(entry['pr'])
    pending = sorted(known-set(numbers))
    return {
        'timestamp_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': 'Structural progress only. No new mathematical, priority, live publication, sheet or final-reconciliation certification.',
        'inventory_timestamp': inventory['completed_at'],
        'highest_pr': inventory['highest_pr'],
        'in_scope_pr_count': len(known),
        'numeric_issue_gaps': sorted(gaps),
        'contiguous_completed_prefix': {'from': state['start_pr'], 'through': state['last_completely_processed_pr'], 'count': len(numbers)},
        'next_pr': state['next_pr'], 'pending_pr_count': len(pending),
        'first_pending_pr': pending[0] if pending else None,
        'last_pending_pr': pending[-1] if pending else None,
        'disposition_counts': counts,
        'own_completed_publications': own,
        'own_completed_dois_unique': True,
        'same_record_referenced_by_multiple_processed_PRs': {doi:prs for doi,prs in sorted(doi_prs.items()) if len(prs)>1},
        'reopened_candidates_requiring_final_override': state.get('reopened_candidates', []),
        'all_inventory_PRs_considered': not pending,
        'final_reconciliation_complete': False,
        'journal_sha256': hashlib.sha256((ROOT/'dispositions.jsonl').read_bytes()).hexdigest(),
        'completion_estimate_percent': state['completion_estimate_percent'],
    }

if __name__ == '__main__':
    print(json.dumps(snapshot(), indent=2))
