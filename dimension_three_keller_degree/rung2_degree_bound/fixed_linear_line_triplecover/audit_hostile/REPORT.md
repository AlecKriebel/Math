# Hostile audit: transverse fixed-linear line triple cover

## Verdict

**PASS**, conditional on the already-banked homogeneous rank-two taxonomy
factorization and the established low-degree plane Keller theorem.  No
omitted specialization or counterexample was found.

## Taxonomy and left-right normalization

The row
\[
(e,a,b,\delta,\nu)=(1,1,3,1,3)
\]
gives
\[
H_4=h\,A_{\rm out}(p,q),
\]
where \(h\) is linear, \(p,q\) are independent linear forms, and the
coprime outer binary triple has degree three and line image.  A target
change sends that line to the first two coordinates, giving
\[
H_4=h(A(p,q),B(p,q),0),
\]
with \(A,B\) coprime binary cubics.

There is no unique cubic analogue of the squaring normal form: degree-three
covers have left-right moduli.  The theorem correctly retains completely
general \(A,B\), so no cover orbit is omitted.  Coprimality makes
\([A:B]\) a degree-three morphism.

The transverse condition \(h\notin\langle p,q\rangle\) says exactly that
\(p,q,h\) form a basis.  Keeping \(p,q\) and taking \(r=h\) gives
\[
H_4=r(A,B,0).
\]
For a linear fixed divisor, this is precisely the nonbinary locus.  The
binary locus \(h\in\langle p,q\rangle\) is not reached by the proof and is
not claimed.

## Cross product and Wronskian cancellation

On \(q=pt,r=ps\), write
\[
A=p^3a(t),\qquad B=p^3b(t),\qquad
w=ab'-a'b.
\]
Direct differentiation gives
\[
\nabla(rA)\times\nabla(rB)
=p^6s\,w(-1,-t,3s).
\]
The sign and exponent \(p^6\) were independently recomputed and checked by
PARI/GP.

For \(G=p^dg(t,s)\),
\[
\begin{aligned}
G_p&=p^{d-1}(dg-tg_t-sg_s),\\
G_q&=p^{d-1}g_t,\qquad
G_r=p^{d-1}g_s.
\end{aligned}
\]
Taking the dot product gives exactly
\[
D(G)=p^{d+5}s\,w(4sg_s-dg).
\]

The Wronskian need not be a unit.  If \(w=0\), then
\((a/b)'=0\) in \(\mathbb C(t)\), so \(a/b\in\mathbb C\) in
characteristic zero, contradicting the degree-three cover.  Thus \(w\) is
a nonzero polynomial.  After setting \(p=1\), the determinant identity is
\[
s\,w(t)(4sg_s-dg)=0
\]
in the integral domain \(\mathbb C[t,s]\).  Cancelling the nonzero product
\(sw\) is therefore valid even at its geometric zero set; no localization
or assumption that \(w\) is a unit is used.

## Polarized determinant identities

With weights \(1,2,3\) on \(JH_2,JH_3,JH_4\):

- \(E_8\) has only type \(3+3+2\).  Since the third row of \(JH_4\) is
  zero, the unique nonzero row assignment is
  \[
  E_8=\det(\nabla P,\nabla Q,\nabla(H_3)_3)=D((H_3)_3).
  \]
- After \((H_3)_3=0\), both \(JH_4\) and \(JH_3\) have zero third row.
  Every \(3+2+2\) polarization in \(E_7\) vanishes.  The remaining
  \(3+3+1\) term is
  \[
  E_7=\det(\nabla P,\nabla Q,\nabla(H_2)_3)=D((H_2)_3).
  \]

Independent matrices with algebraically independent entries reproduce both
coefficients with no missing numerical factor or sign.

## Eigenvalue argument

For an arbitrary homogeneous form, write
\[
g(t,s)=\sum_j c_j(t)s^j.
\]
The operator \(4s\partial_s-d\) acts diagonally with eigenvalues \(4j-d\).
For \(d=3\) and \(d=2\), no nonnegative integer \(j\) gives zero.
Consequently
\[
(H_3)_3=(H_2)_3=0.
\]
Dehomogenization is injective on homogeneous forms, so no polynomial
supported on the omitted chart \(p=0\) escapes this conclusion.

## Plane-field exit

The third component is now a nonzero linear form; invertibility of \(L_0\)
ensures it is nonzero.  Linear changes give
\[
F=(R,S,r),\qquad
\partial(R,S)/\partial(p,q)\in\mathbb C^\times.
\]
Over \(K=\mathbb C(r)\), the plane map has degree at most four.  The known
low-degree plane theorem applies over \(\overline K\): a failure there
would be defined over a finitely generated characteristic-zero field and,
after embedding in \(\mathbb C\), would contradict the complex theorem.
Generic degree is preserved by algebraic base change, so
\[
K(p,q)=K(R,S).
\]
Thus the three-variable map is birational, and the birational Keller
theorem makes it an automorphism.  This does not inherit or assume the
general plane Jacobian conjecture.

## Verifier audit

- The SymPy verifier uses all eight binary-cubic coefficients and all
  degree-two and degree-three monomials.  Its polarization matrices are
  algebraically independent.
- Optimized Python is rejected before checks run.
- The supplied GP wrapper passed injected-diagnostic, trailing-output, and
  nonzero-exit tests.
- The audit GP verifier additionally checks the full \(p^6\) and
  \(p^{d+5}\) identities before setting \(p=1\), as well as both raw
  polarizations.

Recommended exposition clarifications, none theorem-breaking:

1. Say explicitly that general cubic covers retain moduli and that \(A,B\)
   are not being normalized to a special cubic pair.
2. State the integral-domain cancellation of the nonunit Wronskian.
3. Define formulas (5)--(6) explicitly as identities after
   \(q=pt,r=ps\), which makes the powers of \(p\) unambiguous.
4. Add the base-change/generic-degree descent sentence to the plane exit.

Audit marker:
`AUDIT_FIXED_LINEAR_TRIPLECOVER_PARI_PASS_9B6E20`.
