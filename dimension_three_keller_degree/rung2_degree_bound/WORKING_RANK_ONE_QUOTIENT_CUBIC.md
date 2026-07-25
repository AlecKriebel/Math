# Working obstruction: the quotient cubic pencil in the rank-one quartic case

**Status:** proved and independently adversarially audited as part of the
primitive-pencil exit audit.  This is not peer reviewed.  The
source-specific priority search found no exact prior statement and is not a
guarantee of worldwide priority.

**Recorded:** 2026-07-25T01:07:00Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
be a total-degree-four Keller map, where \(L_0\) is invertible and the
\(H_i\) are homogeneous of degree \(i\).  Assume
\[
H_4\ne0,\qquad \operatorname{rank}JH_4=1
\]
over \(\mathbb C(X_1,X_2,X_3)\).

Then
\[
H_4=a\,h
\tag{1}
\]
for a nonzero constant target vector \(a\) and a quartic form \(h\).
Project \(H_3\) to the two-dimensional quotient
\(\mathbb C^3/\mathbb Ca\), and choose quotient coordinates:
\[
\overline H_3=(P,Q),
\tag{2}
\]
where \(P,Q\) are cubic forms.

### Proposition

1. If \(P,Q\) are linearly dependent, then \(F\) is a polynomial
   automorphism.
2. Suppose \(P,Q\) are linearly independent, their pencil has no fixed
   curve,
   \[
   \gcd(P,Q)=1,
   \tag{3}
   \]
   and
   \[
   \mathbb C(P/Q)
   \text{ is relatively algebraically closed in }
   \mathbb C(\mathbb P^2).
   \tag{4}
   \]
   Then the pencil contains exactly one triple-line member.  After
   changing the basis of the quotient pencil, there are a linear form
   \(L\) and constants
   \(\alpha,\beta\), not both zero, such that
   \[
   \boxed{
   P=L^3,\qquad h=cL(\alpha P+\beta Q)
   }
   \tag{5}
   \]
   for some \(c\in\mathbb C^\times\).

In particular, every nonautomorphic Keller map in the rank-one leading
stratum must satisfy one of the following mutually nonexclusive
obstructions:

- the projected cubic pencil is not primitive in the sense of
  (3)--(4); or
- the pencil has the exceptional form (5).

Generic geometric integrality of the cubic pencil implies both (3) and
(4).  Thus a primitive projected pencil with no triple-line member is
incompatible with the Keller identities.

The proposition does **not** exclude the exceptional form (5).

## 2. Why the leading map has a constant image line

Euler's identity gives
\[
JH_4(X)X=4H_4(X).
\tag{6}
\]
Choose a nonzero component \(h=(H_4)_j\).  Generic rank one makes every
\(d(H_4)_i\) proportional to \(dh\) over the function field.  If
\[
d(H_4)_i=\lambda_i\,dh,
\]
then (6) gives
\[
\lambda_i=(H_4)_i/h.
\]
Consequently
\[
d\bigl((H_4)_i/h\bigr)=0.
\]
The constant field of
\(\mathbb C(X_1,X_2,X_3)\) under all three coordinate derivations is
\(\mathbb C\), so every ratio is constant.  This proves (1).

Choose target coordinates with \(a=e_3\).  Then
\[
H_4=(0,0,h),\qquad
H_3=(P,Q,S)
\tag{7}
\]
for a third cubic form \(S\).

## 3. The quotient first-integral identity

Put
\[
A=JH_2,\qquad B=JH_3,\qquad C=JH_4.
\]
The homogeneous degree-seven part of the Keller determinant is
\[
3\Delta(A,C,C)+3\Delta(B,B,C)=0,
\tag{8}
\]
where \(\Delta\) is the polarized determinant.  The first term vanishes:
two copies of \(C=e_3(\nabla h)^T\) have the same one-dimensional image.
Moreover,
\[
3\Delta(B,B,C)
=\operatorname{tr}(\operatorname{adj}(B)C)
=\operatorname{Jac}(P,Q,h).
\]
Hence
\[
\boxed{\operatorname{Jac}(P,Q,h)=0.}
\tag{9}
\]
This identity is independent of \(H_2\), \(S\), and the arbitrary
invertible linear part.

If \(P,Q\) are linearly dependent, a nonzero target covector annihilates
both \(a\) and \(H_3\).  The corresponding target linear combination of
the components of \(F\) has degree at most two.  The quadratic-component
exit theorem therefore makes \(F\) an automorphism.  For completeness,
that theorem uses the following short reduction.  A quadratic polynomial
with nowhere-vanishing gradient is a polynomial coordinate via a
triangular change of degree at most two.  Making the selected component a
source coordinate turns \(F\) into \((G_1,G_2,X_3)\) of degree at most
eight.  Every plane fibre is Keller of degree at most eight and hence is
an automorphism by the unconditional plane lower bound; fibrewise
injectivity and Ax--Grothendieck finish the argument.  This proves part 1.

Assume from now on that \(P,Q\) are linearly independent.  Forms of the
same positive degree that are linearly independent are algebraically
independent.  Indeed, \(u=P/Q\) is nonconstant, and scaling fixes \(u\)
while sending \(Q\) to \(\lambda^3Q\); hence \(Q\) is transcendental over
\(\mathbb C(u)\).  In particular,
\[
D=\nabla P\times\nabla Q
\]
is nonzero, and (9) is \(D(h)=0\).

## 4. The degree-\((3,4)\) homogeneous first integral

