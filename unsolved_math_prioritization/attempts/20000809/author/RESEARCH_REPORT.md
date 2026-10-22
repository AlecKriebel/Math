# Source-aware research report

Date of review: 2026-10-05. Problem 20000809, AIM-ARITHMETIC_GEOMETRY-0055. General disposition: **unsolved; five substantive approach families examined**. This records a bounded research attempt, not an exhaustive literature survey or a priority claim.

## Source recovery and scope

The controlling source is *Components of Hilbert Schemes*, questions discussed at the July 19--23, 2010 AIM workshop, recorded by Izzet Coskun and edited by Li Li. The relevant item is **Problem 8, PDF page 2**. In authored paraphrase, it asks whether an irreducible component containing a smooth Borel-fixed Hilbert point must be rational. The following remark identifies segment ideals as an affirmative case and cites Lella--Roggero.

Problem 8 itself gives no field, characteristic, ambient dimension, Hilbert polynomial, or length. Page 1 uses both Hilbert schemes of points of affine space and projective Hilbert schemes of curves; its convention makes “component” mean irreducible component. Therefore the earlier report's assertion that the surrounding workshop uniquely fixes the setting to arbitrary Hilb^P(P^n) was too strong. We separate the finite-length interpretation, which has a classical complete answer, from the broader projective interpretation, which this packet does not settle. Our default characteristic-zero algebraically closed field and whole-Hilbert-scheme meaning of smoothness are explicit working hypotheses, not extra words recovered from the source.

The selected live catalog page could not be read through the web tool. The supplied complete problem corpus and complete research-report corpus were read directly. The target statement's UTF-8 SHA-256 exactly agrees with the catalog descriptor. The descriptor title describes the earlier AI-generated partial result; it is not the primary question's title or an additional hypothesis. Full corpus and record fingerprints are in `provenance.json`.

The AIM PDF's extracted primary text was available through the web tool; direct byte retrieval returned HTTP 403, and the screenshot request failed. Consequently no AIM PDF byte hash or successful visual-inspection claim is made. The source inspection identifies the question by number, page and context. Other primary PDFs used below were actually retrieved and hashed, with their inspection scope stated separately.

## Actual prior-attempt and repository checks

The full supplied per-problem report had already combined a BB attracting-cell theorem and Gordan's alternative, proposed finite tangent-weight computations, and explicitly left open whether smooth Borel points always satisfy the half-space condition. Reproving that combination cannot count as a new solution.

The fresh repository checks found the row still `queued`, `0/5`, in `unsolved_math_prioritization/QUEUE.md`, at file blob 483de6795be8c12bacc3d18e1ef04900eddedf04. Exact ID/code searches found no matching prior code, PR, commit, or branch. This is bounded search evidence, not a guarantee that all unindexed history or drafts are absent. No remote writes were made.

### Corrections to the supplied report

- Its abstract tangent-attraction implication is valid under its stated smoothness/torus hypotheses and uses standard BB theory.
- Its unqualified identification of a projective tangent space with Hom_S(J,S/J)_0 for **saturated, untruncated** J is false. The explicit length-seven example has dimensions 14 and 12 respectively. The smaller space even passes a half-space test that the actual tangent space fails.
- Its proposed implication from smooth Borel fixation to a pointed tangent cone is false. The credited family in `PROOFS.md` supplies opposite actual full-torus characters.
- The positive finite-length case follows from classical distraction and rationality of the smoothable component; it need not await tangent separation.
- The cited Lella--Roggero arXiv v3 numbering is Theorem 6.3(iii) and Corollaries 6.9--6.10. Earlier versions/citations can have different numbering; the report's reference to Corollary 6.8 should not be blindly transferred to v3.
- Relevant Bertone--Cioffi--Roggero (2017) results were omitted from the prior discussion. Their double-generic condition is additional, not a proof for arbitrary smooth Borel points.

## Five substantive approach families

### 1. Repair and stress-test the infinitesimal BB route

We checked the abstract source criterion against the smooth-locus version of BB theory and replaced the projective tangent input by sheaf Hom/high truncations. A concrete exact calculation shows why the correction matters: at J=(x^2,xy^3,y^4), dimension 12 untruncated Hom is not dimension 14 Hilbert tangent, and the missing character reverses the half-space outcome. This preserves a conditional criterion, not a general answer.

### 2. Search actual Borel points for a half-space obstruction

