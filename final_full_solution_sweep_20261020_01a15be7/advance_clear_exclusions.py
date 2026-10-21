#!/usr/bin/env python3
"""Advance only unambiguous corresponding explicit nonsolution QUEUE statuses.

Any historical claimed_solved row, missing status, multiple-problem ambiguity,
or publication status stops for a root-agent decision. Never audits mathematics,
changes a PR, publishes, or writes the ledger.
"""
import datetime as dt
import json
from pathlib import Path
import re
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent
# All usable explicit statuses other than a full-solution/publication claim are
# excluded by user rule2. Publication-like states stop for a ledger comparison.
PUBLICATION_OR_CLAIM={'claimed_solved','preprint_published','published','resolved','scoped_resolved'}
QUEUE_PATHS={'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}


def main():
    inventory=json.loads((ROOT/'rest_inventory.json').read_text())
    prs={p['number']:p for p in inventory['pull_requests']}
    state=json.loads((ROOT/'STATE.json').read_text())
    processed=[]
    while state['next_pr']<=inventory['highest_pr']:
        n=state['next_pr']
        if n not in prs:
            raise RuntimeError('Numeric gap requires individual investigation')
        path=ROOT/'eligibility'/f'pr{n:04d}.json'
        if not path.exists():
            print(json.dumps({'stopped_at':n,'reason':'no structural receipt yet'}));break
        evidence=json.loads(path.read_text())
        canonical_rows=[r for r in evidence['added_queue_rows'] if r['queue_path'] in QUEUE_PATHS]
        # Custom effort folders need not use attempts/<id>. Exact digit tokens
        # bind a QUEUE row to changed research files without substring matches.
        path_tokens={token for changed in evidence['changed_paths'] if changed not in QUEUE_PATHS
                     for token in re.findall(r'\d+',changed)}
        ids=sorted(set(evidence['path_problem_ids']) |
                   {r['problem_id'] for r in canonical_rows if r['problem_id'] in path_tokens})
        if len(ids)!=1:
            print(json.dumps({'stopped_at':n,'reason':'ambiguous corresponding problem identifiers','ids':ids}));break
        rows=[r for r in canonical_rows if r['problem_id']==ids[0]]
        statuses=set(r['status'] for r in rows)
        if not rows or len(statuses)!=1 or not next(iter(statuses),'').strip() or statuses & PUBLICATION_OR_CLAIM:
            print(json.dumps({'stopped_at':n,'reason':'requires root candidate/publication/missing-status decision','statuses':sorted(statuses)}));break
        status=next(iter(statuses))
        record={'pr':n,'processed_at':dt.datetime.now(dt.timezone.utc).isoformat(),
                'problem_ids':ids,'pr_state':prs[n]['state'],
                'inventory_head_sha':prs[n]['headRefOid'],'inventory_base_sha':prs[n]['baseRefOid'],
                'explicit_pr_queue_statuses':[status],'current_classification':status,
                'disposition':'skip_explicit_non_claimed_solved',
                'reason':'Corresponding canonical QUEUE change explicitly has '+status+'; excluded by user eligibility rule2.',
                'queue_source_lines':[r['source_line'] for r in rows],
                'queue_blob_shas':[q['sha'] for q in evidence['queue_changes'] if q['path'] in QUEUE_PATHS],
                'new_mathematical_audit':False,'new_publication':False,'spreadsheet_mutation':False,
                'duplicate_check':'not_started_as_candidate; excluded by explicit status before substantive mathematics',
                'requires_final_live_head_recheck':True}
        atomic_json(ROOT/f'PR{n:04d}_DISPOSITION.json',record)
        with (ROOT/'dispositions.jsonl').open('a') as f:f.write(json.dumps(record,sort_keys=True)+'\n')
        state.update(next_pr=n+1,last_completely_processed_pr=n,completed_pr_count=n-8)
        atomic_json(ROOT/'STATE.json',state)
        processed.append(n)
    print(json.dumps({'advanced':processed,'next_pr':state['next_pr']}))


if __name__=='__main__':
    main()
