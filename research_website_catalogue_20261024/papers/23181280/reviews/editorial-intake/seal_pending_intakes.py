from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,zipfile,copy
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');now=lambda:datetime.now(timezone.utc).isoformat();h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(a,n,o):(a/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
prior=json.loads((P/'papers/23442760/reviews/analytic/custody.json').read_text())['protected_prior_owned_bindings']
for name,b in prior.items():assert h(name)==b['sha256'],name
for rid in ['23181280','23442760']:
 p=P/'papers'/rid;a=p/'reviews/editorial-intake';base=json.loads((a/'PRESERVATION_BASELINE.json').read_text());bindings=base['original_source_complete_review_and_root_initial_bindings'];checks=[]
 def check(n,c):assert c,n;checks.append({'name':n,'passed':True})
 for name,b in bindings.items():check('original-preserved:'+name,h(name)==b['sha256'])
 copies=json.loads((a/'ORIGINAL_OBJECT_COPIES.json').read_text())['copies']
 for b in copies:check('verbatim-copy:'+b['copy_path'],(a/b['copy_path']).read_bytes()==Path(b['source_path']).read_bytes())
 m=json.loads((a/'METADATA_READER_SUPPORT_REQUIREMENTS.json').read_text());secs=json.loads((a/'PUBLIC_SECTIONS_DRAFT.json').read_text());status=json.loads((a/'INTAKE_STATUS.json').read_text());draft=(a/'PUBLIC_COPY_DRAFT.md').read_text()
 tex=Path(next(k for k in bindings if k.endswith('/source_preparation/root_dependent_spanning_trees.tex') if rid=='23181280') if rid=='23181280' else p/'sources/published-source/manuscript/main.tex').read_text()
 original=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0];visible=re.sub(r'\s+',' ',original).strip().replace('~',' ')
 if rid=='23442760':visible=visible.replace('\\R','\\mathbb R')
 check('exact-source-abstract-substring',(a/'ORIGINAL_ABSTRACT.tex').read_text()==original)
 check('complete-visible-abstract',secs['original_abstract_one_paragraph']==visible and '\n' not in visible and visible in draft)
 check('explicit-Original-abstract-label','## Original abstract\n\n'+visible in draft)
 check('canonical-AA-followup-null',all(m[k] is None and status[k] is None for k in ['canonical','AA','followup']))
 check('all-new-publication-gates-false',all(v is False for v in m['gates'].values()))
 check('no-site-configs',(not(p/'publication.json').exists()) and not(p/'promotion.json').exists())
 check('all-three-whole-original-verdicts',sum('/reviews/' in b['copy_path'] for b in copies)==3)
 for sec in secs['sections']:
  for paragraph in sec['paragraphs']:check('complete-public-paragraph:'+paragraph[:50],paragraph in draft)
 check('actual-ORCID','0009-0001-9320-500X' in draft and m['creators_original'][0]['orcid']=='0009-0001-9320-500X')
 check('actual-date-and-version',m['declared_publication_date'] in (a/'CITATION_DRAFT.bib').read_text().replace('\n','') or ('version = {1.0}' in (a/'CITATION_DRAFT.bib').read_text() and m['version']=='1.0'))
 check('sole-author-citation','author = {Kriebel, Alec}' in (a/'CITATION_DRAFT.bib').read_text())
 check('selected-record-citation',m['DOI'] in (a/'CITATION_DRAFT.bib').read_text())
 check('CC-BY-status','CC BY 4.0' in draft and 'Unrefereed preprint' in draft)
 check('public-no-private-hashes-or-review-timeline',not re.search(r'\b[0-9a-f]{64}\b|2026-10-25|root PASS|checks per run|SHA256|replay receipt',draft,re.I))
 marker94=['one spanning tree','every vertex root','binary','\\{0,1,2\\}','\\{1,2,3\\}','strong NP-completeness','Problem 2','unrestricted optimum','mutual agreement']
 marker95=['nonempty interior','every integer $r\\ge1$','global square','Lebesgue','C_n=4(n+2)^2','C^2','1/[4(r+1)^2]','Totik–Varga','older endpoint-polynomial','constant objectives','arbitrary reference measures','mutual agreement']
 markers=marker94 if rid=='23181280' else marker95
 for x in markers:check('scope-credit-marker:'+x,x in draft)
 for b in m['assets']:
  f=Path(b['source_path']);check('full-asset:'+f.name,h(f)==b['sha256'] and f.stat().st_size==b['bytes'] and hashlib.md5(f.read_bytes()).hexdigest()==b['md5'])
  check('actual-file-object:'+f.name,b['actual_file_object']['size']==b['bytes'] and b['actual_file_object']['links']['self']==b['actual_original_URL'])
 zasset=next(b for b in m['assets'] if b['source_path'].endswith('.zip'));members=[];pdfs=[]
 with zipfile.ZipFile(zasset['source_path']) as z:
  for info in z.infolist():
   if info.is_dir():continue
   data=z.read(info);f=p/'sources/published-source'/info.filename
   check('archive-member:'+info.filename,f.read_bytes()==data)
   members.append({'name':info.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
   if info.filename.lower().endswith('.pdf'):pdfs.append({'name':info.filename,'sha256':hashlib.sha256(data).hexdigest()})
 check('complete-member-count',len(members)==m['support_requirements']['regular_member_count'])
 check('reader-identity-not-another-edition',(len(pdfs)==1 and pdfs[0]['sha256']==m['assets'][0]['sha256']) if rid=='23181280' else len(pdfs)==0)
 # Explicit changed-read controls operate only on in-memory values, no fixture directories.
 negative=[]
 negative.append({'change':'remove complete original abstract','detected':visible not in draft.replace(visible,'')})
 for key in ['canonical','AA','followup']:
  changed=copy.deepcopy(m);changed[key]='premature';negative.append({'change':'set '+key,'detected':not all(changed[k] is None for k in ['canonical','AA','followup'])})
 changed=copy.deepcopy(m);changed['gates']['root_scientific_clearance_adopted']=True;negative.append({'change':'premature root gate','detected':not all(v is False for v in changed['gates'].values())})
 for marker in (['one spanning tree','binary','\\{1,2,3\\}'] if rid=='23181280' else ['every integer $r\\ge1$','C_n=4(n+2)^2','Lebesgue']):negative.append({'change':'drop scope marker '+marker,'detected':marker not in draft.replace(marker,'')})
 vb=next(b for b in copies if '/reviews/analytic/' in b['copy_path']);negative.append({'change':'replace original custom verdict by generic PASS','detected':json.loads((a/vb['copy_path']).read_text())!={'status':'PASS'}})
 rb=next(b for b in copies if b['copy_path'].endswith(('api-receipt.json','api-receipts.json')));receipt=json.loads((a/rb['copy_path']).read_text());changed=copy.deepcopy(receipt);changed[0]['http_status']=201;negative.append({'change':'alter original receipt HTTP fact','detected':changed!=receipt})
 negative.append({'change':'substitute concept DOI in citation','detected':m['DOI'] not in (a/'CITATION_DRAFT.bib').read_text().replace(m['DOI'],'10.5281/zenodo.'+m['concept_record_id'])})
 for x in negative:assert x['detected'],x
 dump(a,'ACCEPTANCE_CHECKS.json',{'utc':now(),'checks':checks,'changed_read_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'mathematical_recertification':False})
 dump(a,'ARCHIVE_READER_IDENTITY.json',{'members':members,'PDF_members':pdfs,'complete_original_ZIP_unchanged':True})
 reads=[]
 for fam in ['scope','analytic','adversarial']:
  for name in ['REPORT.md','VERDICT.json' if fam=='analytic' else 'verdict.json']:
   f=p/'reviews'/fam/name;reads.append({'path':str(f),'sha256':h(f),'extent':'entire complete final original; no replacement or generic verdict manufactured'})
 for f in [p/'sources'/('root_dependent_spanning_trees.pdf' if rid=='23181280' else 'Convex_Body_SOS_Density_Note_v1.0.pdf'),p/'sources'/('published-source/source_preparation/root_dependent_spanning_trees.tex' if rid=='23181280' else 'published-source/manuscript/main.tex'),p/'reviews/root/initial-reconstruction.md',p/'reviews/root/initial-reconstruction-seal.json']:
  reads.append({'path':str(f),'sha256':h(f),'extent':'entire actual manuscript/source or root initial snapshot; root final authority not read/adopted in this pending packet'})
 dump(a,'READ_LEDGER.json',{'utc':now(),'full_readings':reads,'full_source_API_record_and_receipt_objects_read':True,'latest_versions_and_all_technical_JSON_copied_and_machine_compared_in_full':True,'PUBLIC_COPY_DRAFT_entire_read_after_generation':True,'root_final_authority_arrival':'parent announced exact final authorities while pending packets were being finished; not read/adopted until these immutable pending intakes are sealed','primary_new_fetch_or_source_execution':False})
 dump(a,'custody.json',{'utc':now(),'baseline_originals':bindings,'all_baseline_originals_unchanged':True,'earlier_protected_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_mutable_core_site_input_maps_followed':False,'all_original_byte_copies_identical':True,'only_new_editorial_intake_namespaces_written':True,'source_config_shared_site_native_browser_git_deploy_redirect_release_outreach_mutations':False})
 with (a/'RESEARCH_LOG.md').open('a') as f:
  f.write(now()+' — Full original abstracts/scopes, exact metadata, all raw-object copies and source-consumer requirements prepared; full public drafts read. Completion estimate85%.\n')
  f.write(now()+' — Parent announced separate final root authorities; this pending intake intentionally seals first without adopting them. All original bindings/member identities/meaningful editorial controls pass. Pending-intake completion100%; final editorial authority remains a separate later package.\n')
 exclude={'MANIFEST.json','SEAL.json'}
 owned={str(f.relative_to(a)):{'bytes':f.stat().st_size,'sha256':h(f)} for f in sorted(a.rglob('*')) if f.is_file() and f.name not in exclude}
 dump(a,'MANIFEST.json',{'utc':now(),'status':'IMMUTABLE_PRIVATE_EDITORIAL_INTAKE_PENDING_ROOT_AUTHORITY_ADOPTION','owned_output_bindings':owned,'baseline_originals_unchanged':True,'complete_original_object_copies':len(copies),'all_publication_gates_false':True,'canonical':None,'AA':None,'followup':None,'excluded_self_and_seal':sorted(exclude)})
 dump(a,'SEAL.json',{'utc':now(),'status':'COMPLETE_PRIVATE_PENDING_INTAKE_IMMUTABLE','record_id':int(rid),'manifest_sha256':h(a/'MANIFEST.json'),'report_sha256':h(a/'REPORT.md'),'public_copy_sha256':h(a/'PUBLIC_COPY_DRAFT.md'),'new_configs_created':False,'root_final_authority_adopted':False,'completion_percent':100})
 print(json.dumps({'record':rid,'seal_sha256':h(a/'SEAL.json'),'owned':len(owned),'checks':len(checks),'negative_controls':len(negative),'baseline':len(bindings),'earlier_protected':len(prior)}))
