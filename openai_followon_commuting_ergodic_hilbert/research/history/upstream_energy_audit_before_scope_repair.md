# Independent audit: upstream matrix, heat, and smooth-annulus argument

Audit completed: 2026-10-06 22:13 PDT (2026-10-07 05:13 UTC).

Reviewer: internal adversarial research agent `upstream_energy_audit`, with an independently reconstructing internal reviewer `matrix_falsification`. No external individuals were contacted. No upstream files or Git state were changed.

Pinned source: upstream commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, copied into `sources/upstream/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026`. Scope audit completion estimate: 100%. Completion of the full annular theorem, discrete restriction, ergodic theorem, priority audit, and publication package is outside this review's completion estimate.

## Verdict and exact scope

No substantive counterexample or proof gap was found in `build/sections/matrix.tex`, `heat.tex`, or `smooth.tex`. I independently reconstructed their pivotal inequalities, support arguments, heat derivatives, plane integration, jump estimates, rescaling, and hard/smooth kernel identity. The arguments are consistent for arbitrary finite-dimensional complex matrices, including singular Grams, and for complex smooth compactly supported inputs with finite step menus. Constants are independent of grid size, matrix dimension, and endpoint menu.

This verdict does **not** verify the full hard-annular variation theorem. That additionally requires the frequency-block argument, rough endpoint family estimates, completion/linearization, and density arguments. This audit also does not validate formalization, priority, publication metadata, or the proposed discrete/ergodic reduction.

Exact reviewed SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| `build/sections/matrix.tex` | `914af3c5e87cd4af52b1c7a9e7f2a4ac03d82b9456b8be50b69ffbbbee59f9ad` |
| `build/sections/heat.tex` | `c6a85b01fdecf3a7b03bf3ba25ec03a3da68ab71c3c85c5d82da139ce1ebd3c6` |
| `build/sections/smooth.tex` | `dc964effac57c11797de4dba23fa8137978baec49c430f43a46324f49ecc08ee` |

Related sources actually read: `preliminaries.tex`, `introduction.tex`, `main.tex`, manuscript `README.md`, copied `LEAN_SCOPE_082.md`, and the project's original request. No reliance was placed on the existence of a Lean directory or comparator statement.

## Matrix reconstruction

1. **Supported Hessian and order comparison** (`matrix.tex`, lines 54–144). On a fixed support the square-root derivative solves `sqrt(P) X + X sqrt(P) = K`, hence
   \[
   d^2\operatorname{tr}(P^{3/2})(K,K)
     =\frac32\sum_{i,j}\frac{|K_{ij}|^2}{\sqrt{p_i}+\sqrt{p_j}}.
   \]
   The first derivative is `(3/2) tr(sqrt(P) K)`, including the claimed factor. If `P <= a Q`, then `ker Q` is contained in `ker P`, so supported directions for `P` are supported for `Q`. Square-root monotonicity followed by inversion of the positive Sylvester operators gives the claimed lower bound `b_P(K) >= a^(-1/2) b_Q(K)`. In the regularized limit no kernel-touching entry survives; this is essential and is satisfied.

2. **Insertion and rank change.** In singular-value coordinates the inserted Gram cost is
   \[
   \frac32\sum_{ij}\frac{\rho_i^2\rho_j^2}{\rho_i+\rho_j}|C_{ij}|^2.
   \]
   The scalar bound on its coefficient and the squared row/column norms of the compression of `L` give precisely `(3/4)||L||_op^2 sum rho_i^3`. The rank-change derivative follows by regularization; its error is bounded uniformly by `sqrt(eta)` on the compact interpolation segment. The entry-gradient estimate is ordinary Cauchy–Schwarz, since the squared norm of a column of `sqrt(R*R)` is `(R*R)_(jj)`.

3. **Joint convexity** (lines 182–245). With `A = integral sqrt(T_omega)`, vector Cauchy–Schwarz gives `A^2 <= integral T_omega`. Since `A` is positive, square-root order gives `A <= sqrt(integral T_omega)`. The inverse variational formula then yields the cost inequality: the supremum of the average is bounded by the average of the suprema. The manuscript does not incorrectly assert equality. Common support and integrability are explicit hypotheses; uniform positive eigenvalue bounds are unnecessary.

