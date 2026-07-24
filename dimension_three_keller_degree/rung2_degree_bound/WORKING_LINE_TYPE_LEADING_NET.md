# Working theorem: the primitive line-type quartic leading net

**Status:** proved and independently adversarially audited under the explicit
primitive-pencil hypothesis below.  The audit found and removed a false
inference from line image to primitive parametrization.  This is not peer
reviewed; the completed source-specific priority search is not a guarantee of
worldwide priority.

**Recorded:** 2026-07-24T23:26:30Z.

## 1. Statement

Let
\[
F:\mathbb A^3_{\mathbb C}\longrightarrow\mathbb A^3_{\mathbb C}
\]
be a Keller map of total polynomial degree \(4\).  After affine translation
and linear conjugation, write
\[
F=X+H_2+H_3+H_4,
\tag{1}
\]
where \(H_i\) is homogeneous of degree \(i\).

Assume:

1. the three components of \(H_4\) have no common factor; and
2. the projective image of
   \([H_{4,1}:H_{4,2}:H_{4,3}]\) is a line; and
3. the induced rational map to that line is primitive: after target
   coordinates put \(H_4=(P,Q,0)\), the field
   \[
   \mathbb C(P/Q)
   \quad\text{is relatively algebraically closed in}\quad
   \mathbb C(\mathbb P^2).
   \tag{2}
   \]

After a linear conjugation, write
\[
H_4=(P,Q,0),
\tag{3}
\]
where \(P,Q\) are coprime quartics satisfying (2).

Put
\[
R_3=(H_3)_3,\qquad R_2=(H_2)_3.
\]

### Theorem

Exactly one of the following necessary shapes occurs.

1. \(R_3\ne0\).  The pencil \(\langle P,Q\rangle\) contains a fourth power
   \(L^4\) of a linear form, and
   \[
   R_3=\lambda L^3
   \qquad(\lambda\in\mathbb C^\times).
   \tag{4}
   \]
2. \(R_3=0\) and \(R_2\ne0\).  The pencil contains the square of the
   quadratic \(R_2\):
   \[
   \alpha P+\beta Q=\lambda R_2^2
   \tag{5}
   \]
   for some \((\alpha,\beta)\ne(0,0)\) and
   \(\lambda\in\mathbb C^\times\).
3. \(R_3=R_2=0\).  Then \(F\) is a polynomial automorphism.

Consequently a Keller **counterexample** in the primitive line-type
leading-net class must satisfy (4) or (5).  A primitive quartic pencil all of
whose members are squarefree cannot occur.

## 2. Why the leading net factors through a pencil

The degree-nine part of \(\det JF=1\) is
\[
\det JH_4=0.
\tag{6}
\]
Thus the affine cone image of \(H_4\) has dimension at most two, and its
projective image has dimension at most one.

The homogeneous rank-two factorization theorem gives
\[
H_4=h\,A(p,q),\qquad
\deg h+\deg A\cdot\deg(p,q)=4,
\tag{7}
\]
with \(A\) a primitive vector of binary forms and \((p,q)\) a primitive
homogeneous pencil.  This is a direct specialization of Michiel de Bondt,
*Rational maps \(H\) for which \(K(tH)\) has transcendence degree \(2\)
over \(K\)*, arXiv:1501.06046, Theorem 2.7.

Coprimality makes the scalar factor \(h\) constant.  The possible degree
factorizations are
\[
(\deg(p,q),\deg A)=(4,1),(2,2),(1,4).
\tag{8}
\]
The fact that the image set is a line does not select the first case:
\[
H_4=(x^4,y^4,0)
\]
has coprime components and line image, but its minimal pair is \((x,y)\)
and its binary parametrization has degree \(4\).  Likewise
\((p^2,q^2,0)\) realizes the middle case.

Theorem 2.7(ix) says that a pair \((p,q)\) of minimal degree has
\(\mathbb C(p/q)\) relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\).  Hypothesis (2), rather than line image alone,
is what ensures that the displayed quartic ratio \(P/Q\) is already such a
primitive generator.  The composite cases in (8) remain separate quartic
strata and are not covered by the theorem below.

## 3. The power-fibre lemma

### Lemma

Let \(P,Q\) satisfy (2), both of degree \(4\), and let \(R\ne0\) be
homogeneous of degree \(d=2\) or \(3\).  If
\[
\operatorname{Jac}(P,Q,R)=0,
\tag{9}
\]
then:

- for \(d=2\), the pencil contains \(R^2\), up to a nonzero scalar;
- for \(d=3\), there is a linear form \(L\) with
  \(R=\lambda L^3\), and the pencil contains \(L^4\).

