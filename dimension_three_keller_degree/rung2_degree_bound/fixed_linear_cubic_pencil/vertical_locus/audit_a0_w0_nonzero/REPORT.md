# Hostile audit of the \(a=0,\ W_0\ne0\) vertical companion

**Verdict: PASS, unchanged.**  The candidate exclusion in
`../a0_w0_nonzero_attack/NOTE.md` is correct on its stated locus.  No
counterexample, omitted root type, hidden free-parameter divisor, or
minimal/nonminimal scope leak was found.

The exact conclusion is:
\[
E_6=0,\quad W_0\ne0
\quad\Longrightarrow\quad
q\in\operatorname{Sym}^3\langle z,L\rangle
\]
for a nonzero binary linear form \(L\).  This is precisely the
nonminimal boundary of a coprime cubic pencil containing \(z^3\).
Consequently there is no point of this leaf when \((z^3,q)\) is the
minimal pair.

This audit was reconstructed before reading the candidate's selected six
coefficients.  The standalone certificate in this folder uses a new
dependency-free sparse polynomial implementation and forms the literal
weighted determinant
\[
\det(L+tJH_2+t^2JH_3+t^3JH_4).
\]
It neither imports the candidate scripts nor the sparse kernel imported
by one of them.

## 1. Audited setup

The branch is
\[
\begin{aligned}
H_4&=(z^4,zq,0)^T,\\
H_3&=\left(\frac43zW,V,z^3\right)^T,\\
H_2&=(A,B,W)^T,
\end{aligned}
\]
with \(q,A,B,W,V\) initially dense and all nine entries of the constant
linear matrix \(L\) retained.  The assumptions used by the proof are:

1. the coefficient field is \(\mathbb C\);
2. \(z\nmid q\), equivalently \(q_0=q|_{z=0}\ne0\), as follows from
   coprimality of \((z^3,q)\);
3. this leaf has \(W_0=W|_{z=0}\ne0\);
4. the complete \(E_7\) gauge has set \(U=\frac43zW\).

Invertibility of \(L\), \(E_5\), \(E_4\), a discriminant, and every
possibly-zero lower jet are unused.

## 2. Independent raw \(E_6\) reconstruction

Write \(L_3\) for the third linear row and
\(\{f,g\}=f_xg_y-f_yg_x\).  Literal row multilinearity gives
\[
\begin{aligned}
E_6={}&
\operatorname{Jac}(z^4,zq,L_3)
+\operatorname{Jac}\!\left(\frac43zW,zq,W\right)
+\operatorname{Jac}(z^4,V,W)\\
&+\operatorname{Jac}(A,zq,z^3)
+\operatorname{Jac}\!\left(\frac43zW,V,z^3\right)
+\operatorname{Jac}(z^4,B,z^3).
\end{aligned}
\]
The last summand is zero.  The two \(V\)-summands are
\[
4z^3\{V,W\}\quad\text{and}\quad4z^3\{W,V\},
\]
so they cancel without specializing \(V\).  The remaining terms give
\[
\boxed{
3E_6=z\Phi,\qquad
\Phi=4W\{q,W\}+9z^2\{A,q\}+12z^3\{q,L_3\}.
}
\]
Equivalently,
\[
\boxed{
E_6=\frac z3\{q,\,2W^2-9z^2A+12z^3L_3\}.
}
\]

The independent sparse expansion has 186 nonzero terms and fingerprint
`66315d214e861b16738ae96b840e1c857a794e21367d445e21cc7ba3536cb625`.
It agrees both with the exterior expansion above and with the one-bracket
form.  It also verifies \(E_9=E_8=E_7=0\) in the gauged family.  All
coefficients of \(B,V,L_1,L_2\) enter the full raw determinant; their
absence from \(E_6\) is verified cancellation rather than prior
specialization.

The factor \(z/3\) loses nothing: \(\mathbb C[x,y,z]\) is a domain and
three is a unit.  Thus \(E_6=0\) is equivalent to \(\Phi=0\).

## 3. Binary bracket and the sole surviving root type

Taking the \(z^0\)-part of \(\Phi\) gives
\[
4W_0\{q_0,W_0\}=0.
\]
Because \(W_0\) is a nonzero polynomial,
\[
\{q_0,W_0\}=0.
\]

There is no missing squarefree or collision case in the next step.  For
nonzero binary forms \(f,g\) of degrees three and two, Euler's identities
give
\[
\begin{aligned}
2g f_x-3f g_x&=y\{f,g\},\\
2g f_y-3f g_y&=-x\{f,g\}.
\end{aligned}
\]
Hence \(\{f,g\}=0\) makes \(f^2/g^3\) constant.  Unique factorization
then gives \(2\,\operatorname{ord}_P(f)=
3\,\operatorname{ord}_P(g)\) at every irreducible factor \(P\).  The
degrees force one linear form \(L\) and nonzero constants
\(\kappa,\gamma\):
\[
\boxed{q_0=\kappa L^3,\qquad W_0=\gamma L^2,\qquad
\kappa\gamma\ne0.}
\]