4. **Mixed trace** (lines 299–430). Embedding the stars into the zero-diagonal Hermitian block matrix `M` correctly gives `A_v = M P_v M` and `K_v = M P_v D M`, both supported as asserted, with `A_v <= M^2`. Consequently the sum of original costs is at least `b_(M^2)(M D M)/3 = Q/2`. For eigenvalues ordered by decreasing absolute value, the three multiplicity cases for the minimum index in the cubic trace contribute at most
   \[
   D_* A_i,\qquad 3D_*\sqrt{A_iE_i},\qquad 3D_*E_i.
   \]
   In particular the often vulnerable twice-occurring case has the correct powers: `q_i^2 |D_ii| sqrt(sum q_k^2 |D_ik|^2) = sqrt(A_i E_i)`. Summation gives `|tr((DM)^3)| <= 5D_*Q`. The block cycle trace equals `6 Re(tau)`. A unit-modulus rotation of `W_0` changes each affected star by right unitary multiplication, preserving every original energy cost. The proof correctly uses the new auxiliary `Q` after this rotation. Thus the `5/3` constant is justified. Eight-term expansion for complex diagonal insertions gives the stated `20/3` factor.

## Heat reconstruction and attempted attacks

**Rank and differentiation** (`heat.tex`, lines 96–143). Gaussian diagonal factors are positive and invertible for every finite center and positive variance. Row variation fixes `ker R`; column variation fixes `ran R`. Therefore the selected Gram has a fixed support in each derivative. Full joint smoothness follows by the rank factorization displayed in the source: the reduced positive matrix `Q'^(1/2) P' Q'^(1/2)` has exactly the nonzero spectrum. Rank zero is harmless. The density identity `2 partial_sigma w = partial_p^2 w` and the Hessian chain rule reproduce both pure heat identities and the column/column mixed term `Z_v`. No unaccounted derivative of a moving support is used.

**Plane derivatives** (lines 145–208). The Gaussian majorants and inserted-Gram estimate dominate every derivative actually used by a polynomial in the centers times the energy. An edge gives Gaussian decay in its two distinct endpoint centers. Those endpoints are valid free coordinates on the plane; the remaining center is their negative sum plus `d`. This proves integrability and polynomial growth in `d` on compact positive scale intervals. Choosing different dependent coordinates then genuinely gives `partial_d^2 J_v = integral Z_v`. It is an integrated identity, not a false pointwise equality of different center derivatives. The plane measure is deliberately the coordinate measure, so no omitted Euclidean surface factor is present.

**Neighbor comparison and sign** (lines 237–269). Put `R=[A B]` and `Q=diag(A*A,B*B)`. Then `R*R <= 2Q`, and the inserted `R*N R` is supported on both relevant Grams. After the first order comparison, discarding off-diagonal blocks is legitimate because the Hessian in a block eigenbasis is a sum of nonnegative squared entries. Each diagonal block is then compared to the neighboring full star, giving
\[
Y_{w+1,w}+Y_{w-1,w}\le\sqrt2 V_w.
\]
Using `2Z_v <= Y_(v,v+1)+Y_(v,v-1)` produces the coefficient `Sigma_alpha/2-alpha_w`, with the correct sign. For rates `(1,11/10,11/10)` the strict margins are `1-3sqrt(2)/5 > 0` and `11/10-sqrt(2)/2 > 0`. There is no assertion of strict summed-star dissipation for arbitrary disparate rates.

**Initial and single-edge energy** (lines 278–380). The mesh mass bound has at most two uncovered nodes, including the case when `p` equals a grid node. Weighted Hölder costs one factor `M`, because the product mass is at most `M^2`. Each endpoint density integrates to `h`; the resulting norm therefore has `h^2`, agreeing with the specified discrete `L3` norm. In the single-edge case the absent column makes `Z_v=0`; the plane integrals are independent of `d`, giving exact dissipation for all positive endpoint rates. The comparison `Y_full <= Y_edge` has the correct order direction.

