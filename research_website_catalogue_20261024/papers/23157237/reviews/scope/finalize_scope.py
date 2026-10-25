from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers')
notes={
 '23157237':{
 'reiss':'Full contribution, printed pp. 1507–1509: problem formulation and spectral reconstruction question.',
 'hansen-scheinkman':'Scanned printed pp. 26–27 visually inspected, particularly Proposition 5.5. Working-paper edition only.',
 'crommelin2006':'Original journal PDF: spectral residual and nonparametric/grid-fit construction.',
 'crommelin2011':'Author manuscript revised August 31, 2011: equation 4.7 eigenvalue-power weighting, sampling/discretization and nonparametric discussion; publisher-final body unavailable.',
 'nickl':'Model and consistency setting: scalar diffusivity/potential and normal reflection.',
 'giordano-wang':'Model and §1.3 anisotropic-extension discussion.',
 'alberti':'Lemma 3.8 and proof, spectral-cutoff gradient excitation and theorem completion.',
 'grubb':'Theorem 2.2 and Corollary 2.3 domain/elliptic-power interfaces.',
 'lenzen-scherzer':'Section 3, nonlinear forward-operator assumptions and Theorem 3.2.'},
 '22729355':{
 'satnoianu':'Abstract, subsystem endpoint and stability theorem/proof passages; bounded attribution comparison, not endorsement of every general theorem.',
 'anma':'Theorem 1.1 and remarks distinguishing stationary and wave instability.',
 'haas-goldstein':'Abstract, introduction and random-matrix setting.',
 'diego':'Abstract, introduction and graph/characteristic-polynomial framework.',
 'conradi':'Monomial steady-state framework, stationary theorem interface, nine-species example and numerical nonlinear conclusions.',
 'cross-diffusion':'Version 2, introduction and theorem interfaces for designed generally nondiagonal diffusion.',
 'crandall-rabinowitz':'Theorem 1.7 and beginning of proof: simple kernel/cokernel and transversality.'}}
for ident in ['23157237','22729355']:
 p=B/ident/'reviews/scope';c=json.loads((p/'content.json').read_text());s=json.loads((p/'source_integrity.json').read_text());spectral=ident=='23157237'
 assert s['passed'] and s['all_public_record_assets_present'] and c['follow_up'] is None and (p/'REVIEW.md').is_file()
 assert len(s['files'])==(2 if spectral else 8)
 assert [f['pages'] for f in s['published_pdfs']]==([8] if spectral else [19,19])
 assert c['version']==c['source_binding']['zenodo_version'] and c['source_binding']['printed_title_page_version'] is None
 assert c['source_binding']['manuscript_version']==(None if spectral else '1.0.11')
 assert len(c['additional_assets'])==(0 if spectral else 3)
 for a in c['additional_assets']:
  assert set(a)=={'filename','label','kind'} and a['filename'] in [f['filename'] for f in s['files']]
 refs=[]
 for name,note in notes[ident].items():
  r=json.loads((p/'primary-sources'/f'{name}.receipt.json').read_text())
  refs.append(dict(key=name,receipt=r,passages_inspected=note,scope='Primary interface/attribution comparison; not a full reproof.'))
 (p/'primary_sources.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False)+'\n')
 sha=hashlib.sha256((p/'content.json').read_bytes()).hexdigest();now=datetime.now(timezone.utc).isoformat()
 independence=('The required authored mathematical independent_classical_derivation.md also contains historical AI attack dispositions and a final verdict; these were encountered before the own scope checkpoint. SOURCE_EDITIONS.md also exposed historical priority-audit assertions. Strict archived-opinion exclusion is therefore false. None was used as correctness evidence, and no current sibling mathematical findings were consulted.' if spectral else 'Own scope conclusion recorded before current sibling mathematical findings; no dedicated archived audit/research-log/verdict body consulted. Authored manuscript and support verification-status assertions were not treated as validation.')
 limitations=(['Inspected relevant passages of primary predecessors rather than every page of every source; bounded comparison does not certify worldwide priority.','Crommelin–Vanden-Eijnden 2011 publisher-final body was not obtained; exact author/final edition identity is not assumed.','Classical elliptic regularity and inverse-problem convergence theorems are imported dependencies whose interfaces were inspected, not fully reproved.','Historical AI opinions in required authored support were incidentally exposed and explicitly excluded as evidence.'] if spectral else ['Inspected relevant primary-source interfaces rather than every page of every predecessor; bounded comparison does not certify worldwide priority.','Henry and Kato textbook frameworks were identified as substantive imports, but full books were not newly acquired or independently reproved.','The scope reviewer did not execute the full exact-certificate suite; checksum consistency and stored status claims are not mathematical gates.'])
 v=dict(record_id=ident,role='publication_scope_and_primary_literature_review_with_authored_audit_exposure' if spectral else 'independent_publication_scope_and_primary_literature_review',timestamp_utc=now,completion_percent=100,scope_verdict='no_publication_scope_defect_identified',publication_disposition='candidate_content_only_pending_separate_mathematical_gates',mathematical_gate=False,novelty_certified=False,independent_human_peer_review=False,full_published_paper_read=True,published_paper_pages=8 if spectral else 19,published_supplement_pdfs=[] if spectral else [{'filename':'Exact_Diffusion_Design_Supplement_v1.0.11.pdf','pages':19,'read_scope':'all pages'}],all_published_assets_acquired=True,source_integrity_pass=True,strict_archived_opinion_independence=not spectral,archived_review_opinion_exposure=spectral,archived_or_sibling_review_verdicts_used=False,current_sibling_mathematical_findings_consulted=False,independence_note=independence,content_sha256=sha,source_binding=c['source_binding'],follow_up=None,followup_rationale=c['followup_rationale'],defects=[],key_boundaries=c['limitations'],primary_source_review_limitations=limitations)
 (p/'verdict.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
 with (p/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — 100%\n\nScope report, primary-source inventory, source-integrity checks, candidate content and verdict complete. No publication-scope defect identified; mathematical gates remain separate. Follow-up null. Content SHA-256 '+sha+'. '+independence+' No repairs or external mutations.\n')
 (p/'.gitignore').write_text('page1.png\n')
 (p/'primary-sources/.gitignore').write_text('*.pdf\n*.txt\n*.png\n')
 print(ident,sha)
