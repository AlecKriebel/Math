"""Narrow authenticated consumer for three exact editorial/scientific authorities.
Original objects are never rewritten. Only the returned resolver view is temporary.
"""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
import hashlib,json,re,stat,zipfile
from bosonic_source import contained_file,digest
from published_assets import safe_relative
ABM_IDS={'23333353','23416806','23441617'}
PINS=__PIN_LITERAL__
NORMALIZATIONS=__NORMALIZATION_LITERAL__
STATUSES={'23333353':'PASS','23416806':'PASS','23441617':'PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT'}
SCHEMAS={'23333353':('all_actual_assets','api_file_object'),'23416806':('all_assets','original_api_file_object'),'23441617':('all_assets','original_api_file_object')}
def require(value,tag):
    if not value:raise ValueError('ambient_block_modulus:'+tag)
def same(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=False,separators=(',',':'))==json.dumps(b,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def normalize_abm_abstract(rid,text):
    require(rid in ABM_IDS,'unsupported_ID')
    for old,new in NORMALIZATIONS[rid].items():text=text.replace(old,new)
    return ' '.join(text.split())
def validate_abm_assets(paper,rid,raw,api):
    key,objkey=SCHEMAS[rid];require(key in raw and isinstance(raw[key],list),'original_asset_key')
    require(not ({'files','assets','actual_assets','all_assets','all_actual_assets'}-{key})&set(raw),'no_receipt_alias')
    items=raw[key];require(len(items)==len(api['files'])==2,'all_actual_asset_count')
    require(same([x[objkey] for x in items],api['files']),'whole_API_objects_original_order')
    names=[]
    for x in items:
        require(set(x)=={objkey,'path','bytes','sha256','md5'},'exact_original_asset_fields');obj=x[objkey];name=safe_relative(obj['key'],basename=True);names.append(name)
        require(x['path']==str(Path(paper)/'sources'/name),'original_asset_path')
        require(type(x['bytes']) is int and type(obj['size']) is int and x['bytes']==obj['size'],'API_asset_size')
        require(re.fullmatch('[0-9a-f]{64}',x['sha256']) and re.fullmatch('[0-9a-f]{32}',x['md5']),'checksum_case_and_shape')
        require(obj['checksum']=='md5:'+x['md5'],'full_API_MD5')
    require(len(set(names))==2,'unique_actual_assets');return items

def verify_abm_archive(paper,rid,archive,inventory):
    """Read CRC and all qualified occurrences against original extraction; no execution."""
    paper=Path(paper);root=paper/'sources';rows=inventory['members'];observed=[];containers=[]
    bycontainer={x['container']:x for x in inventory.get('archive_containers',[])}
    def visit(data,container,depth):
        require(depth<=2,'archive_depth_bound')
        if rid=='23333353':base=root/'published-source'
        else:
            require(container in bycontainer,'qualified_container_mapping');entry=bycontainer[container];base=Path(entry['extraction_root'])
            require(entry['bytes']==len(data) and entry['sha256']==hashlib.sha256(data).hexdigest() and entry['depth']==depth,'container_bytes_depth')
            require(base.resolve().is_relative_to(root.resolve()),'contained_extraction_root')
        containers.append(container)
        with zipfile.ZipFile(BytesIO(data)) as z:
            seen=set()
            for info in z.infolist():
                if info.is_dir():continue
                name=safe_relative(info.filename);mode=info.external_attr>>16
                require(name==info.filename and name not in seen and not(info.flag_bits&1) and not stat.S_ISLNK(mode),'safe_unique_regular_member');seen.add(name)
                payload=z.read(info);require(len(payload)==info.file_size and len(payload)<=10000000,'bounded_member')
                match=[x for x in rows if x['member']==name and (rid=='23333353' or x['container']==container)]
                require(len(match)==1,'qualified_member_identity');row=match[0]
                path=contained_file(paper,str((base/name).relative_to(paper)))
                require(path.read_bytes()==payload and row['bytes']==len(payload) and row['sha256']==hashlib.sha256(payload).hexdigest() and row['CRC32']==f'{info.CRC:08x}','CRC_hash_and_extraction')
                if rid!='23333353':require(row['extracted_path']==str(path),'original_extraction_mapping')
                observed.append((container,name));require(not name.lower().endswith('.pdf'),'no_embedded_reader')
                if name.lower().endswith('.zip'):visit(payload,container+'::'+name,depth+1)
    visit(archive.read_bytes(),archive.name,0)
    count={'23333353':60,'23416806':186,'23441617':118}[rid];nc={'23333353':1,'23416806':4,'23441617':1}[rid]
    require(len(observed)==len(rows)==count and len(set(observed))==count and len(containers)==nc,'complete_occurrences_not_deduplicated')
    if rid!='23333353':require(set(containers)==set(bycontainer),'all_original_container_identities')
    return {'member_occurrences':count,'containers':nc,'embedded_PDFs':0}

def ambient_block_modulus_source_view(paper,config,gate):
    paper=Path(paper);rid=paper.name;require(rid in ABM_IDS,'unsupported_ID');pin=PINS[rid];P=paper.parents[1]
    cp=contained_file(paper,'publication.json');gp=contained_file(paper,'promotion.json')
    require(digest(cp)==pin['publication'] and digest(gp)==pin['promotion'],'pinned_config_bytes')
    require(same(json.loads(cp.read_bytes()),config) and same(json.loads(gp.read_bytes()),gate),'passed_whole_objects_equal_actual')
    b=config['source_binding'];require(b['record_id']==gate['record_id']==rid,'record_identity')
    # Authenticate complete root first, then accept only this exact per-record status.
    science_path=contained_file(P,gate['root_clearance_file']);editorial_path=contained_file(P,'verification/root-editorial-'+rid+'-20261025.json')
    require(digest(science_path)==pin['science']==gate['root_clearance_sha256']==config['review_metadata']['root_clearance_sha256'],'exact_scientific_authority')
    require(digest(editorial_path)==pin['editorial'],'exact_editorial_authority')
    science=json.loads(science_path.read_bytes());editorial=json.loads(editorial_path.read_bytes())
    require(same(science,gate['root_clearance_record']) and science['status']==gate['status']==STATUSES[rid] and gate['approved_scope']==science['approved_scope'] and gate['disposition_by']=='root','whole_root_exact_literal_status')
    require(gate['publication_sha256']==pin['publication'],'publication_gate_binding')
    require(gate['root_clearance_file']==config['review_metadata']['root_clearance_file']=='verification/root-clearance-'+rid+'-20261025.json','exact_root_path')
    require(editorial['status']=='ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE' and editorial['private_staging_authorized'] is True and editorial['production_integration_authorized'] is False,'private_stage_only')
    ed=paper/'reviews/editorial';seal=contained_file(ed,'SEAL.json');manifest=contained_file(ed,'MANIFEST.json')
    require(digest(seal)==pin['editorial_seal']==editorial['editorial_seal_sha256'] and digest(manifest)==pin['editorial_manifest'],'exact_editorial_seal_manifest')
    se=json.loads(seal.read_bytes());require(se['manifest_sha256']==pin['editorial_manifest'] and se['publication_sha256']==pin['publication'] and se['promotion_sha256']==pin['promotion'],'editorial_config_bindings')
    for rel,item in json.loads(manifest.read_bytes())['owned_output_bindings'].items():
        path=contained_file(paper,rel);require(digest(path)==item['sha256'] and path.stat().st_size==item['bytes'],'editorial_owned_binding')
    originals={}
    for label,field in [('source_receipt','source_receipt_path'),('metadata','metadata_path'),('raw_record','raw_record_path'),('transport_receipt','transport_receipt_path')]:
        path=contained_file(paper,b[field]);require(b[field]==gate[field] and digest(path)==b[label+'_sha256']==gate[label+'_sha256'],'actual_'+label+'_bytes');originals[label]=json.loads(path.read_bytes())
        if label!='transport_receipt':require('papers/'+rid+'/'+b[field]==science[label+'_path'] and b[label+'_sha256']==science[label+'_sha256'],'scientific_'+label+'_binding')
    raw=originals['source_receipt'];api=originals['raw_record'];meta=originals['metadata'];transport=originals['transport_receipt'];snapshot=deepcopy(raw)
    require(same(raw,b['source_receipt_original']) and same(raw,gate['source_receipt_original']),'whole_original_receipt')
    require(same(transport,b['transport_receipt_original']) and same(transport,gate['transport_receipt_original']),'whole_original_transports')
    key,objkey=SCHEMAS[rid];require(b['source_assets_field']==key and same(raw[key],b[key]) and same(raw[key],gate[key]),'whole_original_asset_objects')
    require(same(api['files'],b['published_file_objects']) and same(api['files'],gate['published_file_objects']) and b['published_asset_count']==2,'all_original_file_objects')
    require(same(api['metadata'],meta['metadata']) and str(api['id'])==rid and api['status']=='published','actual_raw_metadata')
    require(same(meta['all_actual_file_objects' if rid=='23333353' else 'all_original_API_file_objects'],api['files']) and same(meta['all_verified_assets' if rid=='23333353' else 'all_assets'],raw[key]),'actual_derivative_metadata_interface')
    m=api['metadata'];require(all(config[k]==m[k] for k in ['title','doi','publication_date']),'actual_title_DOI_declaration')
    require(m['creators'][0]['name']=='Kriebel, Alec' and m['creators'][0]['orcid']=='0009-0001-9320-500X' and config['author']=='Alec Kriebel','actual_author')
    require(m['license']['id']=='cc-by-4.0' and config['license']=='CC BY 4.0','actual_license')
    require(api['created']==b['record_created_utc'] and api['updated']==b['record_updated_utc'] and str(api['conceptrecid'])==b['concept_record_id'],'separate_creation_update_concept')
    require(config['version']==m['version']==b['version']==b['zenodo_version']==gate['version']=='1.0','actual_API_version')
    if rid=='23441617':
        require(b['manuscript_version'] is None and b['manuscript_version_printed'] is False,'honest_unprinted_manuscript_version')
        require(config['review_metadata']['scientific_clearance_status']==STATUSES[rid] and same(json.loads((ed/'BIBLIOGRAPHIC_DISPOSITION.json').read_bytes())['root_original_disposition'],science['noncentral_bibliographic_defect']),'whole_original_bibliographic_defect')
        require(any('Heinonen' in x['title'] and '181 (1998)' in x['title'] and x['url']=='https://doi.org/10.1007/BF02392747' for x in config['background']),'correct_public_181_reference')
    else:require(b['manuscript_version']=='1.0','printed_version')
    require(set(gate['reviews'])==set(science['reviews'])=={'scope','analytic','adversarial'},'three_original_review_roles')
    for role,item in gate['reviews'].items():
        ref=science['reviews'][role];require(same(item['root_authority_entry'],ref),'whole_root_review_entry')
        require(ref['report']=='papers/'+rid+'/'+item['report'] and ref['verdict']=='papers/'+rid+'/'+item['verdict_file'],'original_review_paths')
        require(digest(contained_file(paper,item['report']))==item['report_sha256']==ref['report_sha256'],'complete_original_report')
        vf=contained_file(paper,item['verdict_file']);require(digest(vf)==item['verdict_sha256']==ref['verdict_sha256'] and same(json.loads(vf.read_bytes()),item['verdict']),'whole_original_custom_verdict')
    for name in ['root_review','root_custody_receipt']:require(digest(contained_file(P,science[name]))==science[name+'_sha256'],'final_root_evidence')
    require(gate['follow_up'] is config['follow_up'] is science['follow_up'] is editorial['follow_up'] is gate['AA'] is config['AA'] is config['canonical_url'] is gate['canonical_url'] is None,'unchanged_null_gates')
    flags=['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received']
    require(all(gate[x] is False and config['review_metadata'][x] is False for x in flags) and config['review_metadata']['rendered'] is config['review_metadata']['deployed'] is False,'unchanged_false_gates')
    require(len(transport)==b['transport_receipt_entry_count']==5,'complete_transport_count')
    for event in transport:
        require(event['status']==200 and isinstance(event['headers'],dict) and event['headers'] and 'md5' not in event and 'api_file_object' not in event,'actual_transport_interface_no_inventions')
        path=contained_file(paper,str(Path(event['path']).relative_to(paper)));data=path.read_bytes()
        require(len(data)==event['bytes'] and hashlib.sha256(data).hexdigest()==event['sha256'],'actual_transport_payload')
    for fn in ['SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_MANIFEST.json','SOURCE_SEAL.json','archive-members.json']:
        require(digest(contained_file(paper,'sources/'+fn))==pin['source_pins'][fn],'pinned_original_source_manifest_inventory')
    for fn in ['SOURCE_READY_MANIFEST.json','SOURCE_MANIFEST.json']:
        original_manifest=json.loads((paper/'sources'/fn).read_bytes())
        for item in original_manifest['files']:
            path=Path(item['path']);rel=str(path.relative_to(paper)) if path.is_absolute() else 'sources/'+str(path);path=contained_file(paper,rel)
            require(path.stat().st_size==item['bytes'] and digest(path)==item['sha256'],'all_original_source_bindings')
    tp=contained_file(paper,b['source_tex_path']);require('papers/'+rid+'/'+b['source_tex_path']==science['source_tex_path'] and digest(tp)==b['source_tex_sha256']==science['source_tex_sha256'],'actual_controlling_TeX')
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tp.read_text(),re.S).group(1)
    require(abstract==b['abstract_tex']==contained_file(paper,b['abstract_source']).read_text() and normalize_abm_abstract(rid,abstract)==config['abstract'],'whole_original_abstract')
    bp=contained_file(paper,b['prepared_bibtex_path']);require(bp.read_text()==config['prepared_bibtex'] and digest(bp)==b['prepared_bibtex_sha256'],'exact_prepared_BibTeX')
    selected=[]
    for item in validate_abm_assets(paper,rid,raw,api):
        obj=item[objkey];name=obj['key'];path=contained_file(paper,'sources/'+name);data=path.read_bytes()
        require(len(data)==item['bytes'] and hashlib.md5(data).hexdigest()==item['md5'] and digest(path)==item['sha256'],'actual_asset_bytes_hashes')
        label='pdf' if name==config['pdf_filename'] else 'supplement';require(item['sha256']==b[label+'_sha256']==gate[label+'_sha256']==science[label+'_sha256'],'selected_complete_asset_binding')
        selected.append({'name':name,'url':obj['links']['self'],'bytes':item['bytes'],'sha256':item['sha256'],'zenodo_checksum':obj['checksum']})
    inventory=json.loads((paper/'sources/archive-members.json').read_bytes());verify_abm_archive(paper,rid,paper/'sources'/config['supplement_filename'],inventory)
    require(same(raw,snapshot) and config['additional_assets']==[],'originals_unmodified_one_reader')
    return raw,{'record_id':rid,'files':selected},paper/'sources'
