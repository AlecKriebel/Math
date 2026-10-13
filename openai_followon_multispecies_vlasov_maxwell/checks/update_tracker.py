#!/usr/bin/env python3
"""Append/reconcile one authorized DOI row only after verified production publication."""
import datetime,json,pathlib,re,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
SID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';TAB=1254632077
receipt=R/'receipts/zenodo_published_inspect.json'
pub=json.loads(receipt.read_text())
assert pub['environment']=='production' and pub['state']=='published'
doi=pub['doi'];assert re.fullmatch(r'10\.5281/zenodo\.\d+',doi)
assert pub['record_url']=='https://zenodo.org/records/'+str(pub['id'])
manifest=json.loads((R/'zenodo-deposit.json').read_text());title=manifest['metadata']['title']
assert pub['title']==title
# Every API operation uses the installed CLI and structured JSON, never shell interpolation.
def api(resource,method,params,body=None):
 args=['gws','sheets','spreadsheets',*resource,method,'--params',json.dumps(params)]
 if body is not None:args+=['--json',json.dumps(body,ensure_ascii=False)]
 r=subprocess.run(args,capture_output=True,text=True,timeout=45)
 if r.returncode:raise RuntimeError('Google Workspace operation failed: '+r.stderr[:1500])
 return json.loads(r.stdout)
meta=api([],'get',{'spreadsheetId':SID,'fields':'spreadsheetId,sheets(properties(sheetId,title,gridProperties))'})
matches=[s['properties'] for s in meta['sheets'] if s['properties']['sheetId']==TAB]
assert len(matches)==1
sheet=matches[0];name=sheet['title'];quoted="'"+name.replace("'","''")+"'"
def col(n):
 out=''
 while n:n,r=divmod(n-1,26);out=chr(65+r)+out
 return out
allrange=quoted+'!A:'+col(sheet['gridProperties']['columnCount'])
def readall():return api(['values'],'get',{'spreadsheetId':SID,'range':allrange,'valueRenderOption':'FORMATTED_VALUE'})['values']
rows=readall();headers=rows[0];assert headers.count('DOI')==1
assert all(h in headers for h in ['Original Problem','Solution Chat URL','Notes'])
notes=(title+' — Alec Kriebel (ORCID 0009-0001-9320-500X). Preprint date: '+manifest['metadata']['publication_date']+
       '; production Zenodo publication confirmed '+pub['verified_utc'][:10]+' UTC. '+
       'Global classical existence and uniqueness for fixed finite positive-mass species and arbitrary real charges, '+
       'smooth compact phase distributions, compatible C_b∞∩L² fields; compact phase support on finite intervals and momentum continuation; no neutrality. '+
       'Signed coefficient transfer and simultaneous bootstrap extend OpenAI family 362; base theorem/universal identity inherited. '+
       'Two complete internal adversarial reviews; extensive AI assistance; unrefereed; no reproduced Lean certificate. '+pub['record_url'])
values={'Original Problem':'Global smooth 3D relativistic Vlasov–Maxwell for arbitrary fixed finite multispecies (positive masses, signed charges)',
        'Solution Chat URL':'','DOI':'https://doi.org/'+doi,'Notes':notes}
row=[values.get(h,'') for h in headers]
# Inspect DOI, ID/record URL and title before any write. Ambiguous appends are reconciled by rereading, never immediately repeated.
def find(rows):
 found=[]
 for i,rr in enumerate(rows[1:],2):
  text=' '.join(str(v) for v in rr)
  if re.search(r'(?<![A-Za-z0-9])'+re.escape(doi)+r'(?![A-Za-z0-9])',text) or re.search(re.escape(pub['record_url'])+r'(?![0-9])',text) or title in text:found.append((i,rr))
 return found
existing=find(rows);append_result=None;recovered=False
if existing:
 assert len(existing)==1,'Multiple existing matches; do not append.'
 number,actual=existing[0]
 assert len(actual)>headers.index('DOI') and doi in str(actual[headers.index('DOI')]),'Matching title without verified DOI; manual reconciliation required.'
 assert title in ' '.join(map(str,actual)) and 'Alec Kriebel' in ' '.join(map(str,actual))
 action='reconciled_existing_row'
else:
 try:
  append_result=api(['values'],'append',{'spreadsheetId':SID,'range':quoted+'!A:'+col(len(headers)),
       'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True},
       {'majorDimension':'ROWS','values':[row]})
  (R/'receipts/tracker_append_response.json').write_text(json.dumps(append_result,indent=2,ensure_ascii=False)+'\n')
 except (RuntimeError,subprocess.TimeoutExpired,json.JSONDecodeError) as exc:
  # The operation may have succeeded remotely. Save only a nonsecret error description.
  (R/'receipts/tracker_append_ambiguous.json').write_text(json.dumps({'error':str(exc),'next_action':'read same target tab; never republish paper'},indent=2)+'\n')
  recovered=True
 current=find(readall());assert len(current)==1,'Append not uniquely confirmed; reconcile tracker before any further write.'
 number,actual=current[0];assert actual==row,'Inserted row differs from intended RAW values.'
 action='recovered_after_ambiguous_append' if recovered else 'appended_one_row'
exactrange=quoted+'!A'+str(number)+':'+col(len(headers))+str(number)
readback=api(['values'],'get',{'spreadsheetId':SID,'range':exactrange,'valueRenderOption':'UNFORMATTED_VALUE'})
assert readback['values']==[actual]
final={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'spreadsheet_id':SID,'sheet_id':TAB,
 'sheet_title':name,'headers':headers,'action':action,'range':readback['range'],'values':readback['values'],
 'doi':doi,'deposit_id':pub['id'],'publication_confirmed_first':True,'raw_text_handling':True,
 'solution_chat_url_unknown_left_blank':True,'duplicate_count_after':1}
(R/'receipts/tracker_verified.json').write_text(json.dumps(final,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(final,ensure_ascii=False,indent=2))
