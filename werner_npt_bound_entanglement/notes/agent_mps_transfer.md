# Exact transfer matrices for rank-two qutrit MPS codes

Checkpoint: 2026-07-28 15:38 PDT.

This note develops an exact transfer-matrix search for a negative endpoint
functional
\[
 Q_n(P)=\langle P,{\cal L}^{\otimes n}(P)\rangle,
 \qquad
 {\cal L}(X)=X-\frac12\operatorname{Tr}(X)I_3,
 \tag{1}
\]
where \(P\) is a rank-two projection on
\((\mathbb C^3)^{\otimes n}\).  No negative MPS code was found.  The exact
outcomes are:

1. a \(D^4\)-dimensional transfer formula which includes the logical Gram
   correction and therefore evaluates the orthogonal projection, not an
   unnormalized pair of MPS vectors;
2. a finite exact recurrence of order at most \(D^8\) for the numerator;
3. all-\(n\) no-go theorems for tensors of physical rank at most two,
   every commuting bond-two tensor, and orthogonal diagonal bond-three
   tensors;
4. an exact equality family used to validate the implementation;
5. extensive, but non-probative, searches over real and complex rational
   tensors of bond dimensions two and three.

The MPS search therefore did not produce an Alternative-B witness.

## 1. Open-boundary rank-two MPS code

Fix matrices
\[
 A^0,A^1,A^2\in M_D(\mathbb C),
 \]
a left boundary \(\ell\in\mathbb C^D\), and a boundary map
\[
 R:\mathbb C^2\longrightarrow\mathbb C^D,\qquad
 R|a\rangle=r_a,\quad a=0,1.
 \]
Define \(V_n:\mathbb C^2\to(\mathbb C^3)^{\otimes n}\) by
\[
 V_n|a\rangle
 =
 \sum_{s_1,\ldots,s_n=0}^2
 \ell^\dagger A^{s_1}\cdots A^{s_n}r_a\,
 |s_1\cdots s_n\rangle .
 \tag{2}
\]
Assume that \(V_n\) has rank two.  Its logical Gram matrix is
\[
 G_n=V_n^\dagger V_n\succ0.
 \tag{3}
\]
Thus
\[
 U_n=V_nG_n^{-1/2}
 \tag{4}
\]
has two exactly orthonormal columns, and the code projection is
\[
 P_n=U_nU_n^\dagger
     =V_nG_n^{-1}V_n^\dagger.
 \tag{5}
\]
Formula (5) is preferable in exact arithmetic: no algebraic matrix square
root has to be chosen.

## 2. Exact two-layer and four-layer transfers

Use the tensor-product vectorization convention displayed explicitly
below, so no choice between row and column vectorization is hidden.  Put
\[
 {\mathbb E}
 =
 \sum_{s=0}^2 A^s\otimes\overline{A^s}
 \quad\text{on }\mathbb C^D\otimes\overline{\mathbb C^D}.
 \tag{6}
\]

### Proposition 1 (Gram transfer)

The logical Gram entries are
\[
 \boxed{
 (G_n)_{ab}
 =
 (\ell^\dagger\otimes\ell^T)
 {\mathbb E}^{\,n}
 (r_b\otimes\overline{r_a}).}
 \tag{7}
\]

#### Proof

Expand the two MPS amplitudes:
\[
 \begin{aligned}
 \langle V_n a|V_n b\rangle
 &=
 \sum_{s_1,\ldots,s_n}
 \overline{\ell^\dagger A^{s_1}\cdots A^{s_n}r_a}\,
 \ell^\dagger A^{s_1}\cdots A^{s_n}r_b\\
 &=
 (\ell^\dagger\otimes\ell^T)
 \left(\sum_sA^s\otimes\overline{A^s}\right)^n
 (r_b\otimes\overline{r_a}).
 \end{aligned}
 \]
This is (7). \(\square\)

For one qutrit, the matrix-unit kernel of \({\cal L}\) is
\[
 \begin{aligned}
 k(s,t;u,v)
 &:=
 \operatorname{Tr}\left[
 |s\rangle\langle t|\,
 {\cal L}(|u\rangle\langle v|)\right]\\
 &=\delta_{t,u}\delta_{v,s}
   -\frac12\delta_{s,t}\delta_{u,v}.
 \end{aligned}
 \tag{8}
\]
Define the four-layer transfer
\[
 \boxed{
 {\mathbb T}
 =
 \sum_{s,t=0}^2
 A^s\otimes\overline{A^t}\otimes
 A^t\otimes\overline{A^s}
 -\frac12{\mathbb E}\otimes{\mathbb E}.}
 \tag{9}
\]
It acts on a space of dimension \(D^4\).  The first term in (9) is the
first Kronecker delta in (8), and the second term is the trace term.

