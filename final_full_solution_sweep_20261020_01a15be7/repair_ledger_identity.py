#!/usr/bin/env python3
"""Append missing identifiers to one verified publication's existing Notes cell.

Scientific identity is an explicit root decision, never inferred by this tool.
No publication or new row is created. An exact whole-cell conditional replacement
and full readback preserve concurrent changes rather than overwrite stale notes.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import uuid
from publication_check import ROOT, SHEET, get, zenodo_dois
from checkpoint import live_main
from sweep_io import atomic_json


def gws(resource,params,body=None):
    command=['gws','sheets','spreadsheets']+resource+['--params',json.dumps(params)]
    if body is not None:command+=['--json',json.dumps(body)]
    return json.loads(subprocess.run(command,capture_output=True,text=True,check=True).stdout)


def read_ledger(render='FORMATTED_VALUE'):
    return gws(['values','get'],{'spreadsheetId':SHEET,
        'range':"'Math Puzzles'!A:AQ",'valueRenderOption':render})


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('pr',type=int)
    parser.add_argument('--problem-id',required=True)
    parser.add_argument('--alias',required=True)
    parser.add_argument('--row',type=int,required=True)
    parser.add_argument('--doi',required=True)
    parser.add_argument('--reason',required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    if args.pr<9 or args.row<2 or not args.problem_id.isdigit():raise RuntimeError('Invalid target')
    match=re.fullmatch(r'10\.5281/zenodo\.(\d+)',args.doi)
    if not match:raise RuntimeError('An exact Zenodo version DOI is required')
    record=int(match.group(1))
    receipt_path=ROOT/f'PR{args.pr:04d}_LEDGER_REPAIR.json'
    if receipt_path.exists():raise RuntimeError('Repair already has a receipt; reconcile rather than overwrite it')
    inventory=json.loads((ROOT/'rest_inventory.json').read_text())
    metadata=next(p for p in inventory['pull_requests'] if p['number']==args.pr)
    evidence=json.loads((ROOT/f'eligibility/pr{args.pr:04d}.json').read_text())
    if evidence['inventory_head_sha']!=metadata['headRefOid'] or not any(
            r['problem_id']==args.problem_id and args.alias in [part.strip() for part in r['problem_alias'].split('/')]
            for r in evidence['added_queue_rows']):
        raise RuntimeError('Catalogue ID/source alias not bound to pinned PR QUEUE evidence; manual reconciliation required')
    live=json.loads(subprocess.run(['gh','api','--hostname','github.com',f'repos/AlecKriebel/Math/pulls/{args.pr}'],capture_output=True,text=True,check=True).stdout)
    if live['head']['sha']!=metadata['headRefOid'] or args.doi not in (live['body'] or ''):
        raise RuntimeError('Live PR/head/publication binding changed')
    leads=json.loads((ROOT/f'PR{args.pr:04d}_PUBLICATION_LEADS.json').read_text())
    verified=next(r for r in leads['records'] if r['doi']==args.doi)
    if not verified['published'] or verified['doi_resolution']['status']!=200 or not verified['files'] or not all(f.get('download_verified') for f in verified['files']):
        raise RuntimeError('Published payload has not been fully verified')
    public=json.loads(get('https://zenodo.org/api/records/'+str(record))[0])
    if public.get('doi')!=args.doi or public.get('state')!='done' or public.get('submitted') is not True:
        raise RuntimeError('Live publication no longer matches verified record')
    if {(f['key'],f['size'],f['checksum']) for f in public['files']}!={(f['name'],f['size'],f['checksum']) for f in verified['files']}:
        raise RuntimeError('Live publication file set changed')
    get('https://doi.org/'+args.doi)
    before=read_ledger()
    rows=before.get('values',[])
    target=rows[args.row-1]
    if [i for i,r in enumerate(rows,1) if len(r)>2 and args.doi in zenodo_dois(r[2])]!=[args.row] or zenodo_dois(target[2])!={args.doi}:
        raise RuntimeError('DOI is absent, moved or duplicated in live ledger')
    if len(target)!=4 or not target[0].rstrip('/').endswith('/'+args.alias):
        raise RuntimeError('Original source alias or schema differs from reviewed target')
    old=target[3]
    formula=read_ledger('FORMULA').get('values',[])[args.row-1][3]
    if old!=formula:raise RuntimeError('Notes contain a formula; manual preservation required')
    pr_url=f'https://github.com/AlecKriebel/Math/pull/{args.pr}'
    suffix=''
    if not re.search(r'(?<!\d)'+re.escape(args.problem_id)+r'(?!\d)',old):
        suffix+=' Original problem '+args.problem_id+' / '+args.alias+'.'
    if not re.search(re.escape(pr_url)+r'(?!\d)',old):suffix+=' Reviewed PR: '+pr_url+'.'
    new=old+suffix
    prior_path=ROOT/f'PR{args.pr:04d}_LEDGER_REPAIR_PROPOSAL.json'
    prior=json.loads(prior_path.read_text()) if prior_path.exists() else None
    recovered=False
    if prior:
        if any(prior.get(k)!=v for k,v in {'pr':args.pr,'doi':args.doi,'row':args.row}.items()):
            raise RuntimeError('A different repair proposal exists; manual reconciliation required')
        if old==prior['new_notes'] and prior['new_notes']!=prior['old_notes']:
            original=prior.get('original_row')
            if original is None:
                saved=json.loads((ROOT/'raw'/f'pr{args.pr:04d}'/'ledger_repair_before.json').read_text())
                original=saved['values'][args.row-1]
            if target[:3]!=original[:3] or original[3]!=prior['old_notes']:
                raise RuntimeError('Post-mutation recovery identity differs; manual reconciliation required')
            recovered=True
            new=prior['new_notes']
            suffix=''
        elif old!=prior['old_notes']:
            raise RuntimeError('Notes changed since prepared proposal; preserve and manually reconcile')
    proposal={'pr':args.pr,'at':dt.datetime.now(dt.timezone.utc).isoformat(),
              'main':live_main(),'live_pr_head':live['head']['sha'],
              'live_pr_state':live['state'],'merged':live['merged'],
              'record':record,'doi':args.doi,'row':args.row,'old_notes':old,
              'new_notes':new,'original_row':target[:3]+[old],
              'reason':args.reason,'new_publication':False,'new_row':False}
    execution_observation=proposal
    if prior:
        original=prior.get('original_row')
        if original is None:
            saved=json.loads((ROOT/'raw'/f'pr{args.pr:04d}'/'ledger_repair_before.json').read_text())
            original=saved['values'][args.row-1]
        if not recovered and (target[:3]!=original[:3] or new!=prior['new_notes']):
            raise RuntimeError('Prepared proposal identity/append differs; manual reconciliation required')
        proposal=prior
    raw=ROOT/'raw'/f'pr{args.pr:04d}'
    if raw.is_symlink() or not raw.resolve().is_relative_to(ROOT.resolve()):raise RuntimeError('Unsafe raw path')
    raw.mkdir(exist_ok=True)
    if not prior:
        if (raw/'ledger_repair_before.json').exists():
            raise RuntimeError('An orphan before-snapshot exists; reconcile rather than overwrite it')
        atomic_json(raw/'ledger_repair_before.json',before)
        atomic_json(prior_path,proposal)
    if not args.execute:
        print(json.dumps(proposal,indent=2));return
    # Preserve original preparation artifacts even when nothing was applied yet.
    # Every execution/recovery gets its own immutable fresh observation.
    atomic_json(raw/('ledger_repair_execution_'+uuid.uuid4().hex+'.json'),
                {'context':execution_observation,'before':before,'recovered':recovered})
    response=None
    persistence_errors=[]
    def preserve(path,value):
        try:atomic_json(path,value)
        except OSError as error:persistence_errors.append(str(error))
    def request_for(find,replacement):
        return {'requests':[{'findReplace':{'range':{'sheetId':1254632077,
            'startRowIndex':args.row-1,'endRowIndex':args.row,
            'startColumnIndex':3,'endColumnIndex':4},'find':find,'replacement':replacement,
            'matchCase':True,'matchEntireCell':True,'searchByRegex':False,'includeFormulas':False}}]}
    if suffix:
        request=request_for(old,new)
        atomic_json(raw/'ledger_repair_request.json',request)
        # Recheck the entire target identity/uniqueness immediately before CAS.
        latest=read_ledger().get('values',[])
        if latest[args.row-1]!=target or [i for i,r in enumerate(latest,1) if len(r)>2 and args.doi in zenodo_dois(r[2])]!=[args.row]:
            raise RuntimeError('Concurrent identity/notes/DOI change; no write attempted')
        response=gws(['batchUpdate'],{'spreadsheetId':SHEET},request)
        preserve(raw/'ledger_repair_response.json',response)
    elif recovered and (raw/'ledger_repair_response.json').exists():
        response=json.loads((raw/'ledger_repair_response.json').read_text())
    after=read_ledger()
    preserve(raw/('ledger_repair_recovery_after.json' if recovered else 'ledger_repair_after.json'),after)
    final=after.get('values',[])
    if final[args.row-1]!=target[:3]+[new] or [i for i,r in enumerate(final,1) if len(r)>2 and args.doi in zenodo_dois(r[2])]!=[args.row]:
        # Sheets cannot condition one Notes replacement on other cells. If an
        # identity swap raced the CAS, undo only our exact appended value. A
        # concurrently edited Notes cell never matches this rollback predicate.
        occurrences=(response or {}).get('replies',[{}])[0].get('findReplace',{}).get('occurrencesChanged',0)
        rollback=None
        if suffix and occurrences==1 and len(final)>args.row-1 and len(final[args.row-1])>3 and final[args.row-1][3]==new:
            rollback=gws(['batchUpdate'],{'spreadsheetId':SHEET},request_for(new,old))
            rollback_after=read_ledger()
            preserve(raw/'ledger_repair_conflict_recovery.json',{'after':after,'rollback_response':rollback,'rollback_after':rollback_after})
        raise RuntimeError('Final target row/unique DOI does not match; manual reconciliation required')
    changes=[]
    for i in range(max(len(rows),len(final))):
        a=rows[i] if i<len(rows) else []
        b=final[i] if i<len(final) else []
        if a!=b:changes.append({'row':i+1,'columns':[j+1 for j in range(max(len(a),len(b))) if (a[j] if j<len(a) else '')!=(b[j] if j<len(b) else '')]})
    occurrences=(response or {}).get('replies',[{}])[0].get('findReplace',{}).get('occurrencesChanged',0)
    if occurrences not in {0,1}:raise RuntimeError('Unexpected replacement count')
    receipt={**proposal,'status':'verified','updated':bool(occurrences),
             'recovered_prior_intended_value':recovered,
             'mutation_attribution':'confirmed by saved response' if response else 'no mutation attributed; intended value independently verified',
             'at_completed':dt.datetime.now(dt.timezone.utc).isoformat(),
             'find_replace_response':response,'final_row':final[args.row-1],
             'unique_primary_doi_count':1,'observed_changes':changes,
             'rows_before':len(rows),'rows_after':len(final),
             'persistence_errors':persistence_errors,
             'concurrency_mechanism':'Full identity/DOI recheck, single-cell exact-value CAS, full readback, and conditional removal of only our append on a detected identity race.'}
    print(json.dumps(receipt,indent=2),flush=True)
    atomic_json(receipt_path,receipt)


if __name__=='__main__':main()
