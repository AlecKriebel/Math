# Working theorem: primitive quotient pencils in the rank-one quartic stratum

**Status:** proved and independently adversarially audited.  The audit found
and repaired an omitted arbitrary-linear-part term in degree five.  This is
not peer reviewed.  The source-specific priority search found no exact prior
statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T01:24:00Z.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
be a total-degree-four Keller map, with \(L_0\) invertible and \(H_i\)
homogeneous of degree \(i\).  Suppose that \(H_4\ne0\) and
\(\operatorname{rank}JH_4=1\).  Thus
\[
H_4=a\,h
\]
for a constant target vector \(a\ne0\) and a quartic form \(h\).

Project \(H_3\) to \(\mathbb C^3/\mathbb Ca\), and let \(P,Q\) be two
quotient coordinates.  Assume
\[
\gcd(P,Q)=1,\qquad
\mathbb C(P/Q)\text{ is relatively algebraically closed in }
\mathbb C(\mathbb P^2).
\tag{1}
\]
Equivalently, the cubic pencil has no fixed curve and has geometrically
integral generic member.

### Theorem

Under (1), \(F\) is a polynomial automorphism.

Together with `WORKING_RANK_ONE_QUOTIENT_CUBIC.md`, this says that any
quartic Keller counterexample with rank-one leading Jacobian must have a
nonprimitive projected cubic pencil.  The theorem does not classify that
remaining nonprimitive locus.

## 2. The exceptional degree-seven normal form

The preceding quotient-cubic theorem proves that linearly dependent
\(P,Q\) already give an automorphism.  In the independent case, the
degree-seven Keller identity is
\[
\operatorname{Jac}(P,Q,h)=0.
\]
Its vertical-divisor argument shows that, after independent invertible
linear changes in source and target,
\[
H_4=(0,0,h),\qquad H_3=(P,Q,R),\qquad H_2=(S,T,U),
\tag{2}
\]
where
\[
P=x^3,\qquad
h=x(\mu P+\nu Q)=\mu x^4+\nu xQ,
\qquad (\mu,\nu)\ne(0,0).
\tag{3}
\]
The linear part remains arbitrary and invertible.  These independent
changes preserve the Keller property and total degree.

Put
\[
D(f)=\operatorname{Jac}(P,Q,f).
\tag{4}
\]
Then
\[
D(x)=D(P)=D(Q)=0.
\tag{5}
\]

## 3. Degree six

The homogeneous degree-six determinant coefficient is
\[
\begin{split}
E_6={}&D(R)
+\operatorname{Jac}(P,T,h)
+\operatorname{Jac}(S,Q,h)\\
={}&D(R)-\nu xD(T)
-\frac{4\mu}{3}xD(S)-\frac{\nu Q}{3x^2}D(S).
\end{split}
\tag{6}
\]
Although the last display is written rationally, the first line is
polynomial.  Define the quintic
\[
K=3x^2R-3\nu x^3T-4\mu x^3S-\nu QS.
\tag{7}
\]
Equations (5)--(7) give the polynomial identity
\[
D(K)=3x^2E_6.
\tag{8}
\]
The Keller condition therefore implies \(D(K)=0\).

Assume first that \(K\ne0\).  The degree-zero first integral
\[
\frac{K^3}{Q^5}
\]
lies in \(\mathbb C(P/Q)\), by the same kernel and relative-closure
argument used in the quotient-cubic theorem.  Its divisor gives
\[
3\operatorname{div}(K)=(P/Q)^*\mathcal B
\tag{9}
\]
for an effective divisor \(\mathcal B\) of degree five on the pencil
base.

The pencil has at most one triple-line member.  It already has the member
\(P=x^3\).  Every coefficient of \(\mathcal B\) not divisible by three
must be supported there.  The only resulting partitions of five are
\[
\mathcal B=5[P]
\quad\text{or}\quad
\mathcal B=2[P]+3[C],
\tag{10}
\]
where \(C\) is another cubic member.  Consequently
\[
K=cx^5
\quad\text{or}\quad
K=cx^2C.
\tag{11}
\]
The conclusion \(x^2\mid K\) also holds when \(K=0\).

Suppose \(\nu\ne0\).  In (7), every term other than \(-\nu QS\) is
divisible by \(x^2\).  Since \(\gcd(x,Q)=1\), (11) forces
\[
x^2\mid S.
\tag{12}
\]
As \(S\) is quadratic, \(S=cx^2\).

## 4. The pure fourth-power case

