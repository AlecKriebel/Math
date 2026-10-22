#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,zipfile,stat,re
BASE=Path(__file__).resolve().parent
LIVE=BASE.parent.parent/'publication'
COPY=BASE/'tmp/extracted'
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def require(x,msg):
 if not x:raise RuntimeError(msg)
receipt=json.loads((LIVE/'PACKAGE_RECEIPT.json').read_text())
checks={}
checks['receipt_byte_exact']= (LIVE/'PACKAGE_RECEIPT.json').read_bytes()==(COPY/'PACKAGE_RECEIPT.json').read_bytes()
require(checks['receipt_byte_exact'],'Rebuilt receipt differs')
checks['six_rebuilt_pins']={}
for name,p in receipt['files'].items():
 original=(LIVE/name).read_bytes();rebuilt=(COPY/name).read_bytes()
 require(pin(original)==p,'Live receipt pin '+name)
 require(rebuilt==original,'Rebuilt bytes '+name)
 checks['six_rebuilt_pins'][name]=p
with zipfile.ZipFile(LIVE/'output/simple-brace-counterexample-source-and-verification.zip') as src:
 names=src.namelist()
 require(len(names)==79==len(set(names)),'Source inventory')
 require(all(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n for n in names),'Unsafe member')
 require(all(not stat.S_ISLNK(i.external_attr>>16) for i in src.infolist()),'Source symlink')
 manifest=json.loads(src.read('SOURCE_MANIFEST.json'))
 require(set(manifest)==set(names)-{'SOURCE_MANIFEST.json'},'Manifest inventory')
 require(manifest==receipt['source_members'],'Receipt manifest mismatch')
 for n,p in manifest.items():require(pin(src.read(n))==p,'Source member pin '+n)
 checks['source_member_hashes_checked']=len(manifest)
 require(not any(any(bit in n.lower() for bit in ['/private/','/tmp/','__pycache__','.pyc','.git/']) for n in names),'Cache/source body leak path')
 allowed_pdf=['output/pdf/simple-brace-counterexample.pdf']
 require([n for n in names if n.endswith('.pdf')]==allowed_pdf,'Unexpected third party PDF')
 require(not any(n.endswith(('.html','.xml','.png','.jpg','.tex~','.pdf.txt')) for n in names),'Raw source body types')
 provenance=json.loads(src.read('PROVENANCE.json'))
 require(provenance['source_head_sha']=='f86b108ac1bc024302648eee9f47f74e26c810ec','Head provenance')
 require(pin(src.read('audit/inputs/PROOF.md'))['sha256']=='68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75','Proof provenance')
 for n in ['PROOF.md','SOURCE_METADATA.json','SOURCE_REVIEW.md','MATHEMATICAL_AUDIT.md','ACCEPTANCE.json','STATUS.json','MANIFEST.json','README.md']:
  require(src.read('audit/inputs/'+n)==(BASE.parent.parent/'inputs'/n).read_bytes(),'Frozen input '+n)
 checks['eight_original_inputs_equal']=True
 checks['source_privacy_path_and_type_screen']='PASS; full authored contents manually inspected separately'
 with zipfile.ZipFile(LIVE/'output/zenodo-upload-kit.zip') as kit:
  expected={'simple-brace-counterexample.pdf','simple-brace-counterexample-source-and-verification.zip','zenodo-metadata.json','zenodo-deposit.json','README.md'}
  require(set(kit.namelist())==expected and len(kit.namelist())==5,'Kit inventory')
  require(kit.read('simple-brace-counterexample.pdf')==(LIVE/'output/pdf/simple-brace-counterexample.pdf').read_bytes(),'Kit PDF')
  require(kit.read('simple-brace-counterexample-source-and-verification.zip')==(LIVE/'output/simple-brace-counterexample-source-and-verification.zip').read_bytes(),'Kit source')
  require(kit.read('README.md')==src.read('README.md'),'Kit README')
  require(kit.read('zenodo-metadata.json')==src.read('zenodo-metadata.json')==(LIVE/'zenodo-metadata.json').read_bytes(),'Metadata copies')
  md=json.loads(kit.read('zenodo-metadata.json'));dep=json.loads(kit.read('zenodo-deposit.json'));live_dep=json.loads((LIVE/'zenodo-deposit.json').read_text())
  require(md==dep['metadata']==live_dep['metadata'],'Deposit metadata')
  require(dep['files']==[{'path':'simple-brace-counterexample.pdf'},{'path':'simple-brace-counterexample-source-and-verification.zip'}],'Portable file paths')
  require(all((LIVE/r['path']).is_file() for r in live_dep['files']),'Live file paths')
  require('\\u' not in md['description'],'Literal Unicode escape leak')
  require('Okniński' in md['description'],'Author name')
  checks['all_metadata_copies_identical_and_decoded_unicode_correct']=True
  checks['kit_member_bytes_and_portable_paths_checked']=True
checks['status']='PASS'
(BASE/'PACKAGE_CHECK.json').write_text(json.dumps(checks,indent=2,sort_keys=True)+'\n')
print(json.dumps(checks,indent=2,sort_keys=True))
