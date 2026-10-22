# Problem 2807 / KP-3.9: Haken manifolds and finite quotients

**Outcome: unsolved, 5/5 substantive approach passes.** No complete proof or counterexample is claimed. This is a research attempt and source audit, not a resolution or a novelty claim. The five passes below are distinct mechanisms, not five independently verified solutions.

## Exact target and conventions

Given 3-manifolds M and N with isomorphic profinite completions of their fundamental groups, does the assumption that M is Haken imply that N is Haken? This is Problem 3.9, printed page 138, in *K3: A New Problem List in Low-Dimensional Topology*, edited by R. İ. Baykur, R. C. Kirby and D. Ruberman (AMS, 2026). The companion Problem 3.8 asks for profinite rigidity of finite-volume hyperbolic 3-manifolds.

We use the intended compact, orientable, irreducible 3-manifold setting, with the usual boundary-incompressibility conventions when a boundary is present. In the closed setting, Haken means containing a two-sided, positive-genus, incompressible embedded surface. Our proofs below concern the closed case unless another domain is explicit. We do not exploit omitted hypotheses in the one-sentence catalogue formulation, introduce punctures, or change the meaning of Haken to 'virtually Haken'.

The unresolved central case is a closed hyperbolic Haken rational homology sphere M versus a closed hyperbolic rational homology sphere N. No pair with different Haken behavior and isomorphic profinite completions has been produced here.

## What was established

The self-contained proofs are in `proof.md`.

1. The profinite completion of a finitely generated group determines its abelianization and the first Betti numbers of its corresponding finite-index subgroups. In the closed irreducible 3-manifold setting, positive first Betti number gives an essential surface.
2. For every finitely generated group G, an epimorphism G → D∞ exists exactly when some index-two subgroup H satisfies b₁(H) > b₁(G). Consequently, this particular quotient property is profinitely invariant. This is a special sufficient mechanism, not a characterization of all Haken 3-manifolds.
3. The existence of a positive-dimensional SL₂-character variety over an algebraic closure of a finite field is profinitely invariant. The proof carefully distinguishes characters from conjugacy classes and algebraic closures of finite fields from arbitrary fields of positive characteristic.
4. A negative trace valuation obstructs a fixed vertex in a Bruhat–Tits tree. An exact polynomial control certifies the nonintegrality of every root of one literature trace polynomial; it does not independently identify that polynomial as a trace in a particular manifold.
5. An explicit closed direct summand of the completion of Z² has trivial intersection with the dense Z². This disproves a tempting general subgroup-pullback inference, without giving a 3-manifold counterexample.

These proofs are elementary reconstructions and route controls. No priority is asserted.

## Updated literature and caution

Cheetham-West–Lê, [arXiv:2603.22543v1](https://arxiv.org/abs/2603.22543v1), Theorem 1.3, proves Haken invariance under extra hypotheses involving virtual fibers, signed covering homology, dihedral quotients, character curves, or nonintegral algebraic traces. Its Section 6 still isolates a general obstruction. This March 2026 preprint was absent from the pinned catalogue's literature triage. It supplies substantial known partial progress, not a full solution.

Garden–Tillmann, [arXiv:2411.06859v2](https://arxiv.org/abs/2411.06859v2), proves the positive-characteristic tree/surface theorem and reports an example outside the character-curve mechanism. Two numerical inconsistencies in its §6.3 were found and are documented in `source_checks.md`. They do not establish that the paper's qualitative conclusions are false. We do not certify the example from its inconsistent displayed presentation.

General-group failures of property FA do not resolve the question among 3-manifolds. Nor does the virtual Haken theorem imply that Haken-ness descends from a finite cover.

## Reproduction and limits

Run `python3 controls.py` with Python 3.10 or later; only the standard library is used. It checks cover-chain calculations for four explicit presentations, finite SL₂ matrix relations over F₂/F₃/F₅, a mod-7 irreducibility certificate, the mod-43 repeated-root issue, the displayed abelianization mismatch, and bounded CRT shadows of the dense-intersection example. Expected output is in `controls-output.json`.

These are exact finite controls. They neither compare all finite quotients of hyperbolic manifold groups nor certify an essential surface in a census triangulation. The universal lemmas require the written proofs. No SnapPy or Regina computation, exhaustive manifold census, theorem-prover formalization, or independent referee review is represented as performed.

`approach_log.json` records the five passes and exact remaining gaps. `provenance.json` gives source versions and hashes. `SHA256SUMS` binds the public attempt. Source PDFs and imported datasets are excluded.

Best-guess progress toward a full resolution of the exact target: **5%**, a subjective planning estimate, not a probability of correctness. Evidence does not presently support promotion to claimed_solved or already_solved.
