#!/usr/bin/env python3
"""Read-only full native schemas, archive payload/order and early custody."""
from pathlib import Path
import json,hashlib,zipfile,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;S=R.parents[1]/'sources'
def ck(t,m):
 if not t:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text())
def item(base,x):
 p=base/x['path'];ck(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['SHA256'],'payload mismatch '+str(p))
for name,h in {'SOURCE_READY.json':'1f728d52dd3bb791833a837fb3bae7eab1b3a37ce7ecd9c4655b94f4d693cf46','SOURCE_READY_MANIFEST.json':'d9d203bd6d8f871a4fa436cda24efeea882146e33cf07f264ad845865b54be9d','SOURCE_READY_SEAL.json':'96ba3479d1fe1be42e4fa920037aa42d3fb7b47e8383620da87c1dce64569083'}.items():ck(sha(S/name)==h,'native independent pin '+name)
ready=js(S/'SOURCE_READY.json');manifest=js(S/'SOURCE_READY_MANIFEST.json')
ck(ready['schema']=='source-ready-23430498-native-custody-v1','actual native schema')
for x in manifest['files']:item(S,x)
ck({str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}=={x['path'] for x in manifest['files']}|{'SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'},'native file set changed')
record=js(S/'record-attempt2.body');latest=js(S/'latest.raw.json');assets=ready['all_native_assets_in_original_order']
ck(record['files']==latest['files']==[a['original_api_file_object'] for a in assets],'whole original public file objects and order')
ck([a['original_api_file_object']['key'] for a in assets]==['free-exterior-string-links-v1.0-source-audit-kit.zip','free-exterior-string-links-v1.0.pdf'],'original ZIP/PDF order')
ck(record['metadata']['publication_date']==ready['publication_date_declared']=='2026-10-13','declared original date')
ck(record['metadata']['version']==ready['version']=='1.0','exact version')
ck(record['metadata']['license']==ready['original_native_license_object']=={'id':'cc-by-4.0'},'complete native license object')
for x in assets:
 item(Path('/'),x);p=Path(x['path']);ck(hashlib.md5(p.read_bytes()).hexdigest()==x['MD5']==x['original_api_file_object']['checksum'][4:],'native MD5')
 ck(x['bytes']==x['original_api_file_object']['size'],'whole native asset length')
custody=js(S/'archive-custody.json');ck(len(custody['containers'])==1,'all native containers')
members=custody['regular_members'];archive=Path(custody['containers'][0]['source_path'])
with zipfile.ZipFile(archive) as z:
 infos=z.infolist();ck(len(infos)==len(members)==194 and all(not a.is_dir() for a in infos),'all original regular ZIP entries')
 for i,(a,b) in enumerate(zip(infos,members),1):
  ck(a.filename==b['original_member_name'] and i==b['entry_ordinal'],'native original ZIP order')
  ck(a.file_size==b['declared_uncompressed_bytes'] and a.compress_size==b['compressed_bytes'] and f'{a.CRC:08x}'==b['CRC32'],'all archive lengths and CRC')
  ck(a.flag_bits==b['flag_bits'] and a.compress_type==b['compression_method'] and list(a.date_time)==b['date_time'] and a.external_attr==b['external_attr'] and a.create_system==b['create_system'] and a.comment.hex()==b['comment_hex'] and a.extra.hex()==b['extra_hex'],'complete native ZIP transport metadata')
  raw=z.read(a);ck(raw==Path(b['extracted_path']).read_bytes() and len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['SHA256'],'whole ZIP member bytes')
ck(Path(ready['selected_actual_PDF']['path']).read_bytes()==Path(ready['selected_actual_PDF']['byte_identical_ZIP_members'][0]['extracted_path']).read_bytes(),'both complete reader copies')
ck(sha(R/'INITIAL_SEAL.json')=='c36d1d42f4db0c21985b48877c46c87937cf1ff6355d5ae395f1712ae66d8b60','own early seal')
ck(sha(R/'INITIAL_MANIFEST.json')==js(R/'INITIAL_SEAL.json')['manifest_SHA256'],'early manifest')
initial=js(R/'INITIAL_MANIFEST.json')
for x in initial['files']:item(R,x)
prim=js(R/'PRIMARY_BINDINGS.json')['bindings']
for x in prim:item(Path('/'),x)
for x in js(R/'SUPPLIED_EXECUTION_RECEIPTS.json'):
 ck(Path(x['native_path']).read_bytes()==Path(x['byte_identical_isolated_copy']).read_bytes(),'whole isolated arithmetic code equality')
 ck(x['exit_code']==0 and x['stderr_bytes']==0,'bounded supplied mode receipt')
print(json.dumps({'assessment':'FULL_NATIVE_SOURCE_SCHEMA_ORDER_AND_INDEPENDENT_INITIAL_CUSTODY_SUPPORTED','native_manifest_payloads':len(manifest['files']),'native_total_files':len(manifest['files'])+2,'all_ZIP_regular_occurrences':len(members),'original_public_asset_objects':len(assets),'preserved_initial_payloads':len(initial['files']),'external_primary_bindings':len(prim),'version':ready['version'],'publication_date':ready['publication_date_declared'],'source_mutations':False,'native_transport_objects_order_preserved':True},sort_keys=True,indent=2))
