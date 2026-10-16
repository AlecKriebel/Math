"""Append exactly one confirmed preprint row with gws, retaining uncertain attempts."""
from pathlib import Path
from datetime import datetime, timezone
import json, sys, subprocess

from public_identity import identity, resolution_binding

D = Path(__file__).resolve().parent
A = D.parent
sys.path.insert(0,str(A))
from root_submission_gate import current_clearance, load, sha, utc, O, window, pin, operational_clearance, acquire_shared_write_window

ID = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
assert not (D/'TRACKER_COMPLETE.json').exists()
assert not (D/'tracker_append_preexecution.json').exists(), 'Inspect any earlier uncertain append before retry; never append blindly twice.'
current_clearance()
operational_clearance()
write_window = acquire_shared_write_window()
merged = load(A/'ACTUAL_MERGE_VERIFICATION.json')
post = load(A/'ROOT_POST_MERGE_VERIFICATION.json')
assert merged['status'] == 'PASS_PR311_EXACT_MERGE'
assert post['status'] == 'PASS_PR311_POST_MERGE_EXACT_SUBMISSION' and post['actual_merge'] == merged['actual_merge']
published = load(D/'inspect_published_receipt.json')
public = load(D/'PUBLIC_RECORD_VERIFICATION.json')
identity(published)
resolution_binding(public['doi_resolution'], published['id'])
assert public['record_id'] == published['id'] and public['exact_record_identity_bound']
assert published['state'] == 'published' and published['environment'] == 'production'
assert published['doi'] and published['doi_url'] == 'https://doi.org/'+published['doi']
assert published['record_url'] == 'https://zenodo.org/records/'+str(published['id'])
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES' and public['doi'] == published['doi']
assert len(public['all_file_bytes']) == 2 and all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes'])
meta = load(O/'zenodo-deposit.json')['metadata']
assert published['title'] == meta['title']
for x in published['files']:
    b = (O/x['name']).read_bytes()
    assert len(b) == x['size'] and sha(b) == x['sha256']
private = D/('private_tracker_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
private.mkdir(exist_ok=False)
cli = '/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
assert pin(Path(cli))['sha256'] == '0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
cli_pin = pin(Path(cli))

def execute(argv,label,is_private=False):
    directory = private if is_private else D
    prep = directory/(label+'_preexecution.json')
    assert not prep.exists()
    start = utc()
    prep.write_text(json.dumps({'utc':start,'argv':argv,'automatic_retry':False,
        'orchestrator':pin(Path(__file__))},indent=2)+'\n')
    timed_out = False
    try:
        run = subprocess.run(argv,cwd=D,capture_output=True,timeout=55)
        out,err,code = run.stdout,run.stderr,run.returncode
    except subprocess.TimeoutExpired as e:
        timed_out = True
        out,err,code = e.stdout or b'',e.stderr or b'',124
    for k,b in [('stdout',out),('stderr',err)]:
        (directory/(label+'.'+k)).write_bytes(b)
    rec = {'argv':argv,'cwd':str(D),'started_utc':start,'ended_utc':utc(),'exit_code':code,
        'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),
        'automatic_retry':False,'timed_out':timed_out}
    (directory/(label+'_execution.json')).write_text(json.dumps(rec,indent=2)+'\n')
    assert code == 0, (label,err.decode(errors='replace'),'Inspect any uncertain write through a fresh read; no retry was made.')
    return json.loads(out)

def values(method,params,label,body=None,is_private=False,dry=False):
    argv = [cli,'sheets','spreadsheets','values',method,'--params',json.dumps(params)]
    if body is not None:
        argv += ['--json',json.dumps(body)]
    if dry:
        argv += ['--dry-run']
    return execute(argv,label,is_private)

sheet = execute([cli,'sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':ID,
    'fields':'spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'})],'sheet_metadata',True)
assert sheet['spreadsheetId'] == ID
target = [x['properties'] for x in sheet['sheets'] if x['properties']['sheetId'] == GID]
assert len(target) == 1 and target[0]['title'] == 'Math Puzzles' and target[0]['gridProperties']['columnCount'] >= 4
column_count=target[0]['gridProperties']['columnCount']
last_column='';v=column_count
while v:
    v,rem=divmod(v-1,26);last_column=chr(65+rem)+last_column