Put
\[
 b_n
 =
 \sum_{a,b=0}^1
 (G_n^{-1})_{ab}\,
 r_a\otimes\overline{r_b}
 \in\mathbb C^D\otimes\overline{\mathbb C^D},
 \tag{10}
\]
\[
 \Lambda_4
 =
 (\ell^\dagger\otimes\ell^T)
 \otimes
 (\ell^\dagger\otimes\ell^T).
 \tag{11}
\]

### Proposition 2 (exact endpoint transfer)

\[
 \boxed{
 Q_n(P_n)
 =
 \Lambda_4\,{\mathbb T}^{\,n}(b_n\otimes b_n).}
 \tag{12}
\]

#### Proof

From (5),
\[
 P_n
 =
 \sum_{a,b}
 (G_n^{-1})_{ab}
 |V_na\rangle\langle V_nb|.
 \tag{13}
\]
Insert two copies of (13) into
\(\operatorname{Tr}[P_n{\cal L}^{\otimes n}(P_n)]\).  At every physical
site the four physical indices contract by (8), which produces (9).
The left and right boundary contractions are precisely (11) and two
copies of (10). \(\square\)

Equations (6)--(12) are valid for arbitrary complex tensors.  If all input
data are rational, Gaussian-rational, or algebraic, then every entry in
(12) is in the same exact number field.

### Direct validation

For random complex \(D=2\) tensors, (12) was compared at
\(n=1,2,3\) with explicit construction of the dense \(3^n\times3^n\)
projection followed by direct application of \({\cal L}^{\otimes n}\).
The two calculations agreed to \(3\cdot10^{-16}\).  This check caught the
otherwise easy mistakes of omitting \(G_n^{-1}\) or reversing its two
logical indices.

## 3. A finite exact recurrence for the sign

The dependence of \(b_n\) on \(n\) does not prevent a finite transfer
certificate.  Since the logical dimension is two,
\[
 G_n^{-1}=\frac{\operatorname{adj}G_n}{\det G_n},
 \tag{14}
\]
and \(\operatorname{adj}G_n\) is linear in the four entries of \(G_n\).
Define
\[
 \widetilde b_n=(\det G_n)b_n.
 \tag{15}
\]
Then
\[
 Q_n(P_n)=\frac{N_n}{(\det G_n)^2},
 \qquad
 N_n=\Lambda_4{\mathbb T}^{\,n}
       (\widetilde b_n\otimes\widetilde b_n).
 \tag{16}
\]
The denominator is strictly positive.

### Proposition 3 (finite recurrence)

The sequence \(N_n\) is a matrix coefficient of a fixed matrix obtained
from
\[
 {\mathbb T}\otimes{\mathbb E}\otimes{\mathbb E},
 \tag{17}
\]
after fixed permutations and boundary contractions.  In particular,
\(N_n\) obeys a constant-coefficient linear recurrence of order at most
\[
 D^4D^2D^2=D^8.
 \tag{18}
\]

#### Proof

By (7), every entry of \(G_n\) is a fixed matrix coefficient of
\({\mathbb E}^n\).  Because the adjugate of a \(2\times2\) matrix is
linear in its entries, (15) has the form
\[
 \widetilde b_n=J({\mathbb E}^nx_0)
 \tag{19}
\]
for a fixed linear map \(J\) and fixed boundary vector \(x_0\); the
logical index reversal in (7) is absorbed into \(J\).  Substituting (19)
in (16), expanding the three tensor factors, and collecting the fixed
contraction gives a matrix coefficient of (17) to the \(n\)-th power.
Cayley--Hamilton proves the recurrence bound (18). \(\square\)

This supplies an exact architecture for an eventual-sign proof.  For
example, if the contributing eigenvalue of largest modulus of the
matrix in (17) is a simple positive algebraic number with positive
coefficient, exact root separation gives \(N_n>0\) for every sufficiently
large \(n\); a finite exact check handles the remaining values.  A simple
negative dominant eigenvalue with nonzero coefficient would instead give
negative values on one parity of \(n\).  No tensor with the latter
behavior was found.

## 4. Common-local-support lemma

The following elementary observation eliminates several large MPS
subclasses.

### Lemma 4

Suppose a rank-two projection \(P\) is supported in
\[
 S_1\otimes\cdots\otimes S_n,\qquad \dim S_i\le2.
 \tag{20}
\]
Then
\[
 Q_n(P)\ge0.
 \tag{21}
\]

