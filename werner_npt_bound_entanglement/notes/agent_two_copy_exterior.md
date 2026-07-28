# Two-copy \(d=3\) Ky--Fan inequality via exterior/Hodge structure

Scope: independent first-principles attack on the full \(d=3,n=2\)
endpoint inequality, including simultaneous nonnormal matrices. No external
sources or prior artifacts are used.

## Research log

- **2026-07-28 09:42 PDT.** Began by deriving the exact Ky--Fan dual
  formulation from the rank-two coefficient-matrix inequality. The intended
  normalization is recorded below; it will be adjusted if the parent task
  uses a different convention.
- **2026-07-28 10:12 PDT.** Derived the exterior variational formula, Hodge
  routing, and exact scalar elimination. Proved (KF) whenever either \(A\)
  or \(B\) is normal, with the other matrix arbitrary. The proof uses two
  sharp trace-zero block lemmas and includes the scalar \(c\). Thus the
  remaining case is genuinely simultaneous nonnormality.
- **2026-07-28 10:40 PDT.** Found a positive-dimensional exact equality
  family with both matrices rank-two and nonnormal. Proved a quadratic
  identity for the arbitrary traceless \(2\times2\) Kronecker-sum core,
  which settles all \(A=A_2\oplus0,B=B_2\oplus0,c=0\). Exact symbolic
  checks agree with the hand derivations. No counterexample was found; the
  genuinely three-dimensional simultaneous-nonnormal case remains open in
  this notebook.

## 1. Exact dual formulation

For \(C\in M_3\otimes M_3=M_9\), the two-copy endpoint form is
\[
Q_2(C)=\|C\|_2^2-\frac12\|\operatorname{Tr}_1C\|_2^2
       -\frac12\|\operatorname{Tr}_2C\|_2^2
       +\frac14|\operatorname{Tr}C|^2. \tag{1}
\]
Writing
\[
A_C=\operatorname{Tr}_1C-\frac{\operatorname{Tr}C}{3}I_3,\qquad
B_C=\operatorname{Tr}_2C-\frac{\operatorname{Tr}C}{3}I_3,
\]
orthogonality of scalar and traceless matrices gives
\[
Q_2(C)=\|C\|_2^2-\frac12\|A_C\|_2^2
                    -\frac12\|B_C\|_2^2
                    -\frac1{12}|\operatorname{Tr}C|^2. \tag{2}
\]
Define
\[
\mathcal T(C)=
\left(\frac{A_C}{\sqrt2},\frac{B_C}{\sqrt2},
\frac{\operatorname{Tr}C}{\sqrt{12}}\right).
\]
For traceless \(A,B\in M_3\) and \(c\in\mathbb C\), the adjoint image is,
after rescaling the dual variables,
\[
D(A,B,c)=I_3\otimes A+B\otimes I_3+cI_9. \tag{3}
\]
The corresponding squared dual norm is
\[
N(A,B,c)=2\|A\|_2^2+2\|B\|_2^2+12|c|^2. \tag{4}
\]
Consequently the desired two-copy statement is equivalent to
\[
\boxed{\qquad
s_1(D)^2+s_2(D)^2\le
2\|A\|_2^2+2\|B\|_2^2+12|c|^2,
\qquad \operatorname{Tr}A=\operatorname{Tr}B=0.
\qquad} \tag{KF}
\]
Here \(s_1\ge s_2\) are the two largest singular values.

Indeed, for every \(D\),
\[
\sup_{\substack{\operatorname{rank}C\le2\\\|C\|_2=1}}
|\langle C,D\rangle_{\rm HS}|^2=s_1(D)^2+s_2(D)^2. \tag{5}
\]
Dualizing \(\|\mathcal T(C)\|^2\le\|C\|^2\) over its output space proves
the equivalence in both directions.

## 2. Exterior-square variational form

Let \(V=\mathbb C^3\otimes\mathbb C^3\). Identify a two-form with a
skew-symmetric \(9\times9\) coefficient matrix
\[
Z^T=-Z.
\]
For an arbitrary \(9\times9\) matrix \(D\),
\[
\boxed{\quad
\sup_{0\ne Z^T=-Z}\frac{\|DZ\|_2^2}{\|Z\|_2^2}
=\frac{s_1(D)^2+s_2(D)^2}{2}.
\quad} \tag{6}
\]

