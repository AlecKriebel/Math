# Variational equations for rank-two code projections

Checkpoint: 2026-07-28 13:23 PDT.

This note develops the Grassmannian Euler equations and Hessian for the
endpoint functional, records exact stationary families, and isolates a
precise structural classification which would prove the endpoint theorem
by induction.  It also gives an exact nonfactor equality code at five sites,
showing that a factor-only classification cannot hold for all \(n\).

Throughout this note the local dimension is \(3\), and
\[
 {\cal L}(X)=X-\frac12\operatorname{Tr}(X)I_3,\qquad
 \Phi_n={\cal L}^{\otimes n}.
 \tag{1}
\]
The map \({\cal L}\), and hence \(\Phi_n\), is self-adjoint for the
Hilbert--Schmidt inner product.  For a rank-two orthogonal projection \(P\)
on \((\mathbb C^3)^{\otimes n}\), set
\[
 Q_n(P)=\langle P,\Phi_n(P)\rangle,\qquad A=\Phi_n(P).
 \tag{2}
\]
This is the same as
\[
 Q_n(P)=\operatorname{Tr}\left[
 (P\otimes P)\prod_{i=1}^n(F_i-I/2)\right].
 \tag{3}
\]

## 1. Exact first-order equation

Let \(P(t)=e^{tK}Pe^{-tK}\), where \(K^\dagger=-K\).  Then
\[
 \dot P=[K,P].
 \]
Self-adjointness of \(\Phi_n\) gives
\[
 \frac{d}{dt}Q_n(P(t))\bigg|_{t=0}
 =2\langle[K,P],A\rangle.
 \tag{4}
\]

### Proposition 1 (Euler equation)

A rank-two projection \(P\) is a critical point of \(Q_n\) on
\(\operatorname{Gr}(2,3^n)\) if and only if
\[
 \boxed{[P,\Phi_n(P)]=0.}
 \tag{5}
\]

Equivalently, if \(U:\mathbb C^2\to(\mathbb C^3)^{\otimes n}\) is an
isometry with \(P=UU^\dagger\), then
\[
 AU=UB,\qquad B=U^\dagger AU=B^\dagger.
 \tag{6}
\]
At a critical point,
\[
 Q_n(P)=\operatorname{Tr}B.
 \tag{7}
\]

#### Proof

Cyclicity in (4) gives
\[
 \langle[K,P],A\rangle=\operatorname{Tr}(K[P,A]).
 \]
As \(K\) ranges over all skew-Hermitian matrices, this vanishes exactly
when \([P,A]=0\).  Equation (6) is the same block-invariance statement in
an orthonormal code frame. \(\square\)

Thus a critical code is a self-consistent two-dimensional invariant
subspace of \(A=\Phi_n(P)\).  If \(B\) is diagonalized in the logical
frame, its two eigenvalues \(\lambda_0,\lambda_1\) satisfy
\[
 A u_r=\lambda_r u_r,\qquad
 Q_n(P)=\lambda_0+\lambda_1.
 \tag{8}
\]

## 2. Exact Grassmann Hessian

Write the ambient space as
\(\operatorname{ran}P\oplus\operatorname{ran}P^\perp\).  A tangent vector
is represented uniquely by a matrix
\[
 Z:\mathbb C^2\longrightarrow\operatorname{ran}P^\perp,
 \qquad U^\dagger Z=0.
 \]
Take
\[
 K=ZU^\dagger-UZ^\dagger.
 \]
Then
\[
 \dot P=\Delta=ZU^\dagger+UZ^\dagger,
 \tag{9}
\]
\[
 \ddot P=2ZZ^\dagger-2U Z^\dagger ZU^\dagger.
 \tag{10}
\]

### Proposition 2 (Hessian formula)

At a critical projection \(P\),
\[
 \boxed{\begin{aligned}
 \operatorname{Hess}_P Q_n[Z,Z]
 &=4\operatorname{Tr}\!\left[
 Z^\dagger AZ-Z^\dagger ZB\right]\\
 &\quad+2\langle\Delta,\Phi_n(\Delta)\rangle,
 \qquad
 \Delta=ZU^\dagger+UZ^\dagger .
 \end{aligned}}
 \tag{11}
\]
The associated self-adjoint real-linear tangent operator is
\[
 {\mathscr H}_P(Z)
 =
 4P^\perp\left[
 AZ-ZB+\Phi_n(\Delta)U\right],
 \tag{12}
\]
in the sense that
\[
 \operatorname{Hess}_P Q_n[Z,Z]
 =\operatorname{Re}\operatorname{Tr}
       (Z^\dagger{\mathscr H}_P(Z)).
 \]
Every local minimum must satisfy
\[
 {\mathscr H}_P\succeq0.
 \tag{13}
\]

#### Proof

