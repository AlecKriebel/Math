"""Prepare only new private editorial files and two absent record configs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,shutil
E=Path(__file__).resolve().parent;B=E.parents[1];P=B.parents[1];S=B/'sources'
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def req(c,m):
    if not c:raise RuntimeError(m)
def bind(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def save(name,d):
    p=E/name;req(not p.exists(),'new file only: '+name);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
req(not (B/'publication.json').exists() and not (B/'promotion.json').exists(),'both record configs previously absent')
authority=P/'verification/root-clearance-23217863-20261025.json';req(sha(authority)=='b8f379a432a6866d611b929b8c91a410312a36943b99051574edc135598b280a','root authority')
root=load(authority);req(root['editorial_preparation_authorized'] is True and root['publication_authorized_by_this_object'] is False,'authority scope')
req(sha(P/root['root_review'])==root['root_review_sha256']=='6a875d1669d037458e99e7399d373ae996d145ad8833c9f03e524aaa0dfce13b','root review')
ready=load(S/'SOURCE_READY.json');meta=load(S/'normalized-metadata.json');raw=load(S/'record.raw.json');transport=load(S/'api-receipts.json');inventory=load(S/'archive-members.json')
req(sha(S/'SOURCE_READY.json')==root['source_receipt_sha256'],'ready binding')
req('version' not in raw['metadata'] and ready['version'] is None and meta['version_value'] is None and root['reviewed_zenodo_version'] is None,'absent version')
req(raw['files']==[r['original_api_file_object'] for r in ready['all_assets']]==meta['all_original_API_file_objects'],'whole ordered file objects')
req([r['key'] for r in raw['files']]==['paper.pdf','source-and-verification.zip'],'actual asset order')
req(len(transport)==5 and all(r['status']==200 for r in transport),'genuine five native transport entries')
original_paths=set(S.rglob('*'));original_paths={p for p in original_paths if p.is_file()}
req(len(original_paths)==54,'54 complete source files')
for folder,n in [(B/'reviews/scope','FINAL_MANIFEST.json'),(B/'reviews/analytic','MANIFEST.json'),(B/'reviews/adversarial','FINAL_MANIFEST.json'),(P/'papers/22395326/reviews/adversarial','FINAL_MANIFEST.json')]:
    m=load(folder/n);rows=m.get('files',m.get('portable_files'))
    rows=[dict(v,path=k) for k,v in rows.items()] if isinstance(rows,dict) else rows
    for row in rows:
        p=folder/row['path'];req(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'scientific owned binding');original_paths.add(p)
    original_paths.add(folder/n)
    for seal in ['FINAL_SEAL.json','SEAL.json']:
        if (folder/seal).exists():original_paths.add(folder/seal)
# Bind row104 ignored execution/render evidence as immutable evidence, without copying it.
last=P/'papers/22395326/reviews/adversarial'
for row in load(last/'REPLAY_WORK_MANIFEST.json')['files']:
    p=last/row['path'];req(sha(p)==row['sha256'],'row104 disposable evidence unchanged');original_paths.add(p)
original_paths.update([authority,P/root['root_review'],P/root['root_custody_receipt']])
baseline=[bind(p) for p in sorted(original_paths)]
save('ORIGINAL_BINDINGS_BEFORE.json',{'utc':datetime.now(timezone.utc).isoformat(),'scope':'All54 original source files, current103 scientific owned packets, root authority/custody and immutable104 adversarial packet including its bound disposable evidence; no broad programme/cache copy.','file_count':len(baseline),'files':baseline})
reviews={};copies=[];C=E/'original-objects';C.mkdir(exist_ok=False)
copy_paths=[(S/n,n) for n in ['SOURCE_READY.json','normalized-metadata.json','record.raw.json','latest.raw.json','versions.raw.json','api-receipts.json','archive-members.json','SOURCE_READY_MANIFEST.json','SOURCE_READY_SEAL.json','SOURCE_FINAL_MANIFEST.json','SOURCE_FINAL_SEAL.json']]
copy_paths +=[(authority,'root-clearance.json'),(P/root['root_review'],'root-review.md'),(P/root['root_custody_receipt'],'root-custody-recheck.json')]
for family,entry in root['reviews'].items():
    rp=P/entry['report'];vp=P/entry['verdict'];v=load(vp)
    req(sha(rp)==entry['report_sha256'] and sha(vp)==entry['verdict_sha256'],'literal scientific reports')
    req(v==entry['whole_original_custom_verdict'],'whole original custom verdict equality')
    reviews[family]={'report':str(rp.relative_to(B)),'report_sha256':sha(rp),'verdict_file':str(vp.relative_to(B)),'verdict_sha256':sha(vp),'verdict':v,'root_authority_entry':entry}
    copy_paths.append((vp,family+'-verdict.json'))
for source,name in copy_paths:
    target=C/name;shutil.copyfile(source,target);req(source.read_bytes()==target.read_bytes(),'exact custody copy')
    copies.append({'source':bind(source),'copy':bind(target)})
save('ORIGINAL_OBJECT_COPIES.json',{'copies':copies,'count':len(copies),'custody_copies_not_source_aliases':True})
texpath=S/'published-source/manuscript/main.tex';tex=texpath.read_text();abstract_tex=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
(E/'ORIGINAL_ABSTRACT.tex').write_text(abstract_tex)
abstract=' '.join(abstract_tex.replace('Banach--Mazur','Banach–Mazur').replace('$*$','*').replace('~',' ').split())
copy=load(E/'public-prose.json');copy['abstract']=abstract;(E/'public-prose.json').write_text(json.dumps(copy,indent=2,ensure_ascii=False)+'\n')
bib='''@misc{Kriebel2026OrdinaryBanachMazurRigidity,
  author = {Kriebel, Alec},
  title = {Ordinary Banach--Mazur rigidity of von Neumann algebras},
  year = {2026},
  month = {oct},
  day = {7},
  date = {2026-10-07},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23217863},
  url = {https://zenodo.org/records/23217863},
  note = {Unrefereed preprint; no version number supplied},
  orcid = {0009-0001-9320-500X}
}
''';(E/'CITATION.bib').write_text(bib)
now=datetime.now(timezone.utc).isoformat()
later={'rendered':False,'deployed':False,'rendered_public_copy_approved':False,'local_http_verified':False,'live_http_verified':False,'browser_verified':False,'native_sheet_publication_verified':False,'public_page_published':False,'native_sheet_aa_url':None,'root_editorial_clearance_received':False}
sb={'record_id':23217863,'concept_record_id':ready['conceptrecid'],'record_url':'https://zenodo.org/records/23217863','doi':ready['doi'],'version':None,'version_field_present':False,'zenodo_version':None,'manuscript_version':None,'zenodo_publication_date':ready['publication_date'],'manuscript_date':'2026-10-07','record_created_utc':ready['created'],'record_updated_utc':ready['updated'],'metadata_path':'sources/normalized-metadata.json','metadata_sha256':sha(S/'normalized-metadata.json'),'metadata_original':meta,'raw_record_path':'sources/record.raw.json','raw_record_sha256':sha(S/'record.raw.json'),'raw_record_original':raw,'source_receipt_path':'sources/SOURCE_READY.json','source_receipt_sha256':sha(S/'SOURCE_READY.json'),'source_receipt_schema':'Native all_assets/original_api_file_object and lowercase md5/sha256; metadata nested under metadata; version absent; genuine five-entry api-receipts; SOURCE_FINAL_MANIFEST dict and nested SOURCE_FINAL_SEAL manifest object. No aliases.','source_receipt_original':ready,'source_assets_field':'all_assets','all_assets':ready['all_assets'],'published_file_objects':raw['files'],'published_asset_count':2,'actual_asset_order':['paper.pdf','source-and-verification.zip'],'recursive_archive_inventory_path':'sources/archive-members.json','recursive_archive_inventory_sha256':sha(S/'archive-members.json'),'recursive_archive_inventory_original':inventory,'transport_receipt_path':'sources/api-receipts.json','transport_receipt_sha256':sha(S/'api-receipts.json'),'transport_receipt_original':transport,'transport_receipt_entry_count':5,'source_ready_manifest_path':'sources/SOURCE_READY_MANIFEST.json','source_ready_manifest_sha256':sha(S/'SOURCE_READY_MANIFEST.json'),'source_ready_seal_path':'sources/SOURCE_READY_SEAL.json','source_ready_seal_sha256':sha(S/'SOURCE_READY_SEAL.json'),'source_final_manifest_path':'sources/SOURCE_FINAL_MANIFEST.json','source_final_manifest_sha256':sha(S/'SOURCE_FINAL_MANIFEST.json'),'source_final_manifest_original':load(S/'SOURCE_FINAL_MANIFEST.json'),'source_final_seal_path':'sources/SOURCE_FINAL_SEAL.json','source_final_seal_sha256':sha(S/'SOURCE_FINAL_SEAL.json'),'source_final_seal_original':load(S/'SOURCE_FINAL_SEAL.json'),'asset_root_path':'sources','pdf_sha256':ready['all_assets'][0]['sha256'],'supplement_sha256':ready['all_assets'][1]['sha256'],'source_tex_path':'sources/published-source/manuscript/main.tex','source_tex_sha256':sha(texpath),'abstract_tex':abstract_tex,'abstract_source':'sources/published-source/manuscript/main.tex','abstract_source_sha256':sha(texpath),'abstract_normalization':'Complete original TeX abstract, whitespace folded; Banach--Mazur to en dash, $*$ to *, and nonbreaking ~ to space only. No omissions.','public_page_reader_pdf_count':1,'archive_regular_member_occurrences':41,'archive_container_count':1,'nested_archive_count':0,'archive_embedded_pdf_count':1,'embedded_PDF_role':'Distinct28-page OpenAI upstream supporting manuscript; not an alternative target reader.','total_distinct_target_reader_pdf_count':1,'reader_intro':copy['reader_intro'],'prepared_bibtex_path':'reviews/editorial/CITATION.bib','prepared_bibtex_sha256':sha(E/'CITATION.bib'),'publication_state':'PRIVATE_EDITORIAL_CONFIGS_READY_RENDERING_PENDING','review_boundary':'Separate authenticated root scientific clearance already complete. Every later editorial/render/local/live/browser/native/public gate remains false; no source alias or shared-helper integration performed.'}
pub={**{k:copy[k] for k in ['title','description','abstract','plain_language','result','why_it_works','limitations','background','ai_disclosure','collaboration']},'slug':'ordinary-banach-mazur-rigidity-von-neumann-algebras','abstract_heading':'Original abstract','abstract_is_original':True,'follow_up':None,'followup_rationale':'Default none under separate root authority.','AA':None,'canonical_url':None,'publication_date':'2026-10-07','version':None,'version_field_present':False,'doi':ready['doi'],'author':'Alec Kriebel','orcid':'https://orcid.org/0009-0001-9320-500X','pdf_filename':'paper.pdf','pdf_pages':7,'supplement_filename':'source-and-verification.zip','supplement_label':'Complete original source and verification archive (ZIP)','additional_assets':[],'related_resources':[{'label':'Zenodo original complete seven-page paper','url':raw['files'][0]['links']['self']},{'label':'Zenodo original complete source and verification ZIP','url':raw['files'][1]['links']['self']}],'status':copy['status'],'license':'CC BY 4.0 for original manuscript, prose and verification code','license_url':'https://creativecommons.org/licenses/by/4.0/','license_note':'Unchanged OpenAI family-295 material in the complete source archive retains Apache License 2.0, its original OpenAI attribution, LICENSE and manuscript-specific README citation. CC BY 4.0 does not relicense it. Other linked literature retains its own terms.','publication_date_label':'Manuscript and declared publication date','edition_label':'No version number supplied','citation_edition_label':'No version number supplied','edition_note':copy['edition_note'],'reader_intro':copy['reader_intro'],'bibtex_note':'Unrefereed preprint; no version number supplied','prepared_bibtex':bib,'source_binding':sb,'review_metadata':{'prepared_utc':now,'completion_percent':100,'scientific_clearance_received':True,'root_scientific_status':root['status'],'root_clearance_file':str(authority.relative_to(P)),'root_clearance_sha256':sha(authority),'publication_state':'PRIVATE_EDITORIAL_CONFIGS_READY_RENDERING_PENDING',**later}}
(B/'publication.json').write_text(json.dumps(pub,indent=2,ensure_ascii=False)+'\n')
pro={'record_id':23217863,'status':root['status'],'disposition_by':'root','created_utc':now,'approved_scope':root['approved_scope'],'root_clearance_file':str(authority.relative_to(P)),'root_clearance_sha256':sha(authority),'root_clearance_record':root,'publication_sha256':sha(B/'publication.json'),'pdf_sha256':sb['pdf_sha256'],'supplement_sha256':sb['supplement_sha256'],'source_receipt_path':sb['source_receipt_path'],'source_receipt_sha256':sb['source_receipt_sha256'],'source_receipt_schema':sb['source_receipt_schema'],'source_receipt_original':ready,'all_assets':ready['all_assets'],'published_file_objects':raw['files'],'metadata_path':sb['metadata_path'],'metadata_sha256':sb['metadata_sha256'],'raw_record_path':sb['raw_record_path'],'raw_record_sha256':sb['raw_record_sha256'],'recursive_archive_inventory_original':inventory,'transport_receipt_path':sb['transport_receipt_path'],'transport_receipt_sha256':sb['transport_receipt_sha256'],'transport_receipt_original':transport,'source_final_manifest_original':sb['source_final_manifest_original'],'source_final_seal_original':sb['source_final_seal_original'],'root_custody_receipt':root['root_custody_receipt'],'root_custody_receipt_sha256':root['root_custody_receipt_sha256'],'reviews':reviews,'version':None,'version_field_present':False,'source_repair':False,'human_peer_review':False,'formal_machine_verification':False,'follow_up':None,'canonical_url':None,'AA':None,'preparation_state':'PRIVATE_EDITORIAL_CONFIGS_READY_RENDERING_PENDING',**later}
(B/'promotion.json').write_text(json.dumps(pro,indent=2,ensure_ascii=False)+'\n')
sections={'abstract':[abstract],**{k:copy[k] for k in ['plain_language','result','why_it_works','limitations']},'status':[copy['status'],copy['ai_disclosure'],copy['edition_note']],'reader':[copy['reader_intro']],'background':copy['background'],'collaboration':[copy['collaboration']],'licensing':[pub['license'],pub['license_note']],'follow_up':None}
save('public-sections.json',sections)
doc=['# '+pub['title'],'',pub['description'],'']
for key,title in [('abstract','Original abstract'),('plain_language','The idea in plain English'),('result','The precise result'),('why_it_works','Why the result holds'),('limitations','Scope and limits'),('status','Status and AI use'),('reader','Read the paper'),('background','Background and prior work'),('collaboration','Collaboration'),('licensing','Licensing')]:
    doc+=['## '+title,'']
    if key=='background':
        for r in sections[key]:doc += ['- ['+r['title']+']('+r['url']+'): '+r['note'],'']
    else:
        for para in sections[key]:doc +=[para,'']
doc +=['## Citation','',bib.strip(),''];(E/'PUBLIC_COPY.md').write_text('\n'.join(doc))
save('INTAKE_RECORD.json',{'utc':now,'source_ready_original':ready,'metadata_original':meta,'root_authority_original':root,'original_asset_order':sb['actual_asset_order'],'all_later_publication_gates':later,'no_fresh_transport_claim':True})
save('METADATA_READER_SUPPORT_REQUIREMENTS.json',{'title':pub['title'],'doi':pub['doi'],'version':None,'version_field_present':False,'declared_date':pub['publication_date'],'actual_created_utc':ready['created'],'target_reader':ready['all_assets'][0],'target_reader_pages':7,'full_local_iframe_and_open_and_explicit_download_required':True,'original_Zenodo_reader_url':raw['files'][0]['links']['self'],'complete_original_support':ready['all_assets'][1],'original_Zenodo_support_url':raw['files'][1]['links']['self'],'complete_local_ZIP_link_required':True,'future_article_files':['index.html','paper.pdf','source-and-verification.zip','citation.bib'],'support_member_count':41,'upstream_PDF_distinct_28pages_not_second_target_reader':True,'export_ignored_primary_cache':False,'licenses':{'authored':'CC BY 4.0','unchanged_upstream':'Apache-2.0 with original LICENSE/OpenAI attribution/README citation; no relicensing','Roydor_or_other_literature_redistribution_permission_inferred':False},'prepared_bibtex':bind(E/'CITATION.bib'),'canonical_url':None,'AA':None,'follow_up':None,'publication_gates':later})
save('READ_LEDGER.json',{'utc':now,'root_authority_fully_read':bind(authority),'root_review_fully_read':bind(P/root['root_review']),'current_scientific_reports':{k:{'report':v['report'],'sha256':v['report_sha256'],'full_report_read':True,'literal_verdict_sha256':v['verdict_sha256']} for k,v in reviews.items()},'target_reader_full7pages_read_in_prior_own_scientific_lane':bind(S/'paper.pdf'),'controlling_source_full449lines_reread':bind(texpath),'license_sources_fully_read':[bind(S/'published-source/LICENSES.md'),bind(S/'published-source/sources/upstream/LICENSE'),bind(S/'published-source/sources/upstream/ATTRIBUTION.md'),bind(S/'published-source/sources/upstream/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026/README.md')],'new_PDF_render_or_mathematical_replay':False,'shared_renderer_read_only_observation':bind(P/'scripts/render_page.py'),'no_shared_helper_or_site_compatibility_claim':True})
print(json.dumps({'private_editorial_prepared':True,'source_files_bound':54,'baseline_files':len(baseline),'exact_custody_copies':len(copies),'promotion_status_preserved':pro['status'],'version':None,'all_later_gates_false':True}))
