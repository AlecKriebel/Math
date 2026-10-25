from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
for ident in ['22929486','23088066']:
 p=B/ident/'reviews/scope';c=json.loads((p/'content.json').read_text());s=json.loads((p/'source_integrity.json').read_text())
 assert s['passed'] and s['all_public_record_assets_present'] and c['follow_up'] is None
 assert c['version']==c['source_binding']['zenodo_version']==c['source_binding']['manuscript_version']
 assert (p/'REVIEW.md').is_file()
 sha=hashlib.sha256((p/'content.json').read_bytes()).hexdigest();now=datetime.now(timezone.utc).isoformat();exposed=ident=='23088066'
 v=dict(record_id=ident,
  role='publication_scope_and_primary_literature_review_with_archived_support_exposure' if exposed else 'independent_publication_scope_and_primary_literature_review',
  timestamp_utc=now,completion_percent=100,scope_verdict='no_publication_scope_defect_identified',
  publication_disposition='candidate_content_only_pending_separate_mathematical_gates',mathematical_gate=False,novelty_certified=False,
  independent_human_peer_review=False,full_published_paper_read=True,published_paper_pages=s['main_pdf_pages'],published_supplement_pdfs=[],
  all_published_assets_acquired=True,source_integrity_pass=True,strict_archived_opinion_independence=not exposed,
  archived_review_opinion_exposure=exposed,archived_or_sibling_review_verdicts_used=False,current_sibling_mathematical_findings_consulted=False,
  independence_note=('The required published probability_derivation.md is also a historical independent audit and its PASS assessment was encountered before the own 60% conclusion. The PL supplement also includes a historical review-status sentence. Exposure was disclosed and not used as validation; strict opinion exclusion cannot be claimed. No current sibling mathematical findings or dedicated additional archived priority reports read.' if exposed else 'Own scope conclusion recorded at 60% without archived audit or sibling mathematical findings. Manuscript historical internal-review assertions were not used as validation. Current official notebook external confirmation was consulted only as primary bibliographic status, not as a substitute for proof checking.'),
  content_sha256=sha,source_binding=c['source_binding'],follow_up=None,followup_rationale=c['followup_rationale'],defects=[],key_boundaries=c['limitations'],
  primary_source_review_limitations=(['Original Janson 1990 body not directly acquired; actual author-hosted Frieze–Karoński theorem and proof inspected.', 'Bounded comparison is not an exhaustive novelty certification; not every page of every predecessor independently verified.'] if exposed else ['Historical September notebook and update URLs now return 404; historical absence-of-solution claim not directly certified.', 'Current official notebook reports P. J. Cameron confirmation, but no journal acceptance or underlying human review report was obtained.', 'Initial guessed Cameron2024 publisher URL fetched an unrelated article; receipt marked, correct article acquired separately and used.']))
 if not exposed:v['external_confirmation_reported_by_primary_source']=c['external_status']
 (p/'verdict.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 with (p/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — 100%\n\nSource-bound scope report, candidate content and verdict complete. All public assets and internal manifest entries pass. No scope defect identified; mathematical gates separate. Follow-up null. Content SHA-256 '+sha+'. '+('Historical support opinion exposure remains explicitly disclosed.' if exposed else 'Current official notebook external confirmation is documented separately from journal review; no archived/sibling mathematical opinions used.')+' No repairs or external mutations.\n')
 print(ident,sha)
