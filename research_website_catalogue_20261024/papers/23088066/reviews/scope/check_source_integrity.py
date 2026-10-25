from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, io
from pypdf import PdfReader
B = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident, main, archive, prefix, manifest_name in [
 ('22929486','Kourovka_16_45_Counterexample_v1.0.1.pdf','Kourovka_16_45_Source_and_Verification_v1.0.1.zip','kourovka_16_45/','manifest.json'),
 ('23088066','paper.pdf','source-and-verification.zip','','PACKAGE_MANIFEST.json')
]:
 s=B/ident/'sources';p=B/ident/'reviews/scope'
 record=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
 normalized=[dict(name=f.get('name',f.get('filename')),url=f['url'],bytes=f['bytes'],sha256=f['sha256'],zenodo_checksum=f.get('zenodo_checksum',f.get('record_checksum'))) for f in receipt['files']]
 assert {f['key'] for f in record['files']}=={f['name'] for f in normalized}
 checks=[]
 for f in normalized:
  b=(s/f['name']).read_bytes();sha=hashlib.sha256(b).hexdigest();md5=hashlib.md5(b).hexdigest()
  assert sha==f['sha256'] and 'md5:'+md5==f['zenodo_checksum'] and len(b)==f['bytes']
  live=next(g for g in record['files'] if g['key']==f['name']);assert live['checksum']==f['zenodo_checksum'] and live['size']==len(b)
  checks.append(dict(filename=f['name'],bytes=len(b),sha256=sha,md5=md5,passed=True))
 z=zipfile.ZipFile(s/archive);assert z.testzip() is None
 manifest=json.loads(z.read(prefix+manifest_name))['files']
 if isinstance(manifest,dict):manifest=[dict(path=k,**v) for k,v in manifest.items()]
 for f in manifest:
  name=prefix+f['path'];b=z.read(name)
  assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes'],name
  assert (s/'published-source'/name).read_bytes()==b,name
 pdfs=[];mainbytes=(s/main).read_bytes()
 for name in z.namelist():
  if name.endswith('.pdf'):
   b=z.read(name);pdfs.append(dict(path=name,pages=len(PdfReader(io.BytesIO(b)).pages),sha256=hashlib.sha256(b).hexdigest(),identical_to_main=b==mainbytes))
 assert not any(name.endswith('.zip') for name in z.namelist())
 checksum_count=0
 if ident=='22929486':
  for line in z.read(prefix+'SHA256SUMS').decode().splitlines():
   expected,name=line.split(None,1);name=name.lstrip('*')
   assert hashlib.sha256(z.read(prefix+name)).hexdigest()==expected,name
   checksum_count+=1
 result=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),all_public_record_assets_present=True,files=checks,
  zip_crc_pass=True,top_level_manifest=prefix+manifest_name,manifest_entries_verified=len(manifest),
  extracted_manifest_bytes_match=True,additional_sha256_manifest_entries_verified=checksum_count,
  main_pdf_pages=len(PdfReader(s/main).pages),pdf_members=pdfs,nested_archives=[],passed=True,
  boundary='Read-only byte integrity and page inventory. Source acquisition files are not rewritten; mathematical validation and opinion-exposure boundaries are documented separately.')
 (p/'source_integrity.json').write_text(json.dumps(result,indent=2)+'\n')
 print(ident,len(manifest),checksum_count,pdfs)
