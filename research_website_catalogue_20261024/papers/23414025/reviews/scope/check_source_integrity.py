from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile,io
from pypdf import PdfReader
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for id,main,archive in [('23414025','post-lie-note.pdf','post-lie-verification.zip'),('23390181','property-t-free-product-note.pdf','property-t-free-product-verification.zip')]:
 p=B/id;s=p/'sources';rec=json.loads((s/'record.json').read_text());receipt=json.loads((s/'receipt.json').read_text()); checks=[]
 assert {f['key'] for f in rec['files']}=={f['name'] for f in receipt['files']}
 for f in receipt['files']:
  b=(s/f['name']).read_bytes();actual=hashlib.sha256(b).hexdigest();md5=hashlib.md5(b).hexdigest();assert actual==f['sha256'] and 'md5:'+md5==f['zenodo_checksum'] and len(b)==f['bytes']; checks.append({'filename':f['name'],'bytes':len(b),'sha256':actual,'md5':md5,'pass':True})
 z=zipfile.ZipFile(s/archive);assert z.testzip() is None
 manifest=json.loads(z.read('package_index.json'));n=0
 for f in manifest['files']:
  b=z.read(f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'];n+=1
 pdfs=[];nested=[]
 for name in z.namelist():
  if name.endswith('.pdf'):
   b=z.read(name);pdfs.append({'path':name,'pages':len(PdfReader(io.BytesIO(b)).pages),'sha256':hashlib.sha256(b).hexdigest(),'identical_to_main':b==(s/main).read_bytes()})
  elif name.endswith('.zip'):
   inner=zipfile.ZipFile(io.BytesIO(z.read(name)));assert inner.testzip() is None;nested.append({'path':name,'members':len(inner.infolist()),'pdf_members':[x for x in inner.namelist() if x.endswith('.pdf')],'crc_pass':True})
 out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'all_public_record_assets_present':True,'files':checks,'zip_crc_pass':True,'top_level_manifest':'package_index.json','manifest_entries_verified':n,'main_pdf_pages':len(PdfReader(s/main).pages),'pdf_members':pdfs,'nested_archives':nested,'pass':True,'boundary':'Byte integrity and page inventory only; no prior review verdicts read or validated.'}
 (p/'reviews/scope/source_integrity.json').write_text(json.dumps(out,indent=2)+'\n');print(id,n,pdfs,nested)
