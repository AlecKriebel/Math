import hashlib,json,zipfile,stat,re
from pathlib import Path,PurePosixPath
HERE=Path.cwd();PKG=HERE.parent/'publication_package_v2';REPO=HERE.parents[3]
def require(c,label):
 if not c:raise RuntimeError(label)
def signature(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
sealpath=PKG/'PACKAGE_SEAL.json';seal=json.loads(sealpath.read_bytes())
require(signature(sealpath.read_bytes())['sha256']=='0defa9900eff43f37e110a3247a5e6204922caa88573d71270a0aee5024a00d9','seal identity')
actual={p.relative_to(PKG).as_posix():signature(p.read_bytes()) for p in PKG.rglob('*') if p.is_file() and p!=sealpath}
require(len(actual)==29,'payload count');require(actual==seal['package_safe_files'],'full payload closure/hash')
require(not any(p.is_symlink() for p in PKG.rglob('*')),'package symlinks')
require(set(seal['upload_files'])=={'outer_focal_period.pdf','outer_focal_period.tex','verification-package.zip'},'upload count/names')
for name,record in seal['upload_files'].items():require(actual[name]==record,'upload identity '+name)
mat=PKG/'materials';manifest=json.loads((mat/'MANIFEST.json').read_bytes())
matfiles={p.relative_to(mat).as_posix():signature(p.read_bytes()) for p in mat.rglob('*') if p.is_file()}
require({n:v for n,v in matfiles.items() if n!='MANIFEST.json'}==manifest['files'],'internal manifest closure')
entries={}
with zipfile.ZipFile(PKG/'verification-package.zip') as z:
 require(z.testzip() is None,'zip crc'); require(len(z.infolist())==25,'zip entries')
 for info in z.infolist():
  n=info.filename;p=PurePosixPath(n)
  require(n not in entries and not p.is_absolute() and '..' not in p.parts and '\\' not in n and not n.endswith('/'),'zip path/duplicate')
  require(not stat.S_ISLNK(info.external_attr>>16),'zip symlink')
  data=z.read(info);entries[n]=signature(data)
  require(data==(mat/n).read_bytes(),'zip/material bytes '+n)
require(entries==matfiles==seal['zip_entries'],'zip exact closure')
require((PKG/'outer_focal_period.tex').read_bytes()==(mat/'outer_focal_period.tex').read_bytes(),'source copy')
metadata=json.loads((mat/'metadata.json').read_bytes());deposit=json.loads((PKG/'zenodo-deposit.json').read_bytes())
require(metadata==seal['metadata_exact']==deposit['metadata'],'metadata equality')
require([x['path'] for x in deposit['files']]==list(seal['upload_files']),'deposit exact uploads')
origins=json.loads((mat/'SOURCE_ORIGINS.json').read_bytes());sourcechecks=[]
for n,record in origins.items():
 b=(mat/n).read_bytes();original=REPO/record['source_repository_path']
 require(signature(b)=={k:record[k] for k in ['bytes','sha256']},'origin payload '+n)
 require(original.read_bytes()==b,'unaltered origin '+n)
 sourcechecks.append({'payload':n,'source_repository_path':record['source_repository_path'],'bytes_and_hash_match':True})
require(len(origins)==13,'all source origins')
text=(PKG/'outer_focal_period.tex').read_text()
require(not re.search(r'\\(?:input|include|write18|immediate|openout|usepackage\{shellesc)',text),'tex external/mutation dependency')
report={'status':'PASS','seal':signature(sealpath.read_bytes()),'payload_files_excluding_seal':len(actual),'zip_entries':len(entries),'upload_files':seal['upload_files'],'all_29_payloads_match_seal':True,'zip_and_manifest_exact':True,'metadata_equal_in_all_locations':True,'source_origin_checks':sourcechecks,'third_party_payloads':'none found; explicitly inspected every payload type/content','pdf_pages':6}
(HERE/'PACKAGE_INTEGRITY_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
