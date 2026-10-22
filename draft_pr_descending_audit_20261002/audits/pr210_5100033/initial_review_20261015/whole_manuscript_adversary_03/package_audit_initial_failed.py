from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat,datetime
C=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr210_5100033');D=C/'initial_review_20261015';B=C/'preprint';O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def row(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
expected=load(O/'INPUT_SNAPSHOT.json')['files'];assert all(row(B/s)==r for s,r in expected.items())
rows=[]
with zipfile.ZipFile(B/'k605a-source-verification.zip') as z:
 names=z.namelist();assert len(names)==len(set(names))==181
 prefix=names[0].split('/')[0];assert prefix=='k605a_outer_focal_pedal_product'
 for i in z.infolist():
  p=PurePosixPath(i.filename);rel=p.relative_to(prefix).as_posix()
  assert not p.is_absolute() and '..' not in p.parts and not i.is_dir() and not i.flag_bits&1
  assert not stat.S_ISLNK(i.external_attr>>16)
  assert not set(p.parts)&{'private','private_reading','private_transport','__pycache__','.git'}
  assert p.suffix.lower() not in {'.html','.htm','.png','.jpg','.jpeg','.pyc'}
  assert p.suffix.lower()!='.pdf' or rel=='manuscript.pdf'
  data=z.read(i);assert data==(B/rel).read_bytes();rows.append({'path':rel,'bytes':len(data),'sha256':sha(data),'crc32':i.CRC})
 sm=load(B/'SOURCE_MANIFEST.json');assert len(sm['files'])==180
 assert {r['path'] for r in sm['files']}=={r['path'] for r in rows}-{'SOURCE_MANIFEST.json'}
 for r in sm['files']:assert row(B/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 target=O/'extracted';target.mkdir(exist_ok=True)
 z.extractall(target)
X=O/'extracted'/prefix
assert all(row(X/r['path'])=={k:r[k] for k in ['bytes','sha256']} for r in rows)
manifest_counts={}
for s in ['verification/MANIFEST.json','pr_update/5100033/MANIFEST.json','pr_update/5100033/PUBLICATION_MANIFEST.json','pr_update/5100033/CURRENT_PACKET_MANIFEST.json']:
 m=load(B/s);manifest_counts[s]=len(m['files'])
 for r in m['files']:assert row(B/Path(s).parent/r['path'])=={k:r[k] for k in ['bytes','sha256']}
intake=load(D/'INTAKE.json');assert len(intake['original_source_files'])==20
for r in intake['original_source_files']:
 rel=r['native_path'].split('attempts/5100033/')[1]
 for f in [D/'submitted'/r['native_path'],B/'verification/original_submission'/rel,B/'pr_update/5100033/history/original_submission_20261015'/rel]:
  data=f.read_bytes();assert len(data)==r['bytes'] and sha(data)==r['sha256']
  assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['native_blob']
families=[]
for f in sorted((B/'verification/audits').glob('*/AUTHORED_MANIFEST.json')):
 m=load(f);rs=m.get('authored_files',m.get('files'));families.append({'family':f.parent.name,'payloads':len(rs),'sha256':sha(f.read_bytes())})
 for r in rs:assert row(f.parent/r['path'])=={k:r[k] for k in ['bytes','sha256']}
assert len(families)==5
old=load(B/'verification/original_submission/MANIFEST_V1.json');assert [k for k,v in old['files'].items() if sha((B/'verification/original_submission'/k).read_bytes())!=v]==['SOURCES.md']
assert load(B/'metadata.json')==load(B/'deposit.json')['metadata']
oldzip=B/'history/review02_frozen/k605a-source-verification.zip'
with zipfile.ZipFile(oldzip) as z:
 prev={i.filename.split('/',1)[1]:z.read(i) for i in z.infolist()}
cur={r['path']:(B/r['path']).read_bytes() for r in rows}
diffs={k:'added' if k not in prev else 'changed' for k in set(cur)|set(prev) if cur.get(k)!=prev.get(k)}
assert diffs=={'NATIVE_RELEASE_PLAN.json':'changed','REVIEW02_RESOLUTION.json':'added','SOURCE_MANIFEST.json':'changed'}
q=load(B/'RENDER_QA.json');page_rows=[]
for n in range(1,7):
 f=B/f'rendered/page-{n}.png';r=row(f);assert r['sha256']==q['rendered_pages'][n-1]['sha256']
 page_rows.append({'path':str(f),**r,'actually_viewed_using_view_image':True,'findings':[]})
(O/'VISUAL_QA_RECEIPT.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pdf':row(B/'manuscript.pdf'),'source':row(B/'manuscript.tex'),'pages':page_rows,'view_method':'All six view_image results were emitted and visually inspected; no compile/render rerun.','findings':[]},indent=2)+'\n')
(O/'PACKAGE_INTEGRITY_RECEIPT.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fixed_inputs':expected,'zip_entries':rows,'manifest_counts':manifest_counts,'originals_checked':20,'native_total_files':len(list((B/'pr_update/5100033').rglob('*'))),'families':families,'previous_review02_to_current_changes':diffs,'all_passed':True},indent=2)+'\n')
print({'entries':len(rows),'manifest_counts':manifest_counts,'families':families,'prior_zip_diff':diffs,'extracted':str(X)})
