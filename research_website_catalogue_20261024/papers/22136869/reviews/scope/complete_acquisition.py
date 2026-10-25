from pathlib import Path
from urllib.request import Request,urlopen
from datetime import datetime,timezone
from zipfile import ZipFile
from pypdf import PdfReader
import json,hashlib,io
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22136869')
s=P/'sources';p=P/'reviews/scope'
r=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text())
for f in r['files']:
 if f['key'] in {x['name'] for x in receipt['files']}:continue
 assert f['key']=='SHA256SUMS'
 url=f['links']['self']
 with urlopen(Request(url,headers={'User-Agent':'Research catalogue verification'}),timeout=45) as response:b=response.read()
 assert len(b)==f['size'] and 'md5:'+hashlib.md5(b).hexdigest()==f['checksum']
 (s/f['key']).write_bytes(b)
 receipt['files'].append(dict(name=f['key'],url=url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),zenodo_checksum=f['checksum'],retrieved_utc=datetime.now(timezone.utc).isoformat()))
(s/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert {f['key'] for f in r['files']}=={x['name'] for x in receipt['files']}
for f in receipt['files']:
 b=(s/f['name']).read_bytes();live=next(x for x in r['files'] if x['key']==f['name'])
 assert hashlib.sha256(b).hexdigest()==f['sha256'] and 'md5:'+hashlib.md5(b).hexdigest()==live['checksum']==f['zenodo_checksum'] and len(b)==live['size']==f['bytes']
count=0
for line in (s/'SHA256SUMS').read_text().splitlines():
 expected,name=line.split(None,1);assert hashlib.sha256((s/name).read_bytes()).hexdigest()==expected;count+=1
z=ZipFile(s/'k2p-k3p-theta-collision-19cf11f65ed4.zip');assert z.testzip() is None
members=[];pdfs=[];nested=[]
for f in z.infolist():
 if f.is_dir():continue
 data=z.read(f.filename);dest=s/'published-source'/f.filename
 assert dest.resolve().is_relative_to((s/'published-source').resolve()) and dest.read_bytes()==data
 members.append(f.filename)
 if f.filename.lower().endswith('.pdf'):pdfs.append(dict(path=f.filename,pages=len(PdfReader(io.BytesIO(data)).pages),sha256=hashlib.sha256(data).hexdigest()))
 if f.filename.lower().endswith(('.zip','.tar.gz','.tgz')):nested.append(f.filename)
v=dict(timestamp_utc=datetime.now(timezone.utc).isoformat(),passed=True,all_public_record_assets_present=True,files=receipt['files'],main_pdf_pages=20,top_level_sha256_entries_verified=count,zip_crc_pass=True,extracted_files_identical=len(members),pdf_members=pdfs,nested_archives=nested,boundary='Source byte integrity only; no mathematical conclusion.')
(p/'source_integrity.json').write_text(json.dumps(v,indent=2)+'\n')
(p/'archive_inventory.json').write_text(json.dumps(members,indent=2)+'\n')
print(json.dumps(v,indent=2))
