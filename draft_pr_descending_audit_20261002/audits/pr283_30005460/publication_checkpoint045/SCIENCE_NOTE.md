# Checkpoint 045 candidate: fixed odd-power SOS cones are not always convex

The accepted finding is nonconvexity of `C(3·10^62,6,3)` and, for each fixed odd `q≥3`, nonconvexity of `C(n(q),6,q)` in some finite dimension. This dated scientific research checkpoint, prepared on 6 October 2026, records ROOT-accepted findings for original PR283, submitted head `c0c88b18db237e97a0bddbf28a6d4fdd52af5522`, original status `claimed_solved`, author campaign 2/5. This candidate has not been committed or pushed. Checkpoint 044, `b569035aa9ce654f32e13f2cf19558a94a038b69`, remains the last completed research checkpoint. This note is a scientific progress record; the candidate preprint, PDF and ZIP are not included.

The mathematical and original-source theorem assessment is complete (100%), as is the bounded priority assessment (100%). The whole PR283 workflow is estimated at 60%. The earlier first fresh whole-preprint review was ROOT accepted with no required repairs at that historical selector. The second reviewer subsequently identified a contribution-range and source-reading-extent correction. ROOT applied that repair and rebuilt the preprint and portable package, preserving the old selected bytes. A new first review of the corrected exact package is active; fresh whole-package reviews and ROOT adjudication remain required. The old clearance does not establish readiness of the revised package. Preprint and publication readiness are not accepted. Original author work remains 2/5; the audits, preparation, source correction and this checkpoint add no author proof-search turn. Completed-case counters remain 32/11/11/0 (completed/published/native-merged/tracker-pending). PR293 and PR292 remain held and uncompleted.

## Exact claim and assumptions

For positive finite integers n, positive even m, and fixed positive odd q, let

\[
C(n,m,q)=\{f\in\mathbb R[x_1,\ldots,x_n]_m:
 f(x)\geq0\text{ for all real }x,\quad f^q\text{ is a real sum of squares}\}.
\]

The subscript m denotes homogeneous forms of degree m. All sums of squares use the same real n-variable polynomial ring; positive rational weights may be absorbed into real square roots. The accepted theorem is:

* `C(3·10^62,6,3)` is not convex.
* For every fixed odd integer `q≥3`, there exists a finite dimension `n(q)` for which `C(n(q),6,q)` is not convex.

This answers the general-dimensional fixed-power convexity question recorded by Reznick in OWR14/2023, printed page 779, and repeated by Blekherman–Kozhasov–Reznick (BKR), published 2026, §6. It gives no ternary result, smallest dimension, prescribed small dimension, one dimension for all q, full classification, or assertion that the average has no SOS odd power at any exponent. Closedness and earlier convexity of the union over odd powers remain consistent. Closedness follows from the continuous coefficient power map and the closed finite-degree SOS cone; for odd q, nonnegativity of f follows pointwise from an SOS f^q. For q=1 the cone is the convex SOS cone; the oddness hypothesis is essential to the leading-sign argument.

## Proof mechanism, including the finite tensor step

Use the classical coefficient-1 modified Motzkin sextic

\[
p(x,y,z)=x^4y^2+x^2y^4+z^6-x^2y^2z^2.
\]

AM–GM gives `x^4y^2+x^2y^4+z^6 ≥ 3x^2y^2z^2`, including coordinate-zero boundaries, so p is nonnegative. Its credited cube identity is an exact sum of 16 positive-weight squares of degree-nine polynomials. The supplied checker expands both sides over the rationals. Neither this seed nor its cube identity is claimed as new.

Define a rational functional L on all monomials in x,y,z through degree 18. Put zero on monomials with any odd coordinate exponent. Put L(1)=1. For total degree 2 or 4 use the standard centered Gaussian monomial moment divided by 1024. At degree 6 the complete even-exponent table is:

| Exponent | L value | Exponent | L value |
|---|---:|---|---:|
| (6,0,0) | 2^24 | (0,6,0) | 2^24 |
| (4,2,0) | 1 | (2,4,0) | 1 |
| (0,0,6) | 1 | (2,2,2) | 4 |
| (2,0,4) | 32 | (0,2,4) | 32 |
| (4,0,2) | 4096 | (0,4,2) | 4096 |

At total degrees 8,10,12,14,16,18 multiply the Gaussian moment by `10^16,10^34,10^53,10^73,10^94,10^116`, respectively. For an even exponent `(a,b,c)`, that Gaussian moment is `(a−1)!!(b−1)!!(c−1)!!`, with `(−1)!!=1`. The rule is determined by exponent sum, so mixed-degree entries are consistent.

