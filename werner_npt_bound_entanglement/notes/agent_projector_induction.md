# Rank-two projector induction: exact nonlinear reductions

**Research log entry — 2026-07-28 11:00–13:10 PDT**

This note works only with the endpoint form
\[
Q_n(C):=\sum_{S\subseteq[n]}\left(-\frac12\right)^{|S|}
 \left\|\operatorname{Tr}_S C\right\|_2^2
=\left\langle C,\mathcal L^{\otimes n}(C)\right\rangle ,
\qquad
\mathcal L(A)=A-\frac12\operatorname{Tr}(A)I.
\]
The target is \(Q_n(P)\geq 0\) for every orthogonal rank-two
projection \(P\) on \(H=(\mathbb C^d)^{\otimes n}\).

No all-copy proof or counterexample is obtained below.  The main outputs are:

1. an exact two-replica/parity formulation in which the nonlinear
   Plücker obstruction is isolated;
2. a complete proof of the projector theorem for \(n=2\);
3. an exact common-isometry recursion, together with a precise explanation
   of why scalar induction loses the needed constraint;
4. two stronger nonlinear induction candidates (PPT compression and a
   two-point kernel inequality);
5. an exact equality family showing that a layer-by-layer parity proof
   cannot work.

## 1. Two-replica formula

Let \(F_i\) swap the \(i\)-th factors of two replicas of \(H\), and put
\[
G_i=F_i-\frac12I,\qquad
Y_i=I-\frac12F_i.
\]
For every operator \(C\) on \(H\),
\[
\left\|\operatorname{Tr}_S C\right\|_2^2
=\operatorname{Tr}\!\left[(C^\dagger\otimes C)F_{S^c}\right].
\]
Consequently, for Hermitian \(C\),
\[
\boxed{\quad
Q_n(C)=\operatorname{Tr}\!\left[
(C\otimes C)\prod_{i=1}^n\left(F_i-\frac12I\right)
\right].
\quad}                                                     \tag{1}
\]
Indeed, expanding the product chooses \(F_i\) for \(i\notin S\) and
\(-I/2\) for \(i\in S\).

Let \(R=\prod_iF_i\), the full replica swap.  Since
\[
G_i=F_iY_i,\qquad [F_i,Y_j]=0,
\]
we also have
\[
\prod_iG_i=R\,Y^{\otimes n},\qquad Y=I-\frac12F\succeq0.   \tag{2}
\]

Now let
\[
P=VV^\dagger,\qquad V:\mathbb C^2\longrightarrow H,\qquad V^\dagger V=I_2.
\]
Define the positive \(4\times4\) compression
\[
K_n(V):=(V^\dagger\otimes V^\dagger)Y^{\otimes n}(V\otimes V)\succeq0.
\]
The isometry \(V\otimes V\) intertwines the input swap \(F_2\) with \(R\).
Equations (1)–(2) give
\[
\boxed{\quad Q_n(P)=\operatorname{Tr}\!\left(F_2K_n(V)\right).\quad} \tag{3}
\]
Thus the three-dimensional symmetric input sector contributes positively,
whereas the one-dimensional exterior input sector contributes negatively:
\[
Q_n(P)=\operatorname{Tr}_{\operatorname{Sym}^2\mathbb C^2}K_n(V)
-\left\langle\varepsilon,K_n(V)\varepsilon\right\rangle,   \tag{4}
\]
where
\[
\varepsilon=\frac{|01\rangle-|10\rangle}{\sqrt2}.
\]
The exterior output vector
\[
(V\otimes V)\varepsilon=u_1\wedge u_2
\]
is decomposable.  This is the nonlinear constraint discarded by any
relaxation which treats the two swap sectors only through their weights.

For one copy,
\[
K_1(V)=I_4-\frac12F_2
\]
for every isometry \(V\), hence \(Q_1(P)=0\).

## 2. Full local-parity distribution

