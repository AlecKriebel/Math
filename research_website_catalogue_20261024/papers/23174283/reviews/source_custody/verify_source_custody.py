#!/usr/bin/env python3
"""Read-only complete native source-custody validator; no scientific assessment."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat
E=Path(__file__).resolve().parent;S=E.parents[1]/'sources'
checks=0
def check(value,label):
 global checks
 checks+=1
 if not value:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'SOURCE_READY.json').read_text());raw=json.loads((S/'record.raw.json').read_text())
check(sha(S/'SOURCE_READY.json')=='b9f69bfea594378f8cd69a00d214ce14c894fd33e850047a915327432d96ae20','exact source-ready object')
check(raw['id']==r['record_id'] and raw['metadata']['version']==r['version'],'native record/version')
check(raw['metadata']['publication_date']==r['publication_date'] and raw['created']==r['created'] and raw['updated']==r['updated'],'original declared/create/update dates')
check(json.loads((S/'latest.raw.json').read_text())['id']==r['latest_record_id'],'actual latest object')
check(json.loads((S/'versions.raw.json').read_text())['hits']['total']==r['versions_total_original'],'complete native version count')
check(len(raw['files'])==len(r['all_assets_in_original_order'])==2,'all original native files retained')
for native,item in zip(raw['files'],r['all_assets_in_original_order']):
 f=Path(item['path']);b=f.read_bytes()
 check(native==item['original_api_file_object'],'complete native file object and ordering')
 check(len(b)==native['size']==item['bytes'],'native complete file size')
 check(native['checksum']=='md5:'+hashlib.md5(b).hexdigest(),'native MD5')
 check(hashlib.sha256(b).hexdigest()==item['sha256'],'full original SHA256')
receipts=json.loads((S/'transport-receipts.json').read_text())['ordinary_HTTPS_requests_in_native_object_and_file_order']
check(len(receipts)==5,'five native record/latest/versions/assets transports')
for ordinal,receipt in enumerate(receipts,1):
 body=Path(receipt['body_path']) if 'body_path' in receipt else S/'record.raw.json'
 check(receipt['HTTP_status']==200,'actual ordinary HTTPS status')
 check(body.stat().st_size==receipt['bytes'] and sha(body)==receipt['sha256'],'raw received body identity')
 check(isinstance(receipt['response_headers_in_received_order'],list),'received header order retained')
seal=json.loads((S/'SOURCE_READY_SEAL.json').read_text())
check(sha(S/'SOURCE_READY_MANIFEST.json')==seal['manifest_sha256'],'source-ready manifest seal')
for item in json.loads((S/'SOURCE_READY_MANIFEST.json').read_text())['files']:
 f=S/item['path'];check(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'source original unchanged '+item['path'])
ledger=json.loads((S/'archive-members.json').read_text());items=ledger['full_original_ordered_regular_occurrences']
check(len(items)==r['safe_regular_occurrences'] and sum(a['bytes'] for a in items)==r['expanded_bytes'],'whole selected archive scope')
container=S/items[0]['container']
with zipfile.ZipFile(container) as z:
 check(len([a for a in z.infolist() if not a.is_dir()])==len(items),'every original regular occurrence accounted')
 seen=set()
 for item in items:
  a=z.infolist()[item['ordinal']];p=PurePosixPath(a.filename);canonical='/'.join(p.parts)
  check(not p.is_absolute() and '..' not in p.parts and '\\' not in a.filename and canonical not in seen,'safe canonical member path');seen.add(canonical)
  check(not(a.flag_bits&1) and stat.S_IFMT(a.external_attr>>16) in (0,stat.S_IFREG),'unencrypted regular payload')
  b=z.read(a);check(hashlib.sha256(b).hexdigest()==item['sha256'] and len(b)==item['bytes'],'native CRC-read complete member')
  check(sha(Path(item['path']))==item['sha256'],'exact extracted original payload')
tex=[a for a in items if a['path'].endswith('.tex')]
check(len(tex)==1 and tex[0]['path']==r['controlling_TeX']['path'],'sole associated controlling TeX locator')
check(sha(Path(r['selected_actual_PDF']['path']))==r['selected_actual_PDF']['sha256'],'actual standalone published reader')
for item in r['all_embedded_PDF_members']:
 check((item['sha256']==r['selected_actual_PDF']['sha256'])==item['byte_identical_to_standalone_reader'],'embedded reader identity')
check(not r['target_mathematics_scientifically_read'] and not r['source_programs_executed_or_scientifically_read'],'acquisition-only exposure status')
if (E/'MANIFEST.json').exists():
 seal=json.loads((E/'SEAL.json').read_text());check(sha(E/'MANIFEST.json')==seal['manifest_sha256'],'acquisition manifest seal')
 for item in json.loads((E/'MANIFEST.json').read_text())['files']:
  f=E/item['path'];check(f.stat().st_size==item['bytes'] and sha(f)==item['sha256'],'acquisition evidence '+item['path'])
 check(sha(E/'REPORT.md')==seal['report_sha256'],'acquisition report seal')
print(json.dumps({'status':'PASS','record_id':r['record_id'],'custody_checks':checks,'regular_members':len(items),'no_scientific_assessment':True,'all_original_source_bytes_unchanged':True},indent=2))
