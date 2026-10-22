#!/usr/bin/env python3
"""Independently bind/read-only-compare one captured instance; no service/project imports."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
FRESH=HERE.parent/'root/private/manual_instance_1c68c409f7fc4d2b96b4ce8754c92d74'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
private=HERE/'private/fresh_capture';private.mkdir(mode=0o700,exist_ok=True)
pins=[];data={}
for name in ['account.json','ledger.json','public_record.json','pr.json','sheet_identity.json','doi_resolution.json','READ_ONLY_INSTANCE_GATE.json','EXACT_DIFFERENCES.json']:
 p=FRESH/name;b=p.read_bytes();q=private/name
 if q.exists():require(q.read_bytes()==b,'Fresh capture changed: '+name)
 else:q.write_bytes(b);q.chmod(0o400)
 pins.append({'original':str(p),'snapshot':str(q.relative_to(HERE)),'bytes':len(b),'sha256':sha(b)});data[name]=json.loads(b)
source=json.loads((HERE/'SOURCE_PINS.json').read_text())['files'];lookup={Path(e['original']).name:e for e in source}
old=json.loads((HERE/lookup['account.json']['snapshot']).read_bytes());oldrows=json.loads((HERE/lookup['ledger_live.json']['snapshot']).read_bytes())['response']['values'];plan=json.loads((HERE/lookup['LEDGER_RECONCILIATION_PLAN.json']['snapshot']).read_bytes());baseline=json.loads((HERE/lookup['zenodo_23350364.json']['snapshot']).read_bytes())
new=data['account.json'];oldby={r['id']:r for r in old['records']};newby={r['id']:r for r in new['records']}
require(old['total']==new['total']==197 and len(oldby)==len(newby)==197 and set(oldby)==set(newby),'Account inventory changed')
changes=[]
def compare(a,b,path):
 require(type(a) is type(b),'Value type changed at '+path)
 if isinstance(a,dict):
  require(a.keys()==b.keys(),'Keyset changed at '+path)
  for k in a:compare(a[k],b[k],path+'.'+k)
 elif isinstance(a,list):
  require(len(a)==len(b),'List length changed at '+path)
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'['+str(i)+']')
 elif a!=b:changes.append({'path':path,'old':a,'new':b,'type':type(a).__name__})
for i in sorted(oldby):compare(oldby[i],newby[i],'record['+str(i)+']')
allowed={'downloads','unique_downloads','version_downloads','version_unique_downloads','views','unique_views','version_views','version_unique_views'}
require(len(changes)==152,'Unexpected delta count')
for e in changes:
 m=re.fullmatch(r'record\[([1-9][0-9]*)\]\.stats\.([a-z_]+)',e['path'])
 require(m is not None and m.group(2) in allowed and type(e['old']) is int and type(e['new']) is int and e['old']>=0 and e['new']>=0,'Non-usage delta at '+e['path'])
rows=data['ledger.json']['values'];require(rows==oldrows and len(rows)==181,'Ledger rows differ')
require(data['ledger.json']['majorDimension']=='ROWS' and data['ledger.json']['range'].startswith("'Math Puzzles'!A1:AQ"),'Ledger range changed')
require(rows[0]==plan['schema_columns'],'Ledger header changed')
r=data['public_record.json'];require(r['state']=='done' and r['submitted'] is True and r['id']==23350364 and r['doi']=='10.5281/zenodo.23350364' and str(r['conceptrecid'])=='23350363','Published identity changed');require(r['metadata']==baseline['metadata'],'Provider metadata differs')
filemap=lambda record:{f['key']:(f['size'],f['checksum']) for f in record['files']}
require(len(r['files'])==3 and filemap(r)==filemap(baseline),'Provider file inventory changed')
pr=data['pr.json'];require(pr['head']['sha']==plan['head'] and pr['base']['sha']==plan['base'] and sha(pr['body'].encode())==plan['body_sha256'],'PR immutable binding differs')
require(pr['state']=='open' and pr['draft'] is True and pr['merged'] is False,'PR state differs')
s=data['sheet_identity.json'];require(s['spreadsheetId']==plan['spreadsheet_id'] and [x['properties']['title'] for x in s['sheets'] if x['properties']['sheetId']==1254632077]==['Math Puzzles'],'Sheet identity differs')
require(data['doi_resolution.json']=={'status':200,'final_url':'https://zenodo.org/records/23350364'},'DOI destination differs')
# Every other original leaf/key/list position was recursively compared, so all
# metadata, files, pids, parent identities, URLs, strings and other stats agree.
for p in pins:require(Path(p['original']).read_bytes()==(HERE/p['snapshot']).read_bytes(),'Capture changed during comparison')
result={'read_only':True,'fresh_capture_pins':pins,'old_account_sha256':lookup['account.json']['sha256'],'old_ledger_capture_sha256':lookup['ledger_live.json']['sha256'],'records':197,'record_ids_identical':True,'ledger_rows_identical':181,'whole_records_identical':False,'changed_records':sorted({int(re.match(r'record\[([0-9]+)\]',e['path']).group(1)) for e in changes}),'exact_changed_leaves':changes,'changed_leaf_count':len(changes),'only_exact_eight_nonnegative_integer_stats_counters_changed':True,'all_other_fields_keysets_types_lists_values_equal':True,'identity_text_and_metadata_files_pids_parent_links_unchanged':True,'applicability':'Preserved-instance identity adjudication transfers to this exact read-only fresh capture because every identity-bearing field and every original string/key is unchanged. Usage counters are not identity evidence. No approval of generic v8 or mutation authorization.','fresh_payload_byte_verification':'Root receipt reports3 fresh payload SHA256/MD5 checks; payload bytes are not present in this capture, so this comparison independently checks the public file inventory and metadata, not a fresh re-download.'}
(HERE/'FRESH_INSTANCE_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['fresh_capture_pins','exact_changed_leaves']},indent=2))
