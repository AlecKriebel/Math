from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for id in ['23414025','23390181']:
 p=B/id/'reviews/scope';c=json.loads((p/'content.json').read_text());s=json.loads((p/'source_integrity.json').read_text());now=datetime.now(timezone.utc).isoformat()
 assert s['pass'] and c['follow_up'] is None and c['version']=='1.0.0' and c['publication_date']==c['source_binding']['publication_date']
 assert all((B/id/'sources'/f['name']).exists() for f in c['source_binding']['files'])
 v={'record_id':id,'role':'independent_publication_scope_and_primary_literature_review','timestamp_utc':now,'completion_percent':100,'scope_verdict':'no_publication_scope_defect_identified','publication_disposition':'candidate_content_only_pending_separate_mathematical_gates','mathematical_gate':False,'novelty_certified':False,'independent_human_peer_review':False,'full_published_paper_read':True,'published_paper_pages':s['main_pdf_pages'],'published_supplement_pdfs':[],'all_published_assets_acquired':True,'source_integrity_pass':True,'archived_or_sibling_review_verdicts_used':False,'independence_note':'Own preliminary scope conclusion recorded at the 60% checkpoint. No dedicated archived or sibling mathematical audit verdicts were consulted. The published note and original authored material contain historical review/search/status assertions; these were encountered, not adopted as validation.','content_sha256':hashlib.sha256((p/'content.json').read_bytes()).hexdigest(),'source_binding':c['source_binding'],'follow_up':None,'followup_rationale':c['followup_rationale'],'defects':[],'key_boundaries':c['limitations']}
 (p/'verdict.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 with (p/'RESEARCH_LOG.md').open('a') as f:f.write(f'\n## {now} — 100%\n\nIndependent scope review, bounded primary-source comparison, full manuscript/author-proof reading, source-integrity receipt, exact-abstract page candidate and source-bound verdict finalized. No publication-scope defect identified; mathematical gates remain separate. No follow-up proposed. No website, spreadsheet, Git, Zenodo or outreach actions taken. Content SHA-256: {v["content_sha256"]}.\n')
 print(id,v['content_sha256'],s['main_pdf_pages'],s['manifest_entries_verified'])
