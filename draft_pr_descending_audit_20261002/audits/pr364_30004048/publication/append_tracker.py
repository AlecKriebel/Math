"""Append exactly one fully published, verified preprint row through gws.

All requests are structured subprocess arguments; no credentials are inspected.
A failed or ambiguous append stops without an automatic second write.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
D=Path(__file__).resolve().parent;A=D.parent
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def execute(args,label,private=False):
    directory=D/'private_tracker' if private else D
    started=datetime.now(timezone.utc).isoformat()
    r=subprocess.run(args,capture_output=True)
    (directory/(label+'.stdout')).write_bytes(r.stdout)
    (directory/(label+'.stderr')).write_bytes(r.stderr)
    receipt={'argv':args,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'automatic_retry':False}
    (directory/(label+'_execution.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    assert r.returncode==0,(label,r.returncode,r.stderr.decode(errors='replace'))
    return json.loads(r.stdout)
def gws(method,params,label,body=None,private=False,dry=False):
    args=['gws','sheets','spreadsheets','values',method,'--params',json.dumps(params)]
    if body is not None:args+=['--json',json.dumps(body)]
    if dry:args+=['--dry-run']
    return execute(args,label,private)
assert not (D/'TRACKER_COMPLETE.json').exists() and not (D/'tracker_append_response.stdout').exists(),'Existing or uncertain append: inspect saved response and sheet before any further write'
(D/'private_tracker').mkdir(exist_ok=True)
clearance=load(A/'PUBLISHING_CLEARANCE.json')
assert clearance['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert clearance['second_review_mandatory_findings']==0
for r in clearance['sealed_submission_files']:
    b=(A/'preprint'/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json')
assert merged['status']=='claimed_solved' and merged['all_target_file_hashes_exact']==41
published=load(D/'inspect_published_receipt.json')
assert published['state']=='published' and published['environment']=='production'
assert published['doi'] and published['doi_url']=='https://doi.org/'+published['doi']
assert published['record_url']=='https://zenodo.org/records/'+str(published['id'])
public=load(D/'PUBLIC_RECORD_VERIFICATION.json')
assert public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES' and public['doi']==published['doi']
assert len(public['all_file_bytes'])==2 and all(r['entire_public_download_equals_reviewed_local_file'] for r in public['all_file_bytes'])
metadata=load(A/'preprint/zenodo-deposit.json')['metadata']
assert published['title']==metadata['title']
assert len(published['files'])==2
for r in published['files']:
    b=(A/'preprint'/r['name']).read_bytes();assert len(b)==r['size'] and sha(b)==r['sha256']
sheet_meta=execute(['gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':ID,'fields':'sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'})],'before_append_sheet_metadata',private=True)
target=[s['properties'] for s in sheet_meta['sheets'] if s['properties']['sheetId']==1254632077]
assert len(target)==1 and target[0]['title']=='Math Puzzles' and target[0]['gridProperties']['columnCount']==43
read_params={'spreadsheetId':ID,'range':'Math Puzzles!A1:AQ'+str(target[0]['gridProperties']['rowCount']),'valueRenderOption':'FORMULA'}
before=gws('get',read_params,'before_append',private=True)
assert before['values'][0]==['Original Problem','Solution Chat URL','DOI','Notes']
matches=[r for r in before['values'][1:] if published['doi'] in str(r) or '30004048' in str(r) or 'OWR-16763-022' in str(r) or metadata['title'] in str(r)]
assert not matches,'Existing problem/DOI row: stop without a duplicate append'
problem='OWR-16763-022 (30004048): Biconstrained two-step reachability symmetry'
notes=(metadata['title']+' — Alec Kriebel (ORCID 0009-0001-9320-500X), v'+metadata['version']
       +'. Preprint date: '+metadata['publication_date']+'. Negative universal symmetry answer: absolute gap at (13/27,14/27) and its swap is at least 1/108. Exact rational-boundary formula via minimum incidence degree. '
       +'The existing seven-type matrix and weighted framework of Chudnovsky, Hompe, Scott, Seymour and Spirkl are credited; true degree minima, exact psi values and ordering are unevaluated. '
       +'Dated bounded priority audit found no earlier equivalent theorem; inaccessible 2019 Princeton thesis and incomplete indexing remain coverage gaps, no global novelty certification. '
       +'Four-page unrefereed preprint; extensive AI use and no external human peer review. Two sequential fresh adversarial review rounds completed with all mandatory findings resolved. '
       +'PDF plus portable source/verification ZIP includes all 41 original files, exact matrix/ordinary-graph/gap checks and independent support/LP controls. '
       +'Primary question: https://ems.press/content/serial-article-files/46780, Seymour printed 46–47/PDF 42–43. '
       +'Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/364.')
row=[problem,'',published['doi_url'],notes]
params={'spreadsheetId':ID,'range':'Math Puzzles!A:D','valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
body={'majorDimension':'ROWS','values':[row]}
request={'utc':datetime.now(timezone.utc).isoformat(),'params':params,'body':body,'gid':1254632077,'prior_headers_verified':True,'duplicate_problem_or_doi_found':False,'user_authorization':'Explicit persistent-goal instruction to append after confirmed Zenodo publication'}
(D/'tracker_row_request.json').write_text(json.dumps(request,indent=2)+'\n')
gws('append',params,'tracker_dry_run',body=body,dry=True,private=True)
response=gws('append',params,'tracker_append_response',body=body)
assert response['spreadsheetId']==ID
updates=response['updates'];assert updates['updatedRows']==1 and updates['updatedColumns']==4 and updates['updatedCells']==4
actual_range=updates['updatedRange']
assert actual_range.startswith("'Math Puzzles'!") or actual_range.startswith('Math Puzzles!')
after=gws('get',{'spreadsheetId':ID,'range':actual_range,'valueRenderOption':'FORMULA'},'tracker_readback')
assert after['values']==[row]
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK','gid':1254632077,'spreadsheetId':ID,'updatedRange':actual_range,'doi':published['doi'],'record_url':published['record_url'],'row':row,'solution_chat_cell_blank':True,'no_conversation_shared_or_person_contacted':True}
(D/'TRACKER_COMPLETE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='row'},indent=2))
