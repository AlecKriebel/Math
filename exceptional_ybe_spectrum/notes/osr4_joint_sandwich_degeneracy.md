# Operator-Schmidt rank four: the cubic quotient and joint-sandwich degeneracy

**Date:** 2026-07-29
**Scope:** arbitrary exceptional solutions of operator-Schmidt rank four;
exact lower-assumption calibrations in \(d=4,6\)
**Status:** exact conditional divisibility theorem and universal necessary
condition; not a proof that every rank-four solution has \(4\mid d\)

## 1. Executive conclusion

Let \(H\in M_d(\mathbb C)\otimes M_d(\mathbb C)\) be an exceptional
Hermitian reflection:

\[
H^*=H,\qquad H^2=I,\qquad
\operatorname{Tr}H=0,\qquad
H_{12}H_{23}H_{12}-H_{23}H_{12}H_{23}
=\frac13(H_{12}-H_{23}).
\tag{1}
\]

Assume that \(H\) has operator-Schmidt rank four.  Its intrinsic left and
right Schmidt supports will be denoted by

\[
\mathcal A,\mathcal B\subset M_d(\mathbb C),\qquad
\dim_{\mathbb C}\mathcal A=\dim_{\mathbb C}\mathcal B=4.
\tag{2}
\]

Put

\[
\mathcal O_{\mathcal A}=\mathbb CI+\mathcal A,\qquad
\mathcal O_{\mathcal B}=\mathbb CI+\mathcal B.
\tag{3}
\]

For subspaces \(\mathcal X,\mathcal Y\subset M_d\), define the intrinsic
joint-sandwich map

\[
\mathfrak S_{\mathcal Y\mid\mathcal X}:
\mathcal Y\otimes\mathcal Y\longrightarrow
\operatorname{Hom}_{\mathbb C}(\mathcal X,M_d),
\qquad
\sum_\ell y_\ell\otimes z_\ell\longmapsto
\left[x\longmapsto\sum_\ell y_\ell xz_\ell\right].
\tag{4}
\]

The main result of this audit is:

> **Joint-sandwich divisibility theorem.**
> If either
> \[
> \mathfrak S_{\mathcal B\mid\mathcal O_{\mathcal A}}
> \quad\text{or}\quad
> \mathfrak S_{\mathcal A\mid\mathcal O_{\mathcal B}}
> \tag{5}
> \]
> is injective, then
> \[
> \boxed{4\mid d.}
> \tag{6}
> \]

Consequently, every hypothetical exceptional rank-four solution in
\(d\equiv2\pmod4\) must obey two simultaneous, gauge-invariant
degeneracies:

\[
\boxed{
\ker\mathfrak S_{\mathcal B\mid\mathcal O_{\mathcal A}}\ne0,
\qquad
\ker\mathfrak S_{\mathcal A\mid\mathcal O_{\mathcal B}}\ne0.}
\tag{7}
\]

This is stronger than requiring every individual map
\(\mathcal B\otimes\mathcal B\to M_d\), \(c\mapsto c(x)\), to be singular.
The **same** nonzero coefficient tensor must annihilate all five inputs in
\(\mathbb CI+\mathcal A\), and symmetrically on the other leg.

In a Hermitian Schmidt gauge the common kernel tensor may be chosen with a
nonzero Hermitian \(4\times4\) coefficient matrix.  It is not an arbitrary
kernel vector: it is obtained by applying a functional to the products of
the opposite Schmidt support modulo \(\mathbb CI+\mathcal A\), or modulo
\(\mathbb CI+\mathcal B\).

The proof uses the full cubic in a way absent from the earlier
four-product Clifford-frame theorem.  It covers many non-Clifford
rank-four decompositions.  It does not prove that one of (5) is always
injective.

## 2. Intrinsic Schmidt supports and the Hermitian gauge

Define the left and right slice spaces by

