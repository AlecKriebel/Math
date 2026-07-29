# Haar-equality block collapse and the two-copy kernel frontier

## Status

This note proves two exact reductions for the unrestricted qutrit
three-copy endpoint.

1.  At a negative Haar-filter equality, the complete \(9\times9\)
    matrix of two-copy pairings between the local blocks of one
    rank-two matrix has rank one:
    \[
      {\cal B}_2(C_{rp},C_{sq})
      =\gamma\,\delta_{rp}\delta_{sq}.
      \tag{1}
    \]
2.  The fixed-left two-copy kernel is classified completely whenever
    the left two-plane has deficient local support.  A two-plane with
    minimal support \(2\times2\) has kernel dimension one, whereas a
    plane with a fixed local factor has kernel dimension three.

Together these facts reduce exclusion of a negative Haar equality to
one explicit interior rigidity lemma:
\[
 \boxed{\quad
 \dim\ker {\cal H}_U\geq2
 \ \Longrightarrow\
 U\text{ has a fixed local factor}.
 \quad}
 \tag{2}
\]
Here \(U\subset\mathbb C^3\otimes\mathbb C^3\) is a two-plane and
\({\cal H}_U\) is the fixed-left compression of the two-copy endpoint,
defined precisely in Section 3.  This note proves (2) on every
locally-support-deficient plane.  The only unproved part is the case
in which at least one of the two local supports of \(U\) has dimension
three.

Thus this is not a proof of unrestricted three-copy positivity.  It is
a strict nonlinear reduction of the putative sharp negative equality.
The independent exact checker
`verification/verify_n3_haar_block_collapse.py` verifies the full
coefficient inversion leading to (1).

## 1. Block expansion of the isotropic local form

Let
\[
 {\cal B}_2(D,E)
 =\langle D,{\cal L}^{\otimes2}(E)\rangle_{\rm HS},
 \qquad
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3.
 \tag{3}
\]
Fix the first physical site and write a three-copy matrix as a
\(3\times3\) block matrix
\[
 C=(C_{ap})_{a,p=0}^2,
 \qquad C_{ap}\in M_9.
 \tag{4}
\]
Define
\[
 \beta_{ap,bq}={\cal B}_2(C_{ap},C_{bq}).
 \tag{5}
\]

Suppose that the complete local-filter form is isotropic:
\[
 h(A,B)
 :=
 \left\langle A^{(1)}C,
 {\cal L}^{\otimes3}(B^{(1)}C)\right\rangle_{\rm HS}
 =
 \gamma\left(
 \langle A,B\rangle_{\rm HS}
 -\frac12\overline{\operatorname{Tr}A}\operatorname{Tr}B
 \right)
 \tag{6}
\]
for every \(A,B\in M_3\), with \(\gamma>0\).  The equality
classification of the Haar boundary filter gives exactly (6) at a
putative negative equality.

The blocks of \(A^{(1)}C\) are
\[
 (A^{(1)}C)_{rp}=\sum_a A_{ra}C_{ap}.
 \tag{7}
\]
Applying the remaining local copy of \({\cal L}\) and comparing the
coefficient of \(\overline{A_{ra}}B_{tb}\) gives
\[
 \boxed{\quad
 \delta_{rt}\sum_p\beta_{ap,bp}
 -\frac12\beta_{ar,bt}
 =
 \gamma\delta_{rt}\delta_{ab}
 -\frac\gamma2\delta_{ra}\delta_{tb}.
 \quad}
 \tag{8}
\]

### Proposition 1

Equation (8) has the unique solution
\[
 \boxed{\qquad
 \beta_{ap,bq}=\gamma\,\delta_{ap}\delta_{bq}.
 \qquad}
 \tag{9}
\]

### Proof

If \(r\ne t\), (8) immediately gives
\[
 \beta_{ar,bt}=\gamma\delta_{ar}\delta_{bt}.
 \tag{10}
\]
For the remaining entries put
\[
 D_r^{ab}=\beta_{ar,br},
 \qquad S^{ab}=\sum_pD_p^{ab}.
 \tag{11}
\]
The \(r=t\) instances of (8) say
\[
 S^{ab}-\frac12D_r^{ab}
 =\gamma\delta_{ab}
 -\frac\gamma2\delta_{ar}\delta_{br}.
 \tag{12}
\]
Therefore
\[
 D_r^{ab}
 =2S^{ab}-2\gamma\delta_{ab}
 +\gamma\delta_{ar}\delta_{br}.
 \tag{13}
\]
Summing (13) over \(r=0,1,2\) yields
\[
 S^{ab}=6S^{ab}-5\gamma\delta_{ab},
 \]
and hence \(S^{ab}=\gamma\delta_{ab}\).  Substitution in
(13), together with (10), proves (9).  The calculation determines
all \(81\) entries, so the solution is unique. \(\square\)

