# Hostile audit: vertical fixed-linear primitive cubic pencil

**Verdict: PASS.**

**Completed:** 2026-07-25T11:15:08Z.

The vertical multiplicity theorem in
`../WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md` is correct under its
stated minimal-pair and coprimality hypotheses.  I found no missed
valuation branch, no missed marked-member orbit, no illegal source or
target normalization, and no \(E_8\) survivor outside
\(\langle h^3,q\rangle\) on the primitive triple-vertical stratum.

One exposition point is worth expanding before promotion: in the
\(m=3,s=-4\) branch, the proof should explicitly say that finite poles of
the rational function \(R\) are impossible and that the finite zero orders
sum to four.  Those two facts make the “one zero of order four” conclusion
immediate.  They are consequences of the displayed valuation identity, so
this is a clarification rather than a new hypothesis or correction.

## 1. Reconstructed valuation identity

Put
\[
P=hp,\qquad Q=hq,\qquad u=q/p,
\]
and let \(G\ne0\) be homogeneous of degree \(d\) with
\(\operatorname{Jac}(P,Q,G)=0\).  The banked homogeneous first-integral
descent, using relative algebraic closure of \(\mathbb C(u)\), gives
\[
\frac{G^4}{P^d}=R(u),\qquad R\in\mathbb C(t)^\times.       \tag{1}
\]

Write
\[
p=h^m r,\qquad h\nmid rq,\qquad \gcd(p,q)=1,
\]
and let \(f\) be a prime component of \(p\) of multiplicity
\(a=v_f(p)\).  The function \(u\) has a pole of order \(a\) at \(f\).
With
\[
s=\operatorname{ord}_\infty R
\]
in the standard convention, \(v_f(R(u))=as\).  Since
\[
v_f(P)=a+\mathbf1_{f=h},
\]
taking \(v_f\) in (1) gives exactly
\[
4v_f(G)-d\bigl(a+\mathbf1_{f=h}\bigr)=as.                \tag{2}
\]
No fibre is assumed reduced, and no coefficient or discriminant is
divided out.

## 2. Degree-three exclusion for \(m=1,2\)

Let \(d=3\).

For \(m=1\), equation (2) at \(h\) is
\[
4v_h(G)=6+s,
\]
so
\[
s\equiv2\pmod4.                                          \tag{3}
\]
Every prime component of the quadratic \(r\) has multiplicity
\(a=1\) or \(2\).  At such a prime, (2) requires
\[
4v_f(G)=a(3+s).                                          \tag{4}
\]
But \(3+s\equiv1\pmod4\), and neither \(a=1\) nor \(a=2\)
makes the right side divisible by four.  Thus \(G=0\).

For \(m=2\), the \(h\)-equation is
\[
4v_h(G)=9+2s.                                            \tag{5}
\]
Its right side is odd for every integer \(s\), so this stratum also has
no nonzero cubic first integral.

These congruences are insensitive to the factorization type of \(r\) and
to all moduli of \(q\).

## 3. Complete \(m=3\) divisor classification

For \(m=3\), one has \(p=h^3\) and \(P=h^4\).  Equation (2) at \(h\)
becomes
\[
4v_h(G)=12+3s.
\]
Hence \(s\equiv0\pmod4\).  Because \(0\le v_h(G)\le3\),
the only possibilities are
\[
(s,v_h(G))=(0,3)\quad\text{or}\quad(-4,0).              \tag{6}
\]

If \(s=0\), degree is exhausted at \(h\), so
\[
G\sim h^3.                                               \tag{7}
\]

Suppose \(s=-4\).  For a finite point \(\lambda\), write
\[
n_\lambda=\operatorname{ord}_\lambda R.
\]
If \(f\) is a multiplicity-\(a\) component of the cubic member
\(q-\lambda p\), then \(P\) is a unit at \(f\) and
\[
4v_f(G)=a n_\lambda.                                    \tag{8}
\]
Thus a finite pole \(n_\lambda<0\) is impossible.  The divisor-degree
identity for \(R\) now says
\[
\sum_{\lambda\in\mathbb C}n_\lambda=-s=4.               \tag{9}
\]