\[
\mathcal A=
\{(\operatorname{id}\otimes\omega)(H):\omega\in M_d^*\},
\qquad
\mathcal B=
\{(\omega\otimes\operatorname{id})(H):\omega\in M_d^*\}.
\tag{8}
\]

These spaces are intrinsic.  Any minimal factorization

\[
H=\sum_{i=1}^4 a_i\otimes b_i
\tag{9}
\]
gives bases \((a_i)\) and \((b_i)\) of \(\mathcal A\) and \(\mathcal B\).
Changing a minimal factorization only makes inverse
\(\mathrm{GL}_4(\mathbb C)\) changes on the two bases.  Hence the
injectivity in (5), defined without a basis, is gauge invariant.

Hermiticity gives a particularly useful gauge.  Expand \(H\) in real
Hilbert spaces of Hermitian matrices, using Hermitian
Hilbert--Schmidt-orthonormal bases on each leg.  The coefficient matrix is
real because

\[
\operatorname{Tr}\bigl((X\otimes Y)H\bigr)\in\mathbb R
\quad\text{for Hermitian }X,Y,H.
\tag{10}
\]

A real singular-value decomposition therefore gives

\[
H=\sum_{i=1}^4\sigma_i A_i\otimes B_i,
\qquad \sigma_i>0,
\tag{11}
\]

where \(A_i,B_i\) are Hermitian and Hilbert--Schmidt orthonormal.  In
particular, \(\mathcal A\) and \(\mathcal B\) are \(*\)-closed complex
subspaces.  Degenerate singular values only permit simultaneous real
orthogonal rotations, which do not change (4).

Automatic standardness for the exceptional class, proved in
`track_structural_projection.md`, gives

\[
\operatorname{Tr}_1H=\operatorname{Tr}_2H=0.
\tag{12}
\]

Independence of the Schmidt vectors in (11) then gives

\[
\operatorname{Tr}A_i=\operatorname{Tr}B_i=0
\quad(1\le i\le4).
\tag{13}
\]

Thus \(I\notin\mathcal A,\mathcal B\), and both operator systems in (3)
have complex dimension exactly five.

## 3. The elementary contractions

Although the quotient identity below is the new ingredient, it is useful
to record all immediate Schmidt-coordinate consequences.

Taking the two partial traces of \(H^2=I\) in (11) gives

\[
\boxed{\sum_i\sigma_i^2A_i^2=dI,\qquad
\sum_i\sigma_i^2B_i^2=dI.}
\tag{14}
\]

Taking the first and third partial traces of the cubic in (1), using
(13), gives for every \(j\)

\[
\boxed{
\sum_i\sigma_i^2B_iA_jB_i=-\frac d3A_j,
\qquad
\sum_i\sigma_i^2A_iB_jA_i=-\frac d3B_j.}
\tag{15}
\]

Equivalently, the unital completely positive maps

\[
\Phi_B(x)=\frac1d\sum_i\sigma_i^2B_ixB_i,\qquad
\Phi_A(y)=\frac1d\sum_i\sigma_i^2A_iyA_i
\tag{16}
\]

satisfy

\[
\Phi_B|_{\mathcal A}=-\frac13\operatorname{id}_{\mathcal A},
\qquad
\Phi_A|_{\mathcal B}=-\frac13\operatorname{id}_{\mathcal B}.
\tag{17}
\]

Because the Kraus matrices in (16) are Hermitian, (14) makes the two maps
bistochastic.  These contracted identities alone do not retain enough
overlap information to prove the theorem.

## 4. Exact coefficient extraction from the full cubic

For clarity first use the arbitrary minimal factorization (9).  Direct
expansion gives

\[
H_{12}H_{23}H_{12}
=\sum_{i,j,k}
a_ia_k\otimes b_ia_jb_k\otimes b_j,
\tag{18}
\]

