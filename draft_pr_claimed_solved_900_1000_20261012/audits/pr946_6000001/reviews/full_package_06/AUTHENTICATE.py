import sys,os,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
assert sys.flags.isolated and sys.flags.optimize==0
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_06'
for k,v in {'GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'gc.auto','GIT_CONFIG_VALUE_0':'0','PYTHONDONTWRITEBYTECODE':'1'}.items():os.environ[k]=v
fp='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1';ip='f4742eca6ddd628ecac1e704fed772a17837d42d4d0fdef42c73d3cda3bed254'
s=(P/'accept_pr946.py').read_bytes();assert hashlib.sha256(s).hexdigest()=='8e1a0d7b3ca6e5d72e76415541b393fbfbe52e307368bc86b9e7982d5be27cd7'
assert hashlib.sha256((A/'OPERATIONS_INVENTORY.json').read_bytes()).hexdigest()==ip
assert hashlib.sha256((D/'FREEZE.json').read_bytes()).hexdigest()==fp
ns={'__file__':str(P/'accept_pr946.py'),'__name__':'authenticated_read_only_review06'};exec(compile(s,str(P/'accept_pr946.py'),'exec'),ns)
c=ns['capture_inventory'](ip);f=ns['freeze_check'](ns['read_regular'](D/'FREEZE.json'),fp,c)
pr,parent,source,orig=ns['premerge_gate'](f,require_draft=True);built=ns['archive_check'](f,orig)
# Authenticate actual source cache without importing or changing the catalog.
import sqlite3
cache=R/'unsolved_math_prioritization/cache/catalog.sqlite'
con=sqlite3.connect('file:'+str(cache)+'?mode=ro',uri=True)
tables=con.execute("select name from sqlite_master where type='table'").fetchall();cache_check={'tables':[x[0] for x in tables]}
for (table,) in tables:
 cols=[x[1] for x in con.execute('pragma table_info("'+table.replace('"','""')+'")')]
 if 'id' in cols and 'statement' in cols:
  row=con.execute('select statement from "'+table.replace('"','""')+'" where id=?',(6000001,)).fetchone()
  if row:cache_check.update(statement_sha256=hashlib.sha256(row[0].encode()).hexdigest(),table=table)
record=con.execute('select payload,report from records where key=?',('6000001',)).fetchone()
if record:
 payload=json.loads(record[0]);statement=payload.get('statement',payload.get('problem',{}).get('statement'));cache_check.update(statement_sha256=hashlib.sha256(statement.encode()).hexdigest(),table='records',key='6000001')
if record:
 pair=[json.loads(record[0]),json.loads(record[1])];reviewhash=hashlib.sha256(json.dumps(pair,sort_keys=True).encode()).hexdigest();assert reviewhash==ns['REVIEW'];cache_check['review_sha256']=reviewhash
con.close()
assert cache_check.get('statement_sha256')==ns['STATEMENT'],cache_check
row=ns['claimed_row'](ns['blob'](ns['HEAD'],ns['QUEUE']));assert hashlib.sha256(row.rstrip(b'\n')).hexdigest()=='11fbd85ea991520337b918a2caa719737acff2d202c796aa93e3343c61403895'
for item in orig.values():item.update(archive_mode='100644',disk_and_archive_match=True)
receipt={'status':'PASS','utc':ns['utc_now'](),'original_pr_head':ns['HEAD'],'freeze_sha256':fp,'package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],'candidate_files':f['files'],'payloads':built['payload_files'],'archive_members':built['zip_members'],'originals':orig,'remote_main':parent,'actual_pr':pr,'source_gate':source,'evidence_files':f['evidence_files'],'dependencies':c['inventory']['files'],'cached_statement':cache_check,'head_claimed_row_no_lf_sha256':hashlib.sha256(row.rstrip(b'\n')).hexdigest(),'git_config':'process gc.auto=0; no refs/FETCH_HEAD/index/HEAD mutation','isolated_optimization':sys.flags.optimize}
ns['authentication_schema'](receipt)
label=sys.argv[1];assert label in ['START','END']
(O/('AUTHENTICATION_'+label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','utc':receipt['utc'],'fresh_main':parent,'candidate_files':len(f['files']),'evidence_files':len(f['evidence_files']),'dependencies':len(c['inventory']['files']),'originals':len(orig),'archive_members':built['zip_members'],'payloads':built['payload_files'],'cache':cache_check}))
