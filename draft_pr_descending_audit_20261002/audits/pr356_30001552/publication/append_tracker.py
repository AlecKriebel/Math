"""Append one verified published preprint via gws; never retry an uncertain write."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
D=Path(__file__).resolve().parent;A=D.parent
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def execute(args,label,private=False):
 directory=D/'private_tracker' if private else D
 assert not (directory/(label+'.stdout')).exists()
 started=datetime.now(timezone.utc).isoformat();r=subprocess.run(args,capture_output=True)
 (directory/(label+'.stdout')).write_bytes(r.stdout);(directory/(label+'.stderr')).write_bytes(r.stderr)
 receipt={'argv':args,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':r.returncode,
  'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'automatic_retry':False}
 (directory/(label+'_execution.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 assert r.returncode==0,(label,r.returncode,r.stderr.decode(errors='replace'));return json.loads(r.stdout)
def gws(method,params,label,body=None,private=False,dry=False):
 args=['gws','sheets','spreadsheets','values',method,'--params',json.dumps(params)]
 if body is not None:args+=['--json',json.dumps(body)]
 if dry:args+=['--dry-run']
 return execute(args,label,private)
assert not (D/'TRACKER_COMPLETE.json').exists() and not (D/'tracker_append_response.stdout').exists(),'Existing or uncertain append: inspect saved response and sheet before another write'
(D/'private_tracker').mkdir(exist_ok=True)
clearance=load(A/'PUBLISHING_CLEARANCE.json')
assert clearance['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and clearance['second_review_mandatory_findings']==0
assert len(clearance['fresh_reviews'])==2 and len(clearance['sealed_submission_files'])==4
for r in clearance['sealed_submission_files']:
 b=(A/'preprint'/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
for n in (1,2):
 v=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
 assert v['mandatory_findings']==0 and v['closed_namespace_unchanged'] and v['whole_verifier_output_compared']
 assert sha((A/f'preprint_review_0{n}'/v['review_seal_path']).read_bytes())==v['review_seal_sha256']
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json')
assert merged['status']=='claimed_solved' and merged['all_target_file_hashes_exact']==21 and merged['all_expected_paths_exact']==22
post=load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert post['status']=='PASS_COMPLETE_PR356_POST_MERGE' and post['actual_merge']==merged['actual_merge']
assert post['all_22_source_bindings_exact'] and post['all_16_original_math_files_unchanged'] and post['closed_namespaces_unchanged']
published=load(D/'inspect_published_receipt.json')
assert published['state']=='published' and published['environment']=='production'
assert published['doi'] and published['doi_url']=='https://doi.org/'+published['doi']
assert published['record_url']=='https://zenodo.org/records/'+str(published['id'])
public=load(D/'PUBLIC_RECORD_VERIFICATION.json')
assert public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES' and public['doi']==published['doi']
assert len(public['all_file_bytes'])==2 and all(r['entire_public_download_equals_reviewed_local_file'] for r in public['all_file_bytes'])
metadata=load(A/'preprint/zenodo-deposit.json')['metadata']
assert published['title']==metadata['title'] and len(published['files'])==2
for r in published['files']:
 b=(A/'preprint'/r['name']).read_bytes();assert len(b)==r['size'] and sha(b)==r['sha256']
sheet_meta=execute(['gws','sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':ID,'fields':'sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'})],'before_append_sheet_metadata',private=True)
target=[s['properties'] for s in sheet_meta['sheets'] if s['properties']['sheetId']==1254632077]
assert len(target)==1 and target[0]['title']=='Math Puzzles' and target[0]['gridProperties']['columnCount']==43
before=gws('get',{'spreadsheetId':ID,'range':'Math Puzzles!A1:AQ'+str(target[0]['gridProperties']['rowCount']),'valueRenderOption':'FORMULA'},'before_append',private=True)
assert before['values'][0]==['Original Problem','Solution Chat URL','DOI','Notes']
assert not [r for r in before['values'][1:] if published['doi'] in str(r) or '30001552' in str(r) or 'OWR-4425-007' in str(r) or metadata['title'] in str(r)],'Existing problem/DOI row: stop without duplicate append'
problem='OWR-4425-007 (30001552): Alternating antimorphic Fine-Wilf bound'
notes=(metadata['title']+' — Alec Kriebel (ORCID0009-0001-9320-500X), v'+metadata['version']
 +'. Preprint date: '+metadata['publication_date']+'. Proves the exact unnumbered conjecture after Theorem23, printed2220 in the Nowotka/Bischoff contribution to OWR37/2010: '
 +'alternating theta-periods p,q at length at least p+q-gcd(p,q) force alternating gcd(p,q), for every involutive antimorphism, including fixed letters. '
 +'The canonical finite extension theta(w)w has ordinary periods2p,2q; classical Fine-Wilf and central reflection recover the alternating phase. '
 +'Prior Fine-Wilf theory, the originating conjecture, and Bischoff thesis reflection/doubled-period mechanisms are credited. '
 +'The reversal witness abb establishes a uniform one-letter-lower obstruction; no optimality for every period pair is claimed. The distinct morphic Conjecture27 is outside this result. '
 +'An in-depth bounded primary-literature audit found no earlier exact theorem in inspected sources; access/version gaps, incomplete indexing and unpublished work remain limitations. No global novelty or first-discovery certification. '
 +'Three-page unrefereed research note; extensive AI use and no independent external human peer review. Three independent mathematical approach families and two sequential new full preprint adversaries completed with zero unresolved mandatory findings. '
 +'PDF plus portable verification/source ZIP,69 members and68 payloads, preserves16 original problem files and includes signed-graph, word, definition and priority controls. Current public portable68408 checks; historical five-private-source68413 mode is not certified as reproduced. '
 +'Primary question: https://ems.press/content/serial-article-files/46296, printed2220/PDF26; 2010 workshop report published2March2011. '
 +'Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/356.')
row=[problem,'',published['doi_url'],notes]
params={'spreadsheetId':ID,'range':'Math Puzzles!A:D','valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
body={'majorDimension':'ROWS','values':[row]}
(D/'tracker_row_request.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'params':params,'body':body,'gid':1254632077,'prior_headers_verified':True,'duplicate_problem_or_doi_found':False,'user_authorization':'Explicit persistent-goal instruction to append after confirmed Zenodo publication'},indent=2)+'\n')
gws('append',params,'tracker_dry_run',body=body,dry=True,private=True)
response=gws('append',params,'tracker_append_response',body=body)
assert response['spreadsheetId']==ID
updates=response['updates'];assert updates['updatedRows']==1 and updates['updatedColumns']==4 and updates['updatedCells']==4
actual_range=updates['updatedRange'];assert actual_range.startswith("'Math Puzzles'!") or actual_range.startswith('Math Puzzles!')
after=gws('get',{'spreadsheetId':ID,'range':actual_range,'valueRenderOption':'FORMULA'},'tracker_readback');assert after['values']==[row]
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK','gid':1254632077,'spreadsheetId':ID,'updatedRange':actual_range,'doi':published['doi'],'record_url':published['record_url'],'row':row,'solution_chat_cell_blank':True,'no_conversation_shared_or_person_contacted':True}
(D/'TRACKER_COMPLETE.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='row'},indent=2))
