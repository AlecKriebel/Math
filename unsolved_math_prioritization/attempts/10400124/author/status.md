# Status and scope audit

Problem ID 10400124; AMR-103-0124; reviewed 2026-10-06.

## Decision

**PARTIAL / FORMULATION OBSTRUCTION.** The authored proof establishes an exact missing-phase phenomenon for L(25,2) and an infinite family of lens spaces. It proves the growth formula for #^g(S¹×S²). It does not settle the conditional conjecture for all manifolds or all groups. These derivations use classical formulas, and there is no claim of novelty or exhaustive literature coverage.

The literal all-phase nonzero-amplitude formulation inherited from Conjecture 7.7 cannot hold for the lens-space family described in the proof. A corrected problem record should specify whether zero sectors are excluded, assigned formal exponents, or given an extended-valued order. A formal exponent attached to a zero coefficient is not an observable invariant.

## Original context recovered

The publisher PDF was retrieved in full. Conjecture 7.9 is on printed page 478, PDF page 106 (one-based), with its important follow-up remark on printed page 479. Section 7 begins with a semisimple compact group, connections on the trivial bundle, a closed oriented three-manifold, and integral level k. The shifted parameter is r=k+h∨. The rigorous normalization is Z=τ(M)/τ(S¹×S²). The SU(2) setting used in our proofs is unambiguous and needs no extension to non-simply-connected gauge groups or nontrivial bundles.

Conjecture 7.7 sums by distinct Chern–Simons values, with rational exponents and integer-step corrections. Its error after order E is O(r^(d−E−1)), d the greatest exponent. Its amplitudes are strictly positive times a phase. Conjecture 7.9 takes a generic Zariski-open maximum of h¹−h⁰, not a pointwise maximum. The source warns about degeneracy; the subsequent −Id torus example explains why the generic qualification is essential. [Original source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The exact source text is not reproduced in this package. The live problem URL returned HTTP 403; no claim is made to have inspected its live contents. The supplied complete problem record and its associated review were checked against the expected hashes.

## Primary literature checked

1. Lisa C. Jeffrey, *Chern-Simons-Witten invariants of lens spaces and torus bundles, and the semiclassical approximation* (1992). Theorem 3.4 gives the all-level exact lens-space formula; equation (5.3) identifies the classical phases. We inspected the scanned formula to avoid OCR errors. These established results are the input to our elementary cancellation argument. [Primary paper](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/jeffrey.pdf).

2. Jørgen Ellegaard Andersen, *The Witten-Reshetikhin-Turaev invariants of finite order mapping tori I*, arXiv:1104.5576v1. Theorems 1.1 and 1.2 state the asymptotic expansion and growth-rate results for finite-order mapping tori in the paper's geometric-quantization setting. Its introduction distinguishes that construction from its identification with combinatorial WRT invariants. These are established special-case results, not a resolution for arbitrary manifolds. [Primary manuscript](https://arxiv.org/abs/1104.5576).

3. Andersen and Søren Fuglede Jørgensen, *On the Witten–Reshetikhin–Turaev invariants of torus bundles*, arXiv:1206.2552v2. Theorem 3.3.2 proves the SU(2) growth formula for the trace-two family studied there; Theorem 3.4.2 records AEC formulas for all torus bundles. AEC scope must not automatically be relabeled as growth-equality scope. Remarks 1.1.2–1.1.3 discuss two-framing independence of the exponents. [Primary manuscript](https://arxiv.org/abs/1206.2552).

4. Andersen, Li Han, Yong Li, William Elbæk Mistegård, David Sauzin and Shanzhong Sun, *A proof of Witten’s asymptotic expansion conjecture for WRT invariants of Seifert fibered homology spheres*, arXiv:2510.10678v1, dated 12 October 2025. Theorem 1.1 proves an AEC for the indicated integral homology spheres and bounds the degrees of nontrivial-sector polynomials by half the maximum component dimension. The introduction describes this bound as consistent with the growth conjecture; it does not assert general equality. Its normalization has WRT(S³)=1, so the shift of 3/2 discussed in our proof is required. [Primary manuscript](https://arxiv.org/abs/2510.10678).

A bounded current search did not locate a general proof or a direct treatment of the exact missing-phase example. That negative search result is not evidence of novelty or a definitive claim about the current global status.

## Bounded approaches and stopping point

Three substantive approaches were used:

1. Same-phase cancellation in the exact lens-space formula: successful. The result is an all-orders missing sector, with its logical scope carefully separated from a counterexample to a conditional assertion.
2. Free-group local-system cohomology and TQFT connected sums: successful. This gives an exact infinite positive family, including reducible representations.
3. Componentwise stationary-phase aggregation: produces a precise conditional noncancellation criterion, but supplies no general stationary-phase construction or noncancellation theorem.

No fourth or fifth mathematical approach was needed for this bounded partial-result package. The five-approach limit was not exceeded.

## Checks and limitations

- Proofs use exact roots-of-unity identities, elementary representation cohomology, and explicit TQFT identities; they do not depend on floating-point fits or a finite search.
- The source formula, original conjecture page, normalization, phase-index relabeling, all-level scope, and fixed-framing behavior were checked.
- L(25,2) has a finite phase fiber. The nonempty-open generic maximum cannot discard its noncentral classes.
- The absent sector has no leading exponent. Calling it d=−∞ is an optional added convention, not the original rational-exponent definition.
- No executable checker is part of this package. Runtime optimization, import-shadow, cache, root and entrypoint replay tests are therefore inapplicable to the deliverable. The proof is intended for independent mathematical review.
- This is an author freeze. Independent mathematical acceptance and publication are not claimed here.
