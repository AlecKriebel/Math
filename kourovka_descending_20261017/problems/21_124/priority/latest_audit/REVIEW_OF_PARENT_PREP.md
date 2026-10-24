# Fresh source-and-scope review of parent preparation

UTC: 2026-10-24 22:05. Review completion estimate: 100% of this quick assignment; discovery estimate for 21.124: 0%.

Reviewed frozen inputs:

- SOURCE_CONTRACT.md SHA256 `0ffe364f212e36d946ebddcbd8a595a017bad6c1f8c4659d9f9d1318ca9e75bb`.
- PRIORITY.md SHA256 `abb7464ba876fecce30bd3e190d9b2e655a9c12ea9637ee593c780bb41e526a9`.

**Verdict:** the provisional-eligibility recommendation is supported by the inspected sources. No full solution has been established. One scope clarification is requested before treating the prose as final: display Delage's exact normal form rather than leaving the phrase “relevant unipotent polynomially growing automorphism fixing a rank-two factor” implicit.

## Requested clarification

[Delage2602.08759v3](https://arxiv.org/html/2602.08759v3), dated26March2026, Theorems1.1(1) and1.2(1), give the dichotomy for

φ(a)=a, φ(b)=b, φ(c)=c w(a,b).

In that displayed family, CAT(0) holds iff w=1 or w∉[F₂,F₂]. Nontrivial commutator twists fail even proper semisimple CAT(0) actions. This supports the intended paragraph, but “fixes a rank-two factor” without the normal form can be read as a broader condition allowing two-sided twists or partial conjugations. This review does not certify such a broader extension. Add the display and theorem numbers to eliminate the ambiguity. No new theorem or proof repair is involved.

## Checks that passed

- The Notebook transcription matches the parent's cached official text around21.124. The text neither imposes compactness nor explicitly specifies finite free-kernel rank. Its “weaker” wording is accurately recorded rather than silently repaired.
- [Linton2510.10178v2](https://arxiv.org/html/2510.10178v2), dated22April2026, Theorem1.2 explicitly gives the finite-rank ambient embedding and retraction for finitely generated free-by-Z groups. Corollary1.4 gives the hyperbolic ambient/quasiconvex conclusion when the original group is hyperbolic. Corollary1.5 explicitly gives virtual compact specialness of every hyperbolic free-by-cyclic group. The introduction explicitly permits infinite-rank free kernels. The parent correctly does not assert CAT(0) ambient preservation in the general embedding theorem.
- The corrected [Haglund–Wise primary text](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf), Definition3.2, Corollary3.8, Proposition3.10 and Theorem4.2, supports the A-special/special distinction and the finite-walls hypothesis warning. The parent labels root's parity-cover argument as a separate deduction awaiting its own review. This quick review does not verify that deduction.
- The single-vertex restriction in Wu–Ye, the tubular(VRC) and balanced cycle-disjoint prior subclasses, and the exclusions for Gersten and cocompact-only obstructions match the primary scopes checked in my independent audit.

Minor clarification only: positive-characteristic nonlinearity would indeed obstruct virtual RAAG embedding, using RAAG positive-characteristic linearity and finite-index induced representations. The parent's separate caution that it does not refute characteristic-zero linearity is correct, but should not be read as making that obstruction irrelevant to21.124. The decisive exclusion for Button's example is its failure to be CAT(0).

Limits: source/scope audit only. No independent proof audit of cited theorems, no audit of root's new deductions, no exhaustive priority certification, no publication clearance. No parent file was edited.
