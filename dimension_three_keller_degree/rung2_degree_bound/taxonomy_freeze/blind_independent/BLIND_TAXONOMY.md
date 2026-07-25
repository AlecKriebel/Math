# Blind independent taxonomy of quartic leading maps in dimension three

**Status.** Proposed exhaustive candidate taxonomy, derived independently from
the statement of the problem. No exclusions from the lower Keller identities
are attempted.

## 1. Scope and equivalence

Let
\[
 F=L+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
 \mathbb A^3_{\mathbb C},\qquad F(0)=0,
\]
where \(H_i\) is homogeneous of degree \(i\). For a Keller map,
\(\det JF\in\mathbb C^\times\), so \(L\in \mathrm{GL}_3(\mathbb C)\).
The degree-nine part of the determinant identity is
\[
                         \det JH_4=0.                 \tag{1}
\]
This document classifies all homogeneous quartic triples satisfying (1).
They are **leading-term candidates**. A row is not asserted to extend to a
Keller map: extension requires solving all the lower homogeneous determinant
identities involving \(L,H_2,H_3\).

The principal equivalence used here is left-right linear equivalence
\[
 H(x)\sim T\,H(S^{-1}x),\qquad
 S\in\mathrm{GL}_3(\mathbb C)_{\rm source},\quad
 T\in\mathrm{GL}_3(\mathbb C)_{\rm target}.            \tag{2}
\]
It is the equivalence naturally inherited before fixing \(L\), and it
preserves the Keller condition up to multiplication of its nonzero constant
Jacobian. If one first normalizes \(L=I\), the residual action is the finer
conjugacy action \(H(x)\mapsto S^{-1}H(Sx)\). The discrete taxonomy below
remains complete for that finer action, but the orbit counts labelled
"finite" below refer to the coarser action (2).

Write
\[
 R=\mathbb C[x_0,x_1,x_2],\qquad
 r(H)=\operatorname{rank}_{\mathbb C(x_0,x_1,x_2)}JH.
\]
The Jacobian criterion in characteristic zero identifies \(r(H)\) with
\(\operatorname{trdeg}_{\mathbb C}\mathbb C(H_0,H_1,H_2)\). Equation (1)
gives \(r(H_4)\leq 2\).

For an exact degree-four map \(H_4\neq0\), so only ranks one and two occur.
Rank zero is nevertheless recorded as the unique coefficient-space boundary.

## 2. The complete rank split

### 2.1 Rank zero: `Q4-R0-Z`

A homogeneous positive-degree polynomial with zero gradient is zero in
characteristic zero. Hence
\[
 r(H_4)=0\quad\Longleftrightarrow\quad H_4=0.
\]
This is a single orbit. It is not present when the total degree is required to
be exactly four, but it is needed in the closure of the degree-at-most-four
coefficient space.

### 2.2 Rank one/projective point: `Q4-R1-POINT`

Every nonzero rank-one quartic triple is
\[
                         H_4=c\,f,                     \tag{3}
\]
where \(0\neq c\in\mathbb C^3\) is a constant target vector and
\(0\neq f\in R_4\).

Indeed, the affine image closure is an irreducible one-dimensional cone.
Its projectivization has dimension zero, hence is one point; consequently all
three components are constant multiples of one quartic. Conversely (3) has
Jacobian rank one. Target equivalence sends \(c\) to \((1,0,0)\), leaving the
orbit problem of a ternary quartic \(f\) under source \(\mathrm{PGL}_3\).

In the gcd bookkeeping this is the formal endpoint \(e=4,b=0\): the
projective image has degree zero, the pencil is absent, and \(\nu\) is
undefined. It must not be forced into the positive-\(b\) identity
\(b=\delta\nu\).

This is a genuine moduli problem. Its generic smooth-plane-quartic quotient
has dimension \(14-8=6\), and the row includes every singular, reducible, and
nonreduced quartic.

A stable refinement syntax is
\[
 \texttt{Q4-R1-FAC[(d1,m1);...;(dk,mk)]},
\]
where \(f=\prod_j f_j^{m_j}\), the \(f_j\) are distinct irreducible ternary
forms, and \(\sum_jm_jd_j=4\). Concretely, its coarse factor types are:

