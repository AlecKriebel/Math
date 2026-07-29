# A universal affine identity for the eight odd Hodge sectors

## Status

For every decomposable four-party bivector and every choice of one
alternating local form at each party, the eight odd-sector Hodge
quadratics obey three exact linear relations.  In bit-mask notation they
are
\[
\begin{aligned}
 q_{11}-q_7&=\frac{q_4-q_8}{3},\\
 q_{13}-q_7&=\frac{q_2-q_8}{3},\\
 q_{14}-q_7&=\frac{q_1-q_8}{3}.
\end{aligned}                                               \tag{1}
\]
Equivalently, if \(i\) ranges over the four singleton masks, there is
one common scalar \(h\) such that
\[
 \boxed{\qquad q_{\bar i}=\frac13q_i+h. \qquad}              \tag{2}
\]
The identity is pointwise in the four alternating forms.  It therefore
survives arbitrary local changes of Hodge frame and polarizes to a
covariant identity for the full doubled-label determinant tensor.

This is a genuine nonlinear rank-two realizability identity: it follows
from decomposability and is false for a general vector in the global
antisymmetric space.  It does not, by itself, prove the balanced
four-copy inequality.  In particular, the exact Fourier-rotated graph
code in `agent_balanced_hodge_determinant_counterexample.md` obeys (1)
while its fixed-frame determinant sum is only \(1/3\).  In that example
the failure is not cancellation among the eight sectors: all sector
contributions are phase-aligned pointwise.  Rather, each sector has
Hodge \(\ell^1\)-mass \(1/24\), only one third of its Hermitian sector
mass \(1/8\).  Thus the missing step is a frame-invariant lower bound,
not another Pluecker phase relation.

The exact symbolic reduction below is replayed by
`verification/verify_balanced_hodge_affine.py`.

## 1. Definitions

Let
\[
 H=V_1\otimes V_2\otimes V_3\otimes V_4
\]
and let
\[
 \omega=x\wedge y
 =\frac{x\otimes y-y\otimes x}{\sqrt2}\in\Lambda^2H.
                                                               \tag{3}
\]
Let \(F_r\) swap the two replicas at party \(r\), and for a subset
\(R\subseteq[4]\) put
\[
 \Pi_R=\prod_{r\in R}\frac{I-F_r}{2}
       \prod_{r\notin R}\frac{I+F_r}{2},
 \qquad \omega_R=\Pi_R\omega.                                \tag{4}
\]
Only odd \(R\) occur because \(F_{[4]}\omega=-\omega\).

Choose an alternating form \(A_r\) of rank at most two on \(V_r\), and
put
\[
 J=A_1\otimes A_2\otimes A_3\otimes A_4.                     \tag{5}
\]
The tensor product \(J\) is symmetric.  Define the sectorwise
holomorphic Hodge quadratic
\[
 q_R(A_1,A_2,A_3,A_4)
 =\omega_R^T(J\otimes J)\omega_R.                            \tag{6}
\]
Since \(J\otimes J\) commutes with every \(F_r\), this is also
\(\omega^T(J\otimes J)\Pi_R\omega\).

For the qutrit Hodge matrices
\[
 (L_k)_{ab}=\epsilon_{kab},
\]
equation (6), evaluated at
\((A_1,\ldots,A_4)=(L_{k_1},\ldots,L_{k_4})\), is exactly the contribution
of sector \(R\) to
\[
 \det\!\left(U^T
 (L_{k_1}\otimes\cdots\otimes L_{k_4})U\right).
                                                               \tag{7}
\]
Indeed, summing (6) over odd \(R\) and using
\(\omega=\sum_R\omega_R\) gives
\[
 \sum_{R\ {\rm odd}}q_R
 =\omega^T(J\otimes J)\omega
 =\det(U^TJU).                                               \tag{8}
\]

## 2. A four-qubit moment lemma

Every alternating form \(A_r\) in dimension three has rank zero or two.
After restricting to its two-dimensional support and choosing a basis,
it is a scalar multiple of
\[
 \varepsilon=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\]
The scalar multiples occur on both replicas and are common to every
term, so it is enough to prove the identity for
\[
 H=(\mathbb C^2)^{\otimes4},
 \qquad J=\varepsilon^{\otimes4}.                            \tag{9}
\]

For \(T\subseteq[4]\), define the Walsh moments
\[
 m_T=\omega^T(J\otimes J)F_T\omega.                          \tag{10}
\]
Global antisymmetry immediately gives
\[
 m_{\bar T}=-m_T.                                           \tag{11}
\]

### Lemma 2.1

For four distinct sites \(i,j,k,l\),
\[
 \boxed{\qquad
 2(m_i-m_j)=m_{ik}+m_{il}.
 \qquad}                                                     \tag{12}
\]

### Proof

Use four replica multi-indices \(A,B,C,D\).  At a local site \(r\), put
\[
 Y_r=\varepsilon_{a_rc_r}\varepsilon_{b_rd_r},
 \qquad
 Z_r=\varepsilon_{a_rd_r}\varepsilon_{b_rc_r}.              \tag{13}
\]
Then (10) is the contraction of
\(\omega_{AB}\omega_{CD}\) with
\[
 \prod_{r\notin T}Y_r\prod_{r\in T}Z_r.                     \tag{14}
\]
Consequently, the left side of (12), moved to one side, has coefficient
\[
\begin{aligned}
 K={}&2\bigl(Z_iY_jY_kY_l-Y_iZ_jY_kY_l\bigr)\\
    &-Z_iY_jZ_kY_l-Z_iY_jY_kZ_l.                            \tag{15}
\end{aligned}
\]

