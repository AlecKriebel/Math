import sys
sys.dont_write_bytecode=True
import json,pathlib,hashlib,re,zipfile,stat,subprocess
R=pathlib.Path(__file__).resolve().parent;A=R.parent.parent;P=A/'publication';E=R/'.cache/extracted';sha=lambda b:hashlib.sha256(b).hexdigest()
payloads={p.relative_to(E).as_posix():p.read_bytes() for p in E.rglob('*') if p.is_file()};mf=json.loads(payloads['MANIFEST.json']);assert set(payloads)==set(mf['files'])|{'MANIFEST.json'}
records=[]
for n,d in payloads.items():
 parts=pathlib.PurePosixPath(n).parts;assert not n.startswith('/') and '..' not in parts and n==pathlib.PurePosixPath(n).as_posix();assert not any(p.casefold() in ['sources','scratch','qa','.cache','.secrets'] or '.private' in p.casefold() for p in parts)
 assert pathlib.Path(n).suffix in ['.md','.json','.tex','.txt','.py','']
 if n!='MANIFEST.json':assert mf['files'][n]=={'bytes':len(d),'sha256':sha(d)}
 records.append({'path':n,'bytes':len(d),'sha256':sha(d)})
registry=json.loads(payloads['SEALS.json']);assert registry==mf['nested_seals'];nested=[]
for seal in registry:
 n=seal['path'];assert sha(payloads[n])==seal['sha256'];base=pathlib.PurePosixPath(n).parent;data=payloads[n];rows=[]
 if seal['kind']=='sha256sum':
  for ln in data.decode().splitlines():
   digest,rel=ln.split('  ',1);rows.append((base/rel,digest,None))
 elif seal['kind']=='json-files':
  for row in json.loads(data)['files']:rows.append((base/row['path'],row['sha256'],row['bytes']))
 else:
  assert seal['kind']=='original-audit-json';s=json.loads(data)
  for key,folder in [('publication_safe_author_files',base.parent),('publication_safe_audit_files',base)]:
   for row in s[key]:rows.append((folder/row['path'],row['sha256'],row['bytes']))
 names=[]
 for path,h,size in rows:
  name=path.as_posix();assert name not in names and name!=n and '..' not in path.parts;names.append(name);assert sha(payloads[name])==h and (size is None or len(payloads[name])==size)
 nested.append({'seal':n,'kind':seal['kind'],'sha256':seal['sha256'],'entries':len(rows),'verified_paths':names})
assert len(registry)==7 and sum(s['entries'] for s in nested)==83
ziprows=[]
with zipfile.ZipFile(P/'verification_package.zip') as z:
 for f in z.infolist():
  assert stat.S_ISREG(f.external_attr>>16) and not f.is_dir();ziprows.append({'name':f.filename,'mode':oct(f.external_attr>>16),'timestamp':f.date_time,'crc':f.CRC})
