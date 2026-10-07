# Geometry and analysis follow-on triage (families 032–101)

Checkpoint: 2026-10-06 20:57 PDT. Triage completion estimate: 90%; mathematical validation of follow-ons not undertaken. Four strong corollary-level routes found. They assume correctness of the repository's stated results; this scan did not independently verify the base proofs. No external individuals contacted.

## Priority 1: Smooth even logarithmic Minkowski uniqueness; full even Lp uniqueness for 0<p<1

**Exact target.** For every n≥2, p∈[0,1), and positive smooth even f on S^(n−1), show there is a unique smooth positive support function h of an origin-symmetric strictly convex body satisfying h^(1−p) det(∇²h+h Id)=f. Also, for arbitrary full-dimensional origin-symmetric convex bodies K,L and 0<p<1, identical Lp surface area measures S_(K,p)=h_K^(1−p)S_K and S_(L,p) imply K=L.

**New input:** Family 091, even logarithmic Brunn–Minkowski inequality, exact TeX `preprints/The-logarithmic-Brunn-Minkowski-conjecture-September-23-2026/build/introduction.tex:21`, plus Lp corollary at line 55. Full dimension, origin symmetry, no smoothness restrictions for volume inequality.

**Mechanism:** The existing primary paper by He–Liu, https://arxiv.org/html/2510.21530v1, Theorem 4 (lines 155–161), explicitly transfers the Lp Brunn–Minkowski inequality for p∈[0,1) to uniqueness for positive smooth even data. This resolves the smooth logarithmic endpoint p=0, not only p>0. For 0<p<1 use the classical mixed-volume inequality and its strictness derived from the logarithmic endpoint to cover general convex bodies. The general conjecture is stated as Conjecture 9.4.4 in Böröczky's primary-author book https://www.renyi.hu/~carlos/Book-Brunn-Minkowski.pdf. For background also https://arxiv.org/abs/2210.00194.

**Boundary and gap:** Do NOT claim general nonsmooth p=0 uniqueness. Equal-volume boxes with the same coordinate normal directions have the same cone-volume measure, despite different side lengths. Smooth endpoint rests on the exact He–Liu theorem and needs an independent check of that external input. Remaining work is a theorem-chain check and short write-up, not a new central inequality. Source manuscript states volume and B-conjecture consequences but not this uniqueness result. Lean docs 091 describe log-BM only, not Minkowski uniqueness.

**Impact/tractability:** High impact within convex geometry, named long-standing conjecture; immediate-to-short corollary once both inputs accepted. Novel contribution is recognition and explicit theorem packaging, not a novel uniqueness mechanism.

## Downgraded: Rational Hodge conjecture for K3 moduli spaces and their mixed products

**Exact target:** Rational Hodge conjecture in every codimension for every smooth projective moduli space M of stable sheaves on a complex projective K3 surface, including Hilbert schemes S^[n], and arbitrary finite products of such M (allowing different K3 surfaces). Extend to smooth projective moduli of Bridgeland-stable objects on twisted K3 surfaces exactly within Bülles' hypotheses.

**New input:** Family 032, `preprints/The-rational-Hodge-conjecture-for-products-of-K3-surfaces-October-4-2026`. Its result covers arbitrary products of projective complex K3 surfaces.

**Mechanism:** Bülles https://arxiv.org/abs/1806.08284 proves h(M) is a direct summand of a finite sum of Tate-twisted h(S^k), for k≤dim M. Tensor these decompositions for products, use #032 on the resulting mixed products of K3s, and transfer algebraic cycles through the algebraic correspondences giving the direct-summand maps. Arapura https://arxiv.org/abs/math/0102070 supplies an older explicit Hodge-conjecture conditional reduction for Hilbert schemes and moduli of vector bundles.

**Boundary and gap:** Must retain smoothness, projectivity and actual moduli-space hypotheses. This does not automatically prove Hodge for every deformation of K3^[n]-type; nor does Hodge conjecture imply finite-dimensional Chow motive. Check twisted-object hypotheses and quasi-universal families in cited theorem rather than inventing a universal family. Independent algebra_groups audit found source duplication: `Algebraic-Kuga-Satake-correspondences-and-Hodge-conjectures-on-a-K3-quadratic-locus-September-30-2026/build/paper.tex:5214–5255` already contains conditional moduli-space/self-power corollaries; its extension criterion together with universal Kuga–Satake removes the condition. The new all-K3 mixed-product scope remains valid, but the mechanism and much of the headline are already in the source. Downgrade substantially for originality.

**Impact/tractability:** High algebraic-geometric visibility; short motive-theoretic transfer, but low incremental originality after the source-duplication check. Recommend as a completeness/application appendix, not a top independent research stream.

## Priority 3: Exact two-dimensional hypersingular Riesz energy constants

**Exact target:** For every s>2, prove C_(s,2)=ζ_Λ(s), where Λ is the covolume-one triangular lattice and ζ_Λ(s)=Σ_(v∈Λ\{0})|v|^(−s). Therefore for a smooth compact surface M of area A>0,

E_s(M,N) ~ ζ_Λ(s) A^(−s/2) N^(1+s/2),

with ordered-pair energy E_s=Σ_(i≠j)|x_i−x_j|^(−s). On the unit S² the leading constant is ζ_Λ(s)/(4π)^(s/2).

**New input:** Family 090; exact theorem `preprints/Universal-optimality-of-the-triangular-lattice-September-23-2026/build/sections/01-uniform-gaussian-theorem.tex:32` covers all locally finite centered-disk-density-one configurations and every completely monotone g(|x−y|²). Take g(t)=t^(−s/2), summable at infinity precisely for s>2. The paper already treats planar infinite energy, renormalized 0<s<2 energy, and logarithmic spherical next-order energy. The finite hypersingular constants are not stated as such; corpus searches for `poppy` and `hypersingular` gave no relevant hit.

