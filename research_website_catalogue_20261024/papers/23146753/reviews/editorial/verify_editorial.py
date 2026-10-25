"""Read-only static editorial verifier and in-memory rejection controls.

No rendering, HTTP, source/control execution, source aliases or output writes.
"""
from pathlib import Path
import copy, hashlib, json, re, stat, zipfile

O=Path(__file__).resolve().parent;D=O.parent.parent;P=D.parent.parent;S=D/'sources'
def load(p):return json.loads(p.read_text())
def bind(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return dict(bytes=p.stat().st_size,sha256=h.hexdigest())
def need(c,msg):
    if not c:raise RuntimeError(msg)

clearpath=P/'verification/root-clearance-23146753-20261025.json';clear=load(clearpath)
need(bind(clearpath)['sha256']=='9f03be990c7b547ebc341908662b241f84b77ffb9b26f9d834d72407d34b7860','Exact root authority')
ready=load(S/'SOURCE_READY.json');raw=load(S/'record.raw.json');transport=load(S/'api-and-file-receipts.json')
tex=(S/'published-source/mtp2_edge_closure.tex').read_text()
abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
abstract=' '.join(abstract_tex.replace('MTP$_2$','MTP₂').replace('Conjecture~1','Conjecture 1').split())
pub=load(D/'publication.json');prom=load(D/'promotion.json');sections=load(O/'public-sections.json')
reader=load(O/'READER_REQUIREMENTS.json');text=(O/'PUBLIC_COPY.md').read_text();bib=(O/'CITATION.bib').read_text()
pdf_asset=next(x for x in ready['all_assets'] if x['original_api_file_object']['key']=='mtp2-edge-closure-note.pdf')
zip_asset=next(x for x in ready['all_assets'] if x['original_api_file_object']['key']=='mtp2-edge-closure-verification.zip')

def validate(p,q,sec,r,copytext,citation):
    sb=p['source_binding'];md=p['review_metadata']
    need(p['title']==ready['title']==raw['metadata']['title'],'Exact title')
    need(p['abstract']==abstract and p['abstract_heading']=='Original abstract' and p['abstract_is_original'] is True,'Full original abstract')
    need('\n' not in p['abstract'] and copytext.count('## Original abstract\n\n'+abstract+'\n')==1,'One indexable complete abstract paragraph')
    need(p['publication_date']==raw['metadata']['publication_date']=='2026-10-04','Declared date')
    need(p['version']==q['version']==sb['zenodo_version']==raw['metadata']['version']=='1.0','Actual API edition')
    need(sb['manuscript_version'] is None and sb['manuscript_version_printed'] is False,'Unprinted manuscript version')
    need(sb['record_created_utc']==raw['created'] and sb['record_updated_utc']==raw['updated'],'Actual creation/update')
    need(p['edition_label']==p['citation_edition_label']=='Zenodo version 1.0','Visible/citation edition')
    need('4 October 2026' in p['edition_note'] and 'prints no version number' in p['edition_note'],'Edition note')
    need(p['license']=='CC BY 4.0' and p['license_url']=='https://creativecommons.org/licenses/by/4.0/','License header/schema')
    need('CC BY 4.0' in (S/'published-source/LICENSE.txt').read_text(),'Original license')
    need(p['doi']==ready['doi'] and p['author']=='Alec Kriebel' and p['orcid']=='https://orcid.org/0009-0001-9320-500X','Author DOI ORCID')
    need(sb['source_receipt_original']==q['source_receipt_original']==ready,'Whole original readiness object')
    need(sb['all_assets']==q['all_assets']==ready['all_assets'],'Native asset array/order')
    need(sb['published_file_objects']==q['published_file_objects']==raw['files'],'Whole actual file objects')
    need(sb['transport_receipt_original']==q['transport_receipt_original']==transport,'Whole five actual transport objects')
    need(len(transport)==5 and all(x['status']==200 for x in transport),'Five actual HTTP200 receipts')
    need(sb['source_assets_field']=='all_assets' and sb['source_receipt_path']=='sources/SOURCE_READY.json','Native source interface')
    need(sb['metadata_path']=='sources/normalized-metadata.json' and sb['raw_record_path']=='sources/record.raw.json','Actual metadata interface')
    need(sb['transport_receipt_path']=='sources/api-and-file-receipts.json','Actual transport path')
    for pathkey,hashkey in [('metadata_path','metadata_sha256'),('raw_record_path','raw_record_sha256'),('source_receipt_path','source_receipt_sha256'),('recursive_archive_inventory_path','recursive_archive_inventory_sha256'),('transport_receipt_path','transport_receipt_sha256'),('source_tex_path','source_tex_sha256'),('abstract_source','abstract_source_sha256'),('prepared_bibtex_path','prepared_bibtex_sha256')]:
        need(bind(D/sb[pathkey])['sha256']==sb[hashkey],'Complete publication source binding '+pathkey)
    for pathkey,hashkey in [('metadata_path','metadata_sha256'),('raw_record_path','raw_record_sha256'),('source_receipt_path','source_receipt_sha256'),('transport_receipt_path','transport_receipt_sha256')]:
        need(bind(D/q[pathkey])['sha256']==q[hashkey],'Complete promotion source binding '+pathkey)
    need(q['root_clearance_file']==md['root_clearance_file']==str(clearpath.relative_to(P)) and q['root_clearance_sha256']==md['root_clearance_sha256']==bind(clearpath)['sha256'],'Root authority file binding')
    need(q['root_custody_receipt']==clear['root_custody_receipt'] and q['root_custody_receipt_sha256']==bind(P/q['root_custody_receipt'])['sha256']==clear['root_custody_receipt_sha256'],'Complete root custody binding')
    need(sb['pdf_sha256']==pdf_asset['sha256'] and sb['supplement_sha256']==zip_asset['sha256'],'Original asset hashes')
    need(p['pdf_filename']==pdf_asset['original_api_file_object']['key'] and p['supplement_filename']==zip_asset['original_api_file_object']['key'],'Exact original filenames')
    need(sb['abstract_tex']==abstract_tex and sb['abstract_source_sha256']==hashlib.sha256(abstract_tex.encode()).hexdigest(),'Exact raw abstract')
    need(sb['abstract_normalization']==dict(whitespace='fold consecutive whitespace into one ordinary space',exact_presentational_replacements={'MTP$_2$':'MTP₂','Conjecture~1':'Conjecture 1'},no_word_or_sentence_omission=True),'Exact abstract presentation rule')
    need(p['pdf_pages']==5 and sb['public_page_reader_pdf_count']==1 and sb['total_distinct_reader_pdf_count']==1,'One distinct five-page reader')
    need((sb['archive_outer_regular_file_count'],sb['archive_embedded_pdf_count'],sb['nested_archive_count'])==(13,1,0),'Exact archive inventory')
    need(q['status']==md['scientific_clearance_status']==clear['status']=='PASS_WITH_EXPLICIT_PRIMARY_AND_PRIORITY_LIMITS','Exact separate root status')
    need(q['root_clearance_record']==clear,'Whole exact root object')
    for fam,entry in clear['reviews'].items():
        v=load(P/entry['verdict']);b=q['reviews'][fam]
        need(b['verdict']==v==entry['whole_original_custom_verdict'],'Whole original '+fam+' verdict')
        need(b['root_authority_entry']==entry,'Separate whole '+fam+' root entry')
        need(bind(P/entry['report'])['sha256']==b['report_sha256']==entry['report_sha256'],'Complete '+fam+' report binding')
        need(bind(P/entry['verdict'])['sha256']==b['verdict_sha256']==entry['verdict_sha256'],'Complete '+fam+' verdict binding')
    for obj in [p,q]:
        for field in ['canonical_url','AA','follow_up']:need(obj[field] is None,'Null publication/follow-up field')
    for field in ['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published','root_editorial_clearance_received']:
        need(q[field] is False and md[field] is False,'Later publication gates false')
    need(md['rendered'] is False and md['deployed'] is False and md['native_sheet_aa_url'] is None and q['native_sheet_aa_url'] is None,'No render/live/native authority')
    need(q['human_peer_review'] is False and q['formal_machine_verification'] is False and q['source_repair'] is False,'Scientific status preserved')
    for key,value in sec.items():need(p[key]==value,'Full public section '+key)
    for key in ['plain_language','result','why_it_works','limitations']:
        for paragraph in p[key]:need('\n\n'+paragraph+'\n' in copytext,'Full copy paragraph '+key)
    for bg in p['background']:
        need(f"[{bg['title']}]({bg['url']}) {bg['note']}" in copytext,'Full prior-work credit')
    for key in ['status','ai_disclosure','collaboration','reader_intro','edition_note']:
        need('\n\n'+p[key]+'\n' in copytext,'Full copy status/metadata '+key)
    need(copytext.startswith('# '+p['title']+'\n'),'Copy title')
    need('Manuscript and declared publication date: 4 October 2026 · Zenodo version 1.0' in copytext,'Visible header date/edition')
    need(not any(token in copytext for token in ['SHA256','SOURCE_READY','root-clearance','/Users/','2026-10-25','replay','reviewer-control']),'No private audit narrative')
    base='/research/'+p['slug']+'/'
    expected=[('Open PDF',base+p['pdf_filename'],False),('Download PDF',base+p['pdf_filename'],True),
              ('Download original PDF from Zenodo',pdf_asset['original_api_file_object']['links']['self'],True),
              ('Download complete ZIP',base+p['supplement_filename'],True),
              ('Download original complete ZIP from Zenodo',zip_asset['original_api_file_object']['links']['self'],True),
              ('Download BibTeX',base+'citation.bib',True)]
    need([(x['label'],x['href'],x['download']) for x in r['required_links']]==expected,'Exact open/download/original links')
    need(r['pdf_iframe_count']==1 and r['pdf_iframe_uses_unchanged_local_bytes'] is True,'One complete local iframe')
    need(r['planned_path']==base and r['pdf_local_href']==base+p['pdf_filename'] and r['zip_local_href']==base+p['supplement_filename'],'Exact local asset paths')
    need(r['article_assets']==['index.html',p['pdf_filename'],p['supplement_filename'],'citation.bib'] and r['extra_assets']==[] and p['additional_assets']==[],'Only complete original assets plus citation')
    for label,url,_ in expected:need(f'[{label}]({url})' in copytext,'Copy reader link')
    need(p['prepared_bibtex']==r['prepared_bibtex']==citation,'Exact prepared BibTeX')
    need(sb['prepared_bibtex_sha256']==hashlib.sha256(citation.encode()).hexdigest(),'BibTeX binding')
    for token in ['date = {2026-10-04}','version = {1.0}','doi = {10.5281/zenodo.23146753}','orcid = {0009-0001-9320-500X}','author = {Kriebel, Alec}']:
        need(token in citation,'Citation metadata')
    need(50<=len(p['description'])<=160,'SEO description length')

validate(pub,prom,sections,reader,text,bib)
controls=[]
def reject(label,change):
    a,b,c,d,e,f=copy.deepcopy(pub),copy.deepcopy(prom),copy.deepcopy(sections),copy.deepcopy(reader),text,bib
    modified=change(a,b,c,d,e,f)
    if isinstance(modified,tuple) and len(modified)==2:e,f=modified
    try:validate(a,b,c,d,e,f)
    except RuntimeError as error:controls.append(dict(case=label,outcome='REJECTED',reason=str(error)))
    else:raise RuntimeError('False negative in editorial control: '+label)
reject('truncated_original_abstract',lambda a,b,c,d,e,f:a.__setitem__('abstract',a['abstract'].split('.')[0]+'.'))
reject('generic_root_PASS',lambda a,b,c,d,e,f:b.__setitem__('status','PASS'))
reject('changed_original_scope_history',lambda a,b,c,d,e,f:b['reviews']['scope']['verdict'].__setitem__('production_or_publication_authority',True))
reject('changed_adversarial_null',lambda a,b,c,d,e,f:b['reviews']['adversarial']['verdict'].__setitem__('root_adoption','PASS'))
reject('incomplete_separate_root_entry',lambda a,b,c,d,e,f:b['reviews']['analytic']['root_authority_entry'].pop('whole_original_custom_verdict'))
reject('reversed_native_assets',lambda a,b,c,d,e,f:a['source_binding']['all_assets'].reverse())
reject('fabricated_file_checksum',lambda a,b,c,d,e,f:a['source_binding']['published_file_objects'][0].__setitem__('checksum','md5:bad'))
reject('fabricated_HTTP206',lambda a,b,c,d,e,f:a['source_binding']['transport_receipt_original'][0].__setitem__('status',206))
reject('rewritten_original_checksum_header',lambda a,b,c,d,e,f:a['source_binding']['transport_receipt_original'][4]['headers'].__setitem__('oc-checksum','MD5:0afc4fd82272a87b678e0efce8beea0d'))
reject('printed_version_invented',lambda a,b,c,d,e,f:a['source_binding'].__setitem__('manuscript_version','1.0'))
reject('creation_date_conflated',lambda a,b,c,d,e,f:a['source_binding'].__setitem__('record_created_utc','2026-10-04T00:00:00Z'))
reject('wrong_declared_date',lambda a,b,c,d,e,f:a.__setitem__('publication_date','2026-10-25'))
reject('wrong_license',lambda a,b,c,d,e,f:a.__setitem__('license','CC0'))
reject('changed_PDF_hash',lambda a,b,c,d,e,f:a['source_binding'].__setitem__('pdf_sha256','0'*64))
reject('changed_metadata_hash',lambda a,b,c,d,e,f:a['source_binding'].__setitem__('metadata_sha256','0'*64))
reject('changed_root_authority_hash',lambda a,b,c,d,e,f:b.__setitem__('root_clearance_sha256','0'*64))
reject('changed_abstract_normalizer',lambda a,b,c,d,e,f:a['source_binding']['abstract_normalization'].__setitem__('exact_presentational_replacements',{}))
reject('omitted_scope_paragraph',lambda a,b,c,d,e,f:a['result'].pop())
reject('removed_older_GL_credit',lambda a,b,c,d,e,f:a['background'].pop())
reject('missing_full_disclosure',lambda a,b,c,d,e,f:(e.replace(a['ai_disclosure'],''),f))
reject('private_hash_narrative',lambda a,b,c,d,e,f:(e+'\nSHA256 private audit\n',f))
reject('duplicate_reader_iframe',lambda a,b,c,d,e,f:d.__setitem__('pdf_iframe_count',2))
reject('missing_original_PDF_download',lambda a,b,c,d,e,f:d['required_links'].pop(2))
reject('subset_ZIP_asset',lambda a,b,c,d,e,f:d.__setitem__('zip_local_href','/research/subset.zip'))
reject('wrong_citation_edition',lambda a,b,c,d,e,f:a.__setitem__('citation_edition_label','Version 2.0'))
reject('wrong_prepared_BibTeX',lambda a,b,c,d,e,f:(e,f.replace('date = {2026-10-04}','date = {2026-10-25}')))
reject('live_gate_advanced',lambda a,b,c,d,e,f:b.__setitem__('live_http_verified',True))
reject('canonical_prematurely_assigned',lambda a,b,c,d,e,f:a.__setitem__('canonical_url','https://example.org/'))
reject('non_null_followup',lambda a,b,c,d,e,f:a.__setitem__('follow_up','contact author'))

before=load(O/'BEFORE_BINDINGS.json')['files']
for path,spec in before.items():need(bind(Path(path))==spec,'Earlier original changed: '+path)
protected=load(O/'PROTECTED_PRIOR_PACKAGES.json')['bindings']
for path,spec in protected.items():need(bind(Path(path))==spec,'Earlier private manifest/seal changed: '+path)
original_map={name:S/name for name in ['SOURCE_READY.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_MANIFEST.json','SOURCE_SEAL.json','normalized-metadata.json','record.raw.json','latest.raw.json','versions.raw.json','api-and-file-receipts.json','assets-acquired.json','archive-members.json']}
original_map.update({'verdict-'+fam+'.json':P/r['verdict'] for fam,r in clear['reviews'].items()})
original_map.update({'root-clearance.json':clearpath,'root-custody.json':P/clear['root_custody_receipt']})
for name,path in original_map.items():need((O/'original-objects'/name).read_bytes()==path.read_bytes(),'Whole raw object copy '+name)
for asset in ready['all_assets']:
    p=Path(asset['path']);need(bind(p)['sha256']==asset['sha256'] and p.stat().st_size==asset['bytes'],'Original asset SHA/size')
    need(hashlib.md5(p.read_bytes()).hexdigest()==asset['md5']==asset['original_api_file_object']['checksum'].removeprefix('md5:'),'Original API MD5')
with zipfile.ZipFile(S/'mtp2-edge-closure-verification.zip') as z:
    need(len(z.infolist())==13,'Whole archive count')
    for info in z.infolist():
        need(not info.is_dir() and stat.S_ISREG(info.external_attr>>16),'Regular member')
        need(z.read(info)==(S/'published-source'/info.filename).read_bytes(),'Exact archive member/extraction')
need((S/'mtp2-edge-closure-note.pdf').read_bytes()==(S/'published-source/output/pdf/mtp2_edge_closure.pdf').read_bytes(),'One byte-identical embedded reader')
need(prom['publication_sha256']==bind(D/'publication.json')['sha256'],'Promotion config binding')
need((O/'ORIGINAL_ABSTRACT.tex').read_text()==abstract_tex,'Exact original abstract copy')
if (O/'MANIFEST.json').exists():
    manifest=load(O/'MANIFEST.json')
    for name,spec in manifest['owned_bindings'].items():need(bind(O/name)==spec,'Sealed editorial file changed: '+name)
    for path,spec in manifest['config_bindings'].items():need(bind(Path(path))==spec,'Sealed config changed')
    need(bind(O/'MANIFEST.json')==load(O/'SEAL.json')['manifest_binding'],'Editorial manifest seal')
    current={str(x.relative_to(O)) for x in O.rglob('*') if x.is_file()}
    need(current==set(manifest['owned_bindings'])|{'MANIFEST.json','SEAL.json'},'Unexpected or missing editorial file')
print(json.dumps(dict(status='PASS_READ_ONLY_PRIVATE_EDITORIAL_CONSISTENCY',pristine=True,
    original_bindings=len(before),protected_prior_manifest_seals=len(protected),whole_raw_object_copies=len(original_map),
    original_archive_payload_comparisons=13,negative_controls=controls,
    source_program_or_math_control_reruns=False,rendered_or_live_or_native_gates_passed=False,
    writes=False,sealed=(O/'SEAL.json').exists()),indent=2))
