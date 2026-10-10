# Real-spectrum classification for compactly supported Nijenhuis operators

Authored mathematical proof, 10 October 2026. Target: AMR-020-0509 / problem 2100509. This manuscript gives a torus-collar construction and direct verification. This AI-assisted manuscript is unrefereed; it claims neither bibliographic priority nor external human peer review, journal acceptance, or formal proof-assistant certification.

## Statement and exact scope

For every integer n >= 1, a real Segre/Jordan type is realized on a nonempty open subset of R^n by a globally C-infinity, compactly supported real Nijenhuis (1,1)-tensor if and only if every eigenvalue in that type is real.

There is no restriction on real eigenvalue multiplicities, equality patterns, number of Jordan blocks, or sizes of Jordan blocks. In fact, any specified real Jordan matrix, including its numerical real eigenvalues, can be attained as the matrix of the tensor in a smooth commuting local frame on the realization domain. The type and eigenvalues are allowed to change outside that domain.

This is a smooth statement. It does not assert any nonzero real-analytic compactly supported tensor, nor that the type remains regular outside the realization domain.

## 1. The collar identity, checked directly

Let m = n-1 and work on T^m x (-1,1), with its standard globally defined commuting angular fields e_1,...,e_m and transverse field e_n = partial_t. Angular coordinate functions themselves need only exist locally; the invariant fields and their dual 1-forms exist globally.

Choose smooth functions A(t) in Mat_m(R), b(t) in R^m, and lambda(t) in R. Define

    L e_i = sum_k A_ki(t) e_k              (1 <= i <= m),
    L e_n = sum_k b_k(t) e_k + lambda(t)e_n.

Use N_L(X,Y) = L^2[X,Y] + [LX,LY] - L[LX,Y] - L[X,LY].

For angular pairs e_i,e_j every bracket in this expression is zero. For e_i,e_n, the only nonzero intermediate brackets are

    [L e_i, L e_n] = -lambda A' e_i,
    [L e_i, e_n] = -A' e_i.

Thus

    N_L(e_i,e_n) = (A-lambda I) A' e_i.             (1)

There are no b or b' terms. Since the e_i form a frame and N_L is tensorial and skew-symmetric, these calculations account for every component. Consequently L is Nijenhuis exactly when

    (A-lambda I) A' = 0.                            (2)

Neither A nor A' is assumed invertible or of constant rank.

## 2. A finite smooth path from any real Jordan matrix to zero

Put a chosen real Jordan representative J in upper-triangular block diagonal form, using superdiagonal entries 1. Put the last vector of one Jordan block in position n. Then

    J = [[A_0,b_0],[0,lambda_0]],

where A_0 is again block diagonal with real Jordan blocks: the distinguished block is shortened by one, or disappears if it originally had size one.

We construct a smooth path (A(s),b(s),lambda(s)), 0 <= s <= 1, from (A_0,b_0,lambda_0) to (0,0,0), constant near its endpoints, satisfying (A-lambda I)dA/ds = 0 throughout. Allocate disjoint successive subintervals to the following finitely many operations. Perform each interpolation by a C-infinity switching function that is constant near both endpoints, so concatenation is smooth.

First hold A and lambda fixed and change b from b_0 to zero. This satisfies (2), since A'=0.

Now process each Jordan block of A_0, one at a time. Previously processed blocks remain zero, and as-yet unprocessed blocks retain their initial constant matrices.

For the current block mu I_r + K, first hold A fixed and move lambda to the real number mu. This again satisfies (2).

Write K = sum_{j=1}^{r-1} a_j E_{j,j+1}, with all a_j initially equal to 1. Keep lambda=mu. Change a_1 from 1 to 0, then a_2 from 1 to 0, continuing in this order through a_{r-1}. At every stage only one coefficient changes, and

    K K' = sum_{j=1}^{r-2} a_j a'_{j+1} E_{j,j+2} = 0.   (3)

Indeed, for a'_{j+1} to be nonzero, a_j has already been set identically to zero. The derivative of a_1 has no preceding coefficient. All blocks other than the active block have zero derivative, so (A-lambda I)A'=0 for the whole matrix.

After these operations the active block is mu I_r. Move its scalar value from mu to zero while moving lambda by exactly the same scalar function. During this operation A' is supported in this block, and A-lambda I vanishes on that block. Equation (2) still holds. This includes blocks of size one, for which the arrow-removal step is empty.

Repeat for every block. At the end A=0, b=0, and lambda=0. If the list of blocks is empty, simply move lambda to zero while keeping A empty. Additional constant subintervals near the two endpoints give the claimed endpoint plateaus.

All eigenvalue crossings and Jordan-type changes in this path are permitted by the problem. No division by an eigenvalue or eigenvalue difference occurs.

## 3. Compactification in the transverse direction