Strongly stable finite plane staircases were enumerated through length seven. The first obstruction is the known column-height (4,3) ideal above. Rather than rely on the enumeration, the proof gives two explicit maps and extends them to the known odd-length family (x^2,xy^m,y^(m+1)), m>=3. Syzygies, colength, saturation, Borel fixation and whole-scheme smoothness are all proved. The finite checker supplies 13 exact small-plane separating certificates for lengths <=6 and verifies family samples m=3,...,12. No new minimality claim is made: the source already classifies nonsegment onset at length seven.

Outcome: the report's auxiliary universal half-space conjecture is disproved. This is a method obstruction on rational components, not a negative answer to AIM.

### 3. Bypass weights using distraction and explicit birational coordinates

We proved the general finite-colength monomial smoothing construction and the affine-space chart (monic polynomial plus interpolation polynomials) of the smoothable component. Smoothness at a monomial point then identifies its unique component with this rational component. Projective saturated Borel ideals with constant polynomial reduce to the affine chart.

Outcome: complete credited positive answer for Hilbert schemes of points, in all ambient dimensions under the stated field assumptions. The distraction itself works in arbitrary characteristic over an algebraically closed field. Positive-dimensional projective schemes do not reduce to this finite grid argument.

### 4. Try the double-generic-point and marked-chart bridge

The 2017 theorem proves rationality if the component's double-generic initial point is smooth on that component; codimension-two ACM points are a further established positive case. The given smooth Borel point need not be that point. For our example, a dense contracting Groebner stratum at the point would contradict its opposite tangent characters; the low-degree Hilbert-function discrepancy also rules out equality with a saturated generic initial ideal of general seven points. The proof carefully avoids asserting that saturation preserves all low-degree Hilbert functions.

Outcome: no proof that an arbitrary component's distinguished generic limit is smooth. Replacing “some smooth Borel point” by “smooth double-generic point” would change the problem. An open marked chart, or an etale chart, need not be a dense affine-space chart.

### 5. Test later irrational-component constructions as candidate counterexamples

Farkas--Pandharipande--Sammartano, arXiv:2405.11997v3 (August 2026; final version, listed to appear in *Forum of Mathematics, Sigma*), establish irrational components of Hilbert schemes of points in affine dimension at least 12. Wu's June 2026 preprint arXiv:2606.30386v1 claims an improvement to dimension at least 10; the latter claim is reported as that manuscript's theorem, not independently certified here. Neither candidate can meet the required smooth-monomial-point condition by the classical theorem proved in Approach 3. The exclusion is independent of the full correctness of either irrationality construction.

We also inspected Ramkumar's two-Borel geometry, Staal's arbitrary-characteristic classification, the 2025 marked-resolution paper's concrete rational parametrizations, and the August 2026 smooth-Quot classification. Their checked results concern more restricted geometry or different moduli problems. None supplies the missing general implication. A globally smooth component is a stronger condition than containing one smooth point, and a unirational parameterization is weaker than rationality.

Outcome: no qualifying nonrational component was established. The general projective question remains unresolved by these five approaches.

## Precise useful results and limits

- The original criterion remains a valid sufficient condition only after the tangent-space input is corrected.
- The finite-length case is a classical positive result, explicitly recovered rather than advertised as new.
- The opposite-character family is a fully proved counterexample to a proposed stronger hypothesis. The underlying ideals are previously published.
- No statement here establishes irrationality, stable irrationality, or failure of unirationality of any component containing a smooth Borel point.
- No characteristic-positive strong-stability equivalence is used. The source did not specify characteristic, so a positive-characteristic general answer is not claimed.
- The remaining general scope is positive-dimensional projective subschemes outside the cited positive cases. “Unresolved here” is not a globally certified open-status assertion.

## Verification

`verify.py` computes monomial Hom kernels from all least-common-multiple pair syzygies with exact rational arithmetic, split by their fine multidegrees. It checks the length-seven affine and truncated projective tangent characters, the 12-versus-14 discrepancy, exact failed/passing half-space certificates, Borel stability, Hilbert functions, equal-product obstruction, a distraction evaluation matrix, a general-quadrics rank control, small-length separating certificates, and the odd-length family. Five deliberately false mathematical alternatives are rejected.

The script uses only the Python standard library. It emits deterministic JSON; source-PDF access is not needed for the algebraic replay. A passing run is supplementary finite verification of the supplied proofs, not formal verification of algebraic geometry or resolution of the general source question.
