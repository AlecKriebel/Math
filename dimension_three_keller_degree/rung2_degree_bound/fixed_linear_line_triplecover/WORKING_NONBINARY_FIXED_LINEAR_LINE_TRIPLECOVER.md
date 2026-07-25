# Working theorem: the nonbinary fixed-linear line triple-cover stratum

**Status:** proved by exact homogeneous identities, checked by independent
SymPy and PARI/GP implementations, and independently adversarially
reconstructed.  This is not peer reviewed.  The source-specific priority
search found no exact prior statement and is not a guarantee of worldwide
priority.

**Recorded:** 2026-07-25T05:29:53Z.

**Promoted after audit:** 2026-07-25T05:47:58Z.

## 1. Statement and scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, where \(H_i\) is homogeneous of degree \(i\) and
\(L_0\in\operatorname{GL}_3(\mathbb C)\).  Suppose that the leading map is
in the taxonomy row
\[
(e,a,b,\delta,\nu)=(1,1,3,1,3).
\]
Thus, after independent linear source and target changes,
\[
H_4=h\bigl(A(p,q),B(p,q),0\bigr)^T,                       \tag{1}
\]
where \(p,q,h\) are linear, \(A,B\) are coprime binary cubics, and
\(A/B:\mathbb P^1\to\mathbb P^1\) has degree three.
Degree-three covers have genuine left-right moduli; no special cubic pair
is imposed here.  The forms \(A,B\) remain completely general throughout.

Assume that the fixed linear divisor is transverse to the minimal pencil:
\[
h\notin\langle p,q\rangle.                               \tag{2}
\]

### Theorem

Every Keller map satisfying (1)--(2) is a polynomial automorphism.  In
particular, no degree-four Keller counterexample lies in the entire
nonbinary part of the fixed-linear line triple-cover row.

The theorem does not treat the binary locus \(h\in\langle p,q\rangle\).

## 2. Normal form and the top derivation

Condition (2) makes \(p,q,h\) a basis of the source linear forms.  Write
them as coordinates \(p,q,r\), with \(h=r\), and put
\[
P=rA(p,q),\qquad Q=rB(p,q),\qquad H_4=(P,Q,0)^T.           \tag{3}
\]
Let
\[
D=\nabla P\times\nabla Q.
\]
On the chart \(p\ne0\), set
\[
t=q/p,\qquad s=r/p,\qquad
A=p^3a(t),\qquad B=p^3b(t).
\]
The nonconstant ratio \(A/B\) implies
\[
w(t):=a(t)b'(t)-a'(t)b(t)\ne0.                            \tag{4}
\]
A direct calculation gives
\[
\boxed{
D=p^6s\,w(t)(-1,-t,3s).
}                                                          \tag{5}
\]
This means the identity obtained after substituting \(q=pt,r=ps\);
retaining \(p\) gives the displayed homogeneous power.

If \(G=p^dg(t,s)\) is homogeneous of degree \(d\), Euler's identity and
(5) give the exact formula
\[
\boxed{
D(G)=p^{d+5}s\,w(t)\bigl(4s\,g_s-dg\bigr).
}                                                          \tag{6}
\]
No division by a coefficient or by a possibly vanishing lower component
is involved.

## 3. Degree eight kills the cubic normal component

Put \(G_3=(H_3)_3\).  Since the third row of \(JH_4\) is zero, the
degree-eight homogeneous part of the Keller determinant is
\[
E_8=\operatorname{Jac}(P,Q,G_3)=D(G_3).                   \tag{7}
\]
Write
\[
G_3=p^3g_3(t,s).
\]
Equations (4), (6), and (7), in the domain
\(\mathbb C[t,s]\), imply
\[
4s(g_3)_s=3g_3.                                           \tag{8}
\]
Here \(w\) need not be a unit.  If \(w=0\), then
\((a/b)'=0\), contradicting the nonconstant cover in characteristic zero.
Thus \(sw\ne0\) in the integral domain \(\mathbb C[t,s]\), where its
cancellation is valid.
For a monomial \(s^j\), the operator on the left minus the right has
eigenvalue \(4j-3\).  It has no zero eigenvalue on
\(\mathbb C(t)[s]\).  Therefore
\[
\boxed{(H_3)_3=0.}                                        \tag{9}
\]

This is also the logarithmic-valuation obstruction at the transverse
factor \(r\): an \(r\)-adic order \(v\) would have to satisfy \(4v=3\).

## 4. Degree seven kills the quadratic normal component

Now the third rows of both \(JH_4\) and \(JH_3\) vanish.  In degree seven,
the polarization of type \(3+2+2\) is consequently zero, and the only
surviving type is \(3+3+1\).  Hence, with
\(G_2=(H_2)_3\),
\[
E_7=\operatorname{Jac}(P,Q,G_2)=D(G_2).                   \tag{10}
\]
Writing \(G_2=p^2g_2(t,s)\), equations (6) and (10) give
\[
4s(g_2)_s=2g_2.                                           \tag{11}
\]
The eigenvalues \(4j-2\) are nonzero for every integer \(j\ge0\), so
\[
\boxed{(H_2)_3=0.}                                        \tag{12}
\]
Equivalently, the required transverse valuation would be \(2v=1\).

## 5. Plane-field exit

Equations (3), (9), and (12) say that the third component of \(F\) is a
linear form.  It is nonzero because \(\det L_0\ne0\).  After linear source
and target changes,
\[
F=(R(p,q,r),S(p,q,r),r),
\]
and
\[
\frac{\partial(R,S)}{\partial(p,q)}\in\mathbb C^\times.
\]
Regard \(R,S\) as a plane Keller map over \(\mathbb C(r)\).  Its degree in
\(p,q\) is at most four.  The unconditional established plane
low-degree theorem, after base change to an algebraic closure of
\(\mathbb C(r)\), makes this plane map birational.  Hence \(F\) is
birational, and the birational Keller theorem makes \(F\) a polynomial
automorphism.

For clarity, a failure after base change would be defined over a finitely
generated characteristic-zero field and could be embedded in
\(\mathbb C\), contradicting the complex low-degree theorem.  Generic
degree is invariant under algebraic base change, so degree one descends
back to \(\mathbb C(r)\).

This exit uses a proved low-degree plane result; it does not assume the
plane Jacobian Conjecture.

## 6. Verification and disclosure

`verify_nonbinary_fixed_linear_line_sympy.py` checks (5)--(6) with generic
binary cubics, checks the absence of degree-two and degree-three polynomial
eigenvectors, and reconstructs the degree-eight and degree-seven
polarizations from a symbolic determinant.

`verify_nonbinary_fixed_linear_line_pari.gp`, run through the strict shell
wrapper, independently checks the generic derivation formula and both
determinant coefficients in PARI/GP.

These exact checks are evidence about the encoded algebra, not peer review.
AI systems materially assisted the discovery, symbolic derivation,
verification code, and exposition.  The hostile audit retained all cubic
cover moduli, recomputed both chart identities and polarizations, checked
integral-domain cancellation and base-change descent, and fault-tested both
verification guards.  Every theorem assertion remains subject to
independent human checking.
