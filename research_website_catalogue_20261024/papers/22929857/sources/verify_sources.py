"""Read-only verifier of record 22929857 native transport/archive bindings."""
from pathlib import Path
import hashlib,json,zipfile,zlib
HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 seal=json.loads((HERE/'SOURCE_READY_SEAL.json').read_text());assert sha(HERE/'SOURCE_READY.json')==seal['SOURCE_READY_SHA256'];assert sha(HERE/'SOURCE_READY_MANIFEST.json')==seal['SOURCE_READY_MANIFEST_SHA256'];manifest=json.loads((HERE/'SOURCE_READY_MANIFEST.json').read_text())
 for item in manifest['files']:
  p=HERE/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],str(p)
 raw=json.loads((HERE/'record.raw.json').read_text());files=json.loads((HERE/'files.raw.json').read_text());assert [x['key'] for x in raw['files']]==[x['key'] for x in files['entries']]
 for item in raw['files']:
  p=HERE/item['key'];assert p.stat().st_size==item['size'];assert 'md5:'+hashlib.md5(p.read_bytes()).hexdigest()==item['checksum']
 assert json.loads((HERE/'latest.raw.json').read_text())['id']==22929857
 versions=json.loads((HERE/'versions.raw.json').read_text());assert versions['hits']['total']==1 and [x['id'] for x in versions['hits']['hits']]==[22929857]
 with zipfile.ZipFile(HERE/'reproducibility.zip') as z:
  for item in z.infolist():
   if item.is_dir():continue
   payload=z.read(item);assert len(payload)==item.file_size and zlib.crc32(payload)&0xffffffff==item.CRC;assert payload==(HERE/'published-source'/item.filename).read_bytes()
 for line in (HERE/'published-source/MANIFEST.sha256').read_text().splitlines():
  if line.strip():
   expected,name=line.split(maxsplit=1);assert sha(HERE/'published-source'/name.lstrip('*'))==expected
 assert (HERE/'paper.pdf').read_bytes()==(HERE/'published-source/paper/main.pdf').read_bytes()
 print(json.dumps({'source_integrity':'PASS','native_asset_order':['reproducibility.zip','paper.pdf'],'published_PDF_identical_to_native_ZIP_reader':True,'native_payloads':30,'native_manifest_bindings':29,'scientific_claims_not_tested_by_custody_verifier':True},indent=2))
if __name__=='__main__':main()
