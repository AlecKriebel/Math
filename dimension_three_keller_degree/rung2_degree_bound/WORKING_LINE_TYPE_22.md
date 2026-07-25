# Working theorem: the genuine line-image \((2,2)\) stratum

**Status:** complete theorem, assembled from independently audited joint-orbit
packages. Sections 5--6 retain the earlier conditional-chart calculations
and the normalization defect that forced the joint-moduli analysis; Section 7
records the exhaustive closure. This is not peer reviewed. The
source-specific priority search found no exact prior statement and is not a
guarantee of worldwide priority.

**Recorded:** 2026-07-24T23:59:52Z.

**Completed after final hostile audit:** 2026-07-25T10:07:13Z.

## 1. Setup and theorem

Let \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) be a Keller
map of total degree \(4\), with homogeneous decomposition
\[
F=L_0X+H_2+H_3+H_4,\qquad L_0\in\operatorname{GL}_3(\mathbb C).
\]
Assume that, after target coordinates,
\[
H_4=(A_1(p,q),A_2(p,q),0),
\tag{1}
\]
where:

- \(p,q\) are coprime nonproportional homogeneous quadrics;
- \(\mathbb C(p/q)\) is relatively algebraically closed in
  \(\mathbb C(\mathbb P^2)\); and
- \(A_1,A_2\) are coprime binary quadrics with nonconstant ratio.

Put
\[
R_3=(H_3)_3,\qquad R_2=(H_2)_3.
\]

### Theorem

Every Keller map satisfying (1) is a polynomial automorphism. Equivalently,
no degree-four Keller counterexample belongs to the genuine line-image
taxonomy row
\[
(e,a,b,\delta,\nu)=(0,2,2,1,2).
\tag{2}
\]

The top identity begins the proof with the following sharper alternative.

If the pencil \(\langle p,q\rangle\) has no scheme-theoretic double-line
member, then \(F\) is a polynomial automorphism.

More precisely, the degree-eight Keller identity gives exactly these
alternatives:

1. \(R_3=0\); or
2. the pencil has a unique double-line member \(L^2\), and
   \[
   R_3=cL^3
   \quad\text{or}\quad
   R_3=cL(\alpha p+\beta q).
   \tag{2a}
   \]

Consequently a putative counterexample would have to have the
unique-double-line configuration and one of the two nonzero cubic shapes in
(2a). Section 7 excludes every joint orbit on that remaining locus.

## 2. Degree eight as a vertical-divisor equation

Let
\[
D=\nabla p\times\nabla q.
\]
The binary chain rule factors the degree-eight determinant:
\[
\operatorname{Jac}\bigl(A_1(p,q),A_2(p,q),R_3\bigr)
=J(A_1,A_2)(p,q)\,D(R_3).
\]
The binary Jacobian factor is nonzero, so the Keller identity is
\[
D(R_3)=0.
\tag{3}
\]

We use the following homogeneous first-integral fact.  Let \(p,q\) have
common degree \(d>0\), let \(R\ne0\) be homogeneous of degree \(e\), and
suppose \(D(R)=0\).  If
\[
g=\gcd(d,e),\qquad a=d/g,\qquad b=e/g,
\]
then \(w=R^a/q^b\in\mathbb C(\mathbb P^2)\) is algebraic over
\(\mathbb C(p/q)\).

To prove this, first note that nonproportional \(p,q\) are algebraically
independent: splitting a polynomial relation into scaling-homogeneous pieces
would make \(p/q\) algebraic over \(\mathbb C\), hence constant.  Thus
\(D\ne0\).  The kernel of a nonzero derivation of
\(\mathbb C(X_1,X_2,X_3)\) has transcendence degree at most two; otherwise
the whole function field would be algebraic over the kernel and the
characteristic-zero derivation would vanish.  Its kernel contains
\(\mathbb C(p,q)\), so \(R\), and hence \(w\), is algebraic over
\(\mathbb C(p,q)=\mathbb C(p/q,q)\).

Put \(E=\mathbb C(\mathbb P^2)\).  The homogeneous element \(q\) is
transcendental over \(E\): source scaling fixes \(E\) and gives infinitely
many distinct multiples of \(q\).  If \(w\) were transcendental over
\(\mathbb C(p/q)\), then \(p/q,w\) would be a transcendence basis of \(E\);
adjoining \(q\) would make \(p/q,w,q\) algebraically independent.  This
contradicts the algebraicity of \(w\) over \(\mathbb C(p/q,q)\).

Assume \(R_3\ne0\).  The degree-zero rational function
\[
v=\frac{R_3^2}{q^3}
\]
is invariant under \(D\); the case \((d,e)=(2,3)\) of the preceding lemma
makes it algebraic over \(u=p/q\).  Relative
algebraic closedness gives
\[
v\in\mathbb C(u).
\]
Taking Weil divisors on \(\mathbb P^2\) gives
\[
2\operatorname{div}(R_3)=u^*B
\tag{4}
\]
for an effective divisor \(B\) of degree \(3\) on the base
\(\mathbb P^1\).  Pencil base points are codimension two and do not enter
this divisor calculation.