Differentiate \(Q_n(P)=\langle P,\Phi_n(P)\rangle\) twice:
\[
 Q_n''(0)
 =2\langle\ddot P,A\rangle
  +2\langle\dot P,\Phi_n(\dot P)\rangle.
 \]
Use (10), \(AU=UB\), and cyclicity.  This gives (11).  For Hermitian
\(\Phi_n(\Delta)\),
\[
 \langle\Delta,\Phi_n(\Delta)\rangle
 =2\operatorname{Re}\operatorname{Tr}
   [Z^\dagger\Phi_n(\Delta)U],
 \]
which yields (12). \(\square\)

For a single-column rotation \(Z=|w\rangle\langle r|\), where
\(w\perp\operatorname{ran}P\), \(\|w\|=1\), and \(B|r\rangle=\lambda_r|r\rangle\),
(11) becomes
\[
 4\bigl(\langle w|A|w\rangle-\lambda_r\bigr)
 +2\left\langle
 |w\rangle\langle u_r|+|u_r\rangle\langle w|,
 \Phi_n\!\left(
 |w\rangle\langle u_r|+|u_r\rangle\langle w|
 \right)\right\rangle
 \ge0.
 \tag{14}
\]
This is an exact necessary inequality at every local minimum.

There is also a useful finite-swap inequality at a global minimum.  Replace
\(p_{u_r}=|u_r\rangle\langle u_r|\) by
\(p_w=|w\rangle\langle w|\), and put \(D=p_w-p_{u_r}\).  Exact quadraticity
gives
\[
 0\le
 Q_n(P+D)-Q_n(P)
 =
 2\bigl(\langle w|A|w\rangle-\lambda_r\bigr)
 +\langle D,\Phi_n(D)\rangle.
 \tag{15}
\]

### Symmetry zero modes

The functional is invariant under all local unitaries:
\[
 Q_n\!\left[
 (U_1\otimes\cdots\otimes U_n)P
 (U_1\otimes\cdots\otimes U_n)^\dagger
 \right]=Q_n(P).
 \]
At a critical point, every nontrivial tangent to this local-unitary orbit
is therefore in the Hessian kernel.  A large nullspace at an equality code
is expected and is not by itself evidence of an unstable direction.

## 3. Block recursion for the Euler equation

Split off the first qutrit and write
\[
 U=\sum_{i=0}^2|i\rangle\otimes V_i,
 \qquad
 \sum_iV_i^\dagger V_i=I_2.
 \tag{16}
\]
Let \(\Psi=\Phi_{n-1}\) and
\[
 R=\sum_iV_iV_i^\dagger.
 \]
The \(3\times3\) blocks of \(P\) and \(A\) are
\[
 P_{ij}=V_iV_j^\dagger,
 \]
\[
 A_{ij}
 =
 \Psi(V_iV_j^\dagger)
 -\frac12\delta_{ij}\Psi(R).
 \tag{17}
\]
Hence the exact critical equations are
\[
 \boxed{
 \sum_{j=0}^2\Psi(V_iV_j^\dagger)V_j
 -\frac12\Psi(R)V_i
 =V_iB,\qquad i=0,1,2.}
 \tag{18}
\]
The objective obeys the matching recursion
\[
 Q_n(P)
 =
 \sum_{i,j}
 \left\langle V_iV_j^\dagger,
 \Psi(V_iV_j^\dagger)\right\rangle
 -\frac12\langle R,\Psi(R)\rangle.
 \tag{19}
\]
Equations (18)--(19) are a concrete nonlinear eigenproblem for an
all-\(n\) induction.  The obstruction is that the off-diagonal
\(V_iV_j^\dagger\) are non-Hermitian rank-two matrices, so positivity only
for rank-two projections does not close the recursion.

## 4. Two exact stationary families

### 4.1 Coordinate two-word codes

Let \(x,y\in\{0,1,2\}^n\) and
\[
 P=|x\rangle\langle x|+|y\rangle\langle y|.
 \]
Since \(\Phi_n(P)\) is diagonal, \(P\) is automatically stationary.  If
\(h=d_H(x,y)\), then
\[
 \langle z|\Phi_n(P)|z\rangle
 =
 2^{-n}\left[
 (-1)^{d_H(z,x)}+(-1)^{d_H(z,y)}\right],
 \tag{20}
\]
and therefore
\[
 \boxed{
 Q_n(P)=2^{1-n}\left(1+(-1)^h\right).}
 \tag{21}
\]
Thus \(Q_n(P)=0\) exactly when \(h\) is odd.  If \(h<n\), every coordinate
on which \(x\) and \(y\) agree is a fixed rank-one local factor.  When
\(n\) is odd and \(h=n\), this includes the nonfactor classical repetition
equality code.

### 4.2 Commuting embedded-qubit Pauli codes

