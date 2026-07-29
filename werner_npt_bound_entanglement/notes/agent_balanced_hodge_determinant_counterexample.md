# Exact obstruction to the balanced Hodge-determinant route

## Status

The proposed implication
\[
 A_T=A_{\bar T}\quad(0<|T|<4)
 \quad\Longrightarrow\quad
 \sum_{k\in\{0,1,2\}^4}
 \left|\det\!\left(U^T
 (L_{k_1}\otimes\cdots\otimes L_{k_4})U\right)\right|=1
 \tag{1}
\]
is false.  More importantly, the lower bound with `\(=1\)` replaced by
`\(\geq1\)`, which would have been enough to prove
`\(p_{1234}\geq1/8\)`, is also false.

An exact complement-balanced code has determinant sum
`\(\sqrt{21}/3\)`.  Applying a unitary qutrit Fourier transform on one
physical site preserves every moment `\(A_T\)` but changes the determinant
sum to
\[
 \boxed{\frac13}.
 \tag{2}
\]
Thus the failure is intrinsic to the fixed-coordinate `\(\ell^1\)` norm
of the determinant tensor.  It does not refute complement-balance
positivity itself.

All calculations below are over the Eisenstein integers and are replayed
by
`verification/verify_balanced_hodge_determinant_counterexample.py`.

The determinant tensor is intrinsically a quadratic form of the common
Pluecker vector.  With
\[
 \omega=\frac{u\otimes v-v\otimes u}{\sqrt2},
 \tag{3}
\]
and any symmetric matrix `\(B\)`, direct expansion gives
\[
 \boxed{\quad
 \det(U^TBU)=\omega^T(B\otimes B)\omega .
 \quad}
 \tag{4}
\]
Indeed, the right side is
`\((u^TBu)(v^TBv)-(u^TBv)(v^TBu)\)`.  In the present problem
`\(B=B_k\)` is symmetric because it is a tensor product of four skew
matrices.  Formula (4) is exact, but the counterexample below shows that
the coordinate `\(\ell^1\)` norm of these 81 Pluecker quadratics has no
basis-independent lower bound of one.

## 1. The balanced graph code

Let `\(\zeta^2+\zeta+1=0\)`.  Label the physical computational basis by
`\(\mathbb F_3^4\)`.  Put
\[
 A=
 \begin{pmatrix}
 0&2&2&1\\
 2&0&2&1\\
 2&2&0&1\\
1&1&1&0
 \end{pmatrix},
 \qquad
 s=(2,2,2,1),
 \tag{5}
\]
and
\[
 q(x)=\sum_{i<j}A_{ij}x_ix_j.
 \tag{6}
\]
Define
\[
 u=\frac19\sum_{x\in\mathbb F_3^4}\zeta^{q(x)}|x\rangle,
 \qquad
 v=\frac19\sum_{x\in\mathbb F_3^4}
       \zeta^{q(x)+s\cdot x}|x\rangle.
 \tag{7}
\]
Both vectors have norm one.  Moreover,
\[
 \langle u,v\rangle
 =\frac1{81}\sum_x\zeta^{s\cdot x}=0
 \tag{8}
\]
because `\(s\ne0\)`.  Hence `\(U=(u\ v)\)` is an isometry.

For `\(P=UU^\dagger\)`, exact contraction of the reduced matrices gives
\[
 A_\varnothing=4,\qquad A_{1234}=2,\qquad
 A_T=\frac43\quad(0<|T|<4).
 \tag{9}
\]
In particular the code is complement-balanced.  Walsh inversion gives
\[
 \begin{aligned}
 16p_{1234}
 &=\sum_T(-1)^{|T|}A_T\\
 &=4+2+\frac43(-4+6-4)=\frac{10}{3},
 \end{aligned}
 \qquad
 \boxed{p_{1234}=\frac5{24}}.
 \tag{10}
\]