If a point of \(B\) has odd coefficient, (4) says that every component of
the corresponding conic fibre has even multiplicity.  That fibre is
therefore a double line \(L^2\); a reduced singular conic \(L_1L_2\) does
not suffice.

There cannot be two distinct double-line fibres.  Their ratio would make a
Möbius transform of \(p/q\) a square.  Its square root is algebraic over
\(\mathbb C(p/q)\), so relative algebraic closedness would put the root in
\(\mathbb C(p/q)\), contradicting the odd valuations of a Möbius function.

If there is no double line, all coefficients of \(B\) would be even, which
contradicts \(\deg B=3\).  If the unique double line exists, the only
partitions are \(3\) and \(1+2\), which give precisely (2a).

## 3. The \(R_3=0\) branch

When \(R_3=0\), the third row of \(JH_3\) vanishes.  The degree-seven
identity reduces to
\[
\operatorname{Jac}\bigl(A_1(p,q),A_2(p,q),R_2\bigr)=0,
\]
and hence
\[
D(R_2)=0.
\]
The same degree-zero argument, now applied to \(R_2/q\), gives
\[
R_2\in\langle p,q\rangle.
\tag{5}
\]

More importantly, the third component of the full map has degree at most
two:
\[
F_3=(L_0X)_3+R_2.
\]
The quadratic-component exit in
`WORKING_QUADRATIC_COMPONENT_EXIT.md` makes \(F\) an automorphism.  Thus a
counterexample cannot lie in the \(R_3=0\) branch, regardless of (5).

## 4. Exact necessity of the double-line exception

The exception cannot be deleted from the degree-eight statement.  Take
\[
p=X_1^2,\qquad q=X_2X_3,\qquad
H_4=(p^2,q^2,0),\qquad
H_3=(0,0,X_1^3).
\]
The generic conic \(X_1^2-tX_2X_3\) is geometrically integral, so the pencil
is primitive, and \(p=X_1^2\) is its unique double-line member.
Equation (3) holds with \(R_3=X_1^3\ne0\).

This example certifies only the sharpness of the leading determinant
constraint; it is not claimed to extend to a Keller map.

## 5. Historical conditional charts on the double-line locus

**Status of this section:** retained diagnostic calculation, superseded by
the exhaustive joint-orbit packages in Section 7. The reductions and
degree-seven identities below are proved on the stated simultaneous-normal-
form slices, but those slices are not exhaustive. Nothing in this section
alone claims that the displayed leading data extend to a Keller map.

Suppose now that the pencil has its unique double-line member.  After a
source linear change, a change of pencil basis preserving that member, and
rescaling, put
\[
 p=x^2.
\tag{6}
\]
There are exactly two normal forms for the other generator:
\[
 q=yz
 \qquad\text{or}\qquad
 q=y^2+xz.
\tag{7}
\]
Indeed, restrict \(q\) to the line \(x=0\).  If this binary quadratic has
rank two, put it in the form \(yz\); translations of \(y,z\) by multiples
of \(x\) remove the mixed \(x\)-terms, and replacing \(q\) by \(q+\lambda p\)
removes the \(x^2\)-term.  If it has rank one, put it in the form \(y^2\).
The same operations give \(q=y^2+\lambda xz\).  Here \(\lambda=0\) would
give a second double-line member, so rescaling gives the second form in
(7).

To avoid a collision between the outer quartics and the lower homogeneous
components, write
\[
 \Phi_4=A_1(p,q),\qquad \Psi_4=A_2(p,q),
\]
\[
 H_3=(U_3,V_3,R_3),\qquad H_2=(U_2,V_2,W_2).
\tag{8}
\]
Thus \(W_2\) is the polynomial denoted \(R_2\) in Section 3.

Consider separately the degree-two morphism
\[
 [p:q]\longmapsto[A_1(p,q):A_2(p,q)]
\]
has two normal forms relative to the marked point corresponding to the
double-line fibre.  If that point is critical, use
\[
 (\Phi_4,\Psi_4)=(p^2,q^2),\qquad
 \mathcal K:=J_{p,q}(A_1,A_2)(p,q)=4pq.
\tag{9}
\]
If it is noncritical, use
\[
 (\Phi_4,\Psi_4)=(p^2+q^2,pq),\qquad
 \mathcal K=2(p^2-q^2).
\tag{10}
\]
This is the standard classification of a double cover of
\(\mathbb P^1\), with a marked critical or noncritical source point.
However, the required source change
\[
(p,q)\longmapsto(\lambda p,\mu q+\nu p)
\tag{10a}
\]
need not be induced by a source linear transformation preserving either
normal form (7).  Thus (9) or (10) may be imposed together with (7) only
as an additional chart condition, not as a general simultaneous
normalization.