In vector notation, (9) is
\[
 \beta=\gamma\,|\operatorname{vec}I_3\rangle
                 \langle\operatorname{vec}I_3|.
 \tag{14}
\]
This is substantially stronger than any statement about the nine
diagonal block energies.

## 2. Consequence of the common rank-two factorization

Write the rank-two matrix as
\[
 C=XY^\dagger,
 \qquad
 X,Y:\mathbb C^2\longrightarrow
 (\mathbb C^3)^{\otimes3}.
 \tag{15}
\]
At the selected site decompose
\[
 X=\sum_r|r\rangle\otimes X_r,\qquad
 Y=\sum_p|p\rangle\otimes Y_p,
 \tag{16}
\]
where \(X_r,Y_p:\mathbb C^2\to\mathbb C^3\otimes\mathbb C^3\).
Then
\[
 C_{rp}=X_rY_p^\dagger.
 \tag{17}
\]

For a fixed two-column matrix \(Z\), define the Hermitian form
\[
 k_Z(R,S)
 ={\cal B}_2(ZR^\dagger,ZS^\dagger).
 \tag{18}
\]
Every matrix \(ZR^\dagger\) has rank at most two.  The established
unrestricted qutrit two-copy theorem therefore says
\[
 k_Z(R,R)\geq0
 \quad\hbox{for every }R.
 \tag{19}
\]
Thus \(k_Z\) is represented by a positive semidefinite operator,
which we denote by \({\cal H}_Z\).

From (9), for each fixed \(r\),
\[
 k_{X_r}(Y_p,Y_q)
 =\gamma\,\delta_{rp}\delta_{rq}.
 \tag{20}
\]
The two vectors \(Y_p\), \(p\ne r\), therefore lie in
\(\ker{\cal H}_{X_r}\).  At an interior negative critical point the
one-site reduction of the right singular plane is positive definite,
so the three slices \(Y_0,Y_1,Y_2\) are Hilbert--Schmidt independent.
Consequently
\[
 \boxed{\qquad
 \dim\ker{\cal H}_{X_r}\geq2
 \quad(r=0,1,2).
 \qquad}
 \tag{21}
\]
Because (6) is basis independent, the same conclusion holds after
every local unitary change of basis.  Equivalently, (21) holds for
every generic nonzero linear combination
\[
 X(z)=z_0X_0+z_1X_1+z_2X_2.
 \tag{22}
\]

## 3. Exact kernel classification on the local-support boundary

Let \(U\subset\mathbb C^3\otimes\mathbb C^3\) be a two-plane and
choose any isometry \(Z:\mathbb C^2\to U\).  The kernel dimension of
\({\cal H}_Z\) depends only on \(U\), so write it as
\(\nu(U)\).

### Theorem 2

Suppose both minimal local supports of \(U\) have dimension at most
two.

1. If the support dimensions are \((2,2)\), then
   \[
     \nu(U)=1.
     \tag{23}
   \]
2. If \(U\) has a fixed local factor, so that its support dimensions
   are \((1,2)\) or \((2,1)\), then
   \[
     \nu(U)=3.
     \tag{24}
   \]

### Proof

First consider one physical site.  If the left row support is a
subspace \(W\subset\mathbb C^3\) of dimension \(r\leq2\), then
Cauchy--Schwarz gives
\[
 \|D\|_2^2-\frac12|\operatorname{Tr}D|^2
 \geq\left(1-\frac r2\right)\|D\|_2^2
 \tag{25}
\]
for every operator \(D\) with row support in \(W\).  For \(r=1\)
the compressed one-copy form is positive definite.  For \(r=2\)
it is positive semidefinite with one-dimensional kernel, spanned by
the canonical identity map
\[
 J_W=\sum_{a=0}^1|w_a\rangle\langle\overline{w_a}|
 \tag{26}
\]
for any orthonormal basis of \(W\).

If the support dimensions of \(U\) are \((1,2)\), the two-copy
compression is the tensor product of a positive definite
three-dimensional one-copy form and a one-copy form with a
one-dimensional kernel.  Its kernel therefore has dimension three.
The case \((2,1)\) is identical.  This proves (24).

It remains to treat minimal support \((2,2)\).  Identify the two
supports with \(\mathbb C^2\).  The kernel of the tensor product of
the two compressed one-copy forms consists of matrices
\[
 C=I_2\otimes A+B\otimes I_2.
 \tag{27}
\]
Components of \(A\) or \(B\) whose input lies outside the conjugate
two-dimensional right supports must vanish.  Indeed, a nonzero such
component would make the range of \(C\) contain a full factor plane
\(a\otimes\mathbb C^2\) or
\(\mathbb C^2\otimes b\).  Since the range is contained in the
two-plane \(U\), this would force \(U\) itself to be a factor plane,
contrary to the minimal support dimensions \((2,2)\).

