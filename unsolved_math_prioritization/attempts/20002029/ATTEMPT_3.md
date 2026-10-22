# Attempt 3: dimension six by explicit Ricci-flat restriction injectivity

Outcome: a proof of the dimension-six case, using a classical classification plus three explicit Ricci-flat metrics. This is a scoped resolution and remains subject to the final independent review. The general even-dimensional problem is not resolved. The exact computations have been reproduced, but this is not an independent final audit. No priority or novelty claim is made.

## Statement

Let I(g) be a scalar, pointwise conformal invariant of weight -6 in dimension 6, given by a finite linear combination of complete contractions of covariant derivatives of the Schouten tensor, using metric pairings only. Then I is identically zero.

The potentially unjustified implication “vanishes on Ricci-flat metrics, therefore vanishes identically” is replaced below by an explicit nonsingular evaluation matrix on three actual, positive-definite, Ricci-flat metrics.

## 1. Classification input and its restriction

Fefferman–Graham, *The Ambient Metric*, Theorem 9.4 and the paragraph immediately following it (printed p. 94), show that every even scalar conformal invariant of weight -6 in dimension 6 is a linear combination of

- the ambient invariant D_tilde = |ambient nabla ambient R|^2; and
- complete contractions of three Weyl tensors.

The following elementary algebraic argument shows that the cubic contractions span at most two dimensions. Define, in an orthonormal frame with repeated indices summed,

A(W) = W_abcd W_cdef W_efab,
B(W) = W_abcd W_aecf W_bedf.

For any complete cubic contraction, an internal pairing within one Weyl factor is zero by trace-freeness (or skew symmetry). The contraction graph therefore has three vertices of valency 4 and no loops. Consequently each pair of vertices is joined by exactly two edges.

Call a factor unmixed if its two indices paired with one other factor constitute one of its skew pairs. If a factor is unmixed, relabel it as W_abcd, with a,b paired against the second factor and c,d against the third. Each neighboring factor is either already unmixed or becomes unmixed upon antisymmetrizing in a,b or c,d. The Bianchi identity gives

W_aebf - W_beaf = W_abef.

Thus each such antisymmetrization replaces a mixed neighbor by one half of its unmixed version. The full contraction is therefore, up to sign, A, A/2, or A/4.

If all three factors are mixed, use the curvature symmetries to write the first two as W_abcd W_aecf. The third factor is, up to sign, either W_bedf or W_bfde. Hence the only further possibility besides B is

U = W_abcd W_aecf W_bfde.

Again Bianchi gives W_bedf - W_bfde = W_bdef, so

B - U = W_abcd W_aecf W_bdef
      = (1/2) W_abcd W_acef W_bdef
      = (1/4) W_acbd W_acef W_bdef
      = A/4.

The penultimate equality antisymmetrizes the first factor in a,c, using W_abcd - W_cbad = W_acbd. The last expression is A after dummy-index renaming and pair exchange. This proves that all algebraic Weyl cubics lie in span{A,B} without any dimension-dependent assertion of independence.

We consequently have constants alpha,beta,gamma such that

I = alpha D_tilde + beta A(W) + gamma B(W).

Fefferman–Graham equation (9.3), printed p. 93, is

D_tilde = |V|^2 + 16(W,U_FG) + 16|C|^2,
U_FG_mjkl = C_jkl,m - P_m^i W_ijkl,

and equation (6.3), printed p. 52, gives

V_ijklm = W_ijkl,m + g_im C_jkl - g_jm C_ikl + g_km C_lij - g_lm C_kij.

On a Ricci-flat metric, P and C vanish identically, so U_FG = 0, V = nabla W, and W = R. Hence the full ambient invariant, with all 0/infinity terms already included by (9.3), restricts exactly to

D_tilde = D := |nabla R|^2.

No ambient-jet realization assumption is being made.

## 2. Actual Ricci-flat metrics

