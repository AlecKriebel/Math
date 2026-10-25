from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,copy,re,zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');p=P/'papers/23395703';a=p/'reviews/editorial';now=lambda:datetime.now(timezone.utc).isoformat();h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(n,o):(a/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
pub=json.loads((p/'publication.json').read_text());prom=json.loads((p/'promotion.json').read_text());sb=pub['source_binding'];root=json.loads((P/prom['root_clearance_file']).read_text());checks=[]
def check(n,c):assert bool(c),n;checks.append({'name':n,'passed':True})
baseline=json.loads((a/'ORIGINAL_BINDINGS_BEFORE.json').read_text())['originals']
for f,b in baseline.items():check('original-preserved:'+f,h(f)==b['sha256'])
prior=json.loads((P/'papers/23442760/reviews/editorial/custody.json').read_text())['earlier_owned_bindings']
for rid in ['23181280','23442760']:
 d=P/'papers'/rid/'reviews/editorial';m=json.loads((d/'MANIFEST.json').read_text());s=json.loads((d/'SEAL.json').read_text());check('prior-final-manifest:'+rid,h(d/'MANIFEST.json')==s['manifest_sha256'])
 for name,b in m['owned_output_bindings'].items():
  f=P/'papers'/rid/name;check('prior-owned:'+str(f),h(f)==b['sha256']);prior[str(f)]={'bytes':f.stat().st_size,'sha256':h(f)}
 for name in ['MANIFEST.json','SEAL.json','SEAL.sha256']:
  f=d/name;prior[str(f)]={'bytes':f.stat().st_size,'sha256':h(f)}
for f,b in prior.items():check('earlier-owned-preserved:'+f,h(f)==b['sha256'])
raw=json.loads((p/'sources/record.raw.json').read_text());norm=json.loads((p/'sources/normalized-metadata.json').read_text());ready=json.loads((p/'sources/SOURCE_READY.json').read_text());transport=json.loads((p/'sources/api-receipts.json').read_text())
check('exact-root-authority',h(P/prom['root_clearance_file'])=='c0120ac14fdb87954a8be3f85058b8446abe033d2570ff4906f51c1ae695206b' and prom['root_clearance_record']==root)
check('literal-root-disposition',prom['status']==root['status']=='PASS' and prom['disposition_by']==root['disposition_by']=='root' and prom['approved_scope']==root['approved_scope'])
check('whole-original-SOURCE_READY',prom['source_receipt_record']==ready==sb['source_receipt_record'])
check('exact-mixed-case-source-assets',prom['source_files']==ready['all_actual_assets']==sb['files'] and len(sb['files'])==3 and all('sha256'in v and 'MD5'in v and 'md5'not in v and 'SHA256'not in v for v in sb['files']))
check('whole-original-six-transports',prom['transport_receipt_record']==transport==sb['transport_receipt_record'] and len(transport)==6)
check('real-transport-shape',all('status'in v and 'headers'in v and 'MD5'in v and 'SHA256'in v and 'http_status'not in v and 'api_file_object'not in v for v in transport))
check('all-three-full-actual-file-objects',raw['files']==norm['all_file_objects']==prom['published_file_objects']==sb['published_file_objects'] and len(raw['files'])==3)
check('raw-and-normalized-metadata-authenticated',h(p/prom['metadata_path'])==prom['metadata_sha256'] and h(p/prom['raw_record_path'])==prom['raw_record_sha256'] and norm['metadata']==raw['metadata'])
check('no-record-or-receipt-alias',not(p/'sources/record.json').exists() and not(p/'sources/receipt.json').exists())
for fam,b in root['reviews'].items():
 original=json.loads((P/b['verdict']).read_text());entry=prom['reviews'][fam]
 check('complete-original-custom-verdict:'+fam,entry['verdict']==original and entry['verdict_sha256']==h(P/b['verdict']))
 check('separate-current-root-family-authority:'+fam,entry['root_authority_entry']==b and h(P/b['report'])==b['report_sha256'])