Here every nonzero assertion is justified:

- \(q_0\ne0\) gives \(\kappa\ne0\) and \(L\ne0\);
- \(W_0\ne0\) gives \(\gamma\ne0\);
- a binary change sending \(L\) to \(x\) extends by fixing \(z\), so it
  preserves the triple-vertical form \(z^3\).

Thus all squarefree and double-root \(q_0\) strata are already excluded.
The only binary survivor is the coincident triple root of \(q_0\) and
double root of \(W_0\).

## 4. The six-coefficient elimination

After sending \(L\) to \(x\), retain both nonzero leading scalars and all
lower jets:
\[
\begin{aligned}
q={}&\kappa x^3+
z(\alpha x^2+\beta xy+\chi y^2)
+z^2(\delta x+\epsilon y)+\phi z^3,\\
W={}&\gamma x^2+z(ux+vy)+\omega z^2,\\
A={}&a_{20}x^2+a_{11}xy+a_{02}y^2
+z(a_{10}x+a_{01}y)+a_{00}z^2.
\end{aligned}
\]
An independent \(z\)-adic triangular scan of the complete \(\Phi\), not
the candidate coefficient list, produced the following six coefficients:
\[
\begin{aligned}
[x^3yz]\Phi={}&-16\chi\gamma^2,\\
[x^4z]\Phi={}&4\gamma(-2\beta\gamma+3\kappa v),\\
[x^2yz^2]\Phi={}&-2(27\kappa a_{02}+2\beta\gamma v
+12\chi\gamma u-6\kappa v^2),\\
[y^2z^3]\Phi={}&-2(9a_{02}\beta-9a_{11}\chi
-2\beta v^2+4\chi uv),\\
[x^3z^2]\Phi={}&-27\kappa a_{11}+8\alpha\gamma v
-12\beta\gamma u-8\epsilon\gamma^2+12\kappa uv,\\
[yz^4]\Phi={}&-9a_{01}\beta-18a_{02}\delta+18a_{10}\chi
+9a_{11}\epsilon+12\beta\ell_{32}+4\beta v\omega\\
&\quad-24\chi\ell_{31}-8\chi u\omega
+4\delta v^2-4\epsilon uv.
\end{aligned}
\]

The elimination is valid on every parameter divisor.  First
\(\chi=0\).  Define
\[
\begin{aligned}
r&=2\beta\gamma-3\kappa v,\\
f&=27\kappa a_{02}+2\beta\gamma v-6\kappa v^2,\\
g&=9a_{02}-v^2,\\
h&=9a_{02}\beta-2\beta v^2.
\end{aligned}
\]
The next three equations give \(r=f=h=0\), and the exact identities
\[
f-vr=3\kappa g,\qquad h-\beta g=-\beta v^2
\]
give \(g=0\) and \(\beta v^2=0\).  Multiplying \(r=0\) by
\(v^2\), rather than dividing by \(v\) or \(\beta\), yields
\(-3\kappa v^3=0\).  Since the base is the reduced field
\(\mathbb C\) and \(\kappa\ne0\),
\[
v=\beta=a_{02}=0.
\]

The last two equations now give
\[
27\kappa a_{11}+8\gamma^2\epsilon=0,\qquad
9a_{11}\epsilon=0.
\]
Multiplying the first by \(\epsilon\) and subtracting
\(3\kappa\) times the second gives \(8\gamma^2\epsilon^2=0\).
Therefore
\[
\epsilon=a_{11}=0.
\]

The complete divisor ledger is:

| inference | divisor used | why it is a unit |
|---|---:|---|
| \(\chi=0\) | \(16\gamma^2\) | \(\gamma\ne0\) from \(W_0\ne0\) |
| \(r=0\) | \(4\gamma\) | same |
| \(g=0\) | \(3\kappa\) | \(\kappa\ne0\) from \(q_0\ne0\) |
| \(v=0\) | \(3\kappa\), then radicality | \(\kappa\ne0\), base field \(\mathbb C\) |
| \(\beta=0\) | \(2\gamma\) | \(\gamma\ne0\) |
| \(\epsilon=0\) | \(8\gamma^2\), then radicality | \(\gamma\ne0\), base field \(\mathbb C\) |
| \(a_{11}=0\) | \(27\kappa\) | \(\kappa\ne0\) |

There is no division by
\(\alpha,\beta,\chi,\delta,\epsilon,u,v,\omega\), any coefficient of
\(L\), a discriminant, or a determinant.  In particular, the loci
\(v=0\), \(\beta=0\), and \(\epsilon=0\) are included rather than
discarded.  The candidate phrase “parameter-division-free” is correct in
the intended fail-closed sense of “no possibly-zero parameter”; the two
structural units \(\kappa,\gamma\) are used explicitly.

