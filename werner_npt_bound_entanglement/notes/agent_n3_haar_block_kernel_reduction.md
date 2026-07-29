# Haar-equality block collapse and the two-copy kernel frontier

## Status

This note proves an exact nonlinear exclusion theorem for the
unrestricted qutrit three-copy endpoint.

1.  At a negative Haar-filter equality, the complete \(9\times9\)
    matrix of two-copy pairings between the local blocks of one
    rank-two matrix has rank one:
    \[
      {\cal B}_2(C_{rp},C_{sq})
      =\gamma\,\delta_{rp}\delta_{sq}.
      \tag{1}
    \]
2.  The fixed-left two-copy kernel is classified completely.  Its
    nullity is \(0\) on a plane with a full local support, \(1\) on a
    plane of minimal support \(2\times2\), and \(3\) on a plane with a
    fixed local factor.
3.  The block collapse and this nullity classification force every
    generic one-site slice of both singular planes to be a factor
    plane.  An exact linear-pencil classification then contradicts
    full local support.

Consequently no physical rank-two matrix can realize the isotropic
local form with \(\gamma>0\) even at one site.  In particular, every
sitewise Haar-filter inequality is strict at a hypothetical negative
rank-two matrix, and the formal Haar-saturating negative sector point
is not rank-two realizable.

This is not yet a proof of unrestricted three-copy positivity: a
negative matrix with strict Haar-filter slack is not excluded.  The
independent exact checker
`verification/verify_n3_haar_block_collapse.py` verifies the full
coefficient inversion leading to (1).  The companion checker
`verification/verify_n3_haar_block_gram_collapse.py` audits the
canonical fixed-left nullities and the excluded split branch.

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

## 4. Complete fixed-left nullity classification

The missing interior implication has now been proved independently in
`notes/agent_n3_haar_block_gram_collapse.md`:

> **Fixed-left strictness theorem.**  If \(U\subset
> \mathbb C^3\otimes\mathbb C^3\) is a two-plane and
> \(\ker{\cal H}_U\ne0\), then both minimal local supports of \(U\)
> have dimension at most two.

That proof uses the exact equality conditions in the completed
two-copy reversed-Hodge inequality.  It classifies the kernel of the
rank-two reduction gap into a common-\(2\times2\) branch and one
apparent split full-support branch, then excludes the split branch by
the remaining cross-product equality equations.  No numerical
classification enters the argument.

Combining that theorem with Theorem 2 gives the following exhaustive
statement.

### Corollary 3

For every two-plane
\(U\subset\mathbb C^3\otimes\mathbb C^3\),
\[
 \boxed{
 \nu(U)=
 \begin{cases}
 0,&\text{if at least one minimal local support has dimension }3,\\
 1,&\text{if the minimal support dimensions are }(2,2),\\
 3,&\text{if \(U\) has a fixed local factor.}
 \end{cases}}
 \tag{33}
\]
In particular,
\[
 \boxed{\quad
 \nu(U)\geq2
 \quad\Longleftrightarrow\quad
 U=a\otimes W\ \hbox{or}\ U=W\otimes a .
 \quad}
 \tag{34}
\]

### Proof

The fixed-left strictness theorem gives the first line.  Once both
supports have dimension at most two, a two-plane has either minimal
support \((2,2)\) or a fixed local factor; Theorem 2 gives nullity one
and three, respectively.  These cases are exhaustive, since a
two-dimensional plane cannot have minimal support \((1,1)\).
\(\square\)

## 5. Factor-plane pencils

We record the two elementary algebraic facts needed to pass from
slice-wise factorization to a statement about the full three-copy
code.

### Lemma 4 (upper-rank-one linear spaces)

Let \({\cal V}\) be a complex linear space of matrices, every member
of which has rank at most one.  Then either all members have image in
one common line, or all members have row space in one common line.

### Proof

