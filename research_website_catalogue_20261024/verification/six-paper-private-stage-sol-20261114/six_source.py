"""Six explicit native contracts; original objects are never normalized in place."""
from six_common import *
import re

def frozen_inputs():
    authenticate_root();s=load(OWN/'INPUT_FREEZE_SEAL.json')
    require(bind(OWN/'FROZEN_INPUT_SET.json')['sha256']==s['frozen_input_sha256'],'input_freeze_seal')
    f=load(OWN/'FROZEN_INPUT_SET.json');require(f['records']==list(IDS) and f['root_adoption_sha256']==ROOT_ADOPTION_SHA,'frozen_exact_six')
    for x in f['files']:
        p=contained(PROGRAMME,x['path']);require(bind(p)=={k:x[k] for k in ('bytes','sha256')},'immutable_input:'+str(p))
    for rid in IDS:
        root=PROGRAMME/'papers'/rid/'sources'
        require({str(p) for p in root.rglob('*') if p.is_file()}==
                {x['path'] for x in f['files'] if Path(x['path']).is_relative_to(root)},'no_new_native_source_aliases')
    return f

def native_assets(rid,paper,ready,api,c,spec):
    require(rid in IDS and type(ready) is dict and type(api) is dict,'native_object_types')
    require(list(ready)==spec['ready_keys'] and list(api)==spec['native_record_keys'],'exact_native_top_level_shapes')
    require(list(api['metadata'])==spec['native_metadata_keys'],'exact_native_metadata_shape')
    arr=ready[spec['ready_array']];require(type(arr) is list and len(arr)==2 and len(api['files'])==2,'two_native_assets')
    require([list(x) for x in arr]==spec['asset_keys'],'native_asset_schema_no_alias')
    require(same([x[spec['asset_object_key']] for x in arr],api['files']),'whole_native_file_objects_order')
    require(same(api['files'],load(paper/'sources/record.raw.json')['files']),'complete_original_API_file_objects')
    require([x['key'] for x in api['files']]==spec['asset_order'],'native_asset_order')
    out=[]
    for x,obj in zip(arr,api['files']):
        name=safe_name(obj['key']);path=contained(paper/'sources',x['path'])
        require(path==paper/'sources'/name,'exact_native_saved_path')
        require((not Path(x['path']).is_absolute()) is (rid=='23124601'),'relative_vs_absolute_native_path')
        data=path.read_bytes();require(type(x['bytes']) is int and type(obj['size']) is int and len(data)==x['bytes']==obj['size'],'native_integer_size')
        require(sha(data)==x[spec['digest_key']] and hashlib.md5(data).hexdigest()==x[spec['md5_key']],'actual_native_hashes')
        require(obj['checksum']=='md5:'+x[spec['md5_key']],'actual_API_checksum')
        require(obj['links']['self']==f'https://zenodo.org/api/records/{rid}/files/{name}/content','actual_API_content_URL')
        label='pdf' if name==c['pdf_filename'] else 'supplement'
        require(name==c[label+'_filename'] and sha(data)==c['source_binding'][label+'_sha256'],'selected_complete_asset')
        out.append({'name':name,'url':obj['links']['self'],'bytes':len(data),'sha256':sha(data),'path':str(path)})
    return out

