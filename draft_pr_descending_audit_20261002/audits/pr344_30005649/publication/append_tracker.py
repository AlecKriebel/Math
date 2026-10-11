"""Append one verified published preprint via gws; never retry an uncertain write."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
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
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance
clearance=current_clearance()
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json')
assert merged['status']=='claimed_solved' and merged['all_target_file_hashes_exact']==20 and merged['all_expected_paths_exact']==21
post=load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert post['status']=='PASS_COMPLETE_PR344_POST_MERGE' and post['actual_merge']==merged['actual_merge']
assert post['all_21_source_bindings_exact'] and post['all_15_original_math_files_unchanged'] and post['closed_namespaces_unchanged']
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
assert not [r for r in before['values'][1:] if published['doi'] in str(r) or '30005649' in str(r) or 'OWR-14297740-021' in str(r) or metadata['title'] in str(r)],'Existing problem/DOI row: stop without duplicate append'
problem='OWR-14297740-021 (30005649): Self-duality of quasi-supersingular group schemes'
notes=(metadata['title']+' — Alec Kriebel (ORCID0009-0001-9320-500X), v'+metadata['version']
 +'. Preprint date: '+metadata['publication_date']+'. Gives an explicit negative answer to Takao\'s higher-rank question after Proposition2, printed2479 of OWR42/2023. '
 +'For every prime p>3 and n>=3 over k=an algebraic closure of F_p, constructs a p-killed finite flat commutative W(k)-group of rank p^(2n), with quasi-supersingular special fiber, such that both the special fiber and its Witt-ring lift fail Cartier self-duality. '
 +'Quasi-supersingularity uses actual supersingular elliptic p-torsion factors over k. The proof gives an explicit six-dimensional Dieudonne module, elliptic filtration, image-intersection invariant and finite Honda complement; standard factors cover every n>=3. '
 +'No quasi-supersingular Witt-ring filtration or descent to every perfect field is asserted. Established cyclic-word, supersingular, Dieudonne and finite Honda theory is credited. '
 +'In-depth bounded primary-literature audit; source/access/version limitations retained. No first-discovery, first-application or worldwide continuing-openness certificate. '
 +'Four-page unrefereed research note; extensive AI use, no independent external human peer review. Three independent mathematical approach families and three successive NEW full preprint adversaries. '
 +'Historical review01 B1 and review02 F01/root B2 remain adverse as dated records; both supporting-software defects were repaired globally in the public derivative. The third NEW full review of the repaired v04 packet has zero unresolved mandatory findings. '
 +'PDF plus33-member verification ZIP,32 payloads. Python3.12 and3.14 full outputs compared byte for byte. Dense nonprime basis changes and opposite squared-Frobenius kernel twists verified; targeted negative controls rejected. Characteristic-two tests cover generic semilinear algebra only, not an extension of the p>3 theorem. '
 +'All15 original problem files preserved; original author progress remains1/5. '
 +'Primary question: https://ems.press/content/serial-article-files/47479?nt=1, printed2479/PDF103; report DOI10.4171/OWR/2023/42. '
 +'Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/344.')
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
