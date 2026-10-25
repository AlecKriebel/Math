from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, zipfile, zlib, re
P=Path(__file__).resolve().parents[2]
R=P/'reviews/scope'
S=P/'sources'
now=datetime.now(timezone.utc).isoformat()
receipt=json.loads((S/'receipt.json').read_text())
record=json.loads((S/'record.json').read_text())
extraction=json.loads((S/'extraction-integrity.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj): (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
files=[]
for entry in receipt['files']:
 p=S/entry['name']; data=p.read_bytes()
 out={**entry,'actual_bytes':len(data),'actual_md5':hashlib.md5(data).hexdigest(),'actual_sha256':hashlib.sha256(data).hexdigest()}
 out['unchanged']=out['actual_bytes']==entry['bytes'] and out['actual_md5']==entry['md5'] and out['actual_sha256']==entry['sha256']
 assert out['unchanged']
 files.append(out)
memberchecks=[]
with zipfile.ZipFile(S/'odd_power_sos_verification.zip') as z:
 for e in extraction['members']:
  raw=z.read(e['path']); p=S/'published-source'/e['path']
  item={'path':e['path'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'crc32':f'{zlib.crc32(raw)&0xffffffff:08x}','extracted_sha256':sha(p)}
  item['unchanged']=item['bytes']==e['bytes'] and item['sha256']==e['sha256']==item['extracted_sha256'] and item['crc32']==e['crc32']
  assert item['unchanged']; memberchecks.append(item)
assert sha(S/'record.json')==receipt['record_sha256']
source_integrity={'checked_utc':now,'completion_percent':100,'scope':'File identity and completeness only; not mathematical verification.','all_public_files_unchanged':True,'all_extracted_members_unchanged':True,'record_sha256':sha(S/'record.json'),'record_unchanged':True,'files':files,'members':memberchecks,'additional_reader_pdfs':[],'verifier_run_by_this_reviewer':False}
dump('final_source_verification.json',source_integrity)
read_scopes={
 'bkr-published.pdf':'Published version: definitions/introduction pp.2–4; Theorem 5.3 and proof pp.22–23; §6 fixed-power question, modified Motzkin family and explicit cube identity pp.23–24. Not the complete article.',
 'owr2023-14.pdf':'Complete Reznick contribution, printed pp.778–781, including references; not the complete multi-author workshop report.',
 'bcj1979.pdf':'Entire original article, printed pp.163–169, visually read from scan pages 2–8. Lemma 1 and Theorems 3–4 are the exact interfaces.',
 'rounding2013.pdf':'Appendix A definition A.1 and Lemma A.5 with its complete proof. Not the complete ECCC report.',
 'powermean-v1.pdf':'Monomial-mean definitions and Lemma 2.1 with proof, pp.5–6. Not the complete preprint.',
 'symmetric-v4.pdf':'Proposition 6.4 and its proof, p.22, with the immediately needed basis notation. Not the complete preprint.',
 'stubborn-v1.pdf':'Definition 2.1, Theorem 2.2 and complete proof, pp.3–5. Not the complete preprint.'}
prim=json.loads((R/'cache/primary-sources/receipt.json').read_text())
for e in prim:
 e['local_path']=str(R/'cache/primary-sources'/e['name'])
 assert sha(Path(e['local_path']))==e['sha256']
 e['read_scope']=read_scopes[e['name']]
dump('primary_sources.json',{'completed_utc':now,'completion_percent':100,'sources':prim,'search_scope':'Bounded primary-source and targeted title/phrase search only. The source-authored historical audit was not adopted; PRIORITY_NOTE.md remained unopened. No exhaustive or worldwide-firstness conclusion.','unresolved_priority_boundary':'This review does not inspect all historical literature or establish the current status of every small-dimensional fixed-power problem.'})
abstract='For a fixed odd integer q, consider the nonnegative real homogeneous forms whose qth powers are sums of squares. We give a negative answer to the general-dimensional convexity question recorded by Reznick in 2023. For sextics and q = 3, the cone is nonconvex in the explicit finite dimension 3 · 10^62. For every odd q ≥ 3, it is nonconvex in some finite dimension depending on q. The proof combines a classical modified Motzkin form with an SOS cube, separation from the SOS cone, positivity of product truncated functionals, and elementary distinct-index counting. An explicit rational moment functional gives the displayed dimension; its 220 × 220 local positivity certificate can be checked without floating-point arithmetic. No ternary or smallest-dimension conclusion is made.'
followup='No follow-up is proposed. Reducing the dimension or settling the ternary case would be substantial, but the paper and this review provide no distinct, well-supported new mechanism or carefully delimited conjecture beyond those obvious unresolved boundaries. Listing them as a new research proposal would not meet the requested high bar.'
content={
 'title':'Nonconvexity of fixed odd-power sum-of-squares cones',
 'slug':'fixed-odd-power-sos-nonconvexity',
 'description':'Fixed odd-power sum-of-squares cones can fail to be convex: a sextic cube example uses 3 · 10^62 variables, with an extension to every odd exponent at least three.',
 'abstract':abstract,
 'plain_language':[
  'A sum of squares is a particularly transparent way to show that a polynomial is never negative. Some nonnegative polynomials do not have such a representation themselves, but their cubes do. This paper asks whether averaging polynomials with that property preserves it.',
  'The result is that it can fail. The construction takes many separate copies of one classical polynomial, each with a sum-of-squares cube. Their average remains nonnegative, yet its cube cannot be written as a sum of squares. The displayed example uses 3 · 10^62 variables: a finite existence result, not a small or practical example.',
  'The same obstruction works for every fixed odd exponent at least three, in a finite number of variables that may depend on the exponent. Keeping the exponent fixed is essential. Earlier convexity results allow a larger odd power after the polynomials are added.',
  'The classical polynomial and its sum-of-squares cube come from earlier work. This note uses them with established separation and product arguments to address the general convexity question recorded by Reznick in 2023. It does not settle the three-variable case or claim a verified first resolution.'
 ],
 'result':[
  'For real homogeneous forms f of positive even degree m, let C(n,m,q) consist of those that are nonnegative on R^n and whose fixed positive odd qth power is a finite sum of squares of real polynomials. Nonnegativity follows automatically from the power condition when q is odd. These sets are closed and stable under nonnegative scaling; addition is the issue under investigation.',
  'Put N = 10^62 and use N disjoint triples of variables. For each triple define p_i = x_i^4 y_i^2 + x_i^2 y_i^4 + z_i^6 − x_i^2 y_i^2 z_i^2. Each p_i belongs to C(3N,6,3), but N^−1 times their sum does not. Thus C(3 · 10^62,6,3) is nonconvex.',
  'For every fixed odd q ≥ 3, there is a finite n(q) for which C(n(q),6,q) is nonconvex. The construction may use a different separating functional and a different number of variable blocks for each q. Each counterexample also persists after adding unused variables.',
  'For q = 3, the paper supplies a rational linear functional on polynomials of degree at most 18 in three variables. Its order-nine moment matrix has 220 monomials and splits into eight parity blocks. The accompanying archive contains the manuscript source, the exact local certificate and a standalone rational-arithmetic checker.'
 ],
 'limitations':[
  'The explicit number of variables is a sufficient bound, with no claim of optimality. The theorem does not prove nonconvexity for three variables, for a prescribed small dimension, or in one common dimension that works for all odd exponents.',
  'The result concerns sextics and a prescribed odd exponent. It is not a classification of all degrees, dimensions and exponents. The ordinary sum-of-squares cone at q = 1 remains convex.',
  'Failure at one odd power does not say that every odd power fails. The established convexity of the union over odd exponents is consistent with the result, and no stubbornness claim is made for the constructed average.',
  'The separating functional is positive on squares within its specified degree range. It is not integration against a positive measure: it assigns a negative value to a nonnegative polynomial. The enormous product matrix is handled by a finite algebraic argument, not materialized numerically.',
  'The seed, its cube identity, SOS separation, product positivity and distinct-index counting have earlier sources. The contribution is their application to a fixed-exponent obstruction and the explicit finite cube certificate. The bounded literature comparison does not establish worldwide priority.'
 ],
 'background':[
  {'title':'Reznick, The Odd Powers of the Motzkin Polynomial, etc. (2023)','url':'https://doi.org/10.4171/OWR/2023/14','note':'The contribution on pp.778–781 records the general fixed-odd-power convexity question and the modified Motzkin cube example. The fixed-power question appears on p.779.'},
  {'title':'Blekherman, Kozhasov and Reznick, On odd powers of nonnegative polynomials that are not sums of squares (2026)','url':'https://doi.org/10.1017/fms.2026.10221','note':'Theorem 5.3 proves convexity when the odd exponent may increase. Section 6 repeats the fixed-exponent question and gives the credited cube identity for the modified Motzkin family.'},
  {'title':'Berg, Christensen and Jensen, A remark on the multidimensional moment problem (1979)','url':'https://doi.org/10.1007/BF01420423','note':'Lemma 1 gives exactly the dehomogenized coefficient-1 seed used here. Theorems 3–4 provide classical closure and positive-functional separation results.'},
  {'title':'Barak, Kelner and Steurer, Rounding Sum-of-Squares Relaxations (2013)','url':'https://eccc.weizmann.ac.il/report/2013/184/','note':'Appendix A, Lemma A.5, proves the established product-positivity property for truncated pseudoexpectations used by the disjoint-copy argument.'},
  {'title':'Acevedo and Blekherman, Power Mean Inequalities and Sums of Squares, v1 (2023)','url':'https://arxiv.org/abs/2303.11823v1','note':'Lemma 2.1 is a precedent for separating the leading contribution of distinct indices from lower-order collisions.'},
  {'title':'Blekherman and Riener, Symmetric Nonnegative Forms and Sums of Squares, v4 (2020)','url':'https://arxiv.org/abs/1205.3102v4','note':'Proposition 6.4 provides another related distinct-index asymptotic argument. It is credited as an ingredient, not as the fixed-power nonconvexity theorem.'},
  {'title':'Baldi, Blekherman, Kozhasov, Plaumann, Reznick and Sinn, Stubborn Polynomials, v1 (2026)','url':'https://arxiv.org/abs/2602.01191v1','note':'Theorem 2.2 establishes convexity of the nonstubborn cone by allowing the odd exponent to increase; this is a different statement from fixed-power convexity.'}
 ],
 'collaboration':'I welcome substantive collaboration on an independent review of the fixed-exponent obstruction, its rational moment certificate, the precise relationship to earlier sum-of-squares results, or preparation for journal submission. Expertise in real algebraic geometry and polynomial positivity would be especially useful.',
 'follow_up':None,'followup_rationale':followup,
 'publication_date':'2026-10-06','version':'1.0','doi':'10.5281/zenodo.23191301','author':'Alec Kriebel',
 'pdf_filename':'odd_power_sos_nonconvexity.pdf','supplement_filename':'odd_power_sos_verification.zip','additional_assets':[],
 'why_it_works':[
  'Start with the classical coefficient-1 modified Motzkin sextic p. It is nonnegative and not itself a sum of squares, while its cube has an explicit sum-of-squares identity. Multiplying that identity by the square of p^((q−3)/2) supplies an SOS representation at every odd q ≥ 3.',
  'For a chosen exponent q, separate p from the finite-degree sum-of-squares cone. This gives a normalized linear functional L that is nonnegative on the necessary squares but has L(p) < 0. Taking finite products of this functional preserves positivity on squares involving separate variable blocks.',
  'When the qth power of a sum of many disjoint copies is expanded, terms using q different copies give the leading contribution. Their coefficient is L(p)^q, which is negative because q is odd. Terms that repeat a copy grow at a lower rate, so the product functional eventually assigns a negative value to the entire power. That excludes every sum-of-squares representation.',
  'For the cube, a displayed rational moment table makes the argument finite and explicit. With L(p) = −1 and the specified second and third moments, the resulting cubic expression is negative at N = 10^62. The local positivity certificate and the written product argument play separate roles.'
 ],
 'status':'Unrefereed preprint, version 1.0, developed with extensive AI assistance. No completed human peer review or formal proof-assistant verification is claimed; independent specialist review is welcome.',
 'ai_disclosure':'AI tools were used extensively in derivation, literature comparison, reproduction, writing and adversarial verification. The manuscript identifies itself as unrefereed and without human peer review. Its mathematical and source claims remain open to independent correction.',
 'source_binding':{
  'record_id':'23191301','concept_record_id':'23191300','record_url':'https://zenodo.org/records/23191301','doi':'10.5281/zenodo.23191301','version':'1.0',
  'zenodo_publication_date':'2026-10-06','manuscript_date':'2026-10-06','printed_edition':'6 October 2026; no version number printed in the manuscript. Version 1.0 is the Zenodo metadata value.',
  'source_retrieved_utc':receipt['retrieved_utc'],'pdf_sha256':receipt['files'][0]['sha256'],'supplement_sha256':receipt['files'][1]['sha256'],'files':receipt['files'],
  'reviewed_documents':[{'filename':'odd_power_sos_nonconvexity.pdf','pages':6,'read_scope':'all six pages, with complete paper.tex cross-check and visual inspection of printed p.3'}],
  'support_read_scope':'Complete paper.tex, verification/check_certificate.py and verify_package.py; mathematical moment/initial-block/Schur certificate data; README, CLAIM_SCOPE, SOURCE_VERSIONS and PROVENANCE for scope/provenance only. Dedicated PRIORITY_NOTE.md and expected_output.json were not read. No verifier was run by this scope reviewer.',
  'abstract_source':'Complete original published p.1 abstract, cross-checked against the complete abstract in paper.tex. Only whitespace and mathematical typography normalized; no disclosure or new prose appended.',
  'archive_pdf_identity':'There is no PDF inside the verification archive and no separate reader PDF. The public main PDF is the sole published reader.',
  'review_boundary':'Independent scope and bounded primary-literature review only, completed before any sibling mathematical conclusions. Candidate content remains subject to separate analytic and adversarial gates. No mathematical PASS or exhaustive novelty certification.'
 },
 'review_metadata':{'prepared_utc':now,'completion_percent':100,'disposition':'candidate_content_only_pending_separate_mathematical_gates'}
}
dump('content.json',content)
review=f'''# Independent scope and primary-literature review — Zenodo 23191301

Completed: {now}  
Completion: 100% of the assigned acquisition/scope/content review. This is not a mathematical gate.

## Conclusion

No publication-scope or attribution defect was identified at the exact stated scope. The candidate page is suitable for consideration **only after the independent analytic and adversarial gates**. The important claim is fixed-exponent nonconvexity for real homogeneous sextics: an explicit cube example in 3 · 10^62 variables and an existence statement in some finite n(q) for each odd q ≥ 3. It is neither a ternary result nor a uniform-in-q dimension theorem. No worldwide-firstness claim is justified by this bounded review.

The most interesting point is that separate copies of one classical polynomial each have an SOS cube, but their average eventually does not. This is compatible with the known convexity of the union over odd exponents because that earlier statement increases the exponent.

## Published edition and complete coverage

The reviewed bytes are the freshly acquired public record 23191301, concept 23191300, DOI 10.5281/zenodo.23191301. Zenodo reports version 1.0 and publication date 2026-10-06; the six-page manuscript prints “6 October 2026” without a version number. These are separate metadata facts, not an inferred printed edition. The public API record was retrieved at {receipt['retrieved_utc']}.

- odd_power_sos_nonconvexity.pdf: 92,284 bytes; SHA-256 {receipt['files'][0]['sha256']}.
- odd_power_sos_verification.zip: 28,376 bytes; SHA-256 {receipt['files'][1]['sha256']}.

Both files match the live MD5 and size, the inventory hashes and final local hashes. All 13 safe ZIP members match the archive CRC and original SHA-256 after review. No extra or embedded reader PDF exists. Original assets and extracted sources are unchanged. Receipts, extraction map and reader map remain under sources/; final recheck is final_source_verification.json.

Read all six actual PDF pages and complete paper.tex. Printed p.1 gives the exact cone and theorem; p.2 gives the finite product/partition obstruction and begins separation; p.3 completes separation, gives the exact classical seed and moment table; p.4 gives the local Schur certificate and finite cubic calculation; p.5 completes the sign, limits and disclosure and begins the credited cube identity; p.6 completes the identity and bibliography. The p.3 visual check confirms that the two large degree-six moments are 2^24, not the plain-text extraction's ambiguous “224”.

Complete verifier source was inspected, together with the moment table, initial blocks and all Schur-extension certificate fields. **This scope reviewer did not run either verifier and makes no mathematical PASS claim.** Authored expected output and historical check totals are not evidence of a fresh run. Analytic positivity, exact arithmetic reproduction, falsification controls and mathematical promotion remain the separate reviewers' responsibilities.

## Exact hypotheses and boundaries

C(n,m,q) uses real homogeneous forms, positive even m and positive odd q; SOS means a finite sum of squares of real polynomials. For odd q, f^q being SOS already implies f ≥ 0. “Cone” means closed and nonnegatively scaling-stable here, not an assumption of addition or convexity. In this paper n counts variables, not the dimension of the coefficient vector space.

The seed is p = x^4 y^2 + x^2 y^4 + z^6 − x^2 y^2 z^2, with coefficient 1 on the negative term. It is not the coefficient-3 original Motzkin polynomial, whose stubbornness is discussed in the primary literature. Each disjoint copy has an SOS cube by a credited identity, and p^q = p^3 (p^((q−3)/2))^2 extends membership to all odd q ≥ 3.

For each fixed q the proof selects a separating functional through degree qm = 2d, positive on squares of degree at most d and negative on p. Its finite product is positive on the required global squares because the total-degree moment matrix is a principal submatrix of a tensor product. Expansion over set partitions has leading term L(p)^q s^q < 0; collisions have lower degree. This is an analytic claim for arbitrarily large but finite s, not an infinite product measure or a numerical enormous-matrix computation. Degree-bounded square summands suffice because their highest homogeneous sums of squares cannot cancel.

The cube certificate is local to three variables through degree 18. Its 220 monomials split into eight parity blocks. The supplied table sets L(p) = −1, L(p²) = 11292 · 10^53 and L(p³) = 35039520 · 10^116. The stated cubic formula and bound give a negative value at N = 10^62 if the local positivity certificate is established. The q-general proof obtains a fresh functional rather than extrapolating this degree-18 table outside its domain.

A finite average outside a cone disproves convexity. The least-failing-prefix comment only gives existence of a violating pair in the same ambient space; it does not assign an SOS power to any prescribed untested prefix. Positive scaling transfers the sum obstruction to the average. Adding unused variables preserves the obstruction by restriction.

Explicit limits retained in content.json: no ternary theorem; no minimum or small prescribed dimension; no common dimension for all q; no full degree/dimension/exponent classification; no failure of closedness; no claim that every odd power of the average fails. The separating functional cannot be integration against a positive measure because p is nonnegative but L(p) is negative.

## Primary-source interfaces and credit

Fresh source receipts and exact reading extents are in primary_sources.json. Seven primary PDFs were acquired directly from their publishers, institutional archive or official arXiv versions. No third-party summary substitutes for the following interfaces.

1. **Reznick, OWR 14/2023, printed pp.778–781:** the entire contribution was read. Page 779 asks about the closed/convex property of the fixed-odd-power sets. This supports attribution to the question recorded in 2023, not a certificate that every subcase remained open at the time of this review. The contribution also records the modified Motzkin cube phenomenon.
2. **Blekherman–Kozhasov–Reznick, published Forum of Mathematics, Sigma 14 (2026), e65:** definitions and relevant introduction, Theorem 5.3 with proof, and §6 through the displayed cube formula were read. Theorem 5.3 takes exponents k and k̃ to k + k̃ − 1 for a sum; its convex union conclusion does not preserve a fixed q. Section 6 separately repeats the fixed-power question. The displayed identity specializes at a = 1 to the paper's seed cube, so this ingredient is credited rather than new.
3. **Berg–Christensen–Jensen (1979):** the entire seven-page original article was read visually from the digitized scan. Lemma 1 is exactly x²y²(x² + y² − 1) + 1, the seed dehomogenized at z = 1. Theorems 3–4 prove SOS closure and separation by a positive-on-squares functional that is not a moment functional. The new manuscript includes a finite-degree proof; it does not need to claim that classical duality is new.
4. **Barak–Kelner–Steurer, ECCC TR13-184 (2013):** Appendix A definition A.1 and Lemma A.5 with proof were read. A normalized truncated functional positive on squares has exactly the needed pseudoexpectation convention. Products preserve the relevant positivity. This is an established ingredient, not the added contribution.
5. **Acevedo–Blekherman, arXiv:2303.11823v1, Lemma 2.1**, and **Blekherman–Riener, arXiv:1205.3102v4, Proposition 6.4:** the relevant notation, statements and proofs were read. Distinct-variable terms determine the leading contribution while coincidences have lower asymptotic order. These are appropriate precedents for the counting technique, not assertions of the precise present fixed-power theorem.
6. **Baldi et al., Stubborn Polynomials, arXiv:2602.01191v1, Definition 2.1 and Theorem 2.2 with proof:** the nonstubborn cone is convex in the stated totally real projective setting, by allowing odd powers to increase. This reinforces the crucial distinction and does not contradict the candidate fixed-q claim.

The plausible added contribution is the application of these classical ingredients to a fixed prescribed odd power, plus a fully specified local rational certificate giving an explicit finite cube dimension. The review found no exact earlier fixed-power counterexample in the bounded inspected sources and targeted search, but it is not an exhaustive literature audit. The candidate page therefore makes no verified firstness claim, no claim of a new product-positivity method, and no claim that all cited sources were read in full.

## Follow-up and collaboration

follow_up is null. Reducing the dimension or resolving the ternary case would matter mathematically, but neither the paper nor this scope review supplies a new mechanism or carefully supported conjecture beyond those immediate boundaries. These are not padded into a public follow-up section. The proposed collaboration invitation seeks substantive specialist review or journal preparation and makes no promise of authorship.

## Independence and exposure disclosure

The independent scope conclusion was logged at 70% before any sibling mathematical findings. No sibling or historical review report, dedicated PRIORITY_NOTE.md, or expected_output.json was read. The public metadata and manuscript §6 necessarily contain author claims about earlier priority audits and verification. README, CLAIM_SCOPE, SOURCE_VERSIONS and PROVENANCE likewise contain accepted-scope/audit statements, source-reading statuses, author-turn provenance, and the origin of a checker in an earlier adversarial effort. These were encountered while reading required mathematical support and locating primary versions. They are source-authored assertions and were not adopted as evidence of correctness or novelty; raw primary documents were freshly acquired and compared independently. No old check count is reported as a fresh execution result.

The original abstract is reproduced completely in content.json, with only whitespace and math typography normalized. AI-use and unrefereed status are separate fields. The manuscript expressly states extensive AI assistance, no human peer review and no formal proof-assistant certificate. This review does not convert those statuses into independent human validation.

No original asset was repaired or altered. No website, spreadsheet, Git, Zenodo, publication or outreach action was performed. Scope content is a candidate awaiting the independent mathematical gates.
'''
(R/'REVIEW.md').write_text(review)
verdict={'record_id':'23191301','completed_utc':now,'completion_percent':100,'role':'independent_publication_scope_and_primary_literature_review','scope_verdict':'no_publication_scope_defect_identified','publication_disposition':'candidate_content_only_pending_separate_mathematical_gates','mathematical_gate':False,'mathematical_verifier_executed':False,'novelty_certified':False,'independent_human_peer_review':False,'full_published_paper_read':True,'published_paper_pages':6,'published_supplement_pdfs':[],'all_published_assets_acquired':True,'source_integrity_pass':True,'archived_or_sibling_review_verdicts_used':False,'independence_note':'Own scope conclusion logged before sibling mathematical findings. Dedicated PRIORITY_NOTE.md and all sibling/historical review reports were not opened. Authored verification, accepted-scope, audit and old-source statuses in required support were encountered and disclosed but not accepted as validation. No verifier executed by this reviewer.','content_sha256':sha(R/'content.json'),'review_sha256':sha(R/'REVIEW.md'),'follow_up':None,'followup_rationale':followup,'defects':[],'key_boundaries':['Fixed positive odd exponent; real homogeneous sextics and real SOS.','Explicit cube example in 3 · 10^62 variables; no ternary or minimal-dimension conclusion.','For each odd q ≥ 3 some n(q); no common dimension for all q.','Classical coefficient-1 seed and cube identity, separation, product positivity and distinct-index precedents credited.','Convexity of the union allows exponent growth; no stubbornness claim for the average.','Bounded primary-source scope only; no first-priority certification.']}
dump('verdict.json',verdict)
log=R/'RESEARCH_LOG.md'
log.write_text(log.read_text()+f'\n## {now} — 100%\n\nCompleted independent scope report, precise candidate content, primary-source receipts/reading extents and verdict. Rehashed both original public assets, record metadata and all 13 extracted archive members; all remain byte-identical. Original abstract is complete and separate from AI status. Follow-up remains null. No mathematical verifier run or mathematical PASS is claimed by this role. Candidate publication remains pending separate analytic/adversarial gates. No source repair or external mutation.\n')
artifacts=['REVIEW.md','verdict.json','content.json','primary_sources.json','final_source_verification.json','RESEARCH_LOG.md','published-paper.txt','acquire_primary.py','finalize_scope.py']
dump('evidence_manifest.json',{'generated_utc':now,'completion_percent':100,'role':'scope','artifacts':[{'path':str(R/f),'bytes':(R/f).stat().st_size,'sha256':sha(R/f)} for f in artifacts],'source_receipts':[{'path':str(S/f),'sha256':sha(S/f)} for f in ['receipt.json','record.json','extraction-integrity.json','reader-pdf-map.json']],'all_published_source_bytes_unchanged':True,'mathematical_verifier_run':False,'mathematical_gate':False})
print(json.dumps({'completed_utc':now,'scope_verdict':verdict['scope_verdict'],'review_sha256':verdict['review_sha256'],'content_sha256':verdict['content_sha256'],'unchanged_public_files':len(files),'unchanged_archive_members':len(memberchecks),'primary_sources':len(prim),'mathematical_gate':False},indent=2))
