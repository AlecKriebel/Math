"""Prepare reviewable attributed-prior-result exposition; no native or publication action."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B without optimization')
A = Path(__file__).resolve().parent
P = A.parents[1]
F = A / 'attributed_prior_result_preparation_20261004'
F.mkdir(exist_ok=False)
stamp = dt.datetime.now(dt.timezone.utc).isoformat()
specialization = r'''# Credited prior resolution of Holland Problem 5.51

This is a source audit and checked specialization of prior work, not a new paper or a claim of earliest recognition.

## Exact target and historical evidence

Holland's question asks for an explicit construction of a Blaschke product B on the unit disc, B(0)=0, for which F=(1+B)/(1-B) is a Bloch function. Existence is already assumed in the question. The required product is pure Blaschke, not merely an inner function with an uncontrolled singular factor. The Bloch condition is a global derivative bound, not a numerical sample.

Hayman-Lingham, Research Problems in Function Theory, Fiftieth Anniversary Edition (Springer2019), printed121-122 / supplied PDF127-128, prints the original question and credits Aleksandrov-Anderson-Nicolau [21] with an explicitly constructed inner function satisfying a stronger vanishing hyperbolic-derivative estimate. This supersedes the genuine no-progress wording in the retained arXiv1809.07200v2,21September2018, printed105 / PDF106. The2018 statement was accurately quoted as a dated report; using it after reading2019 to assert continuing open status would be materially incomplete. The adjacent2019 no-progress update is5.52, not5.51.

The2019 update alone speaks of an inner I, so pure Blaschke and B(0)=0 are checked from its cited primary source rather than silently inferred from the book.

## Exact target from AAN1999

Aleksandrov, Anderson and Nicolau, Inner functions, Bloch spaces and symmetric measures, Proc. London Math. Soc.(3)79(1999),318-352, Theorem2 printed320 and proof326-327, states: for every positive continuous phi on(0,1] with phi(0+)=0, an interpolating Blaschke product A exists with

    (1-|z|^2)|A'(z)| <= phi(1-|A(z)|^2),  z in D.

Its construction takes a holomorphic universal covering A:D -> D\Lambda, with Lambda countable, cluster points confined to the unit circle and 0 excluded from Lambda. The proof establishes innerness and excludes the singular factor; this is a pure Blaschke product. Because0 belongs to the covered domain, a preimage p with A(p)=0 exists.

Choose phi(t)=t^2. Let psi(z)=(p+z)/(1+conj(p)z), so psi(0)=p, and set B=A composed with psi. The automorphism identity

    (1-|z|^2)|psi'(z)|=1-|psi(z)|^2

preserves the estimate, giving B(0)=0 and

    (1-|z|^2)|B'(z)| <= (1-|B(z)|^2)^2.

B remains a covering of the same domain, so the source's purity argument applies to it. Independently, purity under precomposition follows from the Blaschke Green identity: for each zero a, the factor modulus at psi(z) equals that of the factor with zero psi^{-1}(a) at z; transformed zeros satisfy the Blaschke sum since (1-|psi^{-1}(a)|^2)/(1-|a|^2) is bounded above and below for fixed p. No singular harmonic defect is introduced. This is precomposition, not an arbitrary target-value Frostman shift.

For F=(1+B)/(1-B), the exact derivative identity and elementary modulus inequality yield

    (1-|z|^2)|F'(z)|
      =2(1-|z|^2)|B'(z)|/|1-B(z)|^2
      <=2(1-|B(z)|^2)^2/|1-B(z)|^2
      <=2(1+|B(z)|)^2 <=8.

The denominator is nonzero inside the disc because B is a nonconstant disc map. Also F(0)=1. Thus the exact stated target is fulfilled by the earlier theorem and its covering construction. The source itself prints the quadratic-weight Cayley application for every unimodular alpha on328-329 with Bloch seminorm bound8c. The choice of a zero and the displayed normalization are our checked specialization, distinguished from a literal printed B(0)=0 formula.

The published problem does not formally define 'explicit' as a finite algebraic recursion with a specified error modulus. Its2019 update explicitly credits AAN's construction. Adopting a narrower operational meaning for a present algorithm does not establish that the original historical question remained open or that PR65 newly resolved it. AAN's covering method differs from PR65's finite-stage algebraic recipe; identical-method priority is not asserted.

## Earlier mechanism and PR65's distinct ordering

Piranian, Two monotonic, singular, uniformly almost smooth functions, Duke Math.J.33(1966),255-262, printed260-261, credits Kahane and prints the fixed absorbed four-adic rule: start at height1; replace a positive height M by(M-1,M+1,M+1,M-1); replace0 by four0s. It excludes finite positive ordinary derivatives at every point. This is an earlier inspected printed antecedent than Kahane1969. Duren-Shapiro-Shields, Singular measures and domains not of Smirnov type, Duke Math.J.33(1966),247-254, printed248-250, defines the affine-periodic primitive and proves its Zygmund condition equivalent to F'(z)=O((1-|z|)^-1) for the Herglotz transform. Their primary application uses exp(-aF), not the Cayley Blaschke answer. Neither complete1966 paper is described here as literally printing Holland's exact application.

PR65's first-stage heights are(2,0,2,0), whereas the fixed old rule gives(0,2,2,0). The measures differ, including first-quarter mass1/2 versus0. The submitted neighbor-directed sign choices are a modified deterministic ordering of an old absorbed-walk mechanism. No necessary new benefit of those choices has been established. Independent checks prove that the old fixed rule has the same mass consistency, atomlessness, singularity, all-point ordinary-density obstruction, circular neighbor bound and effective midpoint approximation modulus. This supports mechanism attribution, not an assertion of literal copying.

## Supported disposition and limits

The exact source problem has an earlier sufficient construction credited as explicit by the2019 problem update. This positive prior evidence is enough to withdraw a newly-solved-open-problem claim. It does not identify the earliest solution, first target-specific articulation, identical algorithm, a complete world-wide priority chain, or the novelty of every quantitative detail in PR65. None of those stronger absence/earliest claims is required to classify the original question as already resolved for this program.

The separately audited PR65 theorem remains mathematically verified. It can be accepted as attributed progress/exposition with status already_solved, not promoted as a novel open-problem solution. Original two proof-search turns out of five stay unchanged. The prior work and this newly written normalization deduction are distinguished. All copyrighted supplied PDFs, full text and rendered pages stay in the private cache; public findings reproduce only the necessary authored mathematical deductions and bibliographical evidence. AI tools were used extensively; this audit is unrefereed and has no conventional human peer-review or formal proof-assistant certification.
'''
current = '''# Current reviewed result - PR65 / AMR-022-5051

Proposed disposition, pending ROOT's reading of the fresh independent final adversary: **verified construction; already resolved in prior work; accept as attributed progress**.

The submitted recursive construction produces a pure infinite Blaschke product B with B(0)=0 and a Bloch Cayley transform. Its mathematics has passed the extensive original reproduction, independent mathematical families, and the two whole-package rounds for the former source scope. This remains a verified theorem, while novelty as a resolution of an open question is withdrawn.

CURRENT_PRIORITY_SPECIALIZATION.md checks the exact Holland target from AAN1999 Theorem2, including pure Blaschke, normalization and a Bloch bound8. Hayman-Lingham2019 credits the cited construction as explicit; the earlier2018v2 no-progress wording is genuinely historical and superseded. Piranian1966 prints Kahane's fixed real-variable rule, and DSS1966 prints its Zygmund/Herglotz bridge. The submitted neighboring-height ordering is different; identical-method and earliest-priority claims are not made.

For an eligible claimed_solved submission found to have a priority issue, the program applies the original human instruction to retain valid already_solved findings as attributed partial progress without making a paper. This means partial research-program acceptance, not a failure of the verified target theorem. The exact original problem is resolved by prior work and independently met by the submitted theorem; a new historical resolution by PR65 is not certified.

The original submitted source bodies and two-line2/5 turn ledger are preserved as dated inputs. Their claimed_solved wording does not govern the corrected current acceptance. The unpublished publication_package_v1 and its frozen reviews are superseded for promotion because the three supplied sources materially change priority. They are historical preparation evidence; no package is publication-ready under the original new-resolution gate. No new paper, Zenodo deposit, publication DOI or tracker row accompanies this attributed prior-result disposition. The PR50 Nencka exception is not extended to PR65. The current PR50 editor remains open and unchanged.

AI tools were used extensively; the work is unrefereed, has no conventional human peer review and no formal proof-assistant certification. Native status, GitHub result and program completion will be recorded only after actual execution and independent readback.
'''
body = '''The mathematical construction is verified, but the priority audit shows that Holland's Problem5.51 already has a sufficient construction in earlier work. Accept this as attributed progress with outcome `already_solved`; withdraw the claim to newly resolve an open problem.

AAN1999 Theorem2 gives a pure interpolating Blaschke covering with a quadratic derivative bound. Normalizing at a preimage of0 gives B(0)=0 and a Bloch bound8 for(1+B)/(1-B). Their pp.328-329 explicitly print the Cayley/Bloch application. Hayman-Lingham2019 Update5.51 credits their construction as explicit, superseding the no-progress wording of the retained2018v2. The checked normalization deduction is distinguished from the literal earlier text.

Credit Kahane's absorbed four-adic mechanism as printed by Piranian1966 pp.260-261, and DSS1966 pp.248-250 for the periodic Zygmund/Herglotz bridge. PR65 changes the child ordering; no assertion of identical construction or earliest recognition is made. The verified proof and reproducible checks remain useful attributed exposition.

The original submitted bodies and2/5 proof ledger remain dated inputs. CURRENT_RESULT.md, CURRENT_PRIORITY_SPECIALIZATION.md and acceptance.json will govern corrected current acceptance after actual merge. The former unpublished note is superseded; no new paper, Zenodo record, DOI or tracker row is created for this prior-result acceptance. Extensive AI assistance; unrefereed and without conventional human peer review.

Validation: universal analytic and factorization audits, reproduction of exact recursion diagnostics, full primary1966 bodies and decisive2019/AAN pages, three independent renewed source families and fresh final priority adversary. Finite controls support transcription and implementation checks; they do not certify universal analytic statements or worldwide earliest priority.
'''
for name, value in [('CURRENT_PRIORITY_SPECIALIZATION.md', specialization), ('CURRENT_RESULT.md', current), ('PR_BODY.md', body)]:
    (F / name).write_text(value)
proposal = {'schema': 'pr65-prospective-attributed-prior-result-disposition/v1', 'UTC': stamp, 'actual_writer_pid': os.getpid(), 'PR':65, 'expected_original_head':'5cc1602c05d79502defb07cec7027963149494d2', 'eligible_intake_literal_status':'claimed_solved', 'original_proof_turns':'2/5', 'new_original_proof_turns':0, 'candidate_mathematics_verified':True, 'proposed_status':'already_solved', 'prior_resolution_of_exact_original_problem_verified':True, 'new_solution_priority_clearance':False, 'candidate_identical_algorithm_priority_certified':False, 'earliest_resolution_certified':False, 'proposed_acceptance':'attributed_partial_research_progress', 'full_target_met_by_prior_work':True, 'proposed_PR_title':'2305051: attributed Blaschke construction; prior resolution credited', 'human_partial_outcome_rule':'If the result was already_solved or unsolved, audit the findings, and if valid and everything checks out, merge the PR as a partial result. Do not make a paper for these.', 'scope_interpretation':'Only claimed_solved PRs qualify at intake. For this eligible submission found to have a priority issue, apply the original human partial-outcome clause; the current goal file itself omits that clause. Never process initially nonclaimed PRs.', 'fresh_final_adversary_pending':True, 'ROOT_final_disposition_gate':False, 'Git_native_PR_mutation_authorized_by_this_proposal':False, 'publication_authorized':False, 'new_paper':False, 'new_DOI':None, 'tracker_append':False, 'PR50_exception_extended':False}
(F / 'DISPOSITION_PROPOSAL.json').write_text(json.dumps(proposal, indent=2) + '\n')
custody = json.loads((A / 'ROOT_provided_source_reading_20261004/PRIVATE_RENDER_CUSTODY.json').read_bytes())
for row in custody['images']:
    p = Path(row['private_path'])
    if len(p.read_bytes()) != row['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        raise RuntimeError('ROOT visually inspected page drift')
(A / 'ROOT_provided_source_reading_20261004/PIXEL_INSPECTION_READBACK.json').write_text(json.dumps({'UTC':stamp,'actual_recorder_pid':os.getpid(),'ROOT_complete_journal_extracted_bodies_read': ['Piranian1966','Duren-Shapiro-Shields1966'], 'ROOT_personally_inspected_all_19_rendered_pages':True, 'HL2019_complete_book_read_claimed':False, 'HL2019_scope':'imprint and complete printed121-122; Chapter5 independent family assigned', 'AAN_rechecked_primary_pixels_printed':[320,326,327,328,329], 'no_layout_OR_OCR_only_basis_for_decisive_equations':True}, indent=2) + '\n')
sup = {'UTC':stamp,'publication_package_v1_superseded_for_promotion':True,'frozen_historical_package_and_reviews_preserved':True,'reason':'Supplied2019 update credits explicit AAN construction; exact prior target verified, and1966 mechanism attribution closes unread-body gaps.', 'old_package_no_longer_currently_ready':True,'current_concrete_preparation':'attributed_prior_result_preparation_20261004','new_paper_or_publication':False}
(A / 'PUBLICATION_PACKAGE_V1_SUPERSEDED_20261004.json').write_text(json.dumps(sup, indent=2)+'\n')
progress_path=P/'CURRENT_PROGRESS.json'
progress=json.loads(progress_path.read_bytes())
if progress['current_PR']!=65 or progress['current_publication_authorization']:
    raise RuntimeError('Current scope changed')
progress.update(UTC=stamp,current_priority_audit_percent=95,current_priority_audit_complete=False,current_qualified_package_ready=False,current_package=None,current_package_historical_supersession_record='audits/pr65_2305051/PUBLICATION_PACKAGE_V1_SUPERSEDED_20261004.json',current_disposition_preparation='audits/pr65_2305051/attributed_prior_result_preparation_20261004',current_priority_final_adversary='/root/pr65_provided_priority_final_adversary_20261004',current_PR_workflow_percent=55,remaining_current_step='Finish independent supplied-source reports, read and verify all evidence, challenge the proposed attributed already-solved disposition with a fresh adversary, then apply guarded current acceptance and exact-head merge if it passes; no paper/DOI/tracker for prior-result disposition.')
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## '+stamp+' - supplied-source exact prior target verified; concrete corrected disposition prepared\n\nROOT read both full1966 extracted bodies and all16 scan pages, plus2019 imprint/complete printed121-122, and rechecked AAN320/326-329 pixels. Positive prior theorem + exact normalization + Bloch bound8 support an already-resolved original question. The2018 no-progress report is genuine but superseded. Old package remains frozen historical evidence and is expressly withdrawn from current promotion. Three new independent source families and a new final outcome adversary challenge current findings. No native/Git/PR/publication/editor mutation. Original2/5 unchanged. Estimates: math100%; priority95% pending final independent adjudication; workflow55%; ordered completion6/99=6.060606%.\n')
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(F.iterdir()) if p.is_file()]
(F/'MANIFEST.json').write_text(json.dumps({'UTC':stamp,'files':files,'proposal_not_execution':True},indent=2)+'\n')
print(json.dumps({'status':'PASS','UTC':stamp,'actual_writer_pid':os.getpid(),'concrete_reviewable_proposal':str(F),'native_or_publication_mutations':False},indent=2))
