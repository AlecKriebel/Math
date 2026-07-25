# Hostile audit: fixed-divisor verticality principle

## Verdict

**PASS after one fail-closed verifier correction.**  The mathematical
theorem, its three stated corollaries, and the exact \(e=2\) frontier
survive the audit.  No counterexample was found to the field descent,
horizontal valuation, determinant coefficient, or quadratic-component
exit.

The supplied PARI wrapper initially had two packaging defects:

1. it was not executable; and
2. it accepted output containing an explicit `FAIL` line provided the
   advertised success sentinel was last.

The wrapper now rejects PARI diagnostics and algebraic `FAIL` lines, is
executable, and has injected-failure tests for a forged failure, a PARI
diagnostic, trailing output, and a nonzero exit.  This correction changes
no mathematical statement.

## 1. Minimal pair versus relative algebraic closure

Let
\[
u=p/q,\qquad
L=\overline{\mathbb C(u)}^{\,\mathbb C(\mathbb P^2)}.
\]
The rational map from \(\mathbb P^2\) to the smooth curve with function
field \(L\) is nonconstant on a general line.  That curve is therefore
dominated by \(\mathbb P^1\), hence rational in characteristic zero.
Thus
\[
L=\mathbb C(r/s)
\]
for coprime equal-degree homogeneous \(r,s\).

If the containment \(\mathbb C(u)\subset L\) is proper, then
\[
u=\frac{A(r,s)}{B(r,s)}
\]
for coprime binary forms \(A,B\) of common degree \(n>1\).  There is no
hidden common divisor after substitution.  At the generic point of such a
divisor, either \(r,s\) both vanish, contradicting their coprimality, or
\([r:s]\) is a common projective zero of \(A,B\), contradicting their
coprimality.  Reduced-fraction uniqueness gives
\[
p=\lambda A(r,s),\qquad q=\lambda B(r,s),\qquad
a=n\deg r.
\]
Conversely, a composition with \(n>1\) gives the proper finite
characteristic-zero extension
\(\mathbb C(p/q)\subsetneq\mathbb C(r/s)\).

Consequently:

- \(a=1\): a coprime nonproportional pair is automatically minimal;
- \(a=2\): the only nonminimal case is a binary quadratic evaluated on a
  linear pair;
- \(a=3\): the only nonminimal case is a binary cubic evaluated on a
  linear pair.

This is exactly the equivalence asserted in the note.  It does not infer
minimality merely from line image.

## 2. Scaling descent

Put \(P=hp,Q=hq\), both of degree four.  They are algebraically
independent: source scaling splits any relation into homogeneous binary
relations, and a nonzero homogeneous binary relation over \(\mathbb C\)
factors into linear factors, one of which would make \(P,Q\)
proportional.

For homogeneous \(G\ne0\) of degree \(d\),
\[
\operatorname{Jac}(P,Q,G)=0
\]
therefore makes \(G\) algebraic over \(\mathbb C(P,Q)\).  With
\[
u=Q/P=q/p,\qquad \Theta=G^4/P^d,
\]
\(\Theta\) is algebraic over \(\mathbb C(u,P)\) and lies in the
degree-zero field \(K_0=\mathbb C(\mathbb P^2)\).

Choose a scaling coordinate \(s\).  Then
\[
\mathbb C(x,y,z)=K_0(s),\qquad P=s^4P_0,
\]
so \(P\) is transcendental over \(K_0\).  Clearing a relation for
\(\Theta\) over \(\mathbb C(u,P)\) and collecting powers of \(P\) gives
\[
\sum_j P^j b_j(\Theta)=0,\qquad b_j(T)\in\mathbb C(u)[T].
\]
Transcendence of \(P\) over \(K_0\) forces every coefficient to vanish.
At least one \(b_j\) is a nonzero polynomial, so \(\Theta\) is algebraic
over \(\mathbb C(u)\).  Relative algebraic closure gives
\[
\Theta=R(u),\qquad R\in\mathbb C(t).
\]
The argument never assumes that a degree-zero algebraic element
automatically belongs to the pencil field.

## 3. Horizontal divisor valuation

For the selected horizontal prime \(f\mid h\),
\[
v_f(p)=v_f(q-\lambda p)=0
\quad\text{for every }\lambda\in\mathbb C.
\]
In particular \(v_f(q)=0\).  A reduced rational function on
\(\mathbb P^1\) factors into finite linear factors, while the degree
difference records the zero or pole at infinity.  Thus every finite
factor \(u-\lambda=(q-\lambda p)/p\), and also the infinity factor
\(1/u=p/q\), has \(f\)-valuation zero.  Hence
\[
v_f(R(q/p))=0.
\]