Likewise, in a pencil basis adapted to the cubic, the two alternatives in
(2a) become
\[
 R_3=x^3
 \qquad\text{or}\qquad
 R_3=xq.
\tag{11}
\]
In the second alternative the conic paired with the double line is distinct,
so it may be chosen as the generator \(q\).  This basis choice can conflict
with the outer-map normalization in exactly the same way as (10a).

## 6. Exact degree-seven equations on the conditional charts

Put
\[
 \delta=q_y\partial_z-q_z\partial_y.
\tag{12}
\]
Then
\[
 \nabla p\times\nabla q=2x\,\delta
\]
where the derivation is identified with its coefficient vector.  The
degree-seven homogeneous part of the Keller determinant is
\[
\begin{split}
 E_7={}&
 \operatorname{Jac}(\Phi_4,\Psi_4,W_2)
 +\operatorname{Jac}(\Phi_4,V_3,R_3)\\
 &+\operatorname{Jac}(U_3,\Psi_4,R_3).
\end{split}
\tag{13}
\]
This formula is independent of the arbitrary invertible linear part
\(L_0\); \(L_0\) first occurs in degree six.

For \(R_3=x^3\), equation (13) is exactly
\[
 E_7=x\left[
 2\mathcal K\,\delta(W_2)+
 3x\bigl((\Phi_4)_q\delta(V_3)
          -(\Psi_4)_q\delta(U_3)\bigr)
 \right].
\tag{14}
\]
For \(R_3=xq\), it is exactly
\[
\begin{split}
 E_7={}&2x\mathcal K\,\delta(W_2)\\
 &+\bigl(q(\Phi_4)_q-2p(\Phi_4)_p\bigr)\delta(V_3)\\
 &+\bigl(2p(\Psi_4)_p-q(\Psi_4)_q\bigr)\delta(U_3).
\end{split}
\tag{15}
\]

### 6.1 Critical outer map

For (9) and \(R_3=x^3\), cancellation of the nonzero factors in (14)
gives
\[
 \delta(3U_3-4xW_2)=0.
\tag{16}
\]
For either normal form (7), direct coefficient comparison gives
\[
 \ker(\delta)\cap\mathbb C[x,y,z]_3
 =\langle x^3,xq\rangle.
\]
Consequently
\[
 3U_3-4xW_2=ax^3+bxq.
\tag{17}
\]

For (9) and \(R_3=xq\), equation (15) becomes
\[
 q^2\delta(U_3)+2x^4\delta(V_3)
 -4x^3q\delta(W_2)=0.
\tag{18}
\]
Since \(\gcd(x,q)=1\), (18) first implies
\[
 \delta(U_3)=c x^3.
\]
After division by \(x^3\), equation (18) says
\[
 \delta(2xV_3-4qW_2)=-c q^2.
\tag{19}
\]
For \(q=yz\), the derivation
\(\delta=z\partial_z-y\partial_y\) has no weight-zero monomial in its
image, so \(q^2\notin\operatorname{im}\delta\).  For
\(q=y^2+xz\), every quartic \(S\) satisfies the coefficient relation
\[
 2[xy^2z](\delta S)
 +3[y^4](\delta S)
 +8[x^2z^2](\delta S)=0,
\tag{20}
\]
where \([M](T)\) denotes the coefficient of \(M\) in \(T\).  The
corresponding value for
\(q^2=y^4+2xy^2z+x^2z^2\) is \(15\), so again
\(q^2\notin\operatorname{im}\delta\).  Thus \(c=0\).

The degree-three and degree-four kernels are
\[
 \ker(\delta)_3=\langle x^3,xq\rangle,\qquad
 \ker(\delta)_4=\langle x^4,x^2q,q^2\rangle
\tag{21}
\]
for both choices in (7).  Equations (18)--(21) therefore give the exact
normal form
\[
\begin{aligned}
 U_3&=a x^3+b xq,\\
 W_2&=x\ell-\frac{\gamma}{2}q,\\
 V_3&=\alpha x^3+\beta xq+2q\ell,
\end{aligned}
\tag{22}
\]
where \(\ell\) is a linear form.

### 6.2 Noncritical outer map

For (10), the two necessary equations are
\[
 R_3=x^3:\quad
 4(p^2-q^2)\delta(W_2)
 +3x\bigl(2q\delta(V_3)-p\delta(U_3)\bigr)=0,
\tag{23}
\]
and
\[
\begin{split}
 R_3=xq:\quad&
 4x(p^2-q^2)\delta(W_2)
 +(2q^2-4p^2)\delta(V_3)\\
 &+pq\delta(U_3)=0.
\end{split}
\tag{24}
\]
These equations have nonzero solution spaces and do not exclude either
branch.