\[
H_{23}H_{12}H_{23}
=\sum_{i,j,k}
a_j\otimes a_ib_ja_k\otimes b_ib_k.
\tag{19}
\]

Let

\[
Q_{\mathcal A}=M_d/(\mathbb CI+\mathcal A)
\tag{20}
\]

and write \([x]_{\mathcal A}\) for the quotient class.  Apply the quotient
map to the first tensor leg of the cubic.  Equation (19) vanishes because
its first factor lies in \(\mathcal A\).  Both terms on the right of (1)
vanish because their first factors lie in \(\mathcal A\) or
\(\mathbb CI\).  Therefore

\[
\sum_{i,j,k}
[a_ia_k]_{\mathcal A}
\otimes b_ia_jb_k\otimes b_j=0.
\tag{21}
\]

Apply an arbitrary linear functional to the third leg.  Since the \(b_j\)
form a basis and the \(a_j\) form a basis, the matrix

\[
x=\sum_j\lambda(b_j)a_j
\tag{22}
\]

ranges over all of \(\mathcal A\).  We obtain the exact all-\(x\)
quotient identity requested for future classification:

\[
\boxed{
\sum_{i,k}[a_ia_k]_{\mathcal A}\otimes b_i x b_k=0
\qquad(x\in\mathcal A).}
\tag{23}
\]

The identity input is supplied by involutivity, not by the cubic.  Apply
the first-leg quotient to

\[
H^2=\sum_{i,k}a_ia_k\otimes b_ib_k=I\otimes I.
\]

This gives

\[
\sum_{i,k}[a_ia_k]_{\mathcal A}\otimes b_i b_k=0.
\tag{24}
\]

Combining (23)--(24),

\[
\boxed{
\sum_{i,k}[a_ia_k]_{\mathcal A}\otimes b_i x b_k=0
\qquad(x\in\mathcal O_{\mathcal A}).}
\tag{25}
\]

Tensor reversal gives the symmetric counterpart

\[
\boxed{
\sum_{i,k}a_i y a_k\otimes[b_ib_k]_{\mathcal B}=0
\qquad(y\in\mathcal O_{\mathcal B}),}
\tag{26}
\]

where

\[
Q_{\mathcal B}=M_d/(\mathbb CI+\mathcal B).
\]

In the Hermitian Schmidt gauge (11), the precise versions are

\[
\sum_{i,k}\sigma_i\sigma_k[A_iA_k]_{\mathcal A}
\otimes B_i xB_k=0
\quad(x\in\mathcal O_{\mathcal A}),
\tag{27}
\]

\[
\sum_{i,k}\sigma_i\sigma_k A_i yA_k
\otimes[B_iB_k]_{\mathcal B}=0
\quad(y\in\mathcal O_{\mathcal B}).
\tag{28}
\]

These are complex tensor identities.  No real-linear quotient is being
used.

## 5. Proof of the joint-sandwich theorem

Suppose first that
\(\mathfrak S_{\mathcal B\mid\mathcal O_{\mathcal A}}\) is injective.
Apply any complex linear functional
\(\varphi:Q_{\mathcal A}\to\mathbb C\) to (27).  The same coefficient
matrix

\[
c_{ik}=\sigma_i\sigma_k\,
\varphi([A_iA_k]_{\mathcal A})
\tag{29}
\]

then satisfies

\[
\sum_{i,k}c_{ik}B_i xB_k=0
\qquad\text{for every }x\in\mathcal O_{\mathcal A}.
\tag{30}
\]

Injectivity says \(c_{ik}=0\) for all \(i,k\).  Since the \(\sigma_i\) are
nonzero and \(\varphi\) was arbitrary,

\[
A_iA_k\in\mathbb CI+\mathcal A
\qquad(1\le i,k\le4).
\tag{31}
\]

It follows that

\[
\mathcal S_{\mathcal A}=\mathbb CI+\mathcal A
\tag{32}
\]

