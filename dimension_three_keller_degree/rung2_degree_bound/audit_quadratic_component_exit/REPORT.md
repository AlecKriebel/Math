# Hostile standalone audit: quadratic-component exit

## Verdict

**PASS**, as of 2026-07-25T22:39:23Z.

The following claim is fully justified:

> If \(F:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}\) is a
> Keller map of total degree at most \(4\), and the target-linear span of
> its components contains a polynomial of degree at most \(2\), then
> \(F\) is a polynomial automorphism.

The proof does **not** assume the plane Jacobian Conjecture.  Its only
dimension-two input is the published, unconditional theorem for plane
étale maps of degree at most \(12\).  The maps produced here have degree
at most \(8\).

This report independently reconstructed the argument and checked its
literature boundary before reading the corresponding passage of the
aggregate `VERIFICATION.md`.  It treats the cited published theorems as
black boxes; it does not purport to reproduce Moh's long proof.

## Independent reconstruction

### 1. The target normalization is legal

Let \(F^0\) denote the original map and let
\[
f=\lambda^T F^0,\qquad 0\ne\lambda\in\mathbb C^3.
\]
Complete \(\lambda^T\) to the third row of a matrix
\(A\in\operatorname{GL}_3(\mathbb C)\), and put \(F=AF^0\).  Then
\[
F_3=f,\qquad
\det JF=(\det A)\det JF^0\in\mathbb C^\times,\qquad
\deg F\le4.
\]
Thus the target change preserves every needed hypothesis and is reversible.
Moreover,
\[
\nabla F_3=\lambda^TJF^0
\]
cannot be zero at any point: a nonzero row vector cannot become zero after
multiplication by an invertible matrix.  In particular the case that the
displayed “low-degree component” is constant is automatically impossible.

### 2. The quadratic-submersion coordinate lemma is complete

Write
\[
f(X)=\tfrac12X^THX+b^TX+c,\qquad \nabla f=HX+b,
\]
where \(H=H^T\).  If \(b\in\operatorname{im}H\), then \(HX=-b\) is
solvable, giving a critical point.  Since no critical point exists,
\[
b\notin\operatorname{im}H.
\]
For a symmetric matrix over \(\mathbb C\),
\[
\operatorname{im}H=(\ker H)^\perp.
\]
This does not use positive definiteness: inclusion follows from symmetry,
and both sides have dimension \(\operatorname{rank}H\).  Therefore there is
a vector \(v\in\ker H\) for which \(\beta=b^Tv\ne0\).

Complete \(v\) to the third column of a matrix
\(P\in\operatorname{GL}_3(\mathbb C)\) and write \(X=PY\).  The third
row and column of \(P^THP\) vanish, while the third entry of \(P^Tb\) is
\(\beta\).  Hence
\[
f(PY)=g(Y_1,Y_2)+\beta Y_3,\qquad \deg g\le2.
\]
Consequently
\[
T(Y)=(Y_1,Y_2,f(PY))
\]
has the triangular inverse
\[
T^{-1}(U)=
\left(U_1,U_2,\frac{U_3-g(U_1,U_2)}{\beta}\right),
\]
with
\[
\deg T\le2,\qquad \deg T^{-1}\le2,\qquad
\det JT=\beta\ne0.
\]
Composing with the preceding linear source change gives the claimed
coordinate in the original variables.  This covers every possible Hessian
rank, including \(H=0\).  It also explains precisely why the first two
coordinates in the working note should be read as newly chosen linear
coordinates.

### 3. Conjugation gives the exact degree-eight bound

Use the coordinate whose third component is \(F_3\), and set
\[
G=F\circ T^{-1}.
\]
Then
\[
G=(G_1,G_2,Z),\qquad
\det JG\in\mathbb C^\times.
\]
The standard composition estimate gives
\[
\deg G\le(\deg F)(\deg T^{-1})\le4\cdot2=8.
\]
There is no second quadratic substitution, so \(8\), not \(16\), is the
correct bound.