def validate_transports(rid,paper,objects,spec):
    require(same(objects,spec['transport_objects']),'whole_native_transports_and_ordered_headers')
    if rid=='23124601':
        xs=objects[0];require(type(xs) is list and len(xs)==6,'six_original_receipts')
        require([Path(x['path']).name for x in xs]==['record.raw.json','latest.raw.json','versions.raw.json',*spec['asset_order'],'files.raw.json'],'six_receipt_acquisition_order')
        for i,x in enumerate(xs):
            require(type(x['status']) is int and x['status']==200 and type(x['headers_in_original_order']) is list,'actual_106_status_headers')
            require(('elapsed_seconds' in x) is (i<5),'native_missing_final_elapsed_field')
            p=contained(paper/'sources',x['path']);require(bind(p)=={'bytes':x['bytes'],'sha256':x['sha256']},'106_saved_response')
    elif rid in {'23333046','23383952','23539734'}:
        xs=objects[0];require(type(xs) is list and len(xs)==5,'five_native_receipts')
        require([Path(x['body']['path']).name for x in xs]==['record.raw.json','latest.raw.json','versions.raw.json',*spec['asset_order']],'native_five_receipt_order')
        for x in xs:
            require(type(x['HTTP_status']) is int and x['HTTP_status']==200 and type(x['response_headers_in_received_order']) is list,'native_HTTP_header_pairs')
            require('status' not in x and 'elapsed_seconds' not in x and 'md5' not in x,'no_transport_fabricated_fields')
            p=contained(paper/'sources',x['body']['path']);require(bind(p)=={k:x['body'][k] for k in ('bytes','sha256')},'native_original_body_object')
    elif rid=='22929857':
        record,acquire=objects
        require(type(record) is dict and list(record)==['UTC','request_url','resolved_url','HTTP_status','headers','bytes','SHA256'],'native_111_record_receipt_shape')
        require(record['HTTP_status']==200 and type(record['headers']) is list and 'MD5' not in record,'native_record_no_fabricated_MD5')
        require(type(acquire) is dict and list(acquire)==['assets_order_preserved_from_record','responses_in_requested_order'],'native_111_acquisition_shape')
        pairs=acquire['responses_in_requested_order'];require(type(pairs) is list and len(pairs)==5 and all(type(x) is list and len(x)==2 for x in pairs),'native_filename_receipt_pairs')
        require([x[0] for x in pairs]==['latest.raw.json','versions.raw.json','files.raw.json',*spec['asset_order']],'native_111_request_order')
        for name,x in pairs:require(type(x['HTTP_status']) is int and x['HTTP_status']==200 and type(x['headers']) is list,'native_111_actual_receipt')
    else:
        require(rid=='23320818' and len(objects)==6,'six_Bianchi_transport_objects')
        require(objects[-1]['ordinary_HTTPS_requests_in_native_object_and_file_order']==objects[:5],'aggregate_whole_heterogeneous_originals')
        for i,x in enumerate(objects[:5]):
            require(type(x['HTTP_status']) is int and x['HTTP_status']==200 and type(x['response_headers_in_received_order']) is list,'native_112_status_header_pairs')
            require(('ordinal' in x) is (i>0) and ('body_path' in x) is (i>0) and 'body' not in x and 'MD5' not in x,'actual_heterogeneous_fields')
            require(('native_MD5_match' in x) is (i>=3),'native_asset_match_boolean_only')

def normalize_abstract(rid,source,c):
    n=c['source_binding']['abstract_normalization']
    if rid=='23383952':
        pairs=[("Morpurgo's",'Morpurgo’s'),(r'\(13/20\)','13/20'),(r'\(321/500\)','321/500'),('min--max','min–max')]
    elif rid=='23539734':pairs=n['replacement_order']
    else:pairs=list(n['exact_presentational_replacements'].items())
    for a,b in pairs:source=source.replace(a,b)
    return ' '.join(source.split())

def _source_manifest(paper,rid):
    S=paper/'sources';m=load(S/'SOURCE_READY_MANIFEST.json');s=load(S/'SOURCE_READY_SEAL.json')
    mk='SOURCE_READY_MANIFEST_SHA256' if rid=='22929857' else 'manifest_sha256'
    rk='SOURCE_READY_SHA256' if rid=='22929857' else 'source_ready_sha256' if rid in {'23124601','23320818'} else 'SOURCE_READY_sha256'
    require(bind(S/'SOURCE_READY_MANIFEST.json')['sha256']==s[mk] and bind(S/'SOURCE_READY.json')['sha256']==s[rk],'native_ready_seal')
    rows=m['files']
    if (S/'SOURCE_FINAL_MANIFEST.json').exists():
        fm=load(S/'SOURCE_FINAL_MANIFEST.json');fs=load(S/'SOURCE_FINAL_SEAL.json')
        expected=fs['manifest']['sha256'] if rid in {'23333046','23383952'} else fs['manifest_sha256']
        require(bind(S/'SOURCE_FINAL_MANIFEST.json')['sha256']==expected,'native_final_source_seal');rows=rows+fm['files']
    dk='SHA256' if rid=='22929857' else 'sha256'
    seen=set()
    for x in rows:
        if x['path'] in seen:continue
        seen.add(x['path']);p=contained(S,x['path'])
        require(type(x['bytes']) is int and bind(p)=={'bytes':x['bytes'],'sha256':x[dk]},'complete_native_manifest_entry')

