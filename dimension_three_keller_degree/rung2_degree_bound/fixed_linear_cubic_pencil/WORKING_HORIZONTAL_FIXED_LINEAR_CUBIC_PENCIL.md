# Theorem: the horizontal fixed-linear cubic-pencil row

**Status:** exact working theorem on the nonvertical locus, independently
hostile-audited with a PASS verdict.  This note is not peer reviewed.

**Recorded:** 2026-07-25T05:56:00Z.

**Promoted after hostile audit:** 2026-07-25T06:18:12Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, where \(L_0\in\operatorname{GL}_3(\mathbb C)\)
and \(H_i\) is homogeneous of degree \(i\).  Suppose independent linear
source and target changes put the leading part in the form
\[
\boxed{H_4=(hp,hq,0)^T,}
\tag{1}
\]
where \(h\) is a nonzero linear form and \(p,q\) are coprime,
nonproportional cubic forms.

Assume that \((p,q)\) is the minimal pair for the induced projective
pencil.  Concretely, it is not obtained from a lower-degree homogeneous
pair by a rational self-map of \(\mathbb P^1\).  Equivalently in this
degree-three row,
\[
\mathbb C(p/q)\text{ is relatively algebraically closed in }
\mathbb C(\mathbb P^2).
\tag{2}
\]

Finally assume that \(h=0\) is horizontal for the pencil:
\[
\boxed{
h\nmid \alpha p+\beta q
\quad\text{for every }(\alpha,\beta)\ne(0,0).
}
\tag{3}
\]

Write
\[
G_3=(H_3)_3,\qquad G_2=(H_2)_3.
\tag{4}
\]

### Theorem

If \(F\) is Keller and (1)--(3) hold, then
\[
\boxed{G_3=G_2=0.}
\tag{5}
\]
Consequently the third component of \(F\) is a nonzero linear form, and
\(F\) is a polynomial automorphism.

Thus no degree-four Keller counterexample belongs to the horizontal part
of the taxonomy row
\[
(e,a,b,\delta,\nu)=(1,3,1,1,1).
\]

The omitted locus is exactly
\[
\mathcal V_h=
\{(p,q):h\mid\alpha p+\beta q
\text{ for some }[\alpha:\beta]\in\mathbb P^1\}.
\tag{6}
\]
It is a genuine exception for the two top identities: Section 7 gives
primitive points of \(\mathcal V_h\) with nonzero quadratic and cubic
normal first integrals.

## 2. Minimality gives relative algebraic closure

We record the implication used in (2), rather than hiding it in the
taxonomy terminology.

### Lemma 1

Let \(p,q\) be coprime homogeneous cubics.  If \(p/q\) does not factor as
\[
\frac pq=\varphi\left(\frac rs\right)
\tag{7}
\]
with \(r,s\) coprime homogeneous forms of degree less than three and
\(\deg\varphi>1\), then \(\mathbb C(p/q)\) is relatively algebraically
closed in
\[
K_0:=\mathbb C(\mathbb P^2).
\]

### Proof

Let \(L\) be the relative algebraic closure of \(\mathbb C(p/q)\) in
\(K_0\).  It has transcendence degree one.  Let \(C\) be the smooth
projective curve with function field \(L\).  The inclusion
\(L\subset K_0\) gives a dominant rational map
\(\mathbb P^2\dashrightarrow C\).  Its restriction to a general line is
nonconstant, so \(C\) is dominated by \(\mathbb P^1\).  Riemann--Hurwitz
then gives \(g(C)=0\), and hence
\[
L=\mathbb C(v)
\tag{8}
\]
for a rational function \(v\in K_0\).

If \(L\ne\mathbb C(p/q)\), then
\[
\frac pq=\varphi(v),\qquad \deg\varphi=n>1.
\tag{9}
\]
Represent \(v=r/s\) by coprime homogeneous forms of the same degree
\(a\), and represent \(\varphi=A/B\) by coprime binary forms of degree
\(n\).  The forms \(A(r,s)\) and \(B(r,s)\) are coprime.  Indeed, a
common prime divisor would make both \(A\) and \(B\) vanish at the
generic value \([r:s]\) of that divisor; since \(A,B\) have no common
point on \(\mathbb P^1\), the prime would divide both \(r\) and \(s\).