Write
\[
S_i=\frac{I+F_i}{2},\qquad A_i=\frac{I-F_i}{2},
\]
and for \(T\subseteq[n]\) put
\[
\Pi_T=\bigotimes_{i\in T}A_i\bigotimes_{i\notin T}S_i,
\qquad
r_T(P)=\operatorname{Tr}\!\left[(P\otimes P)\Pi_T\right]\geq0.
\]
Because the full swap has eigenvalue \((-1)^{|T|}\) on
\(\operatorname{ran}\Pi_T\), even \(T\) see only
\(\operatorname{Sym}^2(\operatorname{ran}P)\), while odd \(T\) see only
\(\Lambda^2(\operatorname{ran}P)\).  Therefore
\[
\sum_{\substack{T\subseteq[n]\\|T|\ {\rm even}}}r_T=3,\qquad
\sum_{\substack{T\subseteq[n]\\|T|\ {\rm odd}}}r_T=1.       \tag{5}
\]
Since
\[
G_i=\frac12(S_i-3A_i),
\]
(1) becomes
\[
\boxed{\quad
Q_n(P)=2^{-n}\sum_{T\subseteq[n]}(-3)^{|T|}r_T(P).
\quad}                                                     \tag{6}
\]

Let
\[
e_k=\sum_{|T|=k}r_T\quad(k\ {\rm even}),\qquad
o_k=\sum_{|T|=k}r_T\quad(k\ {\rm odd}).
\]
Using (5) to cancel the \(k=0\) and \(k=1\) baseline terms gives the exact
identity
\[
\boxed{\quad
Q_n(P)=2^{-n}\sum_{j\geq1}(3^{2j}-1)
\bigl(e_{2j}-3o_{2j+1}\bigr),
\quad}                                                     \tag{7}
\]
where nonexistent layers are zero.

This is not itself a proof: individual brackets in (7) can be negative,
even for the simplest exact projector codes; see Section 5.

## 3. Complete \(n=2\) projector theorem

For \(n=2\), (7) reduces immediately to
\[
Q_2(P)=2e_2=2\operatorname{Tr}\!\left[(P\otimes P)A_1A_2\right]\geq0. \tag{8}
\]
This is already a manifest sum of squares, since \(A_1A_2\) is an
orthogonal projection.

For completeness, expanding (8) gives the familiar marginal-purity form.
Let
\[
a_i=\left\|\operatorname{Tr}_iP\right\|_2^2.
\]
The swap trick gives
\[
e_2=\frac14\left(
(\operatorname{Tr}P)^2-a_1-a_2+\operatorname{Tr}P^2
\right)
=\frac14(6-a_1-a_2),
\]
because \(\operatorname{Tr}P=\operatorname{Tr}P^2=2\).  Hence
\[
Q_2(P)=3-\frac12(a_1+a_2)=2e_2\geq0.                       \tag{9}
\]
Equality holds exactly when
\[
A_1A_2(P\otimes P)=0,                                     \tag{10}
\]
i.e. the two-copy code space has no component which is antisymmetric in
both local replica pairs.

Equation (8) is also a direct proof of linear-entropy subadditivity in the
special form needed here; no entropy theorem is required.

For \(n=3\), the exact next obstruction is already visible:
\[
\boxed{\quad
Q_3(P)=e_2-3o_3.
\quad}                                                     \tag{11}
\]
Thus a three-copy proof is exactly a nonlinear comparison between the
three symmetric-code companions in the ``two local antisymmetries'' sectors
and the decomposable exterior vector in the ``three local
antisymmetries'' sector.

## 4. Common-isometry block recursion

Peel the first physical factor and write
\[
V=\sum_{i=1}^d|i\rangle V_i,\qquad
V_i:\mathbb C^2\longrightarrow H',\qquad
\sum_iV_i^\dagger V_i=I_2.                                \tag{12}
\]
The blocks of \(P\) are
\[
P_{ij}=V_iV_j^\dagger.
\]
They satisfy the nonlinear projection identities
\[
\boxed{\quad
\sum_kP_{ik}P_{kj}=P_{ij}\quad\text{for every }i,j.
\quad}                                                     \tag{13}
\]
Indeed,
\[
\sum_kV_iV_k^\dagger V_kV_j^\dagger
=V_i\left(\sum_kV_k^\dagger V_k\right)V_j^\dagger
=V_iV_j^\dagger.
\]

