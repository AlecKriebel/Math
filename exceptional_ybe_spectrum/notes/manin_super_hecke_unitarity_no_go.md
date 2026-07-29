# The balanced Manin super-Hecke symmetry is not locally unitarizable

**Date:** 2026-07-29
**Scope:** the standard one-parameter \(GL(r|s)\) Manin Hecke symmetry,
including its local-basis conjugates
**Status:** exact ansatz-level exclusion; not a statement about arbitrary
exceptional solutions or multiparameter super-Hecke symmetries

## 1. Convention

Let

\[
V=V_{\bar 0}\oplus V_{\bar 1},\qquad
\dim V_{\bar 0}=r,\quad \dim V_{\bar 1}=s,
\]

and choose an ordered homogeneous basis \(e_1,\ldots,e_{r+s}\), with the
even vectors first.  Write \(p_i\in\{0,1\}\) for the parity of \(e_i\) and

\[
\epsilon_{ij}=(-1)^{p_ip_j}.
\]

Fix \(t\in\mathbb C^\times\) and put \(q=t^2\).  The normalization relevant
to the exceptional class is the operator \(T=T_{r|s}(t)\) defined by

\[
T(e_i\otimes e_j)=
\begin{cases}
q\,e_i\otimes e_i,&i=j,\ p_i=0,\\
-e_i\otimes e_i,&i=j,\ p_i=1,\\
(q-1)e_i\otimes e_j+\epsilon_{ij}t\,e_j\otimes e_i,
   &i<j,\\
\epsilon_{ij}t\,e_j\otimes e_i,&i>j.
\end{cases}
\tag{1}
\]

Equivalently, \(T\) is \(t\) times the usual standard super-Hecke
symmetry whose eigenvalues are \(t\) and \(-t^{-1}\).  Thus its eigenvalues
are \(q\) and \(-1\), exactly in the convention

\[
(T+I)(T-qI)=0.
\tag{2}
\]

This normalization is worth fixing explicitly.  Older sources use both
\(\{t,-t^{-1}\}\) and \(\{q,-1\}\), and at least one commonly cited
display does not transparently match the Hecke polynomial printed beside
it.  No convention-dependent formula is used below without a direct
check.

## 2. Ordinary braid and Hecke relations

This is an ordinary operator in \(\operatorname{End}(V\otimes V)\).  Its
super signs are already included in (1); its placements on three tensor
factors are the ordinary matrices \(T\otimes I\) and \(I\otimes T\).

For \(i<j\), the restriction to
\(\operatorname{span}\{e_i\otimes e_j,e_j\otimes e_i\}\) is

\[
\begin{pmatrix}
q-1&\epsilon_{ij}t\\
\epsilon_{ij}t&0
\end{pmatrix}.
\tag{3}
\]

Its trace is \(q-1\), its determinant is \(-t^2=-q\), and hence its
eigenvalues are \(q,-1\).  The one-dimensional diagonal blocks have
eigenvalue \(q\) for an even index and \(-1\) for an odd index.  This
proves (2).

For completeness, the braid relation can be checked without invoking a
graded tensor convention.  Decompose \(V^{\otimes3}\) according to the
multiset of its three basis indices.

If all three indices are distinct, conjugate the word basis by its Koszul
sign relative to the increasing word.  An adjacent exchange of \(i,j\)
then loses the factor \(\epsilon_{ij}\).  The two operators become the
standard six-dimensional regular Hecke block

\[
S_k f_w=
\begin{cases}
(q-1)f_w+t f_{ws_k},&w_k<w_{k+1},\\
t f_{ws_k},&w_k>w_{k+1}.
\end{cases}
\tag{4}
\]

After division by \(t\), (4) is the usual regular action with quadratic
roots \(t,-t^{-1}\), and direct multiplication gives
\(S_1S_2S_1=S_2S_1S_2\).

If an index \(x\) occurs twice and the other index occurs once, the same
sign conjugation gives, up to reversing the three word vectors,

\[
S_1=
\begin{pmatrix}
\lambda&0&0\\
0&q-1&t\\
0&t&0
\end{pmatrix},
\qquad
S_2=
\begin{pmatrix}
q-1&t&0\\
t&0&0\\
0&0&\lambda
\end{pmatrix},
\tag{5}
\]

where \(\lambda=q\) if \(x\) is even and \(\lambda=-1\) if \(x\) is odd.
The only potentially nonzero entry of the braid difference in (5) is

\[
(q-1)\bigl(\lambda^2-(q-1)\lambda-q\bigr)
=(q-1)(\lambda-q)(\lambda+1)=0.
\tag{6}
\]

If all indices coincide, both braid generators are the same scalar.
Equations (4)--(6) prove the ordinary braid identity

\[
(T\otimes I)(I\otimes T)(T\otimes I)
=(I\otimes T)(T\otimes I)(I\otimes T).
\tag{7}
\]

## 3. Multiplicities

Every unordered pair of distinct indices contributes one \(q\)-eigenvector
and one \((-1)\)-eigenvector.  The diagonal vectors contribute \(r\)
additional \(q\)-eigenvectors and \(s\) additional \((-1)\)-eigenvectors.
Consequently

\[
m_q=\binom{r+s}{2}+r,\qquad
m_{-1}=\binom{r+s}{2}+s.
\tag{8}
\]

For the balanced super space \(r=s\), both multiplicities are
\((r+s)^2/2\).  In particular, \(T_{3|3}(e^{i\pi/6})\) is a \(36\times36\)
ordinary braid matrix satisfying the correct Hecke polynomial and having
eighteen copies of each eigenvalue.  Algebraically it is therefore an
obvious candidate for the unresolved \(d=6\) class.

## 4. Positive-local-metric obstruction