Equation (9) is a finite Eisenstein-integer calculation.  To make the
certificate explicit, if `\(T\)` is retained then every entry of
`\(\operatorname{Tr}_{\bar T}P\)` has the form
\[
 \frac1{81}\sum_{z\in\mathbb F_3^{\bar T}}
 \left[
 \zeta^{q(x,z)-q(y,z)}
 +\zeta^{q(x,z)+s\cdot(x,z)-q(y,z)-s\cdot(y,z)}
 \right].
 \tag{11}
\]
Summing the Eisenstein norms of (11) over `\(x,y\)` gives exactly the
three values in (9).  The verifier performs only these displayed finite
sums.

## 2. The unrotated determinant tensor

Let
\[
 (L_k)_{ab}=\epsilon_{kab},\qquad
 B_k=L_{k_1}\otimes L_{k_2}\otimes L_{k_3}\otimes L_{k_4},
 \qquad S_k=U^TB_kU.
 \tag{12}
\]
Every entry of `\(S_k\)` lies in `\(81^{-1}\mathbb Z[\zeta]\)`, so every
determinant lies in `\(6561^{-1}\mathbb Z[\zeta]\)`.  Direct substitution
of (7) into (12) gives, for every one of the 81 labels `\(k\)`,
\[
 N_{\mathbb Q(\zeta)/\mathbb Q}
 \bigl(6561\det S_k\bigr)
 =15309=3^7\cdot7.
 \tag{13}
\]
Therefore
\[
 |\det S_k|=\frac{\sqrt{21}}{243},
 \qquad
 \sum_k|\det S_k|=\frac{\sqrt{21}}3.
 \tag{14}
\]
This already disproves the equality in (1), but it does not disprove
the lower bound needed by the proposed proof.

## 3. One local Fourier transform

Let
\[
 F_{ab}=\frac1{\sqrt3}\zeta^{ab}
 \tag{15}
\]
and set
\[
 \widetilde U=(F\otimes I\otimes I\otimes I)U.
 \tag{16}
\]
This is a local unitary.  Consequently every swap moment `\(A_T\)` in
(9), and hence complement balance and (10), is unchanged.

The transformed columns have a particularly sparse exact form.  Writing
the output coordinate as `\((a,b,c,d)\)`,
\[
 \widetilde u_{a b c d}
 =\frac{\zeta^{\,2bc+bd+cd}}{3\sqrt3}\,
  {\bf1}_{a+2b+2c+d=0},
 \tag{17}
\]
\[
 \widetilde v_{a b c d}
 =\frac{\zeta^{\,2bc+bd+cd+2b+2c+d}}{3\sqrt3}\,
  {\bf1}_{a+2b+2c+d+2=0}.
 \tag{18}
\]
Indeed, (17)--(18) follow from
`\(\sum_{r=0}^2\zeta^{rh}=3{\bf1}_{h=0}\)`.  Each column has 27
nonzero entries and the supports are disjoint, so orthonormality is also
immediate from these formulas.

Put
\[
 \widetilde S_k=\widetilde U^TB_k\widetilde U.
 \tag{19}
\]
Now each matrix entry has denominator 27 and each determinant has
denominator 729.  Substitution of (17)--(18) gives the following complete
finite table for the determinant numerators:
\[
 729\det\widetilde S_k=
 \begin{cases}
 0,&54\text{ labels},\\
 -9\zeta,&12\text{ labels},\\
 -9,&9\text{ labels},\\
 9+9\zeta=-9\zeta^2,&6\text{ labels}.
 \end{cases}
 \tag{20}
\]
Thus exactly 27 determinants are nonzero and all have modulus `\(1/81\)`.
It follows that
\[
 \boxed{\qquad
 \sum_k|\det\widetilde S_k|
 =27\cdot\frac1{81}=\frac13<1.
 \qquad}
 \tag{21}
\]

For completeness, the nonzero labels `\(k_1k_2k_3k_4\)` are
\[
\begin{gathered}
0002,0010,0021,0100,0111,0122,0201,0212,0220,\\
1001,1012,1020,1102,1110,1121,1200,1211,1222,\\
2000,2011,2022,2101,2112,2120,2202,2210,2221.
\end{gathered}
\tag{22}
\]
Equations (17)--(22) constitute a short direct algebraic certificate;
the verifier checks them without floating-point arithmetic.

### Exact failure of the sectorwise lower bound

