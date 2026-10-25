"""Source-bound editorial consistency and mutated-object controls; no rendering."""
from pathlib import Path
from copy import deepcopy
from io import BytesIO
from datetime import datetime,timezone
import hashlib,json,re,stat,zipfile
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23333353';a=p/'reviews/editorial'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(name,x):(a/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());rootfile=P/g['root_clearance_file'];root=json.loads(rootfile.read_text());ready=json.loads((p/'sources/SOURCE_READY.json').read_text());api=json.loads((p/'sources/record.raw.json').read_text());meta=json.loads((p/'sources/normalized-metadata.json').read_text());transport=json.loads((p/'sources/api-receipts.json').read_text());public=(a/'PUBLIC_COPY.md').read_text();sections=json.loads((a/'public-sections.json').read_text())
checks=[]
def check(name,ok):
    if not ok:raise ValueError(name)
    checks.append({'name':name,'passed':True})
rootsha='9a277414cd2b4891af98abac570cc21eab2c9e35eb89d876ea7bc2d106bb7f8c'
check('exact_completed_root_authority',sha(rootfile)==g['root_clearance_sha256']==rootsha)
baseline=json.loads((a/'ORIGINAL_BINDINGS_BEFORE.json').read_text())['originals']
for path,item in baseline.items():check('original_preserved:'+path,Path(path).stat().st_size==item['bytes'] and sha(path)==item['sha256'])
custody=json.loads((P/root['root_custody_receipt']).read_text());check('complete_root_custody129',len(custody['bindings'])==custody['unique_bindings']==129)
for rel,item in custody['bindings'].items():check('root_final_binding:'+rel,(P/rel).stat().st_size==item['bytes'] and sha(P/rel)==item['sha256'])
prior=json.loads((P/'papers/23395703/reviews/editorial/custody.json').read_text())['earlier_owned_bindings']
d=P/'papers/23395703/reviews/editorial';m=json.loads((d/'MANIFEST.json').read_text())
for rel,item in m['owned_output_bindings'].items():prior[str(P/'papers/23395703'/rel)]=item
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
markers=[
 'countable unital free product','entire original B*C joint law','all exchangeable states','universal unital free product and continuous states',
 'distinct proper unital *-subalgebras with scalar intersection','Every possible downstairs exchangeable witness','every 0<t<1','At t=0 or 1 it is a character','faithful downstairs fair state',
 'no positive unital extension','different from the forbidden zero-evaluation character','equivariant unital C* inclusion','group of finitely supported permutations of ℕ','canonical map between universal unital free products of a C* inclusion is injective',
 'A third copy index','every nonempty finite generator word','null space is a left ideal','not promoted to equality of operators','weak-* cluster subnet','nonempty compact face','cyclic GNS dilations','Krein–Milman',
 'A two-copy invariant extreme witness','fixed-full-marginal convex slice','mixture is extreme in that slice','Faithful-only, tracial-only, trivial-tail','normal W*','tensor-quotient','other five workshop questions','established prior work of Dykema, Köstler and Williams','Historical first priority, independent discovery and current worldwide open status are not asserted'
]
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
    need(pub['publication_date']==api['metadata']['publication_date']=='2026-10-12','declared_date')
    need(pub['source_binding']['record_created_utc']==api['created']=='2026-10-13T05:53:41.831316+00:00','separate_creation')
    need(pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','author_ORCID')
    need(all(pub[k] is prom[k] is None for k in ['AA','canonical_url','follow_up']),'null_gate_fields')
    need(all(prom[k] is False and pub['review_metadata'][k] is False for k in gatenames),'all_false_gates')
    need(prom['root_clearance_record']==root and prom['approved_scope']==root['approved_scope'],'whole_exact_root')
    need(prom['source_receipt_original']==pub['source_binding']['source_receipt_original']==ready,'whole_original_receipt')
    need(prom['transport_receipt_original']==pub['source_binding']['transport_receipt_original']==transport,'whole_original_transport')
    need(prom['all_actual_assets']==pub['source_binding']['all_actual_assets']==ready['all_actual_assets'],'all_original_actual_assets')
    for role,item in prom['reviews'].items():need(item['verdict']==json.loads((P/root['reviews'][role]['verdict']).read_text()) and item['root_authority_entry']==root['reviews'][role],'whole_custom_verdict:'+role)
    need(set(prom['reviews'])=={'scope','analytic','adversarial'},'all_original_family_roles')
    need(pub['source_binding']['pdf_sha256']==root['pdf_sha256'] and pub['source_binding']['supplement_sha256']==root['supplement_sha256'],'unchanged_source_hashes')
    need(pub['pdf_pages']==3 and pub['source_binding']['published_asset_count']==2 and pub['additional_assets']==[],'one_complete_reader')
    need('used extensively'in pub['ai_disclosure'] and 'unrefereed'in pub['ai_disclosure'] and 'human peer review'in pub['ai_disclosure'] and 'formal proof-assistant certification'in pub['ai_disclosure'],'AI_unrefereed_boundaries')
    need([pub['status'],pub['ai_disclosure']]==[sections['status'],sections['ai_disclosure']],'complete_exact_status_paragraphs')
    need('actual research contributions'in pub['collaboration'] and 'mutual agreement'in pub['collaboration'],'passive_actual_contributions')
candidate(c,g);check('complete_candidate_contract',True)
check('whole_original_abstract_source_substring',original==(a/'ORIGINAL_ABSTRACT.tex').read_text()==c['source_binding']['abstract_tex'])
check('full_abstract_one_indexable_paragraph','\n'not in c['abstract'] and '## Original abstract\n\n'+abstract in public)
check('original_normalized_metadata_shape',meta['metadata']==api['metadata'] and meta['all_actual_file_objects']==api['files'] and meta['all_verified_assets']==ready['all_actual_assets'])
check('original_receipt_schema_no_alias','all_actual_assets'in ready and not any(key in ready for key in ['files','assets','actual_assets','exact_assets']))
check('lowercase_original_asset_checksums',all('md5'in x and 'sha256'in x and 'MD5'not in x and 'SHA256'not in x and 'api_file_object'in x for x in ready['all_actual_assets']))
check('five_original_transport_entries',len(transport)==5 and all('status'in x and 'headers'in x and 'requested_url'in x and 'sha256'in x and 'api_file_object'not in x for x in transport))
for role,item in g['reviews'].items():check('complete_report_custom_object_binding:'+role,sha(p/item['report'])==item['report_sha256']==root['reviews'][role]['report_sha256'] and sha(p/item['verdict_file'])==item['verdict_sha256']==root['reviews'][role]['verdict_sha256'])
check('publication_promotion_byte_binding',sha(p/'publication.json')==g['publication_sha256']==sections['publication_config_sha256'])
for key in ['plain_language','result','why_it_works','limitations']:
    check('section_exact:'+key,sections[key]==c[key])
    for paragraph in c[key]:check('public_full_paragraph:'+paragraph[:55],paragraph in public)
for key in ['status','ai_disclosure','collaboration']:check('public_complete_'+key,c[key] in public and sections[key]==c[key])
for b in c['background']:check('substantive_prior_reference:'+b['title'],all(b[k] in public for k in ['title','url','note']))
check('public_no_private_audit_story',re.search(r'\b[0-9a-f]{64}\b|2026-10-25|SHA256|replay receipt|checks passed|root authority|root PASS|native gate|reviewer control',public,re.I) is None)
check('no_source_receipt_record_aliases_created',not(p/'sources/receipt.json').exists() and not(p/'sources/record.json').exists())
bib=(a/'CITATION.bib').read_text();check('complete_prepared_citation',bib==c['prepared_bibtex'] and sha(a/'CITATION.bib')==c['source_binding']['prepared_bibtex_sha256'] and all(x in bib for x in [c['doi'],c['title'],'author = {Kriebel, Alec}','version = {1.0}','date = {2026-10-12}','0009-0001-9320-500X']))
archive=[]
for obj in api['files']:
    path=p/'sources'/obj['key'];data=path.read_bytes();item=next(x for x in ready['all_actual_assets'] if x['api_file_object']==obj)
    check('actual_API_full_asset:'+obj['key'],len(data)==obj['size']==item['bytes'] and sha(path)==item['sha256'] and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum']=='md5:'+item['md5'])
    check('actual_original_link:'+obj['key'],any(x['url']==obj['links']['self'] for x in c['related_resources']))
    if path.suffix=='.pdf':check('three_complete_actual_PDF_pages',len(PdfReader(BytesIO(data)).pages)==3)
    else:
        with zipfile.ZipFile(BytesIO(data)) as z:
            members=[x for x in z.infolist() if not x.is_dir()];check('safe_unique_complete60_members',len(members)==60 and len({x.filename for x in members})==60 and z.testzip() is None and all(not x.filename.startswith('/') and '..'not in Path(x.filename).parts and not stat.S_ISLNK(x.external_attr>>16) for x in members))
            check('no_embedded_reader_or_nested_archive',not any(x.filename.lower().endswith(('.pdf','.zip','.tar','.gz')) for x in members))
            for entry in members:
                member=z.read(entry);check('complete_ZIP_member:'+entry.filename,(p/'sources/published-source'/entry.filename).read_bytes()==member);archive.append({'member':entry.filename,'bytes':len(member),'sha256':hashlib.sha256(member).hexdigest()})
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
reject('conflate_creation_and_declared_date',lambda pub,prom:pub.update(publication_date='2026-10-13'))
reject('replace_custom_scope_with_generic_PASS',lambda pub,prom:prom['reviews']['scope'].update(verdict={'status':'PASS'}))
reject('truncate_root_object',lambda pub,prom:prom.update(root_clearance_record={'status':'PASS'}))
reject('invent_receipt_files_alias',lambda pub,prom:pub['source_binding']['source_receipt_original'].update(files=[]))
reject('drop_original_ZIP_asset',lambda pub,prom:prom.update(all_actual_assets=prom['all_actual_assets'][:1]))
reject('invent_transport_status',lambda pub,prom:prom['transport_receipt_original'][0].update(status=201))
reject('alter_reader_binding',lambda pub,prom:pub['source_binding'].update(pdf_sha256='0'*64))
reject('wrong_page_count',lambda pub,prom:pub.update(pdf_pages=2))
for name in ['AA','canonical_url','follow_up']:reject('set_'+name,lambda pub,prom,name=name:pub.update({name:'premature'}))
for name in gatenames:reject('promote_'+name,lambda pub,prom,name=name:prom.update({name:True}))
check('no_fake_pending_intake',json.loads((a/'INTAKE_RECORD.json').read_text())['status']=='ROOT_SCIENCE_CLEARED_BEFORE_EDITORIAL_INTAKE')
dump('ACCEPTANCE_CHECKS.json',{'utc':datetime.now(timezone.utc).isoformat(),'positive_checks':checks,'changed_object_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'shared_or_render_compatibility_claimed':False})
dump('custody.json',{'utc':datetime.now(timezone.utc).isoformat(),'original_bindings':baseline,'all_originals_unchanged':True,'root_final_129_bindings_reverified':True,'earlier_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_mutable_site_core_input_maps_followed':False,'archive_member_comparisons':archive,'all_actual_API_assets':api['files'],'whole_original_objects_and_separate_current_root_retained':True,'new_configs_and_editorial_only':True})
print(json.dumps({'status':'PASS_EDITORIAL_CONSISTENCY','positive_checks':len(checks),'negative_controls':len(negative),'original_inputs':len(baseline),'earlier_owned':len(prior),'root_final_bindings':129,'archive_members':60},indent=2))
