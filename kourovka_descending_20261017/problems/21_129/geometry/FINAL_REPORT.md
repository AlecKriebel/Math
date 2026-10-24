# Geometry family: bounded research report

Completed 2026-10-24. The full question remains unresolved; no residual pair was distinguished by a proved QI invariant, and no quasi-isometric noncommensurable spherical pair was constructed.

## Strongest checkable deductions

1. **Raw maximal-parabolic coset preservation is false.** A self-QI of `B4/Z(B4)`, induced by conjugation of its normal pure finite-index subgroup by a sphere mapping class swapping the distinguished puncture, sends a standard `A2` parabolic outside finite Hausdorff distance from every raw maximal-proper-parabolic coset. The rational-homology certificate separates all candidate embeddings. This concerns **internal** commensurability only: the image remains abstractly commensurable with `A2` by construction. Proof: `PARABOLIC_PRESERVATION_COUNTERMODEL.md`.
2. **Maximal abelian group retracts.** Every irreducible rank-`n` pure central quotient `Q` has a retract `Z^(n-1)`, split by differences of reflection-hyperplane winding coordinates. The pairing matrix with nested parabolic full twists is exactly the identity. Proof: `NESTED_CENTRAL_RETRACTS.md`.
3. **Ordinary filling is uniformly quadratic in the residual range.** From the preceding retract and the pure central splitting of a finite-index subgroup of a biautomatic spherical Artin group, both `Q` and `A/Z(A)` have quadratic ordinary Dehn function for `n>=3`. Rank two is virtually free and linear; rank one has trivial central quotient. Thus ordinary filling cannot distinguish any of the four residual pairs.

`check_certificates.py` passed all exact rational homology separations, `D/E` tree-deletion enumerations, and nested-twist pairing matrices for ranks two through nine, writing `CERTIFICATES.json`. Finite checks supplement, rather than replace, the general proofs.

## Routes and precise remaining gaps

- The finite raw deletion signatures distinguish all four residual pairs **as raw parabolic families**, but the family itself is not QI invariant by deduction 1. This route is blocked. Reopening requires a materially different intrinsic family and proof that its enlarged patterns preserve a distinguishing signature.
- Ragosta's marking graph is a geometric model, not a quasiflat/QI-recognition theorem. A classification proof would still need product-region or orthant reconstruction and sufficiently rigid incidence data. Hyperbolicity/acylindricity of the parabolic complex and an HHG structure cannot be assumed from that paper.
- Strongly contracting Morse axes exist uniformly; the type-dependent topology or stable dimension of the Morse boundary remains uncomputed here. Existence alone separates none of the residual types.
- The fresh pre-cutoff profinite-rigidity papers do not supply a QI or finite-index bridge. The newest source was handed to the root researcher for a separate audit.

Full mechanism inventory: `GEOMETRIC_MECHANISMS.md`. Timestamps, hypothesis boundaries, and completion estimates: `RESEARCH_LOG.md`.

Bounded geometry-family probe: 100% complete. Best-guess progress toward the full discovery goal: 6%, with no complete-resolution or novelty claim. Independent adversarial review was requested for both proof artifacts; the root researcher is to retain its final disposition before promotion.

No external communication, branch changes, commits, pushes, releases, or publication actions were undertaken by this family.
