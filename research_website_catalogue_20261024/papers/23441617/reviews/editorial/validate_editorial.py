"""Source-bound editorial consistency and mutated-object controls; no rendering."""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
from datetime import datetime,timezone
import hashlib,json,re,stat,zipfile
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23441617';a=p/'reviews/editorial'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(name,x):(a/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());rootfile=P/g['root_clearance_file'];root=json.loads(rootfile.read_text());ready=json.loads((p/'sources/SOURCE_READY.json').read_text());api=json.loads((p/'sources/record.raw.json').read_text());meta=json.loads((p/'sources/normalized-metadata.json').read_text());transport=json.loads((p/'sources/api-receipts.json').read_text());public=(a/'PUBLIC_COPY.md').read_text();sections=json.loads((a/'public-sections.json').read_text())
checks=[]
def check(name,ok):
    if not ok:raise ValueError(name)
    checks.append({'name':name,'passed':True})
rootsha='194f44d3896132a5421b2797e9fd2d887de1df552c11535e29f4565577a890f0'
check('exact_completed_root_authority',sha(rootfile)==g['root_clearance_sha256']==rootsha)
baseline=json.loads((a/'ORIGINAL_BINDINGS_BEFORE.json').read_text())['originals']
for path,item in baseline.items():check('original_preserved:'+path,Path(path).stat().st_size==item['bytes'] and sha(path)==item['sha256'])
custody=json.loads((P/root['root_custody_receipt']).read_text());check('complete_root_custody1884',len(custody['bindings'])==custody['unique_bindings']==1884)
for rel,item in custody['bindings'].items():check('root_final_binding:'+rel,(P/rel).stat().st_size==item['bytes'] and sha(P/rel)==item['sha256'])
prior=json.loads((P/'papers/23416806/reviews/editorial/custody.json').read_text())['earlier_owned_bindings']
d=P/'papers/23416806/reviews/editorial';m=json.loads((d/'MANIFEST.json').read_text())
for rel,item in m['owned_output_bindings'].items():prior[str(P/'papers/23416806'/rel)]=item
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
markers=['For every compact E⊂[0,1]', 'F=ℝ∖E', 'Mod₂Γ(E,S₂)>0 implies Mod₂Γ(E,F)=∞', 'whole plane', 'locally rectifiable on the open parameter interval', 'increasing limit on compact interior subcurves', 'Arclength counts multiplicity', 'isolated endpoints have zero arclength measure', 'Intermediate contacts with either plate or the real axis are allowed', 'actual pointwise nonnegative extended Borel', 'for every connector', 'inf ∅=∞', 'both families consistently use globally rectifiable connectors', 'No extremal density is required', 'Empty E has zero outer modulus', 'Positive-length compact sets without intervals', 'null compact sets of positive conformal capacity', 'pointwise domination everywhere, including infinite values on null sets', 'actual vertical trace 1_E', 'no capacity conclusion', 'without dividing by the frequency at zero', 'length(E)=0', 'does not imply zero conformal capacity', 'Fix each actual e∈E separately', 'liminf subsequence', 'not a claim of a full radial limit', 'first-exit initial cost tends to zero', 'Returns, retracing, winding', 'works at every endpoint', 'no capacity identity for the touching real complement is imported', '1982 Goldstein–Jackson', 'full 2019 Springer problem wording', 'Historical first priority, independent discovery and current worldwide open status remain undetermined', 'no new-mechanism claim', 'A. A. Gonchar', 'communicated by M. Vuorinen']
gatenames=['rendered_public_copy_approved','local_http_verified','live_http_verified','browser_verified','native_sheet_publication_verified','public_page_published']
def candidate(pub,prom):
    def need(value,tag):
        if not value:raise ValueError(tag)
    body='\n'.join(pub['result']+pub['why_it_works']+pub['limitations'])
    for marker in markers:need(marker in body,'scope_or_credit:'+marker)
    need(pub['abstract']==abstract and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True,'whole_original_abstract')
    need(pub['title']==api['metadata']['title'] and pub['doi']==api['metadata']['doi'],'exact_title_selected_DOI')
    need(pub['version']==prom['version']==api['metadata']['version']=='1.0','exact_version')
    need(pub['source_binding']['manuscript_version'] is None and pub['source_binding']['manuscript_version_printed'] is False,'unprinted_manuscript_version_distinct_from_API')
    need(pub['edition_label']==pub['citation_edition_label']=='Version 1.0','exact_visible_edition_labels')
    need(pub['publication_date']==api['metadata']['publication_date']=='2026-10-17','declared_date')
    need(pub['source_binding']['record_created_utc']==api['created']=='2026-10-17T20:15:34.082127+00:00','separate_creation')
    need(pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','author_ORCID')
    need(all(pub[k] is prom[k] is None for k in ['AA','canonical_url','follow_up']),'null_gate_fields')
    need(all(prom[k] is False and pub['review_metadata'][k] is False for k in gatenames),'all_false_gates')
    need(prom['root_clearance_record']==root and prom['approved_scope']==root['approved_scope'],'whole_exact_root')
    need(prom['status']==pub['review_metadata']['scientific_clearance_status']==root['status']=='PASS_WITH_NONCENTRAL_BIBLIOGRAPHIC_DEFECT','literal_noncentral_root_status')
    need(prom.get('noncentral_bibliographic_defect')==root['noncentral_bibliographic_defect'] and prom['source_repair'] is False,'whole_noncentral_defect_disposition')
    need(pub['background']==sections['background'],'complete_original_prepared_credit')
    need(any('Acta Math. 181 (1998), 1–61' in b['title'] and b['url']=='https://doi.org/10.1007/BF02392747' for b in pub['background']),'correct_public_HK181')
    need(prom['source_receipt_original']==pub['source_binding']['source_receipt_original']==ready,'whole_original_receipt')
    need(prom['transport_receipt_original']==pub['source_binding']['transport_receipt_original']==transport,'whole_original_transport')
    need(prom['all_assets']==pub['source_binding']['all_assets']==ready['all_assets'],'all_original_actual_assets')
    for role,item in prom['reviews'].items():need(item['verdict']==json.loads((P/root['reviews'][role]['verdict']).read_text()) and item['root_authority_entry']==root['reviews'][role],'whole_custom_verdict:'+role)
    need(set(prom['reviews'])=={'scope','analytic','adversarial'},'all_original_family_roles')
    need(pub['source_binding']['pdf_sha256']==root['pdf_sha256'] and pub['source_binding']['supplement_sha256']==root['supplement_sha256'],'unchanged_source_hashes')
    need(pub['pdf_pages']==7 and pub['source_binding']['published_asset_count']==2 and pub['additional_assets']==[] and pub['source_binding']['archive_outer_regular_file_count']==118 and pub['source_binding']['archive_regular_member_occurrences']==118 and pub['source_binding']['archive_container_count']==1 and pub['source_binding']['nested_archive_count']==0,'one_complete_reader')
    need('used extensively'in pub['ai_disclosure'] and 'unrefereed'in pub['ai_disclosure'] and 'human peer review'in pub['ai_disclosure'] and 'formal proof-assistant certification'in pub['ai_disclosure'],'AI_unrefereed_boundaries')
    need([pub['status'],pub['ai_disclosure']]==[sections['status'],sections['ai_disclosure']],'complete_exact_status_paragraphs')
    need('actual research contributions'in pub['collaboration'] and 'mutual agreement'in pub['collaboration'],'passive_actual_contributions')
candidate(c,g);check('complete_candidate_contract',True)
check('whole_original_abstract_source_substring',original==(a/'ORIGINAL_ABSTRACT.tex').read_text()==c['source_binding']['abstract_tex'])
check('full_abstract_one_indexable_paragraph','\n'not in c['abstract'] and '## Original abstract\n\n'+abstract in public)
check('original_normalized_metadata_shape',meta['metadata']==api['metadata'] and meta['all_original_API_file_objects']==api['files'] and meta['all_assets']==ready['all_assets'])
check('original_receipt_schema_no_alias','all_assets'in ready and not any(key in ready for key in ['files','assets','actual_assets','exact_assets','all_actual_assets']))
check('lowercase_original_asset_checksums',all('md5'in x and 'sha256'in x and 'MD5'not in x and 'SHA256'not in x and 'original_api_file_object'in x for x in ready['all_assets']))
check('exact_original_PDF_then_ZIP_order',[x['original_api_file_object']['key'] for x in ready['all_assets']]==['Real_Complement_Modulus_Note_v1.0.pdf','Real_Complement_Modulus_Verification_v1.0.zip'])
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
bib=(a/'CITATION.bib').read_text();check('complete_prepared_citation',bib==c['prepared_bibtex'] and sha(a/'CITATION.bib')==c['source_binding']['prepared_bibtex_sha256'] and all(x in bib for x in [c['doi'],c['title'],'author = {Kriebel, Alec}','version = {1.0}','date = {2026-10-17}','0009-0001-9320-500X']))
archive=[]
for obj in api['files']:
    path=p/'sources'/obj['key'];data=path.read_bytes();item=next(x for x in ready['all_assets'] if x['original_api_file_object']==obj)
    check('actual_API_full_asset:'+obj['key'],len(data)==obj['size']==item['bytes'] and sha(path)==item['sha256'] and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum']=='md5:'+item['md5'])
    check('actual_original_link:'+obj['key'],any(x['url']==obj['links']['self'] for x in c['related_resources']))
    if path.suffix=='.pdf':check('seven_complete_actual_PDF_pages',len(PdfReader(BytesIO(data)).pages)==7)
inv=json.loads((p/'sources/archive-members.json').read_text());outer='Real_Complement_Modulus_Verification_v1.0.zip';lookup={x['member']:x for x in inv['members']};data=(p/'sources'/outer).read_bytes()
check('original_single_container118_inventory',len(inv['archive_containers'])==1 and inv['safe_regular_members_all_depths']==inv['top_level_members']==len(lookup)==118 and inv['nested_archive_count']==0)
check('whole_original_archive_container',len(data)==inv['archive']['bytes'] and hashlib.sha256(data).hexdigest()==inv['archive']['sha256']==inv['archive_containers'][0]['sha256'])
with zipfile.ZipFile(BytesIO(data)) as z:
    members=[x for x in z.infolist() if not x.is_dir()]
    check('safe_unique118_members',len(members)==len({x.filename for x in members})==118 and z.testzip() is None and all(not x.filename.startswith('/') and '..'not in Path(x.filename).parts and not stat.S_ISLNK(x.external_attr>>16) for x in members))
    for info in members:
        member=z.read(info);ref=lookup[info.filename];extracted=Path(ref['extracted_path'])
        check('original_member:'+info.filename,ref['container']==outer and len(member)==ref['bytes']==info.file_size and hashlib.sha256(member).hexdigest()==ref['sha256'] and extracted.read_bytes()==member and format(info.CRC,'08x')==ref['CRC32'])
        archive.append({'container':outer,'member':info.filename,'extracted_path':str(extracted),'bytes':len(member),'sha256':hashlib.sha256(member).hexdigest()})
check('all118_occurrences_exact',len(archive)==118 and sum(x['bytes'] for x in archive)==inv['expanded_bytes_all_depths']==629704)
check('no_embedded_reader_or_nested_archive',not any(x['member'].lower().endswith(('.pdf','.zip','.tar','.gz')) for x in archive))
source=(p/c['source_binding']['source_tex_path']).read_text()
check('archived_HK180_preserved',r'Acta Math. \textbf{180} (1998), 1--61' in source and sha(p/'sources/Real_Complement_Modulus_Note_v1.0.pdf')==root['pdf_sha256'])
check('API_version_explicit_manuscript_version_not_printed',api['metadata']['version']=='1.0' and c['source_binding']['manuscript_version'] is None and c['source_binding']['manuscript_version_printed'] is False and re.search(r'version\s+1\.0',source,re.I) is None and re.search(r'version\s+1\.0',(a/'ACTUAL_MANUSCRIPT_READ.txt').read_text(),re.I) is None)
check('private_defect_record_exact',json.loads((a/'BIBLIOGRAPHIC_DISPOSITION.json').read_text())['root_original_disposition']==root['noncentral_bibliographic_defect'])
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
reject('invent_explicit_printed_manuscript_version',lambda pub,prom:pub['source_binding'].update(manuscript_version='1.0',manuscript_version_printed=True))
reject('wrong_visible_edition_label',lambda pub,prom:pub.update(edition_label='Version 9.9'))
reject('wrong_visible_citation_edition_label',lambda pub,prom:pub.update(citation_edition_label='Version 9.9'))
reject('omit_full_status_paragraph',lambda pub,prom:pub.update(status=''))
reject('wrong_declared_date',lambda pub,prom:pub.update(publication_date='2026-10-18'))
reject('replace_custom_scope_with_generic_PASS',lambda pub,prom:prom['reviews']['scope'].update(verdict={'status':'PASS'}))
reject('truncate_root_object',lambda pub,prom:prom.update(root_clearance_record={'status':'PASS'}))
reject('invent_receipt_files_alias',lambda pub,prom:pub['source_binding']['source_receipt_original'].update(files=[]))
reject('drop_original_ZIP_asset',lambda pub,prom:prom.update(all_assets=prom['all_assets'][:1]))
reject('reverse_actual_original_asset_order',lambda pub,prom:prom.update(all_assets=list(reversed(prom['all_assets']))))
def alias_object(pub,prom):
    x=pub['source_binding']['source_receipt_original']['all_assets'][0];x['api_file_object']=x.pop('original_api_file_object')
reject('replace_original_api_file_object_by_alias',alias_object)
reject('invent_transport_status',lambda pub,prom:prom['transport_receipt_original'][0].update(status=201))
reject('alter_reader_binding',lambda pub,prom:pub['source_binding'].update(pdf_sha256='0'*64))
reject('wrong_page_count',lambda pub,prom:pub.update(pdf_pages=2))
reject('truncate118_original_members',lambda pub,prom:pub['source_binding'].update(archive_regular_member_occurrences=117))
reject('invent_nested_archive',lambda pub,prom:pub['source_binding'].update(nested_archive_count=1))
reject('erase_noncentral_root_status',lambda pub,prom:prom.update(status='PASS'))
reject('erase_noncentral_bibliographic_object',lambda pub,prom:prom.pop('noncentral_bibliographic_defect'))
reject('rewrite_literal_original_ZIP_checksum_header',lambda pub,prom:prom['transport_receipt_original'][4]['headers'].update({'oc-checksum':'MD5:'+ready['all_assets'][1]['md5']}))
reject('return_public_HK_to180',lambda pub,prom:pub['background'][3].update(title=pub['background'][3]['title'].replace('181','180')))
for name in ['AA','canonical_url','follow_up']:reject('set_'+name,lambda pub,prom,name=name:pub.update({name:'premature'}))
for name in gatenames:reject('promote_'+name,lambda pub,prom,name=name:prom.update({name:True}))
check('no_fake_pending_intake',json.loads((a/'INTAKE_RECORD.json').read_text())['status']=='ROOT_SCIENCE_CLEARED_BEFORE_EDITORIAL_INTAKE')
dump('ACCEPTANCE_CHECKS.json',{'utc':datetime.now(timezone.utc).isoformat(),'positive_checks':checks,'changed_object_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'shared_or_render_compatibility_claimed':False})
dump('custody.json',{'utc':datetime.now(timezone.utc).isoformat(),'original_bindings':baseline,'all_originals_unchanged':True,'root_final_1884_bindings_reverified':True,'earlier_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_mutable_site_core_input_maps_followed':False,'archive_member_comparisons':archive,'all_actual_API_assets':api['files'],'whole_original_objects_and_separate_current_root_retained':True,'new_configs_and_editorial_only':True})
print(json.dumps({'status':'PASS_EDITORIAL_CONSISTENCY','positive_checks':len(checks),'negative_controls':len(negative),'original_inputs':len(baseline),'earlier_owned':len(prior),'root_final_bindings':1884,'archive_member_occurrences':118},indent=2))
