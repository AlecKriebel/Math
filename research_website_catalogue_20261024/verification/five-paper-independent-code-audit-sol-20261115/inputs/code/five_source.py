"""Read-only, bounded native/editorial adapters. Whole originals stay literal."""
from five_common import *
from five_markup import Tree,text
import re
def authenticate_inputs():
 authorize_editorials()
 seal=load(OWN/'INPUT_FREEZE_SEAL.json')
 for name,key in [('FROZEN_INPUT_SET.json','frozen_inputs_sha256'),('FRESH_BASELINE.json','baseline_sha256'),('PRIVATE_STAGE_POLICY.json','policy_sha256'),('RECORD_LAYOUTS.json','record_layouts_sha256')]:
  need(bind(OWN/name)['sha256']==seal[key],'exact_saved_'+name)
 frozen=load(OWN/'FROZEN_INPUT_SET.json')
 for r in frozen['input_files']:need(bind(r['path'])=={k:r[k] for k in ['bytes','sha256']},'unchanged_whole_input:'+r['path'])
 need(list(frozen['records'])==list(IDS),'exact_five_records')
 need(seal['all_five_editorials_final_before_integration'] is True and seal['production_install_authorized'] is False and seal['AA'] is None,'private_only_input_freeze')
 return frozen
def view_record(rid,original):
 """Temporary rendering view; does not create a substitute source schema."""
 paper=PROGRAMME/'papers'/rid;layout=original['layout'];ready=load(paper/'sources/SOURCE_READY.json')
 need(same(ready,original['source_ready_original']),'whole_native_readiness_shape_and_order:'+rid)
 recordpath=Path(ready['native_record_body_path']) if rid in {'23430498','23149775'} else paper/'sources/record.raw.json'
 record=load(contained(paper,recordpath));need(same(record,original['native_record_original']),'whole_original_record:'+rid)
 for name,raw in original['whole_native_root_JSON_objects'].items():need(same(load(paper/'sources'/name),raw),'whole_native_object:'+rid+':'+name)
 c=load(paper/layout['config']);p=load(paper/layout['promotion'])
 need(same(c,original['whole_config_original']) and same(p,original['whole_promotion_original']),'whole_frozen_editorial_configs:'+rid)
 need(same(load(paper/layout['editorial_seal']),original['editorial_seal_original']),'literal_editorial_seal:'+rid)
 for lane,raw in original['whole_three_custom_verdicts'].items():need(same(load(paper/'reviews'/lane/'VERDICT.json'),raw),'whole_custom_verdict_not_generic_PASS:'+rid+':'+lane)
 rootname,rootsha=CLEARANCES[rid];authority=PROGRAMME/'verification'/rootname
 need(bind(authority)['sha256']==rootsha and same(load(authority),original['whole_root_scientific_authority']),'whole_root_science_authority:'+rid)
 if rid in {'23430498','23149775'}:
  assets=ready['all_native_assets_in_original_order'];hashkey='SHA256';md5key='MD5'
 else:assets=ready['all_assets_in_original_order'];hashkey='sha256';md5key='md5'
 need(len(assets)==2 and same(record['files'],[x['original_api_file_object'] for x in assets]),'complete_original_public_file_objects_order:'+rid)
 meta=record['metadata'];need(str(record['id'])==rid and meta['license']=={'id':'cc-by-4.0'},'native_identity_license:'+rid)
 asset_view=[]
 for a in assets:
  api=a['original_api_file_object'];name=safe_name(api['key']);path=contained(paper,a['path']);data=path.read_bytes()
  need(len(data)==a['bytes']==api['size'] and sha(data)==a[hashkey],'native_whole_asset_bytes:'+rid+':'+name)
  md5=hashlib.md5(data).hexdigest();need(md5==a[md5key] and 'md5:'+md5==api['checksum'],'original_asset_checksum:'+rid)
  asset_view.append({'name':name,'path':str(path),'bytes':len(data),'sha256':sha(data),'native_original_object':a})
 pdf=next(a for a in asset_view if a['name'].lower().endswith('.pdf'));zipasset=next(a for a in asset_view if a['name'].lower().endswith('.zip'))
 selected=ready['selected_actual_PDF'];need(bind(selected['path'])=={'bytes':selected['bytes'],'sha256':selected[hashkey]},'actual_selected_reader:'+rid)
 need(pdf['sha256']==selected[hashkey],'exact_native_reader_not_rebuilt:'+rid)
 if layout['kind'] in {'config','html-config'}:
  need(c['canonical_url'] is None and c['AA'] is None and c['follow_up'] is None,'original_config_public_flags_unassigned:'+rid)
  for key in ['production_integration_authorized','publication_clearance','ready_to_publish','rendered_copy_verified','local_http_verified','deployed','live_verified','browser_verified','native_verified','canonical_verified']:
   need(p[key] is False,'original_private_promotion_flag:'+rid+':'+key)
  need(p['canonical_url'] is None and p['AA'] is None,'original_top_native_AA_unassigned:'+rid)
  title=c['title'];slug=c['slug'];description=c['description'];abstract=c['abstract'];kind=c['status'];source_html=None
  need(c['doi']==record['doi'] and c['publication_date']==meta['publication_date'] and c['version']==meta['version'],'top_config_native_edition_date:'+rid)
  need(c['pdf_filename']==pdf['name'] and c['supplement_filename']==zipasset['name'],'top_config_exact_assets:'+rid)
  if layout['kind']=='html-config':
   source_html=(paper/layout['html']).read_text();tree=Tree(source_html,source_math_style=True)
   need(text(tree.find('h1')[0])==title,'full115_preview_exact_title')
   scholar=strict_json(text(tree.find('script')[0]));need(scholar['abstract']==abstract,'full115_preview_abstract')
   kind=scholar['creativeWorkStatus']
 else:
  state=p['state'];need(state['AA'] is None and state['canonical_url'] is None and state['root_editorial_adoption'] is None,'nested_native_flags_unassigned:'+rid)
  for key in ['public_promotion_authority','production_config_authority','production_config_created','site_created','site_deployed','live_page_verified','browser_publication_gate','native_service_gate','tracker_gate','redirect_gate','git_gate','release_gate']:need(state[key] is False,'nested_original_private_gate:'+rid+':'+key)
  source_html=(paper/layout['html']).read_text();tree=Tree(source_html,source_math_style=True)
  need(len(tree.find('h1'))==len(tree.find('main'))==len(tree.find('article'))==1,'full_editorial_HTML:'+rid)
  title=text(tree.find('h1')[0]);slug=p['proposed']['slug'];abstract=(paper/layout['abstract']).read_text().strip()
  metas={n['attrs'].get('name'):n['attrs'].get('content') for n in tree.find('meta')};description=metas['description']
  scholar=strict_json(text(tree.find('script')[0]));kind=scholar['creativeWorkStatus']
  need(scholar['datePublished']==meta['publication_date'] and scholar['version']==meta['version'] and scholar['identifier']['value']==record['doi'],'nested_native_edition_date:'+rid)
  need(metas['robots']=='noindex,nofollow','original_private_HTML_retained:'+rid)
 need(title==meta['title'] and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug),'exact_title_and_safe_slug:'+rid)
 bibpath=contained(paper,layout['bib']);bib=bibpath.read_bytes();need(record['doi'].encode() in bib,'whole_prepared_citation_identity:'+rid)
 if rid=='23441890':need(b'day = {17}' in bib and b'month = oct' in bib and b'year = {2026}' in bib,'original_separate_BibTeX_date_fields113')
 else:need(meta['publication_date'].encode() in bib,'original_ISO_BibTeX_date_field:'+rid)
 return {'rid':rid,'paper':paper,'layout':layout,'original':original,'c':c,'p':p,'ready':ready,'record':record,
  'title':title,'slug':slug,'description':description,'abstract':abstract,'kind':kind,
  'publication_date':meta['publication_date'],'version':meta['version'],'doi':record['doi'],
  'asset_view':asset_view,'pdf':pdf,'zip':zipasset,'pages':selected['pages'],'bib':bib,'source_html':source_html}
def load_bundles():
 frozen=authenticate_inputs();bundles=[view_record(rid,frozen['records'][rid]) for rid in IDS]
 need(len({x['slug'] for x in bundles})==5,'five_distinct_work_slugs')
 return bundles