#### Proof

Let \(C_i\) project onto \(S_i\).  On a two-dimensional support,
\[
 C_i{\cal L}(X)C_i
 =
 X-\frac12\operatorname{Tr}(X)I_{S_i},
 \]
which is the Hilbert--Schmidt orthogonal projection onto the traceless
operators on \(S_i\).  On a one-dimensional support the compressed map is
multiplication by \(1/2\).  Each compressed local superoperator is
positive semidefinite for the Hilbert--Schmidt inner product, and so is
their tensor product.  Since \(P\) is supported in (20), (21) follows.
\(\square\)

## 5. Exact MPS no-go subclasses

### 5.1 Physical tensor rank at most two

Call
\[
 \dim\operatorname{span}\{A^0,A^1,A^2\}
 \tag{22}
\]
the physical rank of the tensor.

### Proposition 5

If the physical rank is at most two, then every code (2) satisfies
\[
 Q_n(P_n)\ge0
 \quad\text{for every \(n\) for which \(V_n\) has rank two.}
 \tag{23}
\]

#### Proof

There is a nonzero linear relation among the three matrices.  Extend its
normalized coefficient vector to a unitary change of physical basis.
In the new basis one tensor matrix, say \(A^2\), is zero.  Hence every MPS
amplitude containing the physical symbol \(2\) vanishes, and
\[
 \operatorname{ran}P_n
 \subseteq
 \operatorname{span}\{|0\rangle,|1\rangle\}^{\otimes n}.
 \]
Lemma 4 proves (23). \(\square\)

This test is important in computer searches: many sparse tensors that
appear nontrivial are merely physical-rank-two equality codes.

### 5.2 Every commuting bond-two tensor

### Proposition 6

Let \(D=2\).  If \(A^0,A^1,A^2\) commute pairwise, then every code (2)
obeys
\[
 Q_n(P_n)\ge0
 \tag{24}
\]
for all admissible \(n\).

#### Proof

If one of the commuting matrices has two distinct eigenvalues, its two
eigenspaces are preserved by every other matrix.  Thus all three matrices
are simultaneously diagonal:
\[
 A^s=\begin{pmatrix}x_s&0\\0&y_s\end{pmatrix}.
 \]
Every boundary MPS is then a linear combination of
\[
 |x\rangle^{\otimes n},\qquad |y\rangle^{\otimes n},
 \quad
 |x\rangle=\sum_sx_s|s\rangle,\quad
 |y\rangle=\sum_sy_s|s\rangle.
 \]
It is therefore supported in
\(\operatorname{span}\{|x\rangle,|y\rangle\}^{\otimes n}\).

It remains to consider the case in which every nonscalar member has only
one eigenvalue.  Choose one nonscalar member.  In a common basis it is
\(aI+bN\), where \(b\ne0\) and \(N^2=0\).  Its commutant in \(M_2\) is
\(\operatorname{span}\{I,N\}\), so
\[
 A^s=a_sI+b_sN
 \]
for all \(s\).  Expanding a product of these matrices and using \(N^2=0\)
shows that every physical tensor factor is drawn from the two local
vectors
\[
 |a\rangle=\sum_sa_s|s\rangle,\qquad
 |b\rangle=\sum_sb_s|s\rangle.
 \]
Thus the code is supported in
\(\operatorname{span}\{|a\rangle,|b\rangle\}^{\otimes n}\).
Lemma 4 finishes both cases. \(\square\)

This rules out the whole commuting \(D=2\) ansatz, including defective
Jordan tensors, rather than only simultaneously unitarily diagonalizable
ones.

### 5.3 Orthogonal diagonal bond-three tensors

Commuting \(D=3\) tensors are genuinely different: three local product
vectors can span the full qutrit.  There is nevertheless an exact no-go
when those vectors are orthogonal.

### Proposition 7

Let \(e_0,e_1,e_2\in\mathbb C^3\) be orthonormal and put
\[
 {\cal R}_n
 =
 \operatorname{span}\{
 e_0^{\otimes n},e_1^{\otimes n},e_2^{\otimes n}\}.
 \tag{25}
\]
For every rank-two projection \(P\) with range contained in
\({\cal R}_n\),
\[
 Q_n(P)\ge0.
 \tag{26}
\]
Consequently every diagonal bond-three MPS whose three local eigenvalue
vectors are mutually orthogonal is endpoint-undistillable within this
rank-two boundary ansatz.

#### Proof

