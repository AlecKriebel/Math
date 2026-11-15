"""Stdlib-only custody closure: imports/executes no target or review programme."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,stat
OWN=Path(__file__).resolve().parent
SOURCE=OWN.parents[1]/'sources'
def need(ok,label):
 if not ok:raise ValueError('native_custody:'+label)
def parse(data):
 def pairs(rows):
  o={}
  for k,v in rows:need(k not in o,'duplicate_JSON_key');o[k]=v
  return o
 return json.loads(data,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite_JSON')))
def load(p):return parse(Path(p).read_bytes())
def bind(p):d=Path(p).read_bytes();return {'bytes':len(d),'SHA256':hashlib.sha256(d).hexdigest()}
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def source_path(p):
 p=Path(p);need(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(SOURCE.resolve()),'regular_contained_source_input')
 need(all(not q.is_symlink() for q in p.parents if q.is_relative_to(SOURCE)),'source_no_symlink_parent');return p
def verify_snapshot(snapshot=None):
 s=load(OWN/'NATIVE_OBJECTS_SNAPSHOT.json') if snapshot is None else snapshot
 need(same(load(SOURCE/'SOURCE_READY.json'),s['whole_original_SOURCE_READY']),'whole_readiness_history_native_shape')
 for row in s['whole_original_API_objects']:
  p=source_path(row['path']);need(bind(p)=={k:row[k] for k in ['bytes','SHA256']} and same(load(p),row['whole_literal_original_object']),'whole_native_API_object_key_value_type_order')
 row=s['whole_original_transport_aggregate'];p=source_path(row['path']);need(bind(p)=={k:row[k] for k in ['bytes','SHA256']} and same(load(p),row['whole_literal_original_object']),'whole_native_transport_headers_shape_order')
 return len(s['whole_original_API_objects'])
def central(info,n):return {'ordinal_zero_based':n,'filename':info.filename,'original_filename':info.orig_filename,'is_directory':info.is_dir(),'bytes':info.file_size,'compressed_bytes':info.compress_size,'CRC32':format(info.CRC,'08x'),'flags':info.flag_bits,'compression':info.compress_type,'native_date_time':list(info.date_time),'external_attr':info.external_attr,'internal_attr':info.internal_attr,'create_system':info.create_system,'create_version':info.create_version,'extract_version':info.extract_version,'header_offset':info.header_offset,'extra_hex':info.extra.hex(),'comment_hex':info.comment.hex()}
def verify_archives(custody=None):
 c=load(SOURCE/'ARCHIVE_CUSTODY.json') if custody is None else custody;need(len(c['containers'])==4 and len(c['all_safe_regular_occurrences'])==195,'all_four_containers195_occurrences');rows={(r['container_id'],r['ordinal_zero_based']):r for r in c['all_safe_regular_occurrences']};need(len(rows)==195,'unique_native_occurrence_locators');checked=0
 for container in c['containers']:
  p=source_path(container['path']);need(bind(p)=={k:container[k] for k in ['bytes','SHA256']},'whole_native_archive_bytes')
  with zipfile.ZipFile(p) as z:
   infos=z.infolist();need(len(infos)==container['native_member_count_including_directories'] and same([central(i,n) for n,i in enumerate(infos)],container['whole_original_central_directory']) and z.comment.hex()==container['archive_comment_hex'],'every_native_central_directory_field_and_order')
   for n,info in enumerate(infos):
    if info.is_dir():continue
    r=rows[(container['container_id'],n)];name=info.filename;need(not PurePosixPath(name).is_absolute() and '\\' not in name and all(x not in {'','..','.'} for x in name.split('/')),'safe_exact_member_name');raw=z.read(info);ep=source_path(r['extracted_path']);need(name==r['original_member_name'] and len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['SHA256'] and format(info.CRC,'08x')==r['CRC32'] and raw==ep.read_bytes(),'all195_CRC_size_SHA256_and_full_extracted_bytes');checked+=1
 need(checked==195,'all_payloads_not_sampled');return checked
def verify_original58():
 root=SOURCE/'published-source';manifest=load(root/'MANIFEST.json');rows=manifest['files'];actual={str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file()};need(len(rows)==150 and set(actual)=={r['path'] for r in rows}|{'MANIFEST.json'},'entire151_outer_published_files')
 for r in rows:
  b=bind(actual[r['path']]);need(b=={'bytes':r['bytes'],'SHA256':r['sha256']},'all150_published_manifest_bindings')
 identity=load(root/'audit/intake/ROOT_SOURCE_IDENTITY.json');need(len(identity['original_files'])==58,'complete_original58_list')
 for r in identity['original_files']:
  p=source_path(root/'audit/intake/original'/r['path']);raw=p.read_bytes();need(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==r['git_blob'],'all58_original_whole_bytes_and_blob_hashes_without_Git')
 selected=load(root/'audit/intake/SELECTED_PUBLIC_RECORD.json');need(hashlib.sha256(selected['problem']['statement'].encode()).hexdigest()==identity['statement_sha256'],'selected_statement_exact_bytes');need(hashlib.sha256(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode()).hexdigest()==identity['review_hash'],'whole_selected_problem_prior_pair_opaque_binding');return 58
def verify():
 frozen=load(OWN/'SOURCE_NATIVE_MANIFEST.json');need(bind(SOURCE/'SOURCE_READY.json')['SHA256']=='f7cfd3d2e4f2633929fa9e30c04ffd08bc7e22de9f15fba6f0cd46ca99e92e4f','externally_pinned_SOURCE_READY');before={str(p):bind(p) for p in SOURCE.rglob('*') if p.is_file()};need(set(before)=={r['path'] for r in frozen['files']} and len(before)==232,'complete_source232_namespace')
 for r in frozen['files']:need(before[r['path']]=={k:r[k] for k in ['bytes','SHA256']},'every_unchanged_source_file')
 api=verify_snapshot();payloads=verify_archives();originals=verify_original58();ready=load(SOURCE/'SOURCE_READY.json')
 for a in ready['all_native_assets_in_original_order']:
  raw=source_path(a['path']).read_bytes();need(len(raw)==a['bytes']==a['original_api_file_object']['size'] and hashlib.sha256(raw).hexdigest()==a['SHA256'] and 'md5:'+hashlib.md5(raw).hexdigest()==a['original_api_file_object']['checksum'],'whole_native_assets_and_native_checksums')
 need({str(p):bind(p) for p in SOURCE.rglob('*') if p.is_file()}==before,'source_read_only_before_after')
 return {'literal_custom_status':'WHOLE_NATIVE_SOURCE_OBJECTS195_PAYLOADS58_ORIGINALS_AND232_FILES_UNCHANGED','source_files':len(before),'native_API_objects':api,'archive_containers':4,'outer_regular_payloads':151,'nested_regular_payloads':44,'whole_regular_payloads':payloads,'original58_files_and_blob_hashes':originals,'whole_original_swh_empty_object_vs_null_and_files_empty_fields_preserved':True,'source_imports_programme_execution_network_or_writes':False,'historical_full_dataset_rehash_claimed':False}
def verify_packet():
 result=verify()
 if not (OWN/'FINAL_SEAL.json').exists():return result
 before={str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()}
 need(not any(p.is_symlink() for p in OWN.rglob('*')),'owned_no_symlinks')
 seal=load(OWN/'FINAL_SEAL.json');manifest=load(OWN/'OWNED_MANIFEST.json');need(bind(OWN/'OWNED_MANIFEST.json')['SHA256']==seal['OWNED_MANIFEST_SHA256'],'final_manifest_seal')
 rows=manifest['files'];names={r['path'] for r in rows};need(len(rows)==len(names) and set(before)==names|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'complete_final_owned_namespace')
 for r in rows:
  p=OWN/r['path'];need(p.resolve().is_relative_to(OWN) and not p.is_symlink() and bind(p)=={k:r[k] for k in ['bytes','SHA256']},'every_owned_complete_byte:'+r['path'])
 need(bind(OWN/'INITIAL_SEAL.json')['SHA256']=='23f817696da1a15555e64adaf26b9e5374b36865931712be06ddc960790400ed','externally_notified_initial_seal_immutable')
 initial=load(OWN/'INITIAL_SEAL.json');need(bind(OWN/'INITIAL_MANIFEST.json')['SHA256']==initial['INITIAL_MANIFEST_SHA256'],'initial_manifest_original')
 for r in load(OWN/'INITIAL_MANIFEST.json')['files']:need(bind(OWN/r['path'])=={k:r[k] for k in ['bytes','SHA256']},'every_original_initial_payload_still_immutable')
 for key,name in [('REPORT_SHA256','REPORT.md'),('VERDICT_SHA256','VERDICT.json'),('DERIVATIONS_SHA256','DERIVATIONS.md'),('PRIMARY_INTERFACES_SHA256','PRIMARY_INTERFACES.md'),('FINAL_EXPOSURE_SHA256','FINAL_EXPOSURE_LOG.json'),('SOURCE_NATIVE_MANIFEST_SHA256','SOURCE_NATIVE_MANIFEST.json')]:need(bind(OWN/name)['SHA256']==seal[key],'explicit_final_payload_binding:'+name)
 for r in load(OWN/'PRIMARY_NATIVE_BINDINGS.json')['actual_transport_body_bindings']:need(bind(r['path'])=={k:r[k] for k in ['bytes','SHA256']},'actual_foreign_primary_transport_bytes')
 gate=load(OWN/'ROOT_GATE_RECEIPT.json');need(bind(gate['authority_path'])['SHA256']==gate['authority_SHA256'] and gate['authority_body_or_root_scientific_reconstruction_read'] is False,'opaque_root_gate_authority_only')
 need({str(p.relative_to(OWN)):bind(p) for p in OWN.rglob('*') if p.is_file()}==before,'final_custody_is_read_only')
 return {'literal_custom_status':'SEALED_INDEPENDENT_ADVERSARIAL_PACKET_AND_WHOLE_NATIVE_CUSTODY_VALIDATED','owned_payloads':len(rows),'initial_payloads_unchanged':len(load(OWN/'INITIAL_MANIFEST.json')['files']),'native':result,'own_mathematical_diagnostics_reproduced_preseal_in_normal_and_optimized_modes':True,'target_or_peer_programme_import_or_execution':False,'current_peer_opinions_read':False,'network_or_file_writes':False,'publication_authority':False}
if __name__=='__main__':print(json.dumps(verify_packet(),indent=2))