We may therefore regard (27) as a \(4\times4\) matrix.  Put
\[
 \epsilon=
 \begin{pmatrix}0&1\\-1&0\end{pmatrix},
 \qquad J=\epsilon\otimes\epsilon.
 \tag{28}
\]
Right multiplication by \(J\) maps
\[
 \mathfrak{sl}_2\otimes I_2+I_2\otimes\mathfrak{sl}_2
 \tag{29}
\]
isomorphically onto the six-dimensional space of skew-symmetric
\(4\times4\) matrices.  The scalar direction \(I_4\) maps to the
symmetric matrix \(J\).  Hence every matrix in (27) has the unique
form
\[
 CJ=S+cJ,\qquad S^{\mathsf T}=-S.
 \tag{30}
\]

Let \(L\subset(\mathbb C^4)^*\) be the two-dimensional annihilator of
\(U\).  If \(\operatorname{ran}C\subseteq U\), then
\(\ell^{\mathsf T}CJ=0\) for every \(\ell\in L\).  Therefore, for
\(\ell,m\in L\), (30) gives
\[
 0
 =\ell^{\mathsf T}(CJ+(CJ)^{\mathsf T})m
 =2c\,\ell^{\mathsf T}Jm.
 \tag{31}
\]
The restriction of \(J\) to \(L\) cannot vanish identically.  If it
did, every vector of \(L\), reshaped as a \(2\times2\) matrix, would
have determinant zero.  A two-dimensional linear space consisting
entirely of rank-one \(2\times2\) matrices has a common left or right
factor: for independent \(a\otimes b,c\otimes d\), rank one of their
sum forces either \(a\parallel c\) or \(b\parallel d\).  Its
annihilator \(U\) would then be a factor plane, a contradiction.

Thus (31) forces \(c=0\).  A skew matrix whose range is contained in
the two-plane \(U\) is a scalar multiple of its decomposable bivector
\[
 u_0u_1^{\mathsf T}-u_1u_0^{\mathsf T}.
 \tag{32}
\]
The kernel in (27) is consequently one-dimensional.  This proves
(23). \(\square\)

Theorem 2 proves the proposed rigidity statement (2) on the complete
local-support boundary.  It also audits the two visible equality
families exactly: a generic common \(2\times2\) support contributes
one kernel line, while a fixed-factor plane contributes three.

## 4. The remaining interior rigidity lemma

The exact missing statement is now:

> **Two-copy kernel rigidity.**  If \(U\subset
> \mathbb C^3\otimes\mathbb C^3\) is a two-plane and
> \(\nu(U)\geq2\), then \(U=a\otimes W\) or \(U=W\otimes a\).

Numerical discovery tests find no exception.  They also suggest the
stronger statement
\[
 \nu(U)>0
 \quad\Longleftrightarrow\quad
 \dim\operatorname{supp}_1U\leq2
 \ \hbox{and}\
 \dim\operatorname{supp}_2U\leq2,
 \tag{33}
\]
but only the nullity-at-least-two assertion is required here.
Theorem 2 leaves only planes with a three-dimensional support on at
least one side.

## 5. Why the rigidity lemma would exclude the Haar equality

Assume the rigidity lemma.  Equation (21), after arbitrary basis
changes, says that every generic element of the linear space
\[
 {\cal S}_X=\operatorname{span}\{X_0,X_1,X_2\}
 \subset
 \operatorname{Hom}(\mathbb C^2,
 \mathbb C^3\otimes\mathbb C^3)
 \tag{34}
\]
has a fixed factor at one of the two remaining physical sites.
The two possible factor conditions are closed determinantal
varieties.  A complex linear space cannot be contained in their
finite union without being contained in one of them.

Finally, a linear space of matrices all having rank at most one has
either a common image line or a common row factor.  This follows by
applying the same rank-one sum argument used in the proof of
Theorem 2.  Here the reshape is the \(3\times6\) flattening
\[
 X(z):\mathbb C^3\otimes\mathbb C^2\longrightarrow\mathbb C^3
 \tag{35}
\]
across one remaining physical site versus the other site together
with the two-dimensional singular auxiliary space.  In the first
case the full left singular plane has a
one-dimensional local support.  In the second, the common row factor
lies in \(\mathbb C^3\otimes\mathbb C^2\), so the corresponding
physical local support of the full two-plane has dimension at most
two.  Both conclusions contradict the positive-definite one-site
reductions required at an interior negative critical point.

Hence the kernel-rigidity lemma would make the exact isotropic system
(6) impossible for a rank-two matrix.  This excludes the formal
Haar-saturating negative sector point without imposing Hermiticity,
normality, reality, or a fixed tensor ansatz.  It does not by itself
exclude a negative point which fails to saturate the Haar bound.
