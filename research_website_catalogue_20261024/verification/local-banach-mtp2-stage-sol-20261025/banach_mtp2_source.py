"""Read-only two-record consumer. Native objects stay literal; no source aliases.

Exact pinned approvals authenticate full copies and whole custom verdicts. Separate
validators expose the native schema/edition/transport interfaces to fault controls.
"""
from pathlib import Path
from io import BytesIO
import hashlib, json, re, stat, zipfile
from bosonic_source import contained_file, digest
from published_assets import safe_relative
BM_IDS = {'23217863','23146753'}
STATUSES = {'23217863':'PASS_AT_DECLARED_EXTERNAL_THEOREM_LEVEL','23146753':'PASS_WITH_EXPLICIT_PRIMARY_AND_PRIORITY_LIMITS'}
VERSIONS = {'23217863':None,'23146753':'1.0'}
DATES = {'23217863':'2026-10-07','23146753':'2026-10-04'}
ASSET_ORDER = {'23217863':['paper.pdf','source-and-verification.zip'],'23146753':['mtp2-edge-closure-verification.zip','mtp2-edge-closure-note.pdf']}
LICENSES = {'23217863':'CC BY 4.0 for original manuscript, prose and verification code','23146753':'CC BY 4.0'}
PINS = {'23217863': {'publication': '9015e779a369c918f6a08835cce384d9c20d9325060d7910300093367e45cc37',
              'promotion': '155b5fbebb5ad89fce5f68838d3377ab8c9f07e37847c85c0eca67bed82fc2ea',
              'science': 'b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a',
              'editorial': '17ef2f58114a960f8d91ca358d129319beaaf7a4c1e3e4a637fa4b4bd82409cf',
              'editorial_manifest': '99012868fc6abccbd694b30e8ad5b375651a8af2ecff8e144d55cbb8880319a1',
              'editorial_seal': '6d527e22ba9a34cede1e9c8179adbe5b186330bd98313fc3a185b1daf4121615',
              'public_copy': 'c0bc1043da101a4d4942926691fdf836237ab8fcba3ae169d3ca9980343ab395',
              'source_pins': {'SOURCE_FINAL_MANIFEST.json': '9563960191f7c61ebf382fcd819ea888b8a253322950278f2dd13e15798292aa',
                              'SOURCE_FINAL_SEAL.json': '7a4affd82eaf6f41509a2d0810bd88db492b442581dbcaa9f4758f147702c88b',
                              'SOURCE_READY.json': '11f2d44b667633686e28dbcfc51020e006499b7021f01dec800d2a023998bd0b',
                              'SOURCE_READY_MANIFEST.json': '4c6f4084f386eb8e20985b73828ac9cabc9b92c8e9122017895ae392ef29d1e5',
                              'SOURCE_READY_SEAL.json': '8d98d2c9a263caf67730208c61dca6e68fbe6d406cdcf648893fabcffecfc0ce'},
              'inventory': '6e6a4c1cc858624ae930f8d6872cc85ff0b7b8946e832b7ccecb5f20af8cfb97',
              'raw_metadata_keys': ['title',
                                    'doi',
                                    'publication_date',
                                    'description',
                                    'access_right',
                                    'creators',
                                    'keywords',
                                    'related_identifiers',
                                    'language',
                                    'resource_type',
                                    'license',
                                    'relations']},
 '23146753': {'publication': '70d32cfac4132080a916373adeaa9bc0ccecdc276ab9985976f3dbdc4fab12f1',
              'promotion': '68d9fc5e77fd6e701daa92315fb5dacafe45c4dff070b047a39eef9b5204dcdc',
              'science': '9f03be990c7b547ebc341908662b241f84b77ffb9b26f9d834d72407d34b7860',
              'editorial': 'a217022c02f02f94e42a368a2c3ef684792de598b11293eb20121bb3a78fdfd9',
              'editorial_manifest': '796b592549455d177295ac24270e7dfe05c100fa4dfd6861e590e97101808091',
              'editorial_seal': '29f3b620cec56d0ef5faebcee85876219c41bcee22f550fb5c9890cbf5194298',
              'public_copy': '94beca8bd55f21c6b423632e0529c874a738189ba0d4ac6920cc6decd56cbe9c',
              'source_pins': {'SOURCE_MANIFEST.json': 'f4cde61ba37fe705b77ec22edb143ef182bd951f2b71e60f4a116513097e2f22',
                              'SOURCE_READY.json': '99b034e696ba8a6ba772a5829210af3c1a6a97251de5e1b7be687f8785efe0da',
                              'SOURCE_READY_MANIFEST.json': '427d17a871bae870139756077ec84c31c8bbd9a2037d3f7c12850f3587784669',
                              'SOURCE_READY_SEAL.json': '63049ed28a1f1070c5030b4009aa79ecee6b339a9a1cfb114bbfe058b242f1f6',
                              'SOURCE_SEAL.json': '35a2a8debe40a6d4a852f81a207f5269c96c3ca9c7dc1615c507df0866eab565'},
              'inventory': 'b0d1b51f96f865fdd5fb7864b8c91e1c23efd835809fd7c40d697ccb8edb7643',
              'raw_metadata_keys': ['title',
                                    'doi',
                                    'publication_date',
                                    'description',
                                    'access_right',
                                    'creators',
                                    'keywords',
                                    'related_identifiers',
                                    'version',
                                    'language',
                                    'resource_type',
                                    'license',
                                    'relations']}}

