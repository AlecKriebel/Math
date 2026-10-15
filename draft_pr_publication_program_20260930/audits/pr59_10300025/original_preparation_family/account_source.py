#!/usr/bin/env python3
"""Read selected original corpus/SQL records in place; no catalog writes."""
import datetime, hashlib, json, os, pathlib, sqlite3
root=pathlib.Path(__file__).resolve().parent
cache=pathlib.Path('/Users/alec/Documents/Math/unsolved_math_prioritization/cache')
sha=lambda b:hashlib.sha256(b).hexdigest()
def descriptor(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    s=p.stat()
    return {'path':str(p),'bytes':s.st_size,'sha256':h.hexdigest(),'mode_07777':oct(s.st_mode&0o7777)}
problems=json.loads((cache/'problems.json').read_bytes())
reports=json.loads((cache/'research_results.json').read_bytes())
assert type(problems) is list and type(reports) is dict
selected=[x for x in problems if x.get('id')==10300025]
assert len(selected)==1 and type(selected[0]) is dict
record=selected[0]; report=reports['AMR-102-0025']; assert type(report) is dict
assert json.loads((root/'original/source_record.json').read_bytes())==record
assert json.loads((root/'original/prior_report.json').read_bytes())==report
db=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
revision=db.execute('SELECT revision FROM metadata').fetchall()
sql=db.execute('SELECT key,payload,report,typeof(payload),typeof(report) FROM records WHERE key=?',('10300025',)).fetchall()
assert len(sql)==1
key,payload,sql_report,payload_type,report_type=sql[0]
assert payload_type==report_type=='text' and sql_report is not None
assert json.loads(payload)==record and json.loads(sql_report)==report
assert revision==[('37e53eabe540fb458758e198be61634bd02ee008',)]
db.close()
attempt=json.loads((root/'original/attempt.json').read_bytes()); turns=json.loads((root/'original/turns.json').read_bytes())
assert attempt['substantive_attempts_used']==1 and attempt['substantive_attempt_limit']==5
assert type(turns) is list and len(turns)==1 and turns[0]['turn']==1 and turns[0]['discovery_credit'] is False
out={'operator':'SOURCE subagent /root/algebra_reproduction_audit','pid':os.getpid(),
     'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dataset_revision':revision[0][0],
     'raw_corpora':[descriptor(cache/n) for n in ('problems.json','research_results.json','catalog.sqlite')],
     'selected':{'problem_id':10300025,'problem_code':'AMR-102-0025',
       'problems_container_type':'JSON array','unique_problem_type':'JSON object',
       'research_results_container_type':'JSON object','selected_report_key_present':True,
       'selected_report_type':'JSON object','source_record_shape':'unwrapped JSON object',
       'research_result_for_code_wrapper_field_present':False,
       'prior_report_type':'JSON object','sql_key':key,'sql_payload_storage_type':payload_type,
       'sql_report_storage_type':report_type,'sql_report_is_NULL':False,
       'sql_payload_utf8':{'bytes':len(payload.encode()),'sha256':sha(payload.encode())},
       'sql_report_utf8':{'bytes':len(sql_report.encode()),'sha256':sha(sql_report.encode())},
       'selected_problem_semantic_equality':True,'selected_report_semantic_equality':True},
     'original_budget':{'used':1,'limit':5,'turn_records':len(turns),'classification':attempt['status'],
       'turn_discovery_credit':turns[0]['discovery_credit'],'novel_result_claimed':attempt['novel_result_claimed']},
     'new_SOURCE_turns':0,'new_discovery_credit':0,'mathematical_pass_assigned':False}
(root/'SOURCE_ACCOUNTING.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(out,ensure_ascii=False))