Choose a nonzero \(A=a\varphi^{\mathsf T}\in{\cal V}\).  For every
rank-one \(B=b\psi^{\mathsf T}\in{\cal V}\), the condition
\(\operatorname{rank}(A+B)\leq1\) implies
\[
 a\wedge b=0\quad\hbox{or}\quad\varphi\wedge\psi=0.
 \tag{35}
\]
If every \(b\) is proportional to \(a\), there is a common image
line.  Otherwise choose \(B\) with \(a\wedge b\ne0\); then
\(\psi\parallel\varphi\).  If some
\(C=c\chi^{\mathsf T}\) had \(\chi\not\parallel\varphi\), (35) applied
to \(A,C\) would force \(c\parallel a\), but then (35) applied to
\(B,C\) would fail in both factors.  Thus every row factor is
proportional to \(\varphi\). \(\square\)

### Lemma 5 (a pencil cannot switch factor side)

Let
\[
 {\cal S}=\operatorname{span}\{X_0,X_1,X_2\}
 \subset
 \operatorname{Hom}(\mathbb C^2,
 \mathbb C^3\otimes\mathbb C^3).
 \tag{36}
\]
Suppose that, for generic \(z\in\mathbb C^3\), the two-plane
\(\operatorname{ran}X(z)\), where
\[
 X(z)=z_0X_0+z_1X_1+z_2X_2,
 \tag{37}
\]
has a fixed factor on one of the two qutrits.  Then one of the two
physical flattenings of every member of \({\cal S}\) has matrix rank
at most one.

### Proof

For \(j=2,3\), let \({\cal Z}_j\subset\mathbb P^2\) be the common zero
set of the \(2\times2\) minors of the flattening
\[
 X(z):\mathbb C^3\otimes\mathbb C^2\longrightarrow
 \mathbb C^3
 \tag{38}
\]
with the \(j\)-th qutrit as output.  These are closed algebraic sets,
and the hypothesis says that
\({\cal Z}_2\cup{\cal Z}_3\) contains a dense open subset.  Hence this
union is all of \(\mathbb P^2\).

If both sets were proper, choose one nonzero minor polynomial \(f\)
for the first flattening and one nonzero minor polynomial \(g\) for
the second.  Their product would vanish for every \(z\), hence would
be the zero polynomial.  This is impossible because
\(\mathbb C[z_0,z_1,z_2]\) has no zero divisors.  Thus one
\({\cal Z}_j\) is all of \(\mathbb P^2\), which is precisely the
claim. \(\square\)

If the flattening singled out by Lemma 5 always has rank at most one,
Lemma 4 gives two alternatives.  A common image line makes the full
three-copy code have one-dimensional support on that qutrit.  A
common row factor lies in
\(\mathbb C^3\otimes\mathbb C^2\); its qutrit support has dimension
at most two because the auxiliary factor has dimension two.  It
therefore makes the full code have support of dimension at most two
on the other qutrit.  In either case the full code is not locally
full-supported.

## 6. Exclusion of a negative Haar equality

### Theorem 6

No rank-two matrix on three qutrit copies can satisfy the isotropic
local system (6) with \(\gamma>0\) at even one site.  Consequently,
if \(Q_3(C)<0\), then every one of the three sitewise Haar-filter
inequalities is strict.

### Proof

Take a thin singular factorization
\[
 C=XSY^\dagger,\qquad
 X^\dagger X=Y^\dagger Y=I_2,\qquad
 S=\operatorname{diag}(s_1,s_2)>0,
 \tag{39}
\]
and slice it at the selected site:
\[
 X=\sum_a|a\rangle\otimes X_a,\qquad
 Y=\sum_b|b\rangle\otimes Y_b.
 \tag{40}
\]
Then
\[
 C_{ab}=X_aS Y_b^\dagger.
 \tag{41}
\]
The collapse (9) says
\[
 {\cal B}_2(X_aS Y_b^\dagger,X_cS Y_d^\dagger)
 =\gamma\delta_{ab}\delta_{cd}.
 \tag{42}
\]