Choose a smooth even function q:(-1,1)->[0,1] equal to 0 for |t| <= 1/4 and equal to 1 for |t| >= 3/4. Substitute s=q(t) in the preceding path. The chain rule preserves (2), since

    (A(q)-lambda(q)I) d_t A(q)
       = q'(t) (A(q)-lambda(q)I) d_s A(q) = 0.

The resulting tensor equals J in the commuting frame on the central collar, and equals zero for |t| >= 3/4. Its support is contained in T^{n-1} x [-3/4,3/4], a compact subset of the open collar. The lack of smoothness of |t| at zero is irrelevant: q is chosen smooth and constant on a neighborhood of zero.

## 4. Embedding the torus collar in Euclidean space

For every d >= 1 the torus T^d has a smooth hypersurface embedding in R^{d+1}. Here is a direct induction, so no embedding assertion is left implicit.

The circle embeds in R^2. Suppose T^{d-1} is embedded as a smooth hypersurface in R^d. Since both torus and ambient space are orientable, this embedding has a global smooth unit normal nu. Regard the same embedded torus as lying in R^d x {0} inside R^{d+1}. Its rank-two normal bundle is explicitly trivialized by (nu,e_{d+1}). Compactness and the tubular-neighborhood theorem provide an embedded disk bundle T^{d-1} x D^2_epsilon. The boundary is an embedded hypersurface diffeomorphic to T^{d-1} x S^1 = T^d. This completes the induction.

The resulting T^{n-1} in R^n is two-sided. A sufficiently thin tubular collar is diffeomorphic to T^{n-1} x (-1,1), after rescaling its normal coordinate. Push the tensor of Section 3 through this diffeomorphism and extend it by zero outside the collar. It already vanishes on an open neighborhood of both collar ends, so the extension is globally smooth, not merely continuous or finitely differentiable. Naturality of Nijenhuis torsion under diffeomorphism and locality of its defining formula show that torsion vanishes everywhere, including at the extension boundary.

The central collar is a nonempty open subset of R^n on which the exact chosen Jordan type holds. If a coordinate domain is preferred, any sufficiently small connected coordinate box inside this central collar also works.

For n=1, any scalar tensor f(x)Id is Nijenhuis; choose a compactly supported smooth f equal to the desired scalar on an interval. This treats the dimension omitted by the torus-hypersurface induction.

## 5. Necessity of real spectrum

We use the prior rigidity theorem of A. V. Bolsinov, A. Yu. Konyaev and V. S. Matveev, *Nijenhuis Geometry*, arXiv:1903.04603v2, Theorem 6.1, PDF page 41; published in Advances in Mathematics 394 (2022), 108001. For a smooth Nijenhuis tensor on a closed connected manifold, any nonreal eigenvalue occurring at one point occurs everywhere, with constant algebraic multiplicity.

If L has compact support on R^n, use the standard R^n chart in S^n and extend L by zero to the point at infinity. Compact support ensures that this extension is identically zero throughout a neighborhood of infinity, hence is smooth and Nijenhuis on the closed connected manifold S^n. A nonreal eigenvalue anywhere would, by the cited theorem, have to occur at infinity; the zero endomorphism has only the eigenvalue zero. Contradiction.

Thus every compactly supported smooth real Nijenhuis tensor has entirely real spectrum at every point. Combined with Sections 1-4, this proves the exact classification.

## 6. Scope and attribution checks

- The obstruction and the previously known real semisimple and 2-by-2 Jordan examples are prior results, explicitly credited by the problem source.
- The constructive argument in this manuscript is the torus collar plus the finite real matrix path; it deals with every real Jordan partition, rather than just one larger block.
- An arbitrary cutoff of J was never used. The only reparametrization is of a path already verified to satisfy (2).
- Repeated eigenvalues, zero eigenvalues, arbitrary block ordering, and size-one blocks cause no omitted cases.
- Compact support is obtained from compact angular directions plus exact vanishing on open end collars. It is not inferred from a local normal form.
- The proof relies on no real-analytic globalization or globally constant-rank assumption.
- Literature checks locate the exact source versions and the prior nonreal rigidity theorem; they do not establish novelty or exhaust all later publications.

## Public primary references

1. A. Bolsinov, V. Matveev, E. Miranda, S. Tabachnikov, *Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems*, https://arxiv.org/abs/1804.03737v2 ; Problem 5.11, PDF page 29. The v1 counterpart is Problem 4.10, PDF page 37: https://arxiv.org/abs/1804.03737v1 . The corpus label 5.9 is reconciled by full wording, not used as a present-version locator.
2. A. V. Bolsinov, A. Yu. Konyaev, V. S. Matveev, *Nijenhuis Geometry*, https://arxiv.org/abs/1903.04603v2 ; Theorem 6.1, PDF page 41; https://doi.org/10.1016/j.aim.2021.108001 .
3. A. Bolsinov, A. Konyaev, V. Matveev, *Nijenhuis Geometry III: gl-regular Nijenhuis operators*, https://arxiv.org/abs/2007.09506 ; local gl-regular normal-form results do not themselves provide the compact-support construction proved above.
