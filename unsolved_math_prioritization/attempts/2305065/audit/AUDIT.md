# Independent audit of Problem 2305065

## Verdict

PASS for classification `already_solved`, with the cited geometric dependency retained. The exact nonconstant existence question is answered affirmatively by the published Stegenga–Stephenson result, and the packet's supplementary argument correctly derives the needed conclusion from their geometric approximation lemma. No blocking mathematical defect was found. This is an independent AI-assisted adversarial audit, not human peer review or formal verification.

The prior-result verification remains 1/5 discovery turns. This audit neither claims a new solution nor spends another original-research turn. The frozen author artifacts were not revised. One nonblocking parameter-helper defect is recorded in `CORRECTIONS.md`.

## Frozen identity and reproducibility

Audited input: rank 578, problem 2305065, AMR-022-5065, Research Problems in Function Theory Problem 5.65.

Expected and observed author manifest SHA-256:

    22542408192501b6ff6f2c1cd3491cc529463fb0549283fa8164334dfb83012e

All six manifest entries have the recorded byte lengths and SHA-256 digests. Executing the frozen `check_controls.py` reproduces the parsed `CONTROL_RESULTS.json` exactly, with 48 checks passing. The script was also read; it performs finite rational arithmetic and model countercontrols, not an existence proof or a calculation of the exceptional set. An additional out-of-suite input exposes the minor helper-domain issue below. There are no source PDFs, extracted source text, or source images among the redistributable audit files.

## Source and target verification

Fresh independent downloads matched the recorded source hashes. Relevant pages were read and rendered for visual checking, avoiding OCR loss of closure bars and inequality signs.

