#!/usr/bin/env python3
"""Actual queue functions on an explicitly synthetic private one-record catalogue."""
from pathlib import Path
from types import SimpleNamespace
import json,hashlib,sqlite3,shutil,importlib.util,datetime
HERE=Path(__file__).resolve().parent;A=HERE.parent;REPO=A.parents[2];Q=REPO/'unsolved_math_prioritization'
R=HERE/'sandbox'/'synthetic_workflow';R.mkdir(parents=True,exist_ok=True)
shutil.copy2(Q/'queue.py',R/'queue.py')
problem=json.loads((A/'source_snapshot/source_record.json').read_text());raw=json.loads((Q/'cache/research_results.json').read_text());prior=raw['AMR-099-0043'];pair=hashlib.sha256(json.dumps([problem,prior],sort_keys=True).encode()).hexdigest()
write=lambda p,j:p.write_text(json.dumps(j,indent=2)+'\n')
write(R/'policy.json',json.loads((Q/'policy.json').read_text()))
manifest=json.loads((Q/'manifest.json').read_text());manifest['records']=1;write(R/'manifest.json',manifest)
(R/'cache').mkdir(exist_ok=True);db=sqlite3.connect(R/'cache/catalog.sqlite');db.execute('CREATE TABLE records (key TEXT PRIMARY KEY,payload TEXT,report TEXT)');db.execute('CREATE TABLE metadata (revision TEXT)');db.execute('INSERT INTO records VALUES (?,?,?)',('10000043',json.dumps(problem),json.dumps(prior)));db.execute('INSERT INTO metadata VALUES (?)',(manifest['revision'],));db.commit();db.close()
row=[x for x in json.loads((Q/'catalog.json').read_text()) if x['id']=='10000043'][0]
assessment=json.loads((Q/'assessments.json').read_text())['10000043'];write(R/'assessments.json',{'10000043':assessment})
spec=importlib.util.spec_from_file_location('actual_private_queue',R/'queue.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
results=[]
def fixture(state):write(R/'catalog.json',[row]);write(R/'state.json',state)
def call(name,func,args,rejected):
 before=(R/'state.json').read_bytes()
 try:func(args);error=None
 except Exception as e:error=type(e).__name__+': '+str(e)
 assert bool(error)==rejected,(name,error)
 if rejected:assert before==(R/'state.json').read_bytes()
 results.append({'name':name,'rejected':rejected,'error':error,'rejected_without_state_write':before==(R/'state.json').read_bytes() if rejected else None})
evidence={k:'FALSE SYNTHETIC PLACEHOLDER; not mathematical evidence' for k in ['exact_claim','primary_sources','literature_checked_at','success_test','budget','prior_attempt_gap','duplicate_check','proof_artifact','independent_review','novelty_check']};evidence['review_hash']=pair;write(R/'evidence.json',evidence)
args=lambda status:SimpleNamespace(id='10000043',status=status,note='Synthetic isolation test only',evidence=str(R/'evidence.json'))
fixture({});call('partial_without_prior_review',mod.status,args('partial'),True)
fixture({});stale=dict(evidence,review_hash='0'*64);write(R/'stale.json',stale);x=args('ready');x.evidence=str(R/'stale.json');call('stale_pair_hash_readiness',mod.status,x,True)
fixture({});call('candidate_by_generic_status_forbidden',mod.status,args('candidate_result'),True)
fixture({});call('verified_without_candidate_transition',mod.status,args('verified_solved'),True)
fixture({'10000043':{'status':'exhausted','turns_used':5,'review_hash':pair,'readiness_review_hash':pair}});call('restart_at_exhausted_fifth_turn',mod.status,args('ready'),True)
fixture({'10000043':{'status':'in_progress','turns_used':4,'review_hash':pair,'readiness_review_hash':pair}})
call('actual_fifth_unfinished_turn_exhausts',mod.record_turn,SimpleNamespace(id='10000043',outcome='continue',note='Synthetic isolation test'),False)
state=json.loads((R/'state.json').read_text());assert state['10000043']['status']=='exhausted' and state['10000043']['turns_used']==5
call('sixth_turn_refused',mod.record_turn,SimpleNamespace(id='10000043',outcome='continue',note='Synthetic'),True)
fixture({});call('metadata_readiness_with_false_prose_passes',mod.status,args('ready'),False)
line=next(x for x in (R/'QUEUE.md').read_text().splitlines() if '| 10000043 / AMR-099-0043 |' in x);assert len(line.split('|')[1:-1])==8
fixture({'10000043':{'status':'independent_verification','turns_used':2,'candidate_turn':2,'review_hash':pair,'readiness_review_hash':pair}});call('metadata_verified_fields_with_false_prose_passes',mod.status,args('verified_solved'),False)
# Distinguish semantic serialization, stored text, missing values and types.
sha=lambda j:hashlib.sha256(json.dumps(j,sort_keys=True).encode()).hexdigest()
variant=json.loads(json.dumps([problem,prior],indent=7,separators=(',',': ')));assert sha(variant)==pair
variants=[('missing_report', [problem,{}]),('JSON_null',[problem,None]),('string_null',[problem,'null']),('classification_deleted',[problem,{k:v for k,v in prior.items() if k!='classification'}])]
for name,val in variants:assert sha(val)!=pair;results.append({'name':name,'serialized_pair_identity_rejected':True})
# No input rendering normalization can change logical record identity unnoticed.
alt=dict(problem);alt['id']='10000043';assert sha([alt,prior])!=pair;results.append({'name':'numeric_id_to_string','serialized_pair_identity_rejected':True})
report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queue_program_sha256':hashlib.sha256((R/'queue.py').read_bytes()).hexdigest(),'tests':results,'synthetic_legacy_rendered_columns':8,'pair_hash':pair,'stored_JSON_whitespace_does_not_change_parsed_hash':True,'scope':'Actual unmodified queue functions, private synthetic data only. No real proof turn, tracker/status/queue mutation. False prose passing demonstrates metadata checks cannot certify mathematics. Legacy renderer loses maintained12columns.'}
(HERE/'WORKFLOW_CONTROL_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