Applying the definition of \(Q_n\) to blocks yields the exact scalar
recursion
\[
\boxed{\quad
Q_n(P)=
\sum_{i,j}Q_{n-1}(V_iV_j^\dagger)
-\frac12Q_{n-1}\!\left(\sum_iV_iV_i^\dagger\right).
\quad}                                                     \tag{14}
\]
The second argument in (14) can have rank as large as \(2d\).  Replacing
the shared family \((V_i)\) by independent rank-two blocks discards both
(12) and (13), which are precisely the common-isometry/Plücker
constraints.  Thus an induction only on ``rank at most two'' is not
closed.

A successful scalar induction would follow from the stronger invariant
\[
2\sum_{i,j}Q_m(V_iV_j^\dagger)
\ \geq\
Q_m\!\left(\sum_iV_iV_i^\dagger\right)                    \tag{15}
\]
for every common family satisfying (12), but (15) is just (14) repackaged;
it must be proved using (12)–(13), not by treating its terms separately.

## 5. Exact equality family and a failed layerwise strategy

Let
\[
u=\bigotimes_{i=1}^n|a_i\rangle,\qquad
v=\bigotimes_{i=1}^n|b_i\rangle
\]
be orthonormal product vectors such that at each site either
\(|a_i\rangle=|b_i\rangle\) or \(\langle a_i,b_i\rangle=0\).
Let \(h\) be the number of orthogonal sites, so \(h\geq1\), and put
\[
P=|u\rangle\langle u|+|v\rangle\langle v|.
\]
The parity generating polynomial is exactly
\[
\boxed{\quad
\sum_{T\subseteq[n]}r_Tz^{|T|}
=2+2^{\,1-h}(1+z)^h.
\quad}                                                     \tag{16}
\]
Proof: the two self-pairs \(u\otimes u\) and \(v\otimes v\) contribute
the constant \(2\).  The two ordered cross-pairs have only symmetric
parity on the \(n-h\) identical sites, and have the uniform parity
distribution \(2^{-h}(1+z)^h\) on the \(h\) orthogonal sites.

Evaluating (16) at \(z=-3\) and using (6) gives
\[
\boxed{\quad
Q_n(P)=2^{1-n}\bigl(1+(-1)^h\bigr).
\quad}                                                     \tag{17}
\]
Thus every odd \(h\) gives exact equality for every \(n\), while even
\(h\) gives \(Q_n(P)=2^{2-n}\).

There is a still larger equality manifold.  If \(P_2\) is any rank-two
projection on one physical factor and \(|\xi\rangle\) is an arbitrary
(possibly highly entangled) unit vector on all remaining factors, then
\[
P=P_2\otimes|\xi\rangle\langle\xi|
\]
is a rank-two projection and tensor-factorization of the quadratic form
gives
\[
Q_n(P)=Q_1(P_2)\,
Q_{n-1}(|\xi\rangle\langle\xi|)=0.                         \tag{18a}
\]
Thus equality is not confined to classical or fully product codewords;
one zero one-copy projector factor may carry an arbitrary entangled
rank-one suffix.

This family rules out two tempting proof strategies:

* there can be no uniform positive lower bound for projector witnesses;
* the brackets \(e_{2j}-3o_{2j+1}\) in (7) cannot be required to be
  individually nonnegative.

For example, for \(h=4\),
\[
e_2=\frac68,\qquad o_3=\frac48,\qquad e_4=\frac18,
\]
so \(e_2-3o_3=-3/4<0\), but the positive \(e_4\) term in (7) restores the
exact value \(Q_4(P)=1/4\).  Any parity-layer induction must therefore
allow transfer between nonadjacent weights.

## 6. Strong nonlinear candidate I: PPT compression

