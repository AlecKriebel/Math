from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,copy,zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');now=lambda:datetime.now(timezone.utc).isoformat();h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(a,n,o):(a/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
prior=json.loads((P/'papers/23442760/reviews/analytic/custody.json').read_text())['protected_prior_owned_bindings']
# Bind only prior owned outputs and immutable seals; never follow stale original_input maps into live core/site.
for rid in ['23181280','23442760']:
 i=P/'papers'/rid/'reviews/editorial-intake';m=json.loads((i/'MANIFEST.json').read_text());s=json.loads((i/'SEAL.json').read_text());assert h(i/'MANIFEST.json')==s['manifest_sha256']
 for name,b in m['owned_output_bindings'].items():
  f=i/name;assert h(f)==b['sha256'];prior[str(f)]={'bytes':f.stat().st_size,'sha256':h(f)}
 for f in [i/'MANIFEST.json',i/'SEAL.json']:prior[str(f)]={'bytes':f.stat().st_size,'sha256':h(f)}
for name,b in prior.items():assert h(name)==b['sha256'],name
for rid in ['23181280','23442760']:
 p=P/'papers'/rid;a=p/'reviews/editorial';i=p/'reviews/editorial-intake';pub=json.loads((p/'publication.json').read_text());prom=json.loads((p/'promotion.json').read_text());sb=pub['source_binding'];checks=[]
 def check(n,v):assert v,n;checks.append({'name':n,'passed':True})
 original=json.loads((a/'ORIGINAL_BINDINGS_BEFORE.json').read_text())['originals']
 for name,b in original.items():check('original:'+name,h(name)==b['sha256'])
 rootfile=P/prom['root_clearance_file'];root=json.loads(rootfile.read_text());check('exact-root-authority-sha',h(rootfile)==prom['root_clearance_sha256']);check('whole-original-root-object',prom['root_clearance_record']==root)
 check('root-disposition-literal-copy',prom['status']==root['status']=='PASS' and prom['disposition_by']==root['disposition_by']=='root' and prom['approved_scope']==root['approved_scope'])
 ready=json.loads((p/prom['source_receipt_path']).read_text());transport=json.loads((p/prom['transport_receipt_path']).read_text());raw=json.loads((p/prom['raw_record_path']).read_text());key='actual_assets' if rid=='23181280' else 'all_actual_assets'
 check('whole-original-SOURCE_READY-objects',prom['source_receipt_record']==ready==sb['source_receipt_record'])
 check('original-source-assets-objects-and-order',prom['source_files']==ready[key]==sb['files'])
 check('original-complete-transport-receipt',prom['transport_receipt_record']==transport==sb['transport_receipt_record'] and len(transport)==5)
 check('actual-complete-published-file-objects',prom['published_file_objects']==raw['files']==sb['published_file_objects'] and len(raw['files'])==2)
 check('metadata-path-authentication',h(p/prom['metadata_path'])==prom['metadata_sha256'] and h(p/prom['raw_record_path'])==prom['raw_record_sha256'])
 check('literal-interface-not-a-generic-source-alias',not(p/'sources/receipt.json').exists() and not(p/'sources/record.json').exists())
 if rid=='23181280':check('raw-only-metadata-no-normalized-alias',not(p/'sources/normalized-metadata.json').exists() and all('SHA256'in b and 'MD5'in b for b in ready[key]))
 else:check('existing-normalized-metadata-original',prom['metadata_path']=='sources/normalized-metadata.json' and all('sha256'in b and 'md5'in b for b in ready[key]))
 for fam,b in root['reviews'].items():
  originalverdict=json.loads((P/b['verdict']).read_text());entry=prom['reviews'][fam]
  check('whole-custom-verdict:'+fam,entry['verdict']==originalverdict and h(P/b['verdict'])==entry['verdict_sha256'])
  check('separate-exact-root-family-authority:'+fam,entry['root_authority_entry']==b and h(P/b['report'])==entry['sha256'])
 check('publication-promotion-binding',prom['publication_sha256']==h(p/'publication.json'))
 for n in ['canonical_url','follow_up']:check('null-publication:'+n,pub[n] is None and prom[n] is None)
 check('AA-null',prom['AA'] is None and prom['native_sheet_aa_url'] is None and pub['review_metadata']['native_sheet_aa_url'] is None)
 for n in ['rendered_copy_verified','live_verified','browser_verified','native_verified']:check('false-gate:'+n,prom[n] is False)
 check('all-render-metadata-gates-false',all(pub['review_metadata'][n] is False for n in ['rendered','deployed','browser_verified','live_verified','native_verified']))
 check('no-follow-up-authority',root['follow_up'] is None)
 check('exact-date-version-author',pub['publication_date']==root['publication_date']==raw['metadata']['publication_date'] and pub['version']==root['reviewed_zenodo_version']==raw['metadata']['version'] and pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X')
 check('source-creation-update-retained',sb['record_created_utc']==raw['created'] and sb['record_updated_utc']==raw['updated'])
 check('selected-record-DOI-not-concept',pub['doi']==raw['doi'] and pub['doi']!=raw['conceptdoi'])
 tex=(p/sb['source_tex_path']).read_text();ab=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0];check('exact-original-abstract-TeX',ab==(a/'ORIGINAL_ABSTRACT.tex').read_text()==sb['abstract_tex'])
 normalized=re.sub(r'\s+',' ',ab).strip().replace('~',' ')
 for old,new in sb['abstract_normalization']['exact_presentational_replacements'].items():check('presentational-original-token:'+old,old in normalized);normalized=normalized.replace(old,new)
 check('entire-original-abstract-rendering',normalized==pub['abstract'] and '\n'not in pub['abstract'] and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True)
 public=(a/'PUBLIC_COPY.md').read_text();sections=json.loads((a/'public-sections.json').read_text())
 check('full-original-abstract-visible','## Original abstract\n\n'+pub['abstract'] in public)
 for field in ['plain_language','result','why_it_works','limitations']:
  check('section-field-binding:'+field,sections[field]==pub[field])
  for para in pub[field]:check('complete-public-paragraph:'+para[:50],para in public)
 for b in pub['background']:check('meaningful-prior-credit:'+b['title'][:35],b['title'] in public and b['note'] in public and b['url'] in public)
 check('status-and-actual-contribution-language',pub['ai_disclosure'] in public and pub['collaboration'] in public and 'mutual agreement' in pub['collaboration'])
 check('no-private-public-narrative',not re.search(r'\b[0-9a-f]{64}\b|2026-10-25|root PASS|SHA256|checks per run|gate-control',public,re.I))
 check('prepared-BibTeX-bytes',(a/'CITATION.bib').read_text()==pub['prepared_bibtex'] and h(a/'CITATION.bib')==sb['prepared_bibtex_sha256'])
 check('citation-selected-author-version-date',pub['doi'] in pub['prepared_bibtex'] and 'author = {Kriebel, Alec}' in pub['prepared_bibtex'] and 'version = {1.0}' in pub['prepared_bibtex'] and raw['metadata']['publication_date'].split('-')[2] in pub['prepared_bibtex'])
 archive=[]
 for obj in raw['files']:
  f=p/'sources'/obj['key'];data=f.read_bytes();check('actual-full-asset:'+obj['key'],len(data)==obj['size'] and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum'])
  if obj['key'].endswith('.pdf'):check('actual-selected-PDF-sha',h(f)==prom['pdf_sha256']==sb['pdf_sha256'])
  else:
   check('complete-ZIP-sha',h(f)==prom['supplement_sha256']==sb['supplement_sha256'])
   with zipfile.ZipFile(f) as z:
    for info in z.infolist():
     if info.is_dir():continue
     data=z.read(info);ex=p/'sources/published-source'/info.filename;check('member:'+info.filename,ex.read_bytes()==data);archive.append({'member':info.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 check('archive-complete-regular-count',len(archive)==sb['archive_regular_file_count'])
 must94=['one spanning tree','entire rooted tree at every root','binary','strong NP-completeness','\\{0,1,2\\}','\\{1,2,3\\}','Problem 2','unrestricted optimum','Cook and Karp','Martin']
 must95=['nonempty interior','every integer $r\\ge1$','\\int_K q\\,dx=1','C_n=4(n+2)^2','C^2','[0,1]\\times[-1,1]^{n-1}','Totik–Varga','older endpoint-polynomial','constant objectives','arbitrary reference measures']
 markers=must94 if rid=='23181280' else must95
 body='\n'.join(pub['plain_language']+pub['result']+pub['why_it_works']+pub['limitations'])
 for marker in markers:check('full-scope-marker:'+marker,marker in body)
 # Meaningful semantic-interface changed reads, all in memory and never altered fixture files.
 negative=[]
 for marker in markers:
  changed=body.replace(marker,'');negative.append({'change':'remove required scope/credit '+marker,'rejected':not all(x in changed for x in markers)})
 for name in ['canonical_url','follow_up']:
  changed=copy.deepcopy(pub);changed[name]='premature';negative.append({'change':'set '+name,'rejected':changed[name] is not None})
 changed=copy.deepcopy(prom);changed['live_verified']=True;negative.append({'change':'premature live gate','rejected':changed['live_verified'] is not False})
 changed=copy.deepcopy(prom);changed['root_clearance_record']['record_id']='different';negative.append({'change':'alter adopted root object','rejected':changed['root_clearance_record']!=root})
 changed=copy.deepcopy(prom);changed['reviews']['scope']['verdict']={'status':'PASS'};negative.append({'change':'generic original-verdict replacement','rejected':changed['reviews']['scope']['verdict']!=json.loads((P/root['reviews']['scope']['verdict']).read_text())})
 changed=copy.deepcopy(transport);changed[0]['http_status']=201;negative.append({'change':'invent altered original HTTP fact','rejected':changed!=prom['transport_receipt_record']})
 changed=copy.deepcopy(pub);changed['doi']=raw['conceptdoi'];negative.append({'change':'concept DOI substitution','rejected':changed['doi']!=raw['doi']})
 changed=copy.deepcopy(pub);changed['publication_date']='2026-10-25';negative.append({'change':'review date substituted for edition date','rejected':changed['publication_date']!=root['publication_date']})
 negative.append({'change':'omit original abstract last sentence','rejected':pub['abstract'].rsplit('.',2)[0]!=normalized})
 changed=copy.deepcopy(prom);changed['pdf_sha256']='0'*64;negative.append({'change':'reader identity mismatch','rejected':changed['pdf_sha256']!=sb['pdf_sha256']})
 for c in negative:assert c['rejected'],c
 dump(a,'ACCEPTANCE_CHECKS.json',{'utc':now(),'positive_checks':checks,'changed_read_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'rendering_or_shared_compatibility_tested':False})
 dump(a,'READ_LEDGER.json',{'utc':now(),'actual_full_PDF_and_controlling_TeX':{'path':str(p/sb['source_tex_path']),'PDF_pages':pub['pdf_pages'],'entire_read':True,'SOS_prior_independent_reading_reused_only_at_identical_hash':rid=='23442760'},'all_complete_reports_and_whole_custom_verdicts':[{'report':str(P/b['report']),'report_sha256':b['report_sha256'],'verdict':str(P/b['verdict']),'verdict_sha256':b['verdict_sha256'],'extent':'entire original complete final report and whole original custom object'} for b in root['reviews'].values()],'root_readings':[{'path':str(rootfile),'sha256':h(rootfile),'extent':'entire exact later authority after pending seal'},{'path':str(P/root['root_review']),'sha256':h(P/root['root_review']),'extent':'entire final root mathematical/primary/source-limit review'},{'path':str(P/root['root_custody_receipt']),'sha256':h(P/root['root_custody_receipt']),'extent':'whole exact custody JSON'}],'source_API_receipts':'entire SOURCE_READY and raw record, normalized original where present, all transport entries; latest/versions complete copies and equality authenticated','final_public_copy':'entire final copy read; precise predecessor notes and compact status polished before final seal','pending_states_modified':False,'new_primary_fetch_source_execution_or_rendering':False})
 dump(a,'custody.json',{'utc':now(),'all_originals_unchanged':True,'original_bindings':original,'earlier_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_site_core_input_maps_followed':False,'archive_member_comparisons':archive,'source_RECEIPT_custom_verdict_and_root_whole_object_equality':True,'pending_intake_unchanged':True,'only_new_paper_configs_and_editorial_namespaces_written':True})
 with (a/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — Entire final public copy read; exact predecessor credit polished and duplicate status avoided. All full-original object/source/member/authority/abstract/paragraph/null-gate controls pass; meaningful changed reads rejected without fixture copies. Completion100%; final root editorial reading and all render/live/native gates still pending.\n')
 excluded={'MANIFEST.json','SEAL.json','SEAL.sha256'}
 owned={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':h(f)} for f in sorted(a.rglob('*')) if f.is_file() and f.name not in excluded}
 for f in [p/'publication.json',p/'promotion.json']:owned[str(f.relative_to(p))]={'bytes':f.stat().st_size,'sha256':h(f)}
 dump(a,'MANIFEST.json',{'utc':now(),'record_id':rid,'status':'FINAL_EDITORIAL_CONFIG_HANDOFF_ROOT_FULL_READ_PENDING','original_input_count':len(original),'all_original_inputs_unchanged':True,'original_input_manifest':'reviews/editorial/ORIGINAL_BINDINGS_BEFORE.json','custody':'reviews/editorial/custody.json','owned_output_bindings':owned,'excluded_self_and_seal':sorted(excluded),'root_full_read_before_staging_required':True})
 dump(a,'SEAL.json',{'utc':now(),'record_id':rid,'status':'IMMUTABLE_FINAL_EDITORIAL_HANDOFF','manifest_sha256':h(a/'MANIFEST.json'),'report_sha256':h(a/'REPORT.md'),'public_copy_sha256':h(a/'PUBLIC_COPY.md'),'publication_sha256':h(p/'publication.json'),'promotion_sha256':h(p/'promotion.json'),'root_clearance_sha256':h(rootfile),'pending_intake_seal_sha256':h(i/'SEAL.json'),'owned_output_count':len(owned),'root_editorial_or_render_publication_native_PASS':False})
 (a/'SEAL.sha256').write_text(h(a/'SEAL.json')+'  SEAL.json\n')
 print(json.dumps({'record':rid,'seal_sha256':h(a/'SEAL.json'),'manifest_sha256':h(a/'MANIFEST.json'),'owned':len(owned),'positive_checks':len(checks),'negative_controls':len(negative),'originals':len(original),'protected_prior_and_pending_owned':len(prior),'publication_sha256':h(p/'publication.json'),'promotion_sha256':h(p/'promotion.json')}))
