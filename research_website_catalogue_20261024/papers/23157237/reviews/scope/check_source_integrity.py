from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, zipfile, io
from pypdf import PdfReader
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident in ['23157237','22729355']:
 s=B/ident/'sources';p=B/ident/'reviews/scope'
 record=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
 assert {x['key'] for x in record['files']}=={x['name'] for x in receipt['files']}
 checks=[];archives=[];pdfs=[]
 for f in receipt['files']:
  b=(s/f['name']).read_bytes();sha=hashlib.sha256(b).hexdigest();md5=hashlib.md5(b).hexdigest()
  live=next(x for x in record['files'] if x['key']==f['name'])
  assert sha==f['sha256'] and 'md5:'+md5==f['zenodo_checksum']==live['checksum'] and len(b)==f['bytes']==live['size']
  checks.append(dict(filename=f['name'],bytes=len(b),sha256=sha,md5=md5,passed=True))
  if f['name'].endswith('.pdf'):pdfs.append(dict(filename=f['name'],pages=len(PdfReader(io.BytesIO(b)).pages),sha256=sha))
  if f['name'].endswith('.zip'):
   z=zipfile.ZipFile(io.BytesIO(b));assert z.testzip() is None
   root=s/'published-source' if ident=='23157237' else s/'published-source'/Path(f['name']).stem
   members=[];internalpdfs=[];nested=[]
   for item in z.infolist():
    if item.is_dir():continue
    data=z.read(item.filename);assert (root/item.filename).read_bytes()==data,item.filename
    members.append(item.filename)
    if item.filename.endswith('.pdf'):internalpdfs.append(dict(path=item.filename,pages=len(PdfReader(io.BytesIO(data)).pages),sha256=hashlib.sha256(data).hexdigest(),identical_to_published_pdf=next((g['name'] for g in receipt['files'] if g['name'].endswith('.pdf') and (s/g['name']).read_bytes()==data),None)))
    if item.filename.endswith(('.zip','.tar.gz','.tgz')):nested.append(item.filename)
   nmanifest=0
   if ident=='23157237':
    prefix='spectral-tensor-consistency/'
    for f2 in json.loads(z.read(prefix+'MANIFEST.json'))['payload']:
     data=z.read(prefix+f2['path']);assert len(data)==f2['bytes'] and hashlib.sha256(data).hexdigest()==f2['sha256'];nmanifest+=1
   elif 'sha256_manifest.txt' in members:
    for line in z.read('sha256_manifest.txt').decode().splitlines():
     expected,name=line.split(None,1);name=name.removeprefix('./');data=z.read(name);assert hashlib.sha256(data).hexdigest()==expected,name;nmanifest+=1
   archives.append(dict(filename=f['name'],crc_pass=True,extracted_files_identical=len(members),manifest_entries_verified=nmanifest,pdf_members=internalpdfs,nested_archives=nested))
 manifest_count=0
 if (s/'SHA256SUMS.txt').exists():
  for line in (s/'SHA256SUMS.txt').read_text().splitlines():
   expected,name=line.split(None,1);assert hashlib.sha256((s/name).read_bytes()).hexdigest()==expected;manifest_count+=1
 result=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),passed=True,all_public_record_assets_present=True,files=checks,published_pdfs=pdfs,archives=archives,top_level_manifest_entries_verified=manifest_count,boundary='Byte integrity and document inventory only. Published source bytes remain unchanged; no mathematical claim follows from checksums.')
 (p/'source_integrity.json').write_text(json.dumps(result,indent=2)+'\n')
 print(ident,'all assets match',len(checks),'PDF pages',[(x['filename'],x['pages']) for x in pdfs],'archives',[(x['filename'],x['extracted_files_identical'],x['manifest_entries_verified'],len(x['pdf_members']),x['nested_archives']) for x in archives])
