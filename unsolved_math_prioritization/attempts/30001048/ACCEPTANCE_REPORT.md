# Acceptance report: correct partial reduction only

Problem 30001048 / OWR-2089-004. Date: 2026-10-10 UTC.

**Accepted as a correct partial reduction. The conjecture remains unresolved at Approach 1 of 5.** This report and the underlying authored mathematics are AI-assisted and unrefereed. This is an internal mathematical audit, not external peer review, a novelty certification, or a proof-assistant-checked theorem.

## Scope of acceptance

Acceptance covers [PROOF_ATTEMPT.md](PROOF_ATTEMPT.md), together with the supplied explanations in [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md) and [CORRECTION_PRECISION_LEDGER.md](CORRECTION_PRECISION_LEDGER.md). The exact edition members are identified by [MANIFEST.json](MANIFEST.json).

1. The full cusp stabilizer equals the marked peripheral P, and P is a rank-two parabolic lattice. The normalized generator has nonzero lower-left entry and can be written g=[[s,−1],[1,0]].
2. L={(0,t):t>0} has trivial setwise stabilizer and represents the marked core's proper homotopy class. Its projected ends go to unbounded cusp depth, using g(0,t)=(s,1/t), so its projection is proper.
3. For h=[[a,b],[c,d]]≠1, L and hL have an interior intersection exactly when bc∈(−1,0). Every zero-entry, ideal-endpoint, stabilizer, and quotient exception is accounted for.
4. The Shimizu–Leutbecher consequence excludes peripheral witnesses and pγq or pγ⁻¹q with p,q∈P. The elementary Chebyshev level-set argument excludes (pγ)ⁿ for every p∈P and n≠0.
5. The path route is accepted only as a conditional implication under marking-compatible identifications and a proper embedded family throughout the entire compact parameter interval.

The algebraic and cusp deductions do not require minimal parabolicity or a loxodromic marked generator. The audit's accidentally parabolic endpoint argument is explicit and is not misattributed to the narrower wording of Lackenby–Purcell Lemma 4.8. The audit also treats shifted-generator trace values ±2 in the power argument.

## Exact limits

No arbitrary reduced mixed-word interval-avoidance theorem is accepted. No unconditional proof that the proper homotopy representative is in the prescribed core isotopy class is accepted. No extension of a future minimally parabolic path proof to every geometrically finite endpoint is accepted.

The exact matrix h₀=[[2i,1/2],[−1,−i/4]] has determinant one, trace 7i/4, bc=−1/2, and L∩h₀L at height 2. It refutes only a purely algebraic shortcut based on loxodromicity. No required discrete faithful compression-body representation containing that matrix is supplied, so it is not a counterexample to the conjecture.

The multi-handle construction of Burton–Purcell uses independent handle generators and requires at least two handles. Its formal one-handle specialization claims zero self-intersecting tunnels. Replacing an independent handle by a peripheral generator does not preserve the hypotheses.

## Attribution and status

The original conjecture is Purcell's [Oberwolfach question](https://ems.press/journals/owr/articles/2089). The homotopy/Ford-spine/path context is credited to Lackenby–Purcell, [Geodesics and compression bodies](https://arxiv.org/abs/1302.3652). The discreteness estimate and multi-handle construction are credited to Burton–Purcell, [Geodesic systems of tunnels in hyperbolic 3-manifolds](https://arxiv.org/abs/1302.5469). Full citations and bounded source-review history appear in the source ledger. No novelty or general solution is claimed.