The candidate is nevertheless not in the unitary class, even after an
arbitrary local change of basis.

### Proposition

Let \(r,s>0\),

\[
t^2=q=e^{i\pi/3},
\]

and let \(T=T_{r|s}(t)\).  There is no positive-definite Hermitian
\(G\in\operatorname{End}(V)\) such that

\[
T^*(G\otimes G)T=G\otimes G.
\tag{9}
\]

Therefore no local conjugate
\((S\otimes S)T(S\otimes S)^{-1}\) is unitary.

### Proof

If (9) held, eigenspaces of \(T\) for the two distinct unit-modulus
eigenvalues \(q\) and \(-1\) would be orthogonal in the product inner
product induced by \(G\).

Take an even index \(i\) and an odd index \(a\).  The vectors

\[
e_i\otimes e_i,\qquad e_a\otimes e_a
\]

have eigenvalues \(q\) and \(-1\), respectively.  Their orthogonality says

\[
0=\langle e_i\otimes e_i,e_a\otimes e_a\rangle_{G\otimes G}
=G_{ia}^{\,2},
\]

so \(G_{ia}=0\).  Hence \(V_{\bar0}\perp_GV_{\bar1}\).

Put

\[
x=e_i\otimes e_a,\qquad y=e_a\otimes e_i.
\]

It follows that \(x\perp_{G\otimes G}y\), while

\[
\|x\|_{G\otimes G}^2
=\|y\|_{G\otimes G}^2
=G_{ii}G_{aa}=:c>0.
\tag{10}
\]

Since the even basis vectors precede the odd ones, (1) gives

\[
w_q=tx+y,\qquad w_-=x-ty,
\]

with

\[
Tw_q=qw_q,\qquad Tw_-=-w_-.
\]

But (10) yields

\[
\langle w_q,w_-\rangle_{G\otimes G}
=(\overline t-t)c.
\tag{11}
\]

For either square root of \(e^{i\pi/3}\), \(t\) is nonreal, so (11) is
nonzero.  This contradicts orthogonality of the two eigenspaces.
\(\square\)

The same conclusion holds for the common opposite and inverse
normalizations: tensor flip commutes with \(G\otimes G\), and multiplying
the inverse by a phase preserves \(G\)-unitarity if and only if the
original operator does.

## 5. Consequence and limitation

The standard balanced Manin \(GL(s|s)\) family does **not** provide
exceptional unitary solutions in any even dimension, including \(d=6\).
The obstruction is not a failure of the ordinary braid or Hecke
relations; it is exactly the incompatibility of the \(q\)- and
\((-1)\)-eigenvectors with every tensor-square positive metric.

This excludes only the explicit one-parameter symmetry (1) and its local
basis conjugates.  It does not exclude multiparameter super-Hecke
symmetries, nonlocal twists that are separately proved to preserve the
ordinary Yang--Baxter placement, or arbitrary \(d=6\) solutions.

## 6. Orthogonalized eigenspace near miss

There is a natural way to turn the nonnormal Manin operator into a point
of the ordinary Grassmann search space: take the orthogonal projection
\(P_{\mathrm{orth}}\) onto its \((-1)\)-eigenspace in the standard
positive inner product and put

\[
H_{\mathrm{orth}}=I-2P_{\mathrm{orth}}.
\]

For \(r=s=3\), the eighteen normalized spanning vectors have disjoint
supports:

\[
e_a\otimes e_a\quad (a\text{ odd}),\qquad
\frac{e_i\otimes e_j-t\,e_j\otimes e_i}{\sqrt2}\quad (i<j).
\]

Consequently \(P_{\mathrm{orth}}\) is an exact rank-eighteen orthogonal
projection and \(H_{\mathrm{orth}}\) is a trace-zero Hermitian
involution.  It is nevertheless far from the exceptional locus.  Exact
arithmetic gives

\[
\left\|
(H_{\mathrm{orth}})_1(H_{\mathrm{orth}})_2(H_{\mathrm{orth}})_1
-(H_{\mathrm{orth}})_2(H_{\mathrm{orth}})_1(H_{\mathrm{orth}})_2
-\frac13\bigl((H_{\mathrm{orth}})_1-(H_{\mathrm{orth}})_2\bigr)
\right\|_{\mathrm{HS}}^2
=\frac{140}{3},
\tag{12}
\]

and each partial trace has squared distance \(6\) from the scalar
subspace.

Sixteen predeclared unrestricted complex Grassmann runs were initialized
by small seed-dependent perturbations of this point.  Eight minimized the
cubic residual alone and eight also penalized both nonscalar partial
traces.  Every run returned numerically to the same exact values:

\[
\frac{140}{3}
\quad\text{and}\quad
\frac{140}{3}+6+6=\frac{176}{3},
\]

respectively.  This is only a calibrated negative search result, not a
local-minimum proof and not evidence of global nonexistence.  The exact
calculation in (12), rather than optimizer convergence, certifies the
identified near miss.

## 7. Source normalization audit

- P. H. Hai, *On the representation categories of matrix quantum groups
  of type A*, arXiv:math/0502399, equations (1)--(4), records the ordinary
  braid and Hecke conventions and the standard Manin super family.
- D. Gurevich et al., *KZ equations and Bethe subalgebras in generalized
  Yangians related to compatible \(R\)-matrices*, J. Integrable Systems
  4 (2019), §2, displays the standard \(GL(1|1)\) block with eigenvalues
  \(t,-t^{-1}\).  Multiplication by \(t\) gives (1) in the
  \(\{q,-1\}\) normalization.

The proof above is independent of those sources: it directly verifies
the polynomial, the ordinary braid placement, the multiplicities, and
the positive-metric obstruction.