### Proof

Diagonalize \(D^\dagger D\), with eigenvalues
\(\lambda_1\ge\cdots\ge\lambda_9\). In that eigenbasis,
\[
\|Z\|_2^2=2\sum_{i<j}|Z_{ij}|^2,\qquad
\|DZ\|_2^2=\sum_{i<j}(\lambda_i+\lambda_j)|Z_{ij}|^2.
\]
The quotient is maximized by the decomposable form supported on indices
\(1,2\), and its value is \((\lambda_1+\lambda_2)/2\).

It follows that (KF) is equivalent to the pointwise exterior inequality
\[
\boxed{\quad
\|(I\otimes A+B\otimes I+cI)Z\|_2^2
\le\bigl(\|A\|_2^2+\|B\|_2^2+6|c|^2\bigr)\|Z\|_2^2
\quad} \tag{7}
\]
for every skew \(Z\). Although (6) shows it is enough to test decomposable
\(Z=x\wedge y\), a sum-of-squares proof of (7) on the full exterior space
would be equivalent and potentially cleaner.

## 3. The Hodge splitting

Write the entries of \(Z\) as \(Z_{i\alpha,k\beta}\), where Latin indices
belong to the first \(\mathbb C^3\) and Greek indices to the second. Set
\[
\begin{aligned}
P_{i\alpha,k\beta}
 &=\frac12\left(Z_{i\alpha,k\beta}
                 +Z_{k\alpha,i\beta}\right),\\
R_{i\alpha,k\beta}
 &=\frac12\left(Z_{i\alpha,k\beta}
                 -Z_{k\alpha,i\beta}\right).
\end{aligned} \tag{8}
\]
Using \(Z_{k\beta,i\alpha}=-Z_{i\alpha,k\beta}\), the first tensor is
symmetric in \(i,k\) and antisymmetric in \(\alpha,\beta\), while the
second is antisymmetric in \(i,k\) and symmetric in \(\alpha,\beta\).
They are orthogonal and give
\[
\Lambda^2(U\otimes W)
=\bigl(\operatorname{Sym}^2U\otimes\Lambda^2W\bigr)
\oplus
\bigl(\Lambda^2U\otimes\operatorname{Sym}^2W\bigr). \tag{9}
\]

For a traceless \(3\times3\) matrix \(A\), its induced derivation on
\(\Lambda^2\mathbb C^3\) becomes especially simple. Under the Hodge map
\[
\star(e_i\wedge e_j)=\sum_k\epsilon_{ijk}e_k^*,
\]
one has
\[
\star\,(A\otimes I+I\otimes A)|_{\Lambda^2}\,\star^{-1}
=(\operatorname{Tr}A)I-A^T=-A^T. \tag{10}
\]
Thus the skew-preserving part of left multiplication by \(I\otimes A\)
acts on the \(P\)-summand through \(-A^T/2\), while its action on the
\(R\)-summand is half the symmetric-square derivation. The
skew-to-symmetric part lands respectively in
\(\operatorname{Sym}^2U\otimes\operatorname{Sym}^2W\) and
\(\Lambda^2U\otimes\Lambda^2W\). The corresponding statements with
\(A,W\) replaced by \(B,U\) interchange the two roles.

This produces four mutually orthogonal output sectors:
\[
\begin{array}{c|c}
\text{output sector}&\text{contributing input/action pieces}\\ \hline
\operatorname{Sym}^2U\otimes\Lambda^2W
  &B_{\rm sym}P+A_{\wedge}P+cP\\
\Lambda^2U\otimes\operatorname{Sym}^2W
  &B_{\wedge}R+A_{\rm sym}R+cR\\
\operatorname{Sym}^2U\otimes\operatorname{Sym}^2W
  &A_{\rm cross}P+B_{\rm cross}R\\
\Lambda^2U\otimes\Lambda^2W
  &B_{\rm cross}P+A_{\rm cross}R.
\end{array} \tag{11}
\]
Equation (11) is an exact routing rule. The unresolved step is to combine
the four sector norms into the right side of (7) without separately
bounding the nonnormal symmetric-square actions too crudely.