### 4. Every plane restriction is genuinely Keller

For \(c\in\mathbb C\), define
\[
G_c(x,y)=\bigl(G_1(x,y,c),G_2(x,y,c)\bigr).
\]
Since specialization cannot increase total degree, \(\deg G_c\le8\).
Furthermore
\[
JG=
\begin{pmatrix}
G_{1x}&G_{1y}&G_{1z}\\
G_{2x}&G_{2y}&G_{2z}\\
0&0&1
\end{pmatrix},
\]
so
\[
\det JG_c
=G_{1x}G_{2y}-G_{1y}G_{2x}
=\det JG\in\mathbb C^\times.
\]
Thus every \(G_c:\mathbb A^2_{\mathbb C}\to\mathbb A^2_{\mathbb C}\)
is a polynomial étale map.  No generic-fibre argument, properness claim,
or specialization of an inverse is being used.

### 5. The plane input is unconditional and has the needed degree

Vistoli fixes an algebraically closed field \(k\) of characteristic zero
and defines the degree of a polynomial map as the maximum of its component
degrees on journal p. 79.  In the second unnumbered theorem on journal
p. 80 he states:

> An étale polynomial map
> \(\mathbb A^2\to\mathbb A^2\) of degree at most \(12\) is an
> isomorphism.

He attributes this to Moh and immediately notes that the cited reference
actually proves the result through degree \(100\), while degree \(12\) is
all that he uses.  Applying the displayed degree-\(12\) theorem to
\(G_c\), since \(8\le12\), shows that every \(G_c\) is an automorphism.
This is a bounded theorem, not an invocation of the unresolved general
plane Jacobian Conjecture.

### 6. Fibrewise invertibility lifts to a threefold automorphism

If \(G(p)=G(q)\), then the third components give \(p_3=q_3=c\).  The
equality of the first two components is then
\(G_c(p_1,p_2)=G_c(q_1,q_2)\); injectivity of \(G_c\) gives \(p=q\).
Thus \(G\), and hence every map obtained from it by the reversible source
and target changes, is injective.

The first unnumbered theorem on Vistoli's journal p. 80 states that an
injective étale polynomial self-map of \(\mathbb A^n\) is surjective,
citing Bass--Connell--Wright.  Applying it in dimension \(3\) makes \(G\)
surjective.  For completeness, the last scheme-theoretic step is:
injectivity on complex points for this finite-type morphism implies
universal injectivity; an étale universally injective morphism is an open
immersion; and a surjective open immersion is an isomorphism.  Equivalently,
one may use Zariski's Main Theorem after observing that the injective étale
map is quasi-finite and birational.  Therefore \(G\), and finally \(F^0\),
is a polynomial automorphism.

## Hypothesis and dependency audit

| item | where it is used | result |
|---|---|---|
| \(\lambda\ne0\) | completing \(\lambda\) to a target basis and proving \(\lambda^TJF^0\ne0\) | checked |
| Keller condition | nowhere-zero gradient, preservation under coordinate changes, étaleness of \(G\) and \(G_c\) | checked |
| \(\deg f\le2\) | constant Hessian and quadratic inverse for \(T\) | checked |
| \(\deg F\le4\) | \(\deg(F\circ T^{-1})\le8\) | checked |
| base field \(\mathbb C\) | algebraically closed characteristic zero hypotheses in Vistoli/Moh and Ax--Grothendieck | exact match |
| total-degree convention | comparison \(8\le12\) | matches Vistoli p. 79 |
| all fibres, not a generic fibre | global injectivity of \(G\) | checked for every \(c\in\mathbb C\) |

No Bass--Connell--Wright degree-reduction theorem and no dimension-three
degree-three theorem of Vistoli is used here.  Those results cannot hide a
change of dimension or degree in this proof.  Bass--Connell--Wright enters
only through Vistoli's citation for the injective-étale
Ax--Grothendieck statement.

