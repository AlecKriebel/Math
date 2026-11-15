#!/usr/bin/env python3
"""Read-only full native-source, original-order and initial/primary custody."""
from pathlib import Path
import hashlib,json,zipfile,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; P=R.parents[1]; S=P/'sources'
def ck(t,m):
 if not t:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def item(base,x):
 p=base/x['path'];ck(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'payload mismatch: '+str(p))
ck(sha(S/'SOURCE_READY.json')=='61f1a6961c0255fd94bc9789fb468b7baded2a37f988ef0b3000a272306b77cf','source ready pin')
ck(sha(S/'SOURCE_READY_MANIFEST.json')=='920c3b39ec724a447acf6e89585777a3e7bb8b565c37b4be020d5c411fb597fc','native manifest independent pin')
ck(sha(S/'SOURCE_READY_SEAL.json')=='261a600daceedfcfe27f8f0b09ae39beb17049c307dad6d4b29fa45b7e6a6b49','native seal independent pin')
ss=read(S/'SOURCE_READY_SEAL.json');sm=read(S/'SOURCE_READY_MANIFEST.json')
ck(sha(S/'SOURCE_READY_MANIFEST.json')==ss['manifest_sha256'],'source manifest pin')
for x in sm['files']:item(S,x)
ck({str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}=={x['path'] for x in sm['files']}|{'SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'},'native file set changed')
ready=read(S/'SOURCE_READY.json');record=read(S/'record.raw.json');latest=read(S/'latest.raw.json')
assets=ready['all_assets_in_original_order']
ck(record['files']==latest['files']==[x['original_api_file_object'] for x in assets],'whole original public file objects/order')
ck([x['key'] for x in record['files']]==['source-and-verification.zip','paper.pdf'],'native ZIP/PDF order')
ck(record['metadata']['version']==ready['version']=='1.0.0','exact version')
ck(record['metadata']['publication_date']==ready['publication_date']=='2026-10-17','original publication date')
ck(record['metadata']['license']['id']=='cc-by-4.0','native license identity')
for x in assets:
 p=Path(x['path']);item(Path('/'),x)
 ck(hashlib.md5(p.read_bytes()).hexdigest()==x['md5']==x['original_api_file_object']['checksum'][4:],'original checksum')
 ck(x['bytes']==x['original_api_file_object']['size'],'original asset length')
members=read(S/'archive-members.json')['full_original_ordered_regular_occurrences']
preview=read(S/'archive-directory-preview.json')['all_original_ordered_entries']
with zipfile.ZipFile(S/'source-and-verification.zip') as z:
 infos=z.infolist();ck(len(infos)==len(preview),'all original ZIP directory entries')
 for i,(a,b) in enumerate(zip(infos,preview)):
  ck(a.filename==b['original_member_name'] and i==b['ordinal'] and a.is_dir()==b['directory'] and a.file_size==b['bytes'] and a.compress_size==b['compressed_bytes'] and f'{a.CRC:08x}'==b['CRC32'] and (a.external_attr>>16)==b['mode'] and a.flag_bits==b['flags'],'original ZIP directory metadata/order')
 regular=[(i,a) for i,a in enumerate(infos) if not a.is_dir()];ck(len(regular)==len(members)==16,'all regular occurrences')
 for (i,a),b in zip(regular,members):
  raw=z.read(a);extracted=S/'published-source'/b['canonical_extraction_relative_path']
  ck(i==b['ordinal'] and a.filename==b['original_member_name'],'ZIP native ordered occurrence')
  ck(raw==extracted.read_bytes() and len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],'complete ZIP payload equality')
ck((S/'paper.pdf').read_bytes()==(S/'published-source/kourovka-21-149/paper.pdf').read_bytes(),'both reader copies identical')
ck(sha(R/'INITIAL_SEAL.json')=='3eb58109fb69edb448cbaaa69d96d3ac574a7f0ced867e6a1d1458ea3e2b3611','own early seal preserved')
initial=read(R/'INITIAL_SEAL.json');im=read(R/'INITIAL_MANIFEST.json')
ck(sha(R/'INITIAL_MANIFEST.json')==initial['manifest_sha256'],'initial manifest')
for x in im['files']:item(R,x)
prim=read(R/'PRIMARY_BINDINGS.json')['bindings']
for x in prim:item(Path('/'),x)
historical=read(S/'published-source/kourovka-21-149/source_manifest.json')
for a,b in zip(historical,[x for x in prim if x['name'] in ['Notebook October6 exact','Notebook October6 updates exact']]):ck(a['sha256']==b['sha256'] and a['url']==b['url'],'exact historical primary pin')
lean=next(x for x in prim if x['name']=='Pinned Lean complete');raw=Path(lean['path']).read_bytes()
ck(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='16171b31d31c07ba433fa19b73408d515fc9eebb','complete pinned Lean Git blob')
print(json.dumps({'assessment':'NATIVE_SOURCE_ORDER_AND_EARLY_INDEPENDENT_CUSTODY_SUPPORTED','native_manifest_payloads':len(sm['files']),'native_total_files':len(sm['files'])+2,'complete_ZIP_regular_occurrences':len(members),'original_public_asset_objects':len(assets),'preserved_initial_payloads':len(im['files']),'external_primary_bindings':len(prim),'source_mutations':False,'whole_original_objects_and_order':True,'literal_native_version':ready['version'],'literal_publication_date':ready['publication_date'],'source_ready_sha256':sha(S/'SOURCE_READY.json')},sort_keys=True,indent=2))
