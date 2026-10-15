"""ROOT complete raw/SQL importer reconstruction in place; no foreign-body copy."""
from pathlib import Path
import collections,datetime as dt,hashlib,json,os,sqlite3,stat,sys
A=Path(__file__).absolute().parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate key')
        d[k]=v
    return d
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(x,y):
    if type(x) is not type(y):return False
    if type(x) is dict:return x.keys()==y.keys() and all(equal(x[k],y[k]) for k in x)
    if type(x) is list:return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
    return x==y
def read(p):
    assert p.is_file() and not p.is_symlink() and not any(q.is_symlink() for q in p.parents)
    return p.read_bytes()
def row(p):
    b=read(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
assert __debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=read(Path(__file__));cache=R/'unsolved_math_prioritization/cache'
before=[row(cache/n) for n in ['problems.json','research_results.json','catalog.sqlite']]
rb=read(cache/'problems.json');pb=read(cache/'research_results.json');raw=parse(rb);prior=parse(pb)
assert len(rb)+len(pb)==149266659 and len(raw)==15458 and len(prior)==6701
byid={str(z['id']):z for z in raw};assert len(byid)==15458
codes=collections.Counter(z['problem_number'] for z in raw)
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
conn.execute('PRAGMA query_only=ON');assert conn.execute('PRAGMA query_only').fetchone()==(1,)
rows=[];seen=set();selected_sql=None
for key,payload,report in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
    assert key not in seen;seen.add(key)
    expected=dict(byid[key]);code=expected['problem_number'];ambiguous=codes[code]>1 and code in prior
    if ambiguous:expected['_ambiguous_report']=True
    expected_prior={} if ambiguous else prior.get(code,{})
    assert payload==json.dumps(expected) and report==json.dumps(expected_prior),key
    assert equal(parse(payload),expected) and equal(parse(report),expected_prior),key
    rows.append(dict(key=key,payload_sha256=sha(payload.encode()),report_sha256=sha(report.encode()),literal_importer_payload_byte_equal=True,literal_importer_report_byte_equal=True,complete_payload_recursive_type_equal=True,complete_report_recursive_type_equal=True,prior_key_present=code in prior,ambiguous_code=ambiguous))
    if key=='30000703':selected_sql=(payload,report)
metadata=conn.execute('SELECT revision FROM metadata').fetchall();conn.close()
assert seen==set(byid) and len(rows)==15458
key='30000703';code='OWR-1460-009';actual=byid[key]
assert actual['problem_number']==code and code not in prior and type(actual['id']) is int
saved=read(A/'source_snapshot/source_record.json')
assert equal(parse(saved),actual) and saved==(json.dumps(actual,indent=2)+'\n').encode()
assert selected_sql[1]=='{}' and read(A/'source_snapshot/prior_report.json')==b'null\n'
original=parse(read(A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json'))
assert original['selected']['upstream_report_key_present'] is False and original['selected']['upstream_report_presence']=='ABSENT' and original['selected']['sqlite_report_literal']=='{}'
assert len(original['rows'])==15458
original_by_key={r['key']:r for r in original['rows']};assert len(original_by_key)==15458 and set(original_by_key)==seen
for x in rows:
    y=original_by_key[x['key']]
    assert x['key']==y['key'] and x['payload_sha256']==y['payload_utf8_sha256'] and x['report_sha256']==y['report_utf8_sha256']
assert [row(cache/n) for n in ['problems.json','research_results.json','catalog.sqlite']]==before
result=dict(schema='pr49-root-in-place-complete-raw-sql-audit/v1',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),status='PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE',inputs=before,metadata_revision_rows=metadata,full_raw_and_prior_bytes=len(rb)+len(pb),all_SQL_rows=len(rows),complete_row_bindings=rows,source_record_schema='plain_raw_problem_object',complete_saved_source_equals_raw_selected=True,complete_saved_source_byte_exact_default_pretty_JSON=True,selected_prior_key_present=False,selected_prior_fallback={},raw_null_present=False,SQLite_literal_fallback='{}',literal_original_prior_file_value=None,literal_original_prior_differs_from_upstream_absent_fallback=True,original_source_binding=row(A/'source_snapshot/source_record.json'),original_prior_marker_binding=row(A/'source_snapshot/prior_report.json'),original_preparer_full_raw_certificate_binding=row(A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json'),all_preparer_row_hashes_independently_match=True,raw_or_SQL_or_foreign_source_bodies_copied=False,new_substantive_attempts=0,audit_turns=0,future_acceptance_approved=False)
result['retained_initial_ROOT_raw_inspection_failure']={'actual_pid':60964,'reason':'ROOT comparison assumed generic hash keys instead of original payload_utf8_sha256/report_utf8_sha256; distinct V2 preserves actual schema.','actual_capture':row(A.parent/'pr45_9900007/root_pr49_full_raw_SQL_actual_capture/CAPTURE.json'),'full_stderr':row(A.parent/'pr45_9900007/root_pr49_full_raw_SQL_actual_capture/stderr.bin'),'source':row(A/'ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py'),'distinct_corrected_version':True}
result['retained_second_ROOT_raw_inspection_failure']={'actual_pid':61299,'reason':'Original complete row certificate is in raw input order; ROOT SQL reads lexical key order. Distinct V3 compares exact unique key sets and each full row witness by key, retaining both failed inspectors.','actual_capture':row(A.parent/'pr45_9900007/root_pr49_full_raw_SQL_v2_actual_capture/CAPTURE.json'),'full_stderr':row(A.parent/'pr45_9900007/root_pr49_full_raw_SQL_v2_actual_capture/stderr.bin'),'source':row(A/'ROOT_RAW_AUDIT_V2_PRELAUNCH_SOURCE.py'),'distinct_corrected_version':True}
with (A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert read(Path(__file__))==source
print(json.dumps(dict(status=result['status'],actual_pid=os.getpid(),raw_bytes=len(rb)+len(pb),SQL_rows=len(rows),selected_report_key_absent=True,literal_fallback='{}',literal_original_marker='null',future_acceptance_approved=False)))