Partial transpose the positive compression \(K_n(V)\) on its second
input qubit.  With
\[
|\omega_d\rangle=\sum_{i=1}^d|ii\rangle,\qquad
X=I-\frac12|\omega_d\rangle\langle\omega_d|,
\]
one obtains
\[
\boxed{\quad
K_n(V)^\Gamma
=(V^\dagger\otimes V^T)X^{\otimes n}(V\otimes\overline V).
\quad}                                                     \tag{18}
\]
Moreover,
\[
Q_n(P)
=\operatorname{Tr}(F_2K_n(V))
=\langle\omega_2|K_n(V)^\Gamma|\omega_2\rangle.             \tag{19}
\]
Consequently the stronger statement
\[
K_n(V)^\Gamma\succeq0\quad\text{for every isometry }V       \tag{20}
\]
would prove the projector theorem.

At \(n=1\),
\[
K_1(V)^\Gamma=I_4-\frac12|\omega_2\rangle\langle\omega_2|
\succeq0
\]
independently of \(V\).

The exact peeling recursion for (18) exposes the obstruction to a naive
PPT induction.  With (12), set
\[
W_{ij}=V_i\otimes\overline{V_j},\qquad Z=X^{\otimes(n-1)}.
\]
Then
\[
\boxed{\quad
K_n(V)^\Gamma
=\sum_{i,j}W_{ij}^\dagger ZW_{ij}
-\frac12
\left(\sum_iW_{ii}\right)^\dagger
Z
\left(\sum_jW_{jj}\right).
\quad}                                                     \tag{21}
\]
The operator \(Z\) is indefinite.  Also, the diagonal sum
\(\sum_iW_{ii}\) need not map a vector to Schmidt rank at most two.
Therefore neither ordinary Cauchy--Schwarz nor the \((n-1)\)-copy
rank-two hypothesis applies to the second term.  A proof of (20), if
true, needs a cone which retains the entire common family \((V_i)\).

## 7. Strong nonlinear candidate II: a two-point kernel

For vectors \(u,v\in H\), define
\[
\kappa_n(u,v)
:=\left\langle u,\mathcal L^{\otimes n}
\bigl(|v\rangle\langle v|\bigr)u\right\rangle.
\]
Equivalently,
\[
\kappa_n(u,v)
=\sum_{S\subseteq[n]}\left(-\frac12\right)^{|S|}
\operatorname{Tr}\!\left[
\operatorname{Tr}_S|u\rangle\langle u|\,
\operatorname{Tr}_S|v\rangle\langle v|
\right]                                                    \tag{22}
\]
and
\[
\kappa_n(u,v)
=\langle u\otimes v,\prod_iG_i\,u\otimes v\rangle.          \tag{23}
\]
For an orthonormal code basis \(u,v\),
\[
\boxed{\quad
Q_n(P)=\kappa_n(u,u)+\kappa_n(v,v)+2\kappa_n(u,v).
\quad}                                                     \tag{24}
\]

A particularly clean sufficient invariant is
\[
\boxed{\quad
\begin{pmatrix}
\kappa_n(u,u)&\kappa_n(u,v)\\
\kappa_n(u,v)&\kappa_n(v,v)
\end{pmatrix}\succeq0
\quad\text{for all }u,v.
\quad}                                                     \tag{25}
\]
It is basis-free, genuinely nonlinear, and immediately implies (24).
Equivalently,
\[
|\kappa_n(u,v)|^2
\leq\kappa_n(u,u)\kappa_n(v,v).                            \tag{26}
\]

There are two exact positive cases.

* For \(n=1\), if
  \(t=|\langle u,v\rangle|^2/(\|u\|^2\|v\|^2)\in[0,1]\), then
  \[
  \kappa_1(u,u)=\frac12\|u\|^4,\qquad
  \kappa_1(u,v)=\|u\|^2\|v\|^2\left(t-\frac12\right),
  \]
  so (26) is exactly \(|t-\tfrac12|\leq\tfrac12\).