## 4. Elimination of the scalar

Normalize \(\|Z\|_2=1\), put
\[
K=I\otimes A+B\otimes I,\qquad
S=\|A\|_2^2+\|B\|_2^2,
\]
and define
\[
t=\langle Z,KZ\rangle,\qquad
\Delta=S-\|KZ\|_2^2. \tag{12}
\]
Expanding (7) and minimizing its deficit over \(c\in\mathbb C\) gives the
exact equivalence
\[
\boxed{\qquad
\text{(7) for every \(c\)}
\quad\Longleftrightarrow\quad
\Delta\ge\frac{|t|^2}{5}.
\qquad} \tag{13}
\]
Indeed the deficit is
\[
\Delta-2\operatorname{Re}(\overline c\,t)+5|c|^2,
\]
whose minimum is \(\Delta-|t|^2/5\).

For \(c=0\), write
\[
X=(I\otimes A)Z,\qquad Y=(B\otimes I)Z,
\]
and
\[
\delta_A=\|A\|_2^2-\|X\|_2^2,\qquad
\delta_B=\|B\|_2^2-\|Y\|_2^2. \tag{14}
\]
The sharp missing correlation estimate is
\[
|\langle X,Y\rangle|^2\ \stackrel{?}{\le}
\delta_A\delta_B. \tag{15}
\]
If (15) holds, then
\[
\|X+Y\|^2
\le S-(\sqrt{\delta_A}-\sqrt{\delta_B})^2\le S. \tag{16}
\]
Numerical probes, including simultaneous nonnormal matrices, support
(15), but no exact factorization has yet been obtained. The Hodge routing
(11) suggests that its two sides should be the inner product and squared
norms of complementary cross-sector tensors.

The scalar requires the quantitative strengthening (13), not merely
(16). Numerically, \(|t|^2/\Delta\) appears far below the allowed constant
\(5\), and it vanishes in the sharp nilpotent equality family below; this
observation is discovery evidence only.

## 5. Exact nonnormal equality family

Let
\[
A=a|0\rangle\langle1|,\qquad
B=b|0\rangle\langle1|,\qquad c=0.
\]
Both matrices are traceless and nonnormal. A direct invariant-subspace
calculation gives two largest singular values
\[
s_1(D)=s_2(D)=\sqrt{|a|^2+|b|^2}. \tag{17}
\]
For real nonnegative \(a,b\), the exact characteristic polynomial is
\[
\det(\lambda I-D^\dagger D)
=\lambda^5(\lambda-a^2)(\lambda-b^2)
(\lambda-a^2-b^2)^2
\]
and phases are removed by diagonal unitary conjugations.
Indeed, on the active \(2\times2\) tensor grid,
\[
|11\rangle\longmapsto
a|10\rangle+b|01\rangle,
\]
and the normalized vector proportional to
\(\overline b|10\rangle+\overline a|01\rangle\) maps to a vector of the
same norm in the \(|00\rangle\) direction. All remaining singular values
are at most \(\max(|a|,|b|)\). Therefore
\[
s_1(D)^2+s_2(D)^2
=2(|a|^2+|b|^2)
=2\|A\|_2^2+2\|B\|_2^2. \tag{18}
\]
This proves that (KF), if true, is sharp even for simultaneously
nonnormal \(A,B\). For \(a=b=1\), an exterior maximizer is generated by
\[
x=|11\rangle,\qquad
y=\frac{|10\rangle+|01\rangle}{\sqrt2},\qquad Z=x\wedge y.
\]
It has \(t=\langle Z,KZ\rangle=0\), and (15) is an equality:
\[
\|X\|^2=\|Y\|^2=\frac34,\qquad
\langle X,Y\rangle=\frac14,\qquad
\delta_A=\delta_B=\frac14. \tag{19}
\]

### A larger exact simultaneous-nonnormal equality family