Write the \(3\times3\) matrix of \(P\) in the orthonormal repetition basis
\(e_j^{\otimes n}\), and set
\[
 D_0=\sum_{j=0}^2P_{jj}^2.
 \tag{27}
\]
For local matrix units in the \(e_j\) basis, (8) shows that the only
nonzero contractions are:

- \(k(j,k;k,j)=1\) when \(j\ne k\);
- \(k(j,j;j,j)=1/2\);
- \(k(j,j;k,k)=-1/2\) when \(j\ne k\).

Therefore
\[
 Q_n(P)
 =
 \sum_{j\ne k}|P_{jk}|^2
 +2^{-n}\sum_jP_{jj}^2
 +(-2)^{-n}\sum_{j\ne k}P_{jj}P_{kk}.
 \tag{28}
\]
Since \(P\) is a rank-two projection,
\[
 \sum_{j\ne k}|P_{jk}|^2=2-D_0,\qquad
 \sum_{j\ne k}P_{jj}P_{kk}=4-D_0.
 \]
Hence
\[
 Q_n(P)
 =
 2-D_0+2^{-n}\left[D_0+(-1)^n(4-D_0)\right].
 \tag{29}
\]
The diagonal entries of a projection lie in \([0,1]\), and
\(\sum_jP_{jj}=2\), so \(D_0\le2\).  For odd \(n\),
\[
 Q_n(P)=(2-D_0)(1-2^{1-n})\ge0.
 \tag{30}
\]
For even \(n\),
\[
 Q_n(P)=2-D_0+2^{2-n}>0.
 \tag{31}
\]
This proves the claim. \(\square\)

For odd \(n\ge3\), equality in (30) requires \(D_0=2\).  Then all
off-diagonal entries vanish, so \(P\) is one of the three coordinate
two-planes.  Formula (29) therefore also classifies equality in this
subclass.

## 6. An exact equality tensor and transfer spectrum

The following integer \(D=2\) tensor was found repeatedly by numerical
descent:
\[
 A^0=\begin{pmatrix}2&1\\2&2\end{pmatrix},\qquad
 A^1=\begin{pmatrix}-1&1\\2&-1\end{pmatrix},\qquad
 A^2=\begin{pmatrix}-1&-1\\-2&-1\end{pmatrix},
 \qquad
 \ell=\binom12,\qquad R=I_2.
 \tag{32}
\]
The three matrices commute and satisfy
\[
 A^2=I-A^0,\qquad A^1=A^0-3I.
 \tag{33}
\]
Their two common eigenvalue vectors in the physical qutrit are
\[
 x_+=
 (2+\sqrt2,-1+\sqrt2,-1-\sqrt2),
 \]
\[
 x_-=
 (2-\sqrt2,-1-\sqrt2,-1+\sqrt2).
 \tag{34}
\]
They are orthogonal.  Thus the code range is the span of the two
orthogonal product powers \(x_+^{\otimes n},x_-^{\otimes n}\), and
\[
 \boxed{
 Q_n(P_n)=2^{1-n}(1+(-1)^n).}
 \tag{35}
\]
In particular, every odd length is an exact equality code.

The exact transfer characteristic polynomials are
\[
 \chi_{\mathbb E}(\lambda)
 =
 \lambda^2(\lambda^2-24\lambda+112),
 \tag{36}
\]
\[
 \chi_{\mathbb T}(\lambda)
 =
 \lambda^{10}(\lambda-112)^2(\lambda+56)^2
 (\lambda^2-176\lambda+3136).
 \tag{37}
\]
Equations (35)--(37) provide a simple exact regression test for any
implementation of (7) and (12).

## 7. A scalar commuting-\(D=3\) laboratory

For a diagonal \(D=3\) tensor, let \(x_0,x_1,x_2\in\mathbb C^3\) be its
three local eigenvalue vectors and let
\[
 C_{ij}=\langle x_i,x_j\rangle.
 \tag{38}
\]
If a \(3\times2\) coefficient matrix \(W\) specifies the boundary plane,
then
\[
 G_n=W^\dagger C^{\circ n}W,
 \qquad
 M_n=W G_n^{-1}W^\dagger,
 \tag{39}
\]
where \(C^{\circ n}\) is the entrywise power.  Define
\[
 K_{ij;kl}
 =
 C_{jk}C_{li}-\frac12C_{ji}C_{lk}.
 \tag{40}
\]
The full \(D^4=81\) transfer reduces to the scalar sum
\[
 \boxed{
 Q_n
 =
 \sum_{i,j,k,l=0}^2
 (M_n)_{ij}(M_n)_{kl}K_{ij;kl}^{\,n}.}
 \tag{41}
\]
This is the most efficient exact search space found in this investigation.