At this historical chart stage, the next unresolved coefficient was degree
six.  It includes the arbitrary
linear part \(L_0\), the quadratic components \(U_2,V_2,W_2\), and the
curvature term with two rows from \(JH_3\).  Any exclusion must retain these
terms rather than normalize \(L_0\) in a way incompatible with
(6)--(10).

### 6.3 Scope correction from the simultaneous-normalization audit

The audit found an exact family missed by the simultaneous charts.  Take
\[
p=x^2,\qquad q=yz,\qquad
H_4=(p^2,\,2pq-q^2,\,0),\qquad
R_3=xq,\qquad H_2=0.
\tag{25}
\]
The marked double-line point is critical and the other critical point of
the outer double cover is \(p/q=1\).  Normalizing the outer map replaces
\(q\) by \(q'=p-q\), which has rank three and is not source-linearly
equivalent, while preserving \(p=x^2\), to the rank-two form \(yz\).
Moreover
\[
R_3=x(p-q'),
\]
not \(xq'\).  Nevertheless the degree-eight and degree-seven coefficients
of (25) vanish.

More generally, after outer normalization the mixed cubic has the form
\[
R_3=x(\rho p+q),
\]
and its degree-seven equation is the corresponding linear combination of
the \(R_3=x^3\) and \(R_3=xq\) formulas (14)--(15).  Equations
(18), (22), and (24) therefore cover \(\rho=0\) slices, not the complete
joint orbit space.

For the rank-two-restriction pencil
\(\langle x^2,yz\rangle\), its rank-one and rank-two singular fibres are
distinguished, so induced pencil automorphisms only rescale \(p/q\).
The outer critical pair and the companion conic of \(R_3\) consequently
carry genuine cross-ratio parameters.  If the marked point is critical, the
outer critical pair normalizes to either \(\{0,\infty\}\) or
\(\{0,1\}\).  If it is noncritical, the pair is either
\(\{1,\infty\}\) or
\(\{1,\lambda\}\), with
\(\lambda\in\mathbb C^\times\setminus\{1\}\) modulo
\(\lambda\leftrightarrow\lambda^{-1}\).  Formula (10) is only the
\(\lambda=-1\) chart.  For
\(\langle x^2,y^2+xz\rangle\), a shear of \(z\) realizes
\(q\mapsto q+\nu p\), so the compatibility problem is milder; no complete
joint-orbit assertion is made there either.

The exact regression script verifies (13)--(24), the kernel/image
calculations, and the displayed conditional substitutions.  It does not
verify exhaustiveness of the simultaneous normalizations.

## 7. Exhaustive joint-orbit closure

The normalization defect in Section 6.3 is resolved by retaining the outer
critical pair, the marked double-line value, and the cubic companion
simultaneously. The unique-double-line pencil has exactly two source-linear
normal forms:
\[
\langle x^2,yz\rangle,\qquad
\langle x^2,y^2+xz\rangle.
\tag{26}
\]
Their stabilizers and joint orbit spaces are different, so they were audited
separately.

For the rank-two-restriction pencil \(\langle x^2,yz\rangle\):

- `WORKING_LINE_22_FINITE_OUTER_CRITICAL.md` and
  `WORKING_LINE_22_FG_RESONANCE.md` exclude the full finite-critical,
  finite-companion moduli, including every resonance and endpoint;
- `line22_marked_critical_infinity/WORKING_LINE22_MARKED_CRITICAL_INFINITY.md`
  excludes the marked infinity triple orbit;
- `line22_outer_infinity_remaining/NOTE.md` excludes every other finite
  companion in the outer-critical-at-infinity chart; and
- `line22_companion_infinity/NOTE.md` excludes both
  companion-at-infinity outer families, including the reciprocal
  \(t=-2\sim-1/2\) resonance.

For the rank-one-restriction pencil
\(\langle x^2,y^2+xz\rangle\), the full Borel stabilizer gives an unmarked
one-parameter family and three marked orbits. They are exhausted by:

- `line22_rankone_restriction/WORKING_RANKONE_RESTRICTION_OPEN_ORBIT.md`;
- the sibling packages `unmarked_triple_c0`,
  `unmarked_resonance_c3`, and `unmarked_companion_infinity`; and
- the sibling packages `marked_mixed_orbits` and `marked_triple_orbit`.

Each listed terminal package has a complete raw-kernel/gauge certificate,
specialization-safe lower-identity tree, and an independent hostile audit.
Every leaf gives a positive-degree Jacobian contradiction or
\(\det L_0=0\). The \(R_3=0\) branch was already closed in Section 3.
Thus (26) leaves no joint orbit, proving the theorem.
