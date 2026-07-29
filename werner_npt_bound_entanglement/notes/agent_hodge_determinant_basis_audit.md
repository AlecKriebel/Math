# Hodge determinant: sector audit and basis optimization

## Status

This note adversarially audits the proposed balanced-code inequality
\[
 C(U):=\sum_{k\in\{0,1,2\}^4}
 \left|\det\!\left(U^T
 (L_{k_1}\otimes\cdots\otimes L_{k_4})U\right)\right|
 \stackrel{?}{\geq}1.                                      \tag{1}
\]
The fixed-basis inequality is **false exactly**.  The complete
counterexample and its Eisenstein-integer verifier are in
`notes/agent_balanced_hodge_determinant_counterexample.md` and
`verification/verify_balanced_hodge_determinant_counterexample.py`.

The additional conclusions here are:

1. the determinant is exactly one compound bilinear form of the common
   decomposable bivector;
2. on the Fourier-rotated counterexample, the natural odd-sector
   strengthening fails by the exact factor \(3\);
3. optimizing the Hodge frame remains a logically possible replacement:
   a single inverse Fourier transform raises the same code from
   \(C=1/3\) to \(C=\sqrt{21}/3\);
4. numerical local-frame searches on a second, unrestricted balanced
   code also raise \(C\) above \(1\), but this is discovery evidence only.

## 1. Intrinsic determinant formula

Let \(U=(u\ v)\) be an isometry and
\[
 \omega=\frac{u\otimes v-v\otimes u}{\sqrt2}.
\]
For a symmetric matrix \(B\),
\[
 \boxed{\qquad
 \det(U^TBU)=\omega^T(B\otimes B)\omega .
 \qquad}                                                   \tag{2}
\]
Indeed, expansion of the right side gives
\[
 (u^TBu)(v^TBv)-(u^TBv)(v^TBu).
\]
For
\[
 B_k=L_{k_1}\otimes\cdots\otimes L_{k_4},
 \qquad (L_j)_{ab}=\epsilon_{jab},
\]
the matrix \(B_k\) is symmetric because it is a tensor product of four
skew matrices.  Hence (2) applies to every determinant in (1).

## 2. Exact sector diagnosis

Decompose the globally antisymmetric bivector into local-swap sectors:
\[
 \omega=\sum_{\substack{R\subseteq[4]\\ |R|\ {\rm odd}}}\omega_R,
 \qquad \omega_R=\Pi_R\omega,
\]
and put
\[
 d_{R,k}=\omega_R^T(B_k\otimes B_k)\omega_R,\qquad
 d_k=\det(U^TB_kU).
                                                               \tag{3}
\]
Since \(B_k\otimes B_k\) commutes with every local replica swap,
\[
 d_k=\sum_{|R|\ {\rm odd}}d_{R,k}.                         \tag{4}
\]

For the exact Fourier-rotated graph code in the counterexample note,
direct Eisenstein-integer contraction gives the stronger coordinatewise
identity
\[
 \boxed{\qquad d_{R,k}=\frac18d_k
 \quad\text{for every odd }R\text{ and every }k.\qquad}     \tag{5}
\]
Here is an integer normalization check of (5).  Remove the common
\(1/\sqrt{27}\) factor from each codeword and let
\[
 W=u_{\rm num}\otimes v_{\rm num}
   -v_{\rm num}\otimes u_{\rm num},
\qquad
 W_R=\prod_{i=1}^4
 \left(I+(-1)^{{\bf1}_{i\in R}}F_i\right)W.
\]
If \(D_k=729d_k\in\mathbb Z[\zeta]\), exact enumeration gives
\[
 W_R^T(B_k\otimes B_k)W_R=64D_k.                           \tag{6}
\]
But
\[
 \Pi_R\omega=\frac{W_R}{16\cdot27\sqrt2},
\]
so (6) is exactly (5).

Complement balance gives
\[
 \|\omega_R\|^2=\frac18
 \qquad(|R|\ {\rm odd}).
\]
Nevertheless, (5) and \(C(U)=1/3\) give
\[
 \boxed{\qquad
 \sum_k|d_{R,k}|=\frac1{24}
 =\frac13\|\omega_R\|^2
 \qquad(|R|\ {\rm odd}).\qquad}                            \tag{7}
\]
All eight sector contributions are phase-aligned at every \(k\); there
is no cross-sector cancellation.  Thus the failed step is the proposed
sectorwise lower bound
\(\sum_k|d_{R,k}|\geq\|\omega_R\|^2\), not phase alignment.

This is a useful obstruction: complement balance fixes the eight
Hermitian sector norms, but it does not lower-bound the holomorphic
Hodge determinant norm in a fixed physical basis.

## 3. Exact local-basis behavior

For the balanced graph code before the Fourier rotation,
\[
 C(U)=\frac{\sqrt{21}}3.
\]
After applying the qutrit Fourier matrix on the first physical site,
\[
 C((F\otimes I^{\otimes3})U)=\frac13.
\]
Both codes have
\[
 A_T=\frac43\quad(0<|T|<4),
 \qquad p_{1234}=\frac5{24}.
\]
Thus \(C\) is not invariant under local physical unitaries.  Conversely,
on the Fourier-rotated code, applying \(F^{-1}\) at that same single
site restores \(\sqrt{21}/3>1\).  Therefore this example does **not**
refute the frame-optimized replacement
\[
 \sup_{g_1,\ldots,g_4\in U(3)}
 C\!\left((g_1\otimes\cdots\otimes g_4)U\right)\geq1.       \tag{8}
\]
Inequality (8) remains unproved.

The unrotated graph basis appears to be a one-site local maximum.
Starting from it, \(600\) random near-identity complex-unitary proposals
at each of the step scales
\[
 .2,\ .1,\ .05,\ .02,\ .01,\ .005,\ .002,\ .001
\]
accepted no increase over \(\sqrt{21}/3\).  This is numerical evidence,
not a critical-point proof.

## 4. Numerical frame-orbit audit

The following values are floating-point discovery data.

For the exact graph-code local orbit, Haar-random complex unitary changes
on one site gave, over \(5000\) samples,
\[
 \min C\approx0.58345,\qquad
 \operatorname{mean}C\approx1.13808,\qquad
 \max C\approx1.47712.
\]
The exact special Fourier frame \(C=1/3\) and exact original frame
\(C=\sqrt{21}/3\approx1.52753\) lie outside the extrema hit by this
finite random sample.  Independent Haar rotations at all four sites
gave a smaller sampled maximum \(1.22415\), consistent with
high-dimensional concentration and not with a smaller supremum.

For an independently optimized unrestricted balanced frame with
\[
 p_{1234}\approx\frac5{24},\qquad C\approx1.002534,
\]
three thousand one-site Haar trials at sites \(1,2,3,4\) reached maxima
\[
 1.14781,\quad1.12694,\quad1.08359,\quad1.09148.
\]
A crude four-site coordinate ascent reached \(C\approx1.42168\).
Thus the frame-optimized inequality (8) survives these tests, and even
one optimized site sufficed to cross \(1\) in this generic feasible
frame.  None of these numerical statements is a theorem.

## Consequence

The original fixed-coordinate global Pluecker inequality (1) is
rigorously false, with the exact obstruction \(C=1/3\).  Its
sector-by-sector strengthening is also rigorously false, by (7).
Any determinant proof of four-copy positivity must introduce a
local-unitary optimization or a genuinely invariant replacement.
Whether the optimized inequality (8) is true is now a strictly
different unresolved lemma.