Fix a two-dimensional subspace
\(\mathbb C^2=\operatorname{span}\{|0\rangle,|1\rangle\}\subset\mathbb C^3\).
Embed the qubit matrices \(I,X,Y,Z\) by zero on \(|2\rangle\).  Let
\({\cal S}\) be a commuting group of \(2^{n-1}\) Hermitian Pauli strings,
not containing \(-I\), and let
\[
 P=2^{1-n}\sum_{g\in{\cal S}}g.
 \tag{22}
\]
Then \(P\) is the rank-two common \(+1\) projection.

Locally,
\[
 {\cal L}(\bar I)
 =\bar I-I_3=-|2\rangle\langle2|,
 \qquad
 {\cal L}(\bar X)=\bar X,\quad
 {\cal L}(\bar Y)=\bar Y,\quad
 {\cal L}(\bar Z)=\bar Z.
 \tag{23}
\]
If a string \(g\) has at least one identity position,
\(\Phi_n(g)\) is supported in a leakage sector containing \(|2\rangle\)
and annihilates the code on both sides.  If \(g\) has full support, then
\(\Phi_n(g)=g\) and \(gP=P\).

Let \(M({\cal S})\) be the number of full-support elements of
\({\cal S}\).  It follows exactly that
\[
 AP=PA=\frac{M({\cal S})}{2^{n-1}}P,
 \tag{24}
\]
\[
 \boxed{
 Q_n(P)=\frac{M({\cal S})}{2^{n-2}}\ge0.}
 \tag{25}
\]
Every such code is stationary.  It is an equality code precisely when
the group contains no full-support element.

## 5. The tensor-stable common-qubit-support cone

The preceding Pauli family sits in a much larger cone on which the
all-\(n\) endpoint inequality is immediate.

### Proposition 3

Suppose that for every site \(i\) there is a subspace
\(S_i\subset\mathbb C^3\), \(\dim S_i\le2\), such that
\[
 P=(C_1\otimes\cdots\otimes C_n)P
   (C_1\otimes\cdots\otimes C_n),
 \tag{26}
\]
where \(C_i\) projects onto \(S_i\).  Then
\[
 Q_n(P)\ge0.
 \tag{27}
\]

#### Proof

On a two-dimensional support, compression of \({\cal L}\) is
\[
 X\longmapsto X-\frac12\operatorname{Tr}(X)I_2,
 \]
the Hilbert--Schmidt orthogonal projection onto the traceless matrices.
On a one-dimensional support it is multiplication by \(1/2\).  Each
compressed local superoperator is therefore positive semidefinite.
Their tensor product is positive semidefinite, proving (27). \(\square\)

When every \(S_i\) is two-dimensional,
\[
 Q_n(P)
 =
 \left\|
 (\Pi_{\rm traceless})^{\otimes n}(P)
 \right\|_2^2.
 \tag{28}
\]
Thus equality means that the fully traceless component of \(P\) vanishes.

This cone is important for interpreting nonfactor equality codes: they can
be genuinely entangled across every cut while remaining protected by the
common local two-dimensional supports.

## 6. Exact five-site nonfactor equality and its Hessian

Consider the four commuting strings
\[
 \begin{aligned}
 g_1&=XZZXI,\\
 g_2&=IXZZX,\\
 g_3&=XIXZZ,\\
 g_4&=ZXIXZ.
 \end{aligned}
 \tag{29}
\]
Each pair anticommutes at an even number of sites, so the \(g_j\)'s
commute.  They are independent.  The projection
\[
 P_5=\frac1{16}\prod_{j=1}^4(I+g_j)
 \tag{30}
\]
has trace \(32/16=2\), hence rank two.

Direct multiplication gives the following 15 nonidentity strings (with
their stabilizing overall signs suppressed, since only support is used):
\[
\begin{gathered}
XZZXI,\ IXZZX,\ XYIYX,\ XIXZZ,\ IZYYZ,\\
XXYIY,\ IYXXY,\ ZXIXZ,\ YYZIZ,\ ZIZYY,\\
YZIZY,\ YXXYI,\ ZYYZI,\ YIYXX,\ ZZXIX.
\end{gathered}
\tag{31}
\]
Every one has weight four.  Thus \(M({\cal S})=0\), and
\[
 \Phi_5(P_5)P_5=0,\qquad Q_5(P_5)=0.
 \tag{32}
\]

### No tensor factor across any cut

For a subset \(R\) of sites, let \(s_R\) be the binary dimension of the
subgroup of stabilizing strings supported entirely in \(R\).  Pauli
orthogonality gives the exact marginal-purity formula
\[
 \operatorname{Tr}\left[
 (\operatorname{Tr}_{\bar R}P_5)^2\right]
 =
 2^{\,2-|R|+s_R}.
 \tag{33}
\]
For \(|R|\le3\), (31) gives \(s_R=0\).  For \(|R|=4\), exactly three
nonidentity strings are supported in \(R\), so \(s_R=2\).  No proper
subset has marginal purity \(4\).