1. an irreducible quartic;
2. an irreducible cubic times a line;
3. two distinct irreducible conics;
4. the square of an irreducible conic;
5. an irreducible conic times a double line;
6. an irreducible conic times two distinct lines;
7. \(l^4\);
8. \(l^3m\);
9. \(l^2m^2\);
10. \(l^2mn\);
11. four distinct lines.

Here letters denoting different lines are distinct. Singularities of the
irreducible factors and all incidences among distinct factors are further
orbit strata, not exclusions.

### 2.3 Rank two/projective curve

The rank-two case has the form
\[
                  H_4=h\,A(p,q),                       \tag{4}
\]
with the following exact conventions.

* \(h=\gcd(H_{4,0},H_{4,1},H_{4,2})\), up to a nonzero scalar, is homogeneous
  of degree \(e\).
* \(p,q\in R_a\) are linearly independent and coprime.
* \(A=(A_0,A_1,A_2)\) is a triple of binary degree-\(b\) forms with no common
  projective zero. Zero target coordinates and one linear relation among the
  coordinates are allowed. Its span has dimension at least two; span one
  would have a positive-degree common binary factor and belongs to rank one
  after gcd extraction.
* The pencil degree \(a\) is the **least positive common degree among all
  factorizations of the primitive triple \(H_4/h\) of this form**.
* The morphism
  \[
       \alpha_A:\mathbb P^1\longrightarrow\mathbb P^2,\qquad
       [s:t]\longmapsto[A_0(s,t):A_1(s,t):A_2(s,t)]
  \]
  has image degree \(\delta\) and generic cover degree \(\nu\).

Then
\[
                    e+ab=4,\qquad b=\delta\nu.          \tag{5}
\]
The word "minimal" is fixed to mean least \(a\) as above. A different intended
meaning of "minimal pencil" would change the allocation of composite rows.

No coprimality between \(h\) and either \(p\) or \(q\) is imposed. The form
\(h\) may be reducible or nonreduced, and the complete intersection
\(\{p=q=0\}\subset\mathbb P^2\) may be nonreduced. Those cases are essential.

## 3. Why the binary factorization is complete

This section proves existence of (4); it is not an exclusion argument.

Let \(h\) be the component gcd and put \(G=H_4/h\), of degree
\(m=4-e\). Thus \(\gcd(G_0,G_1,G_2)=1\). Rank two and homogeneity imply that
the rational projective map
\[
 \psi_G:\mathbb P^2\dashrightarrow\mathbb P^2,\qquad
 [x]\longmapsto[G_0(x):G_1(x):G_2(x)]
\]
has one-dimensional image. Let \(C\) be its reduced image curve.

The curve \(C\) is rational. For example, restrict \(\psi_G\) to a general
line in \(\mathbb P^2\) not contained in a fiber. This gives a nonconstant
rational map \(\mathbb P^1\dashrightarrow C\), so the normalization of \(C\)
is \(\mathbb P^1\). Let
\[
 \eta:\mathbb P^1\longrightarrow C\hookrightarrow\mathbb P^2
\]
be the normalization map. It is given by a basepoint-free binary triple
\(B=(B_0,B_1,B_2)\) of degree \(\deg C=\delta\).

The lift of \(\psi_G\) to the normalization is a rational map
\(\theta:\mathbb P^2\dashrightarrow\mathbb P^1\). Write
\(\theta=[p_0:q_0]\) with coprime homogeneous forms of a common degree \(a_0\).
Projectively,
\[
             [G_0:G_1:G_2]=[B_0(p_0,q_0):B_1(p_0,q_0):B_2(p_0,q_0)].
\]
The substituted triple \(B(p_0,q_0)\) is primitive: if an irreducible source
factor divided every component, then over its fraction field either \(p_0,q_0\)
would both vanish or \([p_0:q_0]\) would be a base point of \(B\). The first
contradicts \(\gcd(p_0,q_0)=1\), and the second contradicts basepoint-freeness.