## Non-blocking presentation findings

1. After the working note says that the target-changed map is again denoted
   by \(F\), its displayed identity
   \(\nabla F_3=\lambda^TJF\) mixes the pre-change and post-change
   notation.  Correctly, it is
   \(\nabla F_3=\lambda^TJF^0\) before renaming, or
   \(\nabla F_3=e_3^TJF\) afterward.  Either correct identity proves the
   required nowhere-vanishing statement, so this is not a logical gap.
2. The sentence in the working note saying that a plane counterexample has
   degree “at least \(100\)” is more vague than necessary.  The clean
   citation is Vistoli's exact degree-\(\le12\) theorem on p. 80, and
   \(8\le12\).  Vistoli additionally says Moh proves degree
   \(\le100\).  This wording issue does not affect the inference at degree
   \(8\).
3. After the source basis change, the first two entries of \(T\) are chosen
   linear coordinates, not necessarily the originally named \(X_1,X_2\).
   The working proof already says that a source change is made; spelling out
   the basis matrix removes any possible ambiguity.
4. “Ax--Grothendieck makes \(F\) a polynomial automorphism” compresses two
   standard facts.  Vistoli's quoted version gives surjectivity; Keller
   étaleness plus injectivity then makes the bijective map an isomorphism as
   explained above.  This is an expositional omission, not a gap.

## Exact regression checker

`verify_quadratic_component_exit_exact.py` independently checks, over
symbolic exact coefficient rings:

- the Hessian-kernel basis identities;
- a generic quadratic triangular coordinate and both compositions with its
  inverse;
- both constant Jacobian determinants;
- all \(35\) monomials of total degree at most \(4\), obtaining the sharp
  pullback bound \(8\);
- the equality of the threefold and fibre Jacobian determinants.

Run:

```sh
cd dimension_three_keller_degree/rung2_degree_bound/audit_quadratic_component_exit
/usr/bin/python3 verify_quadratic_component_exit_exact.py
```

Observed result:

```text
PASS: exact quadratic-coordinate, degree, and fibre identities verified
```

The checker is a regression certificate for the algebraic identities.  It
does not pretend to computer-prove the two cited literature theorems.

## Literature checked

- Angelo Vistoli, [*The Jacobian conjecture in dimension 3 and degree
  3*](https://doi.org/10.1016/S0022-4049(98)00040-1), *Journal of Pure and
  Applied Algebra* **142** (1999), 79--89.  Journal p. 79 supplies the field
  and degree conventions; journal p. 80 states both exact theorems used
  here.
- T.-T. Moh, [*On the Jacobian conjecture and the configurations of
  roots*](https://doi.org/10.1515/crll.1983.340.140), *Journal für die reine
  und angewandte Mathematik* **340** (1983), 140--212.  This is Vistoli's
  source for the plane bounded-degree theorem.
- Hyman Bass, Edwin H. Connell, and David Wright, [*The Jacobian conjecture:
  reduction of degree and formal expansion of the
  inverse*](https://www.ams.org/bull/1982-07-02/S0273-0979-1982-15032-7/),
  *Bulletin of the American Mathematical Society (N.S.)* **7** (1982),
  287--330.  This is Vistoli's cited source for the injective-étale
  surjectivity theorem.
- For the final standard étale implication, the
  [Stacks Project, Theorem 41.14.1, Tag
  025G](https://stacks.math.columbia.edu/tag/025G) states that an étale
  universally injective morphism is an open immersion.

## Aggregate comparison and scope

The relevant aggregate verification was read only after the independent
reconstruction and primary-source check.  Its degree-\(8\) statement agrees
with this audit and introduces no extra hypothesis.

This theorem excludes precisely the quartic Keller candidates whose
target-linear component span contains a polynomial of degree at most two.
It does not by itself settle all degree-four Keller maps in dimension
three, and this PASS should not be read as such a claim.