is closed under multiplication.  It is unital and \(*\)-closed by
Section 2, so it is a finite-dimensional \(C^*\)-subalgebra of \(M_d\).
Its complex dimension is five.

The only abstract complex \(C^*\)-algebras of dimension five are

\[
\mathbb C^5
\qquad\text{and}\qquad
M_2(\mathbb C)\oplus\mathbb C,
\tag{33}
\]

because a finite-dimensional \(C^*\)-algebra has dimension
\(\sum_\alpha n_\alpha^2\).  Every faithful unital concrete
representation of either algebra has a rank-one projection in its
commutant:

- for \(\mathbb C^5\), take a rank-one subprojection in any nonzero joint
  spectral space;
- for \(M_2\oplus\mathbb C\), take a rank-one subprojection in the
  necessarily nonzero scalar summand.

The commutant of \(\mathcal S_{\mathcal A}\) is exactly the left one-leg
commutant of \(H\), and hence of \(P=(I-H)/2\).  Indeed, independence of
the \(B_i\) makes

\[
[X\otimes I,H]=0
\quad\Longleftrightarrow\quad
[X,A_i]=0\quad\text{for every }i.
\tag{34}
\]

The invariant leg-commutant theorem C17 now applies to this rank-one
projection and gives

\[
8\mid d^2.
\tag{35}
\]

Therefore \(4\mid d\).  The proof from injectivity of the other map is
identical with the two tensor legs exchanged.

### 5.1 The necessary common annihilators when \(d\equiv2\pmod4\)

If \(d\equiv2\pmod4\), neither \(\mathbb CI+\mathcal A\) nor
\(\mathbb CI+\mathcal B\) can be an algebra: the same five-dimensional
\(C^*\)-algebra argument would contradict C17 even without an injectivity
assumption.

Thus at least one quotient product \([A_iA_k]_{\mathcal A}\) is nonzero.
Their span is \(*\)-closed.  Choose a nonzero \(*\)-compatible functional
\(\varphi\), meaning

\[
\varphi(z^*)=\overline{\varphi(z)},
\tag{36}
\]

which detects this product span.  Then the matrix \(C=(c_{ik})\) in (29)
is nonzero and Hermitian:

\[
c_{ki}=\overline{c_{ik}}.
\tag{37}
\]

Taking the ordinary trace of (30) at \(x=I\), and using
\(\operatorname{Tr}(B_iB_k)=\delta_{ik}\), also gives

\[
\boxed{\operatorname{Tr}C=0.}
\tag{38}
\]

Thus this kernel direction is necessarily indefinite, not merely
Hermitian.

Equation (30) exhibits the promised common kernel tensor.  The symmetric
argument gives a nonzero Hermitian coefficient matrix on the other leg.
This proves more than the bare noninjectivity in (7).

## 6. A rank-three completely positive boundary consequence

The common annihilator has an additional exact interpretation.  Put

\[
D=\operatorname{diag}(\sigma_1^2,\ldots,\sigma_4^2)>0
\tag{39}
\]

and let \(C=C^*\ne0\) be the matrix from (29).  Along the real affine line
\(D+tC\), choose a nonzero endpoint \(t=t_*\) of the interval on which
\(D+tC\ge0\).  Then

\[
G=D+t_*C\ge0,\qquad 1\le\operatorname{rank}G\le3.
\tag{40}
\]

The completely positive map

\[
\Psi_B(x)=\frac1d\sum_{i,k}G_{ik}B_i xB_k
\tag{41}
\]

has Kraus rank at most three.  Since \(C\) annihilates
\(\mathcal O_{\mathcal A}\), it has exactly the same action as the
canonical map \(\Phi_B\) on that five-dimensional operator system:

\[
\boxed{
\Psi_B(I)=I,\qquad
\Psi_B|_{\mathcal A}=-\frac13\operatorname{id}_{\mathcal A}.}
\tag{42}
\]