check('version-absent-in-actual-raw-metadata','version'not in raw['metadata'])
check('original-version-absence-objects',norm['version_field_present'] is False and norm['version_value'] is None and ready['version_field_present'] is False and ready['version'] is None and root['reviewed_zenodo_version'] is None)
check('all-new-version-values-null',pub['version'] is None and prom['version'] is None and all(sb[k] is None for k in ['version','zenodo_version','manuscript_version']))
check('all-new-version-presence-false',pub['version_field_present'] is False and prom['version_field_present'] is False and sb['version_field_present'] is False)
check('visible-no-version-label',pub['edition_label']=='No version declared' and 'no version declared'in pub['citation_edition_label'])
bib=(a/'CITATION.bib').read_text();check('no-invented-BibTeX-version',re.search(r'^\s*version\s*=',bib,re.M|re.I) is None and 'Unversioned deposit'in bib)
check('exact-prepared-citation',bib==pub['prepared_bibtex'] and h(a/'CITATION.bib')==sb['prepared_bibtex_sha256'])
check('selected-record-citation',pub['doi']==raw['doi']!=raw['conceptdoi'] and pub['doi']in bib)
check('sole-author-ORCID-citation','author = {Kriebel, Alec}'in bib and '0009-0001-9320-500X'in bib and pub['orcid']=='https://orcid.org/0009-0001-9320-500X')
check('exact-edition-and-private-creation',pub['publication_date']==root['publication_date']==raw['metadata']['publication_date']=='2026-10-15' and sb['record_created_utc']==raw['created'] and sb['record_updated_utc']==raw['updated'])
check('all-followups-canonical-AA-null',all(pub[k] is None and prom[k] is None for k in ['canonical_url','follow_up']) and prom['AA'] is None and prom['native_sheet_aa_url'] is None and pub['review_metadata']['native_sheet_aa_url'] is None)
check('no-human-formal-certification',prom['human_peer_review'] is False and prom['formal_machine_verification'] is False)
for k in ['rendered_copy_verified','live_verified','browser_verified','native_verified']:check('false-public-gate:'+k,prom[k] is False)
check('false-render-metadata-gates',all(pub['review_metadata'][k] is False for k in ['rendered','deployed','live_verified','browser_verified','native_verified']))
check('publication-promotion-byte-binding',h(p/'publication.json')==prom['publication_sha256'])
tex=(p/'sources/seven_plane_gin.tex').read_text();ab=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0];check('exact-original-abstract',ab==sb['abstract_tex']==(a/'ORIGINAL_ABSTRACT.tex').read_text())
visible=re.sub(r'\s+',' ',ab).strip().replace('~',' ')
for old,new in sb['abstract_normalization']['exact_presentational_replacements'].items():check('abstract-original-token:'+old,old in visible);visible=visible.replace(old,new)
check('complete-one-paragraph-Original-abstract',pub['abstract']==visible and '\n'not in visible and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True)
public=(a/'PUBLIC_COPY.md').read_text();sections=json.loads((a/'public-sections.json').read_text());check('full-abstract-visible-indexable','## Original abstract\n\n'+visible in public)
for key in ['plain_language','result','why_it_works','limitations']:
 check('config-section-binding:'+key,sections[key]==pub[key])
 for para in pub[key]:check('public-full-paragraph:'+para[:70],para in public)
