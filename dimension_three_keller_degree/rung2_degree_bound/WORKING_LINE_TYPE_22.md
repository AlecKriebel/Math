# Working theorem: the genuine line-image \((2,2)\) stratum

**Status:** proved and independently audited.  This is not peer reviewed.
The source-specific priority search found no exact prior statement and is not
a guarantee of worldwide priority.

**Recorded:** 2026-07-24T23:59:52Z.

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
   \tag{2}
   \]

Consequently every counterexample in the \((2,2)\) line-image stratum must
have the unique-double-line configuration and one of the two nonzero cubic
shapes in (2).

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
partitions are \(3\) and \(1+2\), which give precisely (2).

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
