"""Proposed authenticated consumer for exactly three immutable cleared records.
All original objects remain whole; only the returned asset view is ephemeral.
"""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re
from bosonic_source import contained_file,digest
from published_assets import safe_relative
SG_IDS={'23181280','23442760','23395703'}
PINS={'23181280': {'publication': '062efd540d71aee6da2423a524a3b663752433738327ada7dd6268eafec967c8',
              'promotion': 'aa486d825a63fb1710e6b67cf21b33e0dc274d0a9d239e3a7767abaf6d85deea',
              'editorial': '02e1ec1a4a5d19c648e5670811eb81ac11ec536b4c6f1baa62af29310898e2f8',
              'science': 'db8b20ff1321cb87e2e198ccacc4c7f6eb9f55d8eee2f6993e7f6e004c83c2a8',
              'editorial_seal': '069f07aba507841b1ae7c10edfce4b1fe8c6f46f772b6f31c58928415017c329',
              'editorial_manifest': '719beecf3eefcfe880a5db34409ec2644d0e3dddd3201b7f015e6baf580c6288'},
 '23442760': {'publication': '49493858d807edc709dbbcb1555cc85572a8876f8a65c8c2f05dd6f879e56d0a',
              'promotion': 'f37589b4033f9083d1056f36a67a03cd65ea9cb98d4d4d810df0fb3e2d0cd136',
              'editorial': 'f9fbc0cd6bdf27eccdd562cf488db0fc916d848338b6d1849e2454718474718a',
              'science': '1ae733563c14ddbcdd6a446a61376aeddd569e09e637f18490c57eb2310d36bd',
              'editorial_seal': '68f8df479dede0ea7b65d87fd206ad0d23331f6beb0969afedc1ffd719bb9cde',
              'editorial_manifest': '029ff665812db6ec543949d68e46fe9a31131bc8c81c01ba89274d5fcb628e64'},
 '23395703': {'publication': '2cff24dbd55f933bf3b0124208d8ce7fbe9f0b422300eb62947699ab953cbc31',
              'promotion': '4a04a58af1ac1abc930c33427c89a4c7057f244f73d299624dc1966843026024',
              'editorial': '5aeba83c3805618f17aa3a7903df7fb0e53e108d6ea9568cae64473b813a6fb5',
              'science': 'c0120ac14fdb87954a8be3f85058b8446abe033d2570ff4906f51c1ae695206b',
              'editorial_seal': '2a1acfdc2968c942cada8bce7a114e623270c4f9f28b72f9610c600a6f4e0101',
              'editorial_manifest': '1825700c88893029d96bd06a975131efabd12158e0b3455de8aad46db77910fc'}}
NORMALIZATIONS={'23181280': {'$\\{0,1,2\\}$': '{0,1,2}', '$\\{1,2,3\\}$': '{1,2,3}'},
 '23442760': {'$K\\subset\\R^n$': 'K⊂ℝⁿ',
              '$f$': 'f',
              '$2r$': '2r',
              '$O_{K,f}(r^{-2})$': 'O_{K,f}(r⁻²)',
              '$r\\ge1$': 'r≥1'},
 '23395703': {'$Q=xy(x-y)(x-2y)zw(x+z+w)$': 'Q=xy(x-y)(x-2y)zw(x+z+w)',
              '$8$': '8',
              '$7$': '7',
              'Bigatti--Palezzato--Torielli': 'Bigatti–Palezzato–Torielli',
              'Hilbert--Burch': 'Hilbert–Burch'}}