The nilpotent example is contained in a four-parameter family. Let
\[
A=\begin{pmatrix}0&p&0\\q&0&0\\0&0&0\end{pmatrix},
\qquad
B=\begin{pmatrix}0&r&0\\s&0&0\\0&0&0\end{pmatrix},
\qquad pq=rs, \qquad c=0. \tag{19a}
\]
Put
\[
\Sigma=|p|^2+|q|^2+|r|^2+|s|^2.
\]
On the active tensor square
\(\operatorname{span}\{|00\rangle,|01\rangle,|10\rangle,|11\rangle\}\),
\(D\) interchanges the even and odd parity subspaces through the two
matrices
\[
\begin{pmatrix}q&r\\s&p\end{pmatrix},
\qquad
\begin{pmatrix}p&r\\s&q\end{pmatrix}. \tag{19b}
\]
Both determinants are \(pq-rs=0\), and both squared Frobenius norms are
\(\Sigma\). Hence each block has one singular value \(\sqrt\Sigma\) and
one zero singular value. The four remaining nonzero candidate singular
values, coming from tensor states with exactly one index equal to \(2\),
are \(|p|,|q|,|r|,|s|\), all at most \(\sqrt\Sigma\). Consequently
\[
s_1(D)=s_2(D)=\sqrt\Sigma,\qquad
s_1(D)^2+s_2(D)^2=2\Sigma
=2\|A\|^2+2\|B\|^2. \tag{19c}
\]
Equivalently,
\[
\det(\lambda I-D^\dagger D)
=\lambda^3(\lambda-\Sigma)^2
(\lambda-|p|^2)(\lambda-|q|^2)
(\lambda-|r|^2)(\lambda-|s|^2). \tag{19d}
\]
When \(|p|\ne|q|\) and \(|r|\ne|s|\), both \(A\) and \(B\) are nonnormal.
Thus the simultaneous-nonnormal equality set has positive dimension and
already includes rank-two matrices; it is not confined to the rank-one
nilpotent boundary.

## 6. Sharp \(3\times3\) trace-zero block lemmas

The following lemmas give a complete proof when one of \(A,B\) is normal.
They require no normality of the matrix called \(B\) below.

### Lemma 6.1: one vector

If \(\operatorname{Tr}B=0\), \(x\) is a unit vector, and
\(\alpha=\langle x,Bx\rangle\), then
\[
\|B\|_2^2-\|Bx\|^2\ge\frac12|\alpha|^2. \tag{20}
\]

#### Proof

Complete \(x\) to an orthonormal basis and write \(B\) in the corresponding
\(1+2\) block form. The squared norms of the last two columns sum to the
left side of (20). Their lower-right \(2\times2\) subblock has trace
\(-\alpha\), hence squared Frobenius norm at least
\(|\alpha|^2/2\).

### Lemma 6.2: two singular values in one shifted block

For every traceless \(B\in M_3\) and \(t\in\mathbb C\),
\[
\boxed{\quad
s_1(B+tI)^2+s_2(B+tI)^2
\le2\|B\|_2^2+\frac{12}{5}|t|^2.
\quad} \tag{21}
\]

#### Proof

Let \(x,y\) be orthonormal test vectors, let \(z\) span their orthogonal
complement, and put
\[
E_B=\|Bx\|^2+\|By\|^2,\qquad
\beta=\langle x,Bx\rangle+\langle y,By\rangle
      =-\langle z,Bz\rangle.
\]
Since \(\|B\|^2-E_B=\|Bz\|^2\ge|\beta|^2\), while Lemma 6.1 applied to
\(z\) gives
\(\|B\|^2-\|Bz\|^2\ge|\beta|^2/2\), one obtains
\[
2\|B\|^2-E_B\ge\frac52|\beta|^2. \tag{22}
\]
Therefore
\[
\begin{aligned}
&2\|B\|^2+\frac{12}{5}|t|^2
 -\bigl(\|(B+tI)x\|^2+\|(B+tI)y\|^2\bigr)\\
&\quad\ge
\frac52|\beta|^2-2\operatorname{Re}(\overline t\beta)
  \frac25|t|^2
=\frac52\left|\beta-\frac25t\right|^2\ge0.
\end{aligned} \tag{23}
\]
Maximizing over \(x,y\) proves (21).

### Lemma 6.3: largest singular values in two shifted blocks

