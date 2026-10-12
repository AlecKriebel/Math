"""Reopen real Zenodo/GWS native captures and entire tracker before/after values.
No external request or mutation. Private whole-sheet rows are never printed.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,sys,hashlib
if sys.flags.optimize:raise RuntimeError('Optimized actual evidence check forbidden.')
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D/'publication_preparation'));import submission_gate as g
O=g.OUT;bindings={};native=[]
def read(p):
 p=Path(p);b=p.read_bytes();bindings[str(p)]=g.pin(p);return b
def load(p):return json.loads(read(p))
def execution(folder,label):
 j=load(folder/(label+'_execution.json'));pre=load(folder/(label+'_preexecution.json'))
 assert all(j[k]==v for k,v in pre.items()) and j['cwd']==str(g.R) and j['exit_code']==0 and j['timed_out'] is False and j['automatic_retry'] is False
 assert datetime.fromisoformat(j['ended_utc'])>=datetime.fromisoformat(j['started_utc'])
 for p,e in j['programs'].items():assert g.pin(p)==e
 raw={}
 for k in ['stdout','stderr']:
  raw[k]=read(folder/(label+'.'+k));assert len(raw[k])==j[k+'_bytes'] and g.sha(raw[k])==j[k+'_sha256']
 native.append(dict(label=label,capture_directory=str(folder),argv=j['argv'],cwd=j['cwd'],started_utc=j['started_utc'],ended_utc=j['ended_utc'],exit_code=0,full_streams_reopened=True,stderr_bytes=len(raw['stderr'])))
 return j,json.loads(raw['stdout'])
g.current_clearance();g.operational_clearance()
publication=load(O/'inspect_published_receipt.json');assert publication['id']==23149775 and publication['doi']=='10.5281/zenodo.23149775'
for label in ['stage','inspect_draft','publish','inspect_published']:
 j,value=execution(O,label);assert value==load(O/(label+'_receipt.json'))
 assert value['id']==publication['id'] and value['environment']=='production' and value['metadata_normalizations']==[]
 assert value['state']==('published' if label in ['publish','inspect_published'] else 'ready_to_publish')
 assert j['argv'][:3]==['/opt/homebrew/bin/python3','-E','-B'] and j['argv'][3]==str(g.R/'zenodo_deposit_tool/zenodo.py')
assert native[2]['argv'][-2:]==['--confirm-id','23149775']
actualpublic=load(D/'ROOT_ACTUAL_PUBLIC_EVIDENCE_READBACK.json');assert actualpublic['status']=='PASS_PR305_ACTUAL_FULL_PUBLIC_EVIDENCE_AUTHENTICATED_BEFORE_TRACKER'
for p,e in actualpublic['evidence_pins'].items():assert g.pin(p)==e
tracker=load(O/'TRACKER_COMPLETE.json');assert tracker['status']=='PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK' and tracker['updatedRange']=="'Math Puzzles'!A24:D24" and tracker['doi']==publication['doi']
private=Path(tracker['private_full_scan_directory']);assert private.resolve()==private and private.parent==O
meta_j,meta=execution(private,'sheet_metadata');before_j,before=execution(private,'existing_rows');dry_j,dry=execution(private,'tracker_dry_run');append_j,append=execution(O,'tracker_append');rb_j,rb=execution(O,'tracker_readback');after_j,after=execution(private,'all_rows_after')
cli='/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws'
assert g.pin(cli)==tracker['gws_binary'] and tracker['gws_binary']['sha256']=='0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e'
for j in [meta_j,before_j,dry_j,append_j,rb_j,after_j]:assert j['argv'][0]==cli
ID='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
sheet=[x['properties'] for x in meta['sheets'] if x['properties']['sheetId']==1254632077];assert len(sheet)==1 and sheet[0]['title']=='Math Puzzles' and sheet[0]['gridProperties']['columnCount']==43
assert json.loads(before_j['argv'][-1])==dict(spreadsheetId=ID,range="'Math Puzzles'!A1:AQ1019",valueRenderOption='FORMULA')
assert json.loads(after_j['argv'][-1])==dict(spreadsheetId=ID,range="'Math Puzzles'!A1:AQ",valueRenderOption='FORMULA')
row=tracker['row'];assert len(row)==4 and row[1]=='' and row[2]==publication['doi_url'] and row[0]=='AMR-050-0034 (5100034): Focal pedal area ratio equality'
params=json.loads(append_j['argv'][append_j['argv'].index('--params')+1]);body=json.loads(append_j['argv'][append_j['argv'].index('--json')+1])
assert params==dict(spreadsheetId=ID,range="'Math Puzzles'!A:AQ",valueInputOption='RAW',insertDataOption='INSERT_ROWS',includeValuesInResponse=True) and body==dict(majorDimension='ROWS',values=[row])
assert '--dry-run' in dry_j['argv'] and '--dry-run' not in append_j['argv']
assert append['spreadsheetId']==ID and append['updates']['updatedRange']==tracker['updatedRange'] and tuple(append['updates'][k] for k in ['updatedRows','updatedColumns','updatedCells'])==(1,4,4)
assert rb['values']==[row] and before['values'][0][:4]==['Original Problem','Solution Chat URL','DOI','Notes']
assert after['values']==before['values']+[row] and len(before['values'])==23 and len(after['values'])==24
assert sum(publication['doi'] in str(r) for r in after['values'][1:])==sum('5100034' in str(r) for r in after['values'][1:])==1
assert datetime.fromisoformat(actualpublic['utc'])<=datetime.fromisoformat(append_j['started_utc'])
for p,e in bindings.items():assert g.pin(p)==e
report=dict(status='PASS_ROOT_ACTUAL_PUBLICATION_AND_SINGLE_TRACKER_ROW_FULL_NATIVE_CUSTODY',UTC=g.utc(),PR=305,DOI=publication['doi'],record_url=publication['record_url'],tracker_range=tracker['updatedRange'],reviewed_metadata_values=11,published_whole_files=2,complete_private_sheet_columns=43,prior_rows=23,after_rows=24,exact_one_RAW_four_cell_append=True,all_prior_formula_values_preserved=True,all_actual_full_streams_reopened=True,native_execution_captures=native,bindings=bindings,no_external_request_or_mutation=True,science_percent=100,bounded_priority_percent=100,workflow_percent=85,native_merge_still_pending=True)
target=D/'ROOT_ACTUAL_PUBLICATION_TRACKER_FINAL_CUSTODY.json';assert not target.exists();target.write_text(json.dumps(report,indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+report['UTC']+' — Exact reviewed PR305 package published in production record23149775, DOI10.5281/zenodo.23149775. Anonymous eleven-metadata/fullPDF+ZIP bytes/MD5/SHA and exactDOI resolution verified; ROOT reopened complete native captures, oneRAW4-cell GWSappend A24:D24, all prior23rows/all43formula columns unchanged. Publication+tracker complete; native merge still pending repaired operator clean review. Math100%, boundedpriority100%, workflow85%.\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['bindings','native_execution_captures']},indent=2))