The moment matrix `M=(L(x^(α+β)))` on all degree-at-most-nine monomials has dimension 220. Its eight parity blocks exhaust the full matrix. Exact rational LDL decomposition gives all 220 pivots strictly positive and reconstructs every block entry. The checker also authenticates the certificate's 20 initial leading minors and 24 Schur traces. The Schur construction independently explains the scales: in each extension, `BᵀA⁻¹B` is positive semidefinite, and its Gaussian-congruent maximum eigenvalue is at most its trace, strictly below the new scale. Thus L is strictly positive on every nonzero square of degree at most nine. In particular,

\[
a=L(p)=-1,\qquad b=L(p^2)=11292\,10^{53},\qquad
c=L(p^3)=35039520\,10^{116}.
\]

For any finite s, take disjoint three-variable copies `p_1,…,p_s`. On blockwise monomials define `L_s` by the product of local L values. Every global monomial of total degree at most nine has one block decomposition, with each local degree at most nine. The global moment matrix is therefore a principal submatrix of the finite Kronecker product `M^⊗s`, and is positive definite. This proves positivity on all coupled squares, including squares involving several blocks. It uses no probability measure, infinite tensor product, or limiting moment extension. The enormous matrix is not materialized.

The cubic collision count is exactly

\[
L_s((p_1+\cdots+p_s)^3)
=sc+3s(s-1)ba+s(s-1)(s-2)a^3
=sc-3s(s-1)b-s(s-1)(s-2).
\]

Since `b≥1`, this is at most `s(c−s²+1)`. At `N=10^62`, `c<N²−1`, so it is strictly negative. Hence the cube of the nonnegative average `N⁻¹∑p_j` is not SOS. Each input has an SOS cube in the same `3N`-variable ring. Binary convexity would imply membership of every finite average by induction, giving a contradiction. A least failing prefix also yields existence of two cone members whose sum leaves the cone; membership of an arbitrary intermediate prefix is not assumed. Squares of degree above nine cannot represent this homogeneous degree-18 polynomial: the highest homogeneous square pieces would have a sum identically zero and hence each would vanish. The separating argument therefore excludes every real SOS representation, not merely a selected monomial support.

For each fixed odd `q≥3`, `p^q=p^3(p^((q−3)/2))²` is SOS. Work afresh in the finite polynomial space through degree `6q`. The SOS cone in this space is closed: integration against a Gaussian bounds the traces of positive Gram matrices because its finite moment matrix is positive definite; a convergent subsequence produces a limiting positive Gram matrix. The seed p is not SOS in this larger space either, by the highest-degree cancellation argument. Finite-dimensional separation gives a functional negative on p and nonnegative on all required squares. A sufficiently small Gaussian perturbation makes it strictly positive on nonzero squares while preserving its negative p-value; normalize its constant value to one. A fresh functional is chosen for each q, so no degree-18 certificate is reused outside its domain.

For the resulting disjoint-copy functional, partition the q labeled factors by equal block indices. The expansion of `L_s((∑p_j)^q)` is a polynomial in s. The singleton partition has the unique degree-q term, with leading coefficient `L(p)^q<0`; every collision partition has smaller degree. It is consequently negative for sufficiently large finite s. Product positivity and finite averaging give the general odd-q conclusion. This is an analytic existence proof, without an explicit general-q dimension bound.

## Reproducible finite certificate

The checkpoint explicitly selects the standard-library checker, complete rational certificate, deterministic expected output, provenance, claim scope, dated priority note and source-version ledger from `preprint_package_v01`. It includes the mathematical and priority assessment/acceptance records, the historical first whole-preprint review/acceptance, and the complete corrective source-extent assessment. Exactly 21 complete bodies are selected. The exact selector identifies each body by byte count, SHA256 and Git blob identifier; no directory glob defines the publication set.

From the PR283 audit directory in a checkout containing these checkpoint files, run:

```sh
python3 -E -B preprint_package_v01/verification/check_certificate.py > /tmp/pr283-checkpoint045-result.json
python3 -E -B -c 'import json; from pathlib import Path; a=json.loads(Path("/tmp/pr283-checkpoint045-result.json").read_bytes()); b=json.loads(Path("preprint_package_v01/verification/expected_output.json").read_bytes()); assert a==b; print(a["status"])'
```

Success prints `PASS_EXACT_RATIONAL_CERTIFICATE`. The calculation uses only Python integers and Fraction, without floating point, downloads, package installation or external code. It checks the exact 220-dimensional local matrix, 20 initial minors, 24 Schur traces, all 16 credited cube squares, the three moments and the entire negative integer at `N=10^62`; small finite collision controls also agree. The whole stdout JSON must match the expected output, not merely its PASS label. The accompanying proof establishes arbitrary finite tensor positivity and each-odd-q existence; the finite checker alone is not a formal proof-assistant certificate.

The checkpoint does not bundle `paper.tex`, the candidate PDF, the candidate ZIP, third-party paper bodies, or every dependency of historical checkers. References to those artifacts in retained historical review/provenance records are evidence descriptions, not inclusion or publication claims. The proof needed for this scientific checkpoint is stated above.

