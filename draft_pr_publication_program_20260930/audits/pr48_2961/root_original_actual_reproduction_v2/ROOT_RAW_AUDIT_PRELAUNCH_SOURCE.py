"""Full original importer reconstruction in place; no foreign raw/cache body copies."""
from pathlib import Path
import collections,datetime as dt,hashlib,json,os,sqlite3,sys
A=Path(__file__).absolute().parent;R=A.parents[2]
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(items):
 o={}
 for k,v in items:
  if k in o:raise ValueError('duplicate key')
  o[k]=v
 return o
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(x,y):
 if type(x) is not type(y):return False
 if type(x) is dict:return x.keys()==y.keys() and all(equal(x[k],y[k]) for k in x)
 if type(x) is list:return len(x)==len(y) and all(equal(a,b) for a,b in zip(x,y))
 return x==y
def read(p):
 assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
 return p.read_bytes()
def ref(p):
 b=read(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
assert __debug__ and not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=read(Path(__file__));cache=R/'unsolved_math_prioritization/cache'
rb=read(cache/'problems.json');pb=read(cache/'research_results.json');raw=parse(rb);prior=parse(pb)
assert len(rb)+len(pb)==149266659 and len(raw)==15458 and len(prior)==6701
byid={str(z['id']):z for z in raw};assert len(byid)==len(raw)
codes=collections.Counter(z['problem_number'] for z in raw)
conn=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True)
conn.execute('PRAGMA query_only=ON');assert conn.execute('PRAGMA query_only').fetchone()==(1,)
rows=[];seen=set();selected_sql={}
for key,payload,report in conn.execute('SELECT key,payload,report FROM records ORDER BY key'):
 assert key not in seen;seen.add(key)
 expected=dict(byid[key]);code=expected['problem_number'];ambiguous=codes[code]>1 and code in prior
 if ambiguous:expected['_ambiguous_report']=True
 expected_prior={} if ambiguous else prior.get(code,{})
 assert equal(parse(payload),expected) and equal(parse(report),expected_prior),key
 rows.append(dict(key=key,payload_sha256=sha(payload.encode()),report_sha256=sha(report.encode()),complete_payload_recursive_type_equal=True,complete_report_recursive_type_equal=True,prior_key_present=code in prior,ambiguous_code=ambiguous))
 if key in {'2961','30004403'}:selected_sql[key]=(payload,report)
conn.close();assert seen==set(byid) and len(rows)==15458
original_native=parse(read(A/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json'))
native={r['key']:r for r in original_native['selected']};assert set(native)=={'2961','30004403'}
selected=[]
for key,code,file in [('2961','KP-4.85','source_record.json'),('30004403','OWR-17471-009','related_source_record.json')]:
 actual=byid[key];assert actual['problem_number']==code and code not in prior
 saved=parse(read(A/'source_snapshot'/file));assert equal(saved,actual) and type(saved['id']) is int and str(saved['id'])==key
 n=native[key];assert n['upstream_report_key_present'] is False and n['upstream_report_presence']=='ABSENT' and n['complete_upstream_report'] is None
 assert equal(n['complete_selected_prior_SQLite'],{}) and n['sqlite_report_literal']=='{}' and n['original_prior_report_file_exists'] is False
 assert selected_sql[key][1]=='{}' and not (A/'source_snapshot/prior_report.json').exists()
 selected.append(dict(key=key,problem_code=code,original_plain_source=ref(A/'source_snapshot'/file),complete_saved_source_equals_raw_selected=True,raw_key_presence='ABSENT',raw_present_null=False,sqlite_literal_fallback='{}',SQLite_typed_fallback={},original_prior_report_file_exists=False,original_operational_prose_null_claim_requires_repair=True))
result=dict(schema='pr48-root-in-place-complete-raw-sql-audit/v1',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_pid=os.getpid(),status='PASS_FULL_RAW_PRIOR_SQL_AND_TWO_ORIGINAL_PLAIN_SOURCES',inputs=[ref(cache/n) for n in ['problems.json','research_results.json','catalog.sqlite']],full_raw_and_prior_bytes=len(rb)+len(pb),all_SQL_rows=len(rows),complete_row_bindings=rows,complete_selected_source_bindings=selected,original_native_selected_read_binding=ref(A/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json'),raw_or_SQL_or_foreign_source_bodies_copied=False,new_substantive_attempts=0,audit_turns=0,future_acceptance_approved=False)
with (A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json').open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert read(Path(__file__))==source
print(json.dumps(dict(status=result['status'],actual_pid=os.getpid(),raw_bytes=len(rb)+len(pb),SQL_rows=len(rows),two_raw_keys_absent=True,fallback='{}',future_acceptance_approved=False)))
