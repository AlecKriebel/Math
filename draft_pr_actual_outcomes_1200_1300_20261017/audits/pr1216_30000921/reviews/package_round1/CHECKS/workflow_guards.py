"""Offline stubs only: never starts Git, gh, gws, network or publication calls."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PUB=HERE.parent.parents[1]/'publication'
TMP=HERE.parent/'temp/workflow';TMP.mkdir(exist_ok=True)
def module(name):
 spec=importlib.util.spec_from_file_location('audit_'+name,PUB/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x)+'\n')
def forbidden(*a,**k):raise RuntimeError('UNSTUBBED EXTERNAL OPERATION')
meta=json.loads((PUB/'zenodo-deposit.json').read_text())
results=[]
# Append success and retry/identity failure modes, with call API fully replaced.
base_row=None
for case in ['first_append','exact_row_recovery','uncertain_intent','duplicate_rows','wrong_existing_row','wrong_headers','unpublished','readback_mismatch']:
 m=module('append_tracker');m.subprocess.run=forbidden;m.ROOT=TMP/('append_'+case);m.ROOT.mkdir(exist_ok=True)
 pub={'state':'published' if case!='unpublished' else 'draft','doi_url':'https://doi.org/10.0000/offline.fixture'}
 save(m.ROOT/'PUBLICATION_RECEIPT.json',pub);save(m.ROOT/'zenodo-deposit.json',meta)
 if case=='uncertain_intent':save(m.ROOT/'tracker/INTENT.json',{'uncertain':True})
 header=['Original Problem','Solution Chat URL','DOI','Notes'];rows=[header]
 if case in ['exact_row_recovery','duplicate_rows','wrong_existing_row']:
  if base_row is None:raise RuntimeError('missing captured fixture')
  r=copy.deepcopy(base_row)
  if case=='wrong_existing_row':r[3]+=' DRIFT'
  rows.append(r)
  if case=='duplicate_rows':rows.append(copy.deepcopy(r))
 if case=='wrong_headers':rows[0][0]='Unexpected'
 calls=[];appended=[]
 def stub(parts,params,body=None):
  calls.append(parts[-1])
  if parts==['spreadsheets','get']:return {'sheets':[{'properties':{'sheetId':m.GID,'title':"Offline's Fixture"}}]}
  if parts[-1]=='append':
   appended.append(body['values'][0]);return {'updates':{'updatedRange':"'Offline''s Fixture'!A2:D2",'updatedRows':1,'updatedColumns':4}}
  if params['range'].endswith('A:D'):return {'values':rows}
  value=copy.deepcopy(appended[0] if appended else rows[1])
  if case=='readback_mismatch':value[3]+=' altered'
  return {'values':[value]}
 m.call=stub
 try:m.main();error=None
 except Exception as e:error=str(e)
 if case=='first_append':
  if error or len(appended)!=1:raise RuntimeError('first append fixture failed '+str(error))
  base_row=appended[0]
 elif case=='exact_row_recovery':
  if error or appended:raise RuntimeError('recovery duplicated append')
 elif case=='readback_mismatch':
  if not error or len(appended)!=1 or not (m.ROOT/'tracker/INTENT.json').exists():raise RuntimeError('readback drift guard failed')
 else:
  if not error or appended:raise RuntimeError('unsafe append case '+case)
 results.append({'script':'append_tracker.py','case':case,'append_calls':len(appended),'outcome':'PASS' if error is None else error,'external_calls':0})
# PR gates: run up to each rejection with local read/bytes fixtures and stubbed Git/gh.
build=json.loads((PUB/'BUILD_RECEIPT.json').read_text())
for case in ['not_main','failed_gate','artifact_drift','metadata_drift','workflow_drift','unexpected_branch','closed_pr','unknown_retry_head','recorded_receipt_head_changed']:
 m=module('update_pr_publication');m.subprocess.run=forbidden;m.subprocess.check_output=forbidden;m.ROOT=TMP/('pr_'+case);m.ROOT.mkdir(exist_ok=True)
 # Copy only exact reviewed artifacts into this isolated fixture.
 for key in ['pdf','verification_zip']:(m.ROOT/build[key]['path']).write_bytes((PUB/build[key]['path']).read_bytes())
 (m.ROOT/'zenodo-deposit.json').write_bytes((PUB/'zenodo-deposit.json').read_bytes())
 (m.ROOT/'fixture_workflow.py').write_text('reviewed')
 digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
 gate={'status':'pass','pdf_sha256':build['pdf']['sha256'],'verification_zip_sha256':build['verification_zip']['sha256'],'metadata_sha256':digest(m.ROOT/'zenodo-deposit.json'),'workflow':{'fixture_workflow.py':digest(m.ROOT/'fixture_workflow.py')}}
 pub={'state':'published','files':[{'name':build[k]['path'],'size':build[k]['bytes'],'sha256':build[k]['sha256']} for k in ['pdf','verification_zip']]}
 tracker={'readback_verified':True}
 if case=='failed_gate':gate['status']='fail'
 if case=='artifact_drift':(m.ROOT/build['pdf']['path']).write_bytes(b'changed')
 if case=='metadata_drift':(m.ROOT/'zenodo-deposit.json').write_text('{}')
 if case=='workflow_drift':(m.ROOT/'fixture_workflow.py').write_text('changed')
 for name,obj in [('BUILD_RECEIPT.json',build),('FINAL_REVIEW_GATE.json',gate),('PUBLICATION_RECEIPT.json',pub),('tracker/TRACKER_RECEIPT.json',tracker)]:save(m.ROOT/name,obj)
 current={'headRefName':m.BRANCH,'headRefOid':m.ORIGINAL,'state':'OPEN','body':''}
 if case=='unexpected_branch':current['headRefName']='unrelated'
 if case=='closed_pr':current['state']='CLOSED'
 if case=='unknown_retry_head':
  current['headRefOid']='changed';save(m.ROOT/'PR_BRANCH_INTENT.json',{'commit':'intended'})
 if case=='recorded_receipt_head_changed':
  current['headRefOid']='changed';save(m.ROOT/'PR_BRANCH_RECEIPT.json',{'commit':'intended'})
 save(m.ROOT.parent/'SUBMITTED_SNAPSHOT.json',{'files':[],'body_sha256':'fixture'})
 gitcalls=[]
 def fakegit(*args,**kw):
  gitcalls.append(args)
  if args==('branch','--show-current'):return b'other' if case=='not_main' else b'main'
  raise RuntimeError('UNEXPECTED GIT EXECUTION '+str(args))
 m.git=fakegit;m.pr=lambda:current
 try:m.main();error=None
 except Exception as e:error=str(e)
 if not error or error.startswith('UNEXPECTED') or error.startswith('UNSTUBBED'):raise RuntimeError('PR guard not reached cleanly '+case+': '+str(error))
 results.append({'script':'update_pr_publication.py','case':case,'outcome':error,'git_calls':[list(c) for c in gitcalls],'external_calls':0})
(HERE/'workflow_guards.json').write_text(json.dumps({'status':'PASS','cases':results,'scope':'Offline rejection/recovery tests only; no deployment, network, Git, gws, gh, upload, append or merge occurred. The current update script does not itself implement upload or merge; those stages remain separately gated.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':len(results),'external_calls':0},indent=2))