A normalized state with a pure marginal factorizes across that cut.
Applied to \(P_5/2\), this says that a pure tensor factor would force one
of these unnormalized marginal purities to equal \(4\).  Therefore \(P_5\)
has no pure factor across any nontrivial cut.

This is an exact obstruction to any assertion that every nonpositive
critical code must split off a tensor factor.  It is not an obstruction
to the common-qubit-support alternative: \(P_5\) is wholly contained in
\((\mathbb C^2)^{\otimes5}\), so Proposition 3 proves its nonnegativity.

### Exact second-order certificate

The Hessian (12) at \(P_5\) is positive semidefinite.  The following table
is an exact dyadic certificate.

Decompose the qutrit Hilbert space by the leakage set
\[
 {\cal H}_R
 =
 |2\rangle_R\otimes(\mathbb C^2)^{\otimes\bar R}.
 \]
The Hessian preserves each leakage set.  In the no-leakage sector, the
15 single-site Pauli errors give 15 mutually orthogonal syndrome blocks.
The real tangent-space blocks have:

\[
\begin{array}{c|c|c|c|c}
|R|&\text{number of blocks}&
\text{real dimension per block}&
\text{annihilating polynomial}&
\text{eigenvalue multiplicities per block}\\ \hline
0&15&8&
x(x-\tfrac32)(x-2)&
0^4,(\tfrac32)^1,2^3\\
1&5&64&
x(x-\tfrac34)(x-\tfrac32)&
0^4,(\tfrac34)^{12},(\tfrac32)^{48}\\
2&10&32&
(x-\tfrac32)(x-\tfrac74)&
(\tfrac32)^8,(\tfrac74)^{24}\\
3&10&16&
x-\tfrac94&
(\tfrac94)^{16}\\
4&5&8&
x-3&
3^8\\
5&1&4&
x-\tfrac{15}{4}&
(\tfrac{15}{4})^4
\end{array}
\tag{34}
\]

The dimensions sum to
\[
 120+320+320+160+40+4=964
 =4(3^5-2),
\]
the full real Grassmann tangent dimension.  All eigenvalues are
nonnegative.

Here is a small independent exact verification architecture for (34).

1. Obtain two real code columns by normalizing
   \(P_5|00000\rangle\) and \(P_5|00001\rangle\).  Each has 16 entries
   equal to \(\pm1/4\).
2. Use the 15 subspaces
   \(\sigma_a^{(i)}\operatorname{ran}P_5\) for \(R=\varnothing\), and
   computational bases of \({\cal H}_R\) for \(R\ne\varnothing\).
3. Build (12) using only the local rational identity
   \[
   \left\langle E_{ab},{\cal L}(E_{cd})\right\rangle
   =
   \delta_{ac}\delta_{bd}
   -\frac12\delta_{ab}\delta_{cd}.
   \tag{35}
   \]
4. The resulting matrices have dyadic rational entries.  Exact
   multiplication gives the annihilating polynomials in (34).  The
   exact traces and squared traces are
   \[
   \begin{array}{c|cccccc}
   |R|&0\text{ (per syndrome)}&1&2&3&4&5\\ \hline
   \operatorname{Tr}{\mathscr H}&
   15/2&81&54&36&24&15\\
   \operatorname{Tr}{\mathscr H}^2&
   57/4&459/4&183/2&81&72&225/4.
   \end{array}
   \tag{36}
   \]
   Together with the block dimensions and the distinct rational roots,
   these traces determine the multiplicities in (34).

Thus \(P_5\) is an exact stationary equality code which also passes the
full second-order necessary condition.  Positive-semidefinite Hessian does
not by itself exclude instability at higher order.

## 7. Exact four-site classification inside the commuting-Pauli family

For \(n=4\), (25) says that a commuting-Pauli code is an equality code
exactly when its three-dimensional isotropic binary subspace contains no
full-support vector.  In this subclass every equality code does factor.

This was checked by a complete finite enumeration, not random sampling:

\[
\begin{array}{c|r}
\text{three-dimensional subspaces of }\mathbb F_2^8&97155\\
\text{totally isotropic subspaces}&11475\\
\text{isotropic subspaces with no weight-four vector}&864\\
\text{of these with no pure stabilizer factor}&0.
\end{array}
\tag{37}
\]
Among the 864 equality spaces, 648 have a one-site pure factor and 216
have a pure three-site factor (equivalently, the logical qubit is localized
on the remaining site).