def _whole_source_objects(rid,paper,c,g,ready,api,transports):
    b=c['source_binding'];S=paper/'sources'
    if rid in {'23124601','23333046'}:
        require(same(b['source_receipt_original'],ready) and same(g['source_receipt_original'],ready),'whole_native_readiness')
        require(same(b['transport_receipt_original'],transports[0]) and same(g['transport_receipt_original'],transports[0]),'whole_original_transport_list')
    else:
        require(same(b['whole_original_source_ready'],ready) and same(g['whole_original_source_ready'],ready),'whole_original_readiness_not_rewritten')
        require(same(b['whole_native_record'],api),'whole_native_record')
        for k,n in [('whole_native_latest_record','latest.raw.json'),('whole_native_versions','versions.raw.json')]:require(same(b[k],load(S/n)),'whole_native_endpoint:'+k)
        if rid=='23383952':require(same(b['whole_native_transport_receipts'],transports[0]) and same(g['whole_original_native_transport_receipts'],transports[0]),'whole_108_transports')
        if rid=='23539734':require(same(b['whole_original_native_transport_receipts'],transports[0]) and same(g['whole_original_native_transport_receipts'],transports[0]),'whole_110_transports')
        if rid=='22929857':
            require(same(b['whole_native_record_transport_receipt'],transports[0]) and same(b['whole_native_acquisition_transport_receipt'],transports[1]),'whole_two_111_transport_objects')
            require(same(b['whole_native_files_endpoint'],load(S/'files.raw.json')),'whole_richer_files_endpoint')
        if rid=='23320818':
            require([x['original'] for x in b['whole_native_transport_objects']]==transports and same(b['whole_native_transport_objects'],g['whole_native_transport_objects']),'whole_all_six_112_objects')
            for x in b['whole_native_transport_objects']:require(bind(contained(paper,x['path']))['sha256']==x['sha256'],'112_each_original_transport_binding')

def validate_authorities(rid,c,g,science):
    """Pure typed whole-authority/gate guard for meaningful in-memory faults."""
    require(rid in IDS,'supported_authority_ID')
    require(g['status']==(STATUSES[rid] if rid in {'23124601','23333046'} else 'PRIVATE_EDITORIAL_PREPARED_UNPUBLISHED'),'literal_editorial_preparation_status')
    require(c.get('follow_up') is None and g.get('follow_up') is None and c.get('canonical_url') is None and g.get('canonical_url') is None and c.get('AA') is None and g.get('AA') is None,'historical_null_gates')
    for obj in [g,c['review_metadata']]:
        for k in ('rendered','deployed','rendered_public_copy_approved','rendered_copy_verified','local_http_verified','live_http_verified','live_verified','browser_verified','native_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received','production_integration_authorized','publication_clearance','ready_to_publish','canonical_verified'):
            if k in obj:require(obj[k] is False,'historical_false_gate:'+k)
    require(science['status']==STATUSES[rid] and (g['status'] if rid in {'23124601','23333046'} else g['scientific_status'])==STATUSES[rid],'literal_qualified_status')
    require(same(g['root_clearance_record' if rid in {'23124601','23333046'} else 'whole_root_scientific_clearance_record'],science),'whole_root_science_preserved')
    require(set(g['reviews'])==set(science['reviews'])=={'scope','analytic','adversarial'},'three_whole_original_families')
    for role,item in g['reviews'].items():
        orig=science['reviews'][role]
        if rid=='23539734':require(same(item,orig),'whole_native_root_family_entry')
        else:
            ek='root_clearance_review_object' if rid=='23383952' else 'root_authority_entry'
            vk='whole_original_custom_verdict' if rid=='23383952' else 'verdict'
            ok='whole_original_custom_verdict' if rid in {'23124601','23333046','23383952'} else 'verdict_original'
            require(same(item[ek],orig) and same(item[vk],orig[ok]),'whole_custom_verdict_no_coercion')