Two primitive triples over the UFD \(R\) that define the same projective
rational map differ by a unit. Therefore
\[
                         G=c\,B(p_0,q_0)
\]
for \(c\in\mathbb C^\times\), and comparison of degrees gives
\[
                         m=a_0\delta.                  \tag{6}
\]
Thus at least one factorization exists.

Choose among all such factorizations one with least positive pencil degree
\(a\), and call the outer degree \(b=m/a\). The morphism \(\alpha_A\) factors
through the normalization \(\eta\) by a finite self-map of \(\mathbb P^1\) of
degree \(\nu\). Pulling back a line in \(\mathbb P^2\) gives
\[
                         b=\delta\nu,
\]
which proves (5).

There is one deliberate theorem gap: this argument proves existence of a
least degree \(a\), but it does **not** prove that the least-degree pencil
\(\langle p,q\rangle\) is unique up to \(\mathrm{PGL}_2\). Distinct
least-degree intermediate rational subfields could in principle give multiple
presentations of one \(H_4\). Accordingly, the five numerical invariants
\((e,a,b,\delta,\nu)\) are canonical after minimizing \(a\), while any finer
"source-pencil orbit" label below is a presentation label unless a separate
uniqueness theorem is supplied. Completeness is unaffected: at least one
minimal presentation always exists.

## 4. The thirteen numerical rank-two rows

Solving \(e+ab=4\) with \(0\leq e\leq3\), \(a,b\geq1\), and then
\(b=\delta\nu\), gives exactly the following thirteen rows. These are all
possibilities, not just generic ones.

| stable proposed ID | \(e\) | \(a\) | \(b\) | \(\delta\) | \(\nu\) | quotient character |
|---|---:|---:|---:|---:|---:|---|
| `Q4-R2-E0-A1-B4-D1-N4` | 0 | 1 | 4 | 1 | 4 | moduli: degree-4 covers of a line |
| `Q4-R2-E0-A1-B4-D2-N2` | 0 | 1 | 4 | 2 | 2 | finite: one orbit |
| `Q4-R2-E0-A1-B4-D4-N1` | 0 | 1 | 4 | 4 | 1 | moduli: rational plane quartics |
| `Q4-R2-E0-A2-B2-D1-N2` | 0 | 2 | 2 | 1 | 2 | coupled orbit problem; generic dimension 2 |
| `Q4-R2-E0-A2-B2-D2-N1` | 0 | 2 | 2 | 2 | 1 | finite: conic-pencil canonical types |
| `Q4-R2-E0-A4-B1-D1-N1` | 0 | 4 | 1 | 1 | 1 | moduli: primitive quartic pencils |
| `Q4-R2-E1-A1-B3-D1-N3` | 1 | 1 | 3 | 1 | 3 | moduli: generic dimensions 1 (`OFF`) and 2 (`ON`) |
| `Q4-R2-E1-A1-B3-D3-N1` | 1 | 1 | 3 | 3 | 1 | mixed: finite `OFF`, marked-cubic moduli `ON` |
| `Q4-R2-E1-A3-B1-D1-N1` | 1 | 3 | 1 | 1 | 1 | moduli: a line and a primitive cubic pencil |
| `Q4-R2-E2-A1-B2-D1-N2` | 2 | 1 | 2 | 1 | 2 | coupled orbit problem; generic dimension 1 |
| `Q4-R2-E2-A1-B2-D2-N1` | 2 | 1 | 2 | 2 | 1 | finite: seven source incidences, unique outer type |
| `Q4-R2-E2-A2-B1-D1-N1` | 2 | 2 | 1 | 1 | 1 | moduli: a conic and a primitive conic pencil |
| `Q4-R2-E3-A1-B1-D1-N1` | 3 | 1 | 1 | 1 | 1 | moduli: a cubic and a linear pencil |

The count is
\[
 (3+2+1)+(2+1)+(2+1)+(1)=13
\]
for \(e=0,1,2,3\), respectively.

The word "finite" means finitely many left-right orbits of the **combined**
map, not merely that the source datum and the outer map separately have finite
quotients. This distinction matters: an embedded pencil can mark the
parameter line, so the two quotients generally cannot be multiplied. All
finite degenerations listed below remain separate subtypes.

