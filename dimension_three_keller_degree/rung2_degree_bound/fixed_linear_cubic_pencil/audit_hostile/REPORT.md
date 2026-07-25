# Hostile audit: horizontal fixed-linear primitive cubic pencil

## Verdict

**PASS**, conditional only on the already-banked homogeneous rank-two
factorization/taxonomy and the established unconditional plane
low-degree bound.  The theorem really excludes the horizontal part of
\[
(e,a,b,\delta,\nu)=(1,3,1,1,1),
\qquad H_4=h(p,q,0),
\]
and does not claim the vertical part.  No Keller counterexample or
nonzero degree-two or degree-three normal component satisfying all the
stated hypotheses was found.

Two verifier defects and one expository overstatement were corrected:

1. optimized Python previously erased every `assert` and falsely printed
   the success sentinel; the verifier now refuses `python -O`;
2. raw GP execution was permissive about diagnostics and trailing output;
   a strict wrapper and injected-failure self-test were added;
3. the vertical determinantal locus was called a “codimension-one
   escape.”  For fixed \(h\), rank at most one in a \(2\times4\)
   restriction matrix has expected and actual codimension three.  The
   corrected wording is “the complete escape visible to the valuation at
   the prime divisor \(h=0\).”

These corrections do not change the theorem.

## Exact scope of the geometric hypotheses

The row \(e=1,a=3,b=1\) has, after an invertible target change,
\[
H_4=(hp,hq,0),
\]
where \(p,q\) are coprime nonproportional homogeneous cubics and the
minimal-pair convention says
\[
\mathbb C(p/q)\subset\mathbb C(\mathbb P^2)
\]
is relatively algebraically closed.  The note also proves the equivalence
with absence of a nontrivial lower-degree homogeneous composition in
degree three, rather than merely assuming it.

The horizontal hypothesis
\[
h\nmid \alpha p+\beta q
\quad((\alpha,\beta)\ne(0,0))
\]
is exactly rank two for the restrictions of \(p,q\) to \(h=0\).  Its
complement is exactly the rank-one determinantal locus.  Coprimality rules
out rank zero and also makes the vertical pencil member unique.  A pencil
coordinate change then gives
\[
p=h^m r_{3-m},\qquad 1\le m\le3,\qquad
h\nmid q r_{3-m},\qquad \gcd(r_{3-m},q)=1.
\]
Thus the theorem neither silently discards a second vertical member nor
mistakes “horizontal” for a generic transversality condition.

## Minimality and relative algebraic closure

Let \(L\) be the relative algebraic closure of \(\mathbb C(p/q)\) in
\(\mathbb C(\mathbb P^2)\).  The induced rational map from
\(\mathbb P^2\) to the smooth curve with field \(L\) restricts
nontrivially to a general line.  Hence that curve is rational, so
\(L=\mathbb C(r/s)\).  If \(L\) were proper, then
\[
\frac pq=\frac{A(r,s)}{B(r,s)}
\]
for coprime binary forms \(A,B\) of a common degree \(n>1\).
After choosing coprime equal-degree homogeneous \(r,s\), the substituted
forms \(A(r,s),B(r,s)\) remain coprime: at the generic point of a putative
common prime divisor, \([r:s]\) would be a common projective zero of
\(A,B\).  Reduced-fraction uniqueness then gives
\[
p=A(r,s),\qquad q=B(r,s),\qquad 3=n\deg r.
\]
Thus \(n=3,\deg r=1\), precisely the excluded lower-degree composition.
There is no hidden cancellation or unproved Lüroth step in this degree.

## Algebraicity and scaling descent

Set \(P=hp,Q=hq\).  These forms are algebraically independent: a relation
can be split by source-scaling weight, and a homogeneous binary relation
over \(\mathbb C\) factors into linear factors, one of which would make
\(P,Q\) proportional.

For a nonzero homogeneous \(G\) with
\(\operatorname{Jac}(P,Q,G)=0\), characteristic zero gives
\[
G\ \text{algebraic over}\ \mathbb C(P,Q).
\]
The degree-zero element
\[
\Theta=G^4/P^d
\]
lies in \(K_0=\mathbb C(\mathbb P^2)\).  Writing \(u=Q/P=q/p\), it is
algebraic over \(\mathbb C(u,P)\).  If \(s\) is a scaling coordinate, then
\(\mathbb C(x,y,z)=K_0(s)\) and \(P=s^4P_0\), so \(P\) is transcendental
over \(K_0\).  A cleared relation
\[
\sum_j P^j b_j(\Theta)=0,\qquad b_j(T)\in\mathbb C(u)[T],
\]
therefore has every coefficient \(b_j(\Theta)=0\).  Since the original
relation was nonzero, at least one \(b_j\) is nonzero, proving that
\(\Theta\) is algebraic over \(\mathbb C(u)\).  Relative closure then
gives \(\Theta=R(u)\).  This descent does not assume that an arbitrary
degree-zero algebraic element automatically belongs to the pencil field.