For any p = (p_1,...,p_5) with sum p_i = sum p_i^2 = 1, define on (0,infinity) x R^5

g_p = dr^2 + sum_i r^(2 p_i) dx_i^2.

This is a smooth positive-definite metric. Let e_0 = partial_r and e_i = r^(-p_i) partial_x_i. Its only nonzero connection coefficients are

nabla_(e_i) e_0 = (p_i/r) e_i,
nabla_(e_i) e_i = -(p_i/r) e_0,

while nabla_(e_0) e_a = 0. In the convention R_abab = sectional curvature, set

K_0i = p_i(1-p_i),
K_ij = -p_i p_j (i,j >= 1 and i != j),
K_aa = 0.

The curvature components are

R_abcd = r^(-2) K_ab (delta_ac delta_bd - delta_ad delta_bc).

The Ricci tensor is diagonal, with

Ric_00 = r^(-2) (sum p_i - sum p_i^2) = 0,
Ric_ii = r^(-2) p_i(1 - sum p_j) = 0.

Thus these are actual Ricci-flat metrics on a neighborhood of r = 1. No completeness or extension through r = 0 is required for a pointwise invariant identity.

## 3. Exact invariant formulas

At r = 1, the diagonal curvature tensor gives

|R|^2 = 4 sum_(a<b) K_ab^2,
A(R) = 8 sum_(a<b) K_ab^3,
B(R) = 6 sum_(a<b<c) K_ab K_ac K_bc.

Because the orthonormal frame is parallel in the radial direction,

nabla_(e_0) R = -2 R at r = 1.

In a spatial direction e_i, covariant differentiation acts on each of the four curvature slots by the infinitesimal rotation in the (0,i)-plane, multiplied by p_i. For each j different from 0,i this pairs the curvature-plane values K_0j and K_ij. Summing the eight equal-square tensor components per such pair yields

D = |nabla R|^2
  = 16 sum_(a<b) K_ab^2
    + 8 sum_(i=1)^5 p_i^2 sum_(j=1,j!=i)^5 (K_0j - K_ij)^2.

These formulas are also independently verified by full tensor-component summation in the accompanying exact rational-arithmetic script. In particular, the derivative check forms every component using the connection above rather than using this closed norm formula.

## 4. Nonsingular evaluation matrix

Take the following three exponent vectors, each satisfying the two Ricci-flat constraints:

p^(1) = (-1/3, 2/3, 2/3, 0, 0),
p^(2) = (-1/2, 1/2, 1/2, 1/2, 0),
p^(3) = (-3/5, 2/5, 2/5, 2/5, 2/5).

At r = 1 the rows (D,A,B) are

(1280/81,       -256/243,       -128/243),
(27,           -3,             -3/2),
(21504/625,     -19968/3125,    -6528/3125).

The determinant is

det M = -65536/3125 != 0.

Changing the overall sign convention for R changes the signs of both cubic columns, leaving this determinant unchanged.

## 5. Conclusion

On each Ricci-flat metric, the Schouten tensor vanishes identically, as do all its covariant derivatives. Every nonconstant Schouten-jet contraction therefore vanishes. In particular I(g_p) = 0 for the three metrics above. The classification representation gives

M (alpha,beta,gamma)^T = 0.

Since M is nonsingular, alpha = beta = gamma = 0. Therefore I is identically zero on all six-dimensional metrics.

This also establishes that restriction to actual Ricci-flat metrics is injective on the entire three-dimensional space of even scalar conformal invariants of weight -6 in dimension 6. The argument does not extrapolate that injectivity to other weights or higher critical dimensions. Products of these metrics with a flat factor do prove the analogous weight -6 statement in every dimension greater than 6, but those weights are not the critical weights of the original general question.

## Reproduction

Run:

python checks/check_kasner_restrictions.py

The script uses SymPy rational arithmetic and checks every relevant tensor component. It prints the three rows and determinant, then checks the rows by independent raw contraction of R and nabla R.
