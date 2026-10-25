from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, io
from pypdf import PdfReader
B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident, main, archive in [('23353160','grassmann_orbitopes_calibrations_separable_state_application.pdf','grassmann_calibrations_source_verification_v1.zip'),('23147866','w4_locc_dense_coding.pdf',None)]:
 s=B/ident/'sources';p=B/ident/'reviews/scope'
 record=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
 files=receipt['files'];assert {f['key'] for f in record['files']}=={f['name'] for f in files}
 checks=[]
 for f in files:
  b=(s/f['name']).read_bytes();sha=hashlib.sha256(b).hexdigest();md5=hashlib.md5(b).hexdigest()
  assert sha==f['sha256'] and 'md5:'+md5==f['zenodo_checksum'] and len(b)==f['bytes']
  live=next(g for g in record['files'] if g['key']==f['name']);assert live['checksum']==f['zenodo_checksum'] and live['size']==len(b)
  checks.append(dict(filename=f['name'],bytes=len(b),sha256=sha,md5=md5,passed=True))
 result=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),all_public_record_assets_present=True,files=checks,main_pdf_pages=len(PdfReader(s/main).pages),passed=True,boundary='Read-only byte integrity and page inventory, not mathematical validation. No source bytes rewritten.')
 if archive:
  z=zipfile.ZipFile(s/archive);assert z.testzip() is None;prefix='grassmann_calibrations_v1/'
  manifest=json.loads(z.read(prefix+'PACKAGE_MANIFEST.json'))['files']
  for f in manifest:
   name=prefix+f['path'];b=z.read(name);assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes'],name
   assert (s/'published-source'/name).read_bytes()==b,name
  pdfs=[];mainbytes=(s/main).read_bytes()
  for name in z.namelist():
   if name.endswith('.pdf'):
    b=z.read(name);pdfs.append(dict(path=name,pages=len(PdfReader(io.BytesIO(b)).pages),sha256=hashlib.sha256(b).hexdigest(),identical_to_main=b==mainbytes))
  nested=[n for n in z.namelist() if n.endswith(('.zip','.tar.gz'))];assert not nested
  result.update(zip_crc_pass=True,manifest_entries_verified=len(manifest),extracted_manifest_bytes_match=True,pdf_members=pdfs,nested_archives=nested)
 else:
  count=0
  for line in (s/'SHA256SUMS.txt').read_text().splitlines():
   expected,name=line.split(None,1);name=name.lstrip('*');assert hashlib.sha256((s/name).read_bytes()).hexdigest()==expected,name;count+=1
  result.update(published_source_archive=False,additional_sha256_manifest_entries_verified=count,pdf_members=[],nested_archives=[])
 (p/'source_integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(ident,result)