The collapse itself makes the three slices \(X_a\) linearly
independent, and likewise the three \(Y_b\).  Indeed, if
\(\sum_b c_bY_b=0\), then for every fixed \(a\),
\[
 0
 =Q_2\left(\sum_b\overline{c_b}C_{ab}\right)
 =\gamma|c_a|^2,
 \tag{43}
\]
where (42) was used in the last equality.  Thus every \(c_a=0\).
The proof for the \(X_a\) is the same, combining blocks down a fixed
column.  In particular, none of the six slices is zero.

Each off-diagonal block has zero two-copy energy.  The strict
rank-one bound
\[
 Q_2(M)\geq\frac14\|M\|_2^2
 \quad(\operatorname{rank}M=1)
 \tag{44}
\]
therefore says that every off-diagonal block is either zero or has
rank two.  At least one is nonzero: otherwise \(C\) would be block
diagonal with three nonzero diagonal blocks, and hence would have
rank at least three.

Starting from one rank-two off-diagonal block, rank two propagates to
all six factors \(X_a,Y_b\).  Indeed, the bipartite graph on the
three \(X\)-vertices and three \(Y\)-vertices with the diagonal
matching removed is connected.  Along an edge, if one factor is
injective and the other is nonzero, their product in (41) is nonzero;
it cannot have rank one by (44), so the other factor is injective.

Fix \(r\).  Equation (42) gives
\[
 {\cal B}_2(X_rS Y_p^\dagger,X_rS Y_q^\dagger)=0
 \qquad(p,q\ne r).
 \tag{45}
\]
The two maps \(Y_p,Y_q\), \(p,q\ne r\), are independent.  After an
invertible change of the two-dimensional auxiliary coordinate,
(45) says
\[
 \nu(\operatorname{ran}X_r)\geq2.
 \tag{46}
\]
Corollary 3 therefore makes \(\operatorname{ran}X_r\) a fixed-factor
plane.  The same argument after an arbitrary local basis change shows
that \(\operatorname{ran}X(z)\) is a fixed-factor plane for generic
\(z\).  Applying the adjoint argument gives the same conclusion for
the \(Y\)-pencil.

Lemma 5 and Lemma 4 now imply that the full left singular plane
\(\operatorname{ran}X\) has local support of dimension at most two on
one of the remaining sites.  The established local-support boundary
theorem therefore gives
\[
 Q_3(C)\geq0.
 \tag{47}
\]
On the other hand, putting \(A=B=I_3\) in (6) gives
\[
 Q_3(C)=\gamma Q_1(I_3)=-\frac32\gamma<0.
 \tag{48}
\]
This contradiction proves the theorem.  The same contradiction could
equally be obtained from \(Y\). \(\square\)

The theorem uses the common origin of all nine block pairings; it
does not bound polarized block contributions separately.  It excludes
the sharp formal sector point without imposing Hermiticity,
normality, reality, or a tensor ansatz.  Its exact remaining
limitation is strict Haar-filter slack: a negative point need not
satisfy the isotropic system (6).

## 7. Exact strict-slack and critical trace formulas

For a normalized matrix \(C\), write
\[
 w_S=\|\Pi_SC\|_2^2
 \qquad(S\subseteq\{1,2,3\}).
 \tag{49}
\]
At site \(i\), with complementary sites \(j,k\), define the sitewise
Haar bracket
\[
 g_i=
 \frac14w_{\{i\}}
 -\frac12\left(w_{\{i,j\}}+w_{\{i,k\}}\right)
 +w_{\{1,2,3\}}.
 \tag{50}
\]
The established boundary-filter identity says
\[
 {\mathbb E}_z\,
 Q_3\left((I-|z\rangle\langle z|)^{(i)}C\right)
 =\frac58g_i,
 \qquad g_i\geq0.
 \tag{51}
\]

### Corollary 7 (sitewise strictness)

If \(\operatorname{rank}C\leq2\) and \(Q_3(C)<0\), then
\[
 \boxed{\qquad g_i>0\quad(i=1,2,3).\qquad}
 \tag{52}
\]

