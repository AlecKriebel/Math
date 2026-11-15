#!/usr/bin/env python3
"""Source-only independent contract freeze. Writes only this new audit namespace."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

A=Path(__file__).resolve().parent
P=A.parents[1]
if (A/'INITIAL_EXPECTATIONS_SEAL.json').exists(): raise RuntimeError('initial expectations immutable')
def now(): return datetime.now(timezone.utc).isoformat()
def load(p): return json.loads(p.read_bytes())
def pin(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def put(n,x):
    p=A/n
    if not p.resolve().is_relative_to(A):raise ValueError('outside own audit namespace')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def check(e):
    p=Path(e['path']);b=p.read_bytes()
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e.get('SHA256',e.get('sha256')):raise ValueError('changed bytes '+str(p))
    return b
def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

external={}; namespaces=[]; wrappers=[]; targets=[]; outputs=[]
def bind(p):
    e=pin(p);external[e['path']]=e;return e
def wrapper_walk(x,owner,filename,pointer=''):
    if isinstance(x,dict):
        if 'whole_literal_object' in x:
            if 'copy' in x:
                f=owner/x['copy']; expected={'path':str(f),'bytes':x['bytes'],'SHA256':x['SHA256']}
            elif 'file' in x:
                expected=x['file'];f=Path(expected['path'])
            else:raise ValueError('unknown literal wrapper '+filename+pointer)
            b=check(expected);bind(f)
            if not same(json.loads(b),x['whole_literal_object']):raise ValueError('typed/key/list literal mismatch '+filename+pointer)
            if isinstance(x.get('original'),dict) and 'path' in x['original']:
                if check(x['original'])!=b:raise ValueError('whole original/copy bytes differ')
                bind(Path(x['original']['path']))
            wrappers.append({'record_id':owner.parents[1].name,'container_file':str(owner/filename),'pointer':pointer,'whole_original_binding':expected,'whole_literal_type':type(x['whole_literal_object']).__name__,'typed_keys_lists_nulls_and_full_value_equal':True})
        for k,v in x.items():wrapper_walk(v,owner,filename,pointer+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(x,list):
        for i,v in enumerate(x):wrapper_walk(v,owner,filename,pointer+'/'+str(i))

for rid,counts,adoptionSHA in [('23392409',(121,69),'e493881b10b281ea2a1bc6aa66d15063374073df2f6a9b99edc5ef5587dc61bf'),('23440943',(81,59),'e516ebd05ef8243a47f5b40bac31182a75751dcced857cb89ec5dbe9875b1ed6')]:
    paper=P/'papers'/rid;owner=paper/'reviews/editorial';source=paper/'sources'
    for folder,count,role in [(source,counts[0],'original_source'),(owner,counts[1],'adopted_editorial_owner')]:
        if any(p.is_symlink() for p in folder.rglob('*')):raise ValueError('symlink in protected namespace')
        files=[bind(p) for p in sorted(folder.rglob('*')) if p.is_file()]
        if len(files)!=count:raise ValueError('protected namespace extent changed '+str(folder))
        namespaces.append({'record_id':rid,'role':role,'path':str(folder),'complete_file_count':len(files),'files':files})
    rp=P/'verification'/('root-editorial-'+rid+'-20261115.json')
    if pin(rp)['SHA256']!=adoptionSHA:raise ValueError('root adoption pin')
    adoption=load(rp);bind(rp)
    for key in ['owner_final_seal','scientific_root_clearance','publication_config','promotion_config','requirements','adapter']:
        check(adoption[key]);bind(Path(adoption[key]['path']))
    original_main=(owner/'PUBLIC_MAIN.html').read_text();config=load(owner/'publication.json');src=load(source/'SOURCE_READY.json')
    reader=adoption['future_exact_reader_only_transform_authorized']
    if original_main.count(reader['from'])!=1 or not original_main.startswith('<main>'):raise ValueError('exact approved transformation precondition')
    expected=original_main.replace(reader['from'],reader['to'],1).replace('<main>','<main id="main">',1)
    dest=A/'EXPECTED_MAINS'/ (rid+'.html');dest.parent.mkdir(exist_ok=True);dest.write_text(expected)
    if config['abstract']!=adoption['original_full_abstract']:raise ValueError('full abstract adoption mismatch')
    if config['follow_up'] is not None or config['code_license'] is not None:raise ValueError('literal followup/code instrument')
    if config['canonical_url'] is not None or config['AA'] is not None:raise ValueError('historical canonical/AA nulls')
    if [x['original_api_file_object']['key'] for x in src['all_native_assets_in_original_order']]!=adoption['actual_native_order']:raise ValueError('native order')
    for name in ['PUBLIC_COPY.md','PUBLIC_MAIN.html','publication.json','promotion.json','PUBLICATION_REQUIREMENTS.json','SCHEMA_ADAPTER.json','SCHOLARLY_METADATA.json','SOURCE_PROTOCOL_BINDINGS.json','citation.bib','SEAL.json','MANIFEST.json']:
        q=owner/name;out=A/'inputs'/rid/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(q.read_bytes());bind(q)
        if name in ['publication.json','promotion.json','SOURCE_PROTOCOL_BINDINGS.json']:wrapper_walk(load(q),owner,name)
    for q,n in [(rp,'ROOT_EDITORIAL_ADOPTION.json'),(Path(adoption['scientific_root_clearance']['path']),'ROOT_SCIENTIFIC_CLEARANCE.json'),(source/'SOURCE_READY.json','SOURCE_READY.json')]:
        (A/'inputs'/rid/n).write_bytes(q.read_bytes());bind(q)
    if not same(config['source_binding']['whole_original_source_ready'],src):raise ValueError('whole SOURCE_READY literal value/order/type')
    base='research/'+config['slug']+'/'
    canonical=adoption['future_proposed_canonical_url']
    if not canonical.endswith('/'+config['slug']+'/'):raise ValueError('planned canonical')
    assetexpect=[]
    for asset in src['all_native_assets_in_original_order']:
        b=check(asset);f=asset['original_api_file_object']['key']
        if hashlib.md5(b).hexdigest()!=asset['original_api_file_object']['checksum'].split(':')[1]:raise ValueError('native asset checksum')
        outputs.append({'website_relative_path':base+f,'kind':'unchanged_native_asset','source':bind(Path(asset['path']))})
        assetexpect.append({'filename':f,'encodingFormat':asset['whole_original_native_files_entry']['mimetype'],'contentUrl':canonical+f,'sameAs':asset['original_api_file_object']['links']['self'],'license':'https://creativecommons.org/licenses/by/4.0/','whole_original_source_asset':asset})
        if (owner/'candidate'/f).read_bytes()!=b:raise ValueError('owner candidate asset differs')
    bib=owner/'citation.bib'
    if bib.read_bytes()!=(owner/'candidate/citation.bib').read_bytes() or bib.read_text()!=config['prepared_bibtex']:raise ValueError('complete Bib mismatch')
    if (rid=='23392409' and 'version =' in bib.read_text()) or (rid=='23440943' and 'version = {1.0.0}' not in bib.read_text()):raise ValueError('Bib version distinction')
    outputs.extend([{'website_relative_path':base+'citation.bib','kind':'unchanged_adopted_Bib','source':bind(bib)},{'website_relative_path':base+'index.html','kind':'new_standard_blog_article','expected_complete_main':pin(dest)}])
    # Copy raw objects byte-for-byte; derived expectations never replace them.
    fields={k:v for k,v in config.items() if k not in ['source_binding','review_metadata']}
    targets.append({'record_id':rid,'sheet_row':130 if rid=='23392409' else 131,'root_editorial_adoption':bind(rp),'owner_namespace_files':counts[1],'source_namespace_files':counts[0],'whole_public_config_unique_fields_in_original_order':fields,'complete_owner_main':bind(owner/'PUBLIC_MAIN.html'),'expected_complete_transformed_main':pin(dest),'exact_reader_transform':reader,'only_other_main_transform':'initial <main> becomes <main id="main">','full_unchanged_abstract':config['abstract'],'original_date':config['publication_date'],'native_version_present':src['version_field_present'],'native_version':src['version'],'printed_version_present':config['printed_version_field_present'],'printed_version':config['printed_version'],'native_assets_and_media_expectations_in_original_order':assetexpect,'future_canonical_proposal_not_current_authority':canonical,'follow_up':None,'code_license':None,'rights':'Original authored note/support/code broad CC BY4.0; third-party rights retained; no MIT instrument inferred.'})

outputs.extend([{'website_relative_path':'research/index.html','kind':'aggregate_exact_existing_cards_preserved_plus_two_new_cards'},{'website_relative_path':'sitemap.xml','kind':'aggregate_exact_existing_locations_preserved_plus_two_new_locations'}])
if len(outputs)!=11 or len({x['website_relative_path'] for x in outputs})!=11:raise ValueError('exact proposed11 output paths')
put('PROTECTED_NAMESPACE_MANIFEST.json',{'UTC':now(),'namespaces':namespaces,'total_complete_files':sum(len(n['files']) for n in namespaces),'website_baseline_or_writer_stage_examined':False})
put('WHOLE_LITERAL_OBJECT_LEDGER.json',{'UTC':now(),'whole_literal_wrappers':wrappers,'whole_wrapper_occurrences':len(wrappers),'whole_raw_configs_and_source_protocol_copied_unchanged':True,'comparison':'recursive exact Python types and dictionary key order/list order/full values; raw source/copy byte checks where wrappers identify them','historical_CLOSED_UNREAD_pending_and_private_status_values_not_rewritten':True})
put('EXPECTED_OUTPUT_PATHS.json',{'proposed_total_outputs':11,'proposed_new_leaves':9,'proposed_changed_aggregates':2,'paths':outputs,'actual_website_baseline_inspected':False})
put('INDEPENDENT_EXPECTATIONS.json',{'schema':'independent_source_only_integration_expectations_130131_v1','UTC':now(),'informed_role_disclosure':'Prior130 editorial fact audit,131 editorial authoring, unrelated earlier acquisitions/stage work and completed130131 correspondence. This is independent integration/code scrutiny from separately frozen source expectations, not a new scientific family. No writer-stage code/copy/opinion exposed before this seal.','targets':targets,'head_contract':{'standard_shared_blog_frame':'Use root-approved shared blog header/footer/stylesheet, skip link targeting main id; actual future website frame awaits separate GO.','canonical':'Each future article has one exact local trailing-slash canonical from root proposal; not an already live canonical certification.','robots':'index,follow for future production article; no private noindex leakage','social_and_scholarly_metadata':'Exact adopted title/description/author/ORCID/original publication date; exact DOI; unchanged original full abstract; citation PDF local original asset; absent130 version omitted rather than default/null public version;131 exact1.0.0.','JSONLD':'Linked WebPage and ScholarlyArticle at proposed local canonical, consistent graph identifiers, exact adopted abstract/title/date/DOI/author/status/CCBY; MediaObject encodings for all original assets in native order, exact local article-root contentUrl/native sameAs/CCBY and MIME types. Do not freeze arbitrary serializer whitespace or unsupported graph fragment spellings.','full_main':'Exact stored expected mains; only two literal root-approved changes, preserving every full paragraph, theorem/limit/credit/disclosure and original relative download link.','article_root_downloads':'No files/ relocation or renamed originals; five native bytes and two Bib bytes unchanged.'},'custody_contract':'Complete121/69/81/59 source/editorial namespaces unchanged. Whole source/native/root/custom original objects remain full, typed, ordered and historically literal; no scientific verdict normalization or UNREAD/CLOSED rewrite.','future_stage_scope':'Exactly nine new leaves and two existing aggregates; source-only preparation until actual root GO and immutable writer FINAL. No site/core/config/Sheet/Git/deploy/redirect/contact mutation.','planning_only':{'current_root_report':{'website_commit_abbreviated_as_supplied':'27cd…','public_files':605,'research_index_entries':90,'sitemap_locations':91,'independently_measured_here':False},'required_future_baseline_after_separate127128_publication_and_root_GO':{'public_files':614,'research_index_entries':92,'sitemap_locations':93,'actual_commit':None,'independently_measured_here':False},'proposed_after_this_two_article_stage':{'public_files':623,'research_index_entries':94,'sitemap_locations':95,'independently_measured_here':False},'native_verified88':'Current root report only; not independently reverified here.'},'held_gates':{'actual_new_website_GO_received':False,'writer_immutable_FINAL_received':False,'website_baseline_inspected_listed_or_frozen':False,'writer_stage_code_copy_or_opinions_read':False,'production_authority':False},'source_only_preparation_percent':100,'overall_independent_integration_audit_percent':25})
put('INPUT_MANIFEST.json',{'UTC':now(),'files':list(external.values()),'source_only':True,'website_or_writer_namespace_paths':[]})
(A/'RESEARCH_LOG.md').write_text((A/'RESEARCH_LOG.md').read_text()+'- '+now()+' — 25% overall audit /100% source-only expectation preparation: Complete adopted copy/mains, unique config fields, requirements/adapter/scholarly/Bib and root transforms read; complete raw repeated objects compared as data without scientific replay. Four source/owner namespaces frozen by exact330-file inventory. Website baseline and writer stage remain unexamined. Await both future root GO and immutable writer FINAL.\n')
print(json.dumps({'status':'SOURCE_ONLY_EXPECTATIONS_PREPARED','protected_files':sum(len(n['files']) for n in namespaces),'literal_wrapper_occurrences':len(wrappers),'proposed_outputs':len(outputs),'website_or_writer_reads':0}))
