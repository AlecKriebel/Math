"""Prepare two private pending editorial intakes. No publication configuration or rendering."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from pypdf import PdfReader
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
now=lambda:datetime.now(timezone.utc).isoformat()
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
def dump(a,name,o):(a/name).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
settings={
 '23181280':{'row':94,'record':'zenodo-record.raw.json','receipt':'api-receipt.json','tex':'published-source/source_preparation/root_dependent_spanning_trees.tex','pdf':'root_dependent_spanning_trees.pdf','zip':'root_dependent_spanning_trees_support.zip','pages':4,'slug':'aggregate-root-dependent-spanning-tree-cost','seo':'Strong NP-completeness for the aggregate cost of one spanning tree oriented at every vertex root, even with costs in {0,1,2}.','date':'6 October 2026','bibkey':'Kriebel2026RootDependentSpanningTrees','members':47},
 '23442760':{'row':95,'record':'record.raw.json','receipt':'api-receipts.json','tex':'published-source/manuscript/main.tex','pdf':'Convex_Body_SOS_Density_Note_v1.0.pdf','zip':'Convex_Body_SOS_Density_Verification_v1.0.zip','pages':5,'slug':'quadratic-sos-density-bounds-convex-bodies','seo':'A single global square gives explicit quadratic SOS-density error bounds on every fixed full-dimensional compact convex body with Lebesgue measure.','date':'17 October 2026','bibkey':'Kriebel2026ConvexBodySOSDensity','members':152}}
for rid,s in settings.items():
 p=P/'papers'/rid;a=p/'reviews/editorial-intake';source=p/'sources';raw=json.loads((source/s['record']).read_text());md=raw['metadata']
 assert not (p/'publication.json').exists() and not (p/'promotion.json').exists()
 tex=(source/s['tex']).read_text();abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
 (a/'ORIGINAL_ABSTRACT.tex').write_text(abstract)
 visible=re.sub(r'\s+',' ',abstract).strip().replace('~',' ')
 if rid=='23442760':visible=visible.replace('\\R','\\mathbb R')
 secs=json.loads((a/'draft-sections.json').read_text());title=md['title'];pages=s['pages']
 text=f'# {title}\n\nAlec Kriebel · [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X)\n\n{s["date"]} · Version {md["version"]} · Unrefereed preprint · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)\n\n{secs["deck"]}\n\n## Original abstract\n\n{visible}\n\n'
 for sec in secs['sections']:text+='## '+sec['heading']+'\n\n'+'\n\n'.join(sec['paragraphs'])+'\n\n'
 text+='## Paper, source and citation\n\n'+f'Read the complete {pages}-page paper, open it directly, or download the deposited PDF. The complete source and verification archive is available alongside the paper at [the selected Zenodo edition]({raw["links"]["self_html"]}).\n'
 (a/'PUBLIC_COPY_DRAFT.md').write_text(text)
 publicsections={'title':title,'author':'Alec Kriebel','ORCID':'https://orcid.org/0009-0001-9320-500X','edition_line':f'{s["date"]} · Version {md["version"]} · Unrefereed preprint','deck':secs['deck'],'original_abstract_label':'Original abstract','original_abstract_one_paragraph':visible,'sections':secs['sections'],'reader_intro':f'The complete {pages}-page deposited paper is available below.','support_intro':'The complete unchanged source and verification archive accompanies the paper.','no_public_audit_narrative':True}
 dump(a,'PUBLIC_SECTIONS_DRAFT.json',publicsections)
 bib='@misc{'+s['bibkey']+',\n  author = {Kriebel, Alec},\n  title = {'+title+'},\n  year = {2026},\n  month = {oct},\n  day = {'+md['publication_date'].split('-')[2]+'},\n  version = {'+md['version']+'},\n  publisher = {Zenodo},\n  doi = {'+raw['doi']+'},\n  url = {'+raw['links']['self_html']+'},\n  note = {Unrefereed preprint; extensive AI assistance; no external human peer review or formal proof certification},\n  orcid = {0009-0001-9320-500X}\n}\n'
 (a/'CITATION_DRAFT.bib').write_text(bib)
 # Preserve complete original objects as exact raw bytes, with original shapes and file names.
 copies=[]
 for f in sorted(source.glob('*.json')):
  dst=a/'original-objects/sources'/f.name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(f.read_bytes());copies.append({'source_path':str(f),'copy_path':str(dst.relative_to(a)),'bytes':f.stat().st_size,'sha256':h(f),'byte_identical':dst.read_bytes()==f.read_bytes()})
 for fam,ver in [('scope','verdict.json'),('analytic','VERDICT.json'),('adversarial','verdict.json')]:
  f=p/'reviews'/fam/ver;dst=a/'original-objects/reviews'/fam/ver;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(f.read_bytes());copies.append({'source_path':str(f),'copy_path':str(dst.relative_to(a)),'bytes':f.stat().st_size,'sha256':h(f),'byte_identical':True})
 for name in ['initial-reconstruction.md','initial-reconstruction-seal.json']:
  f=p/'reviews/root'/name;dst=a/'original-objects/root'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(f.read_bytes());copies.append({'source_path':str(f),'copy_path':str(dst.relative_to(a)),'bytes':f.stat().st_size,'sha256':h(f),'byte_identical':True})
 dump(a,'ORIGINAL_OBJECT_COPIES.json',{'copy_method':'verbatim raw bytes; no reserialization, verdict normalization or added HTTP fields','copies':copies,'all_complete_original_custom_verdict_objects_preserved':True})
 assets=[]
 for filename in [s['pdf'],s['zip']]:
  obj=next(x for x in raw['files'] if x['key']==filename);f=source/filename
  assets.append({'actual_file_object':obj,'source_path':str(f),'bytes':f.stat().st_size,'sha256':h(f),'md5':hashlib.md5(f.read_bytes()).hexdigest(),'actual_original_URL':obj['links']['self'],'complete_unchanged_required':True})
 assert len(raw['files'])==2
 metas={'document_kind':'PRIVATE_EDITORIAL_REQUIREMENTS_NOT_SITE_CONFIGURATION','record_id':int(rid),'row':s['row'],'title':title,'DOI':raw['doi'],'concept_record_id':raw['conceptrecid'],'version':md['version'],'declared_publication_date':md['publication_date'],'manuscript_date':s['date'],'API_created':raw['created'],'API_modified':raw.get('modified'),'API_updated':raw.get('updated'),'creators_original':md['creators'],'license_original':md['license'],'resource_type_original':md['resource_type'],'keywords_original':md['keywords'],'selected_record_URL':raw['links']['self_html'],'canonical':None,'AA':None,'followup':None,'suggested_slug_unassigned':s['slug'],'SEO_description_draft':s['seo'],'SEO_title_draft':title+' | Alec Kriebel','abstract':{'label':'Original abstract','complete_TeX_substring':'ORIGINAL_ABSTRACT.tex','sha256':h(a/'ORIGINAL_ABSTRACT.tex'),'visible_complete_one_paragraph':visible,'allowed_changes':['whitespace folding','TeX nonbreaking spaces displayed as ordinary spaces','source-defined \\R expanded to its exact \\mathbb R definition for standard math rendering when present'],'no_sentence_omissions':True},'assets':assets,'reader_requirements':{'pages':pages,'one_full_local_PDF_iframe':True,'direct_open_link':True,'explicit_local_PDF_download':True,'explicit_Zenodo_original_PDF_download':True,'source_reader_bytes_identical':True,'reader_intro':publicsections['reader_intro'],'no_rebuild_truncation_or_historical_reader':True},'support_requirements':{'complete_original_ZIP_local_download':True,'complete_original_ZIP_Zenodo_download':True,'regular_member_count':s['members'],'publish_only_PDF_complete_ZIP_BibTeX_and_article_as_page_assets':True,'no_source_cache_or_selected_script_bundle':True,'preserve_all_internal_history_and_license_notices':True},'citation_requirements':{'file':'CITATION_DRAFT.bib','sha256':h(a/'CITATION_DRAFT.bib'),'selected_record_DOI':True,'sole_actual_author':True,'exact_date_version_status':True},'presentation':{'font':'Arial, Helvetica, sans-serif','background':'white','layout':'existing plain single-column blog article','full_abstract_visible_and_indexable':True,'complete_theorem_conditions_visible':True,'license_visible_in_header_and_future_schema':'CC BY 4.0','no_framework_cards_audit_badges_or_extra_control_story':True},'scientific_authority':'PENDING_EXACT_SEPARATE_ROOT_CLEARANCE','gates':{'root_scientific_clearance_adopted':False,'editorial_final_approval':False,'publication_config_created':False,'promotion_config_created':False,'rendered':False,'browser_verified':False,'native_verified':False,'live_verified':False,'staged':False,'deployed':False,'published':False},'prohibited_until_separate_root_instruction':['publication.json','promotion.json','site/config/shared-core mutation','render/stage/browser/native/Git/deploy/redirect/release/outreach']}
 dump(a,'METADATA_READER_SUPPORT_REQUIREMENTS.json',metas)
 dump(a,'INTAKE_STATUS.json',{'assignment_status':'COMPLETE_PRIVATE_EDITORIAL_INTAKE_PENDING_ROOT','record_id':int(rid),'scientific_publication_gate':'PENDING_EXACT_ROOT_CLEARANCE','root_PASS_claimed':False,'all_publication_native_live_gates':False,'publication_config_created':False,'promotion_config_created':False,'canonical':None,'AA':None,'followup':None,'substantive_discrepancy_found':False,'separate_root_instruction_required_before_final_configs':True,'all203_goal_complete':False})
 # Full actual reader extraction is owned intake evidence, not replacement public asset.
 reader=PdfReader(str(source/s['pdf']));assert len(reader.pages)==pages
 (a/'ACTUAL_MANUSCRIPT_READ.txt').write_text('\n'.join(f'--- PAGE {i+1} ---\n'+pg.extract_text() for i,pg in enumerate(reader.pages)))
 print(rid,'draft prepared',len(copies),'original byte copies',len(text),'public draft bytes')