### Proof

If \(g_i=0\), the continuous nonnegative integrand in (51) vanishes
for every \(z\).  The exact boundary-zero form classification then
gives the isotropic identity (6), with
\[
 \gamma=-\frac23Q_3(C)>0.
 \]
This contradicts Theorem 6. \(\square\)

The strictness has a uniform, although presently non-explicit,
stability consequence.  For every \(\varepsilon>0\), compactness of
\[
 \left\{C:\operatorname{rank}C\leq2,\ \|C\|_2=1,\
 Q_3(C)\leq-\varepsilon\right\}
 \tag{53}
\]
and continuity of \(g_i\) give a number
\(\eta(\varepsilon)>0\) such that
\[
 g_i(C)\geq\eta(\varepsilon)
 \quad\text{for all three sites.}
 \tag{54}
\]
Thus a sequence whose sitewise Haar slack tends to zero can remain
negative only if its endpoint value tends to zero.  Formula (54) is
qualitative; an explicit lower bound is still missing.

There is also an exact critical-point interpretation of the slack.
Suppose \(C\) is a normalized local minimum of the endpoint Rayleigh
quotient on the rank-two variety, put
\[
 q=Q_3(C)<0,
 \tag{55}
\]
and define the local endpoint and norm forms
\[
\begin{aligned}
 h_i(A,B)&=
 \left\langle A^{(i)}C,
 {\cal L}^{\otimes3}(B^{(i)}C)\right\rangle_{\rm HS},\\
 n_i(A,B)&=\langle A^{(i)}C,B^{(i)}C\rangle_{\rm HS},\\
 G_i&=h_i-qn_i.
\end{aligned}
 \tag{56}
\]
Rank-preserving local-filter variations give
\[
 G_i\succeq0,\qquad G_i(I,A)=0\quad(A\in M_3).
 \tag{57}
\]

### Proposition 8 (Haar slack is the local trace excess)

With the ordinary Hilbert--Schmidt trace on forms on \(M_3\),
\[
 \boxed{\qquad
 \operatorname{Tr}_{\rm HS}G_i
 +8q
 =\frac{15}{2}g_i
 =12\,{\mathbb E}_z
 Q_3\left((I-|z\rangle\langle z|)^{(i)}C\right)>0.
 \qquad}
 \tag{58}
\]
The same identity holds for right local filters.

### Proof

Split the endpoint expectation according to whether site \(i\) is
locally scalar or traceless:
\[
 q=a_i+g_i.
 \tag{59}
\]
Here
\[
 a_i=-\frac18w_\varnothing
 +\frac14(w_{\{j\}}+w_{\{k\}})
 -\frac12w_{\{j,k\}}.
 \tag{60}
\]
For a Hilbert--Schmidt orthonormal matrix-unit basis,
\[
 \sum_{a,b}
 \left\langle E_{ab}X,{\cal L}(E_{ab}X)\right\rangle_{\rm HS}
 =\frac52\|X\|_2^2.
 \tag{61}
\]
Indeed, the summed squared masses in the scalar and traceless output
sectors are respectively \(\frac13\|X\|_2^2\) and
\(\frac83\|X\|_2^2\).  The local endpoint eigenvalues
\(-\frac12,1\) turn their sum into \(5\|X\|_2^2/2\).

Removing the endpoint eigenvalue at site \(i\) changes the scalar
contribution \(a_i\) by the factor \(-2\) and leaves the traceless
contribution \(g_i\) unchanged.  Therefore
\[
 \operatorname{Tr}_{\rm HS}h_i
 =\frac52(-2a_i+g_i)
 =-5q+\frac{15}{2}g_i.
 \tag{62}
\]
Likewise,
\[
 \operatorname{Tr}_{\rm HS}n_i=3\|C\|_2^2=3.
 \tag{63}
\]
Subtracting \(q\operatorname{Tr}n_i\) proves the first equality in
(58), and (51) proves the second.  Strict positivity follows from
Corollary 7. \(\square\)

