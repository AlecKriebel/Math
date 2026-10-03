#!/usr/bin/env python3
"""Independent literal/raw/SQLite comparison; source-only and read-only."""
from pathlib import Path
import datetime, hashlib, json, os, sqlite3
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]
PROGRAM=REPO/'unsolved_math_prioritization'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def h(p):
 b=p.read_bytes();return {'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
started=now()
raw=json.loads((PROGRAM/'cache/problems.json').read_text())
matching=[x for x in raw if type(x.get('id')) is int and x['id']==9700035]
assert len(matching)==1
record=matching[0]
report=json.loads((PROGRAM/'cache/research_results.json').read_text())[record['problem_number']]
manifest=json.loads((PROGRAM/'manifest.json').read_text())
conn=sqlite3.connect('file:'+str((PROGRAM/'cache/catalog.sqlite').resolve())+'?mode=ro&immutable=1',uri=True)
conn.execute('PRAGMA query_only=ON')
sql=conn.execute('SELECT key,payload,report FROM records WHERE key=?',('9700035',)).fetchall()
assert len(sql)==1 and sql[0][0]=='9700035'
sql_record=json.loads(sql[0][1]); sql_report=json.loads(sql[0][2])
assert sql_record==record and sql_report==report
assert conn.execute('PRAGMA query_only').fetchone()==(1,)
revision=conn.execute('SELECT * FROM metadata').fetchall()
assert revision==[(manifest['revision'],)]
cache_hashes={}
for name,info in manifest['files'].items():
 p=PROGRAM/'cache'/name; actual=h(p)
 assert actual['size']==info['bytes'] and actual['sha256']==info['sha256']
 cache_hashes[name]=actual
snapshot=ROOT.parent/'source_snapshot'
assert json.loads((snapshot/'source_record.json').read_text())==record
assert json.loads((snapshot/'prior_report.json').read_text())==report
(ROOT/'sources/raw_record_9700035.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
(ROOT/'sources/raw_prior_9700035.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(ROOT/'sources/sql_record_9700035.json').write_text(json.dumps(sql_record,indent=2,ensure_ascii=False)+'\n')
(ROOT/'sources/sql_prior_9700035.json').write_text(json.dumps(sql_report,indent=2,ensure_ascii=False)+'\n')
result={'started_utc':started,'completed_utc':now(),'pid':os.getpid(),'numeric_id':9700035,'problem_number':record['problem_number'],'cache_files':cache_hashes,'sqlite_file':h(PROGRAM/'cache/catalog.sqlite'),'manifest_file':h(PROGRAM/'manifest.json'),'sqlite_mode':'ro immutable=1 query_only=ON','sqlite_revision':revision[0][0],'typed_raw_record_count':len(matching),'raw_sql_record_exact_equal':sql_record==record,'raw_sql_prior_exact_equal':sql_report==report,'snapshot_record_exact_equal':True,'snapshot_prior_exact_equal':True,'cache_manifest_hashes_match':True}
(ROOT/'source_provenance_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
