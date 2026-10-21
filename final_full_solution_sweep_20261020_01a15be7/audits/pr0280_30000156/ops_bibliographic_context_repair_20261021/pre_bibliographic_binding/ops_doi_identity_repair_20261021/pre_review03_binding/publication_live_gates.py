#!/usr/bin/env python3
"""PR280 exact package + root reconciliations + immediately fresh full live gates."""
import json
from pathlib import Path
from ops_binding import *
from prepublication_check import gather


def verify_local_state_exemptions(cleared, known, observed, expected_deposit_id):
    exemptions=cleared.get('unrelated_local_state_exemptions',[])
    if not isinstance(observed,list):
        raise RuntimeError('Observed local deposit states must be a list')
    if not isinstance(exemptions,list):
        raise RuntimeError('Root unrelated-local-state exemptions must be a list')
    allowed={}
    seen_ids=set()
    for entry in exemptions:
        if (not isinstance(entry,dict) or set(entry)!={'path','sha256','deposit_id','disposition'}
                or entry['disposition']!='distinct_non_target'
                or type(entry['deposit_id']) is not int or entry['deposit_id']<=0
                or entry['deposit_id']==expected_deposit_id or entry['deposit_id'] not in known
                or not isinstance(entry['sha256'],str) or not re.fullmatch('[0-9a-f]{64}',entry['sha256'])
                or not isinstance(entry['path'],str)):
            raise RuntimeError('Invalid or contradictory root unrelated-local-state exemption')
        relative=PurePosixPath(entry['path'])
        if (len(relative.parts)!=2 or relative.parts[0]!='.zenodo-state'
                or not relative.name.endswith('.json') or relative.as_posix()!=entry['path']):
            raise RuntimeError('Unrelated state path must be an exact .zenodo-state JSON filename')
        path=safe_file(REPO,entry['path'])
        if not path.is_file() or entry['path'] in allowed or entry['deposit_id'] in seen_ids:
            raise RuntimeError('Missing or duplicate unrelated-local-state exemption')
        data=path.read_bytes()
        value=json.loads(data)
        actual_id=value.get('id',value.get('deposit_id')) if isinstance(value,dict) else None
        if (sha(data)!=entry['sha256'] or type(actual_id) is not int or actual_id!=entry['deposit_id']):
            raise RuntimeError('Root-exempt unrelated local state bytes or exact integer ID changed')
        allowed[entry['path']]=entry
        seen_ids.add(entry['deposit_id'])
    seen_paths=set()
    accepted=[]
    for entry in observed:
        if not isinstance(entry,dict) or type(entry.get('deposit_id')) is not int:
            raise RuntimeError('Malformed observed local deposit state')
        path=entry.get('path')
        if path is not None:
            if not isinstance(path,str) or path in seen_paths:
                raise RuntimeError('Duplicate or malformed observed local state path')
            seen_paths.add(path)
        if expected_deposit_id is not None and entry['deposit_id']==expected_deposit_id:
            # This is the current target state, never a non-target exemption.
            continue
        prior=allowed.get(path)
        if (prior is None or set(entry)!={'path','sha256','deposit_id'}
                or entry['deposit_id']!=prior['deposit_id'] or entry['sha256']!=prior['sha256']):
            raise RuntimeError('Unreviewed or changed non-target local state; exact root exemption required')
        accepted.append({'path':path,'sha256':entry['sha256'],'deposit_id':entry['deposit_id']})
    return accepted


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
    if (not isinstance(leads,list) or any(type(v.get('record')) is not int or v['record']<=0 for v in leads)
            or len({v['record'] for v in leads})!=len(leads)):
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
    if (len(prior_rows)!=len(cleared['ledger_leads']) or any(
            not isinstance(v,str) or not re.fullmatch('[0-9a-f]{64}',v) for v in prior_rows)):
        raise RuntimeError('Duplicate or malformed root ledger digest exemption')
    target_rows=[]
    if allow_target_row and expected_deposit_id is not None:
        from record_publication_ledger import desired_row
        exact_target=desired_row(expected_deposit_id)
    else:
        exact_target=None
    for match in gate['ledger_matches']:
        row=match['values']
        has_current_doi=(expected_deposit_id is not None and
            '10.5281/zenodo.'+str(expected_deposit_id) in set(re.findall(r'10\.5281/zenodo\.\d+',' '.join(row))))
        if has_current_doi:
            if digest(row) in prior_rows:
                raise RuntimeError('Current target DOI/row contradicts a root non-target ledger exemption')
            if exact_target is not None and row==exact_target:
                target_rows.append(match)
                continue
            raise RuntimeError('Current target DOI appears in a changed/unexpected ledger row')
        if digest(row) in prior_rows:
            continue
        raise RuntimeError('New/changed ledger lead; root review required')
    if len(target_rows)>1:
        raise RuntimeError('Duplicate target ledger rows')
    unrelated_states=verify_local_state_exemptions(cleared,known,gate['local_deposit_state_matches'],expected_deposit_id)
    return {'timestamp':stamp(),'phase':phase,'gate_receipt':gate['receipt'],
        'gate_sha256':sha(Path(gate['receipt']).read_bytes()),'target_rows':target_rows,
        'non_target_records_metadata_and_complete_files_unchanged':sorted(known),
        'unrelated_local_states_exactly_root_bound':unrelated_states,
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
