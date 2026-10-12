#!/usr/bin/python3
"""Bounded final control: own actual receipts and fixed SOURCE hashes only."""
import datetime,hashlib,json,pathlib,stat
F=pathlib.Path(__file__).absolute().parent;H=F.parent/'acceptance_preparation_family_v2';checks=0
def ck(v,n):
    global checks
    if not v:raise ValueError(n)
    checks+=1
def sha(b):return hashlib.sha256(b).hexdigest()
seen=[]
expected={'fixed_corpus':1,'fixed_corpus_v2':1,'fixed_corpus_v3':0,'ownership_phase':0}
for name,code in expected.items():
    d=F/'captures'/name;c=json.loads((d/'CAPTURE.json').read_bytes());p=json.loads((d/'PRELAUNCH.json').read_bytes())
    ck(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==code and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False,'Real retained child')
    ck(all(c[k]==p[k] for k in p if k!='schema'),'Complete literal prelaunch values')
    ck(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==p['source_sha256'] and sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==p['operator_sha256'],'Actual copied source/operator')
    ck(sha(pathlib.Path(p['argv'][2]).read_bytes())==p['source_sha256'],'Current source equals preserved actual source')
    for k in ['stdout','stderr']:
        b=(d/c[k]['path']).read_bytes();ck(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'Complete split stream hash/size')
    start=datetime.datetime.fromisoformat(c['started_utc']);end=datetime.datetime.fromisoformat(c['finished_utc']);created=datetime.datetime.fromisoformat(p['created_utc']);ck(created.utcoffset()==start.utcoffset()==end.utcoffset()==datetime.timedelta(0) and created<=start<=end,'Actual child inside operator interval, not equal clocks')
    ck(c['production_imported_compiled_executed'] is False,'No production source executed')
    if code==0:ck(c['stderr']['bytes']==0 and c['status']=='PASS_PRIVATE_SOURCE_ONLY','Successful real child')
    else:ck(c['stderr']['bytes']>0 and c['status']=='FAILED_PRIVATE_SOURCE_CONTROL_PRESERVED','Failed control remains failed')
    seen.append({'directory':name,'actual_pid':c['pid'],'exit_code':code,'capture_sha256':sha((d/'CAPTURE.json').read_bytes())})
fixed=json.loads((F/'FIXED_CORPUS_RESULT_V3.json').read_bytes());owned=json.loads((F/'OWNERSHIP_PHASE_RESULT.json').read_bytes());ck(fixed['assertions_passed']==77649 and fixed['complete_read_count']==9244 and fixed['unique_canonical_read_count']==2851 and owned['assertions_passed']==12406 and owned['negative_mutants_rejected']==4185 and len(owned['actual_permission_observations'])==4096,'Exact completed own control metrics')
ck(fixed['SOURCE_verdict'] is None and owned['SOURCE_verdict'] is None and fixed['future_acceptance_approved'] is False and owned['future_acceptance_approved'] is False,'Control result never source/future approval')
manifest=(H/'PREPARATION_MANIFEST.json').read_bytes();ck(sha(manifest)==fixed['preparation_manifest_sha256']=='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40','Exact final unchanged SOURCE manifest')
for n,digest in fixed['six_source_sha256'].items():ck(sha((H/n).read_bytes())==digest and stat.S_IMODE((H/n).stat().st_mode)==292,'No production source drift')
out={'schema':'pr46-source-v2-independent-final-capture-controls/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_BOUNDED_FINAL_ACTUAL_CAPTURE_CONTROL','assertions_passed':checks,'complete_retained_actual_captures':seen,'preparation_manifest_sha256':fixed['preparation_manifest_sha256'],'production_imported_compiled_executed':False,'closer_or_verifier_executed_by_reviewer':False,'future_acceptance_approved':False,'SOURCE_verdict':None,'new_substantive_attempts':0,'audit_turns':0}
(F/'FINAL_CAPTURE_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='complete_retained_actual_captures'}))