It remains to treat \(\nu=0\), so \(\mu\ne0\).  Equation (8) now gives
\[
D(3R-4\mu xS)=0.
\tag{13}
\]
The expression in parentheses is cubic.  Applying the degree-\((3,3)\)
first-integral argument shows
\[
3R-4\mu xS\in\langle P,Q\rangle.
\tag{14}
\]
A target row operation subtracting the corresponding combination of the
first two components from the third preserves (2)--(3), and lets us
assume
\[
R=\frac{4\mu}{3}xS.
\tag{15}
\]

With (15), the homogeneous degree-five determinant coefficient simplifies
to
\[
E_5=D(U)+\frac{4\mu}{3}S
       (S_yQ_z-S_zQ_y)
       -\frac{4\mu}{3}xD(\ell_0),
\tag{16}
\]
where \(\ell_0\) is the first linear component of \(L_0X\).  The last
term is essential: it is the surviving
\(6\Delta(L_0,JH_3,JH_4)\) contribution.  The other mixed linear term,
\(\operatorname{Jac}(P,(L_0X)_2,\mu x^4)\), vanishes because
\(\nabla P\) and \(\nabla x^4\) are parallel.

Set
\[
W=9x^2U-2\mu S^2-12\mu x^3\ell_0.
\tag{17}
\]
Directly from (4),
\[
D(W)=9x^2E_5.
\tag{18}
\]
Thus \(D(W)=0\).

If \(W\ne0\), the degree-\((3,4)\) divisor argument produces an effective
base divisor of degree four.  Since \(P=x^3\) is the pencil's unique
triple-line member, the only possibilities are
\[
W=cx^4
\quad\text{or}\quad
W=cxC
\tag{19}
\]
for a cubic member \(C\).  In particular \(x\mid W\); this is also true
when \(W=0\).  Reducing (17) modulo \(x\) gives
\[
x\mid S.
\tag{20}
\]
Write \(S=xM\), with \(M\) linear.

## 5. The selected cubic component is a coordinate

In both cases, the full target component whose cubic part is \(P=x^3\)
has the form
\[
f=x^3+xM+\ell
\tag{21}
\]
for linear forms \(M,\ell\).  In the case \(\nu\ne0\), (12) is the
special case \(M=cx\).

Because \(F\) is Keller, \(df\) is nowhere zero.  This forces \(f\) to be
a polynomial coordinate, with a coordinate change and inverse both of
degree at most three:

- If \(M\) is proportional to \(x\), write
  \(f=g(x)+\ell_\perp\), where \(\ell_\perp\) is the part of \(\ell\)
  transverse to \(x\).  If \(\ell_\perp=0\), the univariate derivative
  \(g'\) has a complex root, contradicting \(df\ne0\).  Otherwise, take
  \(\ell_\perp\) and a complementary transverse linear form as the other
  two coordinates.
- If \(M\) is not proportional to \(x\), use linear coordinates
  \(x,y=M,z\).  Then
  \[
  f=x^3+xy+\alpha x+\beta y+\gamma z.
  \]
  If \(\gamma=0\), the point
  \[
  x=-\beta,\qquad y=-3\beta^2-\alpha
  \]
  is critical.  Hence \(\gamma\ne0\), and \((x,y,f)\) is a triangular
  polynomial coordinate system.

Let \(T\) be such a coordinate automorphism with first coordinate \(f\).
Then
\[
G=F\circ T^{-1}
\]
has first component \(X_1\), is Keller, and has degree at most
\[
\deg F\cdot\deg T^{-1}\le4\cdot3=12.
\tag{22}
\]
For every \(c\in\mathbb C\), the restriction of the last two components
of \(G\) to \(X_1=c\) is a plane Keller map of degree at most twelve.
The unconditional plane lower bound for counterexamples makes every such
fibre map an automorphism.  Therefore \(G\) is injective: two points with
the same image first have the same \(X_1\), and then agree in that plane
fibre.  Ax--Grothendieck makes \(G\), and hence \(F\), a polynomial
automorphism.

## 6. Verification boundary and disclosure

The accompanying exact scripts verify (8) and (18) from generic
homogeneous forms with an arbitrary linear part and independently check the
coordinate critical-point calculation.  They do not verify relative
algebraic closedness or the divisor classifications (10), (19).

The adversarial audit reconstructed every normalization, first-integral
partition, and coordinate-exit step.  It caught that an earlier draft of
(16) had silently used \(L_0=I\).  Retaining the mixed
\(6\Delta(L_0,JH_3,JH_4)\) term produces the correction
\(-12\mu x^3\ell_0\) in (17); the reduction modulo \(x\), and hence the
theorem, remain unchanged.

This proof was developed with AI assistance.  Exact computer algebra is
evidence about the encoded identities, not peer review.  This theorem has
not been peer reviewed.