### Proof

Set \(u=P/Q\).  Choose a generic member of the pencil as denominator, so
that no component of \(R=0\) lies in \(Q=0\).  The rational function
\[
v=\frac{R^4}{Q^d}
\tag{10}
\]
has degree zero on \(\mathbb P^2\).  Equation (9) says that
\(\operatorname{trdeg}\mathbb C(P,Q,R)\le2\); removing the one scaling
parameter shows that \(v\) is algebraic over \(\mathbb C(u)\).  By the
relative-algebraic-closedness hypothesis (2),
\[
v=\varphi(u)
\quad\text{for some }\varphi\in\mathbb C(u).
\tag{11}
\]

The pole divisor of (10) is \(d(Q=0)\).  Therefore \(\varphi\) has one pole,
of order \(d\).  Write its zero orders as a partition
\[
d=n_1+\cdots+n_j.
\tag{12}
\]
For the corresponding pencil fibres \(F_i=0\), comparison of vertical
divisors in (10)--(11) gives
\[
4\,\operatorname{div}(R_i)
=n_i\,\operatorname{div}(F_i),
\qquad
\deg R_i=n_i,
\tag{13}
\]
where the \(R_i\)'s partition the divisor of \(R\).

If \(d=2\), the split partition \(1+1\) would give two fourth-power line
fibres.  Their ratio is a fourth power, making a Möbius transform of \(u\)
a nontrivial fourth power in \(\mathbb C(\mathbb P^2)\), contrary to (2).
Thus (12) is the single part \(2\), and (13) gives
\[
F_1=\lambda R^2.
\]

If \(d=3\), the partition \(1+1+1\) is excluded in the same way.  The
partition \(1+2\) gives one fibre \(L^4\) and another fibre \(S^2\), with
\(\deg L=1\) and \(\deg S=2\).  Their ratio
\[
\frac{L^4}{S^2}
=\left(\frac{L^2}{S}\right)^2
\]
makes a Möbius transform of \(u\) a square, again contradicting (2).
Hence (12) is the single part \(3\).  Equation (13) forces
\[
R=\lambda L^3,\qquad F_1=\mu L^4.
\]
\(\square\)

The relative-algebraic-closedness condition is indispensable.  For example,
a pencil generated by \(L^4\) and \(S^2\) admits the cubic invariant \(LS\),
but its ratio is a square and the pencil is not primitive.

## 4. Extracting the determinant coefficients

Put
\[
A=JH_2,\qquad B=JH_3,\qquad C=JH_4.
\]
In the normalization (3), the third row of \(C\) is zero and its first two
rows are \(\nabla P,\nabla Q\).

The homogeneous degree-eight part of
\(\det(I+A+B+C)=1\) is the term using two rows of \(C\) and one row of
\(B\).  Hence
\[
\operatorname{Jac}(P,Q,R_3)=0.
\tag{14}
\]
If \(R_3\ne0\), the \(d=3\) part of the lemma proves (4).

If \(R_3=0\), the third row of \(B\) is also zero.  All terms of degree
seven using one row of \(C\) and two rows of \(B\) therefore vanish.  The
remaining degree-seven coefficient uses two rows of \(C\) and the third row
of \(A\), giving
\[
\operatorname{Jac}(P,Q,R_2)=0.
\tag{15}
\]
If \(R_2\ne0\), the \(d=2\) part of the lemma proves (5).

## 5. The linear-coordinate exit

If \(R_3=R_2=0\), the normalization (1) has
\[
F_3=X_3.
\]
For each \(c\in\mathbb C\), the restriction
\[
(X_1,X_2)\longmapsto
\bigl(F_1(X_1,X_2,c),F_2(X_1,X_2,c)\bigr)
\]
is a plane Keller map of degree at most \(4\).  The established plane
degree bound makes every such map an automorphism.  Hence equality of two
values of \(F\) first forces equality of their third coordinates and then,
on that fibre, equality of the first two coordinates.  Thus \(F\) is
injective.  The Ax--Grothendieck theorem makes it a polynomial
automorphism.

This invokes an established low-degree plane theorem; it neither assumes
the plane Jacobian Conjecture nor attempts new work in dimension two.

## 6. Next work

1. Analyze the composite \((2,2)\) and \((1,4)\) line parametrizations.
2. Analyze whether the forced \(L^4/L^3\) and \(R_2^2/R_2\) cases are
   themselves triangularizable or incompatible with the remaining seven
   determinant identities.