The equality
\[
\frac pq=\frac{A(r,s)}{B(r,s)}
\]
between two reduced fractions therefore gives, up to nonzero constants,
\[
p=A(r,s),\qquad q=B(r,s).
\tag{10}
\]
Taking degrees yields
\[
3=na.
\tag{11}
\]
Because \(n>1\), equation (11) forces \(n=3\) and \(a=1\), exactly the
forbidden lower-degree factorization (7).  Thus \(L=\mathbb C(p/q)\).
\(\square\)

In taxonomy language, a nonminimal cubic pair in (1) is not part of the
\((a,b)=(3,1)\) row: (10)--(11) reclassify it into the
\((a,b)=(1,3)\) row.

## 3. The degree-zero first-integral lemma

Put
\[
P=hp,\qquad Q=hq
\tag{12}
\]
and define the Jacobian derivation
\[
D(G)=\operatorname{Jac}(P,Q,G)
     =(\nabla P\times\nabla Q)\mathbin{\cdot}\nabla G.
\tag{13}
\]
If
\[
J=\operatorname{Jac}(p,q,h),
\]
direct expansion gives
\[
\begin{aligned}
D(h)&=h^2J,\\
D(p)&=-hpJ,\\
D(q)&=-hqJ.
\end{aligned}
\tag{14}
\]
In particular \(D(P)=D(Q)=D(q/p)=0\).

The following lemma is the divisor obstruction used twice.

### Lemma 2

Assume (2)--(3).  Let \(G\) be a homogeneous polynomial of degree \(d\).
If
\[
\operatorname{Jac}(P,Q,G)=0
\tag{15}
\]
and \(4\nmid d\), then \(G=0\).

### Proof

Assume \(G\ne0\).

First, \(P,Q\) are algebraically independent.  If a polynomial relation
between them existed, source scaling separates it into homogeneous
binary relations.  A nonzero homogeneous binary polynomial factors into
linear factors over \(\mathbb C\), so the domain property would make
\(P,Q\) proportional, contrary to the hypotheses.

Equation (15) says
\[
dP\wedge dQ\wedge dG=0.
\]
In characteristic zero the differentials of an algebraically independent
triple are independent.  Hence \(G\) is algebraic over
\(\mathbb C(P,Q)\).

Now form the degree-zero rational function
\[
\Theta=\frac{G^4}{P^d}\in K_0.
\tag{16}
\]
Set \(u=Q/P=q/p\).  Since
\(\mathbb C(P,Q)=\mathbb C(u,P)\), the preceding algebraicity makes
\(\Theta\) algebraic over \(\mathbb C(u,P)\).  It remains to remove the
scaling variable \(P\); this step is not automatic merely from the words
“degree zero,” so we spell it out.

Choose a linear source coordinate \(s\).  Then
\[
\mathbb C(x,y,z)=K_0(s),
\quad
P=s^4P_0,
\quad
G=s^dG_0
\tag{17}
\]
with \(P_0,G_0\in K_0\).  Thus \(P\) is transcendental over \(K_0\).
Take an algebraic relation for \(\Theta\) over
\(\mathbb C(u)(P)\), clear denominators, and regroup it as
\[
\sum_j P^j b_j(\Theta)=0,
\qquad b_j(T)\in\mathbb C(u)[T].
\tag{18}
\]
Transcendence of \(P\) over \(K_0\), which contains \(u,\Theta\), makes
every \(b_j(\Theta)\) vanish.  At least one \(b_j\) is nonzero, so
\(\Theta\) is algebraic over \(\mathbb C(u)\).  Lemma 1 now gives
\[
\boxed{\Theta=R(u)}
\qquad\text{for some }R\in\mathbb C(t).
\tag{19}
\]

Let \(v_h\) be the prime-divisor valuation along \(h=0\).  Condition (3)
implies
\[
v_h(p)=v_h(q-\lambda p)=0
\quad\text{for every }\lambda\in\mathbb C.
\tag{20}
\]
Factoring the numerator and denominator of \(R\) over \(\mathbb C\)
therefore gives
\[
v_h(R(q/p))=0.
\tag{21}
\]
On the other hand, \(v_h(P)=1\), and (16) gives
\[
v_h(\Theta)=4v_h(G)-d.
\tag{22}
\]
Equations (19), (21), and (22) force
\[
4v_h(G)=d,
\]
which is impossible when \(4\nmid d\).  Hence \(G=0\).
\(\square\)