def require(ok, tag):
    if not ok: raise ValueError('banach_mtp2:'+tag)

def same(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def normalize_bm_abstract(rid,text):
    require(rid in BM_IDS,'supported_ID')
    pairs=[('Banach--Mazur','Banach–Mazur'),('$*$','*'),('~',' ')] if rid=='23217863' else [('MTP$_2$','MTP₂'),('Conjecture~1','Conjecture 1')]
    for old,new in pairs: text=text.replace(old,new)
    return ' '.join(text.split())

def validate_bm_edition(rid,c,g,raw,meta,api):
    require(rid in BM_IDS and type(api) is dict and type(meta) is dict and type(raw) is dict,'native_object_types')
    b=c['source_binding'];m=api['metadata'];v=VERSIONS[rid]
    require(type(m) is dict and list(m)==PINS[rid]['raw_metadata_keys'],'whole_native_metadata_schema')
    require(same(meta['metadata'],m),'whole_nested_metadata')
    expected_id=int(rid) if rid=='23217863' else rid
    require(same(b['record_id'],expected_id) and same(g['record_id'],expected_id) and same(raw['record_id'],int(rid)) and same(meta['record_id'],expected_id) and same(api['id'],int(rid)),'native_ID_types_no_coercion')
    require(api['status']=='published' and all(c[k]==raw[k]==m[k] for k in ('title','doi','publication_date')),'exact_record_identity')
    require(c['publication_date']==b['zenodo_publication_date']==b['manuscript_date']==DATES[rid],'separate_declared_manuscript_dates')
    require(same(c['version'],v) and same(g['version'],v) and same(b['version'],v) and same(raw['version'],v) and same(b['zenodo_version'],v),'exact_API_version_value')
    require(c['version_field_present'] is (v is not None) and b['version_field_present'] is (v is not None) and ('version' in m) is (v is not None),'absence_not_null_alias')
    require(b['manuscript_version'] is None and (b.get('manuscript_version_printed') is False if rid=='23146753' else True),'no_printed_version_invention')
    require((m.get('version')==v if v is not None else 'version' not in m),'native_API_edition')
    require(api['created']==raw['created']==meta['created']==b['record_created_utc'] and api['updated']==raw['updated']==meta['updated']==b['record_updated_utc'],'genuine_creation_update')
    require(str(api['conceptrecid'])==str(raw['conceptrecid'])==meta['conceptrecid']==b['concept_record_id'],'concept_identity')
    require(c['author']=='Alec Kriebel' and m['creators'][0]['name']=='Kriebel, Alec' and m['creators'][0]['orcid']=='0009-0001-9320-500X' and m['license']['id']=='cc-by-4.0','actual_author_API_license')
    require(c['license']==LICENSES[rid] and c['license_url']=='https://creativecommons.org/licenses/by/4.0/','authored_license_distinct_from_bundled')

def validate_bm_assets(paper,rid,raw,api):
    require(type(raw.get('all_assets')) is list and len(raw['all_assets'])==2 and not {'files','assets','actual_assets','all_actual_assets'}&raw.keys(),'native_all_assets_no_alias')
    require(type(api['files']) is list and len(api['files'])==2,'two_actual_public_API_assets')
    require(same([x['original_api_file_object'] for x in raw['all_assets']],api['files']),'whole_API_file_objects_and_order')
    names=[]
    for item in raw['all_assets']:
        require(type(item) is dict and set(item)=={'original_api_file_object','path','bytes','md5','sha256'},'exact_native_asset_fields')
        obj=item['original_api_file_object'];name=safe_relative(obj['key'],basename=True);names.append(name)
        require(item['path']==str(Path(paper)/'sources'/name),'original_asset_paths')
        require(type(item['bytes']) is int and type(obj['size']) is int and item['bytes']==obj['size']>0,'integer_not_boolean_sizes')
        require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}',item['sha256']) and type(item['md5']) is str and re.fullmatch('[0-9a-f]{32}',item['md5']),'lowercase_MD5_SHA')
        require(obj['checksum']=='md5:'+item['md5'] and obj['links']['self']==f'https://zenodo.org/api/records/{rid}/files/{name}/content','actual_original_API_checksum_URL')
    require(names==ASSET_ORDER[rid],'record_specific_native_asset_order')
    return raw['all_assets']