* If both \(u\) and \(v\) factor over the \(n\) sites, then
  \[
  \kappa_n(u,v)=
  \prod_{i=1}^n
  \left(
  |\langle u_i,v_i\rangle|^2
  -\frac12\|u_i\|^2\|v_i\|^2
  \right),
  \]
  and (26) follows by applying the one-copy bound to every factor.

The direct peeling formula again shows why (25) is not closed under a
two-point induction.  Writing
\[
u=\sum_i|i\rangle u_i,\qquad v=\sum_i|i\rangle v_i,
\]
and \(G'=\prod_{k=2}^nG_k\), one gets
\[
\begin{aligned}
\kappa_n(u,v)
={}&\sum_{i,j}
\langle u_i\otimes v_j,G'(u_j\otimes v_i)\rangle\\
&-\frac12\sum_{i,j}
\langle u_i\otimes v_j,G'(u_i\otimes v_j)\rangle .
\end{aligned}                                               \tag{27}
\]
The first line contains a polarized four-vector form, not another
\(\kappa_{n-1}(x,y)\).  Thus a viable induction would have to control the
full polarization
\[
\mathfrak B_m(a,b;c,d)
=\langle a\otimes b,G^{\otimes m}(c\otimes d)\rangle
\]
on the common block family, together with its Plücker relations.

Discovery-only local optimization for real isometries through \(n=5\)
did not find a violation of either the projector inequality or (26), but
this is not evidence for an all-copy theorem and is not used above.

## 8. Most useful next targets

The calculations above reduce the nonlinear work to three sharply stated
possibilities.

1. Prove the four-linear Cauchy inequality needed to close (27), thereby
   establishing (25).
2. Prove that the cone \(K^\Gamma\succeq0\) is preserved by the
   common-family recursion (21).  Any such proof must use
   \(\sum_iV_i^\dagger V_i=I_2\) before separating the \(i,j\) terms.
3. Work directly with the parity polynomial in (6), but permit
   cancellations across weights as forced by (16).  The first genuinely
   new inequality is the three-copy Plücker comparison (11).

The exact product-code family (16) should be used as a mandatory equality
test for every proposed invariant: odd Hamming distance must remain on the
boundary at every copy number.

## 9. Even-reduction identity and an exact obstruction

**Addendum — 2026-07-28 13:25 PDT.**

Define the local reduction superoperators
\[
\mathcal R_i(H)=\operatorname{Tr}_i(H)\otimes I_i-H.
\]
Then
\[
\mathcal L_i=\frac12(\mathrm{Id}-\mathcal R_i).
\]
If \(\mathcal L_{\rm group}(H)=H-\frac12\operatorname{Tr}(H)I_H\),
the elementary even-subset expansion gives
\[
\boxed{\quad
\mathcal L^{\otimes n}-2^{1-n}\mathcal L_{\rm group}
=2^{1-n}
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even},\ |S|\geq2}}
\mathcal R_S,\qquad
\mathcal R_S=\prod_{i\in S}\mathcal R_i.
\quad}                                                     \tag{28}
\]
Proof: since \(I+\mathcal R_i=\mathcal T_i\), where
\(\mathcal T_i(H)=\operatorname{Tr}_i(H)\otimes I_i\), and
\(I-\mathcal R_i=2\mathcal L_i\),
\[
\sum_{|S|\ {\rm even}}\mathcal R_S
=\frac12\left(\prod_i(I+\mathcal R_i)+
\prod_i(I-\mathcal R_i)\right)
=\frac12\mathcal T_{[n]}+2^{n-1}\mathcal L^{\otimes n}.
\]
Subtracting the empty subset and rearranging gives (28).

For a rank-two projection,
\[
\langle P,\mathcal L_{\rm group}(P)\rangle
=\langle P,P-I\rangle=0,
\]
and hence
\[
\boxed{\quad
Q_n(P)=2^{1-n}
\sum_{\substack{S\subseteq[n]\\|S|\ {\rm even},\ |S|\geq2}}
\langle P,\mathcal R_S(P)\rangle.
\quad}                                                     \tag{29}
\]