This example also pinpoints which finer proposed sublemma fails.  Let
`\(\omega=(\widetilde u\otimes\widetilde v-
\widetilde v\otimes\widetilde u)/\sqrt2\)`, let `\(\Pi_R\)` be the
local-swap sector projector, and put
\[
 d_{R,k}=(\Pi_R\omega)^T(B_k\otimes B_k)(\Pi_R\omega).
\]
Exact Eisenstein contraction gives the stronger pointwise identity
\[
 \boxed{\qquad
 d_{R,k}=\frac18\det\widetilde S_k
 \quad\text{for every odd }R\text{ and every }k.
 \qquad}
 \tag{22a}
\]
One short way to verify it is to take the Walsh transform in `\(R\)`.
For
`\(
h_{T,k}=\omega^TF_T(B_k\otimes B_k)\omega
\)`,
the exact values are
\[
 h_{\varnothing,k}=\det\widetilde S_k,\qquad
 h_{[4],k}=-\det\widetilde S_k,\qquad
 h_{T,k}=0\quad(0<|T|<4),
 \tag{22b}
\]
which invert to (22a).

Complement balance gives
`\(\|\Pi_R\omega\|^2=1/8\)` for every odd `\(R\)`.  Nevertheless,
(21) and (22a) give
\[
 \sum_k|d_{R,k}|
 =\frac18\sum_k|\det\widetilde S_k|
 =\frac1{24}
 <\frac18=\|\Pi_R\omega\|^2.
\]
Thus all eight odd-sector determinant contributions do align phasewise;
the failure is exactly the attempted sectorwise
`\(\ell^1\)`-versus-mass lower bound, by a factor of three.

## 4. Consequence for the four-copy attack

For every `\(2\times2\)` complex matrix,
\[
 \|S\|_F^2\geq2|\det S|.
 \tag{23}
\]
Together with the exact Hodge identity
\[
 \sum_k\|S_k\|_F^2=16p_{1234},
 \tag{24}
\]
the hoped-for estimate `\(\sum_k|\det S_k|\geq1\)` would imply
`\(p_{1234}\geq1/8\)`.  The rotated code proves that this estimate is
false even on a highly regular interior balanced code:
\[
 p_{1234}=\frac5{24},
 \qquad
 \sum_k|\det\widetilde S_k|=\frac13.
 \tag{25}
\]

The obstruction is basis dependence.  Complement balance and
`\(\sum_k\|S_k\|_F^2\)` are invariant under local physical unitaries,
whereas the fixed-coordinate `\(\ell^1\)` norm of the determinant tensor
is not.  Any viable determinant argument must therefore optimize over
local Hodge frames or replace this `\(\ell^1\)` quantity by a genuinely
local-unitary-invariant norm.

The immediate frame-optimized replacement is
\[
 \boxed{\quad
 \sup_{g_1,\ldots,g_4\in U(3)}
 \sum_k\left|
 \det\!\left[
 U^T\bigotimes_{i=1}^4(g_i^TL_{k_i}g_i)U
 \right]\right|\ \stackrel{?}{\geq}\ 1 .
 \quad}
 \tag{26}
\]
It would still imply `\(p_{1234}\geq1/8\)`, because (24) is unchanged
by the same local frame rotation.  The present counterexample does not
refute (26): for the Fourier-rotated code, choosing
`\(g_1=F^{-1}\)` and the other `\(g_i=I\)` returns the unrotated value
`\(\sqrt{21}/3>1\)`.  No general proof of (26) is presently known.

## Research log

- **2026-07-28 18:52 PDT.** Found the exact balanced graph code (5)--(7),
  with all proper moments equal to `\(4/3\)` and unrotated determinant
  sum `\(\sqrt{21}/3\)`.
- **2026-07-28 19:02 PDT.** Applied a Fourier transform on one physical
  site.  The determinant sum dropped exactly to `\(1/3\)`, disproving
  both the proposed equality and its proof-relevant lower-bound
  relaxation.
- **2026-07-28 19:11 PDT.** Completed the independent
  Eisenstein-integer verifier and the sparse formulas (17)--(22).
