#!/usr/bin/env python3
"""Advance only unambiguous corresponding explicit nonsolution QUEUE statuses.

Any historical claimed_solved row, missing status, multiple-problem ambiguity,
or publication status stops for a root-agent decision. Never audits mathematics,
changes a PR, publishes, or writes the ledger.
"""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
from sweep_io import atomic_json

ROOT=Path(__file__).resolve().parent
EXCLUSIONS={'already_solved','unsolved','duplicate','partial','exhausted','deferred',
            'in_progress','queued','blocked','statement_needs_correction'}
QUEUE_PATHS={'QUEUE.md','unsolved_math_prioritization/QUEUE.md'}


def parse_row(line,queue_path):
    cells=[c.strip() for c in re.split(r'(?<!\\)\|',line.strip().strip('|'))]
    if len(cells)<9 or not cells[0].isdigit():return None
    return {'queue_path':queue_path,'source_line':line,
            'problem_id':cells[1].split('/')[0].strip(),'status':cells[7]}


def independently_bound_rows(evidence,pr):
    """Compare cached scope and row semantics to the actual pinned PR diff."""
    comparison=pr['baseRefOid']+'...'+pr['headRefOid']
    actual_files=subprocess.run(['git','diff','--no-ext-diff','--no-renames','--name-only','-z',comparison],capture_output=True)
    if actual_files.returncode:return None
    paths=actual_files.stdout.decode().rstrip('\0').split('\0') if actual_files.stdout else []
    if set(paths)!=set(evidence['changed_paths']):return None
    expected=set(paths)&QUEUE_PATHS
    changes=[q for q in evidence['queue_changes'] if q['path'] in QUEUE_PATHS]
    if not expected or len(changes)!=len(expected) or {q['path'] for q in changes}!=expected:return None
    actual_rows=[]
    for q in changes:
        actual=subprocess.run(['git','rev-parse',pr['headRefOid']+':'+q['path']],capture_output=True,text=True)
        if actual.returncode or actual.stdout.strip()!=q['sha']:return None
        patch=subprocess.run(['git','diff','--no-ext-diff','--no-renames','--unified=0',comparison,'--',q['path']],capture_output=True,text=True)
        if patch.returncode:return None
        for line in patch.stdout.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                row=parse_row(line[1:],q['path'])
                if row:actual_rows.append(row)
    cached=[q for q in evidence['added_queue_rows'] if q['queue_path'] in QUEUE_PATHS]
    key=lambda q:(q['queue_path'],q['source_line'],q['problem_id'],q['status'])
    if sorted(map(key,cached))!=sorted(map(key,actual_rows)):return None
    return actual_rows


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
        if (evidence.get('pr')!=n or evidence.get('collection_schema')!=2
                or evidence.get('inventory_head_sha')!=prs[n]['headRefOid']
                or evidence.get('inventory_base_sha')!=prs[n]['baseRefOid']):
            print(json.dumps({'stopped_at':n,'reason':'receipt identity or provenance mismatch'}));break
        invalid_paths=[p for p in evidence['changed_paths']
                       if p.startswith('/') or '..' in Path(p).parts]
        if invalid_paths:
            print(json.dumps({'stopped_at':n,'reason':'malformed changed paths'}));break
        canonical_rows=independently_bound_rows(evidence,prs[n])
        if canonical_rows is None:
            print(json.dumps({'stopped_at':n,'reason':'scope or QUEUE semantics not bound to actual pinned PR diff'}));break
        # An arbitrary digit token can be a PR number or traversal metadata.
        # Automatic binding is restricted to the established research layout.
        ids=sorted({m for changed in evidence['changed_paths']
                    for m in re.findall(r'(?:^|/)(?:attempts|problems)/(\d+)(?=/|_)',changed)})
        if len(ids)!=1:
            print(json.dumps({'stopped_at':n,'reason':'ambiguous corresponding problem identifiers','ids':ids}));break
        if any(r['status'] not in EXCLUSIONS for r in canonical_rows):
            print(json.dumps({'stopped_at':n,'reason':'canonical row contains possible solution/publication or noncanonical status'}));break
        extras=[p for p in evidence['changed_paths'] if p not in QUEUE_PATHS
                and not re.search(r'(?:^|/)(?:attempts|problems)/'+re.escape(ids[0])+r'(?=/|_)',p)]
        if extras:
            print(json.dumps({'stopped_at':n,'reason':'unnumbered or other changed scope requires manual correspondence'}));break
        rows=[r for r in canonical_rows if r['problem_id']==ids[0]]
        statuses=set(r['status'] for r in rows)
        if not rows or len(statuses)!=1 or not statuses<=EXCLUSIONS:
            print(json.dumps({'stopped_at':n,'reason':'requires root candidate/publication/missing-status decision','statuses':sorted(statuses)}));break
        status=next(iter(statuses))
        record={'pr':n,'processed_at':dt.datetime.now(dt.timezone.utc).isoformat(),
                'problem_ids':ids,'pr_state':prs[n]['state'],
                'inventory_head_sha':prs[n]['headRefOid'],'inventory_base_sha':prs[n]['baseRefOid'],
                'inventory_updated_at':prs[n].get('updatedAt'),
                'inventory_body_sha256':hashlib.sha256((prs[n].get('body') or '').encode()).hexdigest(),
                'explicit_pr_queue_statuses':[status],'current_classification':status,
                'disposition':'skip_explicit_non_claimed_solved',
                'reason':'Corresponding canonical QUEUE change explicitly has '+status+'; excluded by user eligibility rule2.',
                'queue_source_lines':[r['source_line'] for r in rows],
                'queue_blob_shas':[q['sha'] for q in evidence['queue_changes'] if q['path'] in QUEUE_PATHS],
                'independent_binding':'complete pinned base...head paths and independently parsed added canonical rows; exact cache equality',
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
