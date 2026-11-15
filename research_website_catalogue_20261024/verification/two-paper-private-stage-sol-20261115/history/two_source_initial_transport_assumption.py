"""Exact two-record heterogeneous native/editorial views; originals immutable."""
from two_common import *
from two_dom import Tree,text
import re
def authenticate():
 seal=load(OWN/'SOURCE_INPUT_SEAL.json');need(bind(OWN/'SOURCE_INPUTS.json')['sha256']==seal['source_inputs_sha256'],'source_freeze_seal');need(bind(OWN/'PRIVATE_POLICY.json')['sha256']==seal['policy_sha256'],'initial_policy_unchanged')
 frozen=load(OWN/'SOURCE_INPUTS.json');need(list(frozen['records'])==list(IDS),'two_explicit_record_order')
 for r in frozen['input_files']:need(bind(r['path'])=={k:r[k] for k in ['bytes','sha256']},'every_complete_frozen_input:'+r['path'])
 return frozen
def view_record(rid,o):
 paper=PROGRAMME/'papers'/rid;ready=load(paper/'sources/SOURCE_READY.json');c=load(paper/'publication.json');p=load(paper/'promotion.json')
 need(same(ready,o['whole_SOURCE_READY_original']) and same(c,o['whole_publication_original']) and same(p,o['whole_promotion_original']),'whole_source_ready_publication_promotion_objects:'+rid)
 for role,x in o['whole_native_API_objects_original'].items():
  a=x['binding_original'];path=contained(paper,a['path']);need(bind(path)=={'bytes':a['bytes'],'sha256':a['SHA256']} and same(load(path),x['whole_original_object']),'complete_native_API_object:'+rid+':'+role)
 record=o['whole_native_API_objects_original']['record']['whole_original_object'];need(str(record['id'])==rid and record['doi']==c['doi'] and c['title']==record['metadata']['title'],'native_identity_title_DOI:'+rid)
 raw_receipts=load(contained(paper,ready['actual_transport_receipt_path']));need(same(raw_receipts,o['whole_native_transport_aggregate_original']),'whole_original_transport_shapes_and_order:'+rid)
 if rid=='23385145':
  need(type(raw_receipts) is dict and len(raw_receipts['receipts'])==7,'118_native_seven_receipt_envelope');receipts=raw_receipts['receipts']
  need(all(r['status']==200 for r in receipts),'118_original_transport_statuses')
 else:
  need(type(raw_receipts) is list and len(raw_receipts)==8,'119_native_eight_receipt_list');receipts=raw_receipts
  need([r['HTTP_status'] for r in receipts].count(400)==1 and [r['HTTP_status'] for r in receipts].count(200)==7,'119_failed_request_and_recovery_preserved')
  original=load(paper/p['transport_receipt_paths']['record']);need(same(original,p['whole_native_record_transport_receipt']),'119_separate_record_receipt_shape_not_enriched')
 assets=[]
 need(same(record['files'],[a['original_api_file_object'] for a in ready['all_assets_in_original_order']]),'every_native_file_object_and_original_order:'+rid)
 for a in ready['all_assets_in_original_order']:
  api=a['original_api_file_object'];name=safe_name(api['key']);path=contained(paper,a['path']);data=path.read_bytes();md5=hashlib.md5(data).hexdigest()
  need(len(data)==a['bytes']==api['size'] and sha(data)==a['sha256'] and md5==a['md5'] and api['checksum']=='md5:'+md5,'whole_native_asset_identity:'+rid+':'+name);assets.append({'name':name,'path':str(path),'original_native_asset':a,'bytes':len(data),'sha256':sha(data)})
 need(len(assets)==(2 if rid=='23385145' else 3),'all_native_assets_including119_checksums');pdf=next(a for a in assets if a['name'].endswith('.pdf'));zipasset=next(a for a in assets if a['name'].endswith('.zip'))
 selected=ready['selected_actual_PDF'];need(bind(selected['path'])=={'bytes':selected['bytes'],'sha256':selected['SHA256']} and pdf['sha256']==selected['SHA256'],'actual_complete_native_reader:'+rid)
 need(c['pdf_filename']==pdf['name'] and c['supplement_filename']==zipasset['name'] and c['pdf_pages']==selected['pages'],'exact_editorial_asset_names_pages')
 need(c['publication_date']==record['metadata']['publication_date'] and c['version']==record['metadata']['version'],'native_date_and_version_not_creation_date:'+rid)
 need(record['metadata']['license']=={'id':'cc-by-4.0'} and c['license_url']=='https://creativecommons.org/licenses/by/4.0/' and c['code_license']==(None if rid=='23385145' else 'MIT'),'actual_mixed_rights_not_invented')
 for key in ['canonical_url','AA','follow_up']:need(c[key] is None and p[key] is None,'unchanged_original_null_flag:'+rid+':'+key)
 for key in ['rendered','deployed','rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified']:need(p[key] is False,'unchanged_original_closed_gate:'+rid+':'+key)
 need(p['native_sheet_aa_url'] is None,'original_native_AA_not_assigned')
 science=root_authority(rid,SCIENCE);editorial=root_authority(rid,EDITORIAL);need(same(science,o['whole_scientific_root_authority_original']) and same(editorial,o['whole_editorial_root_authority_original']),'whole_root_science_and_later_editorial_authorities:'+rid)
 need(same(p['whole_root_scientific_clearance_record'],science),'exact_custom_scientific_authority_not_GENERIC_PASS')
 if rid=='23385145':
  need(editorial['decision']=='ROOT_ADOPTED_COMPLETE_EDITORIAL_COPY_AND_UNIQUE_CONFIGURATION_PROSE_FOR_LATER_PRIVATE_STAGE' and editorial['production_installation_or_live_native_authority'] is False,'118_private_editorial_authority_only')
  for a in editorial['bindings']:need(bind(PROGRAMME/a['path'])=={'bytes':a['bytes'],'sha256':a['sha256']},'118_all_root_bound_editorial_files')
 else:
  need(editorial['status']=='ROOT_FULL_EDITORIAL_COPY_AND_CONFIG_ADOPTED_FOR_SEPARATE_PRIVATE_STAGING' and editorial['production_installation_authority'] is False,'119_private_editorial_authority_only')
  for path,wanted in editorial['pins'].items():need(bind(PROGRAMME/path)['sha256']==wanted,'119_all_root_bound_editorial_files')
 need(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',c['slug']) is not None and c['proposed_canonical_url']=='https://aleckriebel.com/research/'+c['slug']+'/','safe_exact_proposed_slug')
 bib=(paper/o['layout']['bib']).read_bytes();need(bib.decode()==c['prepared_bibtex'],'whole_prepared_citation')
 sections=load(paper/'reviews/editorial/public-sections.json');need(same(sections,o['whole_public_sections_original']),'whole_editorial_section_copy')
 return {'rid':rid,'paper':paper,'original':o,'ready':ready,'record':record,'c':c,'p':p,'assets':assets,'pdf':pdf,'zip':zipasset,'bib':bib,'sections':sections,'title':c['title'],'slug':c['slug'],'description':c['description'],'publication_date':c['publication_date'],'version':c['version'],'doi':c['doi'],'abstract':c['abstract'],'kind':'Unrefereed preprint','source_html':(paper/o['layout']['source_html']).read_text() if rid=='23385145' else None,'public_copy':(paper/'reviews/editorial/PUBLIC_COPY.md').read_text(),'metadata':load(paper/o['layout']['metadata']) if rid=='22983513' else None}
def load_bundles():
 f=authenticate();return [view_record(rid,f['records'][rid]) for rid in IDS]
