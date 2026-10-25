from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22136869');p=P/'reviews/scope'
c=json.loads((p/'content.json').read_text());integrity=json.loads((p/'source_integrity.json').read_text())
assert integrity['passed'] and len(integrity['files'])==3 and integrity['extracted_files_identical']==48
assert integrity['internal_sha256_entries_verified']=={'manifest.sha256':45,'FILE_SHA256SUMS':46}
assert c['version']=='1.2.6' and c['source_binding']['manuscript_version']=='1.2.7' and c['source_binding']['printed_title_page_version'] is None
assert [x['pages'] for x in c['source_binding']['reviewed_documents']]==[20,2,2] and c['follow_up'] is None
for a in c['source_binding']['embedded_assets']:
 assert hashlib.sha256((P/'sources'/a['source_relative_path']).read_bytes()).hexdigest()==a['sha256']
hold='After the independent 60% scope conclusion and local 85% draft, the coordinating agent reported a potential mathematical defect in the page-12 forced-ratio assertion, awaiting independent adversarial confirmation. Candidate content is on hold and must not be promoted. This scope reviewer has not independently resolved that mathematical issue or attempted repair.'
c['publication_hold']={'active':True,'reason':hold,'disposition':'do_not_publish_pending_mathematical_defect_review'}
(p/'content.json').write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n')
refs=[]
notes={
 'brits-v2':'Theta0 restrictions, Lemma5.6 and Corollary5.8, appendix fixed-leaf-order induction setup; 32-page version2 PDF.',
 'brits-v3':'Theta0 restrictions, ordering discussion after Lemma5.5, JC-only Corollary5.7 and §6 high-level Kimura open questions; 30-page version3 PDF.',
 'ardiyansyah':'Section3.4 nice/funnel-free definitions, Lemma3.8 and Lemma5.1 excluding nice strict-level-two trinets; 35-page version1 PDF.',
 'englander-v4':'Strong tree-child definition, generic identifiability interface, Theorem3.2 and its proof; 31-page PDF posted July4,2026 with internal July3 date.'}
for key,note in notes.items():
 r=json.loads((p/'primary-sources'/f'{key}.receipt.json').read_text());refs.append(dict(key=key,receipt=r,passages_inspected=note,limitation='Bounded primary-interface review, not every page or independent reproof.'))
(p/'primary_sources.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat();sha=hashlib.sha256((p/'content.json').read_bytes()).hexdigest()
editorial={'severity':'minor_editorial_non_load_bearing','location':'Main manuscript §12 item5, PDF page18','observation':'The JC future-work item is already answered within the stated Theta0 model by cited Brits et al. v3 Corollary5.7; a different chamber would need specification. The main paper elsewhere correctly excludes any JC counterexample.','evidence':'Original §12 item5 compared directly with fresh primary v3 Corollary5.7 and §6; see REVIEW.md.','action':'Recorded for later attention; omitted from public follow-ups; no source repair.'}
v=dict(record_id='22136869',role='independent_publication_scope_and_primary_literature_review',timestamp_utc=now,completion_percent=100,scope_verdict='no_substantive_publication_scope_defect_identified',publication_disposition='on_hold_pending_reported_mathematical_defect_review',publication_hold=True,mathematical_gate=False,novelty_certified=False,independent_human_peer_review=False,full_published_paper_read=True,published_paper_pages=20,published_supplement_pdfs=c['source_binding']['reviewed_documents'][1:],all_published_assets_acquired=True,source_integrity_pass=True,strict_archived_opinion_independence=True,archived_review_opinion_exposure=False,archived_or_sibling_review_verdicts_used=False,current_sibling_mathematical_findings_consulted_before_own_scope_conclusion=False,current_sibling_findings_received_after_own_scope_conclusion=True,independence_note='Own scope conclusion logged at60% before any current sibling findings. Authored manuscript/supplement status and acknowledgment claims were encountered but not used as validation. No dedicated archived disposition, research log or saved verification-report bodies consulted. After85% draft, coordinator reported an independently reviewed page12 issue; it is recorded solely to hold publication, not as support for the earlier scope conclusion.',post_conclusion_math_gate_note=hold,content_sha256=sha,source_binding=c['source_binding'],follow_up=None,followup_rationale=c['followup_rationale'],defects=[editorial],key_boundaries=c['limitations'],primary_source_review_limitations=['Relevant passages of four primary papers/editions inspected; this is not an exhaustive worldwide novelty search.','Classical Fourier, implicit-function, constant-rank and preimage results are external tools, not independently reproved by this scope reviewer.','The full exact-verifier suite was not executed by the scope reviewer; independent mathematical gates own those checks.','The mathematical validity of the page12 forced-ratio assertion was not certified by this scope review; reported concern keeps all candidate publication on hold.'])
(p/'verdict.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
with (p/'REVIEW.md').open('a') as f:f.write('\n## Post-conclusion publication hold\n\n'+hold+' The earlier scope conclusion is preserved with its timestamp; it is not an approval to publish. All embedded-reader provenance and source hashes are retained for later disposition.\n')
with (p/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — 100%\n\nScope/evidence assignment completed. Source integrity, full24-page reader coverage, exact abstract, edition boundary and primary comparison preserved. Candidate content SHA-256 '+sha+'. '+hold+' No site, renderer, asset staging, Git, sheet, publishing or outreach changes.\n')
(p/'.gitignore').write_text('page1.png\n');(p/'primary-sources/.gitignore').write_text('*.pdf\n*.txt\n*.png\n')
print('22136869',sha,'publication hold active')
