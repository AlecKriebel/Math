"""Independent read-only full raw/SQL reproduction with metadata-only output."""
from pathlib import Path
import collections,datetime,hashlib,json,os,sqlite3,stat
F=Path(__file__).resolve().parent;A=F.parent;R=Path('/Users/alec/Documents/Math');U=R/'unsolved_math_prioritization'
def sha(b):return hashlib.sha256(b).hexdigest()
def read_bound(f):
 before=f.stat();b=f.read_bytes();after=f.stat()
 assert not f.is_symlink() and stat.S_ISREG(before.st_mode)
 assert (before.st_mode,before.st_mtime_ns,before.st_size)==(after.st_mode,after.st_mtime_ns,after.st_size)
 return b,{'path':str(f.relative_to(R)),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(before.st_mode),'mtime_ns':before.st_mtime_ns,'body_read_in_full':True,'body_copied':False}
def typed(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(typed(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
p,pb=read_bound(U/'cache/problems.json');q,qb=read_bound(U/'cache/research_results.json');d,db=read_bound(U/'cache/catalog.sqlite');im,imb=read_bound(U/'queue.py')
assert imb['sha256']=='f72aee023f837bad092da58531c2cc069ce2cf094e835d090221107d20f07ab2'
problems=json.loads(p);reports=json.loads(q)
assert type(problems) is list and type(reports) is dict and len(problems)==15458
keys=[str(v['id']) for v in problems];assert len(set(keys))==len(keys)
counts=collections.Counter(v['problem_number'] for v in problems)
c=sqlite3.connect((U/'cache/catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True);c.execute('PRAGMA query_only=ON')
sql=c.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();revision=c.execute('SELECT revision FROM metadata').fetchall();c.close()
assert len(sql)==15458 and set(v[0] for v in sql)==set(keys)
index={v[0]:v[1:] for v in sql};checks=[];selected=None
old=json.loads((A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes());old_rows={v['key']:v for v in old['rows']}
for raw in problems:
 v=dict(raw)
 if counts[v['problem_number']]>1 and v['problem_number'] in reports:v['_ambiguous_report']=True
 report={} if v.get('_ambiguous_report') else reports.get(v['problem_number'],{})
 key=str(v['id']);sp,sr=index[key]
 assert type(sp) is type(sr) is str and sp==json.dumps(v) and sr==json.dumps(report)
 assert typed(json.loads(sp),v) and typed(json.loads(sr),report)
 metadata={'key':key,'payload_utf8_bytes':len(sp.encode()),'payload_utf8_sha256':sha(sp.encode()),'report_utf8_bytes':len(sr.encode()),'report_utf8_sha256':sha(sr.encode()),'literal_importer_payload_equal':True,'literal_importer_report_equal':True,'recursive_scalar_types_equal':True}
 assert typed(metadata,old_rows[key]);checks.append(metadata)
 if key=='30000703':
  assert type(raw['id']) is int and raw['problem_number']=='OWR-1460-009' and raw['problem_number'] not in reports and sr=='{}'
  assert (json.dumps(raw,indent=2)+'\n').encode()==(A/'source_snapshot/source_record.json').read_bytes()
  assert (A/'source_snapshot/prior_report.json').read_bytes()==b'null\n'
  readiness=json.loads((A/'source_snapshot/readiness.json').read_bytes())
  review_hash=sha(json.dumps([v,report],sort_keys=True).encode());statement_hash=sha(v['statement'].encode())
  assert readiness['review_hash']==review_hash and readiness['statement_hash']==statement_hash
  selected={'key':key,'upstream_report_key_present':False,'upstream_report_presence':'ABSENT','sqlite_literal_report':'{}','original_prior_literal':'null\n','original_prior_is_literal_importer_fallback':False,'plain_source_byte_exact':True,'review_hash':review_hash,'statement_hash':statement_hash}
assert selected is not None
post,postb=read_bound(U/'cache/catalog.sqlite');assert post==d and postb==db
m=json.loads((U/'manifest.json').read_bytes());assert revision==[(m['revision'],)]
for n,b in [('problems.json',pb),('research_results.json',qb)]:assert m['files'][n]=={'bytes':b['bytes'],'sha256':b['sha256']}
res={'schema':'pr49-independent-boundary-full-raw-SQL-read/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'raw_inputs':[pb,qb],'sqlite_input':db,'importer_source':imb,'all_raw_records':len(problems),'all_SQL_rows':len(sql),'all_literal_serializations_and_recursive_types_verified':len(checks),'all_original_row_receipt_metadata_equal':True,'original_raw_receipt_sha256':sha((A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes()),'all_row_metadata_digest':sha(json.dumps(sorted(checks,key=lambda v:v['key']),sort_keys=True,separators=(',',':')).encode()),'selected':selected,'sqlite_pre_post_unchanged':True,'native_SQL_or_cache_writes':False,'foreign_payload_bodies_in_output':False,'future_acceptance_authority':False}
(F/'INDEPENDENT_RAW_READ.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'all_raw_records':len(problems),'all_SQL_rows':len(sql),'selected_report_presence':'ABSENT','native_writes':False,'future_authority':False},indent=2))