## Explicit correction of contribution range and reading extent

Reznick's contribution to OWR14/2023 occupies printed pages 778–781 (PDF pages 38–41), including the bibliography continuing onto page 781 before Maria Infusino's contribution. The operative definition and question remain on printed page 779/PDF page 39. Earlier reports describing a complete contribution as pages 778–780 were incomplete. Those reports and their first-review acceptance are retained as historical evidence, not silently rewritten or treated as current package clearance.

ROOT directly read the complete retained contribution text through page 781 and visually inspected its continuation. The current corrected source ledger distinguishes that new ROOT reading from the earlier family readings; it does not retrospectively expand their extent. The whole workshop report remains unread. The complete corrective assessment is selected as `ROOT_SOURCE_EXTENT_ASSESSMENT_01.md` (3049 bytes, SHA256 `a2f6e48e3b9b9a8a97da4859f6ed11846617de34565a73aa1e16ec09d478edd9`). ROOT's separate `ROOT_SOURCE_EXTENT_ADJUDICATION_01.json` has 2036 bytes, SHA256 `52c5648ff189a5bc130d8a5d5051be4ef3d1a5b1a88a8e6502cf7edaee6916fd`; it is a referenced evidence record, not an additional selected checkpoint payload. The primary PDF remains 734622 bytes, SHA256 `5a9bdc9f9daa12ef35185ceae208c0f2f75e191875827f78b7b6ad0f5cdbf240`.

The continuation's references to Reznick's Hilbert construction, Scheiderer's projective Positivstellensatz and Stengle's integral solution identify no exact competing fixed-power theorem. Family A had already read Stengle 1979 in full and the relevant Scheiderer corollary. This does not assert complete reading of every reference. The theorem, certificate, question's parameter scope and bounded priority conclusions are unchanged. ROOT applied the source-ledger, bibliography and priority-disclosure corrections and rebuilt the package. The revised preprint requires new reviews. This is a citation/extent repair, with no author proof-search turn.

## Credit, bounded priority and remaining gap

The proposed contribution is the fixed-power nonconvexity application and its explicit finite certificate. Earlier credit is required for the seed (Berg–Christensen–Jensen 1979, Lemma 1, printed 164–165), SOS closure/separation (their Proposition 2 and Theorems 3–4), the cube (Reznick 2023 and BKR 2026 §6), disjoint product positivity (Barak–Kelner–Steurer, ECCC TR13-184, Lemma A.5; also Papp 2011 thesis Lemma 4.18 and Kapelevich–Coey–Vielma 2022 Lemma 3.1), and distinct-index/collision precedents (Acevedo–Blekherman Lemma 2.1 and Blekherman–Riener Proposition 6.4). Earlier absorption and union-convexity results of BKR, the credited Pinelis ingredient, and Stubborn Polynomials remain earlier results. Their sum theorem changes equal exponents q to `2q−1`, so it does not establish fixed-q addition.

Stubborn Polynomials has six authors, in this order: Lorenzo Baldi, Grigoriy Blekherman, Khazhgali Kozhasov, Daniel Plaumann, Bruce Reznick and Rainer Sinn. The detailed `PRIORITY_NOTE.md` and `SOURCE_VERSIONS.json` preserve dates and actual reading extents. BKR's final article, online 27 April 2026, DOI `10.1017/fms.2026.10221`, retains the question as a dated historical record; this is not a certificate of present worldwide openness.

Two extensive independent bounded searches found no earlier exact fixed-power nonconvexity theorem or equivalent negative-mean disjoint-copy theorem in the sources actually examined. They establish neither worldwide firstness nor exclusion of later, unpublished or inaccessible results. The full final Papp–Alizadeh 2013 body was unavailable; its classical tensor ingredient is independently available in the 2011 predecessor, the 2022 paper and BKS 2013. Schmüdgen 1979 was unavailable (retained 403), and the captured Choi–Lam–Reznick 1995 scan was unread. Partial readings and incomplete bibliography, citation-index and talk coverage remain limits. Material competing evidence reopens this assessment.

The strongest verified result is the stated finite nonconvexity theorem, original general-dimensional source correspondence, exact local certificate, and completed bounded priority audit with the explicit contribution-range correction. The exact workflow gap is fresh whole-package reviews and ROOT adjudication of the corrected exact preprint version, followed by any necessary repair and only then publication operations. This dated point may remain an honest historical checkpoint while later local workflow advances; a later material theorem/credit/priority repair requires a new checkpoint candidate. Frozen maps must never roll back a newer remote checkpoint or overwrite later live research maps when ROOT records completion.

Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. AI tools were used extensively. The work is unrefereed, without human peer review or formal machine proof. No outside individual was contacted; no new DOI, release, Zenodo, tracker or PR operation is part of this preparation.
