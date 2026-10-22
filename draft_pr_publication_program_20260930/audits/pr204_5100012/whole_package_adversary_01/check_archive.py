import hashlib,json,zipfile,stat
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent.parent
P=BASE/'publication_package_v1'
O=Path(__file__).resolve().parent
def pin(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def require(v,s):
 if not v:raise RuntimeError(s)
seal=json.loads((P/'PACKAGE_SEAL.json').read_text())
require(pin((P/'PACKAGE_SEAL.json').read_bytes())=={'bytes':29496,'sha256':'8808d37f4f0ed5a7cac015d9ef989aa07afca65498f450324d0128d1dd26d8fb'},'seal pin')
actual={str(p.relative_to(P)):pin(p.read_bytes()) for p in P.rglob('*') if p.is_file()}
require(len(actual)==181,'outer count')
require({k:v for k,v in actual.items() if k!='PACKAGE_SEAL.json'}==seal['files'],'all outer exact inventory')
require(not any(p.is_symlink() for p in P.rglob('*')),'outer symlinks')
manifest=json.loads((P/'PUBLIC_MATERIALS_MANIFEST.json').read_text())
expected={**manifest['files'],'PUBLIC_MATERIALS_MANIFEST.json':actual['PUBLIC_MATERIALS_MANIFEST.json']}
with zipfile.ZipFile(P/'verification-package.zip') as z:
 infos=z.infolist();names=[x.filename for x in infos]
 require(len(names)==177 and len(names)==len(set(names)),'ZIP count/duplicates')
 require(set(names)==set(expected),'exact ZIP file set')
 for x in infos:
  n=x.filename;q=PurePosixPath(n)
  require(not q.is_absolute() and '..' not in q.parts and not x.is_dir(),'unsafe ZIP path')
  require(not stat.S_ISLNK(x.external_attr>>16),'ZIP symlink')
  data=z.read(x)
  require(pin(data)==expected[n] and pin(data)==actual[n],'ZIP member pin '+n)
 require(z.testzip() is None,'ZIP CRC')
for n,v in manifest['external_manuscript_uploads'].items():require(actual[n]==v,'external '+n)
require(set(manifest['external_manuscript_uploads'])=={'centered_pedal_dn.pdf','centered_pedal_dn.tex'},'external list')
require(actual['zenodo-deposit.json']==seal['exact_intended_Zenodo_metadata'],'metadata exact')
require(actual['portable_verification_01/INPUT_PINS.json']==manifest['scientific_input_pin_manifest'],'scientific manifest')
for n in names:
 require(not any(s in PurePosixPath(n).parts for s in ['__pycache__','node_modules','runtime_packages','primary_source_private']),'cache/dependency/private '+n)
 require(not n.endswith(('.pyc','.pyo','.pdf')),'binary/private primary '+n)
require(not any('RUNTIME_CACHE_INCIDENT_01.json' in n for n in names),'private incident included')
c=json.loads((P/'materials/ORIGINAL_SUBMISSION_CUSTODY.json').read_text())
original={str(q.relative_to(P/'materials/original_submitted_head')):pin(q.read_bytes()) for q in (P/'materials/original_submitted_head').rglob('*') if q.is_file()}
require(len(original)==20 and set(original)==set(c['files']),'original20 file set')
blob_pins={}
for n,v in c['files'].items():
 data=(P/'materials/original_submitted_head'/n).read_bytes()
 blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 require(original[n]=={'bytes':v['bytes'],'sha256':v['sha256']} and blob==v['git_blob'],'original bytes/blob '+n)
 require(data==(BASE/'original_submitted_head'/n).read_bytes(),'public-original input equality '+n)
 blob_pins[n]=blob
trees=json.loads((P/'materials/original_git_metadata/ALL_AUTHENTICATED_NONRECURSIVE_TREES.json').read_text())
tree_pins={}
for h,obj in trees.items():
 require(not obj.get('truncated',False),'truncated native tree')
 entries=sorted(obj['tree'],key=lambda x:x['path'].encode()+ (b'/' if x['type']=='tree' else b''))
 body=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']) for x in entries)
 got=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()
 require(got==h==obj['sha'],'native tree hash '+h)
 tree_pins[h]=len(entries)
# Verify original path traversal binds all20 blobs to original HEAD tree.
root=c['original_tree']
for rel,v in c['files'].items():
 parts=('unsolved_math_prioritization/attempts/5100012/'+rel).split('/')
 h=root
 for i,s in enumerate(parts):
  require(h in trees,'missing authenticated ancestor '+h)
  hits=[x for x in trees[h]['tree'] if x['path']==s];require(len(hits)==1,'missing native component '+s)
  entry=hits[0];h=entry['sha']
 require(entry['type']=='blob' and h==v['git_blob'],'native membership '+rel)
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','outer_files':len(actual),'ZIP_entries':len(names),'original_files':len(original),'original_total_bytes':sum(v['bytes'] for v in original.values()),'all_native_blob_pins':blob_pins,'all_native_tree_hashes':tree_pins,'exact_all_outer_pins':True,'ZIP_members_equal_outer_and_manifest':True,'metadata_and_upload_pins':True,'all_original_files_bound_to_HEAD_native_tree':True,'private_PDFs_dependencies_caches_absent_by_exact_inventory':True,'seal_pin':actual['PACKAGE_SEAL.json'],'uploads':seal['intended_uploads']}
(O/'ARCHIVE_CHECK.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