Thus every hypothetical \(d\equiv2\pmod4\), rank-four exceptional
solution produces a **unital** CP map of Kraus rank at most three with the
prescribed negative eigenspace (42), and symmetrically on the other leg.
This may be useful with low-Kraus-rank channel structure theorems.

There is an important scope guard.  Trace preservation of (41) additionally
requires

\[
\sum_{i,k}C_{ik}B_kB_i=0.
\tag{43}
\]

Equation (25) only gives the order \(B_iB_k\).  Hence \(\Psi_B\) is not
automatically bistochastic.  It is bistochastic under the additional
condition that the transpose direction \(C^T\) also lies in the identity
kernel; in particular this holds when the selected \(C\) is real symmetric
or purely imaginary skew-symmetric.  No such transpose invariance has been
proved universally.

## 7. A one-leg reflection-frame corollary

There is a separate exact parity theorem inside the canonical Schmidt
branch.

> **Proposition.**  Suppose that, on either leg of a Hermitian Schmidt
> decomposition of an exceptional rank-four \(H\), the four orthogonal
> Schmidt vectors are proportional to traceless Hermitian involutions
> \(U_1,\ldots,U_4\), and every pair \(U_i,U_j\) either commutes or
> anticommutes.  Then \(4\mid d\).

To prove it, suppose \(d=2s\) with \(s\) odd.  Two commuting balanced
reflections are simultaneously diagonalizable.  If
\(n_{++}\) is their common \(+1\) multiplicity, then

\[
\operatorname{Tr}(U_iU_j)=4n_{++}-2s\equiv2\pmod4,
\tag{44}
\]

contradicting Hilbert--Schmidt orthogonality.  Hence all six pairs
anticommute.  Four pairwise anticommuting complex reflections generate a
copy of \(M_4(\mathbb C)\), so \(4\mid d\), a contradiction.

This proposition needs only one canonical leg and is therefore distinct
from the two-leg four-product Clifford-frame theorem C61.  Pairwise
commute-or-anticommute is essential: Section 9 gives four exact orthogonal
balanced reflections in \(d=6\) for which that dichotomy fails.

## 8. Exact rank calibrations

The verifier computes both the ranks for individual inputs and the stacked
rank on the full operator system.  The latter is the invariant used in the
theorem.

| exact model | OSR | individual ranks on a support basis | stacked rank on support only | stacked rank on \(\mathbb CI+\) support |
|---|---:|---|---:|---:|
| published \(d=4\) exceptional witness, right on left | 3 | \(7,7,4\) | \(9\) | \(9\) |
| published witness, left on right | 3 | \(7,7,4\) | \(9\) | \(9\) |
| C61 \(d=4\) Clifford calibration, either direction | 4 | \(7,7,7,7\) | \(14\) | \(16\) |
| \(d=6\) color involution below, either direction | 4 | \(4,4,4,4\) | \(4\) | \(8\) |
| \(d=6\) controlled calibration, right on left | 4 | \(16,14,14,16\) | \(16\) | \(16\) |
| \(d=6\) controlled calibration, left on right | 4 | \(15,15,12,11\) | \(16\) | \(16\) |

The published rank-three support already closes:

\[
\dim\operatorname{span}(\mathbb CI+\mathcal A+\mathcal A^2)
=\dim\operatorname{span}(\mathbb CI+\mathcal B+\mathcal B^2)=4.
\tag{45}
\]

For the C61 calibration these dimensions are \(11,11\); its stacked map
becomes injective only after the identity input from \(H^2=I\) is included.
This exactly illustrates why (24) materially strengthens the
cubic-only identity.

## 9. Exact lower-assumption models in \(d=6\)

### 9.1 A fully standard controlled reflection with full sandwich rank

Let

\[
X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
Y=\begin{pmatrix}0&-i\\i&0\end{pmatrix},\quad
Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\quad
D=\operatorname{diag}(1,1,-1),
\tag{46}
\]

