"""Pure PR195 native presentation constructor. No remote or filesystem writes.
Actual publication/tracker/merge facts must be authenticated by Root first.
Historical original23 files are separately retained in original_submitted_head.
"""
from pathlib import Path
import hashlib,json
A=Path(__file__).resolve().parent.parent
NATIVE='unsolved_math_prioritization/attempts/30004601/'
CASE='draft_pr_publication_program_20260930/audits/pr195_30004601/'
ORIGINAL='e776a961293116775fed2cb2a3019d577b84c04a'
STAGES={'published_pending_merge','actual_merge_accepted','factual_checkpoint_accepted'}
PRESERVED={'candidate_rank_check.py','candidate_rank_check_output.json','adversarial_controls.py','adversarial_controls_output.json','independent_review/INDEPENDENT_CHECKS.json','independent_review/INDEPENDENT_REVIEW.md','independent_review/RANK_CERTIFICATES.json','independent_review/REVIEW_SHA256SUMS','independent_review/independent_rank_certificate.py','sources/.gitignore','sources/prior_report_30004601.json','sources/source_record_30004601.json'}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def originals():
    j=json.loads((A/'ORIGINAL_SUBMISSION_CUSTODY.json').read_bytes())
    assert j['original_head']==ORIGINAL and len(j['files'])==23
    out={}
    for n,pin in j['files'].items():
        p=A/'original_submitted_head'/n;b=p.read_bytes()
        assert p.is_file() and not p.is_symlink() and p.stat().st_mode&0o777==0o444
        assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==pin['git_blob']
        out[n]=b
    return out