Geometrically, (3) says the divisor \(h=0\) dominates the pencil base
\(\mathbb P^1\).  Therefore a rational function pulled back from that
base has valuation zero along \(h\).  Equation (22) is the incompatible
valuation supplied by the fixed factor in \(P=hp\).

## 4. Degree eight kills the cubic normal component

Let
\[
A=JH_2,\qquad B=JH_3,\qquad C=JH_4.
\]
The third row of \(C\) is zero, and its first two rows are
\(\nabla P,\nabla Q\).  Hence
\[
\operatorname{adj}C
=(\nabla P\times\nabla Q)e_3^T.
\tag{23}
\]

Use source scaling to package the determinant identities:
\[
\mathcal J(\tau)=L_0+\tau A+\tau^2B+\tau^3C.
\tag{24}
\]
The Keller condition makes every positive-degree coefficient of
\(\det\mathcal J(\tau)\) vanish.  Weight eight can only be
\(3+3+2\), so
\[
\begin{aligned}
0=E_8
&=\operatorname{tr}(\operatorname{adj}C\,B)\\
&=(\nabla P\times\nabla Q)\mathbin{\cdot}\nabla G_3\\
&=\operatorname{Jac}(P,Q,G_3).
\end{aligned}
\tag{25}
\]
Lemma 2 with \(d=3\) gives
\[
\boxed{G_3=0.}
\tag{26}
\]

## 5. Degree seven kills the quadratic normal component

After (26), the third row of \(B\) is also zero.  Weight seven consists
of the patterns \(3+3+1\) and \(3+2+2\):
\[
E_7=
\operatorname{tr}(\operatorname{adj}C\,A)
+\operatorname{tr}(\operatorname{adj}B\,C).
\tag{27}
\]
The second trace is zero because both \(B\) and \(C\) have zero third
row.  The first trace is the remaining normal Jacobian, so
\[
0=E_7=\operatorname{Jac}(P,Q,G_2).
\tag{28}
\]
Lemma 2 with \(d=2\) gives
\[
\boxed{G_2=0.}
\tag{29}
\]

No division by \(J\), by a pencil discriminant, or by either possibly
zero normal component occurs in this argument.

## 6. The plane-field exit

Equations (1), (26), and (29) show that the third component of \(F\) is
the third row of \(L_0X\).  That row is nonzero because \(L_0\) is
invertible.  Linear source and target changes therefore put the full map
in the form
\[
F=(F_1(x,y,z),F_2(x,y,z),z).
\tag{30}
\]
Its Jacobian identity becomes
\[
\frac{\partial(F_1,F_2)}{\partial(x,y)}
=\det JF\in\mathbb C^\times.
\tag{31}
\]

For each \(c\in\mathbb C\), restriction to \(z=c\) gives a plane Keller
map
\[
(x,y)\longmapsto
\bigl(F_1(x,y,c),F_2(x,y,c)\bigr)
\tag{32}
\]
of degree at most four.  The established unconditional plane
low-degree theorem makes every map (32) a polynomial automorphism.  If
two points have the same image under (30), their \(z\)-coordinates agree
and injectivity of the corresponding plane fibre makes the points equal.
Thus \(F\) is injective.  Ax--Grothendieck makes \(F\) a polynomial
automorphism.

This exit uses only the banked plane degree bound; it does not assume the
plane Jacobian Conjecture.

## 7. The vertical exceptional locus is sharp

Reduce \(p,q\) modulo \(h\):
\[
\bar p,\bar q\in
\mathbb C[x,y,z]/(h)\cong\mathbb C[s,t].
\]
Because \(\gcd(p,q)=1\), they are not both zero.  Condition (3) fails
exactly when
\[
\operatorname{rank}\langle\bar p,\bar q\rangle=1.
\tag{33}
\]
In coefficients, this is the common zero locus of all \(2\times2\)
minors of the \(2\times4\) matrix of the two restricted binary cubics.
Thus (6) is an explicit closed determinantal locus.