MATH={'23181280': {'N\\ge1': 'N≥1',
              '2N|E|': '2N|E|',
              '\\{0,1,2\\}': '{0,1,2}',
              '\\{1,2,3\\}': '{1,2,3}',
              'N(N-1)': 'N(N−1)',
              'p': 'p',
              'q': 'q',
              'h': 'h',
              'K=2m+n': 'K=2m+n',
              'q\\ge m': 'q≥m',
              'h=1': 'h=1',
              'q=m': 'q=m',
              'p+2q=K+(1-h)+(q-m)': 'p+2q=K+(1−h)+(q−m)'},
 '23442760': {'K\\subset\\mathbb R^n': 'K⊂ℝⁿ',
              'n\\ge1': 'n≥1',
              'f': 'f',
              'H_r(f,K)': 'Hᵣ(f,K)',
              '\\int_K f q\\,dx': '∫_K f q dx',
              'q': 'q',
              '2r': '2r',
              '\\int_K q\\,dx=1': '∫_K q dx=1',
              'r\\ge1': 'r≥1',
              '0\\le H_r(f,K)-f_*\\le C_nG/r^2': '0≤Hᵣ(f,K)−f*≤CₙG/r²',
              'f_*=\\min_K f': 'f*=min_K f',
              'a': 'a',
              'H=\\max_K\\|\\nabla^2f\\|_{\\mathrm{op}}': 'H=max_K ‖∇²f‖_op',
              '\\gamma=1+H/2': 'γ=1+H/2',
              'g(x)=\\nabla f(a)\\cdot(x-a)+\\gamma\\|x-a\\|^2': 'g(x)=∇f(a)·(x−a)+γ‖x−a‖²',
              'G=\\max_K g': 'G=max_K g',
              '0<G<\\infty': '0<G<∞',
              'C_n=4(n+2)^2(\\pi/2)^{2n+4}(1+2^{n+2})': 'Cₙ=4(n+2)²(π/2)^(2n+4)(1+2^(n+2))',
              'K': 'K',
              'C^2': 'C²',
              'g': 'g',
              'u=g/G': 'u=g/G',
              'F(t)\\le(t/s)^nF(s)': 'F(t)≤(t/s)ⁿF(s)',
              '0<s\\le t': '0<s≤t',
              'F(t)=\\operatorname{vol}_n\\{x\\in K:u(x)\\le t\\}': 'F(t)=volₙ{x∈K:u(x)≤t}',
              'K=[0,1]': 'K=[0,1]',
              'f(t)=t': 'f(t)=t',
              'H_r(f,K)\\ge1/[4(r+1)^2]': 'Hᵣ(f,K)≥1/[4(r+1)²]',
              'f(t,y)=t': 'f(t,y)=t',
              '[0,1]\\times[-1,1]^{n-1}': '[0,1]×[−1,1]^(n−1)',
              'r^{-2}': 'r⁻²',
              'O(\\log^2 r/r^2)': 'O((log r)²/r²)'},
 '23395703': {'K': 'K',
              'S=K[x,y,z,w]': 'S=K[x,y,z,w]',
              'Q=xy(x-y)(x-2y)zw(x+z+w)': 'Q=xy(x−y)(x−2y)zw(x+z+w)',
              'J=(Q_x,Q_y,Q_z,Q_w)': 'J=(∂Q/∂x,∂Q/∂y,∂Q/∂z,∂Q/∂w)',
              'B': 'B',
              'x_1>x_2>x_3>x_4': 'x₁>x₂>x₃>x₄',
              'p=\\min\\{d\\ge0:x_2^d\\in B\\}=8': 'p=min{d≥0:x₂ᵈ∈B}=8',
              'K[x_1,x_2,x_3]': 'K[x₁,x₂,x₃]',
              'x_3': 'x₃',
              'p': 'p',
              'd_0+1=p': 'd₀+1=p',
              '1,2,3': '1,2,3',
              'H_2(6,7,8)=(3,1,0)': 'H₂(6,7,8)=(3,1,0)',
              'H_3(5,6,7)=(21,24,24)': 'H₃(5,6,7)=(21,24,24)',
              'x_4': 'x₄',
              'U_{2,4}': 'U_(2,4)',
              'U_{3,4}': 'U_(3,4)',
              'x': 'x',
              '0\\to S(-7)^3\\oplus S(-9)\\to S(-6)^5\\to J^{\\mathrm{top}}\\to0': '0→S(−7)³⊕S(−9)→S(−6)⁵→J^(top)→0',
              'J^{\\mathrm{top}}': 'J^(top)',
              'J': 'J'}}
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
