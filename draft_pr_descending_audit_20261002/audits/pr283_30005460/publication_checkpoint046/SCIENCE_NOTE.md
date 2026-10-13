# Completed PR283: fixed odd-power SOS nonconvexity

Checkpoint prepared on 2026-10-06 UTC. Problem/case completion estimate: **100%**. The repository checkpoint itself remains pending until its separate recorded publication and readback; these are distinct estimates.

**Published research note:** *Nonconvexity of fixed odd-power sum-of-squares cones*, Alec Kriebel, independent researcher, ORCID https://orcid.org/0009-0001-9320-500X. Version 1.0, 2026-10-06, CC BY 4.0. Record https://zenodo.org/records/23191301; DOI https://doi.org/10.5281/zenodo.23191301. The record contains the reviewed six-page PDF and portable exact-arithmetic verification ZIP. The observed concept record is 23191300; this identifier was read from both provider records rather than inferred arithmetically.

## Exact question, hypotheses and accepted result

For real nonnegative homogeneous forms of positive even degree, let C(n,m,q) consist of degree-m forms in n variables whose fixed odd qth power is a sum of squares over the real coefficient field. The original general-dimensional convexity question is OWR-12697710-006 / repository problem 30005460, in Reznick's OWR2023 contribution. The operative question is on printed page 779; the complete contribution spans printed pages 778–781 (PDF pages 38–41). Historical shorter source extents are superseded and retained as history.

The accepted theorem states that C(3*10^62,6,3) is not convex, and that for every fixed odd q>=3 there is some finite dimension n(q) in which C(n(q),6,q) is not convex. This answers the original general-dimensional question negatively. It does not settle the ternary case, find a smallest dimension, prescribe a small dimension, give one dimension working for every q, classify every parameter triple, or show that the finite average has no SOS odd power at all. Earlier convexity results for the union over odd powers and the relevant closedness and Hilbert equality cases remain consistent with the theorem.

## Checkable mechanism and reproduction

The classical coefficient-1 modified Motzkin sextic is p=x^4 y^2+x^2 y^4+z^6-x^2 y^2 z^2. Its nonnegativity and non-SOS character, and the positive weighted 16-square identity for p^3, are credited classical ingredients. The new result combines these ingredients with a finite positive truncated moment functional and an analytically justified finite tensor construction.

For q=3, the complete local moment matrix has dimension 220 and eight parity blocks. The portable verifier uses only Python standard-library integers and Fraction. It reconstructs the local matrices, checks their positive rational LDL pivots, authenticates all 20 initial minors and 24 Schur traces, checks the exact seed cube identity, and reproduces the moments a1=-1, a2=11292*10^53, a3=35039520*10^116. Written arguments prove the arbitrary finite tensor positivity; the astronomical global matrix is not materialized.

With N=10^62 disjoint copies p_i, set F_N=(p_1+...+p_N)/N. Each p_i belongs to C(3N,6,3). The tensor functional evaluates F_N^3 as

    [N*a3 - 3*N*(N-1)*a2 - N*(N-1)*(N-2)] / N^3 < 0.

It is positive on all required squares, so this negative value proves that F_N^3 is not SOS. A finite average outside the cone contradicts convexity. For every fixed odd q, the written finite-order extension and finite tensor argument give a negative qth moment for sufficiently large N; the SOS cube implies the seed's every odd power q>=3 is SOS by multiplication by a square. The dimension in this existence argument may depend on q. The functional is not claimed to be integration against a measure on real points.

The exact checker is reproducible evidence for the finite local certificate and specified cubic sign. The arbitrary finite tensor step and every-odd-q existence rely on the written proof. This package is not a formal proof-assistant certificate. The paper's verification README, expected output and certificate specify the reproducibility boundary explicitly.

## Priority, credit and review

Independent algebraic and tensor-certificate adversarial families checked the original mathematics and source scope. Separate primary-source and repository-discovery families examined priority. The corrected complete package passed fresh whole-package reviews 03 and 04 after repairing the original source-extent statement globally. No remaining material mathematical, credit or package repair was identified.

Classical seed/cube contributions, modern duality and tensor precedents, and earlier varying-exponent/union results are credited in the paper and priority note. The bounded audit found no earlier exact competing theorem in the reviewed sources. It does not certify worldwide firstness or current openness. The disclosed source-access limits include unavailable final Papp2013 and Schmuedgen1979 bodies and incomplete CLR1995/talk coverage; publication does not erase those qualifications.

AI tools were used extensively in solving, checking and preparing this work. This is an unrefereed preprint, without human peer review. No individual was contacted on behalf of this project. The original author budget remains 2/5 substantive turns; these audits and publication steps added no new author proof-search turn.

## Actual publication, tracker and repository outcome

The exact reviewed PDF and ZIP were published once using the repository Zenodo kit, and full public downloaded entities were verified against the approved bytes. Publication metadata and both record/concept identifiers were read back. The original seven named publication runtimes were authenticated; the original framework-engine prelaunch gap remains explicitly qualified, rather than retroactively certified.

One Google Workspace CLI RAW/INSERT_ROWS append recorded the DOI in **'Math Puzzles'!A33:D33**, spreadsheet 1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20, gid1254632077. The exact four cells and the complete older A:D prefix were reread and verified. No append or publication was replayed.

PR https://github.com/AlecKriebel/Math/pull/283 was updated at reviewed author head b31a0703ba3cd1ccd8298cdff8b507eb82a0b6fb and natively merged as e0a94b93520610553c001f265f210f959b591c2c. Its first parent is the observed main commit f9f840d21305bdc353d151abe8dd5c51b6a27dd6; its second parent is the exact reviewed author head. All 43 selected author bodies, eight authored trees and 21 inherited historical leaves were separately accepted before merging. The merged target subtree is e437823362249c6c1822e8bb2951f504bc89ac9b.

The final actual-actions adversary independently checked 43 inner and seven outer original invocations, all seven actual ancestor trees, five accepted target descendant trees, all 43 selected-body hashes, and all 111/23/68 unrelated ancestor siblings. The whole QUEUE comparison preserved every non-target byte while retaining claimed_solved, original 2/5 and the published DOI on target line308. Seventeen independent falsification controls rejected unrelated-tree and QUEUE alterations. The review found no material required repair; ROOT independently rechecked the closed evidence and canonical content before accepting the completed case at 2026-10-06T16:17:50 UTC.

Two operational failures remain preserved with their actual unsuccessful outcomes. The original author CAS was acknowledged, but an immediate PR/ref readback disagreed; its cause remains UNKNOWN. A separate GET-only reconciliation verified the updated branch and every selected body without replay. The initial final merge command was parser-rejected for unsupported --match-head. Installed help and a fresh open-PR readback established the supported --match-head-commit option, and a separately reviewed, bounded new attempt succeeded. Neither failure changes the mathematical paper or supplies a fabricated success record. Reviewer harness failures are likewise retained and qualified.

Completed descending-case counters are now **33/12/12/0** (completed cases / published claimed-solved cases / native merges / tracker pending). Held PRs293 and292 remain uncompleted pending essential priority-source clearance. This effort continues downward through original submitted QUEUE status exactly claimed_solved, skipping PR8 and every other status. The five owned maps/logs were updated once, with whole before-images and other inventory/held records preserved. The current main checkpoint baseline is the independently accepted checkpoint045, 44e2669a2d863aac8e796cb3aae2af417c7c0be6.