For traceless \(B\), arbitrary \(t,u\in\mathbb C\), and arbitrary unit
vectors \(x,y\) (which need not be orthogonal),
\[
\begin{aligned}
\|(B+tI)x\|^2+\|(B+uI)y\|^2
\le{}&2\|B\|^2\\
&+\frac52(|t|^2+|u|^2)
 +\operatorname{Re}(\overline t u).
\end{aligned} \tag{24}
\]

#### Proof

Put \(\alpha=\langle x,Bx\rangle\) and
\(\beta=\langle y,By\rangle\). Applying Lemma 6.1 separately to \(x,y\)
gives
\[
2\|B\|^2-\|Bx\|^2-\|By\|^2
\ge\frac12(|\alpha|^2+|\beta|^2). \tag{25}
\]
Introduce the positive matrix
\[
M=\begin{pmatrix}5/2&1/2\\1/2&5/2\end{pmatrix},
\qquad
M^{-1}=
\begin{pmatrix}5/12&-1/12\\-1/12&5/12\end{pmatrix}. \tag{26}
\]
For \(v=(\alpha,\beta)^T\),
\[
v^\dagger M^{-1}v
=\frac5{12}(|\alpha|^2+|\beta|^2)
 -\frac16\operatorname{Re}(\overline\alpha\beta)
\le\frac12(|\alpha|^2+|\beta|^2), \tag{27}
\]
because the difference is \(|\alpha+\beta|^2/12\).
The matrix Cauchy inequality
\[
2\operatorname{Re}\left(
\overline t\alpha+\overline u\beta\right)
\le
\begin{pmatrix}t\\u\end{pmatrix}^{\!\dagger}
M\begin{pmatrix}t\\u\end{pmatrix}
+v^\dagger M^{-1}v \tag{28}
\]
combined with (25)--(27) proves (24).

## 7. Exact theorem when one summand is normal

### Theorem 7.1

The Ky--Fan inequality (KF) holds if either \(A\) or \(B\) is normal. The
other matrix may be arbitrary and nonnormal.

### Proof

By symmetry suppose \(A\) is normal. After unitary conjugation write
\[
A=\operatorname{diag}(a_1,a_2,a_3),\qquad
a_1+a_2+a_3=0.
\]
Then \(D\) is the orthogonal direct sum
\[
D=\bigoplus_{j=1}^3\bigl(B+t_jI_3\bigr),
\qquad t_j=a_j+c. \tag{29}
\]
There are two possibilities for the two largest singular values of \(D\).

If both come from the same block \(j\), Lemma 6.2 gives
\[
s_1(D)^2+s_2(D)^2
\le2\|B\|^2+\frac{12}{5}|a_j+c|^2. \tag{30}
\]
On the Hilbert space
\[
\{(a_1,a_2,a_3):\textstyle\sum a_i=0\}\oplus\mathbb C
\]
with squared norm \(2\sum_i|a_i|^2+12|c|^2\), the evaluation functional
\((a,c)\mapsto a_j+c\) has squared dual norm
\[
\frac12\left(1-\frac13\right)+\frac1{12}
=\frac5{12}. \tag{31}
\]
Thus
\[
\frac{12}{5}|a_j+c|^2
\le2\|A\|^2+12|c|^2,
\]
which proves (KF) in this case.

If the two singular values come from distinct blocks \(j\ne k\), apply
Lemma 6.3 to their respective right singular vectors:
\[
\begin{aligned}
s_1(D)^2+s_2(D)^2\le 2\|B\|^2
+M(t_j,t_k), \tag{32}
\end{aligned}
\]
where
\[
M(t,u)=\frac52(|t|^2+|u|^2)
       +\operatorname{Re}(\overline t u).
\]
The Gram matrix of the two evaluation functionals
\((a,c)\mapsto(a_j+c,a_k+c)\) is exactly \(M^{-1}\) from (26). Equivalently,
by the two-variable matrix Cauchy inequality,
\[
M(a_j+c,a_k+c)
\le2\sum_i|a_i|^2+12|c|^2. \tag{33}
\]
Combining (32) and (33) proves (KF). Interchanging the two tensor factors
handles the case in which \(B\) is normal.

