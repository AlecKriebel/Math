# PR628 independent geometric adversarial review

Verdict: **PASS for the universal geometric upper bound and V4 improvement; no mandatory or optional repair identified in this family.** This does not certify priority, the independent arithmetic sharpness certificate, or a subsequently prepared publication package.

## Inputs and independence

Original PR628 head: `677673860f9e67dffc610f52384f0bd60e65e363`. Problem `30000403 / OWR-1188-004` has exact status `claimed_solved` in the parent's immutable-head scope capture. All36 captured native files were independently rehashed before and after this review; their hashes and sizes match that capture. The proof binding is SHA256 `20cb77c2ac8befd8d2f9be9a421d2925580c29e24002a1abc8e3dedb13caeb5a`.

I read the entire frozen proof, prior audit, corrections and release clarifications. I independently reconstructed the geometric proof rather than accepting their PASS declarations. I did not contact the parent's other mathematical family, any other shard, or any outside individual. No PR, QUEUE, publication, tracker, repository index or branch was modified. All authored files are in `reviews/geometry_01`.

## Source and quantifier match

I freshly retrieved both primary PDFs, read the complete relevant problem passages and mathematical framework, and visually inspected the original printedp326 and the manuscript's classification page5. URL, byte counts, hashes and retrieval times are in SOURCE_BINDINGS.json; raw PDFs/text/renders are only under ignored tmp.

- [OWR report, Cadoret contribution, pp325–328](https://publications.mfo.de/bitstream/handle/mfo/2936/OWR_2006_06.pdf?isAllowed=y&sequence=1): characteristic zero; inner G-marking; coarse spaces; optimal upper-bound problem on p326; r>=3 finite-stabilizer convention; existing bounds on p327.
- [Cadoret author manuscript](https://webusers.imj-prg.fr/~anna.cadoret/GPGL2.pdf): §§1.1–1.2 distinguish coarse rational points from models; Lemma2.1 provides stable representatives and normalizers; Lemma2.3 and Proposition2.4 give the cocycle framework; Corollaries3.9/3.11 give prior bounds; Remark3.14 discusses optimality; Corollary5.1 includes the stronger r=3 conclusion.

The source asks for bounds for a reduced coarse point's minimal lift degree. It does not demand actual marked cover objects to descend over that extension. Keeping the existing actual-cover exclusion is mathematically necessary, not an evasion. The proved theorem is the sharp *universal constant* over all admissible fields and Hurwitz data, together with a sharper V4 stratum. It does not decide degree1 versus2 for every individual input or every fixed datum. Existing proof and release clarifications state that limitation adequately. A future paper must retain it.

## Independent derivation and attack outcomes

DERIVATION.md supplies the complete family argument and the precise boundary cases. The principal attacks were:

1. **Wrong geometric stabilizer or wrong quotient.** The cover-point stabilizer is a subgroup of the branch-divisor stabilizer and need not equal it. The proof uses the former throughout its upper bound. Three distinct branch points make it finite. The geometric coarse quotient has a single orbit over each geometric reduced point. Neither a central gerbe nor non-neutrality of a cover-model stack changes the implication from a fixed geometric coarse point to a rational point of the coarse variety.
2. **Nonabelian cocycle orientation.** With sigma(y)=a_sigma^-1 y, the quotient cocycle is c_(sigma tau)=c_sigma sigma(c_tau). A PGL2 coboundary h^-1 sigma(h) projecting to c makes hy fixed. The proof's multiplication order is correct; a finite nonabelian model supplies216 additional direction controls.
3. **An extra quadratic extension hidden in the torus case.** For C_n, n>=2, kill the C2 component once and apply ordinary Hilbert90 over that same field. The proof does not multiply two quadratic degrees. For E=1, only a PGL2 torsor occurs: its conic has index<=2. No invalid general period-index assertion is used.
4. **Nonconstant finite normalizer.** For V4, N is not generally constant and no rational S3 section is available. The independent calculation gives24 normalizer elements, only8 rational over Q, but all6 quotient classes are Galois-invariant. The proof uses the constant quotient correctly.
5. **A full S3 action that cannot be realized in split PGL2.** Every cubic etale action is realized by the nonzero two-torsion of Y²=F(X), whose quotient by inversion is the split X-line. The translation construction proves the required realization. The conjugating h can have large auxiliary degree without changing the field of definition of the resulting point hy. Requiring h to be rational or quadratic would be an incorrect additional condition.
6. **A mislabeled V4 action or inverse action.** The normalizer realizes every labeling. Equivariance gives h^-1 sigma(h) acting as c_sigma, not c_sigma^-1. Its PGL2 cohomology class vanishes by construction. Thus the degree1 conclusion holds for every possible quotient cocycle.
7. **Small r, characteristic and boundary assumptions.** r=3 has an older stronger degree1 theorem; no universal-optimality claim for this r is made. r=4 includes special divisor automorphisms as well as proper cover-point stabilizers; all are covered by the subgroup classification. Collided branch points, r<=2, positive characteristic, compactification boundaries and the separate actual-cover obstruction are outside the stated theorem.

No hidden extra hypothesis was needed in any attack. In characteristic zero k is perfect and infinite, so all uses of separability, choice of a transverse line, choice of a cubic primitive element and algebraic-coordinate descent are legitimate.

## Checkable controls

Run `/Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python /Users/alec/Documents/Math/draft_pr_claimed_solved_600_700_20261012/audits/pr628_30000403/reviews/geometry_01/check_geometry.py`. The checker imports none of the supplied verifiers and passes41 named checks in SymPy1.14.0. It derives the two-torsion transformation directly from the elliptic chord law, verifies generic projective V4 products and nonsingularity on the distinct-root locus, constructs the24-element normalizer and its Galois-constant quotient, exercises all four cubic action images1/C2/C3/S3, and checks216 finite nonabelian coboundary identities.

These are exact algebraic or finite controls, not numerical approximations. They do not mechanically prove Hilbert90, the finite-subgroup classification, conic descent, all-field coarse-moduli facts, or the complete continuum argument; those are reviewed mathematically in DERIVATION.md. RESULTS.json records the scope and individual controls.

## Strongest verified conclusion and remaining work

For every characteristic-zero k containing the Hurwitz datum's field of definition, every k-rational reduced **inner coarse** Hurwitz point with r>=3 has an ordinary inner coarse lift over an extension of degree at most2. If its geometric cover-point stabilizer is V4, it has a lift already over k. No mathematical gap remains in that upper-bound family.

I read the six-branch C2 lower-bound argument for consistency with the objects above, but this family does not claim an independent replay of its15 j-values or arithmetic obstruction certificate. The parent's separate arithmetic family must establish the sharpness example before promoting the full word 'sharp'. Priority and the final preprint-package review remain separate required gates. The conic step and most non-V4 cases are classical consequences of the cited framework; the priority audit should focus especially on whether the all-S3 split V4 realization has already yielded the identical general Hurwitz statement. This observation is a priority-search direction, not an established prior-resolution claim.

This is an independent AI mathematical audit, unrefereed and not a formal certification or external human peer review.
