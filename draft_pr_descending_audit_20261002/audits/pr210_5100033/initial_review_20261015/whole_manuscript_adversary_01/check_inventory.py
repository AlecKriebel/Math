from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,datetime,sys
HERE=Path(__file__).parent
P=HERE.parent.parent/'preprint'
D=P.parent/'initial_review_20261015'
def h(x):return hashlib.sha256(x).hexdigest()
def read(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(P).as_posix(),bytes=len(b),sha256=h(b))
def checkrow(base,r):
 b=(base/r['path']).read_bytes();assert len(b)==r['bytes'] and h(b)==r['sha256'],str(base/r['path'])
source=read(P/'SOURCE_MANIFEST.json')
assert len(source['files'])==168
for r in source['files']:checkrow(P,r)
ziprows=[]
with zipfile.ZipFile(P/'k605a-source-verification.zip') as z:
 ns=z.namelist();assert len(ns)==len(set(ns))==169
 for i in z.infolist():
  pp=PurePosixPath(i.filename);assert pp.parts[0]=='k605a_outer_focal_pedal_product' and '..' not in pp.parts and not pp.is_absolute()
  rel=PurePosixPath(*pp.parts[1:]).as_posix();raw=z.read(i);assert raw==(P/rel).read_bytes()
  assert i.file_size==len(raw) and not i.is_dir() and i.flag_bits&1==0 and (i.external_attr>>16)&0o170000==0o100000
  assert not set(pp.parts)&{'private','private_reading','private_transport','private_upstream','__pycache__','.git'}
  ziprows.append(dict(path=i.filename,bytes=len(raw),sha256=h(raw),CRC=i.CRC))
 assert set(ns)=={'k605a_outer_focal_pedal_product/'+r['path'] for r in source['files']}|{'k605a_outer_focal_pedal_product/SOURCE_MANIFEST.json'}
manifest=read(P/'PACKAGE_MANIFEST.json')
for r in [manifest['source_manifest'],*manifest['submission_files'],manifest['manuscript_source'],manifest['metadata']]:checkrow(P,r)
verify=P/'verification';vm=read(verify/'MANIFEST.json')
for r in vm['files']:checkrow(verify,r)
assert len(vm['files'])==117
assert {r['path'] for r in vm['files']}=={f.relative_to(verify).as_posix() for f in verify.rglob('*') if f.is_file() and f.name!='MANIFEST.json'}|{f.relative_to(verify).as_posix() for f in verify.rglob('MANIFEST.json') if f!=verify/'MANIFEST.json'}
intake=read(D/'INTAKE.json'); originals=[];native=P/'pr_update/5100033'
for r in intake['original_source_files']:
 rel=r['native_path'].split('/5100033/')[1]
 copies=[D/'submitted'/r['native_path'],verify/'original_submission'/rel,native/'history/original_submission_20261015'/rel]
 data=[f.read_bytes() for f in copies];assert data[0]==data[1]==data[2]
 assert len(data[0])==r['bytes'] and h(data[0])==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(data[0])).encode()+b'\0'+data[0]).hexdigest()==r['native_blob']
 originals.append(dict(path=rel,bytes=len(data[0]),sha256=h(data[0]),git_blob_SHA1=r['native_blob']))
assert len(originals)==20
nm=read(native/'CURRENT_PACKET_MANIFEST.json')
for r in nm['files']:checkrow(native,r)
assert set(r['path'] for r in nm['files'])=={f.relative_to(native).as_posix() for f in native.rglob('*') if f.is_file() and f.name!='CURRENT_PACKET_MANIFEST.json'}
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
 for r in read(native/name)['files']:checkrow(native,r)
receipt=read(native/'verification.json');assert receipt['original_result']==read(verify/'original_submission/verification.json')
assert receipt['original_proof_sha256']==h((verify/'original_submission/PROOF.md').read_bytes())
assert (native/'verify.py').read_bytes()==(verify/'original_submission/verify.py').read_bytes()
assert (native/'PROOF.md').read_bytes()!=(verify/'original_submission/PROOF.md').read_bytes()
metadata=read(P/'metadata.json');assert metadata==read(P/'deposit.json')['metadata']
assert metadata['creators'][0]['orcid']=='0009-0001-9320-500X' and metadata['license']=='cc-by-4.0' and metadata['publication_type']=='preprint'
# Detect textual primary payloads by allowed paths and extensions, in addition to forbidden-path checks.
assert all(PurePosixPath(r['path']).suffix.lower() not in {'.html','.htm','.png','.jpg','.pyc'} for r in source['files'])
assert [r['path'] for r in source['files'] if PurePosixPath(r['path']).suffix.lower()=='.pdf']==['manuscript.pdf']
rows=[pin(P/n) for n in ['manuscript.tex','manuscript.pdf','metadata.json','k605a-source-verification.zip','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json','verification/MANIFEST.json']]
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),completion_percent=40,input_pins=rows,source_rows=168,zip_entries=169,verification_rows=117,native_manifest_rows=len(nm['files']),all_zip_bytes_and_inventory_checked=True,all_native_manifest_rows_checked=True,all_original_20_bytes_and_git_blobs_checked=True,all_metadata_checks_passed=True,zip_inventory=ziprows,original_inventory=originals)
(HERE/'INPUT_AND_INTEGRITY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'zip_inventory','original_inventory'}},indent=2))