The exact verifier enumerates every binary reduced-row-echelon
\(3\times8\) matrix.  For each row space \(S\), it checks
\[
 \langle(x,z),(x',z')\rangle_{\rm sp}
 =x\cdot z'+z\cdot x'=0
\]
on the three rows, rejects \(S\) if some nonzero vector has all four
sites in its support, and then verifies that some proper site set \(R\)
satisfies
\[
 \dim\{v\in S:\operatorname{supp}v\subseteq R\}=|R|.
 \tag{38}
\]
RREF pivot positions make the list of 97155 row spaces exhaustive and
duplicate-free.  All operations are over \(\mathbb F_2\).

This is evidence for a four-site factor classification, but only in the
commuting-Pauli stationary subclass.

## 8. A precise structural target

The computations and exact examples suggest the following statement.

### Critical-point classification target

If
\[
 [P,\Phi_n(P)]=0,\qquad Q_n(P)\le0,
 \tag{39}
\]
then at least one of the following holds:

1. **Pure-factor reduction:** for some nontrivial cut \(R:\bar R\),
   \[
   \operatorname{Tr}\left[
   (\operatorname{Tr}_{\bar R}P)^2\right]=4
   \quad\text{or}\quad
   \operatorname{Tr}\left[
   (\operatorname{Tr}_{R}P)^2\right]=4;
   \tag{40}
   \]
   hence \(P\) factors as a lower-site rank-two code times a pure state.
2. **Common local qubit supports:** every one-site marginal of \(P\) has
   rank at most two, so Proposition 3 applies.

For \(n=4\), this classification would prove \(Q_4(P)\ge0\): in case 1
the rank-two factor occupies at most three sites, and in case 2 the
tensor-stable cone proves positivity.  If the same statement held for
all \(n\), it would prove the endpoint all-copy theorem by induction.

The five-site code in Section 6 shows why case 2 is essential.

### Why a pure factor preserves the sign

If
\[
 P=P_R\otimes|\xi\rangle\langle\xi|_{\bar R},
\]
then
\[
 Q_n(P)=Q_{|R|}(P_R)\,
 Q_{|\bar R|}(|\xi\rangle\langle\xi|).
 \tag{41}
\]
The rank-one factor on the right is strictly positive.  Indeed, in the
local swap-parity expansion of
\(|\xi\rangle\langle\xi|^{\otimes2}\), only even total local antisymmetry
occurs, and
\[
 Q_m(|\xi\rangle\langle\xi|)
 =
 2^{-m}\sum_{\substack{T\subseteq[m]\\|T|\ {\rm even}}}
 3^{|T|}r_T>0.
 \tag{42}
\]
Thus (41) has the sign of the smaller rank-two problem.

What remains missing is a proof that the Euler equation (5), together
with Hessian positivity (13) and \(Q_n(P)\le0\), forces (40) or the local
rank defects of case 2.

## 9. Fourier formulation and a stronger two-point route

Choose a local Hilbert--Schmidt orthonormal basis
\[
 \tau_0=I/\sqrt3,\qquad
 \operatorname{Tr}\tau_\mu=0\quad(\mu=1,\ldots,8).
 \]