## 5. Complete outer-map strata for \(b\leq4\)

Changing the basis of an abstract source pencil acts on \(A\) by
\(\mathrm{PGL}_2\); target equivalence acts by \(\mathrm{PGL}_3\).
The following is the full outer-map menu **in isolation**. Section 6 explains
the coupled quotient: once the pencil is embedded in ternary forms, only
parameter automorphisms induced by its source stabilizer act on the intrinsic
outer subspace.

### 5.1 Degree \(b=1\)

There is one type:
\[
                    A=(s,t,0),\qquad(\delta,\nu)=(1,1).
\]

### 5.2 Degree \(b=2\)

There are two types, both single orbits:
\[
\begin{array}{c|c|c}
(\delta,\nu)&\text{normal form}&\text{description}\\ \hline
(1,2)&(s^2,t^2,0)&\text{double cover of a line},\\
(2,1)&(s^2,st,t^2)&\text{conic embedding}.
\end{array}
\]
Every degree-two map \(\mathbb P^1\to\mathbb P^1\) is left-right equivalent
to \([s^2:t^2]\) in characteristic zero.

### 5.3 Degree \(b=3\)

For \((\delta,\nu)=(1,3)\), write
\[
                         A=(P_3,Q_3,0),\qquad\gcd(P_3,Q_3)=1.
\]
This is the Hurwitz quotient of degree-three maps
\(\mathbb P^1\to\mathbb P^1\). Its exhaustive ramification refinements are
indexed by the Riemann-Hurwitz partitions of total ramification four:

* `COV3-T2`: two totally ramified points (one orbit, represented by \(z^3\));
* `COV3-T1S2`: one total and two simple ramification points (one finite
  left-right type);
* `COV3-S4`: four simple ramification points (a one-dimensional Hurwitz
  moduli stratum, with its automorphism subloci).

For \((\delta,\nu)=(3,1)\), the image is an irreducible rational plane cubic.
Its arithmetic genus is one, so it has exactly one \(\delta\)-unit of
singularity. There are precisely two outer orbits:

* `CUBIC-NODE`;
* `CUBIC-CUSP`.

The cuspidal orbit is a boundary of the nodal family. No smooth plane cubic
belongs here because the normalization is \(\mathbb P^1\).

### 5.4 Degree \(b=4\)

For \((\delta,\nu)=(1,4)\),
\[
                         A=(P_4,Q_4,0),\qquad\gcd(P_4,Q_4)=1,
\]
and the generic quotient dimension is \(2(4)-5=3\).

To include every ramification collision without relying on a genericity
assumption, use the following finite Hurwitz index. At a branch value a
degree-four cover has one of the nontrivial cycle/ramification types
\[
\begin{array}{c|c|c}
\text{code}&\text{fiber partition}&\text{Riemann--Hurwitz contribution}\\ \hline
S&(2,1,1)&1\\
D&(2,2)&2\\
T&(3,1)&2\\
Q&(4)&3.
\end{array}
\]
A subtype is
`\(\texttt{COV4-S^s-D^d-T^t-Q^q-[Nielsen]}\)`, where
\[
                       s+2d+2t+3q=6,                  \tag{7}
\]
and `[Nielsen]` records a transitive product-one tuple in \(S_4\), modulo
simultaneous conjugacy and Hurwitz moves. Keeping exactly the admissible
tuples makes this an exhaustive finite list of ramification topologies.
Moving the branch values gives dimension
\(\max\{s+d+t+q-3,0\}\), up to finite Hurwitz maps. The generic subtype is
`COV4-S^6`, of dimension three. Codes \(D,T,Q\) record all collisions and
higher ramification boundaries.

For \((\delta,\nu)=(2,2)\), there is one orbit:
\[
                         A=(s^4,s^2t^2,t^4),
\]
the unique double cover of \(\mathbb P^1\) followed by the conic embedding.