### Sharpness and limitation

The constants in the proof cannot simply be reduced. Lemma 6.2 is sharp:
for any \(t\), take
\[
B=\operatorname{diag}(t/5,t/5,-2t/5).
\]
Then the two largest singular values of \(B+tI\) are both \(6|t|/5\),
and both sides of (21) equal \(72|t|^2/25\). Theorem 7.1 does not address
the remaining case in which both \(A\) and \(B\) are nonnormal; the
nilpotent family (17)--(19) shows that this remaining case contains
equality points, so it cannot be disposed of by a strict perturbative
margin.

## 8. An exact simultaneous-nonnormal \(2\times2\) core theorem

The larger equality family admits a useful extension that covers arbitrary
nonnormal matrices on a common \(2+1\) reducing decomposition, provided
their one-dimensional blocks vanish and \(c=0\).

### Lemma 8.1: paired singular values

Let \(A_2,B_2\in M_2\) be arbitrary traceless matrices and set
\[
K=I_2\otimes A_2+B_2\otimes I_2,\qquad
S=\|A_2\|^2+\|B_2\|^2.
\]
Then
\[
\left(K^\dagger K\right)^2
-S K^\dagger K
+|\det A_2-\det B_2|^2 I_4=0. \tag{34}
\]
Consequently the singular values of \(K\) occur in equal pairs
\[
\sigma_+,\sigma_+,\sigma_-,\sigma_-,
\qquad
\sigma_+^2+\sigma_-^2=S. \tag{35}
\]

#### Proof

Every traceless \(2\times2\) matrix \(M\) satisfies the directly checked
identities
\[
M^2=-\det(M)I_2,\qquad
M^\dagger M+MM^\dagger=\|M\|^2I_2. \tag{36}
\]
Here is the full collection step. Write
\[
\begin{gathered}
a=\|A_2\|^2,\quad b=\|B_2\|^2,\quad
\alpha=\det A_2,\quad\beta=\det B_2,\\
X=A_2^\dagger A_2,\quad Y=B_2^\dagger B_2,\\
P=I\otimes X+Y\otimes I,\quad
C=B_2^\dagger\otimes A_2+B_2\otimes A_2^\dagger.
\end{gathered}
\]
Then \(K^\dagger K=P+C\). Cayley--Hamilton applied to the positive
\(2\times2\) matrices \(X,Y\) gives
\[
X^2=aX-|\alpha|^2I,\qquad
Y^2=bY-|\beta|^2I.
\]
Using also \(A_2A_2^\dagger=aI-X\) and
\(B_2B_2^\dagger=bI-Y\), direct multiplication yields
\[
\begin{aligned}
P^2-(a+b)P
={}&-bI\otimes X-aY\otimes I+2Y\otimes X\\
&-(|\alpha|^2+|\beta|^2)I,\\
C^2
={}&bI\otimes X+aY\otimes I-2Y\otimes X
  +2\operatorname{Re}(\alpha\overline\beta)I.
\end{aligned}
\]
Finally, (36) implies
\[
XA_2+A_2X=aA_2,\qquad
YB_2^\dagger+B_2^\dagger Y=bB_2^\dagger,
\]
and their adjoints, whence
\[
PC+CP=(a+b)C.
\]
Adding these identities gives
\[
(P+C)^2-(a+b)(P+C)
=-|\alpha-\beta|^2I,
\]
which is (34). The two roots of the scalar quadratic in (34) are
nonnegative and sum to \(S=a+b\). Since
\[
\det(\lambda I_4-K^\dagger K)
=\left(\lambda^2-S\lambda
+|\det A_2-\det B_2|^2\right)^2,
\]
each occurs twice, proving (35).

### Corollary 8.2

Let
\[
A=A_2\oplus0,\qquad B=B_2\oplus0,\qquad c=0,
\]
where \(A_2,B_2\) are arbitrary traceless \(2\times2\) matrices. Then (KF)
holds, even when both matrices are nonnormal.