- [Hayman–Lingham, Problem and Update 5.65](https://arxiv.org/pdf/1809.07200), printed page 109, PDF page 110: the target includes nonconstancy, membership in the disc algebra, and interior-image membership at almost every angular boundary parameter. The update is affirmative.
- [Stegenga–Stephenson 1985](https://msp.org/pjm/1985/119-1/pjm-v119-n1-p12-s.pdf), printed pages 227–228 and 231–234: the exceptional-set convention, explicit Problem 5.65 identification, Theorem 3.1, Lemma 3.2, and their proofs were checked. The geometric lemma gives a surjective disc-algebra self-map close to the identity with a small circle-contact set.

The retained original input record agrees with the book's target. Its earlier open-status summary contradicts the book's update. The claim should therefore be recorded as prior literature verification. Gol'dberg's separate construction is not needed and its proof was not audited. Repository duplicate searches and live catalogue status were not repeated in this mathematical audit.

Source hashes:

    SS1985: 8a85618f4bfa1e7087486b82ec0c1098e863c3e2a68c8ecb80830b6e6ded8c69
    HL2018: 8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0

## Exact theorem mapping

1. Every disc-algebra function has its stated continuous boundary value along every approach from the disc. The source's additional exceptional points for failure of nontangential limits therefore disappear. The remaining exceptional set is exactly the packet's E(f).
2. The choice h(t)=t is admissible under both the conventional gauge definition and the source's stated requirements. Zero corresponding Hausdorff measure implies zero angular measure. The packet's bound is correct: a covering disc of radius r meeting T is contained on T in a disc centered on T of radius 2r, and the resulting angular length is at most 4 arcsin(r) ≤ 2πr. Countable subadditivity yields the required outer-measure estimate. Radius versus diameter conventions change only a harmless factor.
3. The norm ball of radius 1/2 around the identity contains no constant. Evaluation at 1 and -1 proves every constant is at distance at least 1. Density therefore gives a nonconstant solution.
4. Normalized measure on T and Lebesgue measure on [0,2π) have the same null sets under the angular parametrization. No positive-measure boundary failure is concealed by notation.
5. The gauge is chosen before the function. Nothing established here supplies one nonconstant function for all gauges simultaneously.

## Independent check of the analytic deduction

### Persistence under perturbation

For nonconstant f and a covered boundary value f(ζ), an interior preimage a exists by hypothesis. The analytic function f-f(ζ) is not identically zero. An isolating circle about a can therefore be selected with closed interior in D and a positive minimum modulus b on the circle. The packet compares h-h(ξ) with f-f(ζ), rather than incorrectly holding the moving boundary value fixed. Its error bound is b/8+b/8+b/4=b/2<b. Rouché's theorem then guarantees an interior preimage of h(ξ). Compactness of K permits a finite cover and a common positive perturbation tolerance. This handles multiple interior zeros as well as simple ones. Empty K is a trivial vacuous case.

### Openness and the role of constants

The constants form a closed subspace C of A(D), so X=A(D)\C is open. An open subspace of a complete metric space is Baire. For f in X, the open mapping theorem makes f(D) open; hence E(f) is closed in T. Outer regularity provides a small open neighborhood O of E(f), and the compact-persistence result applied to T\O shows that sufficiently nearby functions have exceptional sets inside O. Taking the perturbation small enough to remain in X proves the asserted relative openness.

The restriction is essential. E(c) is empty, while E(c+εz)=T for every ε≠0. The packet explicitly identifies and repairs the source's openness-at-constants omission. Its corrected proof never applies the defective unrestricted statement.

The omission also does not invalidate the dense G-delta conclusion in the ambient disc algebra for the Lebesgue case. To see this independently, let U_N be the packet's open sets in X; they are open in A(D), since X is open. The success set in X is the G-delta set ∩_N U_N. Adjoining the closed set C preserves the G-delta property in a metric space: a finite union of G-delta sets is G-delta. Density follows from density in the dense subspace X. This supplies an explicit repair beyond what is needed for the existence question.

### Composition and density

The lemma's g is continuous on the closed disc and maps its interior onto D. Continuity implies g maps the closed disc into the closed disc, so f∘g is well-defined and continuous there; holomorphy of the composition holds in D. Uniform continuity of f turns uniform approximation g≈id into f∘g≈f. Surjectivity gives the exact equality (f∘g)(D)=f(D). It simultaneously ensures nonconstancy of f∘g when f is nonconstant and ensures that a boundary point with |g(ζ)|<1 is covered by the composition from the interior.

The contraction g(z)=rz, 0<r<1, correctly defeats the weakened, nonsurjective version: it has no circle contacts but all of T is exceptional for g. Thus the crucial image equality has not been replaced by mere inclusion.

The Baire intersection is nonempty and dense in X, and the inequalities m(E(f))<1/N for all N force measure zero. This completes the exact deduction conditional only on the cited geometric lemma and the standard analytic/topological theorems named above.

## Geometric dependency audit

The geometric input was checked in the primary proof, not inferred from its title. The surface construction, its projection, boundary extension, shrinking-neighborhood harmonic measure, and rotational normalization were examined for their roles. The following are independent consistency checks and explain the remaining proof boundary.

- Filling a slit by cross-gluing a supplementary sheet must restore points over the slit itself, including its interior endpoint. Without that fact, the projection need not cover D. Here the branch endpoint is an interior point of the constructed surface; the rest of the original disc remains covered. Surjectivity is consequently a substantive part of the construction.
- Uniformizing a simply connected surface by D requires its hyperbolic conformal type. A nonconstant bounded projection rules out the plane by Liouville's theorem and rules out the sphere. The boundary-continuity step additionally needs the claimed local Jordan neighborhoods or the equivalent prime-end extension result. Neither follows from surjectivity alone.
- Shrinking the added neighborhoods must force the outer-boundary harmonic measure at slit-side points to zero. Away from the finitely many tips/corners, a local barrier comparison in a thin neighborhood of an analytic slit gives the needed vanishing. Isolated exceptional boundary points have zero harmonic measure here. Bounded convergence against harmonic measure on the fixed slit domain then gives the limit at 0. These are standard potential-theory dependencies, not finite-control computations.
- The doorway estimate is strict: reaching the outer circle requires first leaving the inner disc through a doorway, and after that there remains positive probability of hitting a slit. This strictness is needed to choose a positive neighborhood thickness while preserving the desired upper bound.
- Rotational symmetry fixes equal parameter arcs only after normalizing the conformal map and adjusting its phase. Projected boundary pieces then control the boundary norm; the maximum principle passes that estimate into the disc. Harmonic-measure invariance identifies circle-contact measure with the outer-boundary harmonic measure.

No contradictory topological or analytic requirement was found. However, this audit has not supplied a fully detailed source-free uniformization, prime-end theory, barrier construction, or potential-theory development. The packet accurately discloses that level of imported dependence. Acceptance is as an application of an established published result, with its geometric lemma explicitly cited. It must not be relabeled as a new, elementary, constructive, or formally verified proof.

## Adversarial controls and limits

- Constants are excluded from the open-family proof and from the selected norm ball.
- A nonconstant solution cannot have an empty exceptional set: a boundary maximum-modulus value is not taken in the interior. The target only asks for a null exceptional set.
- A univalent disc-algebra function cannot work: its continuous inverse on the interior image would send f(rζ) toward an interior preimage while rζ tends to a boundary point.
- Small circle contact without surjectivity is insufficient.
- The cited theorem concerns a fixed gauge. The proof here uses only h(t)=t.
- The controls do not approximate a limiting analytic witness, measure an actual exceptional set, prove the imported geometric lemma, or formalize Baire/Rouché.
- Finite source verification does not certify every statement elsewhere in the 1985 paper. The separate slit-domain example and its twist-point theorem are not dependencies of this verdict.

## Corrections and release recommendation

There are no blocking corrections to the exact target proof. The general-purpose parameter helper should be hardened to enforce n≥2 for all positive epsilon. Its tested inputs are valid, so the reported 48/48 result remains true. An explicit n≥2 in the prose parameter choice would be clearer. See `CORRECTIONS.md` for the reproduced counterexample and optional changes.

Keep `already_solved`, the prior-result nature, the 1/5 discovery-turn accounting, the attribution, and the source-free-proof limitation visible. The frozen packet passes the mathematical audit in that scope. This verdict authorizes no remote action and does not verify a later modified packet.
