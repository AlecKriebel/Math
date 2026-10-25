from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,stat
b=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23431676');a=b/'reviews/analytic';s=b/'sources';p=s/'published-source/pr1097_support_v1_0';receipt=json.loads((s/'receipt.json').read_text());r=json.loads((s/'record.json').read_text())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assets=[]
for row in receipt['assets']:
 f=s/row['name'];actual={'filename':f.name,'bytes':f.stat().st_size,'md5':hashlib.md5(f.read_bytes()).hexdigest(),'sha256':sha(f)}
 for k in ['sha256','md5','bytes']:
  if actual[k]!=row[k]:raise RuntimeError('asset mismatch '+k)
 assets.append(actual)
z=s/'pr1097_support_v1_0.zip';members=[]
with zipfile.ZipFile(z) as f:
 if f.testzip() is not None:raise RuntimeError('CRC failure')
 names=set()
 for row in f.infolist():
  name=row.filename;parts=Path(name).parts
  if name in names or Path(name).is_absolute() or '..' in parts or '\\' in name:raise RuntimeError('unsafe or duplicate path')
  names.add(name)
  if row.is_dir():continue
  if stat.S_ISLNK(row.external_attr>>16):raise RuntimeError('symlink')
  data=f.read(row);target=p/name
  if not target.is_file() or target.read_bytes()!=data:raise RuntimeError('extracted mismatch '+name)
  members.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
prim=b/'reviews/scope/cache/primary-sources';ps=[]
for name,scope,url in [
 ('bl-1992.pdf','Definitions and halting/bounded-game interfaces pp.3–5; primitive kernel and period-deletion pp.12–13; reduced uniqueness pp.16–17.','https://lovasz.web.elte.hu//morepapers/abacus.pdf'),
 ('farrell-levine-v3.pdf','Definitions/nonnegative adjacency-input halting pp.1–3; least action and tree/kernel interfaces pp.4–7; full hardness reduction and total-Laplacian construction pp.10–13.','https://arxiv.org/pdf/1502.04690v3'),
 ('hkt-v4.pdf','Definitions/encoding, Theorem1 and Lemmas2–5, Proposition8 pp.2–6; Theorem12 full proof pp.8–9; Theorem14 full proof pp.9–10; Problem19 p.12.','https://arxiv.org/pdf/1507.03209v4'),
 ('kiss-tothmeresz-v3.pdf','Full Section4 pp.11–14, reserve/finite-horizon simulation and Eulerian restriction; attribution interface only.','https://arxiv.org/pdf/1407.6958v3'),
 ('tothmeresz-v2.pdf','Definitions/encoding pp.2–4; full chip-firing Section2 pp.4–7, especially Theorem2.3, Claim2.4 and Proposition2.8.','https://arxiv.org/pdf/2102.11970v2')]:
 ps.append({'path':str(prim/name),'sha256':sha(prim/name),'bytes':(prim/name).stat().st_size,'read_scope':scope,'url':url})
checkfiles=['paper.tex','paper.pdf','scripts/run_checks.py','scripts/common.py']
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'record_id':'23431676','metadata_version':r['metadata'].get('version'),'publication_date':r['metadata']['publication_date'],'record_created':r.get('created'),'date_note':'Preparation/publication metadata date is distinct from creation; no first deposit or priority inference.','receipt_sha256':sha(s/'receipt.json'),'record_sha256':sha(s/'record.json'),'assets':assets,'zip_crc_pass':True,'regular_members':len(members),'extracted_members_byte_equal':True,'opaque_historical_members':'Hashed as bytes only; bodies not read.','current_support':[{'path':x,'sha256':sha(p/x)} for x in checkfiles],'primary_interfaces':ps}
(a/'evidence/source-custody.json').write_text(json.dumps(result,indent=2)+'\n');(a/'evidence/zip-members.json').write_text(json.dumps(members,indent=2)+'\n')
seal=json.loads((a/'evidence/pre_helper_seal.json').read_text())
for name,h in seal['files'].items():
 if sha(a/'evidence'/name)!=h:raise RuntimeError('independent seal changed')
print(json.dumps({k:result[k] for k in ['checked_utc','metadata_version','publication_date','record_created','regular_members','receipt_sha256']},indent=2))
print('Source assets, all extracted members and independent seal verified')
