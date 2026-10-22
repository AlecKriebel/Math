# Second new sequential whole-result / publication-package adversarial review

**Recommendation:** accept the frozen scientific package and its dated current attribution addendum within the scope below. No mandatory scientific or publication correction, and no unresolved optional correction, was identified. This recommendation grants no Git, native-checkpoint, service, tracker, publication or other operational authority; Root retains final acceptance.

**Object:** already-merged PR210 / problem 5100033, Alec Kriebel, *The outer focal-pedal area product in odd elliptic billiards*, immutable version 1.0 DOI [10.5281/zenodo.23398175](https://doi.org/10.5281/zenodo.23398175), together with the current addendum/index. Candidate 02 manifest is 43,166 bytes, SHA256 `17df6ef2fea59c5c177e5e9deee9de07bfa8eceafc5026b41dbcc63d99879dd6`, binding 151 payload files and 2,140,908 bytes. Every candidate row independently rehashed without mismatch.

## Independence and falsification protocol

CLAIM_FREEZE.md was authored at 2026-10-17T03:38:03.578140Z. It freezes the exact geometry, signed-area conventions, assumptions, success criteria and falsifiers after the full published source was read, and before reading any old/new acceptance or adoption conclusion. The first sequential review's report was not read or used as a premise. Manifest fields mentioning a prior review were merely scope metadata. The freeze SHA256 is `8f34bf43f00047c19dd92c62f6e65eec39378bdfa5b0dd37ee0dc589bcf0ceac`.

The main argument and both auxiliary mechanisms were reconstructed; newly authored independent controls use exact arithmetic and no imported target checker. Published supplementary derivations were read as objects to attack, after the freeze. Current adoption language and Root's replay receipts were inspected only after the independent mathematical construction and initial exact controls. An app interruption resumed the same audit and preserved all completed artifacts.

Falsification attempts focused on wrong construction/foci, stars and parametrization completeness; missed imaginary periods or poles; two simultaneous singular vertices; N=3 and cyclic-cut terms; complementary-zero and zero-function branches; false even fixtures; insufficient geometric area transfer; misleading current priority/coverage; hash/data/source/PDF mismatch; and hidden or excessive execution effects. The checkable universal reconstruction is in UNIVERSAL_RECONSTRUCTION.md.

## Strongest verified mathematical result

For a>b>0, c²=a²-b², and a fixed proper confocal elliptical caustic with 0<lambda<b², assume the family has odd least period N≥3 and any admitted coprime winding. At each original billiard vertex use the tangent to the boundary ellipse. Consecutive intersections form the outer polygon. Project the two **original** foci onto the actual ordered **side lines**, and use trajectory-order signed shoelace area for the feet. Their area product is constant along the family.

The manuscript's complete proof survives the following independent reconstruction and attacks:

| Attack / exact locator | Finding |
| --- | --- |
| Published source lines42-54; canonical coordinates lines67-81; PDF pp.1-2 | The caustic parameter relations imply 0<k<1, 0<v<K. Direct addition formulas prove every chord is tangent at the correct midpoint phase. The unit-direction tangency identity lambda=a²b²(e·n_E)² supplies the confocal reflection check. Two tangents from a boundary point establish completeness of the forward/reverse branches. Stachel Theorem 4.3/(4.9) expressly supplies coprime stars. |
| Source lines83-111, PDF p.2 | Direct perpendicular projection yields Q_+. Adjacent tangents are finite and distinct, so these feet are on the actual outer sides. Q_-=-Q_+(w+2K) gives the correct area focus shift. No original-chord observable or altered focus has been substituted. |
| Source lines113-140, PDF pp.2-3 | Common Jacobi poles are removable; degree-two sn on its own torus exhausts the other roots. The full vector has period 4iK', with a reflection after 2iK'; treating2iK' as a vector period would be wrong. Both imaginary rows are included. Simple opposite residue vectors at the two roots are independently confirmed. |
| Lemma 2, lines142-167, PDF p.3 | At a singular trace phase exactly two adjacent vertices are singular. Their double determinant coefficient vanishes. Other incident edges have one singular endpoint; N=3 shares only the regular endpoint. The closing edge is valid because Ndelta=4Ktau is a true vector period. Bezout gives real periodL=4K/N and two possible simple poles on the reduced torus. |
| Source lines169-202, PDF p.3 | Reflection reverses cyclic order while changing determinant sign, yielding evenness after recentering. The2iK' antiperiod supplies regular complementary zeros atp+L/2 and3p+L/2. Every pole of the shifted product cancels. The pole-free branch forces zero trace; no area division occurs. OddN converts the focus shift toL/2. |
| Corollary 3 and following paragraph, lines204-217, PDF p.4 | Fixed repetitions multiply each area by s and product by s²; reversal negates both areas. A circle is a separate rotational argument. Even **primitive** periods only give equal focal areas, and do not inherit square constancy. |
| Section 5 lines227-260 and archived EXACT_BICENTRIC_DN_BRIDGE.md | Projectivity alone is insufficient. The additional polarity with homogeneous line coordinate-a² gives negative circumcenter d=-c lambda/beta² and a genuine nested bicentric pair. Positive tangent lengths are justified for star ordering. The contact-area ratio follows by a local dn addition identity and cyclic reindexing. An independent Fourier derivation gives the old arbitrary-order Landen identity, with nome q_b^N and exactly the needed original-focus half-period alignment. No central difficulty is moved to an unsupported contact-area assertion. |
| Section 5 lines262-278 and archived CHECKABLE_TRANSFER.md | The pointwise scale Q_+=a(a-csnw)R_- is phase dependent and cannot by itself transport area. The inverse double-pole area reduces to simple poles through isotropic collinearity and local odd reversal. Its nonzero trace and the foot trace occupy the same at-most-one-dimensional antiperiodic simple-pole space. Matching residues gives B_e=gammaD_-e without division through complex zeros. This is a valid additional application, not proof of earlier printing. |

Strictness matters throughout. For any interior parameters the nonzero root derivatives and two-row separation hold. As c→0, lambda→0 or beta→0 the formulas can degenerate; the exact circle is separate and collapsed/grazing caustics are excluded. The proof does not assert a uniform numerical condition bound at these limits. Dimensional checks agree: the foot/contact area has degree two in length, its product degree four; unit inverse areas have inverse-square scaling and the proportionality carries degree four. No empirical assumption enters the universal geometry.

## Fresh exact finite evidence

The new independent_controls.py is stdlib-only and uses exact arithmetic in Q(sqrt5,sqrt21), including exact order comparisons. It passed **165 exact equalities**, **15 exact positivity checks**, and **6,234 finite singular-phase lattice checks** for primitive grids with3≤N≤39. The latter verifies the two adjacent singular indices, including wraparound; the general argument, rather than the finite upper bound, covers every period.

For a²=21,b²=16,lambda=336/25, the independently constructed actual tangent intersections and side-line feet give:

| Fixture | B_+ | B_- | Outer product | Original-chord product | Original unit-inverse product |
| --- | --- | --- | --- | --- | --- |
| H, manuscript Section 6 | (49sqrt21+7sqrt5)/10 | (49sqrt21-7sqrt5)/10 |12544/25|7225344/390625|1/324|
| V, manuscript Section 6 |112/5|112/5|12544/25|7225344/390625|1/324|

These cases additionally verify boundary, common caustic discriminant, reflection with positive direction, actual side incidence/orthogonality, auxiliary circle, cyclic cut, reversal, fixed repetition, the true bicentric circle/contact condition, contact-area ratio 2/15, and opposite-focus inverse factor 2016/5.

The genuine four-periodic D,C phases on x²/4+y²=1 withlambda4/5 have B_±=4 and5, respectively, hence products 16 and 25. This independently checks the parity boundary. Focus dependence was handled exactly as a quadratic area polynomial and evaluated using f²=3. The rectangle actually printed in Ferudun 0062 p.6, (±2/sqrt5,±2/sqrt5), is on the boundary but fails reflection: our unnormalized reflected-edge cross residual is -48/17, with the edge orientation specified in the code. This differs in normalization/orientation from the published correction's unit-vector residual, and confirms the same failure. The corrected C fixture fits the cited inverse products 1 and 25/16: D's inverse area is1; C's inverted parallel sides have horizontal separation sqrt5/4 and summed half-heights sqrt5, giving area 5/4. This local source example error does not refute its general odd inverse theorem.

Finite data distinguish these geometric objects. They do not replace the universal proof or certify all possible families numerically. INDEPENDENT_EXACT_RESULTS.json contains the compact reproducible result, and the code writes only that sibling file.

## Source, priority and current addendum

The actual RGK editions were compared at their definitions, construction and Table7, with visual checks of both table pages. v11 p.9 k605,a is the primed outer product; final 2021 p.349 k606 is the same target. Published k605 is the original-chord product. The stated least-period/star/repetition conventions are the manuscript's explicit precision, rather than falsely quoted formal source definitions.

Ferudun's later exact-target article, DOI [10.5281/zenodo.23404834](https://doi.org/10.5281/zenodo.23404834), Theorem C on p.3, has the same strict confocal, original-focus, signed side-line, odd least-period and all-windings hypotheses. Its definitions onpp1-2, Lemma 5.3 p.14, proof p.16 and Remark 6.6 pp.16-17 were checked. It credits this deposit and describes its own proof as independent. The current addendum accurately attributes those author statements and explicitly declines to certify historical firstness, causal independence or simultaneity. This review does not certify all five theorems of that follow-up paper.

Existing saved record/DataCite fields independently inspected here agree with the addendum: both publication dates are 15 October 2026; our server-created/DOI-registered times are 14:26:52.483806/14:26:53 UTC; the later record's are 20:31:27.602400/20:31:29 UTC. These are recorded event fields, not certificates of first public visibility. No fresh provider query was performed by this reviewer.

The complete official KoG issue was read for all eight pages of Stachel's Triple article (printed 44-51, PDF 46-53); it supplies projective grid/polarity/incidence results, with no printed exact metric focal-pedal product proof identified in the read article. The current note closes that access gap and keeps the incomplete final Talented journal comparison explicit. Its bounded literature qualification remains necessary. This review did not expand the global search or independently re-fetch all historical sources. The older v1 bounded-search statement is not made false by a later article. Historical novelty outside the inspected corpus remains unresolved.

CURRENT_ADOPTION_NOTE.md is 6,486 bytes/hash c846435880ae02775063d1770a2ffa368f37277dce1df712bd2d1c42a83b5062. ADOPTION_INDEX.md is 2,099 bytes/hash ac4301463a056e607f6c41f8d60387381b041d169a6ae5e4c200d2b3abae6d3b. The index explicitly links the current note beside dated native SOURCES/README snapshots. That makes their old access/readiness statements historical rather than misleading current conclusions. No new DOI/version, paper/metadata correction, duplicate tracker row or remerge is called for by the findings here.

## Package, PDF and reproduction coherence

package_check.py independently verified the complete 181-entry ZIP, all 180 SOURCE_MANIFEST rows and exact file set, the 125-row verification manifest and exact file set, all 20 preserved original files, and all five authored family manifest sets (9/7/6/16/11 rows). External and ZIP paper/source/metadata are byte-identical; deposit metadata matches metadata.json. No duplicate/unsafe ZIP member was found. Every candidate pin still matches.

The frozen manuscript is 6 pages/90,186 bytes/hash efa4617d9b3ce2091afe472eb35b5144ec30f3117ffac22dc201498f95a0b731. Full source is 19,892 bytes/hash 71e45462370c5314a2e43cc43678571931f8dc177536637e24cea050034b496e. All six pages were rendered and visually inspected without a substantive layout/glyph/formula discrepancy. Author/ORCID, theorem scope, formulas, exact fixtures, bibliography, metadata, extensive AI assistance, unrefereed status and absence of human peer review agree.

The harness/dependency/normalization logic was read in full, all ten current job sources inventoried statically, and key exact controls read in full. The ten-job and separate genuine-primary Root receipts bind to this exact ZIP's script hashes, frozen result hashes and normalized scientific JSON hashes. Default attested-PDF substitution is correctly disclosed; the separate genuine-primary run has its distinct semantics. Both receipts state no interval certification and no whole-manuscript-review claim. This reviewer freshly hashed the three canonical primary PDFs but **did not rerun the ten inherited jobs**. System and bundled Python lacked SymPy; new controls deliberately avoid that dependency. No installation or large duplicate numerical sweep occurred. See CODE_AND_EFFECT_REVIEW.md for exact execution scope.

No old forensic/builder/publisher/fetcher or native-effect helper was executed or granted scientific/operational authority. The AST inventory is a finite source/effect inspection, not an exhaustive security proof. Numerical errors in archived jobs remain uncertified diagnostics; exact JSON equality is reproducibility of recorded outputs, not proof over all N.

## Findings, gaps and disposition

**Mandatory findings:** none. There is no identified central proof gap, exact counterexample in the stated domain, construction error, false current attribution, package corruption or necessary immutable-v1 repair.

**Optional findings:** none unresolved in the frozen scientific candidate. The current index already supplies the relevant dated-source/current-addendum navigation. Completion of Root's final review/index/status and separately audited adoption checkpoint remains Root work; those pending actions are not scientific defects or authority conferred by this report.

**Remaining limits:** informal rather than formal proof; no conventional independent human peer review; no interval certification of numerical samples; finite independent controls; no comprehensive priority or first-public-visibility certificate; final Talented journal comparison remains incomplete; this reviewer inspected saved provider evidence without live source retrieval; Root replay is verified as receipt-bound evidence rather than falsely claimed as this reviewer's new replay. Original publishers/preparers and the fixed native-effect candidate remain outside this scientific verdict.

The strongest conclusion is a checkable all-odd theorem under the exact strict domain, corroborated by independent finite exact construction checks, coherent immutable publication bytes, and a qualified current attribution note. No substantive correction is required before Root considers this second scientific review complete.
