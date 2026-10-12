"""Read-only typed source/accounting checks, no historical checker imports.

Reads in-place original/preparer references and raw JSON/immutable SQL. Does
not alter native files or copy whole corpora into this family. Stdout only.
"""
import hashlib
import json
import os
from pathlib import Path
import sqlite3

family=Path(__file__).resolve().parent
preparer=family.parent/'original_preparation_family'
auth=json.loads((preparer/'ORIGINAL_AUTHENTICATION.json').read_text())
account=json.loads((preparer/'SOURCE_ACCOUNTING.json').read_text())
head='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
assert auth['original_head']==head==account['original_head']
original=json.loads((preparer/'original/source_record.json').read_text())
source_bodies=[]
for desc in auth['original_science_files']:
    path=Path(desc['local_path']); body=path.read_bytes()
    assert len(body)==desc['bytes']
    assert hashlib.sha256(body).hexdigest()==desc['sha256']
    assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==desc['git_blob_sha1']
    source_bodies.append({'path':str(path),'bytes':len(body),'sha256':desc['sha256'],'full_mode':oct(path.stat().st_mode & 0o7777),'semantically_read':desc['relative_path'] in ['source_record.json','CANDIDATE.md','verify.py','turns.json']})
refs={}
for name,desc in account['raw_corpus_references'].items():
    path=Path(desc['path']); body=path.read_bytes()
    assert len(body)==desc['bytes'] and hashlib.sha256(body).hexdigest()==desc['sha256']
    refs[name]={'path':str(path),'bytes':len(body),'sha256':desc['sha256']}
    if name=='problems.json':
        problems=json.loads(body)
    else:
        reports=json.loads(body)
matches=[p for p in problems if str(p['id'])=='30003354' or p['problem_number']=='OWR-15208-008']
assert len(matches)==1 and matches[0]==original
raw_presence={k:k in reports for k in ['30003354','OWR-15208-008']}
assert not any(raw_presence.values()) and account['raw_report_key_present'] is False
db=sqlite3.connect('file:'+account['SQL_database_reference']['path']+'?mode=ro&immutable=1',uri=True)
row=db.execute('SELECT payload,report,typeof(report) FROM records WHERE key=?',('30003354',)).fetchone()
assert row is not None and json.loads(row[0])==original
assert row[1]=='{}' and row[2]=='text' and row[1] is not None
turns=json.loads((preparer/'original/turns.json').read_text())
assert turns['budget']==5 and turns['substantive_proof_attempts']==1
assert not (preparer/'original/status.json').exists()
assert account['original_turn_limit']==5 and account['original_turns_used']==1
wrapper_prior={k:k in original for k in ['upstream_report','research_result','report']}
assert not any(wrapper_prior.values())
print(json.dumps({'schema':'pr57-independent-source-controls/v1','process_pid':os.getpid(),'original_head':head,'authenticated_science_body_count':len(source_bodies),'source_bodies':source_bodies,'raw_corpus_references':refs,'numeric_or_source_code_problem_matches':len(matches),'selected_problem_typed_equal_to_original_and_SQL':True,'raw_report_key_presence':raw_presence,'raw_report_value':'ABSENT: no raw value','SQL_report_is_NULL':False,'SQL_report_type':row[2],'SQL_report_literal':row[1],'original_wrapper_prior_field_presence':wrapper_prior,'original_status_file_present':False,'original_turns_used':1,'original_turn_limit':5,'historical_checker_imports':False,'native_mutation':False},indent=2,sort_keys=True))
