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

## 5. Polarized tensor and a four-dimensional Lorentz reduction

The full polarized determinant tensor is
\[
 T_{k\ell}
 =\frac12(A_kC_\ell+C_kA_\ell)-B_kB_\ell,
 \qquad
 R_k=(A_k,\sqrt2B_k,C_k),
 \tag{9}
\]
so, with
\[
 \Theta=
 \begin{pmatrix}
 0&0&1\\0&-1&0\\1&0&0
 \end{pmatrix},
\]
one has
\[
 T=\frac12R\Theta R^t,\qquad
 \|T\|_2^2
 =\frac14\operatorname{Tr}(\Theta\overline G\Theta G),
 \qquad G=R^\dagger R.                                    \tag{10}
\]
The all-locally-symmetric part of \(T\) is the only part visible to
diagonal determinant evaluation.  For the exact balanced graph code,
\[
 \|T\|_2^2=1,\qquad \|T_{\mathrm{loc.sym.}}\|_2^2=\frac5{12}.
 \tag{11}
\]
Thus the raw norm cannot simply be substituted into a diagonal
quadratic-form estimate.

There is nevertheless a useful exact reduction of the numerically
observed identity \(\|T\|_2^2=1\).  For a subset \(S\), let
\(\Gamma_S\) be the real Pauli Gram matrix of the reduced logical
channel:
\[
 (\Gamma_S)_{\mu\nu}
 =
 \operatorname{Tr}\!\left(
 {\cal N}_S(\sigma_\mu){\cal N}_S(\sigma_\nu)
 \right),
 \qquad 0\leq\mu,\nu\leq3.                                \tag{12}
\]
Define its alternating Walsh sum
\[
 \widehat\Gamma
 =\sum_{S\subseteq[4]}(-1)^{|S|}\Gamma_S
 =
 \begin{pmatrix}s&h^t\\h&M\end{pmatrix}.                  \tag{13}
\]
Complement balance and the exact subset/complement Pauli-Gram identity
give
\[
 s=\operatorname{Tr}M,\qquad
 M=2I_3+D,\qquad s=6+t,                                   \tag{14}
\]
where
\[
 D=\sum_{|S|=2}G_S-2\sum_{|S|=1}G_S,\qquad t=\operatorname{Tr}D,
 \tag{15}
\]
and
\[
 h=\sum_{|S|=2}b_S-2\sum_{|S|=1}b_S.                      \tag{16}
\]

To check the constants, the compressed swap has the Pauli expansion
\[
 {\cal A}_S
 =\frac14\sum_{\mu,\nu=0}^3
 (\Gamma_S)_{\mu\nu}\,\sigma_\mu\otimes\sigma_\nu.
 \tag{17}
\]
Consequently the all-antisymmetric logical effect is
\[
 E_{[4]}
 =\frac1{64}\left[
 sI\otimes I+
 \sum_a h_a(I\otimes\sigma_a+\sigma_a\otimes I)
 \sum_{a,b}M_{ab}\sigma_a\otimes\sigma_b
 \right]_{\operatorname{Sym}^2\mathbb C^2}.               \tag{18}
\]
In the Cartesian spin-one basis, write \(E_{[4]}={\cal A}+i{\cal K}\)
with \({\cal A}\) real symmetric and \({\cal K}\) real
antisymmetric.  Equations (14) and (18) give
\[
 {\cal A}=\frac{sI-M}{32}
 =\frac{(4+t)I-D}{32},
 \qquad
 {\cal K}=-\frac{[h]_\times}{32},                          \tag{19}
\]
up to an irrelevant common real orthogonal change of Cartesian axes.
Since
\[
 \|T\|_2^2
 =64\operatorname{Tr}
 (E_{[4]}\overline{E}_{[4]})
 =64\bigl(\operatorname{Tr}{\cal A}^2-\|{\cal K}\|_2^2\bigr),
 \]
we obtain the exact formula
\[
 \boxed{\qquad
 \|T\|_2^2
 =
 \frac{s^2+\operatorname{Tr}M^2-2|h|^2}{16}.
 \qquad}                                                   \tag{20}
\]
Therefore the raw-norm conjecture on the complement-balanced slice is
equivalent to the single Lorentzian Pluecker identity
\[
 \boxed{\qquad
 s^2+\operatorname{Tr}M^2-2|h|^2=16.
 \qquad}                                                   \tag{21}
\]
Equivalently,
\[
 \boxed{\qquad
 2|h|^2=32+16t+t^2+\operatorname{Tr}D^2.
 \qquad}                                                   \tag{22}
\]
Equations (20) and (22) cleanly separate the already-proved linear
complement geometry from the missing nonlinear common-isometry
relation.  Equation (22) has not yet been proved.

For a full-rank unrestricted balanced numerical frame, the two sides
of (22), after division by \(1024\), were respectively
\[
 0.0002126654544,\qquad 0.0002126595747,
\]
with the discrepancy tracking the residual complement-balance error.
Across all balanced feasibility runs checked, (21) agreed to the
constraint residual.  This is discovery evidence, not a certificate.

The possible spectral shortcut
\[
 \operatorname{spec}E_{[4]}
 \stackrel{?}{=}\{0,p_{[4]}-\tfrac18,\tfrac18\}
 \tag{23}
\]
is false.  For the exact balanced graph code,
\[
 \operatorname{spec}E_{[4]}
 =\left\{\frac1{24},\frac1{12},\frac1{12}\right\},
 \qquad p_{[4]}=\frac5{24}.                                \tag{24}
\]
For the generic numerical balanced frame the spectrum was approximately
\[
 \{0.03514097,\ 0.06031395,\ 0.10572443\}.
 \tag{25}
\]
The pattern in (23) occurs only on the rank-deficient boundary reached
by many feasibility searches.

## 6. Frame-optimization audit on a generic balanced code

On the full-rank balanced frame used above, a checked Riemannian
one-site optimizer gave
\[
 C_{\rm initial}=1.1075940101
\]
and one-site optima between \(1.1437\) and \(1.1897\).  Cyclic
four-site ascent reached
\[
 C=1.4815407067.
\]
After twenty independent local-unitary scramblings, optimizing only one
site always crossed one; the smallest maximum over the four possible
optimized sites was \(1.0179508\).  This does not prove that one-site
optimization always suffices.

Independent four-site Haar estimates with \(5000\) samples gave
\[
\begin{array}{c|c|c}
\text{frame}&\text{mean }C&\text{standard error}\\ \hline
\text{exact balanced graph}&1.0261720&0.000393\\
\text{generic balanced frame}&1.0235093&0.000343 .
\end{array}
\tag{26}
\]
Near-boundary balanced frames had \(C\) essentially identically one.
These data suggest the stronger possible route
\(\mathbb E_{\rm local\ Haar}C\geq1\), but no exact first-moment
inequality for the special determinant tensor has yet been proved.
