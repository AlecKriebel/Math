from pathlib import Path
import json,hashlib,base64,stat
D=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr214_30005244/native_source_custody_01");P=D/'_private'
def native(k,b):return hashlib.sha1(k.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
inv=json.loads((D/'INVENTORY.json').read_bytes());br=json.loads((D/'BODY_RECORDS.json').read_bytes());ledger=json.loads((P/'API_LEDGER.json').read_bytes())
responses={}
for r in ledger:
 b=(P/r['raw_path']).read_bytes();assert pin(b)==r['stdout_pin'] and r['exit']==0 and r['method']=='GET' and r['hostname']=='github.com'
 responses.setdefault(r['route'],[]).append(json.loads(b))
treecount=0
for n in ['AUTHENTICATED_TREES.json','BODY_ADDITIONAL_TREES.json','SOURCE_DIRECTORY_TREES.json']:
 p=D/n
 if not p.exists():continue
 for oid,rows in json.loads(p.read_bytes()).items():
  ordered=sorted(rows,key=lambda s:s.encode()+(b'/' if rows[s]['type']=='tree' else b''))
  raw=b''.join(rows[s]['mode'].lstrip('0').encode()+b' '+s.encode()+b'\0'+bytes.fromhex(rows[s]['sha']) for s in ordered)
  assert native('tree',raw)==oid
  rr=responses['git/trees/'+oid][0];assert rr['sha']==oid and rr['truncated'] is False and {r['path']:{k:r[k] for k in ('mode','type','sha')} for r in rr['tree']}==rows
  treecount+=1
for name in ['original','current']:
 x=inv[name];oid=x['commit']['sha'];b=(P/'native_commits'/(oid+'.commit')).read_bytes();assert native('commit',b)==oid and pin(b)==x['commit']['raw_commit_pin']
 for path,row in x['instructions'].items():
  b=(P/'reading'/name/path).read_bytes();assert native('blob',b)==row['sha'] and pin(b)=={k:row[k] for k in ('bytes','sha256')}
 row=x['queue'];b=(P/'reading'/name/'unsolved_math_prioritization/QUEUE.md').read_bytes();assert native('blob',b)==row['sha'] and pin(b)=={k:row[k] for k in ('bytes','sha256')}
 assert row['status']=='claimed_solved'
for r in br['records']:
 p=D/r['reading_copy'];b=p.read_bytes();assert stat.S_IMODE(p.stat().st_mode)==0o444 and native('blob',b)==r['sha'] and pin(b)=={k:r[k] for k in ('bytes','sha256')}
 rr=responses['git/blobs/'+r['sha']][0];assert rr['sha']==r['sha'] and rr['encoding']=='base64' and type(rr['size']) is int and rr['size']==len(b) and base64.b64decode(''.join(rr['content'].split()),validate=True)==b
assert br['original_count']==31 and br['current_count']==41 and br['all_original31_preserved_exact_in_current'] is True
assert len(br['original31_current_archival_comparisons'])==31 and all(r['exact_mode_type_native_body'] is True for r in br['original31_current_archival_comparisons'])
print(json.dumps({'all_checked':True,'tree_object_checks_including_repeated_pins':treecount,'native_GET_responses':len(ledger),'own_and_applicable_readme_bodies':len(br['records']),'original_files':31,'current_files':41,'all31_preserved':True,'original_status':inv['original']['queue']['status'],'current_status':inv['current']['queue']['status'],'current_effort':inv['current']['queue']['effort'],'BODY_RECORDS_pin':pin((D/'BODY_RECORDS.json').read_bytes()),'INVENTORY_pin':pin((D/'INVENTORY.json').read_bytes())},sort_keys=True))
