#!/usr/bin/env python3
"""Reconcile/append one tracker row only after a verified publication receipt."""
from pathlib import Path
import json,subprocess,datetime
ROOT=Path(__file__).resolve().parents[1]
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TABID=1254632077
pub=json.loads((ROOT/'receipts/zenodo_published_inspect.json').read_text())
assert pub.get('state')=='published' and pub.get('doi') and pub.get('id'),'publication unverified'
meta=json.loads((ROOT/'zenodo-deposit.json').read_text())['metadata'];doi=pub['doi'];did=str(pub['id']);title=meta['title']
def gws(method,params,body=None):
 cmd=['gws','sheets','spreadsheets',*method.split('.'),'--params',json.dumps(params)]
 if body is not None:cmd+=['--json',json.dumps(body)]
 r=subprocess.run(cmd,text=True,capture_output=True)
 if r.returncode:raise RuntimeError(r.stderr+'\n'+r.stdout)
 return json.loads(r.stdout)
metadata=gws('get',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties)'})
found=[x['properties'] for x in metadata['sheets'] if x['properties']['sheetId']==TABID]
assert len(found)==1;tab=found[0];name=tab['title'];quoted="'"+name.replace("'","''")+"'"
read=gws('values.get',{'spreadsheetId':SID,'range':quoted+'!A1:AQ'+str(tab['gridProperties']['rowCount']),'valueRenderOption':'FORMULA'})
rows=read.get('values',[]);headers=rows[0];assert headers==['Original Problem','Solution Chat URL','DOI','Notes'],headers
matches=[]
for i,row in enumerate(rows[1:],2):
 text='\n'.join(str(x) for x in row)
 if doi in text or title in text or ('zenodo.org/records/'+did) in text:matches.append({'row':i,'values':row})
notes=(title+' — Alec Kriebel, v1.0.0 ('+meta['publication_date']+'). '+
 'Exact ordered-pair C_(s,2)=zeta_Lambda(s) for every real s>2; covolume-one triangular lattice. '+
 'Smooth compact embedded surfaces, including smooth boundary; ambient Euclidean distance; coefficient zeta_Lambda(s) A^(-s/2), sphere zeta_Lambda(s)/(4*pi)^(s/2). '+
 'Consequence of OpenAI universal energy plus established HSS/HLSS finite reductions and corrected Hardin–Saff theorem; no independent base breakthrough or firstness claim. '+
 'Two fresh whole-package AI adversarial reviews; extensive AI use; unrefereed, no conventional human peer review; full Lean build unverified. '+pub['record_url'])
values=['https://www.math.vanderbilt.edu/saffeb/texts/235.pdf — Conjecture 2, d=2, s>2 (KS1998 Conjecture 1)', '',pub['doi_url'],notes]
receipt={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'spreadsheet_id':SID,'sheet_id':TABID,'tab_title':name,'headers':headers,'publication_doi':doi,'deposit_id':pub['id']}
if matches:
 assert len(matches)==1 and matches[0]['values']==values,{'duplicate_or_conflicting_matches':matches}
 row=matches[0]['row'];receipt['operation']='already_present_reconciled';rng=quoted+f'!A{row}:D{row}'
else:
 # Persist exact intended append before mutation; on ambiguity rerun begins with a duplicate search.
 request={'params':{'spreadsheetId':SID,'range':quoted+'!A1:D'+str(tab['gridProperties']['rowCount']),'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},'body':{'majorDimension':'ROWS','values':[values]}}
 (ROOT/'receipts/tracker_append_intent.json').write_text(json.dumps(request,indent=2)+'\n')
 result=gws('values.append',request['params'],request['body']);(ROOT/'receipts/tracker_append_result.json').write_text(json.dumps(result,indent=2)+'\n')
 rng=result['updates']['updatedRange'];receipt['operation']='appended';receipt['append_result']=result
back=gws('values.get',{'spreadsheetId':SID,'range':rng,'valueRenderOption':'FORMULA'})
assert back.get('values')==[values],back
receipt.update({'verified_range':rng,'verified_values':back['values'],'status':'verified'})
(ROOT/'receipts/tracker_verified.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'verified','range':rng,'doi':doi,'operation':receipt['operation']}))
