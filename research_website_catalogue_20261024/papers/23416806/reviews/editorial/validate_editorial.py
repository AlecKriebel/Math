"""Source-bound editorial consistency and mutated-object controls; no rendering."""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
from datetime import datetime,timezone
import hashlib,json,re,stat,zipfile
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23416806';a=p/'reviews/editorial'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(name,x):(a/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());rootfile=P/g['root_clearance_file'];root=json.loads(rootfile.read_text());ready=json.loads((p/'sources/SOURCE_READY.json').read_text());api=json.loads((p/'sources/record.raw.json').read_text());meta=json.loads((p/'sources/normalized-metadata.json').read_text());transport=json.loads((p/'sources/api-receipts.json').read_text());public=(a/'PUBLIC_COPY.md').read_text();sections=json.loads((a/'public-sections.json').read_text())
checks=[]
def check(name,ok):
    if not ok:raise ValueError(name)
    checks.append({'name':name,'passed':True})
rootsha='2fb0c7b2d3402e58c75aba0493699f76e0b9f3b4770b6a2a3c2a489375dc1489'
check('exact_completed_root_authority',sha(rootfile)==g['root_clearance_sha256']==rootsha)
baseline=json.loads((a/'ORIGINAL_BINDINGS_BEFORE.json').read_text())['originals']
for path,item in baseline.items():check('original_preserved:'+path,Path(path).stat().st_size==item['bytes'] and sha(path)==item['sha256'])
custody=json.loads((P/root['root_custody_receipt']).read_text());check('complete_root_custody262',len(custody['bindings'])==custody['unique_bindings']==262)
for rel,item in custody['bindings'].items():check('root_final_binding:'+rel,(P/rel).stat().st_size==item['bytes'] and sha(P/rel)==item['sha256'])
prior=json.loads((P/'papers/23333353/reviews/editorial/custody.json').read_text())['earlier_owned_bindings']
d=P/'papers/23333353/reviews/editorial';m=json.loads((d/'MANIFEST.json').read_text())
for rel,item in m['owned_output_bindings'].items():prior[str(P/'papers/23333353'/rel)]=item
for name in ['MANIFEST.json','SEAL.json','SEAL.sha256']:
    f=d/name;prior[str(f)]={'bytes':f.stat().st_size,'sha256':sha(f)}
audit=P/'verification/cylinder-discotope-code-audit-sol-20261025';am=json.loads((audit/'FINAL_MANIFEST.json').read_text())
for item in am['files']:prior[str(audit/item['path'])]={'bytes':item['bytes'],'sha256':item['SHA256']}
for name in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
    f=audit/name;prior[str(f)]={'bytes':f.stat().st_size,'sha256':sha(f)}