def validate_bm_transports(paper,rid,events,raw,api):
    require(type(events) is list and len(events)==5,'one_genuine_five_event_list')
    for e in events:
        require(type(e) is dict and set(e)=={'requested_url','started_utc','completed_utc','status','final_url','headers','path','bytes','sha256'},'literal_transport_schema')
        require(type(e['status']) is int and e['status']==200 and type(e['headers']) is dict and bool(e['headers']) and type(e['bytes']) is int and e['bytes']>0,'genuine_success_transport_types')
        path=contained_file(paper,str(Path(e['path']).relative_to(paper)))
        require(path.stat().st_size==e['bytes'] and digest(path)==e['sha256'],'transport_saved_payload')
    require([Path(e['path']).name for e in events[:3]]==['record.raw.json','latest.raw.json','versions.raw.json'] and [Path(e['path']).name for e in events[3:]]==ASSET_ORDER[rid],'record_latest_versions_then_native_order')
    latest=json.loads(Path(events[1]['path']).read_bytes());versions=json.loads(Path(events[2]['path']).read_bytes())
    require(same(latest,api),'actual_latest_whole_record')
    hits=versions['hits']['hits'];require(type(hits) is list and len(hits)==1 and same(hits[0]['id'],int(rid)),'actual_single_version_record')
    expected=dict(api);expected['swh']=None
    require(api['swh']=={} and same(hits[0],expected),'literal_versions_swh_null_difference')
    for event,item in zip(events[3:],raw['all_assets']):
        obj=item['original_api_file_object'];require(event['requested_url']==event['final_url']==obj['links']['self'],'actual_transport_API_URL')
        checksum='MD5:afc4fd82272a87b678e0efce8beea0d' if rid=='23146753' and obj['key'].endswith('.pdf') else 'MD5:'+item['md5']
        require(event['headers']['oc-checksum']==checksum,'literal_opaque_oc_checksum_no_padding')

