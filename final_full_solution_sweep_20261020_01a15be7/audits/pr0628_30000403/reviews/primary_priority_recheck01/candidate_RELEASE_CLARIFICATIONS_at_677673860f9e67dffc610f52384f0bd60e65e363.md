# Reviewed scope and release clarifications

Problem 30000403 / OWR-1188-004. Current disposition: **claimed_solved, 3/5**. The independent AI adversarial audit passed with nonblocking presentation and literature notes; no mathematical correction was required. This separate note applies all five recommendations in [CORRECTIONS.md](audit/CORRECTIONS.md). It does not alter any frozen author or audit bytes. Historical references to pending review in the author packet are preserved as historical status, superseded by the completed [audit](audit/AUDIT_REPORT.md).

## 1. Groups with Galois action

In the V4 argument, the intended description of the conjugation isomorphism N/E0 → Aut(E0) is **an isomorphism of groups with Gamma_k-action**. Neither quotient notation intrinsically designates the Galois group of a particular named extension. The quotient is the constant S3, whereas the normalizer itself need not be constant or admit a Galois-equivariant section. The frozen proof's wording “Galois groups with action” is to be read in this precise sense.

## 2. Auxiliary coordinates versus the descended point

The auxiliary field needed to define h need not have small degree; the point h p0, rather than h itself, is fixed over k. In the V4 construction, the conjugating projective transformation h can therefore require a larger auxiliary field without changing the degree-one conclusion for the ordinary coarse Hurwitz point. The proof constructs the appropriate normalizer cocycle with trivial PGL2 class and uses the stated coarse-point lifting criterion.

## 3. Apparent older cubic-descent counterexample

The older Fuertes–González-Diez real cubic-descent assertion should be read together with their [2013 erratum](https://link.springer.com/article/10.1007/s00013-013-0582-4) and [author corrigendum](https://verso.mat.uam.es/~gabino.gonzalez/Corrigendum.pdf). The corrected statement restricts the field of definition of the descent isomorphism; that extra restriction is absent from this coarse-point problem. Lercier–Ritzenthaler–Sijsling, [section 3D, printed pp. 483–484](https://msp.org/obs/2013/1-1/obs-v1-n1-p23-s.pdf), independently identifies the error and descends the cited genus-five family to Q. These contextual corrections remove the apparent contradiction. Their large formulas are neither reproduced here nor used as dependencies of the proof.

The audit read the corrigendum's indexed text, but direct PDF byte retrieval failed; no PDF hash is asserted for it. Related Hidalgo manuscript status is recorded in the audit only as publication history, not as evidence of priority or invalidity.

## 4. Exact universal-constant scope

For characteristic-zero fields k containing the field of definition of the fixed Hurwitz data, and r >= 3 distinct branch points, every k-rational reduced **inner coarse** Hurwitz point has an ordinary coarse lift over an extension of degree at most two. The universal constant two is attained over Q by the explicit six-branch C2 example. The V4 geometric base-stabilizer stratum has degree one.

This does not determine the optimal bound separately for every fixed k, G, C, r, or individual point. It does not assert that actual marked G-cover objects always descend over the same extension when a central field-of-moduli obstruction remains. No positive-characteristic conclusion is asserted.

## 5. Review, reproducibility, and priority

The completed review is an **independent AI audit**, not external human peer review or formal certification. AI tools were used extensively in research, proof writing, exact computation, adversarial review, and preparation. This work is unrefereed. The bounded literature search establishes no novel priority claim. Cadoret and the classical results used by the proof remain credited dependencies.

The finite controls check the explicit certificates and generic identities. They do not mechanically prove the full descent theorem, the finite-subgroup classification, Hilbert 90, or existence and effectivity of the coarse moduli spaces. The audit separately reviews the mathematical argument.

The audit freshly retrieved and hash-matched the two principal PDFs. Its unsuccessful live catalogue retrieval did not independently rehash the entire catalogue corpus or re-audit historical queue-readiness assertions. Such global-corpus and historical readiness metadata remain explicitly author-supplied. [LIVE_GATE.json](LIVE_GATE.json) separately records current repository checks performed for this draft PR.
