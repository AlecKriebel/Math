"""Proposed authenticated consumer for exactly three immutable cleared records.
All original objects remain whole; only the returned asset view is ephemeral.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re
from bosonic_source import contained_file,digest
from published_assets import safe_relative
SG_IDS={'23181280','23442760','23395703'}
PINS=__PIN_LITERAL__
NORMALIZATIONS=__NORMALIZATION_LITERAL__
MATH=__MATH_LITERAL__
SCHEMAS={'23181280':('actual_assets','SHA256','MD5',2),'23442760':('all_actual_assets','sha256','md5',2),'23395703':('all_actual_assets','sha256','MD5',3)}
def require(value,tag):
    if not value:raise ValueError('spanning_sos_gin:'+tag)
def normalize_sg_abstract(rid,text):
    require(rid in SG_IDS,'unsupported_ID');text=' '.join(text.replace('~',' ').split())
    for old,new in NORMALIZATIONS[rid].items():text=text.replace(old,new)
    return text
def display_sg_text(rid,text):
    require(rid in SG_IDS,'unsupported_ID')
    def replace(m):
        require(m.group(1) in MATH[rid],'unrecognized_body_math:'+m.group(1));return MATH[rid][m.group(1)]
    text=re.sub(r'\$([^$]+)\$',replace,text)
    require('\\' not in text and '$' not in text,'unrendered_body_command')
    return text
def validate_sg_assets(paper,rid,raw,api):
    key,sh,mh,count=SCHEMAS[rid];require(key in raw and isinstance(raw[key],list),'original_asset_key')
    require(not ({'files','assets','actual_assets','all_actual_assets'}-{key})&set(raw),'no_receipt_alias')
    items=raw[key];require(len(items)==len(api['files'])==count,'all_actual_asset_count')
    require([x['api_file_object'] for x in items]==api['files'],'full_original_API_objects_in_order')
    names=[]
    for x in items:
        expected={'api_file_object','path','bytes',sh,mh}|({'size_equals_API','checksum_equals_API'} if rid=='23181280' else set())
        require(set(x)==expected,'exact_original_asset_fields');obj=x['api_file_object'];name=safe_relative(obj['key'],basename=True);names.append(name)
        require(x['path']==str(Path(paper)/'sources'/name),'original_asset_path')
        require(type(x['bytes']) is int and x['bytes']==obj['size'],'API_asset_size')
        require(re.fullmatch('[0-9a-f]{64}',x[sh]) and re.fullmatch('[0-9a-f]{32}',x[mh]),'checksum_field_case_and_shape')
        require(obj['checksum']=='md5:'+x[mh],'full_API_MD5')
        if rid=='23181280':require(x['size_equals_API'] is x['checksum_equals_API'] is True,'original_API_flags')
    require(len(set(names))==count,'unique_actual_assets')
    return items
def spanning_sos_gin_source_view(paper,config,gate):
    paper=Path(paper);rid=paper.name;require(rid in SG_IDS,'unsupported_ID');pin=PINS[rid];P=paper.parents[1]
    cp=contained_file(paper,'publication.json');gp=contained_file(paper,'promotion.json')
    require(digest(cp)==pin['publication'] and digest(gp)==pin['promotion'],'pinned_config_bytes')
    require(json.loads(cp.read_bytes())==config and json.loads(gp.read_bytes())==gate,'passed_objects_equal_actual_configs')
    b=config['source_binding'];require(b['record_id']==gate['record_id']==rid,'record_identity')
    require(gate['publication_sha256']==pin['publication'] and gate['status']=='PASS' and gate['disposition_by']=='root','separate_root_disposition')
    originals={}
    for label,field in [('source_receipt','source_receipt_path'),('metadata','metadata_path'),('raw_record','raw_record_path'),('transport_receipt','transport_receipt_path')]:
        path=contained_file(paper,b[field]);require(b[field]==gate[field] and digest(path)==b[label+'_sha256']==gate[label+'_sha256'],'actual_'+label+'_bytes');originals[label]=json.loads(path.read_bytes())
    raw=originals['source_receipt'];api=originals['raw_record'];meta=originals['metadata'];transport=originals['transport_receipt']
    require(raw==b['source_receipt_record']==gate['source_receipt_record'],'whole_original_receipt')
    require(transport==b['transport_receipt_record']==gate['transport_receipt_record'],'whole_original_transports')
    key,sh,mh,count=SCHEMAS[rid];require(b['source_assets_field']==key and raw[key]==b['files']==gate['source_files'],'whole_original_asset_objects')
    require(api['files']==b['published_file_objects']==gate['published_file_objects'] and b['published_asset_count']==count,'all_published_file_objects')
    require(api['metadata']==meta['metadata'] and str(api['id'])==rid and api['status']=='published','actual_raw_metadata')
    if rid!='23181280':
        require(meta['all_actual_file_objects' if rid=='23442760' else 'all_file_objects']==api['files'],'actual_normalized_metadata_interface')
    else:require(meta==api and b['metadata_path']==b['raw_record_path']=='sources/zenodo-record.raw.json','raw_only_metadata_no_alias')
    m=api['metadata'];require(all(config[k]==m[k] for k in ['title','doi','publication_date']),'actual_title_DOI_declaration')
    require(m['creators'][0]['name']=='Kriebel, Alec' and m['creators'][0]['orcid']=='0009-0001-9320-500X' and config['author']=='Alec Kriebel','actual_author')
    require(m['license']['id']=='cc-by-4.0' and config['license']=='CC BY 4.0','actual_license')
    require(api['created']==b['record_created_utc'] and api['updated']==b['record_updated_utc'] and str(api['conceptrecid'])==b['concept_record_id'],'separate_creation_update_concept')
    if rid=='23395703':require('version' not in m and config['version'] is b['version'] is b['zenodo_version'] is b['manuscript_version'] is gate['version'] is None and b['version_field_present'] is gate['version_field_present'] is meta['version_field_present'] is False and meta['version_value'] is None,'honest_missing_version')
    else:require(config['version']==m['version']==b['version']==b['zenodo_version']==b['manuscript_version']=='1.0','declared_version')
    science_path=contained_file(P,gate['root_clearance_file']);editorial_path=contained_file(P,'verification/root-editorial-'+rid+'-20261025.json')
    require(digest(science_path)==pin['science']==gate['root_clearance_sha256']==config['review_metadata']['root_clearance_sha256'],'exact_scientific_authority')
    require(digest(editorial_path)==pin['editorial'],'exact_editorial_authority')
    science=json.loads(science_path.read_bytes());editorial=json.loads(editorial_path.read_bytes())
    require(science==gate['root_clearance_record'] and science['status']=='PASS' and science['approved_scope']==gate['approved_scope'],'whole_original_root_authority')
    for label in ['source_receipt','metadata','raw_record']:
        require(b[label+'_path']==science[label+'_path'] and b[label+'_sha256']==science[label+'_sha256'],'scientific_'+label+'_binding')
    require(gate['root_clearance_file']==config['review_metadata']['root_clearance_file']=='verification/root-clearance-'+rid+'-20261025.json','exact_root_authority_path')
    require(editorial['status']=='ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE' and editorial['private_staging_authorized'] is True and editorial['production_integration_authorized'] is False,'private_stage_authority_only')
    ed=paper/'reviews/editorial';seal=contained_file(ed,'SEAL.json');manifest=contained_file(ed,'MANIFEST.json')
    require(digest(seal)==pin['editorial_seal']==editorial['exact_editorial_seal_sha256'] and digest(manifest)==pin['editorial_manifest'],'exact_editorial_seal_manifest')
    se=json.loads(seal.read_bytes());require(se['manifest_sha256']==pin['editorial_manifest'] and se['publication_sha256']==pin['publication'] and se['promotion_sha256']==pin['promotion'],'editorial_configs_binding')
    for rel,item in json.loads(manifest.read_bytes())['owned_output_bindings'].items():
        path=contained_file(paper,rel);require(digest(path)==item['sha256'] and path.stat().st_size==item['bytes'],'editorial_owned_binding')
    require(set(gate['reviews'])==set(science['reviews'])=={'scope','analytic','adversarial'},'three_complete_original_review_roles')
    for role,item in gate['reviews'].items():
        ref=science['reviews'][role];require(item['root_authority_entry']==ref,'whole_root_review_entry')
        require(ref['report']=='papers/'+rid+'/'+item['report'] and ref['verdict']=='papers/'+rid+'/'+item['verdict_file'],'original_review_paths')
        require(digest(contained_file(paper,item['report']))==item['sha256']==ref['report_sha256'],'complete_original_report')
        vf=contained_file(paper,item['verdict_file']);require(digest(vf)==item['verdict_sha256']==ref['verdict_sha256'] and json.loads(vf.read_bytes())==item['verdict'],'whole_original_custom_verdict')
    for name in ['root_review','root_custody_receipt']:require(digest(contained_file(P,science[name]))==science[name+'_sha256'],'final_root_evidence')
    require(gate['follow_up'] is config['follow_up'] is science['follow_up'] is editorial['follow_up'] is None and gate['AA'] is None and config['canonical_url'] is gate['canonical_url'] is None,'unchanged_null_gates')
    require(all(gate[x] is False for x in ['rendered_copy_verified','live_verified','browser_verified','native_verified']) and all(config['review_metadata'][x] is False for x in ['rendered','deployed','browser_verified','live_verified','native_verified']),'unchanged_false_publication_gates')
    require(len(transport)==b['transport_receipt_entry_count']==(6 if rid=='23395703' else 5),'complete_transport_entry_count')
    for event in transport:
        status='status' if rid=='23395703' else 'http_status';headers='headers' if rid=='23395703' else 'response_headers';byteskey='bytes_received' if rid=='23181280' else 'bytes';th='sha256' if rid=='23442760' else 'SHA256';tm='md5' if rid=='23442760' else 'MD5'
        require(event[status]==200 and isinstance(event[headers],dict) and event[headers],'actual_transport_interface')
        actual_path=Path(event['path']);relative=str(actual_path.relative_to(paper)) if actual_path.is_absolute() else 'sources/'+str(actual_path)
        path=contained_file(paper,relative);data=path.read_bytes()
        require(len(data)==event[byteskey] and hashlib.sha256(data).hexdigest()==event[th] and hashlib.md5(data).hexdigest()==event[tm],'actual_transport_payload_binding')
    tp=contained_file(paper,b['source_tex_path']);require(b['source_tex_path']==science['source_tex_path'] and digest(tp)==b['source_tex_sha256']==science['source_tex_sha256'],'actual_controlling_TeX')
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tp.read_text(),re.S).group(1)
    require(abstract==b['abstract_tex']==contained_file(paper,b['abstract_source']).read_text() and normalize_sg_abstract(rid,abstract)==config['abstract'],'whole_original_abstract')
    bp=contained_file(paper,b['prepared_bibtex_path']);require(bp.read_text()==config['prepared_bibtex'] and digest(bp)==b['prepared_bibtex_sha256'],'exact_prepared_BibTeX')
    if 'pending_intake_seal_path' in b:require(digest(contained_file(paper,b['pending_intake_seal_path']))==b['pending_intake_seal_sha256'],'immutable_pending_intake')
    original_snapshot=deepcopy(raw);selected=[]
    for item in validate_sg_assets(paper,rid,raw,api):
        obj=item['api_file_object'];name=obj['key'];path=contained_file(paper,'sources/'+name);data=path.read_bytes()
        require(len(data)==item['bytes'],'actual_asset_bytes');require(hashlib.md5(data).hexdigest()==item[mh] and digest(path)==item[sh],'actual_asset_hashes')
        if name==config['pdf_filename']:require(item[sh]==b['pdf_sha256']==gate['pdf_sha256']==science['pdf_sha256'],'selected_PDF_binding')
        elif name==config['supplement_filename']:require(item[sh]==b['supplement_sha256']==gate['supplement_sha256']==science['supplement_sha256'],'complete_ZIP_binding')
        else:require(rid=='23395703' and item==b['published_TeX_asset'] and item[sh]==gate['published_tex_sha256']==b['source_tex_sha256'],'third_actual_TeX_asset')
        selected.append({'name':name,'url':obj['links']['self'],'bytes':item['bytes'],'sha256':item[sh],'zenodo_checksum':obj['checksum']})
    require(raw==original_snapshot and config['additional_assets']==[],'originals_unmodified_only_one_reader')
    return raw,{'record_id':rid,'files':selected},paper/'sources'
