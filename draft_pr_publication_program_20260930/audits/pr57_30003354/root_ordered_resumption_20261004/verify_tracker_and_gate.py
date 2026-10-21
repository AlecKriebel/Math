"""Independently read the actual appended row and bind the current ROOT gate."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]
O=A/'ordered_publication_operations_20261004'
C=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
def sha(b): return hashlib.sha256(b).hexdigest()
def bind(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
def load(p): return json.loads(p.read_bytes())
def save(p,v):
    with p.open('x') as f: json.dump(v,f,indent=2); f.write('\n')
if sys.flags.optimize: raise RuntimeError('Optimization forbidden')
spec=importlib.util.spec_from_file_location('tracker',R/'draft_pr_publication_program_20260930/infrastructure/append_publication.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
pub=load(F/'PUBLICATION_VERIFICATION.json')
assert pub['published'] and pub['all_public_bytes_identical'] and pub['DOI']=='10.5281/zenodo.23131374'
cap=C/'root_pr57_tracker_append_20261004_actual_capture'
assert load(cap/'CAPTURE.json')['status']=='PASS'
result=load(cap/'stdout.bin'); assert result['state']=='appended_verified' and result['append_performed'] is True
attempt=Path(result['receipt_dir']); attempt.relative_to(F/'tracker')
request=load(attempt/'request.json'); response=load(attempt/'response.json'); original_read=load(attempt/'readback.json')
row=request['body']['values'][0]; title=request['resolved_title']; ran=result['range']
source=load(A/'original_preparation_family/original/source_record.json')
assert source['id']==30003354 and source['problem_number']=='OWR-15208-008'
assert title=='Math Puzzles' and request['sheetId']==t.SHEET_ID and request['execute_requested'] is True
assert request['problem_keys']==['unsolvedmath:30003354','unsolvedmath:OWR-15208-008']
assert row==['https://www.unsolvedmath.com/problems/OWR-15208-008','','https://doi.org/'+pub['DOI'],(F/'TRACKER_NOTES.txt').read_text().rstrip('\r\n')]
assert original_read['values']==[row] and response['updates']['updatedData']['values']==[row]
number=t.range_row(ran,title)
private=F/'fresh_tracker_readback'; private.mkdir()
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def run(name,params):
    argv=['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60)
    (private/(name+'.stdout')).write_bytes(out); (private/(name+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return json.loads(out)
params={'spreadsheetId':t.SPREADSHEET_ID,'range':"'Math Puzzles'!A:D",'majorDimension':'ROWS','valueRenderOption':'UNFORMATTED_VALUE'}
values=run('values',params); formulas=run('formulas',{**params,'valueRenderOption':'FORMULA'})
assert t.a1_range(values['range'],title)==t.a1_range(formulas['range'],title)
assert values['majorDimension']==formulas['majorDimension']=='ROWS'
rows=[t.padded_row(r) for r in values['values']]; frows=[t.padded_row(r) for r in formulas['values']]
assert len(rows)==len(frows) and rows[0]==frows[0]==t.HEADERS
assert all(r[c]==f[c] and not f[c].startswith('=') for r,f in zip(rows,frows) for c in (0,2))
assert t.duplicate_row(rows,{'unsolvedmath:OWR-15208-008','unsolvedmath:30003354'},t.normalize_doi(pub['DOI']))==(number,row)
assert rows[number-1]==row
freshrow=run('row',{**params,'range':ran}); assert freshrow['values']==[row] and t.range_row(freshrow['range'],title)==number
track={'schema':'pr57-ordered-publication-tracker-verification/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'DOI':pub['DOI'],'range':ran,'spreadsheet_id':t.SPREADSHEET_ID,'sheet_id':t.SHEET_ID,'append_performed':True,'independent_readback_exact':True,'fresh_full_table_exactly_one_matching_problem_DOI_row':True,'actual_four_cells':row,'original_problem_aliases_verified_from_original_source':True,'append_result':bind(attempt/'result.json'),'request':bind(attempt/'request.json'),'append_response':bind(attempt/'response.json'),'independent_row_readback':bind(private/'row.stdout'),'original_append_row_readback':bind(attempt/'readback.json'),'fresh_full_table_values':bind(private/'values.stdout'),'fresh_full_table_formulas':bind(private/'formulas.stdout'),'fresh_actual_commands':bind(private/'COMMANDS.json')}
save(F/'TRACKER_VERIFICATION.json',track)
inputs=load(O/'SOURCE_BINDINGS.json')
assert inputs['integration_helper']['sha256']=='9c481725fe96fbe1097166cdb24e3a45dbb564418b9cf39dbc9b4ba938c32718'
assert bind(R/inputs['integration_helper']['path'])==inputs['integration_helper']
for pin in inputs['final_artifacts']: assert bind(R/pin['path'])==pin
gate={'schema':'pr57-ordered-publication-final-gate/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'PR':57,'reviewed_head':inputs['reviewed_head'],'eligible_intake_literal_status':'claimed_solved','original_budget':'1/5','new_central_proof_attempts':0,'goal_objective_sha256':'1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04','exact_claim':inputs['exact_claim'],'publication_authorized':True,'root_personally_read_helper_source':True,'root_personally_revalidated_exact_package':True,'all_current_substantive_findings_resolved':True,'full_specified_finite_integer_source_target_resolved':True,'never_process_initially_nonclaimed_PRs':True,'bounded_priority_audit_complete':True,'AI_tools_used_extensively':True,'worldwide_priority_guarantee':False,'PR50_exception_extended':False,'human_peer_review':False,'formal_proof_certification':False,'source_bindings':bind(O/'SOURCE_BINDINGS.json'),'publication_verification':bind(F/'PUBLICATION_VERIFICATION.json'),'tracker_verification':bind(F/'TRACKER_VERIFICATION.json'),'PR57_ordered_workflow_percent':95,'dated_completed_program_fraction_percent':5/99*100,'native_merge_or_acceptance_performed':False,'goal_complete':False}
for key in ['ROOT_final_package_adjudication','ROOT_priority_adjudication','ROOT_current_exact_package_readback','original_authentication','original_custody','current_SOURCE_custody','priority_custody','manifest','clean_reviews','final_artifacts']: gate[key]=inputs[key]
save(F/'FINAL_NATIVE_GATE.json',gate)
print(json.dumps({'tracker':track,'gate':gate},indent=2))
