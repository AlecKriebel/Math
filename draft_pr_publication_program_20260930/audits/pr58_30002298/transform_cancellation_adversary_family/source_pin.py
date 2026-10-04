"""Read-only, dated byte/source/budget pins. No reviewer code imports."""
import datetime,hashlib,json,os,sqlite3
from pathlib import Path

base=Path(__file__).resolve().parent; prep=base.parent/'original_preparation_family'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
auth=json.loads((prep/'ORIGINAL_AUTHENTICATION.json').read_text())
account=json.loads((prep/'SOURCE_ACCOUNTING.json').read_text())
head='465d771ec1ddc91877e8d9db51ed59aea1b0d97d'
assert auth['original_head']==head==account['original_head']
entries=[]
for d in auth['original_science_files']:
    p=Path(d['local_path']); b=p.read_bytes()
    assert len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['git_blob_sha1']
    entries.append({'name':d['relative_path'],'path':str(p),'bytes':len(b),'sha256':d['sha256'],'observed_mode_07777':format(p.stat().st_mode&0o7777,'04o'),'observation_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'semantically_read':d['relative_path'] in ['SOURCE_STATUS.md','source_record.json','check_denominators.py']})
wrapper=json.loads((prep/'original/source_record.json').read_text())
raw={}; hashes=[]
for name,d in account['raw_corpus_references'].items():
    p=Path(d['path']); b=p.read_bytes()
    assert hashlib.sha256(b).hexdigest()==d['sha256'] and len(b)==d['bytes']
    raw[name]=json.loads(b); hashes.append({'name':name,'path':str(p),'sha256':d['sha256'],'bytes':len(b)})
selected=[p for p in raw['problems.json'] if str(p['id'])=='30002298' or p['problem_number']=='OWR-12339-004']
assert len(selected)==1 and selected[0]==wrapper['record']
assert not any(k in raw['research_results.json'] for k in ['30002298','OWR-12339-004'])
assert 'research_result_for_code' in wrapper and wrapper['research_result_for_code'] is None
db=sqlite3.connect('file:'+account['SQL_database_reference']['path']+'?mode=ro&immutable=1',uri=True)
payload,report,kind=db.execute('SELECT payload,report,typeof(report) FROM records WHERE key=?',('30002298',)).fetchone()
assert json.loads(payload)==wrapper['record'] and report=='{}' and kind=='text'
assert account['original_used_substantive_attempts']==0 and account['original_maximum_substantive_attempts']==5
assert account['original_turn_log_entries']==[] and account['original_readiness_status_literal']=='already_solved'
finish=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps({'schema':'pr58-transform-dated-source-pins/v1','operator':'transform_cancellation_adversary','process_pid':os.getpid(),'started_utc':start,'finished_utc':finish,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'original_head':head,'actual_merge_base':auth['actual_merge_base_oid'],'GH_api_base':auth['github_base_oid'],'original_science_body_count':len(entries),'entries':entries,'raw_body_references':hashes,'selected_record_typed_equal_to_raw_and_SQL':True,'raw_report':'ABSENT: no raw value','wrapper_research_result_field_present':True,'wrapper_research_result_literal':None,'SQL_report_is_NULL':False,'SQL_report_literal':report,'SQL_report_type':kind,'original_substantive_attempts':0,'original_maximum_attempts':5,'original_recommended_status':'already_solved','original_turn_log_entries':[],'external_modes_are_dated_observations_not_final_freeze_claims':True,'source_preparation_or_ROOT_acceptance_credit':False,'native_mutation':False},indent=2,sort_keys=True))