For a zero of order \(n\in\{1,2,3\}\), (8) would require \(4\mid na\)
for every component multiplicity \(a\) of a cubic divisor.

- For \(n=1\) or \(3\), every \(a\) would have to be divisible by four.
- For \(n=2\), every \(a\) would have to be even, making the total degree
  of the cubic divisor even.

Both alternatives are impossible.  Therefore (9) consists of one zero
of order four.  Say it occurs at \(\lambda\).  Equation (8) then gives
the same component multiplicities for \(G\) and \(q-\lambda p\); both
have degree three, so
\[
G\sim q-\lambda p.                                      \tag{10}
\]

Combining (7) and (10) proves the exact kernel
\[
\boxed{\ker\bigl(\operatorname{Jac}(h^4,hq,-):
  \mathbb C[X]_3\to\mathbb C[X]_8\bigr)
  =\langle h^3,q\rangle.}                               \tag{11}
\]

## 4. Exactly two nonzero companion orbits

Normalize \(h=z\) and \(p=z^3\).  Write a nonzero companion as
\[
G=\alpha p+\beta q.
\]
The residual pencil transformation
\[
q'=a q+b p,\qquad a\ne0
\]
is an honest invertible target change on the first two leading
components.  In the basis \((p,q')\),
\[
G=\left(\alpha-\frac{\beta b}{a}\right)p
  +\frac{\beta}{a}q'.                                   \tag{12}
\]

- If \(\beta=0\), scaling the third target coordinate gives \(G=p=z^3\).
- If \(\beta\ne0\), choose \(b=a\alpha/\beta\), then scale the third
  target coordinate to obtain \(G=q'\).

The two cases cannot merge.  The condition \(h\mid G\) holds in the first
case and fails in the second because \(h\nmid q\).  It is invariant under
the full equivalence preserving the leading stratum: uniqueness of the
vertical pencil member forces it to map to the vertical member, and the
third target row must scale rather than acquire a component in the
leading image plane.

Thus, after the separately treated \(G=0\) exit, there are exactly the two
claimed nonzero companion types
\[
\boxed{G=z^3}\qquad\text{and}\qquad\boxed{G=q}.           \tag{13}
\]
No special stabilizer of \(q\) produces a third orbit.

## 5. Marked source orbits and stabilizers

For \(m=1\), let \(r\) be the quadratic cofactor and set
\[
\rho=\operatorname{rank}(r|_{h=0}),\qquad
R=\operatorname{rank}(r).
\]
Because \(h\nmid r\), one has \(\rho=1\) or \(2\).

If \(\rho=2\), a parabolic change preserving \(h=0\) removes both
\(h\)-linear cross terms and leaves a nondegenerate binary quadratic plus
\(\kappa h^2\).  The cases \(\kappa=0\) and \(\kappa\ne0\) have ranks
\((2,2)\) and \((2,3)\), represented by
\[
xy,\qquad xy+z^2.
\]

If \(\rho=1\), normalize the restriction to \(x^2\) and remove the
\(xz\)-term.  The remaining form is
\[
x^2+b\,yz+c z^2.
\]
The cases \(b\ne0\), \(b=0,c\ne0\), and \(b=c=0\) give respectively
\[
x^2+yz,\qquad x^2+z^2,\qquad x^2
\]
with rank pairs \((1,3),(1,2),(1,1)\).  These five rank pairs are
parabolic invariants, so the representatives neither merge nor omit a
stratum.

For \(m=2\), the residual linear factor is transverse to \(z\), and the
parabolic is transitive on such lines, giving \(p=z^2x\).  For \(m=3\),
one has \(p=z^3\).

The displayed stabilizers are also exact:

- preserving \(z^3\) requires and permits
  \(z\mapsto cz\) and
  \((x,y)^T\mapsto A(x,y)^T+vz\);
- preserving \(zx^2\) requires \(z\mapsto cz\) and \(x\mapsto ax\);
  \(x\mapsto ax+bz\) is illegal because it creates \(z^2x\) and \(z^3\)
  terms.  The remaining coordinate \(y\) may undergo every shear listed
  in the candidate.

The candidate does not collapse the \(q\)-moduli: its quotient (13)
retains the full marked-member stabilizer and the addition of a multiple
of \(p\).

## 6. Minimality is essential and sharply retained

There is a genuine larger \(E_8\)-kernel if the minimal-pair hypothesis is
dropped.  For example, take
\[
p=z^3,\qquad q=x^3+x^2z+xz^2.
\]
Then \(p,q\in\operatorname{Sym}^3\langle x,z\rangle\), so this is exactly
the candidate's nonminimal boundary.  Since \(q_y=0\),
\[
\operatorname{Jac}(z^4,zq,G)
=4z^5(q_xG_y-q_yG_x)
=4z^5q_xG_y.
\]
Every cubic \(G\in\mathbb C[x,z]_3\) is therefore in the kernel.  The
kernel has dimension four, compared with
\(\dim\langle z^3,q\rangle=2\); for example \(G=x^3\) is an extra
survivor.

This is not a counterexample to the theorem.  It confirms that the
relative-algebraic-closure condition and reclassification boundary must
remain prominent.  On two primitive exact samples,
\[
q=x^3+y^3,\qquad q=x^3+y^3+xyz,
\]
the independently computed cubic kernel has dimension two and is exactly
\(\langle z^3,q\rangle\).

## 7. Degree-two kernel and top-three witnesses

Repeating (2) for \(d=2\) confirms the auxiliary table.

- For \(m=1\), the only compatible order is \(s=0\), and every component
  of the quadratic \(r\) must have even multiplicity.  Thus
  \(r=L^2\) and degree forces \(G\sim hL\).
- For \(m=2\), the \(h\)-equation forces \(s\) odd, while the residual
  simple line requires \(s\equiv2\pmod4\); there is no solution.
- For \(m=3\), the only degree-compatible solution is
  \(s=0,v_h(G)=2\), giving \(G\sim h^2\).

The dependency-free exact certificate recomputes the degree-two and
degree-three kernel dimensions on all seven marked representatives.

For
\[
h=z,\quad p=z^3,\quad q=x^3+y^3,\quad
H_4=(z^4,zq,0),\quad L_0=I,\quad H_2=0,
\]
it independently expands
\[
\det\bigl(I+\tau^2J(0,0,G)+\tau^3JH_4\bigr)
\]
for \(G=z^3\) and \(G=q\).  In both cases the coefficients
\(E_8,E_7,E_6\) vanish and a lower nonconstant coefficient remains.
The witnesses are therefore correctly described as top-identity
survivors, not Keller maps.

## 8. Independent exact certificate

Run:

```sh
./verify_strict_and_faults.sh
```

The verifier uses no computer-algebra dependency.  It implements exact
multivariate polynomial arithmetic, rational Gaussian elimination, and
integer divisor enumeration from scratch.  It checks:

- all degree-three \(h\)-valuation possibilities and both exclusions;
- every cubic-fibre multiplicity type in the \(m=3,s=-4\) branch;
- absence of finite poles and uniqueness of the order-four zero pattern;
- the two companion normalizations and their invariant separation;
- all five simple-vertical rank pairs and both displayed stabilizers;
- degree-two and degree-three kernels on the seven representatives;
- two primitive triple-vertical kernels and one sharp nonminimal boundary;
- both top-three determinant witnesses.

Eleven injected faults alter the fixed \(h\)-multiplicity, modulus,
companion shear sign, orbit separation, rank classification, stabilizers,
kernel dimensions, minimality boundary, and an \(E_8\) companion.  Every
fault is required to exit nonzero through its intended guard.

This audit was AI-assisted and is not peer reviewed.  Exact checks are
evidence about the encoded algebra, not peer review.  The universal result
rests on the divisor proof above, not on finite computation.