and identify \(V=\mathbb C^2\otimes\mathbb C^3\).  Put

\[
W=X\otimes D,\quad X_0=X\otimes I_3,\quad
Y_0=Y\otimes I_3,\quad Z_0=Z\otimes I_3
\tag{47}
\]

and

\[
S=\frac1{17}
\begin{pmatrix}
-1&0&-12&0&0&-12\\
0&17&0&0&0&0\\
-12&0&9&0&0&-8\\
0&0&0&17&0&0\\
0&0&0&0&17&0\\
-12&0&-8&0&0&9
\end{pmatrix}.
\tag{48}
\]

The rational matrix \(S\) is orthogonal.  Let

\[
(B_0,B_1,B_2,B_3)
=S(W,X_0,Y_0,Z_0)S^T
\tag{49}
\]

and define the diagonal matrices

\[
\begin{aligned}
A_0&=\operatorname{diag}(1,-1,0,0,0,0),\\
A_1&=\operatorname{diag}(0,0,1,1,-1,-1),\\
A_2&=\operatorname{diag}(0,0,1,-1,1,-1),\\
A_3&=\operatorname{diag}(0,0,1,-1,-1,1).
\end{aligned}
\tag{50}
\]

Then

\[
H_{\mathrm{ctl}}
=A_0\otimes B_0+
\frac1{\sqrt3}\sum_{j=1}^3A_j\otimes B_j
\tag{51}
\]

is a Hermitian involution of operator-Schmidt rank four with

\[
\operatorname{Tr}H_{\mathrm{ctl}}=0,\qquad
\operatorname{Tr}_1H_{\mathrm{ctl}}
=\operatorname{Tr}_2H_{\mathrm{ctl}}=0.
\tag{52}
\]

Indeed, its six control blocks are \(B_0,-B_0\) and the four tetrahedral
Pauli reflections

\[
\frac{\pm B_1\pm B_2\pm B_3}{\sqrt3}
\tag{53}
\]

with sign patterns \(+++, +--, -+-, --+\).

Its exact Gram matrices are

\[
G_A=\operatorname{diag}(2,4,4,4),\qquad
G_B=
\begin{pmatrix}
6&2&0&0\\
2&6&0&0\\
0&0&6&0\\
0&0&0&6
\end{pmatrix}.
\tag{54}
\]

Both joint-sandwich maps in (5) have full rank \(16\).  Yet

\[
\dim\operatorname{span}(\mathbb CI+\mathcal A+\mathcal A^2)=6,
\qquad
\dim\operatorname{span}(\mathbb CI+\mathcal B+\mathcal B^2)=8,
\tag{55}
\]

so neither five-dimensional operator system is an algebra.  The theorem
therefore detects directly that (51) cannot satisfy the cubic.  This model
is important: Hermiticity, involutivity, full standardness, balance, and
OSR four do **not** force sandwich degeneracy in \(d=6\).  The cubic is the
essential input.

### 9.2 A noncontrolled color involution with highly degenerate sandwiches

Using the same \(D\), put

\[
C_1=X\otimes I_3,\quad C_2=Z\otimes I_3,\quad
C_3=X\otimes D,\quad C_4=Z\otimes D
\tag{56}
\]

and

\[
H_{\mathrm{col}}
=\frac12\left(
-C_1\otimes C_1+C_2\otimes C_2
+C_3\otimes C_3+C_4\otimes C_4\right).
\tag{57}
\]

On a pair of color sectors, (57) is \(Z\otimes Z\) when the two
\(D\)-signs agree and \(-X\otimes X\) when they differ.  Consequently

\[
H_{\mathrm{col}}^*=H_{\mathrm{col}},\quad
H_{\mathrm{col}}^2=I,\quad
\operatorname{Tr}_1H_{\mathrm{col}}
=\operatorname{Tr}_2H_{\mathrm{col}}=0,
\quad\operatorname{OSR}(H_{\mathrm{col}})=4.
\tag{58}
\]

