"""One exact DOI row through gws after anonymous full public verification."""
from submission_gate import *
from public_identity import identity,resolution_binding
from datetime import datetime,timezone
import json
lock=acquire();clear=current_clearance();OUT.mkdir(exist_ok=True)
assert not (OUT/'TRACKER_COMPLETE.json').exists() and not (OUT/'tracker_append_preexecution.json').exists(),'Inspect uncertain previous append; do not append twice.'
published=load(OUT/'inspect_published_receipt.json');public=load(OUT/'PUBLIC_RECORD_VERIFICATION.json')
identity(published);resolution_binding(public['doi_resolution'],published['id'])
assert published['state']=='published' and published['environment']=='production'
assert public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES' and public['record_id']==published['id'] and public['doi']==published['doi'] and public['exact_record_identity_bound']
assert len(public['all_file_bytes'])==2 and all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes'])
expected_names={'focal-pedal-ratios-note.pdf','focal-pedal-ratios-verification.zip'}
assert {x['name'] for x in public['all_file_bytes']}==expected_names
for x in public['all_file_bytes']:
 b=(O/x['name']).read_bytes();assert x['bytes']==len(b) and x['sha256']==sha(b) and x['md5']==hashlib.md5(b).hexdigest()
 for field in ['argv','cwd','orchestrator_sha256','started_utc','finished_utc','exit_code','stdout_bytes','stdout_sha256','stderr_bytes','stderr_sha256']:
  assert field in x['native']
 assert x['native']['exit_code']==0 and x['native']['stdout_bytes']==len(b) and x['native']['stdout_sha256']==sha(b)
 assert x['native']['orchestrator_sha256']==pin(D/'publication_preparation/public_identity.py')['sha256']
 assert x['native']['origin_credentials_absent'] and x['native']['default_configuration_disabled']
 assert x['native']['argv'][:2]==['/usr/bin/curl','-q']
 assert x['native']['argv'][-1]==f'https://zenodo.org/api/records/{published["id"]}/files/{x["name"]}/content'
meta=load(O/'zenodo-deposit.json')['metadata'];assert published['title']==meta['title']
for x in published['files']:
 b=(O/x['name']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256']
cli='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
assert pin(cli)['sha256']=='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20';GID=1254632077
private=OUT/('private_tracker_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'));private.mkdir(exist_ok=False)
def values(method,params,label,body=None,is_private=False,dry=False):
 argv=[cli,'sheets','spreadsheets','values',method,'--params',json.dumps(params)]
 if body is not None:argv+=['--json',json.dumps(body)]
 if dry:argv+=['--dry-run']
 return execute(label,argv,private if is_private else None)
sheet=execute('sheet_metadata',[cli,'sheets','spreadsheets','get','--params',json.dumps({'spreadsheetId':ID,'fields':'spreadsheetId,sheets(properties(sheetId,title,gridProperties(rowCount,columnCount)))'})],private)
assert sheet['spreadsheetId']==ID
x=[s['properties'] for s in sheet['sheets'] if s['properties']['sheetId']==GID];assert len(x)==1 and x[0]['title']=='Math Puzzles';x=x[0];columns=x['gridProperties']['columnCount'];assert columns>=4
last='';v=columns
while v:v,rem=divmod(v-1,26);last=chr(65+rem)+last
whole="'Math Puzzles'!A1:"+last
before=values('get',{'spreadsheetId':ID,'range':whole+str(x['gridProperties']['rowCount']),'valueRenderOption':'FORMULA'},'existing_rows',is_private=True)
assert before['values'][0][:4]==['Original Problem','Solution Chat URL','DOI','Notes']
assert not [r for r in before['values'][1:] if published['doi'] in str(r) or '5100034' in str(r) or meta['title'].lower() in str(r).lower()],'Existing target/title/DOI requires reconciliation.'
problem='AMR-050-0034 (5100034): Focal pedal area ratio equality'
notes=(meta['title']+' — Alec Kriebel, ORCID 0009-0001-9320-500X; v'+meta['version']+'; preprint '+meta['publication_date']+'. '
 +'The displayed focal-ratio equality E is proved for every primitive convex or coprime star elliptic billiard with a strict nondegenerate confocal elliptical caustic. The stronger M gives a positive outer/original pedal-area multiplier independent of phase and common to both foci. Signed supporting-line areas, nonvanishing, reversal and repetition are covered. An exact triangle disproves the interpretation C that the common focal ratio is itself phase constant. '
 +'The April 2020 observation, known even symmetry, conditional triangular implication of old geometric results, classical negative corollary, canonical coordinates and established elliptic principal-part methods are credited. No absolute firstness, even-M novelty, separate triangular novelty, new negative theorem or new general method is claimed; six unavailable journal editions remain bounded-priority coverage limits. '
 +'Six-page unrefereed research note, extensive AI assistance, successive new whole-package adversarial reviews; no external human peer review or formal proof-assistant certification. PDF plus portable verification archive, standalone source, historical supplement, exact and finite noninterval diagnostics, actual outputs and provenance. Original author history 1/5 preserved. '
 +'Primary source: https://doi.org/10.1007/s40598-021-00174-y. Record: '+published['record_url']+'. Reviewed PR: https://github.com/AlecKriebel/Math/pull/305.')
row=[problem,'',published['doi_url'],notes]
params={'spreadsheetId':ID,'range':"'Math Puzzles'!A:"+last,'valueInputOption':'RAW','insertDataOption':'INSERT_ROWS','includeValuesInResponse':True}
body={'majorDimension':'ROWS','values':[row]}
(OUT/'tracker_row_request.json').write_text(json.dumps({'utc':utc(),'gid':GID,'params':params,'body':body,'headers_verified':True,'duplicate_found':False,'user_authorization':'Explicit persistent-goal instruction to append confirmed paper DOI and details.'},indent=2)+'\n')
values('append',params,'tracker_dry_run',body,is_private=True,dry=True)
current_clearance();operational_clearance();window();response=values('append',params,'tracker_append',body)
assert response['spreadsheetId']==ID
u=response['updates'];assert (u['updatedRows'],u['updatedColumns'],u['updatedCells'])==(1,4,4)
actual=u['updatedRange'];assert actual.startswith("'Math Puzzles'!") or actual.startswith('Math Puzzles!')
readback=values('get',{'spreadsheetId':ID,'range':actual,'valueRenderOption':'FORMULA'},'tracker_readback');assert readback['values']==[row]
after=values('get',{'spreadsheetId':ID,'range':whole,'valueRenderOption':'FORMULA'},'all_rows_after',is_private=True)
assert after['values']==before['values']+[row],'Prior rows changed or append duplicated; stop and reconcile read-only.'
assert sum(published['doi'] in str(r) for r in after['values'][1:])==1
assert sum('5100034' in str(r) for r in after['values'][1:])==1
receipt={'utc':utc(),'status':'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK','spreadsheetId':ID,'gid':GID,'updatedRange':actual,'doi':published['doi'],'record_url':published['record_url'],'row':row,'solution_chat_cell_blank':True,'no_individual_contacted':True,'all_original_sheet_columns_scanned':columns,'all_prior_rows_unchanged':True,'exact_one_target_row_in_whole_postscan':True,'single_cli_append_invocation':True,'automatic_append_retry':False,'gws_binary':pin(cli),'whole_before_after_rows_equal_plus_exact_one_new_row':True,'private_full_scan_directory':str(private)}
(OUT/'TRACKER_COMPLETE.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='row'},indent=2))