As one symmetric algebraic subfamily, take unit vectors with common real
overlap
\[
 \langle x_i,x_j\rangle=t\quad(i\ne j),
 \qquad -\frac12\le t<1,
 \]
and take \(W\) to span the coefficient plane orthogonal to
\((1,1,1)\).  Then \(M_n=(I-J/3)/(1-t^n)\), and direct enumeration in
(41) gives
\[
 \begin{aligned}
 Q_n=\frac1{(1-t^n)^2}\bigg[&
 \frac43\left(\frac12\right)^n
 -\frac{16}3\left(\frac t2\right)^n
 +\frac83\left(t^2-\frac12\right)^n\\
 &-\frac83\left(\frac{t(2t-1)}2\right)^n
 +2\left(\frac{t^2}2\right)^n
 +\frac23\left(1-\frac{t^2}2\right)^n\\
 &+\frac43\left(\frac{t(2-t)}2\right)^n
 \bigg].
 \end{aligned}
 \tag{42}
\]
This formula is exact and involves only seven scalar transfer eigenvalues.
Dense high-precision scans through \(n=200\) found no negative value, but
an all-\(n\) proof of (42) was not obtained.  Thus (42) is a tractable
remaining analytic subproblem, not evidence for an all-copy theorem.

## 8. Discovery search and exact screening

All results in this section are discovery evidence only.

### 8.1 Search ranges

- \(100{,}000\) real \(D=2\) integer tensors with entries in
  \(\{-2,-1,0,1,2\}\), several integer left boundaries, and lengths
  \(5,10,20,40,80\);
- \(50{,}000\) complex \(D=2\) Gaussian-integer tensors with real and
  imaginary parts in \(\{-1,0,1\}\), three complex boundaries, and
  lengths through \(50\);
- \(5{,}000\) real \(D=3\) integer tensors with fixed boundary planes,
  followed by \(20{,}000\) tensors with random real left boundaries and
  random logical two-planes;
- \(5{,}000\) complex \(D=3\) Gaussian-integer tensors with random complex
  boundaries and lengths \(5,10,20,30\);
- \(100{,}000\) normalized real diagonal-\(D=3\) product triples with
  random coefficient planes, evaluated by (41);
- \(20{,}000\) weighted Pauli tensors
  \(A^0=aI,A^1=bX,A^2=cZ\) over a logarithmic parameter range.

No nonzero negative value survived conditioning checks.  Typical positive
values decay exponentially with \(n\), so ordinary double precision is a
poor sign oracle at large length.

### 8.2 A false floating-point negative

For
\[
 A^0=\begin{pmatrix}1&1\\1&1\end{pmatrix},\quad
 A^1=\begin{pmatrix}0&-1\\0&1\end{pmatrix},\quad
 A^2=-A^1,\quad
 \ell=\binom10,
 \tag{43}
\]
double precision reported
\[
 Q_{27}\approx-1.19\cdot10^{-7}
 \]
when the logical Gram condition number was about \(2.7\cdot10^8\).
Exact rational transfer evaluation instead gives
\[
 Q_{27}
 =
 \frac{39531596699314859}
 {302231450400057683083264}
 >0.
 \tag{44}
\]
The negative value was entirely caused by inversion of the ill-conditioned
Gram matrix.  This example justifies the rule used throughout the search:
every negative or near-zero candidate must be recomputed from (7) and
(12) in exact arithmetic before it is retained.

## 9. What the MPS program did and did not establish

Established exactly:

1. the Gram-corrected transfer formula (12);
2. the finite recurrence/spectral certificate (16)--(18);
3. the physical-rank-two, commuting-\(D=2\), and orthogonal
   diagonal-\(D=3\) no-go theorems;
4. the exact equality family (32)--(37);
5. the scalar diagonal-\(D=3\) formula (41), including the seven-eigenvalue
   symmetric specialization (42).

Not established:

- a negative rank-two qutrit MPS code;
- nonnegativity for general noncommuting \(D=2\) tensors;
- nonnegativity for general commuting or noncommuting \(D=3\) tensors;
- an eventual-sign theorem without checking the exact contributing
  spectrum in (17);
- either Alternative A or Alternative B.

The most promising continuation inside this ansatz is exact analysis of
the scalar product-state-plane formula (41), beginning with (42), or an
algebraic search which targets a negative dominant contribution in the
combined transfer (17) rather than minimizing very small floating-point
values of \(Q_n\) directly.