Thus \(-8q\) is the sharp local trace floor for the positive critical
form \(G_i\), and the Haar bracket is exactly its excess above that
floor.  Equality at the floor is the isotropic form already excluded
by Theorem 6.  The unresolved strict-slack problem is to turn this
qualitative rigidity into an explicit common-origin lower bound strong
enough to force \(q\geq0\).

## 8. An explicit local stability estimate

The sitewise slack controls the distance of the complete local form
from the forbidden isotropic form.  The constant below is deliberately
elementary rather than optimized.

Let \({\mathscr H}_i:M_3\to M_3\) represent \(h_i\):
\[
 h_i(A,B)=\langle A,{\mathscr H}_i(B)\rangle_{\rm HS}.
 \tag{64}
\]

### Theorem 9 (quantitative isotropy)

For every normalized rank-at-most-two \(C\), put \(q=Q_3(C)\).
Then
\[
\boxed{\qquad
 \left\|
 {\mathscr H}_i+\frac{2q}{3}{\cal L}
 \right\|_{\rm op}
 \leq360\sqrt{15}\,\sqrt{g_i}.
 \qquad}
 \tag{65}
\]
Equivalently,
\[
 g_i\geq
 \frac1{1\,944\,000}
 \left\|
 {\mathscr H}_i+\frac{2q}{3}{\cal L}
 \right\|_{\rm op}^2.
 \tag{66}
\]
Here the operator norm is for the Hilbert--Schmidt structure on
\(M_3\).

### Proof

Write
\[
 A_z=I-|z\rangle\langle z|,
 \qquad
 f(z)=h_i(A_z,A_z),
 \qquad
 m={\mathbb E}_zf(z)=\frac58g_i.
 \tag{67}
\]
The boundary theorem gives \(f\geq0\).  As a function on
\(\mathbb {CP}^2\), \(f\) lies in the space of bidegree-\((2,2)\)
functions, whose complex dimension is at most
\[
 \dim\operatorname{End}(\operatorname{Sym}^2\mathbb C^3)=36.
 \tag{68}
\]
For Haar probability measure, the diagonal of the reproducing kernel
of this space is constant and equals its dimension.  Therefore
\[
 \|f\|_\infty\leq6\|f\|_2.
 \tag{69}
\]
Since \(f\geq0\),
\[
 \|f\|_2^2\leq\|f\|_\infty m.
 \]
Combining this with (69) gives the explicit bound
\[
 \boxed{\qquad \|f\|_\infty\leq36m.\qquad}
 \tag{70}
\]

Fix \(z\).  The two linear spaces
\[
 {\cal R}_z=\{B:|z\rangle\langle z|B=0\},
 \qquad
 {\cal C}_z=\{B:B|z\rangle\langle z|=0\}
 \tag{71}
\]
consist entirely of singular matrices and both contain \(A_z\).
Thus \(h_i\) restricts to a positive semidefinite form on each.
Moreover,
\[
 |h_i(B,B)|
 \leq\|B^{(i)}C\|_2^2
 \leq\|B\|_2^2,
 \tag{72}
\]
because the endpoint superoperator has operator norm one.
Positive-form Cauchy--Schwarz therefore gives
\[
 |h_i(B,A_z)|\leq\|B\|_2\sqrt{f(z)}
 \quad(B\in{\cal R}_z\text{ or }B\in{\cal C}_z).
 \tag{73}
\]

The tangent hyperplane to the determinant hypersurface at \(A_z\) is
\[
 {\cal T}_z=\{B:z^\dagger Bz=0\}.
 \tag{74}
\]
Every \(B\in{\cal T}_z\) is an orthogonal sum of one member of
\({\cal R}_z\) and one member of \({\cal C}_z\).  Hence (73) implies
\[
 |h_i(B,A_z)|
 \leq\sqrt2\,\|B\|_2\sqrt{f(z)}
 \quad(B\in{\cal T}_z).
 \tag{75}
\]
The Hilbert--Schmidt orthogonal complement of \({\cal T}_z\) is
\(\mathbb C|z\rangle\langle z|\).  Equations (70) and (75) consequently
give scalars \(\lambda_z\) and errors \(e_z\) such that
\[
\begin{aligned}
 {\mathscr H}_i(A_z)
 &=\lambda_z|z\rangle\langle z|+e_z,\\
 \|e_z\|_2&\leq\varepsilon,
 \qquad
 \varepsilon:=\sqrt{72m}.
\end{aligned}
 \tag{76}
\]