The vertical pencil member is unique: two distinct such members would
make \(h\) divide both \(p\) and \(q\).  After a
\(\operatorname{GL}_2\) change of pencil coordinates, every point of
\(\mathcal V_h\) has the sharp normal form
\[
\boxed{
p=h^m r_{3-m},\quad
1\le m\le3,\quad
h\nmid q r_{3-m},\quad
\gcd(r_{3-m},q)=1.
}
\tag{34}
\]

This also identifies the exact point at which the proof of Lemma 2
changes.  With \(u=q/p\) and
\(\Theta=R(u)\), one has
\[
v_h(P)=m+1,\qquad v_h(u)=-m,
\]
and therefore
\[
\boxed{
4v_h(G)-d(m+1)
=m\,\operatorname{ord}_{\infty}R.
}
\tag{35}
\]
The right side was zero on the horizontal locus, but can be nonzero
here.  Thus (33)--(35), rather than an unspecified degeneracy, are the
complete escape visible to the valuation at the prime divisor \(h=0\).

The top identities do not force the normal components to vanish on all
of (34).

### A simple vertical member can preserve \(G_2\)

Take
\[
h=z,\qquad p=zx^2,\qquad q=x^3+y^3.
\tag{36}
\]
Then
\[
P=hp=z^2x^2=(zx)^2,
\]
so
\[
G_2=zx\ne0,\qquad
\operatorname{Jac}(P,Q,G_2)=0.
\tag{37}
\]
The pair is still minimal: over
\(\overline{\mathbb C(t)}\), the generic fibre
\[
x^2z-t(x^3+y^3)=0
\tag{38}
\]
is irreducible.  Indeed, it is linear in \(z\), and a nontrivial
\(z\)-free factor would divide both \(x^2\) and \(x^3+y^3\).
Therefore (37) is a primitive \(m=1\) exception to any unconditional
degree-seven vanishing claim.

### A triple vertical member can preserve \(G_3\)

Take
\[
h=z,\qquad p=z^3,\qquad q=x^3+y^3.
\tag{39}
\]
Now \(P=z^4\), and hence
\[
G_3=z^3\ne0,\qquad
\operatorname{Jac}(P,Q,G_3)=0.
\tag{40}
\]
The generic fibre
\[
z^3-t(x^3+y^3)=0
\tag{41}
\]
is a smooth plane cubic over \(\overline{\mathbb C(t)}\), since its
three partial derivatives have no common projective zero.  It is
therefore geometrically integral and the pencil is minimal.  If one
instead sets \(G_3=0\), the same example also permits
\(G_2=z^2\ne0\) in (28).

These are counterexamples only to an overly broad claim about what
\(E_8,E_7\) force.  They are not asserted to satisfy the remaining
Keller identities.

## 8. Verification boundary

The accompanying exact checks are:

- `verify_horizontal_fixed_linear_cubic_pencil_sympy.py`, which checks
  the general derivation identities (14), the formal weights
  \(E_8,E_7\), zero low-degree kernels for a concrete horizontal Hesse
  pencil, and both vertical examples;
- `verify_horizontal_fixed_linear_cubic_pencil_pari.gp`, which
  independently checks the weighted determinant coefficients, the
  horizontal kernel ranks, and the vertical first integrals over exact
  rational arithmetic;
- `audit_hostile/audit_finite_field.py`, which reconstructs polynomial
  arithmetic, kernel ranks, determinant polarizations, and the exceptional
  witnesses independently over a large prime field.

From the repository root, run:

```text
/usr/bin/python3 dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/verify_horizontal_fixed_linear_cubic_pencil_sympy.py
dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/verify_horizontal_fixed_linear_cubic_pencil_pari_strict.sh
dimension_three_keller_degree/rung2_degree_bound/fixed_linear_cubic_pencil/audit_hostile/audit_finite_field_strict.sh
```

The scripts do not prove the relative-algebraic-closure step or the
plane low-degree theorem.  Those are mathematical inputs proved or
identified above.  Exact computer algebra is evidence about the encoded
identities, not peer review.  AI systems materially assisted the proof,
verification, audit, and exposition.