stage_before=json.loads((audit/'STAGE_BEFORE.json').read_text())['bindings']
for path,item in stage_before.items():prior[path]=item
for path,item in prior.items():check('prior_owned_preserved:'+path,Path(path).stat().st_size==item['bytes'] and sha(path)==item['sha256'])
original=(p/c['source_binding']['source_tex_path']).read_text().split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
abstract=' '.join(original.split())
for old,new in c['source_binding']['abstract_normalization']['exact_presentational_replacements'].items():abstract=abstract.replace(old,new)
markers=['nonempty two-sided irreducible sofic shift', 'specified onto block code', 'any total completion', 'including ε', 'regular two-sided bad-word ideal', 'Choose any finite monoid M', 'N=max{2,ℓ,4(|M|+1)}', '(1) f extends to a block map G:S→T', '(2) a locally testable language C contains L and avoids B', '(3) Lang(T[N])∩B=∅', '(4) F(T[N])=T', 'Containment S⊇T is non-strict', 'no other local-rule completion, extension radius or containing finite alphabet', 'Place–van Rooijen–Zeitoun, Theorem 4.2 (2014)', 'without multiplicities', 'does not reprove its general algebraic separation argument', 'every vertex initial and final', 'including ε and short words', 'all-path accepting-state reachability', 'no empirical word-length cutoff', 'agree on sufficiently high T[n]', 'all allowed k-factors', 'length at least 2k', 'profile sets used for LT from profile multiplicities', 'Onto is used only', 'only if T is of finite type', 'odd m and m+2>n', 'Periodic irreducible targets', 'Problem 16.2', "Dykstra's broader reducible-sofic homomorphism problem", 'No practical complexity improvement or implemented arbitrary-input solver', 'Ballier uses canonical-approximation normalization', 'Dykstra and Barth–Dykstra', 'Historical first priority, originality, independent discovery and current worldwide open status are not certified', 'unread final Barth–Dykstra and Ballier journal bodies']
gatenames=['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']
def candidate(pub,prom):
    def need(value,tag):
        if not value:raise ValueError(tag)
    body='\n'.join(pub['result']+pub['why_it_works']+pub['limitations'])
    for marker in markers:need(marker in body,'scope_or_credit:'+marker)
    need(pub['abstract']==abstract and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True,'whole_original_abstract')
    need(pub['title']==api['metadata']['title'] and pub['doi']==api['metadata']['doi'],'exact_title_selected_DOI')
    need(pub['version']==prom['version']==api['metadata']['version']=='1.0','exact_version')
    need(pub['edition_label']==pub['citation_edition_label']=='Version 1.0','exact_visible_edition_labels')
    need(pub['publication_date']==api['metadata']['publication_date']=='2026-10-16','declared_date')
    need(pub['source_binding']['record_created_utc']==api['created']=='2026-10-16T11:30:08.825717+00:00','separate_creation')
    need(pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','author_ORCID')
    need(all(pub[k] is prom[k] is None for k in ['AA','canonical_url','follow_up']),'null_gate_fields')
    need(all(prom[k] is False and pub['review_metadata'][k] is False for k in gatenames),'all_false_gates')
    need(prom['root_clearance_record']==root and prom['approved_scope']==root['approved_scope'],'whole_exact_root')
    need(prom['source_receipt_original']==pub['source_binding']['source_receipt_original']==ready,'whole_original_receipt')
    need(prom['transport_receipt_original']==pub['source_binding']['transport_receipt_original']==transport,'whole_original_transport')
    need(prom['all_assets']==pub['source_binding']['all_assets']==ready['all_assets'],'all_original_actual_assets')
    for role,item in prom['reviews'].items():need(item['verdict']==json.loads((P/root['reviews'][role]['verdict']).read_text()) and item['root_authority_entry']==root['reviews'][role],'whole_custom_verdict:'+role)
    need(set(prom['reviews'])=={'scope','analytic','adversarial'},'all_original_family_roles')
    need(pub['source_binding']['pdf_sha256']==root['pdf_sha256'] and pub['source_binding']['supplement_sha256']==root['supplement_sha256'],'unchanged_source_hashes')
    need(pub['pdf_pages']==4 and pub['source_binding']['published_asset_count']==2 and pub['additional_assets']==[] and pub['source_binding']['archive_outer_regular_file_count']==150 and pub['source_binding']['archive_regular_member_occurrences']==186 and pub['source_binding']['archive_container_count']==4 and pub['source_binding']['nested_archive_count']==3,'one_complete_reader')
    need('used extensively'in pub['ai_disclosure'] and 'unrefereed'in pub['ai_disclosure'] and 'human peer review'in pub['ai_disclosure'] and 'formal proof-assistant certification'in pub['ai_disclosure'],'AI_unrefereed_boundaries')
    need([pub['status'],pub['ai_disclosure']]==[sections['status'],sections['ai_disclosure']],'complete_exact_status_paragraphs')
    need('actual research contributions'in pub['collaboration'] and 'mutual agreement'in pub['collaboration'],'passive_actual_contributions')
candidate(c,g);check('complete_candidate_contract',True)
check('whole_original_abstract_source_substring',original==(a/'ORIGINAL_ABSTRACT.tex').read_text()==c['source_binding']['abstract_tex'])
check('full_abstract_one_indexable_paragraph','\n'not in c['abstract'] and '## Original abstract\n\n'+abstract in public)
check('original_normalized_metadata_shape',meta['metadata']==api['metadata'] and meta['all_original_API_file_objects']==api['files'] and meta['all_assets']==ready['all_assets'])
check('original_receipt_schema_no_alias','all_assets'in ready and not any(key in ready for key in ['files','assets','actual_assets','exact_assets','all_actual_assets']))
check('lowercase_original_asset_checksums',all('md5'in x and 'sha256'in x and 'MD5'not in x and 'SHA256'not in x and 'original_api_file_object'in x for x in ready['all_assets']))
check('exact_original_ZIP_then_PDF_order',[x['original_api_file_object']['key'] for x in ready['all_assets']]==['source-and-verification.zip','paper.pdf'])
check('five_original_transport_entries',len(transport)==5 and all('status'in x and 'headers'in x and 'requested_url'in x and 'sha256'in x and 'original_api_file_object'not in x for x in transport))
for role,item in g['reviews'].items():check('complete_report_custom_object_binding:'+role,sha(p/item['report'])==item['report_sha256']==root['reviews'][role]['report_sha256'] and sha(p/item['verdict_file'])==item['verdict_sha256']==root['reviews'][role]['verdict_sha256'])
check('publication_promotion_byte_binding',sha(p/'publication.json')==g['publication_sha256']==sections['publication_config_sha256'])
for key in ['plain_language','result','why_it_works','limitations']:
    check('section_exact:'+key,sections[key]==c[key])
    for paragraph in c[key]:check('public_full_paragraph:'+paragraph[:55],paragraph in public)
for key in ['status','ai_disclosure','collaboration']:check('public_complete_'+key,c[key] in public and sections[key]==c[key])
for b in c['background']:check('substantive_prior_reference:'+b['title'],all(b[k] in public for k in ['title','url','note']))
check('public_no_private_audit_story',re.search(r'\b[0-9a-f]{64}\b|2026-10-25|SHA256|replay receipt|checks passed|root authority|root PASS|native gate|reviewer control',public,re.I) is None)
check('no_source_receipt_record_aliases_created',not(p/'sources/receipt.json').exists() and not(p/'sources/record.json').exists())
bib=(a/'CITATION.bib').read_text();check('complete_prepared_citation',bib==c['prepared_bibtex'] and sha(a/'CITATION.bib')==c['source_binding']['prepared_bibtex_sha256'] and all(x in bib for x in [c['doi'],c['title'],'author = {Kriebel, Alec}','version = {1.0}','date = {2026-10-16}','0009-0001-9320-500X']))
archive=[]
for obj in api['files']:
    path=p/'sources'/obj['key'];data=path.read_bytes();item=next(x for x in ready['all_assets'] if x['original_api_file_object']==obj)
    check('actual_API_full_asset:'+obj['key'],len(data)==obj['size']==item['bytes'] and sha(path)==item['sha256'] and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum']=='md5:'+item['md5'])
    check('actual_original_link:'+obj['key'],any(x['url']==obj['links']['self'] for x in c['related_resources']))
    if path.suffix=='.pdf':check('four_complete_actual_PDF_pages',len(PdfReader(BytesIO(data)).pages)==4)
inv=json.loads((p/'sources/archive-members.json').read_text());containers={};outer='source-and-verification.zip';lookup={(x['container'],x['member']):x for x in inv['members']}
check('recursive_inventory_complete_shape',inv['container_count']==len(inv['archive_containers'])==4 and inv['safe_regular_members_all_depths']==len(lookup)==186 and inv['top_level_regular_members']==150 and inv['nested_archive_count']==3)
for entry in sorted(inv['archive_containers'],key=lambda x:x['depth']):
    name=entry['container']
    if name==outer:data=(p/'sources'/outer).read_bytes()
    else:
        parent,member=name.rsplit('::',1)
        with zipfile.ZipFile(BytesIO(containers[parent])) as z:data=z.read(member)
    check('exact_original_archive_container:'+name,len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'])
    containers[name]=data
    with zipfile.ZipFile(BytesIO(data)) as z:
        members=[x for x in z.infolist() if not x.is_dir()]
        check('safe_unique_container:'+name,len({x.filename for x in members})==len(members) and z.testzip() is None and all(not x.filename.startswith('/') and '..'not in Path(x.filename).parts and not stat.S_ISLNK(x.external_attr>>16) for x in members))
        if name==outer:check('150_outer_original_members',len(members)==150)
        for info in members:
            member=z.read(info);ref=lookup[(name,info.filename)];extracted=Path(ref['extracted_path'])
            check('recursive_original_member:'+name+'::'+info.filename,len(member)==ref['bytes']==info.file_size and hashlib.sha256(member).hexdigest()==ref['sha256'] and extracted.read_bytes()==member and format(info.CRC,'08x')==ref['CRC32'])
            archive.append({'container':name,'member':info.filename,'extracted_path':str(extracted),'bytes':len(member),'sha256':hashlib.sha256(member).hexdigest()})
check('all186_original_occurrences_exact',len(archive)==186 and sum(x['bytes'] for x in archive)==inv['expanded_bytes_all_depths']==815561)
check('no_embedded_reader_any_depth',not any(x['member'].lower().endswith('.pdf') for x in archive))
check('four_containers_three_original_nested_archives',len(containers)==4 and sum(x['member'].lower().endswith('.zip') for x in archive)==3)
for item in json.loads((a/'ORIGINAL_OBJECT_COPIES.json').read_text())['copies']:check('verbatim_original_object:'+item['copy'],(a/item['copy']).read_bytes()==Path(item['source']).read_bytes())
negative=[]
def reject(name,change):
    pub,prom=deepcopy(c),deepcopy(g);change(pub,prom)
    try:candidate(pub,prom)
    except ValueError as e:negative.append({'change':name,'rejected':True,'reason':str(e)})
    else:raise RuntimeError('accepted_mutated_candidate:'+name)
for marker in markers:
    def remove(pub,prom,marker=marker):
        for key in ['result','why_it_works','limitations']:pub[key]=[x.replace(marker,'REMOVED_SCOPE_CONTROL') for x in pub[key]]
    reject('omit_required_scope_or_credit:'+marker,remove)
reject('truncate_original_abstract',lambda pub,prom:pub.update(abstract=pub['abstract'].rsplit('.',2)[0]))
reject('concept_DOI_substitution',lambda pub,prom:pub.update(doi=api['conceptdoi']))
reject('invent_version9.9',lambda pub,prom:pub.update(version='9.9'))
reject('wrong_visible_edition_label',lambda pub,prom:pub.update(edition_label='Version 9.9'))
reject('wrong_visible_citation_edition_label',lambda pub,prom:pub.update(citation_edition_label='Version 9.9'))
reject('omit_full_status_paragraph',lambda pub,prom:pub.update(status=''))
reject('wrong_declared_date',lambda pub,prom:pub.update(publication_date='2026-10-17'))
reject('replace_custom_scope_with_generic_PASS',lambda pub,prom:prom['reviews']['scope'].update(verdict={'status':'PASS'}))
reject('truncate_root_object',lambda pub,prom:prom.update(root_clearance_record={'status':'PASS'}))
reject('invent_receipt_files_alias',lambda pub,prom:pub['source_binding']['source_receipt_original'].update(files=[]))
reject('drop_original_PDF_asset',lambda pub,prom:prom.update(all_assets=prom['all_assets'][:1]))
reject('reverse_actual_original_asset_order',lambda pub,prom:prom.update(all_assets=list(reversed(prom['all_assets']))))
def alias_object(pub,prom):
    x=pub['source_binding']['source_receipt_original']['all_assets'][0];x['api_file_object']=x.pop('original_api_file_object')
reject('replace_original_api_file_object_by_alias',alias_object)
reject('invent_transport_status',lambda pub,prom:prom['transport_receipt_original'][0].update(status=201))
reject('alter_reader_binding',lambda pub,prom:pub['source_binding'].update(pdf_sha256='0'*64))
reject('wrong_page_count',lambda pub,prom:pub.update(pdf_pages=2))
reject('drop_nested_occurrences',lambda pub,prom:pub['source_binding'].update(archive_regular_member_occurrences=150))
reject('change_archive_container_count',lambda pub,prom:pub['source_binding'].update(archive_container_count=1))
reject('lose_three_nested_ZIPs',lambda pub,prom:pub['source_binding'].update(nested_archive_count=0))
for name in ['AA','canonical_url','follow_up']:reject('set_'+name,lambda pub,prom,name=name:pub.update({name:'premature'}))
for name in gatenames:reject('promote_'+name,lambda pub,prom,name=name:prom.update({name:True}))
check('no_fake_pending_intake',json.loads((a/'INTAKE_RECORD.json').read_text())['status']=='ROOT_SCIENCE_CLEARED_BEFORE_EDITORIAL_INTAKE')
dump('ACCEPTANCE_CHECKS.json',{'utc':datetime.now(timezone.utc).isoformat(),'positive_checks':checks,'changed_object_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'shared_or_render_compatibility_claimed':False})
dump('custody.json',{'utc':datetime.now(timezone.utc).isoformat(),'original_bindings':baseline,'all_originals_unchanged':True,'root_final_262_bindings_reverified':True,'earlier_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_mutable_site_core_input_maps_followed':False,'archive_member_comparisons':archive,'all_actual_API_assets':api['files'],'whole_original_objects_and_separate_current_root_retained':True,'new_configs_and_editorial_only':True})
print(json.dumps({'status':'PASS_EDITORIAL_CONSISTENCY','positive_checks':len(checks),'negative_controls':len(negative),'original_inputs':len(baseline),'earlier_owned':len(prior),'root_final_bindings':262,'archive_member_occurrences':186},indent=2))