assert len(ziprows)==102
freeze=json.loads((R/'REPRODUCTION_LEDGER.json').read_text())['freeze'];assert freeze=={p.name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in P.iterdir() if p.is_file()}
assert freeze['verification_package.zip']=={'bytes':197194,'sha256':'6af7c815f863d44ba4b24708d5ae70bec4d5e0fd55789114083a605c08a27a20'}
assert freeze['make_package.py']['sha256']=='bc1d4879f8fa4faae7cfdfe9a5340d8040f29065011e81bb5ac4426ee3f00ecd'
assert freeze['seshadri_counterexample.pdf']=={'bytes':71160,'sha256':'8f50f329fac5b30ffea3d98f82e36ec71af0d3d5df44e38a21f992eb45aa4c48'}
assert freeze['seshadri_counterexample.tex']['sha256']=='6e85f3254cb8edc0bd428383a9ba7d231386fa2173cdfb19c336868c7235b065'
assert freeze['zenodo-deposit.json']['sha256']=='52fa2518f84c23f0a6d9a3f6fe06ce08657b5e1c843b8ee0fb0447ead4ad6500'
meta=json.loads((P/'zenodo-deposit.json').read_text());md=meta['metadata'];assert md['publication_date']=='2026-10-14' and md['version']=='1.0' and md['license']=='cc-by-4.0' and md['publication_type']=='preprint' and md['creators'][0]['orcid']=='0009-0001-9320-500X';assert len(md['related_identifiers'])==10
(R/'FREEZE_AND_INVENTORY.json').write_text(json.dumps({'status':'PASS','freeze':freeze,'payloads':sorted(records,key=lambda x:x['path']),'nested':nested,'archive_entries':ziprows,'outer_payloads':101,'archive_members':102,'nested_entries':83,'nested_seals':7,'metadata_all_fields_reviewed':meta,'original_acquisition_sha256':sha((A/'ORIGINAL_SNAPSHOT.json').read_bytes()),'pdf_five_pages_visually_inspected':True,'publication_unchanged':True},indent=2)+'\n')
S=A.parent.parent/'sources/pr585';scopes={'owr2009.pdf':('https://ems.press/content/serial-article-files/46224?nt=1','Entire Szemberg contribution printed1124–1126/PDF24–26 directly extracted before checkpoint; p1124 visually checked afterward. Other contributions not read.'),'szemberg2007v1.pdf':('https://arxiv.org/pdf/0711.0584v1','Complete p7 final challenge directly extracted before checkpoint, visually checked afterward. Rest not fully read by this family; journal version not compared.'),'primer2010v2.pdf':('https://arxiv.org/pdf/0810.0728v2','Entire Q6.1.6 p17 and surrounding page directly extracted before checkpoint; page visually checked afterward. Rest not fully read; published version not compared.'),'bauer1999v1.pdf':('https://arxiv.org/pdf/math/9903072v1','Full pp9–14 read, including canonical slope, Prop3.3/Lemma3.5 and complete proof/asymptotic qualification. Other pages not fully read.'),'bauer_szemberg2010v1.pdf':('https://arxiv.org/pdf/1011.0979v1','Full pp1–3 read including entire Prop2.1 proof. Remaining pages not read by this family.'),'fuentes_cyclic2006v2.pdf':('https://arxiv.org/pdf/math/0511547v2','All16 extracted pages read, split into1–7 and8–16 after initial combined truncation. Classical cover Section2p3 checked directly; no independent reproving of all other results claimed.'),'ein_laz1993.pdf':('https://www.math.stonybrook.edu/~roblaz/Reprints/Ein.Laz.Seshadri.Consts.Smooth.Sfs.pdf','Image-only scan: complete printed182/PDF6,184/PDF8,185/PDF9 visually read including Example3.1/3.7. Other pages not read.'),'fuentes_ruled.pdf':('https://arxiv.org/pdf/math/0503253','Full p10 Theorems4.14/4.16 read for historical route; rest not fully read. Not a main theorem dependency.')}
sources=[]
for n,(url,scope) in scopes.items():
 f=S/n;sources.append({'file':n,'url':url,'bytes':f.stat().st_size,'sha256':sha(f.read_bytes()),'own_actual_scope':scope,'raw_redistributed':False})
f=A/'reviews/priority01/.cache/bauer_szemberg2008v1.pdf';sources.append({'file':'bauer_szemberg2008v1.pdf','url':'https://arxiv.org/pdf/0801.3245v1','bytes':f.stat().st_size,'sha256':sha(f.read_bytes()),'own_actual_scope':'Complete p6 including Example1.3 read; remaining8pages not fully read by this family.','raw_redistributed':False})
(R/'SOURCE_LEDGER.json').write_text(json.dumps({'sources':sources,'own_priority_search':'No new comprehensive web/literature search. This is a fresh final-publication textual/source comparison, not an upgrade of the bounded priority assessment. No403 route retried.','previous_family_scope_records_read':['geometry01/SOURCE_LEDGER.json','pencil01/SOURCE_READ_SCOPE.json','priority01/SOURCE_LEDGER.json','priority02/SOURCE_LEDGER.json'],'priority_limits_retained':['Full2025survey unread','Roy2019thesis unread','Schulz/Schmidtthesis bodies unread','Long sources/citation bodies selectively read','Final journal versions not globally compared','Unindexed/unpublished earlier work not excluded'],'independence':'EARLY_CHECKPOINT.md predates root receipt/status/verdict, paper, original proof and prior review access; assignment supplied mechanism but no correctness verdict.','skill':'PDF skill read-only render/visual workflow; no authoring operation marker or editor action.'},indent=2)+'\n')
print(json.dumps({'status':'PASS','archive_members':102,'nested_entries':83,'source_records':len(sources),'freeze':freeze},indent=2))