Put \(K={\mathscr H}_i(I)\).  For every orthonormal basis
\((z_1,z_2,z_3)\), summing (76) and using
\(\sum_aA_{z_a}=2I\) gives
\[
 2K=\sum_a\lambda_{z_a}|z_a\rangle\langle z_a|+E,
 \qquad \|E\|_2\leq3\varepsilon.
 \tag{77}
\]
Thus, for every orthogonal pair of unit vectors \(x,y\),
\[
 |x^\dagger Ky|\leq\frac32\varepsilon.
 \tag{78}
\]
An elementary two-vector rotation now makes \(K\) nearly scalar.
Indeed, in a fixed basis (78) bounds every off-diagonal entry by
\(\delta=3\varepsilon/2\).  Applying it also to
\((e_a+e_b)/\sqrt2,(e_a-e_b)/\sqrt2\) bounds every diagonal
difference by \(4\delta\).  Therefore, with
\[
 \kappa=\frac{\operatorname{Tr}K}{3}=\frac q3,
 \tag{79}
\]
one has
\[
 \|K-\kappa I\|_2\leq8\delta=12\varepsilon.
 \tag{80}
\]
Taking the \(z\)-diagonal entry in (77), with a basis containing \(z\),
then yields
\[
 |\lambda_z-2\kappa|\leq27\varepsilon.
 \tag{81}
\]
Equations (76), (80), and (81) give, for every rank-one projection
\(P_z\),
\[
 \left\|
 {\mathscr H}_i(P_z)-\kappa(I-2P_z)
 \right\|_2
 \leq40\varepsilon.
 \tag{82}
\]

Finally, rank-one projections linearly span \(M_3\).  The diagonal
matrix units are themselves projections.  For \(a\ne b\), the standard
four-projection polarization writes \(E_{ab}\) as one half of a sum
of four signed rank-one projections.  Hence (82) bounds the error on
diagonal matrix units by \(40\varepsilon\) and on off-diagonal units
by \(80\varepsilon\).  Taking the Hilbert--Schmidt norm of the
superoperator gives
\[
 \left\|
 {\mathscr H}_i-\kappa(\operatorname{Tr}(\,\cdot\,)I
 -2\,\operatorname{id})
 \right\|_{\rm op}
 \leq120\sqrt3\,\varepsilon.
 \tag{83}
\]
Since
\[
 \kappa(\operatorname{Tr}(A)I-2A)
 =-\frac{2q}{3}{\cal L}(A),
 \tag{84}
\]
and
\[
 120\sqrt3\,\sqrt{72m}
 =360\sqrt{15}\,\sqrt{g_i},
 \tag{85}
\]
equation (83) is (65).  Squaring gives (66). \(\square\)

The estimate is local and dimension-specific, but it is fully
effective: any negative witness with small \(g_i\) must have its
entire \(9\times9\) local-filter form close to the one-site isotropic
boundary form.  The next missing step is a quantitative version of
the common-factor contradiction in Sections 4--6 which converts the
three local anisotropy distances into a lower bound incompatible with
the sector identity
\[
 \sum_i g_i
 =\frac13-\frac34w_1+\frac83q.
 \tag{86}
\]