For \((\delta,\nu)=(4,1)\), \(A\) is any basepoint-free birational net in
\(H^0(\mathbb P^1,\mathcal O(4))\). Equivalently it is a rational irreducible
plane quartic together with its normalization. The generic quotient dimension
is
\[
                  \dim\operatorname{Gr}(3,5)-\dim\mathrm{PGL}_2=6-3=3.
\]
This row includes, rather than discards, every singularity degeneration.
The genus formula gives the exhaustive constraint
\[
                \sum_{P\in\operatorname{Sing}C}\delta_P=3.       \tag{8}
\]
A stable refinement code is
`\(\texttt{P4-[local branch semigroups]-[contact matrices]}\)`, with the
local data ranging over all reduced plane-curve singularities satisfying
(8) and realizable in degree four. More explicitly, the partitions of the
total delta invariant are
\[
                           1+1+1,\qquad 2+1,\qquad 3.
\]
Reduced plane singularities with local delta at most three have the following
simple-type menu:
\[
\begin{array}{c|l}
\delta_P&\text{local analytic types}\\ \hline
1&A_1\text{ (node)},\ A_2\text{ (cusp)}\\
2&A_3\text{ (tacnode)},\ A_4\text{ (ramphoid cusp)}\\
3&A_5,\ A_6,\ D_4\text{ (ordinary triple point)},\ D_5,\ E_6.
\end{array}
\]
Consequently the possible baskets are three choices from
\(\{A_1,A_2\}\), one choice from \(\{A_3,A_4\}\) plus one from
\(\{A_1,A_2\}\), or one type from the delta-three line. These are candidate
subrows; none is deleted here on the basis of a global degree-four
realizability claim. Set-theoretically, `D4-N1` is defined by the actual
basepoint-free birational nets, so an empty candidate basket cannot create a
false map. The refinement code also remembers branch contacts,
infinitely-near data, and moduli such as positions of preimages on the
normalization. Formula (8), not the generic three-node picture, defines the
row.

The image of \(\mathbb P^1\) is irreducible and reduced, so reducible plane
quartics do not occur in `D4-N1`; reducibility appears only after a degree or
rank boundary and is then reclassified.

## 6. Source/gcd orbit data

For fixed \((e,a)\), the remaining datum is
\[
       (h,\langle p,q\rangle),\qquad
       0\neq h\in\mathbb P(R_e),\quad
       \langle p,q\rangle\in\operatorname{Gr}(2,R_a),
                                                               \tag{9}
\]
subject to \(\gcd(p,q)=1\) and least-degree minimality. This datum is taken
modulo source \(\mathrm{PGL}_3\), with pencil-basis changes coupled to
precomposition of \(A\).

The complete coarse status is:

| source code | \((e,a)\) | source quotient |
|---|---:|---|
| `SRC-01` | (0,1) | one orbit |
| `SRC-02-KS[...]` | (0,2) | finitely many symmetric-pencil Kronecker--Segre types |
| `SRC-04` | (0,4) | moduli, generic dimension \(26-8=18\) |
| `SRC-11-ON/OFF` | (1,1) | two orbits |
| `SRC-13` | (1,3) | moduli, generic dimension \(2+16-8=10\) |
| `SRC-21-[...]` | (2,1) | seven orbits |
| `SRC-22` | (2,2) | moduli, generic dimension \(5+8-8=5\) |
| `SRC-31` | (3,1) | moduli, generic dimension \(9+2-8=3\) |

These generic dimensions are dimension counts of the indicated projective
parameter spaces. Special stabilizers create lower-dimensional substacks.

The finite refinements are as follows.

* `SRC-02-KS[...]`: identify a ternary quadric with a symmetric \(3\times3\)
  matrix. A pencil is classified under congruence and pencil-coordinate
  change by its full Kronecker--Segre symbol. The symbol must include regular
  elementary divisors and any singular minimal-index blocks; retain the
  coprime symbols, with the final least-degree test applied to the coupled
  datum as in Section 6.1. There are only finitely many in size three: at most
  three generalized eigenvalues occur and
  \(\mathrm{PGL}_2\) removes their positions. This code deliberately uses the
  full canonical symbol, rather than the discriminant cubic alone, because a
  repeated root can have different Jordan/rank types. Pencils depending on
  only two linear forms are nonminimal and move to \(a=1,b=4\).