def verify_bm_archive(paper,rid,archive,inventory,selected_pdf):
    require(type(inventory) is dict and type(inventory['members']) is list and type(inventory['archive_containers']) is list and len(inventory['archive_containers'])==1,'native_archive_schema')
    expected=41 if rid=='23217863' else 13
    table={x['member']:x for x in inventory['members']}
    require(len(table)==len(inventory['members'])==expected,'all_unique_regular_members')
    payloads={}
    with zipfile.ZipFile(BytesIO(archive.read_bytes())) as z:
        require(len(z.infolist())==expected,'complete_ZIP_not_subset')
        for entry in z.infolist():
            name=safe_relative(entry.filename);mode=entry.external_attr>>16
            require(name==entry.filename and name not in payloads and not entry.is_dir() and not entry.flag_bits&1 and stat.S_IFMT(mode) in (0,stat.S_IFREG),'safe_unique_regular_path')
            row=table[name];data=z.read(entry)
            require(type(row['bytes']) is int and row['bytes']==len(data)==entry.file_size and row['compressed_bytes']==entry.compress_size,'actual_member_sizes')
            require(row['container']==archive.name and row['CRC32']==f'{entry.CRC:08x}' and row['sha256']==hashlib.sha256(data).hexdigest(),'every_CRC_hash')
            require(row['extracted_path']==str(Path(paper)/'sources/published-source'/name) and contained_file(paper,'sources/published-source/'+name).read_bytes()==data,'unchanged_existing_extraction')
            if rid=='23217863': require(row['safe_regular_member'] is True and row['nested_archive'] is None,'native_Banach_member_types')
            else: require(row['ZIP_CRC_read'] is True and row['nested_archive'] is False and type(row['archive_mode']) is int and row['archive_mode']==mode,'native_MTP_member_types')
            require(not name.lower().endswith(('.zip','.tar','.tar.gz','.tgz','.gz')),'no_nested_archive')
            payloads[name]=data
    pdfs=[k for k in payloads if k.lower().endswith('.pdf')];require(len(pdfs)==1,'one_embedded_PDF')
    require((payloads[pdfs[0]]==selected_pdf.read_bytes()) is (rid=='23146753'),'correct_distinct_or_identical_reader_role')
    return {'occurrences':expected,'containers':1,'embedded_PDFs':1}

