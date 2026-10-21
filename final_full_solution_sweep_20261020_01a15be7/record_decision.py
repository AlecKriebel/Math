"""Root-agent decisions only; this module does not infer scientific identity."""
import datetime as dt
import json
from pathlib import Path
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent


def record(pr,decision):
    state=json.loads((ROOT/'STATE.json').read_text())
    if state['next_pr']!=pr:raise RuntimeError('Decision must follow numerical cursor')
    journal=[json.loads(s) for s in (ROOT/'dispositions.jsonl').read_text().splitlines()]
    if [x['pr'] for x in journal]!=list(range(9,pr)):raise RuntimeError('Journal not contiguous or decision already recorded')
    inv=json.loads((ROOT/'rest_inventory.json').read_text())
    metadata=next(x for x in inv['pull_requests'] if x['number']==pr)
    evidence=json.loads((ROOT/f'eligibility/pr{pr:04d}.json').read_text())
    if evidence['pr']!=pr or evidence['inventory_head_sha']!=metadata['headRefOid'] or evidence['inventory_base_sha']!=metadata['baseRefOid']:
        raise RuntimeError('Unbound eligibility receipt')
    result={'pr':pr,'processed_at':dt.datetime.now(dt.timezone.utc).isoformat(),
            'pr_state':metadata['state'],'inventory_head_sha':metadata['headRefOid'],
            'inventory_base_sha':metadata['baseRefOid'],
            'new_mathematical_audit':False,'new_publication':False,'spreadsheet_mutation':False,
            'requires_final_live_head_recheck':True,**decision}
    atomic_json(ROOT/f'PR{pr:04d}_DISPOSITION.json',result)
    with (ROOT/'dispositions.jsonl').open('a') as f:f.write(json.dumps(result,sort_keys=True)+'\n')
    state.update(next_pr=pr+1,last_completely_processed_pr=pr,completed_pr_count=pr-8,
                 active_candidate=None,status='ordered_sweep')
    atomic_json(ROOT/'STATE.json',state)
    return result


def published(pr,problem_ids,row,doi,reason):
    leads=json.loads((ROOT/f'PR{pr:04d}_PUBLICATION_LEADS.json').read_text())
    normalized=doi.removeprefix('https://doi.org/')
    matches=[x for x in leads['matches'] if x['row']==row and len(x['values'])>=3
             and str(x['values'][2]).removeprefix('https://doi.org/').strip()==normalized]
    records=[x for x in leads['records'] if x['doi']==normalized and x['published'] and x['doi_resolution']['status']==200]
    if len(matches)!=1 or len(records)!=1:raise RuntimeError('Publication/row lead not verified')
    rec=records[0]
    atomic_json(ROOT/f'PR{pr:04d}_PUBLICATION_VERIFICATION.json',{
        **rec,'checked_at':leads['checked_at'],'ledger_row':row,
        'root_identity_review':reason,'identity_comparison_fields':['original problem and source alias','mathematical objects/hypotheses/conclusion','PR reference','paper title','DOI'],
        'review_type':'existing-publication identity and payload coverage, not a new proof/novelty audit'})
    return record(pr,{'problem_ids':problem_ids,'current_classification':'published',
        'disposition':'skip_entirely_already_published','duplicate_check':'already_published_correctly_recorded',
        'doi':normalized,'ledger_row':row,'ledger_checked_at':leads['checked_at'],
        'reason':reason,'publication_evidence':f'PR{pr:04d}_PUBLICATION_VERIFICATION.json'})


def withdrawn(pr,problem_ids,reason,correction_reference):
    current=json.loads((ROOT/'CURRENT_CANONICAL_QUEUE_SNAPSHOT.json').read_text())
    rows=[current['rows'][i] for i in problem_ids]
    if not rows or any(r['status'] not in {'already_solved','unsolved','partial','duplicate','exhausted','deferred'} for r in rows):
        raise RuntimeError('No explicit current negative status')
    return record(pr,{'problem_ids':problem_ids,'explicit_pr_queue_statuses':['claimed_solved'],
        'current_classification':rows[0]['status'],'disposition':'skip_explicit_non_claimed_solved',
        'canonical_statuses':rows,'canonical_snapshot_commit':current['main'],
        'correction_reference':correction_reference,'reason':reason,
        'duplicate_check':'live_GWS_leads_reconciled; current explicit withdrawal excludes substantive mathematics under user rule2'})