The coefficient inversion in Proposition 1 makes this stability
visible directly in the common block Gram.  For an arbitrary local
form matrix \(K_{ra,tb}\), the inverse of (8) is
\[
\boxed{
\begin{aligned}
 G_{ab}&=\frac25\sum_sK_{sa,sb},\\
 \beta_{ar,bt}
 &=\frac45\delta_{rt}\sum_sK_{sa,sb}-2K_{ra,tb}.
\end{aligned}}
 \tag{87}
\]
Indeed, summing \(K_{ra,rb}=G_{ab}-\beta_{ar,br}/2\) over \(r\)
gives \(5G_{ab}/2\), and substitution gives the second line.

For the Frobenius norms of the two \(9\times9\) coefficient arrays,
(87) implies
\[
 \|\Delta\beta\|_2\leq\frac{22}{5}\|\Delta K\|_2.
 \tag{88}
\]
To see this, Cauchy--Schwarz gives
\[
 \left\|\sum_s\Delta K_{sa,sb}\right\|_{a,b}^2
 \leq3\|\Delta K\|_2^2;
\]
the two terms in the second line of (87) then have norms at most
\(12\|\Delta K\|_2/5\) and \(2\|\Delta K\|_2\).

Since a \(9\times9\) operator has Frobenius norm at most three times
its operator norm, Theorem 9 yields the explicit block-Gram estimate
\[
\boxed{\quad
 \left(
 \sum_{a,p,b,q}
 \left|
 {\cal B}_2(C_{ap},C_{bq})
 -\gamma\delta_{ap}\delta_{bq}
 \right|^2
 \right)^{1/2}
 \leq4752\sqrt{15}\,\sqrt{g_i},
 \quad
 \gamma=-\frac{2q}{3}.
 \quad}
 \tag{89}
\]
Thus strict Haar slack is quantitatively equivalent, up to explicit
constants in one direction, to failure of the rank-one block-Gram
collapse.  In particular, for fixed \(r\), the \(2\times2\) Gram
matrix indexed by \(p,q\ne r\) has norm at most the right side of
(89).  The exact remaining stability lemma is to convert these three
simultaneous near-kernel pairs into a lower bound for the local-support
determinants of the common singular plane.

At a stationary point, Theorem 9 immediately sees marginal
nonuniformity.

### Corollary 10 (critical marginal anisotropy)

Suppose \(C\) is stationary under left and right local filters and
\[
 q=-\delta<0.
 \tag{90}
\]
For the normalized one-site densities
\[
 \rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger),
 \qquad
 \rho_i^R=\operatorname{Tr}_{\widehat i}(C^\dagger C),
 \tag{91}
\]
one has
\[
\boxed{
\begin{aligned}
 g_i&\geq
 \frac{\delta^2}{5\,832\,000}
 \left\|\rho_i^L-\frac13I\right\|_2^2,\\
 g_i&\geq
 \frac{\delta^2}{5\,832\,000}
 \left\|\rho_i^R-\frac13I\right\|_2^2.
\end{aligned}}
 \tag{92}
\]

### Proof

Stationarity gives
\[
 h_i(A,I)=q\,\operatorname{Tr}(A^\dagger\rho_i^L).
 \tag{93}
\]
Therefore, for
\[
 \Delta_i={\mathscr H}_i+\frac{2q}{3}{\cal L},
 \]
the identity \({\cal L}(I)=-I/2\) gives
\[
 \Delta_i(I)=q\left(\rho_i^L-\frac13I\right).
 \tag{94}
\]
Since \(\|I\|_2=\sqrt3\),
\[
 \|\Delta_i\|_{\rm op}
 \geq\frac{\delta}{\sqrt3}
 \left\|\rho_i^L-\frac13I\right\|_2.
 \tag{95}
\]
Insert (95) in (66).  The right-filter proof is identical. \(\square\)

Thus the only branch on which the explicit stability estimate can be
small at fixed negative depth is simultaneously close to the six
maximally mixed one-site marginals.  The marginal floor
\[
 \rho_i^{L,R}\succeq
 \frac{\delta}{1+2\delta}I
 \tag{96}
\]
at a negative global minimizer prevents degeneration in the opposite
direction.  The remaining quantitative common-factor problem is
therefore confined to a compact, well-conditioned, near-uniform
marginal region.
