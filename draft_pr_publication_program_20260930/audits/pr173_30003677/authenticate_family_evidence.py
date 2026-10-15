#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,stat,datetime
A=Path(__file__).resolve().parent
def need(c,s):
 if not c: raise RuntimeError(s)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(p): return {'bytes':p.stat().st_size,'sha256':digest(p),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
specs=[
('branching_local_adversary','MANIFEST.json','cff8f99adfdbbe84c4e1bdbee26ccc2a53b6f591e5c1793d9750a3557054cbcc','files',24,{'first_seal/SHA256SUMS.sha256':'1fe89d5fcc443bf16e000a2829714d36595cc847b2203c19f935a6b1290a7749'},'public_allowlist.json','allowlisted_relative_paths'),
('literal_model_scope_adversary','final0444_manifest.json','6688f4022bea9bdca2b954770239a635d8a32291d990f8ffc434df01a8298a9a','file_inventory_recursive',43,{'first0444_manifest.json':'a1301be315cdc989784955d077d47279bcca09f046865987c1a27670803862f9'},'public/public_allowlist.json','explicit_public_allowlist'),
('path_diagonal_adversary','INVENTORY.json','cf31e52e28e50bd5070a336d899ce4e1b18604bfd48dea862dbe85e0dc307999','files',92,{'FINAL_SEAL.json':'55b15487fa6e60b2011ba52cff22cd4ba46c580a947f84342e1f999d04c270f3','FIRST_SEAL.json':'32f1d3c4539a650c3cfb90960479e94544b60a58092a62eba5579806d0b439c4'},'PUBLIC_ALLOWLIST.json',None),
('path_diagonal_adversary_public_support','INVENTORY.json','4b0929add1452af0805d95b7b0a92ee02086a3187ed4e5aed5f271b131177869','files',13,{'EXPORT_SEAL.json':'d672a2053f6bf014e5c772aedeb40c03de4e6a5e4ec28f6543b3b0801dbe07b7'},'PUBLIC_ALLOWLIST.json',None)]
records=[]
for name,mf,expected,key,count,external,allowf,allowkey in specs:
 root=A/name;need(digest(root/mf)==expected,'manifest digest '+name)
 d=json.loads((root/mf).read_text()); rows=d[key]; listed=set()
 allfiles={str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file()}
 need(len(allfiles)==count,'retained count '+name)
 for e in rows:
  p=e['path']; need(p not in listed,'duplicate '+p);listed.add(p)
  need(not Path(p).is_absolute() and '..' not in Path(p).parts,'unsafe '+p)
  need(p in allfiles and not allfiles[p].is_symlink(),'missing/symlink '+p)
  act=ident(allfiles[p]);need(act['mode']=='0444','unsealed '+p)
  need(act['bytes']==e['bytes'],'bytes '+p)
  if e.get('sha256'):need(act['sha256']==e['sha256'],'sha '+p)
  else: need(p in {mf,*external},'unhashed non-manifest '+p)
 need(set(allfiles)==listed|{mf},'membership mismatch '+name)
 need(ident(root/mf)['mode']=='0444','manifest unsealed')
 for p,h in external.items():need(digest(root/p)==h,'external seal '+p)
 al=json.loads((root/allowf).read_text())
 if allowkey: allow=al[allowkey]
 else:
  choices=[v for k,v in al.items() if isinstance(v,list) and all(isinstance(x,str) for x in v)]
  need(len(choices)==1,'unknown allowlist schema '+name);allow=choices[0]
 need(len(set(allow))==len(allow) and set(allow)<=set(allfiles),'allow membership')
 need(all(not p.startswith(('private/','private_sources/','raw_runs/')) for p in allow),'private public')
 # Verify all first-seal manifest member pins as well, not only final membership.
 if name=='branching_local_adversary':
  for line in (root/'first_seal/SHA256SUMS.sha256').read_text().splitlines():
   h,p=line.split(None,1);p=p.strip().lstrip('*');need(digest(root/'first_seal'/p)==h,'first '+p)
 if name=='literal_model_scope_adversary':
  f=json.loads((root/'first0444_manifest.json').read_text())
  for e in f['file_inventory_recursive']:
   need(ident(root/e['path'])['sha256']==e['sha256'],'first '+e['path'])
 records.append({'family':name,'all_retained_files_authenticated':len(allfiles),'manifest':ident(root/mf),'external_pins':external,'public_allowlist':allow,'all_files_0444':True})
prep=A/'MATHEMATICAL_REPAIR_PREPARATION.json'
rr=json.loads((A/'ROOT_REPAIRED_CHECKERS_REPRODUCTION.json').read_text())
need(ident(prep)['sha256']==rr['repair_preparation']['sha256'],'repair prep')
for p,e in rr['candidate_files'].items():
 i=ident(A/'repaired_candidate_v1'/p);need(i['sha256']==e['sha256'] and i['bytes']==e['bytes'] and i['mode']=='0444','repaired '+p)
need(len(rr['baseline_runs'])==4 and len(rr['negative_runs'])==12 and rr['false_variant_rejections_across_modes']==12,'repair counts')
need(rr['baseline_receipts_identical_across_modes'] and not rr['source_side_writes'],'repair invariants')
out=A/'ROOT_FAMILY_EVIDENCE_ACCEPTANCE.json';need(not out.exists(),'acceptance already exists')
body={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ALL_THREE_SCIENTIFIC_FAMILY_INVENTORIES_AND_ADDITIVE_SUPPORT_AUTHENTICATED','families':records,'repaired_verifier_receipt':ident(A/'ROOT_REPAIRED_CHECKERS_REPRODUCTION.json'),'scope':'Artifact authentication only; ROOT separately reads full mathematical reports and adjudicates the proof. No priority, publication or MAIN authority.'}
out.write_text(json.dumps(body,indent=2)+'\n');out.chmod(0o444)
print(json.dumps({'status':body['status'],'retained_files':sum(r['all_retained_files_authenticated'] for r in records),'family_counts':[r['all_retained_files_authenticated'] for r in records]}))

