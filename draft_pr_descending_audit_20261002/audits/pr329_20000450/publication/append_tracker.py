"""Append exactly one published preprint row with gws; preserve uncertain attempts."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,subprocess
D=Path(__file__).resolve().parent;A=D.parent
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance,load,sha,utc,O
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
assert not (D/'TRACKER_COMPLETE.json').exists()
assert not (D/'tracker_append_preexecution.json').exists(),'Inspect any prior uncertain append before retry; never append blindly twice.'
current_clearance()
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json');post=load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert merged['status']=='PASS_PR329_EXACT_MERGE'
assert post['status']=='PASS_PR329_POST_MERGE_EXACT_SUBMISSION' and post['actual_merge']==merged['actual_merge']
published=load(D/'inspect_published_receipt.json');public=load(D/'PUBLIC_RECORD_VERIFICATION.json')
assert published['state']=='published' and published['environment']=='production'
assert published['doi'] and published['doi_url']=='https://doi.org/'+published['doi']
assert published['record_url']=='https://zenodo.org/records/'+str(published['id'])
assert public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES' and public['doi']==published['doi']
assert len(public['all_file_bytes'])==2 and all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes'])
meta=load(O/'zenodo-deposit.json')['metadata'];assert published['title']==meta['title']
for x in published['files']:
    b=(O/x['name']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256']
private=D/('private_tracker_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
private.mkdir(exist_ok=False)
def execute(argv,label,is_private=False):
    directory=private if is_private else D
    prep=directory/(label+'_preexecution.json');assert not prep.exists()
    start=utc();prep.write_text(json.dumps(dict(utc=start,argv=argv,automatic_retry=False),indent=2)+'\n')
    run=subprocess.run(argv,capture_output=True)
    for k,b in [('stdout',run.stdout),('stderr',run.stderr)]: (directory/(label+'.'+k)).write_bytes(b)
    rec=dict(argv=argv,started_utc=start,ended_utc=utc(),exit_code=run.returncode,
        stdout_bytes=len(run.stdout),stdout_sha256=sha(run.stdout),stderr_bytes=len(run.stderr),stderr_sha256=sha(run.stderr),automatic_retry=False)
    (directory/(label+'_execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert run.returncode==0,(label,run.stderr.decode(errors='replace'))
    return json.loads(run.stdout)
def values(method,params,label,body=None,is_private=False,dry=False):
    argv=['gws','sheets','spreadsheets','values',method,'--params',json.dumps(params)]
    if body is not None:argv+=['--json',json.dumps(body)]
    if dry:argv+=['--dry-run']
    return execute(argv,label,is_private)
sheet=execute(['gws','sheets','spreadsheets','get','--params',json.dumps(dict(spreadsheetId=ID,fields='sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'))],'sheet_metadata',True)
target=[x['properties'] for x in sheet['sheets'] if x['properties']['sheetId']==GID]
assert len(target)==1 and target[0]['title']=='Math Puzzles'
before=values('get',dict(spreadsheetId=ID,range="'Math Puzzles'!A1:D"+str(target[0]['gridProperties']['rowCount']),valueRenderOption='FORMULA'),'existing_rows',is_private=True)
assert before['values'][0]==['Original Problem','Solution Chat URL','DOI','Notes']
assert not [r for r in before['values'][1:] if published['doi'] in str(r) or '20000450' in str(r) or meta['title'] in str(r)],'An existing problem/title/DOI row requires reconciliation; no duplicate append.'
problem='AIM McCallum Question 17 (20000450): Compute the 5-torsion of the regular-pentagon quintic pencil'
notes=(meta['title']+' — Alec Kriebel, ORCID 0009-0001-9320-500X; v'+meta['version']+'; preprint '+meta['publication_date']
    +'. Complete 25-point geometric fifth-torsion and full division field for the explicitly normalized regular-pentagon pencil over Q(sqrt(5)), with origin [0:1:0]. Exact elliptic range, both birational maps, residual degree-ten polynomial, all nonsingular specialization cases, splitting criterion and Galois action, including the allowed cuspidal plane member through normalization. '
    +'Source infinity subgroup and classical Fisher/Verdure/Morton results explicitly credited; bounded priority audit, no first-discovery or worldwide continuing-openness certificate. Nonregular/star-pentagon variants and Tate-Shafarevich/local-solubility constructions outside the theorem. '
    +'Seven-page unrefereed research note; extensive AI use, no independent external human peer review. Successive new full-preprint adversarial reviews; first source-attribution defect repaired globally, final full review independently reproduced with no unresolved findings. PDF plus 50-payload verification package and manifest; exact symbolic, arithmetic, direct finite group-law and deliberate false-claim/integrity controls. '
    +'Original author progress 1/5 preserved. Primary question: https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf#page=51. Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/329.')
row=[problem,'',published['doi_url'],notes]
params=dict(spreadsheetId=ID,range="'Math Puzzles'!A:D",valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True)
body=dict(majorDimension='ROWS',values=[row])
(D/'tracker_row_request.json').write_text(json.dumps(dict(utc=utc(),gid=GID,params=params,body=body,headers_verified=True,duplicate_found=False,
    user_authorization='Explicit persistent-goal instruction to append the confirmed published paper and DOI.'),indent=2)+'\n')
values('append',params,'tracker_dry_run',body,is_private=True,dry=True)
current_clearance()
response=values('append',params,'tracker_append',body)
assert response['spreadsheetId']==ID
u=response['updates'];assert u['updatedRows']==1 and u['updatedColumns']==4 and u['updatedCells']==4
actual=u['updatedRange'];assert actual.startswith("'Math Puzzles'!") or actual.startswith('Math Puzzles!')
readback=values('get',dict(spreadsheetId=ID,range=actual,valueRenderOption='FORMULA'),'tracker_readback')
assert readback['values']==[row]
receipt=dict(utc=utc(),status='PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK',spreadsheetId=ID,gid=GID,updatedRange=actual,
    doi=published['doi'],record_url=published['record_url'],row=row,solution_chat_cell_blank=True,
    no_chat_shared_or_outside_person_contacted=True,prior_rows_read_privately=True,automatic_append_retry=False)
(D/'TRACKER_COMPLETE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='row'},indent=2))
