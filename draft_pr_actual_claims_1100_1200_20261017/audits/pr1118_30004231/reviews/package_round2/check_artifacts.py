import hashlib,json,pathlib,zipfile,stat,subprocess,sys,datetime
HERE=pathlib.Path(__file__).resolve().parent
PUB=HERE.parents[1]/'publication'
def require(v,msg):
 if not v: raise RuntimeError(msg)
def fp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
r=json.loads((PUB/'PACKAGE_RECEIPT.json').read_text());checked=[]
for name,expected in r['files'].items():
 actual=fp((PUB/name).read_bytes()); require(actual==expected,name); checked.append(name)
src=zipfile.ZipFile(PUB/'output/totally-mixed-face-posets-source-and-verification.zip')
kit=zipfile.ZipFile(PUB/'output/zenodo-upload-kit.zip')
for z in (src,kit):
 names=z.namelist();require(len(names)==len(set(names)),'duplicate names')
 for i in z.infolist():
  p=pathlib.PurePosixPath(i.filename)
  require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'unsafe path')
  require(not stat.S_ISLNK(i.external_attr>>16),'symlink')
 require(z.testzip() is None,'CRC')
require(len(src.namelist())==29,'source count');require(len(kit.namelist())==5,'kit count')
man=json.loads(src.read('SOURCE_MANIFEST.json'))
(HERE/'evidence/manifest_shape.json').write_text(json.dumps(man,indent=2)+'\n')
for n,e in r['source_members'].items():require(fp(src.read(n))==e,'source receipt '+n)
require(set(src.namelist())==set(r['source_members'])|{'SOURCE_MANIFEST.json'},'source extra/missing')
# The manifest schema is inspected explicitly below.
meta=json.loads((PUB/'zenodo-metadata.json').read_text());dep=json.loads((PUB/'zenodo-deposit.json').read_text())
require(meta==dep['metadata'],'local deposit identity')
require(json.loads(src.read('zenodo-metadata.json'))==meta,'source metadata identity')
require(json.loads(kit.read('zenodo-metadata.json'))==meta,'kit metadata identity')
require(json.loads(kit.read('zenodo-deposit.json'))['metadata']==meta,'kit deposit metadata identity')
for n in ['main.tex','README.md','zenodo-metadata.json','output/pdf/totally-mixed-face-posets.pdf']:
 require(src.read(n)==(PUB/n).read_bytes(),'source/local '+n)
for n in kit.namelist():
 if n.endswith('.pdf'):require(kit.read(n)==(PUB/'output/pdf/totally-mixed-face-posets.pdf').read_bytes(),'kit PDF')
 elif n.endswith('source-and-verification.zip'):require(kit.read(n)==(PUB/'output/totally-mixed-face-posets-source-and-verification.zip').read_bytes(),'kit source')
require(meta['creators'][0]['orcid']=='0009-0001-9320-500X','ORCID')
require(meta['license']=='cc-by-4.0' and meta['publication_type']=='preprint','license/type')
require('unrefereed' in src.read('main.tex').decode().lower(),'unrefereed')
require('AI tools were used extensively' in src.read('main.tex').decode(),'AI')
require(not any(n.endswith(('.pdf','.html')) for n in src.namelist() if n!='output/pdf/totally-mixed-face-posets.pdf'),'thirdparty bodies')
src.extractall(HERE/'tmp/unpacked')
res={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen':r['files'],'checked_frozen_files':checked,'source_members':src.namelist(),'kit_members':kit.namelist(),'archive_metadata_crc_paths':'PASS'}
(HERE/'evidence/ARTIFACT_RESULTS.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({'result':'PASS','source_members':len(src.namelist()),'kit_members':kit.namelist(),'manifest_keys':list(man),'deposit_keys':list(dep)},indent=2))