The factor \(\omega_{AB}\omega_{CD}\) is antisymmetric separately under
\(A\leftrightarrow B\) and \(C\leftrightarrow D\).  Either swap sends
every \(Y_r\) to \(Z_r\) and every \(Z_r\) to \(Y_r\).  Hence \(K\) may
be replaced in the contraction by its double antisymmetrization
\[
\begin{aligned}
 K^-&=\frac12\bigl(K(Y,Z)-K(Z,Y)\bigr)\\
 &=-\frac12\,(Y_iZ_j-Y_jZ_i)
 \bigl(2Y_kY_l-Y_kZ_l-Y_lZ_k+2Z_kZ_l\bigr).                 \tag{16}
\end{aligned}
\]

We now check that \(K^-\) is a completely alternating four-replica
tensor.  It changes sign under \(A\leftrightarrow B\) and under
\(C\leftrightarrow D\), because those swaps interchange \(Y\) and \(Z\).
For the remaining adjacent transposition
\(B\leftrightarrow C\), the two-dimensional epsilon identity
\[
 \varepsilon_{ab}\varepsilon_{cd}
 =\varepsilon_{ac}\varepsilon_{bd}
  -\varepsilon_{ad}\varepsilon_{bc}                         \tag{17}
\]
gives, at every site,
\[
 (Y_r,Z_r)\longmapsto(Y_r-Z_r,-Z_r).                        \tag{18}
\]
Under (18), the first factor in (16) changes sign and the second factor
is unchanged.  Thus \(K^-\) changes sign under all three adjacent
transpositions and is completely alternating.

The contraction of a four-form with
\(\omega\otimes\omega\) is the contraction with
\(\omega\wedge\omega\).  Since \(\omega=x\wedge y\) is decomposable,
\[
 \omega\wedge\omega=x\wedge y\wedge x\wedge y=0.            \tag{19}
\]
The contraction of (16) therefore vanishes, which is exactly (12).
\(\square\)

## 3. Walsh inversion and the affine relation

From (4), (6), and (10),
\[
 q_R=\frac1{16}\sum_{T\subseteq[4]}
 (-1)^{|R\cap T|}m_T.                                      \tag{20}
\]
Let \(i,j,k,l\) be the four singleton masks.  Directly separating the
terms in (20) according to whether \(T\) contains \(i\) or \(j\), and
then using (11), gives
\[
\begin{aligned}
 &(3q_{\bar i}-q_i)-(3q_{\bar j}-q_j)\\
 &\hspace{2cm}
 =m_i-m_j-\frac12(m_{ik}+m_{il}).                           \tag{21}
\end{aligned}
\]
The right side is zero by Lemma 2.1.  Therefore
\[
 3q_{\bar i}-q_i=3q_{\bar j}-q_j
 \quad\text{for every }i,j.                                \tag{22}
\]
Taking \(h=(3q_{\bar i}-q_i)/3\) proves (2), and choosing the fourth
singleton as the reference gives (1).

Nothing in the proof selected a qutrit basis.  Since every local
alternating form was allowed, (1) is a polynomial identity in the four
forms \(A_r\).  Polarizing it in those forms yields the corresponding
identity for all doubled Hodge labels.  This is the basis-covariant
content that survives the fixed-frame determinant counterexample.

## 4. What the identity does and does not control

For a complement-balanced code,
\[
 \|\omega_i\|^2=\|\omega_{\bar i}\|^2=\frac18
 \qquad(i=1,2,4,8).                                        \tag{23}
\]
Equation (2) couples the holomorphic quadratics of these eight vectors,
but (23) is Hermitian while (2) is bilinear.  There is no implication
of the form
\[
 \sum_k|q_R(L_{k_1},\ldots,L_{k_4})|
 \geq \|\omega_R\|^2.                                      \tag{24}
\]
The Fourier-rotated exact graph code gives, for every odd \(R\),
\[
 \|\omega_R\|^2=\frac18,
 \qquad
 \sum_k|q_R(L_{k_1},\ldots,L_{k_4})|=\frac1{24}.             \tag{25}
\]
All eight \(q_R(k)\) are phase-aligned at each supported \(k\), so
\[
 \sum_k\left|\sum_Rq_R(k)\right|
 =\sum_R\sum_k|q_R(k)|
 =\frac13.                                                  \tag{26}
\]
Thus neither equal Hermitian sector masses nor the affine Pluecker
identity supplies the missing magnitude estimate.

A determinant route must retain the full polarized covariant and use a
local-unitary-invariant norm, or optimize over local Hodge frames.  The
remaining explicit lemma suggested by this route is the frame-optimized
inequality
\[
 \sup_{g_1,\ldots,g_4\in U(3)}
 \sum_{k\in\{0,1,2\}^4}
 \left|
 \sum_{R\ {\rm odd}}
 q_R(g_1^TL_{k_1}g_1,\ldots,g_4^TL_{k_4}g_4)
 \right|\geq1,                                             \tag{27}
\]
under (23).  Identity (2) reduces its eight sector polynomials to five,
but no proof of (27) is presently known.

## Research log

- **2026-07-28 19:06 PDT.** Exact sparse integer evaluations gave rank
  five for the eight pointwise sector quadratics and the nullspace
  displayed in (1).
- **2026-07-28 19:13 PDT.** Reduced the nullspace to the four-qubit moment
  identity (12), then proved it by double antisymmetrization and the
  two-dimensional epsilon identity.
- **2026-07-28 19:18 PDT.** The exact Fourier-rotated graph code refuted
  the sectorwise magnitude inequality (24): each sector has Hermitian
  mass \(1/8\) but Hodge \(\ell^1\)-mass \(1/24\).