* For `SRC-11`, the linear pencil has a center point
  \(P=\{p=q=0\}\). The two types are `ON` if \(P\in\{h=0\}\), equivalently
  \(h\in\langle p,q\rangle\), and `OFF` otherwise.

* For `SRC-21`, the datum is a plane conic \(h=0\) and the center point \(P\)
  of the linear pencil. Its seven types are
  \[
  \begin{array}{c|c}
  \operatorname{rank}(h)&\text{position of }P\\ \hline
  3&\texttt{SMOOTH-ON},\ \texttt{SMOOTH-OFF}\\
  2&\texttt{PAIR-NODE},\ \texttt{PAIR-SMOOTHPOINT},\
     \texttt{PAIR-OFF}\\
  1&\texttt{DOUBLELINE-ON},\ \texttt{DOUBLELINE-OFF}.
  \end{array}
  \]
  Over \(\mathbb C\), these are the source \(\mathrm{PGL}_3\)-orbits.

All moduli source codes include every internal boundary:

* \(h\) may become singular, reducible, or nonreduced;
* the base scheme \((p=q=0)\) may collide or become nonreduced while retaining
  no common curve component;
* a member of the pencil may factor or acquire singularities;
* \(h\) may pass through base points or share factors with individual pencil
  members;
* stabilizers may jump.

None of these is a reason to delete a row.

### 6.1 The coupled quotient and the genuinely finite rows

It is useful to state the coupling precisely. Let
\(U=\langle p,q\rangle\subset R_a\). After target equivalence, the outer datum
is intrinsically a subspace
\[
                         V_A\subset\operatorname{Sym}^b U,
\]
of dimension two for a line image and dimension three for a nondegenerate
plane image. A change of the displayed basis \(p,q\) merely changes
coordinates on the same \(V_A\); it does not move \(V_A\). After fixing the
source orbit of \((h,U)\), the actual group acting on \(V_A\) is the image of
\(\operatorname{Stab}_{\mathrm{PGL}_3}(h,U)\) in
\(\mathrm{PGL}(U)\), which can be smaller than the full
\(\mathrm{PGL}_2\).

This gives the following checks on the status column in Section 4.

* If \(b=1\), then \(V_A=U\), so there is no extra outer choice.
* If \(b=2,\delta=2\), then
  \(V_A=\operatorname{Sym}^2U\), again with no extra choice. Hence
  `E0-A2-B2-D2-N1` is the finite Kronecker--Segre list and
  `E2-A1-B2-D2-N1` is exactly the seven conic/point incidences.
* If \(b=2,\delta=1\), \(V_A\) is a basepoint-free plane in
  \(\operatorname{Sym}^2U\). For a generic conic pencil its stabilizer is
  finite, giving generic quotient dimension two in `E0-A2-B2-D1-N2`.
  For a generic smooth-conic/point source pair, the residual one-dimensional
  group leaves generic quotient dimension one in `E2-A1-B2-D1-N2`.
* For \((e,a)=(1,1)\), write `OFF` when \(h\notin U\) and `ON` when
  \(h\in U\). The `OFF` stabilizer induces all of
  \(\mathrm{PGL}(U)\); the `ON` stabilizer induces only the Borel subgroup
  preserving the distinguished line \(\langle h\rangle\subset U\).
  Thus degree-three line covers have generic dimensions one (`OFF`) and two
  (`ON`). A birational cubic has the two finite node/cusp types in the `OFF`
  piece, while the `ON` piece is a marked-normalization orbit problem of
  generic dimension one.
* For \((e,a)=(0,1)\), the source stabilizer induces the full
  \(\mathrm{PGL}(U)\), so the isolated outer classifications of Section 5 are
  the actual classifications. In particular the conic/double-cover quartic
  is one orbit.

This coupling is also why source and outer refinement codes should both be
attached to a numerical ID instead of treating the table as a Cartesian
product of two independent orbit lists. Likewise, least-degree minimality is
a condition on the coupled pair \((U,V_A)\), not on \(U\) alone. A pencil
that is visibly composed through lower-degree forms is certainly nonminimal,
but a special outer subspace can also make the resulting triple admit a
smaller presentation even when the whole pencil \(U\) does not. Such a point
is reassigned by the global minimization in Section 8.