whole_range="'Math Puzzles'!A1:"+last_column
before = values('get',{'spreadsheetId':ID,'range':whole_range+str(target[0]['gridProperties']['rowCount']),
    'valueRenderOption':'FORMULA'},'existing_rows',is_private=True)
assert before['values'][0][:4] == ['Original Problem','Solution Chat URL','DOI','Notes']
assert not [r for r in before['values'][1:] if published['doi'] in str(r) or '30005303' in str(r)
    or meta['title'].lower() in str(r).lower()], 'Existing target/title/DOI row requires reconciliation; no duplicate append.'
problem = 'OWR-11695865-001 (30005303): Total Positivity and Graphical Model Factorization'
notes = (meta['title']+' — Alec Kriebel, ORCID 0009-0001-9320-500X; v'+meta['version']+'; preprint '+meta['publication_date']
    +'. Source Conjecture 1 resolved affirmatively for every finite binary graph: the finite MTP2 original-edge model is closed and equals the closure of positive attractive Ising laws on the same edges. Arbitrary zero supports, pins, equality blocks, isolated and empty graph conventions included. '
    +'The negative witness for Conjectures 2 and 3 is credited to Gandolfi–Lenarda, published 13 April 2017; its C6 lift is not claimed new. Prior toric, MTP2, support and graph-cut foundations are explicitly credited, including Kahle–Sullivant. Bounded priority audit; no first-discovery or worldwide continuing-openness certificate. '
    +'Five-page unrefereed research note; extensive AI use, no independent external human peer review or proof-assistant certification. Successive new full-preprint adversarial reviews, with provenance and count-label defects globally corrected before a fresh full review. PDF plus portable standard-Python verification package, source, expected outputs, provenance and exact metadata. Finite controls supplement unrestricted proofs. Original author history 2/5 preserved. '
    +'Primary question: https://doi.org/10.4171/owr/2022/55. Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/311.')
row = [problem,'',published['doi_url'],notes]
params = {'spreadsheetId':ID,'range':"'Math Puzzles'!A:"+last_column,'valueInputOption':'RAW',
    'insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
body = {'majorDimension':'ROWS','values':[row]}
(D/'tracker_row_request.json').write_text(json.dumps({'utc':utc(),'gid':GID,'params':params,'body':body,
    'headers_verified':True,'duplicate_found':False,
    'user_authorization':'Explicit persistent-goal instruction to append the confirmed published paper and DOI.'},indent=2)+'\n')
values('append',params,'tracker_dry_run',body,is_private=True,dry=True)
current_clearance()
window()
response = values('append',params,'tracker_append',body)
assert response['spreadsheetId'] == ID
u = response['updates']
assert u['updatedRows'] == 1 and u['updatedColumns'] == 4 and u['updatedCells'] == 4
actual = u['updatedRange']
assert actual.startswith("'Math Puzzles'!") or actual.startswith('Math Puzzles!')
readback = values('get',{'spreadsheetId':ID,'range':actual,'valueRenderOption':'FORMULA'},'tracker_readback')
assert readback['values'] == [row]
after = values('get',{'spreadsheetId':ID,'range':whole_range,
    'valueRenderOption':'FORMULA'},'all_rows_after',is_private=True)
assert after['values'] == before['values'] + [row], 'Whole-row sequence changed or append duplicated; stop and reconcile read-only.'
assert sum(published['doi'] in str(r) for r in after['values'][1:]) == 1
assert sum('30005303' in str(r) for r in after['values'][1:]) == 1
receipt = {'utc':utc(),'status':'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK','spreadsheetId':ID,'gid':GID,
    'updatedRange':actual,'doi':published['doi'],'record_url':published['record_url'],'row':row,
    'solution_chat_cell_blank':True,'no_chat_shared_or_outside_person_contacted':True,
    'prior_rows_read_privately':True,'all_prior_rows_unchanged':True,'exact_one_target_row_in_whole_postscan':True,'whole_postscan_native':str(private/'all_rows_after_execution.json'),'all_original_sheet_columns_scanned':column_count,'whole_before_after_rows_equal_plus_exact_one_new_row':True,'automatic_append_retry':False,'gws_binary':cli_pin,'gws_version':'0.22.5','single_cli_append_invocation':True}
(D/'TRACKER_COMPLETE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'row'},indent=2))