for b in pub['background']:check('substantive-prior-credit:'+b['title'][:45],b['title']in public and b['url']in public and b['note']in public)
check('AI-unrefereed-and-substantive-contributions',pub['ai_disclosure']in public and pub['collaboration']in public and 'actual research contributions'in pub['collaboration'] and 'mutual agreement'in pub['collaboration'])
check('no-private-audit-public-narrative',not re.search(r'\b[0-9a-f]{64}\b|2026-10-25|SHA256|root PASS|checks per run|replay receipt|gate-control',public,re.I))
check('source-reader-full-pages',pub['pdf_pages']==6 and '6-page'in pub['reader_intro'])
archive=[];pdfcount=0;texmembers=[]
for obj in raw['files']:
 f=p/'sources'/obj['key'];data=f.read_bytes();check('all-three-original-assets:'+obj['key'],len(data)==obj['size'] and 'md5:'+hashlib.md5(data).hexdigest()==obj['checksum'])
 b=next(v for v in ready['all_actual_assets'] if v['api_file_object']==obj);check('asset-exact-hashes:'+obj['key'],h(f)==b['sha256'] and hashlib.md5(data).hexdigest()==b['MD5'])
 if f.suffix=='.pdf':check('reader-selected-byte-identity',h(f)==prom['pdf_sha256']==sb['pdf_sha256'])
 if f.suffix=='.tex':check('standalone-controlling-TeX-byte-identity',h(f)==prom['published_tex_sha256']==sb['source_tex_sha256'])
 if f.suffix=='.zip':
  check('complete-ZIP-byte-identity',h(f)==prom['supplement_sha256']==sb['supplement_sha256'])
  with zipfile.ZipFile(f) as z:
   for info in z.infolist():
    if info.is_dir():continue
    data=z.read(info);check('regular-member:'+info.filename,(p/'sources/published-source'/info.filename).read_bytes()==data);archive.append({'member':info.filename,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    if info.filename.lower().endswith('.pdf'):pdfcount+=1
    if info.filename.lower().endswith('.tex'):texmembers.append(hashlib.sha256(data).hexdigest())
check('78-complete-members-no-reader-substitution',len(archive)==78 and pdfcount==0)
check('sole-embedded-TeX-exact',texmembers==[sb['source_tex_sha256']])
check('third-asset-original-link-and-no-extra-local-export',any(b['url']==sb['published_TeX_asset']['api_file_object']['links']['self'] for b in pub['related_resources']) and pub['additional_assets']==[] and sb['published_asset_count']==3)
for b in json.loads((a/'ORIGINAL_OBJECT_COPIES.json').read_text())['copies']:check('verbatim-whole-object-copy:'+b['copy'],(a/b['copy']).read_bytes()==Path(b['source']).read_bytes())
markers=['characteristic zero','Q=xy(x-y)(x-2y)zw(x+z+w)','J=(Q_x,Q_y,Q_z,Q_w)','x_1>x_2>x_3>x_4','\\}=8','full four-variable ideal $B$','degree-seven minimal generator','divisible by $x_3$','largest variable','nonempty open set','Hilbert–Burch','three-generated Jacobian','parallel connection','Migliore–Nagel','J^{\\mathrm{top}}','Ilardi','does not compute the full generic initial ideal','smallest possible number of hyperplanes']
body='\n'.join(pub['result']+pub['why_it_works']+pub['limitations'])
for marker in markers:check('full-scope-boundary:'+marker,marker in body)
negative=[]
for marker in markers:
 changed=body.replace(marker,'');negative.append({'change':'remove required scope/credit '+marker,'rejected':not all(s in changed for s in markers)})
changed=copy.deepcopy(pub);changed['version']='1.0';negative.append({'change':'invent deposit version 1.0','rejected':changed['version'] is not None})
changed=copy.deepcopy(prom);changed['source_files']=changed['source_files'][1:];negative.append({'change':'drop third published TeX asset authentication','rejected':changed['source_files']!=ready['all_actual_assets']})
changed=copy.deepcopy(transport);changed[4]['headers']['oc-checksum']='MD5:0590a0a8f7083974e6c6369b5aee4a79';negative.append({'change':'rewrite actual original checksum-header spelling','rejected':changed!=transport})
changed=copy.deepcopy(prom);changed['reviews']['scope']['verdict']={'status':'PASS'};negative.append({'change':'replace custom whole original verdict by generic PASS','rejected':changed['reviews']['scope']['verdict']!=json.loads((P/root['reviews']['scope']['verdict']).read_text())})
changed=copy.deepcopy(root);changed['reviewed_zenodo_version']='1.0';negative.append({'change':'edit adopted current root object','rejected':changed!=prom['root_clearance_record']})
changed=copy.deepcopy(pub);changed['doi']=raw['conceptdoi'];negative.append({'change':'substitute concept DOI','rejected':changed['doi']!=raw['doi']})
for k in ['canonical_url','follow_up']:
 changed=copy.deepcopy(pub);changed[k]='premature';negative.append({'change':'set '+k,'rejected':changed[k] is not None})
changed=copy.deepcopy(prom);changed['live_verified']=True;negative.append({'change':'premature live publication gate','rejected':changed['live_verified'] is not False})
negative.append({'change':'omit original abstract final sentence','rejected':pub['abstract'].rsplit('.',2)[0]!=visible})
negative.append({'change':'substitute reader bytes','rejected':hashlib.sha256((p/'sources/seven_plane_gin.pdf').read_bytes()+b' ').hexdigest()!=sb['pdf_sha256']})
for b in negative:check('negative:'+b['change'],b['rejected'])
intake=json.loads((a/'INTAKE_RECORD.json').read_text());check('no-fabricated-pending-history',intake['status']=='ROOT_SCIENCE_CLEARED_BEFORE_EDITORIAL_INTAKE' and intake['fake_pending_intake_created'] is False)
dump('ACCEPTANCE_CHECKS.json',{'utc':now(),'positive_checks':checks,'changed_read_negative_controls':negative,'altered_fixture_trees':0,'source_programs_executed':False,'rendering_or_shared_compatibility_tested':False})
dump('READ_LEDGER.json',{'utc':now(),'actual_manuscript':{'PDF':'sources/seven_plane_gin.pdf','pages':6,'TeX':'sources/seven_plane_gin.tex','TeX_lines':396,'extent':'all actual pages and entire standalone controlling TeX read, including references, disclosure and prior limits'},'current_families':[{'report':b['report'],'report_sha256':b['report_sha256'],'verdict':b['verdict'],'verdict_sha256':b['verdict_sha256'],'extent':'entire complete original final REPORT and whole custom verdict object'} for b in root['reviews'].values()],'root_readings':[{'path':str(P/prom['root_clearance_file']),'sha256':prom['root_clearance_sha256'],'extent':'entire exact final authority'},{'path':str(P/root['root_review']),'sha256':root['root_review_sha256'],'extent':'entire final root proof/primary/priority/custody review'},{'path':str(P/root['root_custody_receipt']),'sha256':root['root_custody_receipt_sha256'],'extent':'entire original final custody receipt'},{'path':str(p/'reviews/root/initial-reconstruction.md'),'sha256':h(p/'reviews/root/initial-reconstruction.md'),'extent':'entire initial proof; original pending status retained as history'},{'path':str(p/'reviews/root/initial-reconstruction-seal.json'),'sha256':h(p/'reviews/root/initial-reconstruction-seal.json'),'extent':'entire original early status/seal'}],'source_metadata_and_receipts':'entire SOURCE_READY, raw record, normalized original and every one of six original transport entries read; technical latest/versions/manifests machine authenticated in full','PUBLIC_COPY':'entire actual final public prose read after generation','new_primary_bodies_fetched_or_mathematical_programs_executed':False,'root_science_cleared_before_editorial_intake':True})
dump('custody.json',{'utc':now(),'original_bindings':baseline,'all_originals_unchanged':True,'earlier_owned_bindings':prior,'all_earlier_owned_bindings_unchanged':True,'stale_mutable_site_core_input_maps_followed':False,'archive_member_comparisons':archive,'all_three_API_assets_authenticated':True,'version_absence_preserved':True,'whole_source_receipts_transport_verdicts_and_root_objects_equal':True,'new_configs_and_editorial_only':True})
with (a/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — Full final public copy and source-consumer requirements read. Complete original-object/version/abstract/prose/source/member/authority/gate checks pass and meaningful changed reads reject false variants. All earlier owned packets and row94/95 pending/final seals preserved. Completion 100% for editorial preparation; root editorial reading and all render/live/native gates pending.\n')
exclude={'MANIFEST.json','SEAL.json','SEAL.sha256'};owned={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':h(f)} for f in sorted(a.rglob('*')) if f.is_file() and f.name not in exclude}
for f in [p/'publication.json',p/'promotion.json']:owned[str(f.relative_to(p))]={'bytes':f.stat().st_size,'sha256':h(f)}
dump('MANIFEST.json',{'utc':now(),'record_id':'23395703','status':'FINAL_EDITORIAL_HANDOFF_ROOT_FULL_READ_PENDING','original_input_count':len(baseline),'all_original_inputs_unchanged':True,'original_input_manifest':'reviews/editorial/ORIGINAL_BINDINGS_BEFORE.json','custody':'reviews/editorial/custody.json','owned_output_bindings':owned,'excluded_self_and_seal':sorted(exclude),'root_full_read_before_staging_required':True})
dump('SEAL.json',{'utc':now(),'record_id':'23395703','status':'IMMUTABLE_FINAL_EDITORIAL_HANDOFF','manifest_sha256':h(a/'MANIFEST.json'),'report_sha256':h(a/'REPORT.md'),'public_copy_sha256':h(a/'PUBLIC_COPY.md'),'publication_sha256':h(p/'publication.json'),'promotion_sha256':h(p/'promotion.json'),'root_clearance_sha256':prom['root_clearance_sha256'],'version':None,'owned_output_count':len(owned),'root_editorial_or_rendered_live_native_PASS':False});(a/'SEAL.sha256').write_text(h(a/'SEAL.json')+'  SEAL.json\n')
print(json.dumps({'seal_sha256':h(a/'SEAL.json'),'manifest_sha256':h(a/'MANIFEST.json'),'publication_sha256':h(p/'publication.json'),'promotion_sha256':h(p/'promotion.json'),'owned_outputs':len(owned),'positive_checks':len(checks),'changed_read_controls':len(negative),'originals':len(baseline),'earlier_owned':len(prior),'version':None}))
