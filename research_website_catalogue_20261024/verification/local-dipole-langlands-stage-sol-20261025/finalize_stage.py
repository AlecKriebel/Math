"""Finalize read-only custody and seal the bounded private-stage handoff."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,re
O=Path(__file__).resolve().parent;R=O.parents[1]
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
IDS=['23390551','23430326']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
 p=O/name;p.write_text(obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
initial=json.loads((O/'inputs-before.json').read_text())['bindings']
legacy=json.loads((O/'old-comparison-inputs-before.json').read_text())['bindings']
merged=dict(initial)
for name,row in legacy.items():
 if name in merged:assert merged[name]==row,name
 merged[name]=row
after={}
for name,row in merged.items():
 p=Path(name);current={'bytes':p.stat().st_size,'sha256':sha(p)}
 assert current==row,name;after[name]=current
site_before={name:row for name,row in initial.items() if Path(name).is_relative_to(LIVE)}
assert len(site_before)==464
assert {str(p) for p in LIVE.rglob('*') if p.is_file()}==set(site_before)
assert not (R/'scripts/dipole_source.py').exists()
assert not (O/'memory-render').exists()
for name in ['bosonic_source.py','published_assets.py']:
 assert (R/'scripts'/name).read_bytes()==(O/'inputs'/name).read_bytes()
edits=json.loads((O/'reversible-proposal-edits.json').read_text())
for label,old,proposed in [('renderer','render_page.py','render_page.proposed.py'),('checker','final-content-check.py','final-content-check.proposed.py')]:
 content=(O/proposed).read_text()
 for a,b,count in reversed(edits[label]):assert content.count(b)==count;content=content.replace(b,a)
 assert content==(O/'inputs'/old).read_text()
save('entire-existing-scripts-preservation.json',{'utc':now(),'status':'PASS','entire_current_renderer_recovered_by_exact_reversal':True,'entire_current_checker_recovered_by_exact_reversal':True,'current_shared_renderer':sha(R/'scripts/render_page.py'),'current_shared_checker':sha(R/'verification/final-content-check.py'),'existing_helpers_unchanged':{name:sha(R/'scripts'/name) for name in ['bosonic_source.py','published_assets.py']},'new_helper_not_installed':True,'actual_site_file_count_unchanged':464})

class Frames(HTMLParser):
 def __init__(self,text):super().__init__();self.frames=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  if tag=='iframe':self.frames.append(dict(attrs))

source_bindings={};ledger=[]
for rid in IDS:
 p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());spec=json.loads((p/'reviews/editorial/public-sections.json').read_text())
 page=O/'public/research'/c['slug']/'index.html';html=page.read_text();actual_file=O/('public-sections-'+rid+'.json');actual=json.loads(actual_file.read_text());frames=Frames(html).frames
 assert len(frames)==1 and frames[0]=={'class':'paper-pdf',**next(x['iframe'] for x in spec['sections'] if x['id']=='paper')}
 actual['iframes']=frames;save(actual_file.name,actual)
 assert spec['header']['title']==c['title'] and spec['header']['description']==c['description'] and spec['header']['publication_date']==c['publication_date'] and spec['header']['version']==c['version']
 mapping={'abstract':c['abstract'].split('\n\n'),'plain-language':c['plain_language'],'result':c['result'],'proof':c['why_it_works'],'limits':c['limitations'],'status':[c['ai_disclosure'],c['edition_note']]}
 for section in spec['sections']:
  if section['id'] in mapping:assert section['paragraphs']==mapping[section['id']]
  if section['id']=='background':assert section['references']==c['background']
 assert spec['bibtex']==(p/'reviews/editorial/citation.bib').read_text()==(page.parent/'citation.bib').read_text()
 authority=json.loads((R/g['root_clearance_file']).read_text());assert authority==g['root_clearance_record']
 raw=json.loads((p/g['source_receipt_path']).read_bytes());assert raw==g['source_receipt_record']
 for role,item in g['reviews'].items():assert item['verdict']==json.loads((p/item['verdict_file']).read_bytes())
 b=c['source_binding'];source_bindings[rid]={'publication_sha256':sha(p/'publication.json'),'promotion_sha256':sha(p/'promotion.json'),'source_binding':b,'original_complete_receipt_sha256':sha(p/g['source_receipt_path']),'separate_root_scientific_sha256':sha(R/g['root_clearance_file']),'separate_root_editorial_sha256':sha(R/f'verification/root-editorial-{rid}-20261025.json'),'editorial_seal_sha256':sha(p/'reviews/editorial/SEAL.json'),'original_custom_objects_structurally_equal':True,'selected_public_pdf_sha256':sha(page.parent/c['pdf_filename']),'complete_public_zip_sha256':sha(page.parent/c['supplement_filename']),'prepared_bibtex_sha256':sha(page.parent/'citation.bib'),'actual_public_copy_sha256':sha(O/('public-copy-'+rid+'.txt')),'actual_sections_sha256':sha(actual_file),'iframe_exact_approved_attributes':True}
 for relative in ['reviews/editorial/REPORT.md','reviews/editorial/PUBLIC_COPY.md','reviews/editorial/public-sections.json','reviews/editorial/SCHEMA_ADAPTER.json','reviews/editorial/SEAL.json','publication.json','promotion.json','reviews/root/ROOT_REVIEW.md']:
  f=p/relative;extent='Complete full text read.'
  if relative.endswith('.json'):extent='Complete object parsed; every public field compared with full read copy/specification; all original custom verdict, receipt and root objects compared structurally and bound to exact authorities.'
  ledger.append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f),'read_extent':extent})
 for name in [g['root_clearance_file'],f'verification/root-editorial-{rid}-20261025.json']:
  f=R/name;ledger.append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f),'read_extent':'Complete separate root authority object read; exact hash matched.'})
 for name in ['public-copy-'+rid+'.txt','public-sections-'+rid+'.json']:
  f=O/name;ledger.append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f),'read_extent':'Complete actual visible copy/ordered sections read; complete paragraphs, background notes, links/downloads and approved iframe compared.'})
save('source-bindings.json',{'utc':now(),'records':source_bindings,'original_receipts_and_custom_objects_unchanged':True,'new_helper_view_persisted':False,'synthetic_HTTP_fields_created':False,'source_aliases_created':False})
for name,extent in [
 ('dipole_source.py','Complete new production helper and all authentication requirements read.'),
 ('render_page.proposed.py','Complete renderer read, narrow proposal diff reviewed, all54 old configured executions compared as exact bytes.'),
 ('final-content-check.proposed.py','Relevant original architecture/dispatch/source handling and entire new normalizer/archive/check block read; entire original checker recovered by exact reverse edits, all54 original dispatches compared.'),
 ('proposed-dipole-source.diff','Complete diff reviewed.'),('proposed-shared-renderer.diff','Complete diff reviewed.'),('proposed-shared-checker.diff','Complete narrow diff reviewed.'),
 ('renderer-staging-overrides.diff','Complete explicit private override diff reviewed.'),('checker-staging-overrides.diff','Complete explicit private override diff reviewed.')]:
 f=O/name;ledger.append({'path':str(f),'bytes':f.stat().st_size,'sha256':sha(f),'read_extent':extent})
save('READ_LEDGER.json',{'utc':now(),'scope':'Private integration/copy/object/custody verification; no new independent scientific verdict or literature audit.','complete_readings_and_structural_comparisons':ledger,'all_source_and_old_render_original_reads_bound':True,'old_abstract_source_count':54,'old_configured_renderer_executions':108,'old_output_files_written':0,'source_mathematical_programs_rerun':False,'browser_UI_used':False,'individual_contact_or_outreach':False,'original_renderer_and_existing_helpers_read_in_full':True,'original_checker_read_scope':'Relevant architecture and prior SCB/common branches; preserved whole file by exact edit reversal and old-dispatch executions, not a claimed fresh mathematical reading of every old paper.'})
save('custody-after.json',{'utc':now(),'status':'ALL_BOUND_ORIGINALS_UNCHANGED','original_bindings':len(merged),'initial_lean_bindings':len(initial),'legacy_read_bindings':len(legacy),'bindings':after,'actual_site_files':464,'prior_owned_packages':json.loads((O/'protected-prior-packages.json').read_text()),'own_mutation_scope':str(O),'actual_site_inventory_unchanged':True,'new_helper_installed':False})
target=json.loads((O/'target-stage-check-final.json').read_text());controls=json.loads((O/'negative-controls.json').read_text());stage=json.loads((O/'stage-validation.json').read_text())
assert target['status']=='PASS' and all(all(x['checks'].values()) for x in target['papers'].values())
assert controls['controls_rejected']==40 and controls['fixture_stage_copies']==0
assert stage['private_index_entries']==57 and stage['private_sitemap_urls']==58
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(now()+' — 100%: Full actual new2 public copies/sections and complete proposals reviewed;137/137 target checks and40 changed-read rejections complete. All54 old dispatches and54 configured old render outputs byte-identical; privateindex57/sitemap58 preserve55/56 original entries. All'+str(len(merged))+' original bindings including464 actualsitefiles and four prior sealed packages rehashed unchanged. Only owned private output exists. No source programs, actual production/browser/live/native/Git/deployment/release action. Full manifest sealed for root reading; overall203programme ongoing.\n')
save('completion.json',{'utc':now(),'status':'PRIVATE_STAGE_CHECKS_PASS_PENDING_ROOT_ACCEPTANCE_AND_PUBLICATION_GATES','completion_percent_of_assigned_private_stage':100,'records':IDS,'target_checks':{rid:{'passed':sum(x['checks'].values()),'total':len(x['checks'])} for rid,x in target['papers'].items()},'negative_controls':40,'fixture_copies':0,'old_dispatches_unchanged':54,'old_configured_renderer_outputs_byte_identical':54,'private_index_entries':57,'private_sitemap_urls':58,'original_bindings_unchanged':len(merged),'actual_site_files_unchanged':464,'source_or_config_or_shared_core_mutated':False,'new_helper_installed':False,'actual_site_rendered':False,'live_verified':False,'browser_verified':False,'native_sheet_modified':False,'native_AA':None,'source_programs_rerun':False,'git_or_deploy_or_release_action':False,'external_contact_or_outreach':False,'overall_goal_complete':False})
report=(O/'REPORT.md').read_text()
for old,new in [('overall203-paper','overall 203-paper'),('—23390551','— 23390551'),('—23430326','— 23430326'),('say11 and9','say 11 and 9'),('restricted to23390551','restricted to 23390551'),('CC BY4.0','CC BY 4.0'),('zero3×3','zero 3×3'),('support atκ=','support at κ='),('rational-mesh3×3','rational-mesh 3×3'),('All37','All 37'),('Dipole69/69','Dipole 69/69'),('Langlands68/68','Langlands 68/68'),('all55 old','all 55 old'),('giving56','giving 56'),('a45-second','a 45-second'),('actual464-file','actual 464-file'),('Their2897','Their 2897'),('about6.7MiB','about 6.7 MiB'),('previous55-paper','previous 55-paper')]:report=report.replace(old,new)
(O/'REPORT.md').write_text(report)
excluded={'stage-readiness-manifest.json','stage-readiness-manifest.sha256'}
owned={str(p.relative_to(O)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.rglob('*')) if p.is_file() and p.name not in excluded}
manifest={'utc':now(),'status':'PRIVATE_STAGE_CHECKS_PASS_PENDING_ROOT_ACCEPTANCE_AND_PUBLICATION_GATES','completion_percent':100,'scope':'Owned private stage only; no actual production/live/browser/native publication PASS.','original_input_bindings':merged,'all_original_inputs_unchanged':True,'owned_output_bindings':owned,'excluded_self':'stage-readiness-manifest.json and its checksum sidecar','proposal_sha256':{name:sha(O/name) for name in ['dipole_source.py','render_page.proposed.py','final-content-check.proposed.py']},'actual_site_render_live_browser_native_publication_pass':False}
save('stage-readiness-manifest.json',manifest)
digest=sha(O/'stage-readiness-manifest.json');save('stage-readiness-manifest.sha256',digest+'  stage-readiness-manifest.json\n')
print(json.dumps({'status':manifest['status'],'manifest_sha256':digest,'original_bindings':len(merged),'owned_outputs':len(owned),'private_public_files':len(list((O/'public').rglob('*')))}))
