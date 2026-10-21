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
from publication_check import ROOT, SHEET, get
from checkpoint import live_main
from sweep_io import atomic_json


def gws(resource,params,body=None):
    command=['gws','sheets','spreadsheets']+resource+['--params',json.dumps(params)]
    if body is not None:command+=['--json',json.dumps(body)]
    return json.loads(subprocess.run(command,capture_output=True,text=True,check=True).stdout)


def read_ledger(render='FORMATTED_VALUE'):
    return gws(['values','get'],{'spreadsheetId':SHEET,
        'range':"'Math Puzzles'!A1:AQ1169",'valueRenderOption':render})


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
    normalized=lambda s:str(s).strip().removeprefix('https://doi.org/')
    if [i for i,r in enumerate(rows,1) if len(r)>2 and normalized(r[2])==args.doi]!=[args.row]:
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
    proposal={'pr':args.pr,'at':dt.datetime.now(dt.timezone.utc).isoformat(),
              'main':live_main(),'live_pr_head':live['head']['sha'],
              'live_pr_state':live['state'],'merged':live['merged'],
              'record':record,'doi':args.doi,'row':args.row,'old_notes':old,
              'new_notes':new,'reason':args.reason,'new_publication':False,'new_row':False}
    raw=ROOT/'raw'/f'pr{args.pr:04d}'
    if raw.is_symlink() or not raw.resolve().is_relative_to(ROOT.resolve()):raise RuntimeError('Unsafe raw path')
    raw.mkdir(exist_ok=True)
    atomic_json(raw/'ledger_repair_before.json',before)
    atomic_json(ROOT/f'PR{args.pr:04d}_LEDGER_REPAIR_PROPOSAL.json',proposal)
    if not args.execute:
        print(json.dumps(proposal,indent=2));return
    response=None
    if suffix:
        request={'requests':[{'findReplace':{'range':{'sheetId':1254632077,
            'startRowIndex':args.row-1,'endRowIndex':args.row,
            'startColumnIndex':3,'endColumnIndex':4},'find':old,'replacement':new,
            'matchCase':True,'matchEntireCell':True,'searchByRegex':False,'includeFormulas':False}}]}
        atomic_json(raw/'ledger_repair_request.json',request)
        response=gws(['batchUpdate'],{'spreadsheetId':SHEET},request)
        atomic_json(raw/'ledger_repair_response.json',response)
    after=read_ledger()
    atomic_json(raw/'ledger_repair_after.json',after)
    final=after.get('values',[])
    if final[args.row-1]!=target[:3]+[new] or [i for i,r in enumerate(final,1) if len(r)>2 and normalized(r[2])==args.doi]!=[args.row]:
        raise RuntimeError('Final target row/unique DOI does not match; manual reconciliation required')
    changes=[]
    for i in range(max(len(rows),len(final))):
        a=rows[i] if i<len(rows) else []
        b=final[i] if i<len(final) else []
        if a!=b:changes.append({'row':i+1,'columns':[j+1 for j in range(max(len(a),len(b))) if (a[j] if j<len(a) else '')!=(b[j] if j<len(b) else '')]})
    occurrences=(response or {}).get('replies',[{}])[0].get('findReplace',{}).get('occurrencesChanged',0)
    if occurrences not in {0,1}:raise RuntimeError('Unexpected replacement count')
    receipt={**proposal,'status':'verified','updated':bool(occurrences),
             'at_completed':dt.datetime.now(dt.timezone.utc).isoformat(),
             'find_replace_response':response,'final_row':final[args.row-1],
             'unique_primary_doi_count':1,'observed_changes':changes,
             'rows_before':len(rows),'rows_after':len(final),
             'concurrency_mechanism':'Single-cell matchEntireCell exact-value conditional findReplace, then full-sheet/row/DOI readback.'}
    atomic_json(receipt_path,receipt)
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