## 7. Boundary and degeneration ledger

The thirteen rows are the open numerical pieces only after exact gcd
extraction and pencil minimization. The following ledger records every way
the defining conditions can fail and how to renormalize. It is part of the
taxonomy.

### 7.1 Outer triple acquires a binary gcd

Suppose \(A=D\,A'\), where \(D\) has binary degree \(c\), \(1\le c\le b\).
Then
\[
 hA(p,q)=\bigl(hD(p,q)\bigr)A'(p,q),\qquad
 (e,a,b)\longmapsto(e+ac,a,b-c).                         \tag{10}
\]
If \(b-c=0\), the result is rank one. Otherwise minimize the surviving pencil
again. Ignoring a possible further minimization, all numerical arrows are:

\[
\begin{array}{c|l}
(e,a,b)&\text{possible targets as }c\text{ increases}\\ \hline
(0,1,4)&(1,1,3),(2,1,2),(3,1,1),R1\\
(0,2,2)&(2,2,1),R1\\
(0,4,1)&R1\\
(1,1,3)&(2,1,2),(3,1,1),R1\\
(1,3,1)&R1\\
(2,1,2)&(3,1,1),R1\\
(2,2,1)&R1\\
(3,1,1)&R1.
\end{array}                                             \tag{11}
\]
After removal of \(D\), the new outer triple may have any
\((\delta',\nu')\) with \(\delta'\nu'=b-c\).

### 7.2 The source pencil acquires a common factor

Suppose \(p=g p'\), \(q=g q'\), with \(\deg g=c\), \(1\le c\le a\). Homogeneity
of \(A\) gives
\[
 hA(p,q)=\bigl(hg^b\bigr)A(p',q'),\qquad
 (e,a,b)\longmapsto(e+bc,a-c,b).                         \tag{12}
\]
For \(c=a\), the projective pencil is constant and the result is rank one.
The non-rank-one arrows are
\[
\begin{array}{c|l}
(0,2,2)&(2,1,2)\\
(0,4,1)&(1,3,1),(2,2,1),(3,1,1)\\
(1,3,1)&(2,2,1),(3,1,1)\\
(2,2,1)&(3,1,1).
\end{array}                                             \tag{13}
\]
Rows with \(a=1\) go directly to rank one when the pencil degenerates this
way. Again, apply least-degree minimization afterward.

### 7.3 A displayed pencil ceases to be minimal

A visible sufficient mechanism is
\[
 p=P(r,s),\quad q=Q(r,s),\quad
 \deg P=\deg Q=k>1,\quad a=ka',
\]
which rewrites
\[
 A(p,q)=(A\circ(P,Q))(r,s),\qquad
 (e,a,b)\longmapsto(e,a/k,bk).                           \tag{14}
\]
The possible numerical moves are
\[
\begin{array}{c|l}
(0,2,2)&(0,1,4)\\
(0,4,1)&(0,2,2)\text{ or }(0,1,4)\\
(1,3,1)&(1,1,3)\\
(2,2,1)&(2,1,2).
\end{array}                                             \tag{15}
\]
The image degree stays \(\delta\), while the cover degree is multiplied by
\(k\). Thus, for example, a composite conic pencil in the
`D2-N1` outer row moves to `B4-D2-N2`, whereas a composite line row moves to
the corresponding higher-cover line row.

Equation (14) is not claimed to characterize every possible coincidence
between two nonunique pencil presentations. The row assignment is defined by
the global least \(a\), so even an exotic coincidence is still assigned
correctly. This is where the uniqueness gap from Section 3 matters.

### 7.4 Image degree and cover degree jump with fixed \(b\)

Within the basepoint-free outer parameter space, the only possibilities are
the divisor pairs of \(b\) already in the table:

* \(b=4:\ (4,1),(2,2),(1,4)\);
* \(b=3:\ (3,1),(1,3)\);
* \(b=2:\ (2,1),(1,2)\);
* \(b=1:\ (1,1)\).

Linear dependence of the three coordinates produces the line-image strata.
Nonbirational specialization can produce the conic/double-cover stratum when
\(b=4\). A further span drop to one cannot remain basepoint-free for \(b>0\);
after gcd extraction it is rank one. All cover ramification collisions are
retained by the Hurwitz codes of Section 5.

### 7.5 Internal geometric boundaries

The following changes do not necessarily alter
\((e,a,b,\delta,\nu)\), so they must not be mistaken for missing top-level
rows:

* factorization, multiplicity, or singularity changes of \(h\);
* collisions and infinitely-near structure in the pencil base scheme;
* changes of Kronecker--Segre symbol for conic pencils;
* changes of ramification/Nielsen class of a cover;
* nodal-to-cuspidal degeneration of a rational cubic;
* every equisingular or adjacency degeneration of a rational quartic subject
  to \(\sum\delta_P=3\);
* all special incidences between \(h\), pencil members, and pencil base points.

They are recorded by the refinement codes and orbit problems above.

### 7.6 Rank drops and the zero boundary

If the projective image becomes a point, the map is reclassified as
`Q4-R1-POINT`; no factorization assumption is needed for that conclusion.
If all quartic coefficients vanish, the terminal boundary is `Q4-R0-Z`.

## 8. Normalization algorithm and completeness certificate

Given any homogeneous quartic triple \(H\) with \(\det JH=0\):

1. Compute \(r(H)\).
2. If \(r=0\), assign `Q4-R0-Z`.
3. If \(r=1\), write \(H=c f\) and assign `Q4-R1-POINT`, refined by the
   factorization and projective orbit of \(f\).
4. If \(r=2\), extract the exact component gcd \(h\), producing a primitive
   triple \(G\).
5. Apply the normalization construction of Section 3 to obtain at least one
   coprime homogeneous pencil factorization.
6. Choose the least possible pencil degree \(a\); let \(b=(4-e)/a\).
7. Compute the projective image degree \(\delta\) and cover degree
   \(\nu=b/\delta\).
8. The integer equations force exactly one of the thirteen numerical IDs.
   Attach an outer Hurwitz/singularity code and a source-orbit code. If
   multiple least-degree pencils exist, attach multiple presentation codes to
   the same numerical object rather than deleting it.

This algorithm terminates and has no genericity step. Outer base points,
source common factors, and nonminimal compositions are removed by
(10)--(15); rank drops are sent to Sections 2.1--2.2; all remaining
degenerations stay inside the explicitly inclusive source or outer orbit
spaces. Consequently the list is exhaustive under (1), independently of any
future Keller exclusions.

## 9. Assumptions and unresolved points

1. The base field is algebraically closed of characteristic zero. The
   Jacobian criterion, separability of covers, and rationality arguments are
   used in that form.
2. "Component gcd" means the UFD gcd in
   \(\mathbb C[x_0,x_1,x_2]\). "Basepoint-free binary triple" means no common
   zero on \(\mathbb P^1\), equivalently no positive-degree binary gcd.
3. "Minimal pencil" is defined here as least polynomial degree \(a\) among all
   primitive binary-pullback presentations. This convention is essential.
4. Existence of a polynomial binary-pencil factorization is proved in
   Section 3. The remaining gap is uniqueness of the least-degree pencil, not
   existence or numerical completeness.
5. The Kronecker--Segre and Nielsen labels are canonical finite indexing
   devices. Expanding them into a preferred list of explicit normal forms is
   bookkeeping, not an additional mathematical case.
6. Only the top Keller identity has been used. Nothing here asserts that a
   row survives the lower determinant identities or that it is realized by a
   non-linear Keller map.

## 10. Short final inventory

The exhaustive quartic candidate space is the disjoint rank inventory
\[
 \boxed{\texttt{Q4-R0-Z}}\quad\sqcup\quad
 \boxed{\texttt{Q4-R1-POINT}}\quad\sqcup\quad
 \boxed{\text{the thirteen `Q4-R2-E*-A*-B*-D*-N*' rows}},
\]
where rank zero is omitted for exact degree four, rank one contains the full
ternary-quartic orbit space, and every rank-two boundary is normalized back
into one of these pieces by the boundary ledger.