## Smooth masks, scaling, and endpoints

**Energy jumps** (`smooth.tex`, lines 65–129). Changing `A_0` changes stars `R_0` and `R_1` only. Their row and column norm bounds reproduce the factors `2XY+HY+QX`. The measure `h^(-2) w_0(i)w_1(j) d pi_0` has total mass one. Its free centers are independent normals with means `u_i,u_j`; the third center is their negative sum. The expectations displayed in lines 96–99 have the correct variance sums and signs. Centered lattice maximal functions at `-i-j` apply to the zero-extended arrays. The relevant changes of slice coordinate are bijections on all of `Z`, so the four square-root majorants have norms `C n_0,C n_0,C n_2,C n_1`. Hölder then gives `n_0^3+n_0^2(n_1+n_2)` per unit switch count. The total variation of each masked entry is at most `2n |A_0|`, including coincident openings/closings and complex coefficients.

**Window insertion** (lines 133–171). The ratio `k_s/g_(lambda s)` is bounded uniformly in both center and scale: its linear factor in `t/sqrt(s)` is absorbed by a Gaussian whose exponent is strictly negative. Narrowing the row only gives exactly
\[
(R_v^b)^*D_vR_v^b=\sqrt{s}\,U_v^n,
\qquad T_v^n\le\sqrt\lambda\,T_v^b.
\]
Order comparison therefore bounds the base cost by `C s V_v^n`; the integration measure `ds/s` cancels this factor. The row narrowing preserves support, and its rate triple is one of the strictly dissipative triples. At the left side the three densities are exactly `h k_s`, yielding the factor `h^3` in the cyclic Riemann sum. Normalizing the original norms to `(n^(-1/2),1,1)` makes the jump bound uniformly bounded and rescaling produces `sqrt(n)` with no hidden width dependence. The finitely many endpoints are fixed before `h` tends to zero, so `h^2 <= s_-` costs no endpoint uniformity.

**Hard/smooth identity** (lines 181–202). Directly, `k_s = Dil_(sqrt(s)) k_1`, `psi=-g_3'''`, and `k_s*k_s*k_s = s^(-1/2) psi(t/sqrt(s))`. Substitution `z=|t|/sqrt(s)` gives exactly the difference of `P` values divided by `t`. Furthermore `c_0=2g_3''(0)=-(2/3)g_3(0)` is negative but nonzero; positivity is never needed. The even extension of `P` is smooth and vanishes to second order. Thus `E_rho(0)=0` is the correct continuous value. The hard identity is valid away from endpoint values, which are immaterial under the scalar integrals. This reconstructs only the identity; estimating many hard endpoint errors still requires the later sections.

## Numerical corroboration and formalization boundary

Floating-point computations were supplementary bookkeeping checks only. My independent seeded test (`812606`, bundled Python and NumPy) sampled 5,000 complex cyclic triples in dimensions 1–5, half with deliberately rank-deficient edges, and 15,000 neighbor comparisons. The largest ratios to the stated right sides were `0.07470168193073122` for mixed trace and `0.707003261832278` for neighbors; no violation was found. The additional independent matrix reviewer reported reconstructing all of the matrix proof and stress-testing singular support, probability averaging, and cubic expansion without a violation. Numerical treatment of near-zero eigenvalues cannot certify the supported inequalities; the exact algebra above supplies the verification.

The copied `LEAN_SCOPE_082.md` explicitly associates its scope with the **September 24 maximal** manuscript and claims a maximal estimate. It does not state the October 5 full annular variation theorem. Neither this scope document nor a comparator link certifies the annular dependency; no formal build was reproduced by this review.

Strongest result verified here: the finite-dimensional matrix and Gaussian dissipation machinery, and its complete deduction of the repeated-choice **smooth** annulus estimate for finite step menus. Exact remaining gap in this scoped review: the later frequency/rough-kernel/completion argument needed for hard-annular count and pointwise variation, plus every new restriction/transference and priority claim.