def construct(stage,f):
    assert stage in STAGES and f['publication_ready_gate_accepted'] is True
    assert f['DOI']=='10.5281/zenodo.'+str(f['record_id']) and f['record_id']>0
    assert f['actual_publication_verified'] is True and f['actual_tracker_row_verified'] is True
    assert f['package']=='publication_package_v2' and len(f['whole_package_review_events'])>=2
    assert f['historical_priority_established'] is False
    if stage!='published_pending_merge':
        assert f['actual_merge_receipt']['accepted'] is True and f['actual_merge_receipt']['original_head']==ORIGINAL
    if stage=='factual_checkpoint_accepted':assert f['actual_factual_receipt']['accepted'] is True
    old=originals();out=dict(old);doi='https://doi.org/'+f['DOI'];paper=CASE+f['package']+'/seven_plane_gin.pdf'
    state={'published_pending_merge':'Preprint published and tracker verified; original-HEAD-safe merge pending.','actual_merge_accepted':'Original-HEAD-safe merge actually accepted; factual completion checkpoint pending.','factual_checkpoint_accepted':'Published, tracked, original-HEAD-safe merged; factual completion checkpoint actually accepted.'}[stage]
    text=f'''# 30004601: verified seven-hyperplane counterexample

{state}

Preprint: [{f['DOI']}]({doi}). Author: Alec Kriebel, independent researcher, ORCID 0009-0001-9320-500X. The note is unrefereed, developed with extensive AI assistance, and has not undergone conventional human peer review.

For `Q=xy(x-y)(x-2y)zw(x+z+w)` in characteristic zero, the revlex generic initial ideal of the ambient Jacobian has pure-second-variable cutoff 8 and a degree 7 minimal generator in the first three variables divisible by the third. The proof establishes dimensions on a nonempty open set; it does not infer genericity from sampled ranks. Four ambient partial derivatives are computed before restricting. This respects the prior three-variable arrangement theorem.

The original conjecture uses the second variable. `SOURCE_NORMALIZATION.json` gives the current source-checked statement. `sources/source_record_30004601.json` retains dated upstream metadata with the first-variable transcription error; it is not the current statement or a current world-openness assessment.

The arrangement is a classical parallel connection. The logarithmic/polar, Hilbert–Burch and generic-sectional tools are prior. Migliore–Nagel's applicable resolution concerns the distinct five-generated unmixed part. The explicit calculation is verified; historical novelty, firstness and independent discovery remain unestablished. Ilardi (2018) full text was not obtained. See `QUALIFIED_PRIORITY.md`.

The authoritative standalone note and verification ZIP are in [{f['package']}](../../../{CASE}{f['package']}/). The package includes five standard-library exact replayers and nineteen bounded earlier-example comparisons. Three new distinct mathematical review families and successive fresh whole-package reviews are documented in the publication audit folder. Review01 assessed v1; the manuscript/PDF were unchanged in v2, which added two exact predecessor comparisons and cosmetic README corrections; review02 assessed the full v2.

`CANDIDATE_PROOF.md` has current status/attribution annotations. The exact original reviewed copy, all 23 original submitted files and historical manifests remain in `../../../{CASE}original_submitted_head/`. Old candidate/recovery/review records are dated history. Preserved author/independent scripts and certificates retain their original bytes; use the current package's Python 3.11+ no-write commands for the full scientific replay.

Historical consumed author turns remain unknown and nonzero; one recovered substantive author turn is documented. Audit, verification and publication work do not reset or fabricate that history. Current factual receipts are recorded in `PUBLICATION_STATUS.json`.
'''
    out['README.md']=text.encode()
    proof=old['CANDIDATE_PROOF.md'].decode();start='**Status:** complete candidate found in recovered substantive turn 1; independent adversarial review pending. No correctness, novelty, priority, or publication claim is made before that review.'
    assert proof.count(start)==1
    proof=proof.replace(start,'**Current status (15 October 2026):** mathematical counterexample verified by new independent audits; published as a qualified unrefereed research note. '+state+' Historical priority is unresolved. The original pending-review candidate is preserved byte-for-byte in the publication audit archive; this copy updates status and attribution without changing its mathematical argument.')
    sentence='The new candidate contribution is this explicit arrangement and the scalar-syzygy obstruction to the proposed bound.'
    assert proof.count(sentence)==1
    proof=proof.replace(sentence,'The verified result recorded here is the explicit generic-sectional calculation and its violation of the bound. The arrangement is an instance of the classical Falk–Proudfoot parallel connection; the logarithmic/polar mechanism and other proof tools are prior. Migliore–Nagel (2025) also gives applicable family data for the distinct unmixed ideal. No novelty of the arrangement, method or historical priority is asserted; see QUALIFIED_PRIORITY.md and the published note.')
    out['CANDIDATE_PROOF.md']=proof.encode()
    current={'UTC':f['UTC'],'problem_id':30004601,'original_head':ORIGINAL,'status':stage,'state':state,'mathematical_result_valid':True,'exact_result':'Characteristic-zero Q=xy(x-y)(x-2y)zw(x+z+w): pure-second-variable revlex-gin cutoff 8, degree 7 minimal generator with largest index3.','historical_priority_established':False,'human_peer_review':False,'extensive_AI_use':True,'DOI':f['DOI'],'Zenodo_record_id':f['record_id'],'actual_publication_verified':True,'tracker_range':f['tracker_range'],'actual_tracker_row_verified':True,'publication_package':CASE+f['package'],'publication_gate':CASE+'ROOT_PUBLICATION_GATE_01.json','publication_receipt':CASE+'ROOT_PUBLICATION_RECEIPT.json','tracker_receipt':CASE+'ROOT_TRACKER_RECEIPT.json','whole_package_review_events':f['whole_package_review_events'],'original_author_effort':'prior unknown; 1 recovered','actual_merge_receipt':f.get('actual_merge_receipt'),'actual_factual_receipt':f.get('actual_factual_receipt')}
    out['PUBLICATION_STATUS.json']=enc(current)
    review=json.loads(old['REVIEW_STATUS.json']);out['REVIEW_STATUS.json']=enc({**current,'historical_original_submission_review':review,'current_proof_annotations_change_math':False})
    ready=json.loads(old['readiness.json']);out['readiness.json']=enc({**current,'historical_original_submission_readiness':ready,'review_loop_complete':True,'publication_ready':True,'scope':'Publication readiness is for this fully credited qualified note, not certification of historical firstness.'})
    ledger=json.loads(old['turns.json']);assert ledger['historical_consumed_turns'] is None and ledger['recovered_substantive_author_turns']==1
    ledger.update(current_publication_status=stage,current_DOI=f['DOI'],current_mathematical_audit_accepted=True,current_historical_priority_established=False,dated_turn_records_are_historical=True,review_or_publication_work_not_counted_as_recovered_proof_search=True)
    out['turns.json']=enc(ledger)
    manifest=json.loads(old['FROZEN_REVIEW_MANIFEST.json']);manifest.update(scope='Historical original frozen snapshot only. File hashes refer to the separately preserved original_submitted_head copies, not later annotated current files.',original_submission_archive=CASE+'original_submitted_head/',current_status_file='PUBLICATION_STATUS.json');out['FROZEN_REVIEW_MANIFEST.json']=enc(manifest)
    qualified=f'''# Qualified historical-priority statement

{f['UTC']} — Mathematical verification and publication are distinct from historical firstness. The exact proof resolves the correctly transcribed general-dimensional conjecture by counterexample, while novelty and independent discovery remain unestablished.

Credit: Bigatti–Palezzato–Torielli's Conjecture 5.7, the Palezzato–Torielli/OWR lineage, and Marchesi–Palezzato–Torielli's valid three-variable theorem; Falk–Proudfoot's classical parallel-connection construction; the classical logarithmic, Hilbert–Burch, strong-stability and generic-sectional methods; Migliore–Nagel (2025) Corollary 8.12's applicable resolution of the distinct five-generated unmixed Jacobian part.

The bounded 15 October 2026 audit contains 36 primary-source records and 120 targeted queries. Exact comparisons exclude 3 PT examples, 14 rigid octics and 2 specific nine-factor examples as earlier refutations of this bound. These are nineteen checked examples, not an exhaustive classification. No complete predecessor was identified in the inspected corpus.

Ilardi (2018), DOI 10.1016/j.jalgebra.2018.04.029, remains a material full-text access gap; publisher retrieval failed/reached a CAPTCHA and the institutional postprint was restricted. Its possible overlap is unexcluded. The 63 octic parameter families, Boolean extensions, other related examples, full nine-factor gins, historical code/coordinate families and earliest public-disclosure chronology were not exhausted or certified. Negative searches are not proofs of absence. The two newly excluded nine-factor base examples have cutoff 10 and zero earlier third-truncation kernels; computing full gins was unnecessary for that limited exclusion.

This work used AI extensively and is unrefereed, with no conventional human peer review. The original candidate's phrase about a new arrangement/method is superseded by these credits and the precise qualified note. The checked preprint and exact package are available at {doi}.
'''
    out['QUALIFIED_PRIORITY.md']=qualified.encode()
    for n in ['SOURCE_AUDIT.md','SOURCE_METADATA_ADDENDUM.md']:
        out[n]=old[n]+('\n\n## Current dated qualification, 15 October 2026\n\n'+qualified+'\n').encode()
    note=f'\n\n## {f["UTC"]} — Current publication checkpoint\n\n{state} Preprint {doi}; tracker {f["tracker_range"]}. The mathematical proof survived three new distinct audit families and the successive fresh whole-package process. Historical priority remains unresolved; the classical construction/method/family overlap and material access gaps are credited in QUALIFIED_PRIORITY.md. Current proof annotations update status and attribution only. The original 23 submitted files and their original frozen hashes remain archived separately. Historical author effort remains unknown/nonzero plus one recovered substantive turn. Estimate: mathematical validation 100%; full PR publication workflow '+('100% after actual factual checkpoint acceptance.' if stage=='factual_checkpoint_accepted' else '95%, with actual integration/factual acceptance still required.')+'\n'
    for n in ['RESEARCH_LOG.md','POST_REVIEW_LOG.md','PACKAGE_SCOPE.md']:out[n]=old[n]+note.encode()
    raw_source=json.loads(old['sources/source_record_30004601.json']);assert raw_source['id']==30004601
    out['SOURCE_NORMALIZATION.json']=enc({'UTC':f['UTC'],'id':30004601,'historical_source_record':'sources/source_record_30004601.json','historical_upstream_status_and_original_statement_preserved':True,'historical_upstream_statement_contains_first_variable_transcription_error':True,'current_verified_statement':'For a central hyperplane arrangement over a characteristic-zero field, let B be the degree-reverse-lexicographic generic initial ideal of its Jacobian and p=min{d:x2^d in B}. Must every minimal generator involving x3 have degree at least p?','original_primary_source':'https://ems.press/content/serial-article-files/46883 printed p.234, Conj7','BPT_notation':'Conj 5.7 uses d0 with x2^(d0+1); p=d0+1.','current_mathematical_resolution':'Explicit four-dimensional seven-hyperplane counterexample: p8, degree 7 witness in first three variables involving third.','source_correction_not_a_discovery':True,'prior_three_variable_theorem_credited':True,'historical_priority_established':False,'DOI':f['DOI']})
    assert set(out)==set(old)|{'PUBLICATION_STATUS.json','QUALIFIED_PRIORITY.md','SOURCE_NORMALIZATION.json'}
    for n in PRESERVED:assert out[n]==old[n]
    assert len(PRESERVED)==12 and len(out)==26
    return {NATIVE+n:b for n,b in out.items()}
