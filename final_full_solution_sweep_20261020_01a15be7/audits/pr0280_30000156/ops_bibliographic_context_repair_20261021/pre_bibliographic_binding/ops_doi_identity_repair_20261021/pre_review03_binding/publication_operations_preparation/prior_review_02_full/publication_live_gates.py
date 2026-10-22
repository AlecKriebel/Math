#!/usr/bin/env python3
"""PR280 exact package + root reconciliations + immediately fresh full live gates."""
import json
from pathlib import Path
from ops_binding import *
from prepublication_check import gather


def reconcile(gate, phase, expected_head, expected_deposit_id=None, allow_target_row=False):
    fresh(gate['started_utc'])
    fresh(gate['completed_utc'])
    if (gate['phase']!=phase or gate.get('expected_pr_head')!=expected_head
            or gate.get('expected_deposit_id')!=expected_deposit_id or gate.get('read_only') is not True
            or gate.get('release_manifest_sha256')!=RELEASE_SHA or gate.get('release_files')!=release()['files']
            or gate.get('account_positive_control')!='PASS_23174283'):
        raise RuntimeError('Malformed or wrong-phase/head live gate')
    cleared=json.loads((AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_text())
    if (cleared.get('pr')!=280 or cleared.get('root_identity_reconciliation_complete') is not True
            or cleared.get('unresolved_leads')!=[] or cleared.get('release_manifest_sha256')!=RELEASE_SHA):
        raise RuntimeError('Root exact identity reconciliation absent/incomplete')
    raw=Path(gate['raw_receipts'])
    account_path=raw/'account_complete.json'
    if sha(account_path.read_bytes())!=gate['account_complete_sha256']:
        raise RuntimeError('Complete account receipt changed')
    account=json.loads(account_path.read_text())
    records={int(v['id']):v for v in account['records']}
    if len(records)!=account['total'] or len(records)!=gate['account_complete_total']:
        raise RuntimeError('Account gate inventory is incomplete or duplicated')
    leads=cleared.get('account_leads')
    if not isinstance(leads,list) or len({v['record'] for v in leads})!=len(leads):
        raise RuntimeError('Root account lead schema invalid')
    known={int(v['record']):v for v in leads}
    if any(v.get('disposition')!='distinct_non_target' for v in leads) or expected_deposit_id in known:
        raise RuntimeError('Only explicit root-distinct non-target records may be exempted')
    for identifier,prior in known.items():
        if identifier not in records or digest(identity_projection(records[identifier]))!=prior['metadata_and_files_sha256']:
            raise RuntimeError('Root-cleared non-target metadata or complete file projection changed')
    if not {int(v['id']) for v in gate['unexpected_account_matches']}.issubset(known):
        raise RuntimeError('New account publication/draft lead; root review required')
    if expected_deposit_id is not None and expected_deposit_id not in records:
        raise RuntimeError('Expected record/draft missing')
    if not isinstance(cleared.get('ledger_leads'),list) or any(
            v.get('disposition')!='distinct_non_target' for v in cleared['ledger_leads']):
        raise RuntimeError('Root ledger lead dispositions absent')
    prior_rows={v['values_sha256'] for v in cleared['ledger_leads']}
    target_rows=[]
    if allow_target_row and expected_deposit_id is not None:
        from record_publication_ledger import desired_row
        exact_target=desired_row(expected_deposit_id)
    else:
        exact_target=None
    for match in gate['ledger_matches']:
        row=match['values']
        if digest(row) in prior_rows:
            continue
        if exact_target is not None and row==exact_target:
            target_rows.append(match)
            continue
        raise RuntimeError('New/changed ledger lead; root review required')
    if len(target_rows)>1:
        raise RuntimeError('Duplicate target ledger rows')
    if gate['local_deposit_state_matches'] and (expected_deposit_id is None or any(
            type(v.get('deposit_id')) is not int or v['deposit_id']!=expected_deposit_id
            for v in gate['local_deposit_state_matches'])):
        raise RuntimeError('Unexpected local target deposit state')
    return {'timestamp':stamp(),'phase':phase,'gate_receipt':gate['receipt'],
        'gate_sha256':sha(Path(gate['receipt']).read_bytes()),'target_rows':target_rows,
        'non_target_records_metadata_and_complete_files_unchanged':sorted(known),
        'root_reconciliation_sha256':sha((AUDIT/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes()),
        'new_unreviewed_publication_or_ledger_leads':[],'read_only':True}


def collect(phase, expected_head, expected_deposit_id=None, allow_target_row=False):
    require_release_clearance()
    gate=gather(phase,expected_head,expected_deposit_id)
    acceptance=reconcile(gate,phase,expected_head,expected_deposit_id,allow_target_row)
    require_release_clearance()
    fresh(gate['started_utc'])
    atomic_json(Path(gate['raw_receipts'])/'acceptance.json',acceptance)
    return gate,acceptance