Both leg coefficient algebras are

\[
M_2(\mathbb C)\otimes\operatorname{span}\{I_3,D\},
\tag{59}
\]

whose commutants have only even-rank projections.  Thus no odd-rank
commutant argument follows from the two-site data.  The joint-sandwich
ranks are only \(8\), with eight-dimensional common kernels.

This reflection deliberately fails the cubic.  There are \(15\) color
triples for which the two adjacent Pauli types agree and \(12\) for which
they differ.  The two exact residual norms per color triple are
\(256/9\) and \(64/9\), respectively, so

\[
\|\operatorname{Cub}(H_{\mathrm{col}})\|_{\mathrm{HS}}^2
=15\frac{256}{9}+12\frac{64}{9}=512.
\tag{60}
\]

Its canonical Schmidt singular values are

\[
\{4,\,2,\,2\sqrt2,\,2\sqrt2\}.
\tag{61}
\]

The nondegenerate singular directions for \(4\) and \(2\) are supported
on the rank-two and rank-one color projections, respectively, and are
singular.  Thus a nonorthogonal factorization by local involutions does
not imply that the canonical Hermitian Schmidt factors are involutions.

### 9.3 Four orthogonal balanced reflections do not force Clifford form

Let

\[
U_1=X\otimes I_3,\quad U_2=Y\otimes I_3,\quad U_3=Z\otimes I_3.
\tag{62}
\]

For \(k\in\mathbb Z/3\mathbb Z\), put

\[
\psi_k=\frac{|0,k\rangle+|1,k+1\rangle}{\sqrt2},\qquad
Q=\sum_{k=0}^2|\psi_k\rangle\langle\psi_k|,
\quad U_4=I-2Q.
\tag{63}
\]

The four \(U_i\) are traceless Hermitian involutions and are mutually
Hilbert--Schmidt orthogonal.  However, \(U_4\) neither commutes nor
anticommutes with all of \(U_1,U_2,U_3\).  Hence the
commute-or-anticommute hypothesis in Section 7 cannot be deleted on the
basis of local reflection geometry alone.

## 10. What is proved, and what remains open

This audit proves a universal algebraic restriction on every exceptional
OSR-four solution:

\[
d\equiv2\pmod4
\quad\Longrightarrow\quad
\text{two nonzero all-input elementary-operator annihilators.}
\tag{64}
\]

It also replaces several tempting but false shortcuts:

- \(H^2=I\), standardness, and OSR four do not force an odd-rank leg
  projection;
- a nonorthogonal involutory factorization does not force involutory
  canonical Schmidt factors;
- four orthogonal balanced local reflections in \(d=6\) need not form a
  commute-or-anticommute frame;
- singularity for each individual sandwich input is weaker than the
  common-kernel condition actually forced by the equations.

The unresolved step is to classify pairs of four-dimensional
\(*\)-closed traceless supports satisfying (14)--(15), (27)--(28), and
the two common-kernel conditions in (7).  A complete OSR-four
divisibility theorem would follow if those conditions forced either
five-dimensional support closure, a rank-one true leg projection, or a
canonical four-generator Clifford module.

## 11. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_osr4_joint_sandwich_degeneracy.py
```

The verifier uses exact SymPy arithmetic.  It checks:

1. the finite-dimensional \(C^*\)-algebra dimension-five alternatives;
2. all sandwich ranks in Section 8, including the identity input;
3. the full exact \(d=6\) controlled reflection and a nonzero exact cubic
   residual block;
4. the color involution, its Gram data, canonical Schmidt spectrum, and
   residual norm \(512\);
5. the four-reflection limitation model in (62)--(63).

The verifier checks the finite models and coefficient ranks; the
all-dimension quotient argument and \(C^*\)-algebra proof are
human-readable arguments in Sections 4--5.