The individual summands in (29) are not nonnegative.  There is a minimal
exact counterexample already at \(n=3\).  Let \(Q\) be a rank-two local
projection on the first site and let
\[
|\phi\rangle_{23}=\frac{|00\rangle+|11\rangle}{\sqrt2},
\qquad
P=Q_1\otimes|\phi\rangle\langle\phi|_{23}.
\]
This is a rank-two orthogonal projection (and it embeds into every
\(d\geq2\)).  Since the quadratic form factorizes over tensor factors,
\[
\begin{aligned}
\langle P,\mathcal R_1\mathcal R_2(P)\rangle
&=\langle Q,\mathcal R(Q)\rangle\,
  \langle\phi,(\mathcal R\otimes\mathrm{Id})
  (|\phi\rangle\langle\phi|)\phi\rangle
=2\left(\frac12-1\right)=-1,\\
\langle P,\mathcal R_1\mathcal R_3(P)\rangle&=-1,\\
\langle P,\mathcal R_2\mathcal R_3(P)\rangle&=2.
\end{aligned}                                               \tag{30}
\]
Here
\[
\langle Q,\mathcal R(Q)\rangle
=(\operatorname{Tr}Q)^2-\operatorname{Tr}Q^2=2,
\]
and the Bell vector has one-party reduced purity \(1/2\).
Thus the three even-reduction terms are \((-1,-1,2)\): only their cyclic
sum is nonnegative, and in fact it is zero.

The connection to the parity variables is also exact.  For even \(S\),
\[
\boxed{\quad
\langle P,\mathcal R_S(P)\rangle
=2^{|S|}\sum_{T\supseteq S}(-1)^{|T|}r_T(P).
\quad}                                                     \tag{31}
\]
To prove (31), use
\[
\langle P,\mathcal T_U(P)\rangle
=\operatorname{Tr}\!\left[(P\otimes P)F_{U^c}\right]
\]
and expand \(\prod_{i\in S}(\mathcal T_i-I)\).  Equivalently,
\[
\langle P,\mathcal R_S(P)\rangle
=(-2)^{|S|}
\operatorname{Tr}\!\left[(P\otimes P)R A_S\right],
\]
which has the sign shown in (31) when \(|S|\) is even.

For \(n=3\), (29) is the single cyclic inequality
\[
\langle P,\mathcal R_1\mathcal R_2(P)\rangle+
\langle P,\mathcal R_1\mathcal R_3(P)\rangle+
\langle P,\mathcal R_2\mathcal R_3(P)\rangle\geq0.          \tag{32}
\]
Writing \(P=VIV^\dagger\) and
\[
E_a=V\sigma_aV^\dagger,\qquad a=1,2,3,
\]
purification/complementarity reduces (32) to the following equivalent
logical-information inequality:
\[
\boxed{\quad
\sum_{i=1}^3\sum_{a=1}^3
\left\|\operatorname{Tr}_{[3]\setminus\{i\}}E_a\right\|_2^2
\leq 6.
\quad}                                                     \tag{33}
\]
Indeed, purify \(P/2\) by a logical qubit \(R\).  Expanding the \(Ri\)
marginal in the Pauli basis gives
\[
\operatorname{Tr}\rho_{Ri}^2
=\frac18\sum_{\mu=0}^3
\left\|\operatorname{Tr}_{\bar i}E_\mu\right\|_2^2,
\qquad E_0=P,
\]
while
\[
\operatorname{Tr}\rho_i^2=\frac14
\left\|\operatorname{Tr}_{\bar i}P\right\|_2^2.
\]
Substitution into (32) cancels the \(E_0\) terms and yields (33).
Thus even the three-copy case can be viewed as a sharp
``no simultaneous broadcasting of all three logical Pauli directions''
bound.  The example (30) saturates it.  A direct proof of (33) would be a
genuine nonlinear advance; it does not follow by bounding the three
reduction terms separately.