**Mechanism:** Existing poppy-seed bagel theorem gives existence of C_(s,2), universality across surfaces, and the lattice upper bound. For lower bound, periodize scaled finite square near-minimizers with an ε√N gap between √N boxes. The cross-cell energy per particle is O_ε(N^(1−s/2)), which tends to zero. Rescale the periodic configuration to density one, apply #090, then N→∞ and ε→0. This is a short boundary/tail argument; preserve ordered-pair convention and covolume normalization. Then apply Hardin–Saff's manifold theorem.

**Primary literature:** Hardin–Saff's original explicit constant conjecture is in https://www.math.vanderbilt.edu/saffeb/texts/201.pdf (Notices AMS 2004). Brauchart–Hardin–Saff https://www.math.vanderbilt.edu/saffeb/texts/235.pdf, Conjecture 2, states the lattice constant in d=2,4,8,24. The universality theorem is https://doi.org/10.1016/j.aim.2004.05.006 or arXiv:math-ph/0311024; use its corrigendum if treating the full rectifiable-set generality. Start with smooth compact surfaces to keep hypotheses transparent.

**Boundary and gap:** This does not prove microscopic uniqueness/crystallization of all finite minimizers. Family 090 itself explicitly identifies minimum values, not all minimizers. Avoid the critical s=2 case, whose N²log N leading asymptotic is already known. Avoid claiming this proves all BHS second-order terms for 0<s<2 on arbitrary manifolds.

**Impact/tractability:** Strong clear quantitative result spanning all surfaces and all s>2. Some technical write-up beyond a one-line corollary but no central conjecture remains.

## Priority 4: Costa's polynomial-retract question over C is false

**Exact target:** Construct a C-algebra retract of C[x1,…,x5] of transcendence degree four that is not a polynomial C-algebra. Equivalently, exhibit a smooth affine fourfold which is a scheme retract of A⁵ but is not A⁴.

**New input:** Family 047 has A=C[p,s,u,F,J]/(H), x=s²+u³+p²F, H=x²F−(1+2sx)J−p²J²−pu; A[w]≅C^[5] but A≄C^[4]. Exact source `preprints/An-explicit-failure-of-complex-affine-space-cancellation-September-23-2026/build/sections/01-introduction.tex:49–70`.

**Mechanism:** A→A[w] is the coefficient inclusion and ev_(w=0):A[w]→A is its C-algebra retraction. Conjugate by the stated polynomial-ring isomorphism. On spectra this gives a section Spec A→A⁵ and a retraction A⁵→Spec A. Since A[w] is smooth, A is smooth. No extra structure or unknown theorem required.

**Literature:** Costa asks whether every k-retract of k^[n] is polynomial. Nagamine https://arxiv.org/abs/1811.04153, Proposition 1.4, explicitly observes that a positive answer in n+1 variables implies cancellation for A^n; that paper establishes only the n=3 characteristic-zero case. https://www.sciencedirect.com/science/article/pii/S0022404926002185 explicitly describes the question as open in characteristic zero before this new input.

**Boundary and gap:** This is a negative answer over C in ambient dimension five; it does not settle the four-variable retract problem. Abstract isomorphism suffices for an existential counterexample. A five-polynomial explicit idempotent endomorphism requires extracting the source's stabilization isomorphism, which is more work but no new conceptual obstruction. Source #047 has no `retract` occurrence; no related Costa polynomial-retract conclusion found in corpus TeX.

**Impact/tractability:** Very fast named-conjecture consequence. Best as a clear corollary note bundled with other consequences; claiming an independent major breakthrough would overstate novelty.

## Verification limits and rejected jumps

Comparator files are statements, not certification: `lean/ComparatorChallenges/ComplexCancellation.lean` ends `theorem main : MainStatement := by sorry`. That may be intentional benchmark scaffolding; the corresponding actual solution tree must be checked separately. We did not run Lean.

Do not market general Hodge conjecture from CM-only abelian Hodge; generalized Hodge does not follow from ordinary Hodge. Fujita freeness does not by itself settle sharp very ampleness. Nagata does not by itself settle SHGH interpolation. The sharp simplex isotropic constant bound does not automatically settle KLS. Log-BM does not give unrestricted nonsymmetric inequalities. No conclusion here treats those central gaps as routine.

## Independent audit of Lane–Emden stream (#370)

Checkpoint: 2026-10-06 21:03 PDT. Triage completion estimate: 100%. Read local exact Corollary lane-emden and PQS primary PDF https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf. The transfer passes for n≥3, p,q>1, strict unweighted subcritical hyperbola. Theorems 4.2 and 4.3 require only bounded entire nonnegative Liouville nonexistence and deliver zero-Dirichlet half-space nonexistence, universal distance estimates, and exterior decay. Strong maximum principle converts any nontrivial nonnegative entire solution into a strictly positive pair, so #370 supplies the input. For bounded-domain Dirichlet uniform estimates require a fixed bounded C²/suitably smooth domain; boundary flattening and rescaling produce a bounded half-space solution, excluded by Theorem 4.2. Do not infer boundary uniformity directly from dist-to-boundary estimates. Theorem 7.3 covers continuous nonlinearities asymptotic to positive multiples of powers; x-dependent coefficients need a separate adaptation. No automatic extension to p≤1, q≤1, the critical hyperbola or weighted-subcritical boundary ranges.
