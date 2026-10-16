"""Verify actual PR50 append receipts and new full-table reads; freeze final gate."""
from pathlib import Path
import datetime as dt
import hashlib
import importlib.util
import json
import os
import subprocess

Q=Path(__file__).resolve().parent; A=Q.parent; R=A.parents[2]
O=A/'qualified_publication_operations_20261004'
C=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'
def binding(p): return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p): return json.loads(p.read_bytes())
def save(p,value):
    with p.open('x') as f: json.dump(value,f,ensure_ascii=False,indent=2); f.write('\n')
spec=importlib.util.spec_from_file_location('tracker',R/'draft_pr_publication_program_20260930/infrastructure/append_publication.py')
t=importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
pub=load(Q/'PUBLICATION_VERIFICATION.json')
assert pub['published'] and pub['all_public_bytes_identical'] and pub['DOI']=='10.5281/zenodo.23131001'
capture=C/'root_pr50_qualified_tracker_append_20261004_actual_capture'
assert load(capture/'CAPTURE.json')['status']=='PASS'
result=load(capture/'stdout.bin')
assert result['state']=='appended_verified' and result['append_performed'] is True
attempt=Path(result['receipt_dir']); attempt.relative_to(O/'private/tracker')
request=load(attempt/'request.json'); response=load(attempt/'response.json'); oldread=load(attempt/'readback.json')
row=request['body']['values'][0]; title=request['resolved_title']; ran=result['range']
assert title=='Math Puzzles' and request['sheetId']==t.SHEET_ID and request['execute_requested'] is True
assert row==['https://www.unsolvedmath.com/problems/AMR-105-0042','', 'https://doi.org/'+pub['DOI'],(Q/'TRACKER_NOTES.txt').read_text().rstrip('\r\n')]
assert oldread['values']==[row] and response['updates']['updatedData']['values']==[row]
number=t.range_row(ran,title)
private=O/'private/fresh-tracker-readback'; private.mkdir()
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def run(name,params):
    argv=['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','sheets','spreadsheets','values','get','--params',json.dumps(params)]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60)
    (private/(name+'.stdout')).write_bytes(out); (private/(name+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,
       'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
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
match=t.duplicate_row(rows,{'unsolvedmath:AMR-105-0042','unsolvedmath:10600042'},t.normalize_doi(pub['DOI']))
assert match==(number,row) and rows[number-1]==row
track={'schema':'pr50-qualified-note-tracker-verification/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
 'DOI':pub['DOI'],'range':ran,'spreadsheet_id':t.SPREADSHEET_ID,'sheet_id':t.SHEET_ID,
 'append_performed':True,'independent_readback_exact':True,'fresh_full_table_exactly_one_matching_problem_DOI_row':True,
 'actual_four_cells':row,'original_problem_aliases_verified_from_original_source':True,
 'append_result':binding(attempt/'result.json'),'request':binding(attempt/'request.json'),
 'append_response':binding(attempt/'response.json'),'independent_row_readback':binding(attempt/'readback.json'),
 'fresh_full_table_values':binding(private/'values.stdout'),'fresh_full_table_formulas':binding(private/'formulas.stdout'),
 'fresh_actual_commands':binding(private/'COMMANDS.json'),'historical_priority_certified':False,'present_openness_certified':False}
save(Q/'TRACKER_VERIFICATION.json',track)
adjudication=load(Q/'ROOT_REVIEW_ADJUDICATION.json')
for b in adjudication['final_artifacts']:
    assert binding(R/b['path'])==b
gate={'schema':'pr50-qualified-publication-final-gate/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
 'reviewed_head':adjudication['reviewed_head'],'publication_authorized':True,'user_exception_priority_unresolved':True,
 'all_current_substantive_findings_resolved':True,'priority_clearance':False,'historical_priority_certified':False,'present_openness_certified':False,
 'exact_claim':'Explicit four classical and eight virtual reversible algebraic scheme families classify ordinary oriented unframed link closures using only even-strand braid states, with arbitrary finite word blocks and the stated syntactic supports.',
 'manifest':pub['manifest'],'final_artifacts':adjudication['final_artifacts'],
 'clean_reviews':[x['verdict'] for x in adjudication['reviews']],
 'ROOT_semantic_adjudication':binding(Q/'ROOT_REVIEW_ADJUDICATION.json'),
 'publication_verification':binding(Q/'PUBLICATION_VERIFICATION.json'),'tracker_verification':binding(Q/'TRACKER_VERIFICATION.json'),
 'new_central_proof_attempts':0,'original_budget':'1/5','program_completion_asserted':False}
save(Q/'FINAL_NATIVE_GATE.json',gate)
print(json.dumps({'tracker':track,'gate':gate},indent=2,ensure_ascii=False))