This remains valid when a *different* prime factor of \(h\) is shared
with \(p\) or a pencil member.  The dependency-free audit includes
\[
h=yz,\qquad p=xz,\qquad q=x^2+y^2,
\]
where \(z\) is shared by \(h,p\) but the selected factor \(y\) is
horizontal.  It independently reproduces full cubic-kernel rank and
checks both finite and infinity factors in the valuation ledger.

Writing \(m=v_f(h)\), horizontality also gives \(v_f(P)=m\), so
\[
4v_f(G)=dm.
\]
For \(d=3\) and \(1\le m\le e\le3\), the right side is never divisible by
four.  Therefore the cubic normal component vanishes.  There is no
division by \(h\), a discriminant, or a leading coefficient.

## 4. Weight-eight coefficient and orientation

For
\[
JF(tX)=L_0+tJH_2+t^2JH_3+t^3JH_4,
\]
weight eight has only the row-weight pattern \(3+3+2\).  With row
convention
\[
JH_4=\begin{pmatrix}\nabla P\\ \nabla Q\\0\end{pmatrix},
\]
\[
\operatorname{adj}(JH_4)
 =(\nabla P\times\nabla Q)e_3^T.
\]
Consequently
\[
[t^8]\det JF(tX)
=\operatorname{tr}(\operatorname{adj}(JH_4)JH_3)
=\det(\nabla P,\nabla Q,\nabla(H_3)_3).
\]
The sign and row orientation are correct.  The independent modular audit
reconstructed this coefficient for 128 exact matrix samples.

## 5. Quadratic-component exit

Once \((H_3)_3=0\), the third component of \(F\) has degree at most two.
It is nonconstant because the third row of \(L_0=JF(0)\) is nonzero.
The banked quadratic-submersion lemma straightens it with an automorphism
and inverse of degree at most two.  Conjugating a degree-four map therefore
produces plane fibres of degree at most eight, not sixteen.

The unconditional plane lower bound excludes a counterexample on every
fibre.  Fibrewise injectivity and Ax--Grothendieck then give a polynomial
automorphism.  No form of the plane Jacobian Conjecture is assumed.

## 6. Corollary scope and the \(e=2\) frontier

The theorem is confined to
\[
H_4=(hp,hq,0),\qquad e+\deg p=4,
\]
with binary outer degree one and a minimal coprime pencil.  It does not
claim a statement for arbitrary quartic leading forms.

- For \(e=1\), the unique line factor of \(h\) must be vertical.
- For \(e=3,a=1\), a vertical prime divides a linear pencil member, hence
  is itself a linear member.  If every prime is vertical, all factors of
  \(h\) lie in \(\mathbb C[p,q]\), so \(h\in\mathbb C[p,q]\).
- For \(e=2\), the three frontier shapes are exhaustive:

  1. irreducible \(h\): a vertical quadratic member is proportional to
     \(h\);
  2. \(h=\ell^2\): the unique vertical prime gives a member
     \(\ell m\);
  3. \(h=\ell_1\ell_2\): if the two unique vertical members coincide,
     that member is \(h\); if they differ, they form a pencil basis
     \[
     p=\ell_1m_1,\qquad q=\ell_2m_2.
     \]

  A prime cannot divide two different members because then it divides
  \(\gcd(p,q)\).  There is no omitted incidence case.

The vertical witness
\[
h=p=z^2,\qquad q=x^2+y^2,\qquad G_3=z^3
\]
is minimal: the generic conic is smooth and geometrically integral.  It
correctly demonstrates only that the horizontal hypothesis is sharp for
the top identity, not the existence of a Keller map.

## 7. Independent verification

The following all pass:

```text
/usr/bin/python3 verify_fixed_divisor_verticality_sympy.py
./verify_fixed_divisor_verticality_pari_strict.sh
/usr/bin/python3 audit_hostile/audit_reconstruct_modp.py
./audit_hostile/test_supplied_runners.sh
```

The modular reconstruction uses no computer-algebra dependency.  It checks
all three rows, the mixed shared-factor degeneration, finite and infinite
valuation factors, the vertical witness, and the \(E_8\) orientation.  The
runner test confirms rejection of optimized Python, forged algebraic
failure, PARI diagnostics, trailing output, and nonzero exits.

Exact checks are evidence about the encoded algebra, not peer review.
