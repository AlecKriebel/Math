# Independent initial attack — full package 04

Saved at 2026-10-16T19:46:22.913422+00:00. No candidate note, original proof, assessment, verdict, report, helper source or helper stdout/stderr has been inspected. Pinned manifests were read as neutral shapes and hashed mechanically; preflight output remains unopened. This is a reconstructed attack, not a conclusion borrowed from the package.

## Primary statement and locator

I read question-neutral O.pdf physical one-based 118–121 as extracted full pages and rendered images. Printed 490–492 are physical 118–120; the alternative physical 119–121 includes printed 491–493 and therefore misses the first coefficient-ring page. Printed 490 defines R1 as the inverse limit of Z[q,q^{-1}] modulo (q−1)(q²−1)…(q^N−1). Printed 492 defines R1' as lim R1[t]/P_N(t), P_N=product_{j=1}^N(t−q^j), and asks for all n≥1, with rank one fixed to 1. There is no inverted q−1, factorial, rational rank interpolation, or shifted rank in this statement. The displayed natural map R1 to Z[[q−1]] is asserted injective. The adjacent update concerns 7.29, not 7.30.

## My mathematical mechanism: first jet of the diagonal formal curve

Set h=q−1 and work after the primary Taylor map in Q[[h]]. For a polynomial f(t) with coefficient series, q^n=1+n h mod h², so f(q^n)=f(1)+n h f_t(1) mod h². For an inverse-limit element, its reduction modulo P_2 has a representative f=a(q)+b(q)t of degree less than two. Compatibility at any higher stage changes this by a multiple of P_2. At every positive rank, P_2(q^n) has h-adic order at least two (and is exactly zero at ranks one and two), so the displayed first-jet formula remains valid at *every* fixed n. This is a finite quotient argument, not an unproved interchange of infinite sums.

Consequently the coefficient c_n=[h]I^{sl_n}(M) must be affine in n, and its constant term at h=0 must be independent of n. The rank-one convention forces c_n=(n−1)c_2. In particular c_3−2c_2+c_1=0. No torsion assumptions or division by q^a−q^b are required after applying the Taylor map.

A likely falsification comes from the usual theta/Casson first perturbative coefficient. With the standard long-root-length-two form on sl_n, contraction of the adjoint Casimir is proportional to h∨ dim(sl_n)=n(n²−1); a universal nonzero first-order manifold term would give c_n=K(M)n(n²−1). The rank triple (1,2,3) yields 0,6K,24K and second difference 12K, which conflicts with affine rank dependence whenever K≠0. Orientation reversal changes K's sign and cannot remove this nonzero obstruction. S³ and Casson-zero manifolds are boundary cases that this test does not exclude.

## Exact remaining bridge, not assumed solved

The algebraic affine-jet restriction above is proved. For a mathematical disproof of the primary conjecture I still need to verify from primary sources the normalization of the unified sl_n Taylor series and a concrete integral homology sphere with nonzero K, including q versus q^{1/2}, rank-one convention, orientation, S³ normalization, and that the same coefficient is obtained for n=2 and n=3. I have retrieved Le's primary QUANTUM.pdf (bibliography247), whose introduction explicitly distinguishes q from other authors' squared parameters, but I have not yet identified a displayed first-coefficient formula in it. The remembered theta/Casson bridge is currently a hypothesis to test, not certified input.

A second attempted route is root-of-unity rank collision: for order r, q^a=q^b if a≡b mod r, forcing equal specialized unified invariants. This could furnish a different counterexample, but I have no evaluated pair yet and do not count it as evidence. It is not legitimate to import positive-level SU(n) values at arbitrary small r without checking the primary domain.

## Planned post-boundary adversarial work

Check primary theta and unified/perturbative bridges; try failure of coefficient injectivity/continuity, characteristic or localization escapes, nonlinear rank and completion conventions; inspect package source/executable assertions and priority evidence only after this file is saved. A satisfactory outcome may be a valid narrow counterexample without novelty, topology-certification, or safety claims.

Checkpoint: 12% of entire-package review complete (authentication and independent necessary condition established; quantum bridge, package, operations, priority, histories, and final reauthentication remain).
