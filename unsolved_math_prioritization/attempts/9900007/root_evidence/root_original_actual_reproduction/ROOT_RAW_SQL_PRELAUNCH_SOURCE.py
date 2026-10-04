"""ROOT full type-sensitive source/prior importer reproduction, read-only database."""
from pathlib import Path
import collections
import datetime as dt
import hashlib
import json
import os
import sqlite3

A=Path(__file__).resolve().parent
R=A.parents[2]
D=A/'root_original_actual_reproduction'
C=R/'unsolved_math_prioritization/cache'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pairs(rows):
    o={}
    for k,v in rows:
        assert k not in o
        o[k]=v
    return o
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def pin(p):
    raw=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes()
with (D/'ROOT_RAW_SQL_PRELAUNCH_SOURCE.py').open('xb') as f:f.write(source)
raw_bytes=(C/'problems.json').read_bytes();prior_bytes=(C/'research_results.json').read_bytes()
raw=parse(raw_bytes);priors=parse(prior_bytes)
byid={str(v['id']):v for v in raw}
codes=collections.Counter(v['problem_number'] for v in raw)
assert len(raw)==len(byid)==15458 and len(priors)==6701
conn=sqlite3.connect('file:'+str(C/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
conn.execute('PRAGMA query_only=ON');assert conn.execute('PRAGMA query_only').fetchone()==(1,)
rows=conn.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall()
assert len(rows)==15458
for key,payload,report in rows:
    expected=dict(byid[key]);code=expected['problem_number']
    if codes[code]>1 and code in priors:expected['_ambiguous_report']=True
    expected_prior={} if expected.get('_ambiguous_report') else priors.get(code,{})
    assert equal(parse(payload),expected) and equal(parse(report),expected_prior),key
conn.close()
selected=byid['9900007'];code=selected['problem_number'];assert code=='AMR-098-0007'
original=(A/'source_snapshot/source_record.json').read_bytes()
assert equal(selected,parse(original))
prior_present=code in priors;prior=priors.get(code,{})
for name,data in [('pinned_problem.json',original),('pinned_prior_report.json',(json.dumps(prior,indent=2)+'\n').encode())]:
    with (A/name).open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
obj={'schema':'pr45-root-complete-raw-SQL-source-audit/v1','status':'PASS_ROOT_FULL_TYPED_RAW_SQL_AND_LITERAL_SOURCE','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'raw_full_bytes':len(raw_bytes),'prior_full_bytes':len(prior_bytes),'whole_raw_and_prior_bytes':len(raw_bytes)+len(prior_bytes),'raw_records':15458,'prior_records':6701,'SQL_rows':15458,'all_entire_payload_and_prior_objects_type_sensitive_equal':True,'raw_prior_key_present':prior_present,'entire_selected_prior_report':prior,'SQL_empty_object_is_absent_key_fallback':not prior_present,'retrieved_raw_null_prior':prior_present and prior is None,'entire_original_source_record_equal':True,'source_record':pin(A/'source_snapshot/source_record.json'),'pinned_problem':pin(A/'pinned_problem.json'),'pinned_prior_report':pin(A/'pinned_prior_report.json'),'foreign_original_cache_inputs_individually_pinned_not_copied':[pin(C/n) for n in ['problems.json','research_results.json','catalog.sqlite']],'original_substantive_attempts':1,'new_substantive_attempts':0,'audit_turns':0,'mathematical_proof_or_priority_certified_by_data_comparison':False}
with (D/'ROOT_RAW_SQL_AUDIT.json').open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert Path(__file__).read_bytes()==source
print(json.dumps({'status':obj['status'],'actual_pid':os.getpid(),'whole_raw_and_prior_bytes':obj['whole_raw_and_prior_bytes'],'SQL_rows':15458,'prior_raw_key_present':prior_present,'retrieved_raw_null_prior':obj['retrieved_raw_null_prior'],'selected_source_record_sha256':sha(original),'result':pin(D/'ROOT_RAW_SQL_AUDIT.json')}))