def load_bundles():
    frozen=frozen_inputs();out=[]
    for rid in IDS:
        T=PROGRAMME/'papers'/rid;S=T/'sources';c=load(T/'publication.json');g=load(T/'promotion.json');b=c['source_binding'];spec=frozen['native_specs'][rid]
        ready=load(S/'SOURCE_READY.json');api=load(S/'record.raw.json');meta=api['metadata']
        require(type(ready['record_id']) is int and ready['record_id']==api['id']==int(rid) and type(api['id']) is int,'actual_integer_native_ID')
        require(type(b['record_id']) is str and b['record_id']==g['record_id']==rid,'literal_config_ID_types')
        require(c['publication_date']==meta['publication_date']==DATES[rid] and c['version']==meta['version']==VERSIONS[rid],'API_declared_date_version')
        require(c['title']==api['title']==ready['title'] and c['doi']==api['doi'],'native_exact_work_identity')
        require(c['source_binding']['record_created_utc']==api['created'] and b['record_updated_utc']==api['updated'],'creation_not_publication_date')
        require(c['author']=='Alec Kriebel' and c['orcid']=='https://orcid.org/0009-0001-9320-500X' and meta['license']['id']=='cc-by-4.0','author_ORCID_deposit_license')
        require(c['license']=='CC BY 4.0' and c['license_url']=='https://creativecommons.org/licenses/by/4.0/','exact_article_license')
        require(c.get('code_license')==('MIT' if rid=='22929857' else 'CC BY 4.0' if rid=='23539734' else None),'record_specific_code_license_no_imported_MIT')
        require(b['manuscript_version'] is None and b['manuscript_version_printed'] is False if rid in {'23124601','23333046'} else b['manuscript_version']==VERSIONS[rid],'printed_vs_API_version')
        science=load(spec['whole_root_science']['path']);require(bind(spec['whole_root_science']['path'])['sha256']==g['root_clearance_sha256'],'pinned_root_scientific_authority')
        validate_authorities(rid,c,g,science)
        assets=native_assets(rid,T,ready,api,c,spec);trans=[load(S/n) for n in spec['transport_files']]
        validate_transports(rid,T,trans,spec);_source_manifest(T,rid);_whole_source_objects(rid,T,c,g,ready,api,trans)
        tex=contained(T,b['source_tex_path']);require(bind(tex)['sha256']==b['source_tex_sha256'],'controlling_TeX')
        match=re.findall(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex.read_text(),re.S)
        require(len(match)==1 and (match[0].strip()==b['abstract_tex'] if rid=='23383952' else match[0]==b['abstract_tex']),'complete_original_abstract_substring:'+rid)
        abstract=normalize_abstract(rid,match[0],c);require(abstract==c['abstract'],'authorized_abstract_presentation_only')
        bib=contained(T,spec['citation_path']).read_bytes();require(('prepared_bibtex' not in c or bib==c['prepared_bibtex'].encode()) and c['additional_assets']==[],'exact_prepared_citation_four_assets')
        from pypdf import PdfReader
        import subprocess
        reader=PdfReader(T/'sources'/c['pdf_filename'])
        extracted=subprocess.run(['pdftotext','-enc','UTF-8',str(T/'sources'/c['pdf_filename']),'-'],capture_output=True,check=True,timeout=20).stdout.decode('utf8')
        pages=extracted.split('\f')
        if not pages[-1].strip():pages.pop()
        chars=[len(p.strip()) for p in pages]
        require(len(reader.pages)==len(chars)==c['pdf_pages'] and all(x>100 for x in chars),'complete_searchable_actual_reader')
        out.append({'rid':rid,'paper':T,'c':c,'g':g,'asset_view':assets,'prepared_bibtex':bib,'normalized_source_abstract':abstract,'pdf_chars_per_page':chars})
    return out
