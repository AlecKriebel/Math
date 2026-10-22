import datetime,hashlib,json,pathlib
ROOT=pathlib.Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr952_10400145';R=A/'reviews/full_package_02';D=A/'preprint'
def sha(b):return hashlib.sha256(b).hexdigest()
f=json.loads((D/'FREEZE.json').read_bytes()); reports=[]
specs=[(ROOT/v['manifest_path'],v['manifest_sha256'],None) for v in f['family_authentication'].values()]
for name,candidate in [('operations_engineering_01','candidate01'),('operations_engineering_02','candidate02'),('operations_engineering_03',None),('package_engineering_01',None),('reviews/full_package_01',None)]:
 p=A/name/'MANIFEST.json';key=str(p.relative_to(ROOT));pin=f['evidence_files'].get(key,{}).get('sha256')
 if name=='reviews/full_package_01':assert pin=='c17f8f4c8812685a2b4a6442695ad99d84359750ab8a13467a21d71d8244e9d9'
 assert pin,key
 specs.append((p,pin,candidate))
for p,pin,candidate in specs:
 assert sha(p.read_bytes())==pin
 m=json.loads(p.read_bytes());base=ROOT if m.get('path_base')=='repository_root' else p.parent
 members=m.get('files',m.get('payloads',m.get('public_payloads')))
 if isinstance(members,list): members={e['path']:e for e in members}
 if isinstance(m.get('explicit_public_allowlist'),list):assert set(m['explicit_public_allowlist'])==set(members) and len(m['explicit_public_allowlist'])==len(members)
 observed={}
 for path,rec in members.items():
  q=base/path;historical=False
  if candidate and path in json.loads((D/'reviewed_candidates'/candidate/'OPERATIONS_INVENTORY.json').read_bytes())['files']:
   q=D/'reviewed_candidates'/candidate/'operations'/path;historical=True
  b=q.read_bytes(); assert sha(b)==rec['sha256'] and len(b)==rec['bytes'],str(q)
  observed[path]={'bytes':len(b),'sha256':sha(b),'read_path':str(q.relative_to(ROOT)),'historical_snapshot':historical}
 reports.append({'manifest':str(p.relative_to(ROOT)),'manifest_sha256':pin,'members':observed})
(R/'SEALED_INTAKE_AUTHENTICATION.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z'),'seals':reports},indent=2)+'\n')
print('SEALED_ALLOWLISTS_AUTHENTICATED',len(reports))