Indeed \(D\) is the orthogonal direct sum of
\[
K,\qquad A_2,\qquad B_2,\qquad 0. \tag{37}
\]
Every squared singular value in these four blocks is at most
\[
S=\|A_2\|^2+\|B_2\|^2:
\]
this is immediate for \(A_2,B_2\), and follows from (35) for \(K\).
Therefore the sum of the two largest squared singular values is at most
\(2S=2\|A\|^2+2\|B\|^2\).

The equality condition \(\det A_2=\det B_2\) makes
\(\sigma_- =0\) and \(\sigma_+^2=S\), recovering (19a)--(19d) after
choosing the displayed off-diagonal \(2\times2\) matrices. Thus the most visible
simultaneous-nonnormal equality manifold is fully controlled by the
dimension-two Hodge identity (36). The unresolved configurations are those
with genuinely three-dimensional nonnormal coupling, or with nontrivial
interaction between such a core and the scalar/one-dimensional blocks.

## 9. Exact obstruction exposed by Hodge complementation

Let
\[
K_{ij}=|i\rangle\langle j|-|j\rangle\langle i|,
\qquad 0\le i<j\le2.
\]
The elementary Hodge/reduction identity is
\[
\sum_{i<j}K_{ij}MK_{ij}^\dagger
=\operatorname{Tr}(M)I-M^T. \tag{38}
\]
It gives, for every \(A\),
\[
\|A\|^2I-A^\dagger A
=\sum_{i<j}(K_{ij}A^T)(K_{ij}A^T)^\dagger. \tag{39}
\]
Thus each individual deficit in (14) has an exact Gram factorization.
This is the expected local Hodge square.

The difficulty occurs when the \(A\)- and \(B\)-factorizations are paired
to reproduce \(\langle X,Y\rangle\). Moving a Hodge factor through the
skew matrix \(Z\) uses \(Z^T=-Z\) and reverses left/right multiplication.
The resulting complementary norm contains \(AA^\dagger\) where the
desired deficit contains \(A^\dagger A\), and analogously for \(B\).
Their difference is precisely the nonnormal commutator
\[
[A,A^\dagger]\quad\text{or}\quad[B,B^\dagger]. \tag{40}
\]
When one summand is normal this orientation defect disappears, consistent
with Theorem 7.1. When both are nonnormal, separately positive
\(\operatorname{Sym}^2/\Lambda^2\) sector effects do not remember that the
two Hodge tensors in (9) arose from one common decomposable two-form. The
missing information is the nonlinear Plücker relation \(Z\wedge Z=0\).

This explains why simply applying Cauchy--Schwarz to all four lines of
(11) loses the sharp constant: it treats the \(P,R\) components as
independent, while the equality families (19a) and Corollary 8.2 use exact
phase alignment between them.

## 10. Precise status

### Proved

1. The original \(d=3,n=2\) rank-two endpoint inequality is exactly
   equivalent to (KF), the skew-matrix inequality (7), and the strengthened
   scalar-free condition (13).
2. The Hodge decomposition and all four action routes in (9)--(11) are
   exact, including the traceless action \(-A^T\) on
   \(\Lambda^2\mathbb C^3\).
3. The full inequality, with arbitrary \(c\), holds when either \(A\) or
   \(B\) is normal; the other summand may be arbitrary.
4. The inequality is sharp on simultaneous-nonnormal matrices. The family
   (19a) gives exact equality, and Lemma 8.1/Corollary 8.2 settle its entire
   arbitrary traceless \(2\times2\) core.

### Not proved

No proof or counterexample was obtained for arbitrary simultaneously
nonnormal \(3\times3\) matrices with genuine three-dimensional coupling.
Consequently this notebook does not by itself settle the full two-copy
endpoint theorem.

The remaining exact target can be taken to be either:

- the correlation inequality (15) plus the scalar strengthening (13); or
- a sum-of-squares factorization of the four Hodge sectors (11) that uses
  the common Plücker relation rather than treating \(P,R\) independently.

Alternating floating-point optimization repeatedly converged to ratio
\(1\), including nonnormal equality points, and did not find a ratio above
\(1\). This is discovery evidence only and is not used in any proof.

No hardware limitation affected the exact work. Larger searches might help
guess the missing Plücker square, but cannot certify the uniform
inequality without an exact identity.