Expand
\[
 P=\sum_{\boldsymbol\mu}\widehat P_{\boldsymbol\mu}
 \tau_{\mu_1}\otimes\cdots\otimes\tau_{\mu_n},
\]
and let
\[
 W_k(P)=
 \sum_{\#\{i:\mu_i\ne0\}=k}
 |\widehat P_{\boldsymbol\mu}|^2.
 \]
Then
\[
 W_k\ge0,\qquad
 \sum_{k=0}^nW_k=\operatorname{Tr}P^2=2,\qquad
 W_0=\frac4{3^n},
 \tag{43}
\]
and
\[
 \boxed{
 Q_n(P)=
 \sum_{k=0}^n
 \left(-\frac12\right)^{n-k}W_k(P).}
 \tag{44}
\]
An all-copy Fourier proof must establish the signed dominance
\[
 \sum_{\substack{k\\n-k\ {\rm even}}}
 2^{-(n-k)}W_k
 \ge
 \sum_{\substack{k\\n-k\ {\rm odd}}}
 2^{-(n-k)}W_k
 \tag{45}
\]
using the nonlinear projection identity \(P^2=P\).  Positivity of the
weights alone is far too weak.

If \(T_\rho\) denotes the usual depolarizing noise operator which fixes
the identity and multiplies every traceless local operator by \(\rho\),
then
\[
 \Phi_n=(-1/2)^nT_{-2}^{\otimes n}.
 \tag{46}
\]
The required point is outside the ordinary contractive noise range.
Consequently a standard positive-parameter hypercontractive inequality
does not directly control (44); a rank-two, signed version would be
needed.

### Two-point kernel inequality

For unit vectors \(u,v\), define
\[
 \kappa_n(u,v)
 =
 \left\langle |u\rangle\langle u|,
 \Phi_n(|v\rangle\langle v|)\right\rangle.
 \tag{47}
\]
If \(P=p_u+p_v\) with \(u\perp v\), then
\[
 Q_n(P)=\kappa_n(u,u)+\kappa_n(v,v)+2\kappa_n(u,v).
 \tag{48}
\]
The stronger inequality
\[
 |\kappa_n(u,v)|^2
 \le\kappa_n(u,u)\kappa_n(v,v)
 \tag{49}
\]
would imply \(Q_n(P)\ge0\) immediately.  Equivalently, it asks for
nonnegativity of the \(\Phi_n\)-quadratic form on every Hermitian
two-dimensional span generated by two pure projectors.

At one site,
\[
 \kappa_1(u,v)=|\langle u,v\rangle|^2-\frac12,
\]
so (49) holds sharply.  However the kernel is not positive definite on
three points: for three orthogonal local basis vectors its Gram matrix
has diagonal \(1/2\), off-diagonal \(-1/2\), and a negative eigenvalue.
Thus any proof of (49) must be intrinsically two-point/rank-two; it cannot
come from positivity of \(\Phi_n\) on the whole positive cone.

The finite-swap condition (15) is a variational manifestation of exactly
this two-point kernel.

## 10. Failed parity-layer closure at four sites

Let
\[
 r_T=\operatorname{Tr}[(P\otimes P)\Pi_T],\qquad
 R_t=\sum_{|T|=t}r_T.
 \]
Average the proved three-block inequality over the six partitions
consisting of one merged pair and two singleton blocks; call this average
\(\overline Q_{\rm merge}\).  Direct parity algebra gives
\[
 Q_4(P)-\frac12\overline Q_{\rm merge}(P)
 =
 \frac1{12}\left(R_2-9R_3+54R_4\right).
 \tag{50}
\]
It was tempting to try to prove the residual nonnegative.  This is false,
even at exact stationary equality codes.  A coordinate code whose two
words have Hamming distance \(3\) has
\[
 (R_0,R_1,R_2,R_3,R_4)
 =
 \left(\frac94,\frac34,\frac34,\frac14,0\right),
 \]
\[
 Q_4=0,\qquad
 R_2-9R_3+54R_4=-\frac32.
 \tag{51}
\]
Direct minimization of the residual functional reaches the further
exact-looking value \(-3\).  Hence neither stationarity nor the grouped
three-block inequalities can be closed by this standalone layer
inequality.

## 11. Discovery computations

All numerical work in this section is discovery evidence only.

- Real Grassmann descent from 30 random starts at \(n=3\), 30 starts at
  \(n=4\), and 10 starts at \(n=5\) reached \(Q_n\) between
  \(2\times10^{-13}\) and \(6\times10^{-12}\), never a negative value.
- Complex Grassmann descent from 20 random starts at \(n=4\) and 10 starts
  at \(n=5\) likewise reached \(Q_n\approx0\), never a negative basin.
- Every inspected \(n=4\) zero limit had a subset marginal purity
  numerically equal to \(4\), hence a pure factor across that cut.
- At \(n=5\), both factorized limits and nonfactor limits occurred.  This
  is consistent with the exact five-site equality code above.
- The exact Hessian certificate (34)--(36) was checked independently with
  rational arithmetic using only dyadic entries and (35).

No additional hardware is needed for the exact calculations here.
Larger-memory parallel optimization could search much larger \(n\), but
it would not convert finite-copy numerical evidence into an all-copy
proof.

## 12. Status

Established exactly:

1. the full first- and second-order Grassmann equations (5), (11), and
   (12);
2. the block recursion (18)--(19);
3. exact coordinate and commuting-Pauli stationary families;
4. the tensor-stable common-local-qubit-support cone;
5. a genuine nonfactor five-site equality code with an exact
   positive-semidefinite Hessian;
6. an exhaustive factor classification for four-site commuting-Pauli
   equality codes;
7. the signed Fourier formulation and the precise two-point kernel
   inequality which would settle all copies.

Not established:

- a classification of all nonpositive critical projections at \(n=4\);
- the structural alternative in Section 8;
- \(Q_4(P)\ge0\) for every rank-two projection;
- the all-copy endpoint theorem.

The main actionable target is now sharply stated: combine the nonlinear
Euler system (18) and Hessian positivity (11) to force either a pure
factor or common local two-dimensional supports whenever \(Q_n(P)\le0\).

## 13. Stress test of a proposed sector hierarchy

Checkpoint: 2026-07-28 14:25 PDT.

For the parity masses in (50), consider
\[
 H_j(P)=
 \sum_{\ell\ge j}\binom{2\ell}{2j}R_{2\ell}
 -3R_{2j+1}.
 \tag{52}
\]
The first member is
\[
 H_1=\sum_{\ell\ge1}\binom{2\ell}{2}R_{2\ell}-3R_3.
 \tag{53}
\]
At four sites this is the sharp-looking inequality
\[
 H_1=R_2+6R_4-3R_3.
 \tag{54}
\]

The full hierarchy (52) is false.  The obstruction is exact and already
occurs in the five-site cyclic equality code of Section 6.

### 13.1 Exact purity form

Put
\[
 p_S=\operatorname{Tr}\left[
       \left(\operatorname{Tr}_{\bar S}P\right)^2\right].
 \tag{55}
\]
The swap identity
\[
 p_S=\operatorname{Tr}[(P\otimes P)F_S]
     =\sum_T(-1)^{|S\cap T|}r_T
 \]
and Walsh inversion give
\[
 r_T=2^{-n}\sum_S(-1)^{|S\cap T|}p_S.
 \tag{56}
\]
Consequently
\[
 H_j(P)=\sum_{S\subseteq[n]}a^{(n,j)}_{|S|}p_S,
 \tag{57}
\]
where
\[
 a^{(n,j)}_s
 =
 2^{-n}\left[
 \sum_{\ell\ge j}\binom{2\ell}{2j}K^{(n)}_{2\ell}(s)
 -3K^{(n)}_{2j+1}(s)\right],
 \tag{58}
\]
\[
 K^{(n)}_t(s)
 =
 \sum_q(-1)^q\binom{s}{q}\binom{n-s}{t-q}.
 \tag{59}
\]
Equations (55)--(59) give an efficient exact evaluator and a
Grassmann gradient: the ambient \(P\)-gradient of \(p_S\) is
\[
 2\left(\operatorname{Tr}_{\bar S}P\right)\otimes I_{\bar S},
 \tag{60}
\]
with tensor factors restored to their original order.  Thus the same
Euler and Hessian calculation as in Sections 1--2 applies to every
\(H_j\).

### 13.2 Coordinate codes obey every member

For a coordinate code whose two words differ on \(D\), \(|D|=h\ge1\),
direct local symmetric/antisymmetric decomposition gives
\[
 r_\varnothing=2+2^{1-h},\qquad
 r_T=2^{1-h}\quad(\varnothing\ne T\subseteq D),
 \qquad
 r_T=0\quad(T\not\subseteq D).
 \tag{61}
\]
It follows that, when \(h>2j\),
\[
 H_j
 =
 2^{1-h}\binom{h}{2j}
 \left[
 2^{h-2j-1}
 -\frac{3(h-2j)}{2j+1}\right],
 \tag{62}
\]
while for \(h=2j\),
\[
 H_j=2^{1-2j}.
 \tag{63}
\]
For \(h<2j\), \(H_j=0\).
These quantities are nonnegative.  Indeed, for
\(m=h-2j\ge1\), one needs
\[
 2^{m-1}\ge\frac{3m}{2j+1}.
 \]
For \(j=1\), this is \(2^{m-1}\ge m\); for \(j\ge2\), it follows from
\(2^{m-1}\ge m\) and \(3/(2j+1)\le3/5<1\).
Thus the coordinate stationary family does not expose the failure below.

### 13.3 Exact five-site counterexample to \(H_2\)

Use the four commuting independent generators
\[
 XZZXI,\qquad IXZZX,\qquad XIXZZ,\qquad ZXIXZ
 \tag{64}
\]
on the embedded qubit space, and let \({\cal S}\) be their group.  As in
(22),
\[
 P=\frac1{16}\sum_{g\in{\cal S}}g
 \tag{65}
\]
is a rank-two orthogonal projection.  Every one of the fifteen
nonidentity group elements has weight four.

For \(S\subseteq[5]\), let
\[
 N_S=\#\{g\in{\cal S}:\operatorname{supp}g\subseteq S\}.
 \]
Pauli orthogonality gives the exact marginal-purity formula
\[
 p_S=2^{2-|S|}N_S.
 \tag{66}
\]
There is only the identity when \(|S|\le3\).  For each four-set there
are exactly three nonidentity group elements supported in it, and all
sixteen group elements are supported in the full set.  Hence \(p_S\)
depends only on \(s=|S|\), with
\[
 (p_0,p_1,p_2,p_3,p_4,p_5)
 =
 \left(4,2,1,\frac12,1,2\right).
 \tag{67}
\]
Walsh inversion (56) now gives
\[
 r_T=
 \begin{cases}
 9/8,&|T|=0,\\
 3/16,&|T|=1,\\
 3/16,&|T|=2,\\
 0,&|T|=3,\\
 0,&|T|=4,\\
 1/16,&|T|=5.
 \end{cases}
 \tag{68}
\]
Thus
\[
 (R_0,R_1,R_2,R_3,R_4,R_5)
 =
 \left(\frac98,\frac{15}{16},\frac{15}{8},
       0,0,\frac1{16}\right).
 \tag{69}
\]
In particular,
\[
 H_1=\frac{15}{8}>0,\qquad
 \boxed{H_2=R_4-3R_5=-\frac3{16}<0.}
 \tag{70}
\]
This is a short exact counterexample to the proposed hierarchy.  Tensoring
the code with any number of fixed one-site pure factors leaves every old
\(r_T\) unchanged and makes every sector containing a new site vanish.
Therefore the same value \(H_2=-3/16\) occurs for every \(n\ge5\).

A minimal independent verifier for (67)--(70) is:
```
from fractions import Fraction

G = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]

def bits(w):
    x = z = 0
    for i, c in enumerate(w):
        if c in "XY": x |= 1 << i
        if c in "ZY": z |= 1 << i
    return x, z

G = list(map(bits, G))
stab = []
for m in range(16):
    x = z = 0
    for i, (a, b) in enumerate(G):
        if (m >> i) & 1:
            x ^= a
            z ^= b
    stab.append((x, z))

pc = lambda m: bin(m).count("1")
assert sorted(pc(x | z) for x, z in stab) == [0] + [4] * 15
p = []
for S in range(32):
    N = sum(((x | z) & ~S) == 0 for x, z in stab)
    p.append(Fraction(4 * N, 2 ** pc(S)))

r = [sum((-1) ** pc(S & T) * p[S]
         for S in range(32)) / 32 for T in range(32)]
R = [sum(r[T] for T in range(32) if pc(T) == t)
     for t in range(6)]
assert R == [Fraction(9, 8), Fraction(15, 16), Fraction(15, 8),
             0, 0, Fraction(1, 16)]
assert R[4] - 3 * R[5] == Fraction(-3, 16)
```

### 13.4 Why a termwise conditional proof of \(H_1\) fails

There is a useful exact decomposition
\[
 H_1
 =
 \sum_{\substack{J\subseteq[n]\\|J|=2}}
 \left[
   \sum_{\substack{T\supseteq J\\|T|\ {\rm even}}}r_T
   -
   \sum_{\substack{T\supseteq J\\|T|=3}}r_T
 \right].
 \tag{71}
\]
It is tempting to prove every bracket nonnegative.  This strengthening is
false already for three sites.

Let
\[
 P=
 (|0\rangle\langle0|+|1\rangle\langle1|)_1
 \otimes|\Omega_3\rangle\langle\Omega_3|_{23}.
 \tag{72}
\]
It is a rank-two projection.  A direct swap calculation gives the only
nonzero sectors
\[
 r_\varnothing=2,\qquad
 r_{\{1\}}=\frac23,\qquad
 r_{\{2,3\}}=1,\qquad
 r_{\{1,2,3\}}=\frac13.
 \tag{73}
\]
For \(J=\{1,2\}\) and \(J=\{1,3\}\), the bracket in (71) is
\(-1/3\); for \(J=\{2,3\}\), it is \(2/3\).  Their sum is zero:
\[
 H_1=R_2-3R_3=1-1=0.
 \tag{74}
\]
Thus any proof of \(H_1\) must use cancellation among marked pairs.
Simple conditioning on a fixed antisymmetric pair cannot prove it.

### 13.5 Discovery results for the surviving \(H_1\) conjecture

This paragraph is numerical evidence only.

- Complex Grassmann descent for qutrit sites gave minima
  \(-1.4\cdot10^{-14}\) at \(n=4\) (30 starts),
  \(6.5\cdot10^{-12}\) at \(n=5\) (20 starts), and
  \(6.5\cdot10^{-7}\) at \(n=6\) (four underconverged starts).
  No nonzero negative value occurred.
- For local dimension four, the corresponding minima were
  \(-3.3\cdot10^{-15}\) at \(n=3\) (30 starts) and
  \(-9.0\cdot10^{-15}\) at \(n=4\) (30 starts).  Two underconverged
  \(n=5\) runs remained positive at \(2.1\cdot10^{-5}\) and
  \(1.4\cdot10^{-5}\).
- Exact evaluation of random commuting-Pauli rank-two codes found no
  \(H_1<0\) example: 30,000 samples each at \(n=5,6\), 20,000 at
  \(n=7\), 10,000 at \(n=8\), 5,000 at \(n=9\), and 2,000 at \(n=10\).
  Higher \(H_j\)'s were frequently negative, in agreement with (70).

The exact conclusion is therefore narrow but useful: the proposed
all-\(j\) hierarchy cannot be an induction invariant.  Its leading member
\(H_1\) survives all tests and appears dimension-independent, but remains
unproved.  Equation (71) and counterexample (72) show that a successful
conditional interpretation must average over the marked pairs before
applying positivity.
