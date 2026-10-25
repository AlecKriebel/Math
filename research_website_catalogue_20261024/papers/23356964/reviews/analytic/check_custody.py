"""Final source and archive identity verification; no historical opinion parsing."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,stat,zipfile
R=Path(__file__).resolve().parent;P=R.parents[1];S=P/'sources'
ROOT=S/'published-source/generic-wreath-hyperfiniteness-verification'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(v,s):
 if not v:raise RuntimeError(s)
expected={'generic-wreath-hyperfiniteness-note.pdf':'a164240679a1ed733c4eebce1817c239a423a9cd7952d93d9902e0885160ae4e','generic-wreath-hyperfiniteness-verification.zip':'3d73bb07b994c619df8a7e27ed2e43c99dd4e30c9fc1e5406454ee0671d1ebdd','record.json':'f4096d4c3f6357b761902cc97f30454d12e3dbbfe78e8ff4f2ec5201bb0eb827'}
for n,h in expected.items():need(sha(S/n)==h,'source pin '+n)
receipt=json.loads((S/'receipt.json').read_text())
for f in receipt['files']:
 p=S/f['name'];need(len(p.read_bytes())==f['bytes'],'API byte count');need(hashlib.md5(p.read_bytes()).hexdigest()==f['md5']==f['zenodo_checksum'][4:],'API MD5');need(sha(p)==f['sha256'],'receipt SHA')
with zipfile.ZipFile(S/'generic-wreath-hyperfiniteness-verification.zip') as z:
 names=[i.filename for i in z.infolist() if not i.is_dir()]
 need(len(names)==len(set(names))==121,'outer member count')
 for n in names:
  q=PurePosixPath(n);need(not q.is_absolute() and '..' not in q.parts,'safe outer path');need((ROOT/n).read_bytes()==z.read(n),'outer member '+n)
 need({str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file()}==set(names),'outer closed inventory')
metadata=json.loads((ROOT/'source/PUBLICATION_METADATA.json').read_text());nested=[]
for arc in metadata['archives']:
 zpath=ROOT/'source'/arc['path'];target=ROOT/'source'/arc['extract_root']
 need(sha(zpath)==arc['sha256'],'nested archive pin')
 with zipfile.ZipFile(zpath) as z:
  items=z.infolist();need(len(items)==arc['regular_members'],'nested inventory')
  for i in items:
   p=PurePosixPath(i.filename);need(not i.is_dir() and not p.is_absolute() and '..' not in p.parts,'safe nested path')
   need(z.read(i)==(target/i.filename).read_bytes(),'nested opaque byte identity')
 nested.append({'archive':str(zpath.relative_to(S)),'sha256':sha(zpath),'members_equal':len(items)})
need(len(nested)==3 and sum(a['members_equal'] for a in nested)==51,'nested total')
need((ROOT/'note.pdf').read_bytes()==(S/'generic-wreath-hyperfiniteness-note.pdf').read_bytes(),'embedded main reader')
before=json.loads((R/'source-custody-before.json').read_text())['files_sha256'];after={str(f.relative_to(S)):sha(f) for f in sorted(S.rglob('*')) if f.is_file()};need(before==after,'all source bytes unchanged')
primary=[]
for rec in json.loads((P/'reviews/scope/primary-source-receipts.json').read_text()):
 if rec.get('status')!='acquired':continue
 f=P/'reviews/scope/cache/primary-sources'/rec['name'];need(sha(f)==rec['sha256'],'primary pin '+rec['name']);primary.append({k:rec.get(k) for k in ['name','url','resolved_url','version','bytes','sha256','retrieved_utc']})
res={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','public_pins':expected,'public_api_MD5_and_bytes_match':True,'outer_members_equal':121,'nested_archives':nested,'nested_members_equal':51,'archive_entries_verified_including_nested_views':172,'all_source_files_unchanged':len(after),'embedded_reader_identical':True,'primary_receipts_checked':primary,'after_source_files_sha256':after,'scope':'Nested archives and historical assessment files inspected only as opaque byte identities, except the expressly read mathematical support/code. No adoption of historical assessment content.'}
(R/'custody-results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:res[k] for k in ['status','outer_members_equal','nested_members_equal','all_source_files_unchanged']}))