## 5. Why the survivor is exactly the nonminimal boundary

The eliminated coefficients are exactly all \(y\)-bearing coefficients
of the cubic \(q\):
\[
\boxed{
q=\kappa x^3+\alpha x^2z+\delta xz^2+\phi z^3
\in\operatorname{Sym}^3\langle x,z\rangle.
}
\]
This is not merely a convenient degenerate sample.

If \(q\in\operatorname{Sym}^3\langle z,L\rangle\), then with
\(r=L/z\),
\[
\frac q{z^3}=P(r)
\]
for a degree-three polynomial \(P\), because \(\kappa\ne0\).  Thus
\(\mathbb C(P(r))\subsetneq\mathbb C(r)\), with degree three, so
\(\mathbb C(z^3/q)\) is not relatively algebraically closed in
\(\mathbb C(\mathbb P^2)\).  The pencil is nonminimal.

Conversely, the minimalization degree divides the degree of the coprime
cubic pair.  Since three is prime, a nonminimal cubic pair factors
through a degree-one pencil and both generators are binary cubics in a
two-dimensional space of linear forms.  If one generator is \(z^3\),
that space contains \(z\), so it is \(\langle z,L\rangle\).  Hence
\[
q\in\operatorname{Sym}^3\langle z,L\rangle
\]
is exactly, not just a subset of, the nonminimal boundary.  It is
correctly reclassified into the \((a,b)=(1,3)\) row.

## 6. Counterexample and scope attacks

The following attacks were made.

- **Drop \(W_0\ne0\).**  With
  \(q=x^3+y^3,\ W=A=B=V=0,\ L=I\), one has
  \[
  \det(L+tJH_2+t^2JH_3+t^3JH_4)
  =(1+3t^2z^2)(1+3t^3y^2z).
  \]
  Thus \(E_6=0\) on a minimal \(W_0=0\) point.  This confirms that the
  audited theorem must not be extended to the separate zero-\(W_0\)
  leaf.

- **Drop minimality.**  The candidate's witness
  \(q=x^3,\ W=x^2,\ A=B=V=0,\ L=I\) gives
  \[
  1+\frac{t^2}{3}z(8x+9z)-\frac{8t^3}{3}x^3.
  \]
  It survives \(E_8,\ldots,E_4\) and fails only below.  This sharply
  confirms that the binary survivor is a genuine reclassification
  boundary, not an algebraic contradiction.

- **Change the \(E_7\) gauge.**  Replacing \(\frac43zW\) by \(zW\)
  breaks the raw factorization and is rejected.

- **Reverse the first bracket, omit \(\chi y^2z\), forget
  \(\gamma\ne0\), or run under optimized Python.**  Each deliberate
  mutation fails through a named independent guard.

- **Free-tail search.**  The factors
  \(\alpha,\delta,\phi,u,\omega,a_{20},a_{10},a_{01},a_{00},
  \ell_{31},\ell_{32},\ell_{33}\) remain symbolic throughout.  None
  creates a rank divisor in the six-step elimination.

No attack produced a minimal \(W_0\ne0\) survivor.

## 7. Certificates and reproducibility

Run:

```sh
./verify_strict.sh
```

from this audit directory.  The terminal markers are:

```text
A0_W0_NONZERO_INDEPENDENT_PASS_7C2E19
A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D
```

The strict harness runs the exact certificate, four fail-closed
mutations, and the optimized-Python guard.  At audit completion:

```text
d460e0fccab2475fc8887e2e7d5e514ae14cad9242204a6fdf5ec2a161b632b5  verify_a0_w0_nonzero_independent.py
865bb7475878c7f669ef2d10bb69db79e158d41954e227bad5f3a81cc8226292  verify_strict.sh
```

The supplied candidate suite also passes:

```text
PASS: A0_W0_NONZERO_SYMPY_E6_6E2A91
PASS: A0_W0_NONZERO_SPARSE_E6_D91C47
PASS: A0_W0_NONZERO_STRICT_31F80B
```

The candidate sparse checker imports a hash-pinned arithmetic kernel from
an earlier audit.  That is not a correctness defect, but it is why the
present audit supplies a standalone implementation instead of treating
the two candidate checkers as independent evidence.

## 8. Final scope

The candidate may be promoted exactly as an exclusion of
\[
\boxed{a=0,\quad W_0\ne0}
\]
on the vertical companion.  It covers every root type of \(q_0\) and
uses only \(E_6\).  It does not cover \(W_0=0\), does not assert that
boundary points are Keller maps, and does not exclude the reclassified
nonminimal binary row.  Those limitations are both necessary and
correctly stated.
