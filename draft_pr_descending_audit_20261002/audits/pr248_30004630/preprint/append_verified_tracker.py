"""Append the published PR248 DOI once through GWS, with durable reconciliation."""
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess
PRE=Path(__file__).resolve().parent
PUB=PRE.parent/'publication'
OUT=PUB/'tracker-private'
OUT.mkdir(parents=True,exist_ok=True)
GWS='/Users/alec/.nvm/versions/node/v22.16.0/bin/gws'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
utc=datetime.now(timezone.utc).isoformat()

def call(label,args):
    r=subprocess.run([GWS,*args],capture_output=True,text=True)
    (OUT/(label+'.stdout.json')).write_text(r.stdout)
    (OUT/(label+'.stderr.txt')).write_text(r.stderr)
    if r.returncode:raise RuntimeError(label+' failed; inspect saved output and reconcile before another write')
    return json.loads(r.stdout)

assert not (PUB/'TRACKER_VERIFIED_APPEND.json').exists(), 'Already verified; read-only inspection only'
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified']
doi=z['doi_url']
properties=call('01-properties',['sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':SHEET,'fields':'sheets.properties'})])
matches=[s['properties'] for s in properties['sheets'] if s['properties']['sheetId']==1254632077]
assert len(matches)==1 and matches[0]['title']=='Math Puzzles'
row=['https://www.unsolvedmath.com/problems/OWR-4990378-001','',doi,
     'Failure of strong quadratic growth in unregularized sparse control of a critical wave equation — Alec Kriebel, v1.0, 2026-10-14. '
     'Explicit negative answer to retaining ordinary-cone strict positivity and strong control-L2 growth unchanged at beta2=0 in the actual critical quintic-wave model. '
     'Unique global zero optimizer with a zero cone; Linfinity-null concentrating controls defeat L2-squared growth. '
     'For each fixed finite nonnegative velocity weight, every optimizer under positive radial target perturbations fails a Lipschitz L2 estimate. '
     'Local L1 growth and weaker fixed-basepoint upper bounds survive. Independent math/source reproduction, bounded priority and three sequential fresh full preprint reviews passed, '
     'including a full revised-payload review and separate editorial addendum. Classical wave, sparse threshold and concentration/NDC inputs credited; no worldwide-firstness certificate. '
     'AI tools used extensively; unrefereed, no external human peer review. Six-page paper and113-file portable verification archive.']
values=call('02-before-rows',['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D"})]).get('values',[])
assert values and values[0]==['Original Problem','Solution Chat URL','DOI','Notes']
existing=[(n,r) for n,r in enumerate(values,1) if any(z['doi'] in str(c) for c in r)]
attempt=OUT/'APPEND_ATTEMPT.json'
append_count=0
if existing:
    assert len(existing)==1 and existing[0][1]==row and attempt.exists(), 'DOI exists; inspect it before any write'
    target="'Math Puzzles'!A"+str(existing[0][0])+':D'+str(existing[0][0])
    reconciled=True
else:
    assert not attempt.exists(), 'Previous append outcome unresolved; reconcile saved attempt before any retry'
    payload={'majorDimension':'ROWS','values':[row]}
    attempt.write_text(json.dumps({'utc':utc,'spreadsheet_id':SHEET,'sheet_id':1254632077,'doi_url':doi,'values':payload,'status':'write about to be attempted; outcome not yet known'},indent=2)+'\n')
    response=call('03-append',['sheets','spreadsheets','values','append','--params',json.dumps({'spreadsheetId':SHEET,'range':"'Math Puzzles'!A:D",'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}),'--json',json.dumps(payload)])
    updates=response['updates']
    assert updates['updatedRows']==1 and updates['updatedCells']==4
    assert updates['updatedData']['values']==[row]
    target=updates['updatedRange'];append_count=1;reconciled=False
readback=call('04-exact-readback',['sheets','spreadsheets','values','get','--params',json.dumps({'spreadsheetId':SHEET,'range':target})])
assert readback['values']==[row]
receipt={'utc':datetime.now(timezone.utc).isoformat(),'verified':True,'spreadsheet_id':SHEET,'sheet_id':1254632077,
         'updated_range':target,'doi_url':doi,'values':row,'cli':'Google Workspace CLI',
         'append_count':append_count,'reconciled_existing_attempt':reconciled,'exact_all_four_cells_readback':True}
(PUB/'TRACKER_VERIFIED_APPEND.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(receipt,indent=2,ensure_ascii=False))
