"""Standalone pure row133 metadata/opaque custody verifier.
Only stdlib imports. No project imports, network, subprocess, scientific code,
rendering, bytecode generation, or writes. Original scientific bytes are hashed
opaquely; only explicitly frozen native/custody metadata JSON is parsed.
"""
from pathlib import Path
from hashlib import sha256,md5
import json,sys,zipfile,io,zlib
A=Path(__file__).resolve().parent
checks=0
def need(ok,label):
 global checks
 checks+=1
 if not ok:raise ValueError(label)
def binding(b):return {'bytes':len(b),'SHA256':sha256(b).hexdigest()}
def read(p):
 need(p.is_file() and not p.is_symlink(),'regular nonsymlink '+str(p));return p.read_bytes()
def load(p):return json.loads(read(p))
def same(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def namespace(p):
 allp=list(p.rglob('*'));need(not any(x.is_symlink() for x in allp),'namespace symlinks forbidden')
 return sorted(str(x.relative_to(p)) for x in allp if x.is_file())
need(sys.argv[1:] in ([],['--preseal']),'bounded option')
preseal=sys.argv[1:]==['--preseal'];m=load(A/'INPUT_MANIFEST.json');contract=load(A/'WHOLE_LITERAL_NATIVE.json');S=Path(m['source_root'])
need(m['original_source_regular_files']==len(m['files'])==87,'whole87 source files')
need(namespace(S)==m['source_namespace'],'complete actual original source namespace, no exclusions')
need(namespace(A/'raw')==m['source_namespace'],'complete raw namespace, no exclusions')
need(read(A/'.gitignore').decode().splitlines()==['raw/'] and m['raw_entire_folder_ignored_before_creation'] is True,'entire raw folder ignored beforecopy')
lookup={row['original']:row for row in m['files']}
for row in m['files']:
 b=read(A/row['copy']);need(binding(b)=={'bytes':row['bytes'],'SHA256':row['SHA256']},'whole raw original byte custody')
 need(read(Path(row['original']))==b,'actual original whole byte identity')
def original_raw(path):return A/lookup[str(Path(path))]['copy']
r=contract['SOURCE_READY_whole_literal'];seal=contract['SOURCE_READY_SEAL_whole_literal']
need(binding(read(A/'raw/SOURCE_READY.json'))['SHA256']=='28a9736d92beaadb1faa37c9146d56191be83fb217116f24b33162bea922e469','exact source ready authority pin')
need(binding(read(A/'raw/SOURCE_READY_SEAL.json'))['SHA256']=='c523e830e06555037254c26d9d85c82f4324c841cdd268f99d95664bf02e2150','exact source final seal authority pin')
whole_pairs=[(S/'SOURCE_READY.json','SOURCE_READY_whole_literal'),(S/'SOURCE_READY_SEAL.json','SOURCE_READY_SEAL_whole_literal'),(S/'ALL_TRANSPORT_RECEIPTS.json','transport_aggregate_whole_literal'),(S/'NATIVE_SCHEMA_TYPES.json','schema_whole_literal'),(S/'ARCHIVE_CUSTODY.json','archive_custody_whole_literal'),(S/'MANUSCRIPT_CUSTODY.json','manuscript_custody_whole_literal'),(S/'SOURCE_READY_MANIFEST.json','source_manifest_whole_literal'),(S/'SOURCE_READY_CLOSURE.json','source_closure_whole_literal'),(S/'INPUT_MANIFEST.json','source_input_manifest_whole_literal')]
for p,key in whole_pairs:need(same(load(original_raw(p)),contract[key]),'whole typed/key/list/order/null object '+key)
need(len(r['whole_native_API_objects'])==len(contract['native_API_whole_literal'])==4,'actual4native APIs')
for d,object_ in zip(r['whole_native_API_objects'],contract['native_API_whole_literal']):
 need(binding(read(original_raw(d['path'])))=={'bytes':d['bytes'],'SHA256':d['SHA256']},'native API original descriptor')
 need(same(load(original_raw(d['path'])),object_),'whole typed/key/list/order/null native API')
transports=contract['transport_aggregate_whole_literal'];need(type(transports) is list and len(transports)==7,'actual transport aggregate list7; no schema coercion')
need(type(contract['schema_whole_literal']) is list and len(contract['schema_whole_literal'])==403,'actual403-row schema list; no coercion')
need([x['HTTP_status'] for x in transports]==r['HTTP_status_sequence']==[200,301,200,200,200,200,200],'literal request/redirect order')
for t,original in zip(transports,contract['seven_transport_objects_whole_literal']):
 need(same(t,original) and same(load(original_raw(t['body_path']+'.transport.json')),t),'whole transport object type/key/header/list/order/null identity')
 need(binding(read(original_raw(t['body_path'])))=={'bytes':t['bytes'],'SHA256':t['SHA256']},'whole actual transport response body')
 need(type(t['actual_request_headers_in_sent_order']) is list and type(t['response_headers_in_received_order']) is list,'actual ordered native headers')
record,latest,versions,files=contract['native_API_whole_literal']
need(record['id']==latest['id']==r['record_id']==23331331,'original record identity')
need(type(record['conceptrecid']) is str and record['conceptrecid']=='23331330','native concept identifier string retained')
need(same(record['swh'],{}) and same(latest['swh'],{}),'native record/latest empty objects')
need(versions['hits']['hits'][0]['swh'] is None,'native version-hit null distinct from empty/missing')
need(type(files['entries']) is list and same(files['order'],[]) and files['default_preview']=='outer_pedal_centroid.pdf','native files list/order/preview actualstring')
need(type(files['default_preview']) is str,'defaultpreview string not null or missing')
assets=r['all_native_assets_in_original_order'];need(len(assets)==2 and [Path(x['path']).suffix for x in assets]==['.zip','.pdf'],'native ZIP then PDF order')
for i,a in enumerate(assets):
 b=read(original_raw(a['path']));need(binding(b)=={'bytes':a['bytes'],'SHA256':a['SHA256']} and 'md5:'+md5(b).hexdigest()==a['original_api_file_object']['checksum'],'complete native asset SHA/MD5/size')
 need(same(record['files'][i],a['original_api_file_object']),'original record file object and ordinal')
 match=[x for x in files['entries'] if x['key']==a['original_api_file_object']['key']]
 need(len(match)==1 and same(match[0],a['whole_original_native_files_entry']),'whole files-entry object preserved withoutflattening')
archive=contract['archive_custody_whole_literal'];occ=archive['regular_payload_occurrences'];need(len(occ)==38 and len(archive['containers'])==1 and r['whole_regular_payload_occurrences']==38 and r['recursive_archive_container_count']==1,'whole38 payloads1container')
opaque=load(A/'ARCHIVE_OPAQUE_COMPARISONS.json');need(len(opaque['checks'])==38,'all38 opaquecomparison receipts')
with zipfile.ZipFile(io.BytesIO(read(original_raw(assets[0]['path'])))) as z:
 regular=[x for x in z.infolist() if not x.is_dir()];need(len(regular)==38,'actual completeZIP38regular entries')
 byname={x.filename:x for x in regular};need(len(byname)==38,'literal ZIP namesunique')
 for o,e in zip(occ,opaque['checks']):
  info=byname[o['original_member_name']];b=z.read(info)
  need(b==read(original_raw(o['extracted_path'])) and binding(b)=={'bytes':o['bytes'],'SHA256':o['SHA256']},'complete opaqueZIPmember/extracted identity')
  need(info.CRC==(zlib.crc32(b)&0xffffffff) and f'{info.CRC:08x}'==o['CRC32'],'whole native CRC')
  need(e['original_member_name']==o['original_member_name'] and e['opaque_bytes_equal'] is True and e['SHA256']==o['SHA256'] and e['CRC32']==o['CRC32'],'opaque comparisonreceipt literal')
  need(e['compressed_bytes']==info.compress_size and e['compression_method']==info.compress_type and e['whole_original_external_attr']==info.external_attr and e['whole_original_flags']==info.flag_bits and e['whole_original_date_time']==list(info.date_time),'whole native ZIPmetadata retained')
need(r['selected_actual_PDF']['pages']==5 and r['controlling_TeX']['opaque_byte_splitlines_count']==342,'actual source page/linecount metadata')
need(len(read(original_raw(r['controlling_TeX']['extracted_path'])).splitlines())==342,'actual opaque342TeXlinecount')
need(r['completion_percent_at_preseal']==100 and seal['completion_percent']==100,'actual historical100not95')
for flag in ['printed_title_date_version_inspected','target_PDF_text_extracted','target_PDF_rasters_visually_read','mathematical_PDF_TeX_or_pixels_read','TeX_preamble_or_mathematical_body_read','source_scientific_proofs_code_results_triage_reviews_or_opinions_read']:need(r[flag] is False,'source historicalunreadflag '+flag)
need(r['target_PDF_pages_rendered'] is True and r['scientific_verdict'] is None and r['publication_authority'] is False and r['source_programmes_executed']==[],'source historical rendered/unread/null/nonexecution distinctions')
need(same(r['native_schema_distinctions']['files_default_preview'],{'present':True,'original_value':'outer_pedal_centroid.pdf'}),'wholepreview presence/valueobject')
owned=contract['source_manifest_whole_literal'];ex=owned['excluded_terminal_files']
need(ex==['SOURCE_READY_CLOSURE.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json'],'exact original rootterminal exclusions')
need(len(owned['files'])==84 and len(m['source_namespace'])==87,'owner84plus3rootterminals guardedaswhole87')
for row in owned['files']:
 p=Path(row['path']);p=p if p.is_absolute() else S/p
 need(binding(read(original_raw(p)))=={'bytes':row['bytes'],'SHA256':row['SHA256']},'whole originalowner manifest binding')
initial=load(A/'INITIAL_SEAL.json')
for p,e in initial['frozen_input_payloads'].items():need(binding(read(A/p))==e,'unchangedinitial metadataseal payload')
if not preseal:
 final=load(A/'SEAL.json');manifest=load(A/'MANIFEST.json')
 need(binding(read(A/'MANIFEST.json'))==final['manifest'],'whole own finalmanifest seal')
 need(sorted(set(namespace(A))-{'MANIFEST.json','SEAL.json'})==sorted(manifest['payloads']),'whole own namespace exactrootterminalexclusions')
 for p,e in manifest['payloads'].items():need(binding(read(A/p))==e,'whole ownpayload')
 need(load(A/'CUSTOM_VERDICT.json')['scientific_verdict'] is None,'no scientificdispositionconveyed')
print(json.dumps({'scope':'row133 metadata/opaque custody only','mode':'preseal' if preseal else 'sealed default custody','positive_checks':checks,'original_source_files':87,'whole_native_API_objects':4,'actual_transports':7,'whole_ZIP_payloads':38,'containers':1,'own_scientific_reading_or_execution':False,'project_imports_network_subprocess_or_writes':False},ensure_ascii=False,indent=2))