Set
\[
u=P/Q,\qquad w=h^3/Q^4.
\tag{10}
\]
The function \(w\) has homogeneous degree zero.  It is algebraic over
\(\mathbb C(u)\).

To see this, the kernel of a nonzero derivation of
\(\mathbb C(X_1,X_2,X_3)\) has transcendence degree at most two.  The
kernel of \(D\) contains the algebraically independent \(P,Q\) and also
\(h\), so \(h\) is algebraic over \(\mathbb C(P,Q)\).  Therefore \(w\) is
algebraic over \(\mathbb C(u,Q)\).

Let
\[
E=\mathbb C(\mathbb P^2)
\]
be the degree-zero subfield.  The homogeneous element \(Q\) is
transcendental over \(E\), because scaling fixes \(E\) and produces
infinitely many multiples of \(Q\).  If \(w\) were transcendental over
\(\mathbb C(u)\), then \(u,w,Q\) would be algebraically independent,
contradicting the preceding algebraicity.  Thus \(w\) is algebraic over
\(\mathbb C(u)\).  Hypothesis (4) now gives
\[
w=\phi(u),\qquad \phi\in\mathbb C(u).
\tag{11}
\]

## 5. The effective base divisor

Let \(\infty\in\mathbb P^1\) denote the fibre \(Q=0\), and define
\[
\mathcal B=\operatorname{div}_{\mathbb P^1}(\phi)+4[\infty].
\tag{12}
\]
From (10)--(11),
\[
\boxed{
3\operatorname{div}_{\mathbb P^2}(h)=u^*\mathcal B.
}
\tag{13}
\]

There is no fixed prime divisor in the pencil by (3).  Consequently the
codimension-one pullback of a point \(t\in\mathbb P^1\) is precisely the
scheme-theoretic cubic fibre \(\alpha P+\beta Q=0\).  The base locus
\(\{P=Q=0\}\) is codimension two and contributes nothing to Weil
divisors, so it introduces no extra term in (13).

The divisor \(\mathcal B\) is effective.  Indeed, if \(b_t\) is its
coefficient at \(t\) and a prime component \(\Gamma\) occurs in the
cubic fibre over \(t\) with multiplicity \(m_\Gamma>0\), then (13) gives
\[
3\operatorname{ord}_\Gamma(h)=b_t m_\Gamma.
\tag{14}
\]
The left side is nonnegative, hence \(b_t\ge0\).  Also
\[
\deg\mathcal B=4.
\tag{15}
\]

At least one coefficient \(b_t\) is not divisible by three.  For such a
coefficient, (14) says that every component multiplicity
\(m_\Gamma\) is divisible by three.  Since the fibre has total degree
three, it must be
\[
\alpha P+\beta Q=cL^3
\tag{16}
\]
for a linear form \(L\).

## 6. Uniqueness and the exceptional normal form

There is at most one triple-line fibre.  Otherwise, after a Möbius change
of \(u\), two fibres would be
\[
P=c_0L_0^3,\qquad Q=c_1L_1^3.
\]
Then \(L_0/L_1\) is algebraic over \(\mathbb C(u)\).  Relative algebraic
closedness would put \(L_0/L_1\) in \(\mathbb C(u)\), but its cube is a
nonzero scalar multiple of \(u\).  This is impossible: the divisor of a
cube in \(\mathbb C(u)\) has all coefficients divisible by three, whereas
\(\operatorname{div}(u)\) has a simple zero and a simple pole.

Let \(t_0\) be the unique triple-line fibre.  Every coefficient of
\(\mathcal B\) away from \(t_0\) is divisible by three.  Combining this
with (15) leaves exactly two possibilities:
\[
\mathcal B=4[t_0],
\qquad\text{or}\qquad
\mathcal B=[t_0]+3[t_1]\quad(t_1\ne t_0).
\tag{17}
\]

In the first case, (13) and \(u^*[t_0]=3\operatorname{div}(L)\)
give
\[
h=cL^4.
\tag{18}
\]
In the second case, if \(R\) is the cubic member over \(t_1\), then
\[
\operatorname{div}(h)
=\operatorname{div}(L)+\operatorname{div}(R),
\]
and hence
\[
h=cLR.
\tag{19}
\]
Taking the triple-line member as the first pencil basis vector proves
(5).  This completes the proposition.

The exceptional form is sharp for the degree-seven identity alone.
Indeed, \(D(P)=D(L^3)=0\) implies \(D(L)=0\), while \(D\) kills every
member of \(\langle P,Q\rangle\).  Hence
\[
D\bigl(L(\alpha P+\beta Q)\bigr)=0.
\]

## 7. Boundary of the result

For \(H_2=0\), earlier determinant identities force
\((\nabla h)^Ta=0\).  That conclusion is false for arbitrary \(H_2\).
For example, the shear-composition automorphism
\[
\left(X_1+X_2^2,\,
X_2+(X_1+X_2^2)^2,\,
X_3\right)
\]
has
\[
H_4=e_2X_2^4,\qquad
D_{e_2}(X_2^4)=4X_2^3\ne0.
\]
Thus no invariance of the factors in (5) under the image direction \(a\)
is asserted here.

The remaining rank-one-leading work is to combine the lower homogeneous
Keller identities with (5), and separately to classify nonprimitive
projected cubic pencils.

## 8. Verification and disclosure

The accompanying exact checks verify the degree-seven determinant
identity and the formal satisfaction of that identity by (5).  They do
not verify the divisor argument or exclude the exceptional locus.

This note was developed with AI assistance.  Exact computer algebra is
evidence about the encoded identities, not peer review.  The result has
not been peer reviewed.