def banach_mtp2_source_view(paper,c,g):
    paper=Path(paper);rid=paper.name;require(rid in BM_IDS,'supported_ID');pin=PINS[rid];programme=paper.parents[1];b=c['source_binding']
    cp,gp=contained_file(paper,'publication.json'),contained_file(paper,'promotion.json')
    require(digest(cp)==pin['publication'] and digest(gp)==pin['promotion'],'exact_config_bytes')
    require(same(json.loads(cp.read_bytes()),c) and same(json.loads(gp.read_bytes()),g),'whole_passed_objects_typed')
    science_path=contained_file(programme,'verification/root-clearance-'+rid+'-20261025.json');editorial_path=contained_file(programme,'verification/root-editorial-'+rid+'-20261025.json')
    require(digest(science_path)==pin['science'] and digest(editorial_path)==pin['editorial'],'separate_pinned_scientific_editorial_authorities')
    science,editorial=json.loads(science_path.read_bytes()),json.loads(editorial_path.read_bytes())
    require(same(science,g['root_clearance_record']) and g['status']==science['status']==STATUSES[rid] and g['disposition_by']=='root' and g['approved_scope']==science['approved_scope'],'whole_literal_qualified_root_status')
    require(g['root_clearance_file']==c['review_metadata']['root_clearance_file']==str(science_path.relative_to(programme)) and g['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']==pin['science'],'exact_root_path_hash')
    require(editorial['status']=='ROOT_EDITORIAL_ACCEPTED_FOR_PRIVATE_STAGE' and editorial['private_staging_authorized'] is True and editorial['production_integration_authorized'] is False and editorial['root_scientific_status_preserved_literal']==STATUSES[rid],'private_only_editorial_authority')
    ed=paper/'reviews/editorial';mf,sf=contained_file(ed,'MANIFEST.json'),contained_file(ed,'SEAL.json')
    require(digest(mf)==pin['editorial_manifest'] and digest(sf)==pin['editorial_seal'] and digest(contained_file(ed,'PUBLIC_COPY.md'))==pin['public_copy'],'original_editorial_seal_copy')
    manifest,sealed=json.loads(mf.read_bytes()),json.loads(sf.read_bytes());owned=[]
    if rid=='23217863':
        require(sealed['manifest']['sha256']==pin['editorial_manifest'] and sealed['publication']['sha256']==pin['publication'] and sealed['promotion']['sha256']==pin['promotion'],'native_Banach_editorial_seal')
        for row in manifest['files']:
            path=Path(row['path'])
            if path.is_relative_to(ed) or path in (cp,gp): owned.append((path,row))
        require(len(owned)==39,'Banach_owned_editorial_only')
    else:
        require(sealed['manifest_binding']['sha256']==pin['editorial_manifest'],'native_MTP_editorial_seal')
        owned=[(ed/name,row) for name,row in manifest['owned_bindings'].items()]+[(Path(name),row) for name,row in manifest['config_bindings'].items()]
        require(len(owned)==37,'MTP_owned_editorial_only')
    for path,row in owned:
        path=contained_file(paper,str(path.relative_to(paper)));require(type(row['bytes']) is int and path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],'all_owned_editorial_originals')
    originals={}
    for key in ('source_receipt','metadata','raw_record','transport_receipt','recursive_archive_inventory'):
        path=contained_file(paper,b[key+'_path']);require(digest(path)==b[key+'_sha256'],'actual_original_'+key)
        originals[key]=json.loads(path.read_bytes())
        if key+'_original' in b: require(same(originals[key],b[key+'_original']),'whole_config_'+key)
        if key+'_original' in g: require(same(originals[key],g[key+'_original']),'whole_gate_'+key)
        if key in ('source_receipt','metadata','raw_record','transport_receipt'):require(b[key+'_path']==g[key+'_path'] and b[key+'_sha256']==g[key+'_sha256'],'native_gate_source_binding')
    raw,meta,api=originals['source_receipt'],originals['metadata'],originals['raw_record']
    validate_bm_edition(rid,c,g,raw,meta,api)
    validate_bm_assets(paper,rid,raw,api)
    require(same(raw['all_assets'],b['all_assets']) and same(raw['all_assets'],g['all_assets']) and same(api['files'],b['published_file_objects']) and same(api['files'],g['published_file_objects']),'whole_original_asset_arrays')
    require(set(g['reviews'])==set(science['reviews'])=={'scope','analytic','adversarial'},'all_three_review_families')
    for role,item in g['reviews'].items():
        original=science['reviews'][role]
        require(same(item['root_authority_entry'],original) and original['report']=='papers/'+rid+'/'+item['report'] and original['verdict']=='papers/'+rid+'/'+item['verdict_file'],'whole_native_root_family_entry')
        require(digest(contained_file(paper,item['report']))==item['report_sha256']==original['report_sha256'],'whole_scientific_report')
        verdict=contained_file(paper,item['verdict_file']);require(digest(verdict)==item['verdict_sha256']==original['verdict_sha256'] and same(json.loads(verdict.read_bytes()),item['verdict']),'whole_custom_verdict_no_PASS_coercion')
    for key in ('root_review','root_custody_receipt'):require(digest(contained_file(programme,science[key]))==science[key+'_sha256'],'actual_root_evidence')
    flags=('rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received')
    require(all(g[k] is False and c['review_metadata'][k] is False for k in flags) and c['review_metadata']['rendered'] is False and c['review_metadata']['deployed'] is False,'all_historical_false_gates')
    require(all(c[k] is None and g[k] is None for k in ('canonical_url','AA','follow_up')) and science['follow_up'] is None and editorial['follow_up'] is None,'all_historical_null_gates')
    validate_bm_transports(paper,rid,originals['transport_receipt'],raw,api)
    for name,expected in pin['source_pins'].items():require(digest(contained_file(paper,'sources/'+name))==expected,'native_pinned_source_custody')
    final_name='SOURCE_FINAL_MANIFEST.json' if rid=='23217863' else 'SOURCE_MANIFEST.json';final=json.loads((paper/'sources'/final_name).read_bytes())
    ready=json.loads((paper/'sources/SOURCE_READY_MANIFEST.json').read_bytes());readyseal=json.loads((paper/'sources/SOURCE_READY_SEAL.json').read_bytes())
    require(readyseal['manifest_sha256']==pin['source_pins']['SOURCE_READY_MANIFEST.json'] and readyseal['SOURCE_READY_sha256']==digest(paper/'sources/SOURCE_READY.json'),'native_ready_seal')
    if rid=='23217863':
        require(type(final['files']) is dict and len(final['files'])==52,'native_Banach_final_dict')
        rows=[dict(v,path=k) for k,v in final['files'].items()];fs=json.loads((paper/'sources/SOURCE_FINAL_SEAL.json').read_bytes());require(fs['manifest']['sha256']==pin['source_pins'][final_name],'native_nested_Banach_final_seal')
    else:
        require(type(final['files']) is list and len(final['files'])==25,'native_MTP_final_list');rows=final['files'];fs=json.loads((paper/'sources/SOURCE_SEAL.json').read_bytes());require(fs['manifest_sha256']==pin['source_pins'][final_name],'native_flat_MTP_final_seal')
    for row in ready['files']+rows:
        path=contained_file(paper,'sources/'+row['path']);require(type(row['bytes']) is int and path.stat().st_size==row['bytes'] and digest(path)==row['sha256'],'all_original_source_manifest_entries')
    tex=contained_file(paper,b['source_tex_path']);require(digest(tex)==b['source_tex_sha256']==science['source_tex_sha256'],'sole_controlling_TeX')
    abstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex.read_text(),re.S).group(1)
    require(abstract==b['abstract_tex']==contained_file(paper,'reviews/editorial/ORIGINAL_ABSTRACT.tex').read_text() and normalize_bm_abstract(rid,abstract)==c['abstract'],'whole_original_abstract_declared_normalization_only')
    bib=contained_file(paper,b['prepared_bibtex_path']);require(bib.read_text()==c['prepared_bibtex'] and digest(bib)==b['prepared_bibtex_sha256'] and c['additional_assets']==[],'complete_prepared_BibTeX_no_extra_asset')
    selected=[]
    for item in raw['all_assets']:
        obj=item['original_api_file_object'];name=obj['key'];path=contained_file(paper,'sources/'+name);data=path.read_bytes();label='pdf' if name==c['pdf_filename'] else 'supplement'
        require(len(data)==item['bytes'] and hashlib.md5(data).hexdigest()==item['md5'] and digest(path)==item['sha256']==b[label+'_sha256']==g[label+'_sha256']==science[label+'_sha256'],'complete_original_assets_byteidentity')
        selected.append({'name':name,'url':obj['links']['self'],'bytes':item['bytes'],'sha256':item['sha256'],'zenodo_checksum':obj['checksum']})
    stats=verify_bm_archive(paper,rid,paper/'sources'/c['supplement_filename'],originals['recursive_archive_inventory'],paper/'sources'/c['pdf_filename'])
    require(stats=={'occurrences':b['archive_regular_member_occurrences'],'containers':b['archive_container_count'],'embedded_PDFs':b['archive_embedded_pdf_count']} and b['nested_archive_count']==0,'exact_complete_archive_roles')
    if rid=='23217863':
        authored=contained_file(paper,'sources/published-source/LICENSES.md').read_text();upstream=contained_file(paper,'sources/published-source/upstream/openai-family-295/LICENSE').read_text()
        require('CC BY 4.0' in authored and 'Apache License' in upstream and 'Version 2.0' in upstream and c['license_note'].startswith('Unchanged OpenAI family-295 material'),'actual_mixed_licenses_original_notices')
    else:require('Creative Commons Attribution 4.0' in contained_file(paper,'sources/published-source/LICENSE.txt').read_text(),'actual_authored_CC_BY_notice')
    return raw,{'record_id':rid,'files':selected},paper/'sources'