## The divisor calculation

Horizontality includes
\[
v_h(p)=0,\qquad v_h(q-\lambda p)=0
\quad\text{for every }\lambda\in\mathbb C.
\]
Factoring a reduced \(R(t)\) into finite linear factors (with the degree
difference accounting for infinity) gives
\[
v_h(R(q/p))=0.
\]
No numerator/denominator cancellation or division by a pencil
discriminant is being used.  Since \(v_h(P)=1\),
\[
0=v_h(\Theta)=4v_h(G)-d.
\]
For \(d=2,3\), this is impossible.  The same proof actually gives the
stated lemma for every \(d\) not divisible by four.

On a vertical member \(p=h^m r\), the corrected equality is
\[
4v_h(G)-d(m+1)=m\,\operatorname{ord}_\infty R,
\]
so the right side can absorb the mismatch.  This exactly explains why
the proof stops there.

## Keller determinant coefficients

For
\[
JF(\tau X)=L_0+\tau JH_2+\tau^2JH_3+\tau^3JH_4,
\]
the weight-eight coefficient has only the pattern \(3+3+2\).  Because
the third row of \(JH_4\) is zero,
\[
E_8=\det(\nabla P,\nabla Q,\nabla(H_3)_3).
\]
The divisor lemma with \(d=3\) gives \((H_3)_3=0\).

At weight seven the patterns are \(3+3+1\) and \(3+2+2\).  After the
cubic normal component vanishes, both \(JH_3\) and \(JH_4\) have zero
third row, so every \(3+2+2\) determinant is zero.  Hence
\[
E_7=\det(\nabla P,\nabla Q,\nabla(H_2)_3),
\]
and the \(d=2\) case gives \((H_2)_3=0\).  The finite-field audit
independently reconstructed both polarizations from the six determinant
permutations for 128 exact samples.

## Plane-fibre exit

The third component is now a nonzero linear form (plus an inessential
constant); nonzero follows from \(L_0\in\mathrm{GL}_3\).  Linear changes
and a target translation give
\[
F=(F_1(x,y,z),F_2(x,y,z),z).
\]
For each \(c\in\mathbb C\), the fibre map
\[
(x,y)\longmapsto(F_1(x,y,c),F_2(x,y,c))
\]
is a complex plane Keller map of degree at most four, so the established
low-degree plane theorem makes it an automorphism.  Equality of two
three-dimensional images first forces equal \(z\), then fibrewise
injectivity forces the points equal.  Ax--Grothendieck gives a polynomial
automorphism.  This uses a proved finite plane degree bound, not the
general plane Jacobian Conjecture.

## Sharpness and attempted counterexamples

The two advertised boundary witnesses are valid and primitive.

- For \(h=z,p=zx^2,q=x^3+y^3\), one has
  \(P=(zx)^2\) and \(G_2=zx\).  The generic member
  \(x^2z-t(x^3+y^3)\) is primitive and linear in \(z\), hence irreducible
  over \(\overline{\mathbb C(t)}\).
- For \(h=z,p=z^3,q=x^3+y^3\), one has \(P=z^4\), so both \(z^3\) and
  \(z^2\) are first integrals of the required degrees.  The generic member
  \(z^3-t(x^3+y^3)\) is a smooth plane cubic over
  \(\overline{\mathbb C(t)}\), hence geometrically integral.

Thus both pencils satisfy the minimality condition and show that dropping
horizontality really invalidates the \(E_8/E_7\) vanishing claim.  They
are correctly labeled as witnesses only for the top identities, not as
Keller maps.

As an additional counterexample search, the dependency-free audit sampled
64 deterministic horizontal cubic pairs over
\(\mathbb F_{1,000,003}\).  In every case the maps
\[
G_d\longmapsto\operatorname{Jac}(hp,hq,G_d)
\]
had full input rank \(6\) for \(d=2\) and \(10\) for \(d=3\).  This is
not part of the proof, but it detected no missed low-degree kernel and
independently reproduced both vertical witnesses.

## Verifier audit

All of the following pass:

```text
/usr/bin/python3 verify_horizontal_fixed_linear_cubic_pencil_sympy.py
./verify_horizontal_fixed_linear_cubic_pencil_pari_strict.sh
./audit_hostile/audit_finite_field_strict.sh
./audit_hostile/audit_supplied_runners.sh
```

The runner self-test verifies rejection of optimized Python, injected GP
diagnostics, trailing output, and nonzero GP exits.  The finite-field
auditor uses no SymPy or PARI/GP code and implements polynomial arithmetic,
Gaussian elimination, and weighted determinants independently.

Audit marker:
`AUDIT_HORIZONTAL_CUBIC_PENCIL_PASS_8D1A77`.
