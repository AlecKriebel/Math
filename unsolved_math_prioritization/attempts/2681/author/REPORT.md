# Double branched covers of hyperbolic L space knots

## Result and scope

K3 Problem 1.22, database identifier 2681, asks whether the double cyclic cover of
the three-sphere branched over a hyperbolic L-space knot can be an L-space.
The requested conclusion has **not been proved or refuted here**. Five distinct
mathematical proof attempts are completed below. Each contains an actual
derivation, its precise scope, and the step that remains unavailable.
Source identification, literature searches, and computational checks are not
counted as mathematical attempts. None of the elementary lemmas below is claimed
to be a new research theorem.

The exact problem is in K3, printed page 30, Problem 1.22 [K3]. It is not the
different Problem 1.22 of Kirby's 1997 list. We use coefficients in
`F_2` when discussing Heegaard Floer or Khovanov ranks. Put

\[
Y=\Sigma_2(K),\qquad D=|\Delta_K(-1)|.
\]

For a knot, `D` is a nonzero odd integer. Thus `Y` is a rational homology sphere;
the desired conclusion is

\[
\dim\widehat{HF}(Y;\mathbb F_2)>D.
\]

Mirroring does not change this rank question. When discussing positive
monodromy, choose the mirror for which the L-space surgery is positive.

### Two necessary source corrections

1. The relevant Corollary 7.3 is in Boyer--Gordon--Hu's **Recalibrating
   R-order trees and Homeo+(S1)-representations of link groups** [BGH24],
   arXiv:2306.10357v3, printed page 39. In particular, Theorem 7.2 gives
   left-orderability for every branched-cover order at least two and non-L-space
   status for orders at least three. Its discussion explicitly leaves the
   double-cover question open. The K3 bibliography instead associates [BGH25]
   with the **Seifert links** paper [BGH-S]. That paper's Seifert-exterior
   hypotheses must not be applied to a hyperbolic knot exterior. Left-orderability
   alone is not the requested Floer-homology conclusion.
2. The older proposal to settle this problem through the Li--Ni conjecture on
   unit-circle Alexander roots is no longer available. Baker--Kegel [BK24],
   Proposition 2.1 and Theorem 4.4, supply hyperbolic L-space knots with cyclotomic
   Alexander polynomials. Their arXiv v3, dated 19 August 2026, explicitly flags
   the negative answer to K3 Problem 1.21(c)(iii). Remark 4.6 explains why these
   examples do not refute Problem 1.22: they are not definite.

These are different issues. Neither correction resolves the double-cover
problem. The original sources inspected and their public identifiers are listed
at the end and in `SOURCE_MANIFEST.json`.

## Inputs used in the attempts

We use the following established results, rather than count them as attempts.

- L-space knots in `S^3` are prime, fibered, and, after mirroring if necessary,
  strongly quasipositive. Their Alexander polynomial is monic. These inputs
  and their original references are recorded in [BBG19a] and [BGH24].
- If a strongly quasipositive knot has an L-space cyclic branched cover, its
  Seifert form is definite. For a monic Alexander polynomial, all Alexander
  roots are roots of unity in the double-cover case
  [BBG19a, Theorem 1.1 and Corollary 1.2].
- For a hyperbolic fibered knot with fractional Dehn twist coefficient `c`, the
  filling of its `n`-fold cyclic exterior cover at slope `mu_n+q lambda_n`
  admits a co-oriented taut foliation if `|nc-q| >= 1`
  [BH19, Theorem 1.2]. Such a foliation rules out an L-space.
- [FRW24, Theorem A] excludes genus-two hyperbolic L-space knots. Its
  Corollary 1.3 resolves the branched-cover problem when `n>2`. The genus-one
  case is also known. A hypothetical counterexample therefore has genus at
  least three.
- The Floer surgery exact triangle and the spectral sequence from reduced
  Khovanov homology to Floer homology of a double branched cover are the
  inputs for Attempts 4 and 5 [OS03].

## Attempt 1  Integral monodromy and cyclotomic algebra

### Proposed route

Assume `Y` is an L-space. Use definiteness to force periodic monodromy and
contradict hyperbolicity. The homological part of this route works completely;
the passage from homological monodromy to the surface mapping class does not.

### A precise homological obstruction

Let `V` be a Seifert matrix of a fiber surface, of size `2g`. It is unimodular.
Choose the sign so that `Q=V+V^T` is positive definite whenever the knot is
definite. With a standard convention, the action on first homology is

\[
A=V^{-1}V^T.
\]

Changing the monodromy convention replaces this by its inverse or a conjugate;
all conclusions below are unchanged. Direct multiplication gives

\[
A^T V A=V,\qquad A^T Q A=Q.
\]

**Lemma 1.** If `V` is integral and unimodular and `V+V^T` is definite, then
`A` has finite order in `GL(2g,Z)`.

**Proof.** After changing the sign of `Q`, assume it is positive definite.
Every power `B=A^k` is integral and satisfies `B^T Q B=Q`. If `b_j` is its
`j`th column, then `b_j^T Q b_j=Q_jj`. Positive definiteness bounds the ordinary
Euclidean length of every column, independently of `k`. There are only finitely
many integral matrices with these column bounds. Two powers coincide;
invertibility then gives `A^N=I` for some positive integer `N`. This proves the
lemma. In particular, `A` is semisimple over `C` and its eigenvalues are roots
of unity. The Alexander identity

\[
\det(tV-V^T)=\det(V)\det(tI-A)
\]

identifies its characteristic polynomial with the Alexander polynomial, up to
the usual normalization. QED.

**Consequence.** For a hyperbolic L-space knot, any one of the following would
settle the double-cover question for that particular knot:

- a nondefinite Seifert matrix;
- an Alexander root off the unit circle;
- a nontrivial Jordan block in homological monodromy at a root of unity;
- any other proof that integral homological monodromy has infinite order.

The Jordan-block obstruction retains information absent from the Alexander
polynomial. For example, the formal reciprocal polynomial

\[
p(t)=\Phi_6(t)^2\Phi_{30}(t)
=t^{12}-t^{11}+t^{10}-t^7+t^6-t^5+t^2-t+1
\]

has alternating nonzero coefficients and `p(1)=1`. Its companion matrix `C`
satisfies

\[
C^{30}\ne I,\qquad (C^{30}-I)^2=0.
\]

The second identity follows because `p` divides `(t^30-1)^2`; the first follows
because the companion minimal polynomial is `p`, which does not divide
`t^30-1`. Writing `C^30=I+N` gives `(I+N)^k=I+kN`, so `C` has infinite order.
This is an algebraic example only. No realization by an L-space knot is claimed.

### An actual family defeats the stronger proposed conclusion

Let `K_n`, for `n>=1`, be the Baker--Kegel knots in [BK24]. Set

\[
a=4n+5,\qquad b=4n+2,\qquad
p_n(t)=\frac{(t^a+1)(t^b+1)}{(t+1)(t^2+1)}.
\]

The public source proves that `K_n` is hyperbolic and an L-space knot and gives
`p_n` as its Alexander polynomial. The following extra conclusions follow
directly by algebra, without a census computation.

1. Both numerator factors have simple roots. They have no common root: if
   `z^a=z^b=-1`, then computing `z^(ab)` in the two ways gives `1=-1`, since
   `a` is odd and `b` is even. Dividing out the stated factors leaves a
   squarefree polynomial.
2. If `L=lcm(2a,2b)`, then `p_n` divides `t^L-1`. Since the knot is fibered,
   Cayley--Hamilton implies that its actual homological monodromy satisfies
   `A_n^L=I`.
3. The degree is `8n+4`, so `g(K_n)=4n+2`. Evaluation at `-1`, using the
   removable factor `t+1`, gives `D=4n+5`.
4. The published signature formula in [BK24, Remark 4.6] is
   `|sigma(K_n)|=g(K_n)+2`. Consequently,

   \[
   2g(K_n)-|\sigma(K_n)|=4n>0.
   \]

Thus even **hyperbolicity plus the L-space-knot property plus finite-order
homological monodromy** does not force a torus knot. These knots are nevertheless
excluded from the current conjecture by their signature defect. For `n=1`, the
derived values are genus `6`, determinant `9`, and homological order dividing
`36`.

### Where this attempt stops

The residual hypothesis includes definiteness, not just cyclotomicity or finite
homological order. No argument here shows that a definite hyperbolic L-space knot
cannot exist, or that its double cover has extra Floer homology. Replacing this
missing step by Li--Ni is invalid. More generally, [MS19] gives hyperbolic
fibered strongly quasipositive knots with the same Seifert form as a torus knot;
those examples are proved not to be L-space knots. Algebraic data cannot silently
replace the L-space-knot condition or the embedded fiber.

## Attempt 2  Boundary rotation and direct taut foliations

### Proposed route

Build a co-oriented taut foliation of `Y` from the pseudo-Anosov monodromy of
the fibered knot. This would imply the required Floer conclusion without using
the unproved left-orderability implication.

Let `F` be the fiber, `h` its monodromy, and `c=c(h)>0` after the positive
orientation choice. The two-fold unbranched cover of the exterior is the mapping
torus of `h^2`. On its boundary write `mu_2,lambda_2`, with images `2mu,lambda`
on the original exterior. The branched cover is the meridional filling
`Y=X_2(K)(mu_2)`.

The coefficient scales as `c(h^2)=2c`. Applying the foliation construction to
this actual filling succeeds when

\[
2c\ge1.
\]

This settles the subclass `c>=1/2`. It does not follow from right-veering:
right-veering in the pseudo-Anosov case supplies positivity, not that lower bound.

### Deriving the exact residual filling window

Suppose now `0<c<1/2`. For an integer `q`, the sufficient filling condition is
`|2c-q|>=1`. A direct solution of the strict reverse inequality gives

\[
|2c-q|<1\quad\Longleftrightarrow\quad q\in\{0,1\}.
\]

Indeed, `0<2c<1`; for `q<=-1`, `2c-q>1`, and for `q>=2`, `q-2c>1`.
For `q=0` and `q=1`, the absolute value is strictly less than one. Thus all
integer fillings `mu_2+q lambda_2` outside the two adjacent slopes are known to
be non-L-spaces by this construction. The target remains exactly the slope
`q=0`, with `q=1` the other unhandled slope. At the boundary `c=1/2`, the target
meets the sufficient condition with equality.

This calculation prevents an erroneous perturbation argument: foliations at the
other integer slopes are foliations on different closed manifolds. There is no
continuity theorem here allowing one to fill the omitted meridian.

### Testing the natural orienting-cover repair

One might try to coorient the suspended invariant foliation by taking the double
cyclic exterior cover. That cover changes the **time direction** of the mapping
torus, not the fiber. On the nonsingular part `F^o` of each fiber its restriction
is the identity. If the orientation obstruction of the invariant foliation
restricts to a nonzero class

\[
w_1\in H^1(F^o;\mathbb Z/2),
\]

then its pullback restricts to exactly the same nonzero class upstairs.
Consequently this time cover cannot remove that obstruction. This is a precise
reason the cyclic double cover cannot automatically be identified with the
orientation double cover of the invariant foliation.

### Where this attempt stops

For `0<c<1/2`, an additional construction is required at the meridional filling.
It must establish coorientation, extension over the filling torus, and tautness.
Neither a nonzero coefficient nor the order-tree action in [BGH24] supplies
those three conclusions. The argument proves a genuine sufficient subclass and
isolates the two-slope gap, but does not close it.

## Attempt 3  Positive Hopf plumbing and ADE lattices

### Proposed route

Use definiteness to classify an actual positive Hopf-plumbed fiber and force its
boundary to be a torus knot. For a **standard positive arborescent plumbing along
a tree**, this route can be carried out. The word "standard" and the geometric
plumbing hypothesis cannot be omitted.

Let `T` be a finite connected tree. Up to changing signs of the band-core basis
along the tree, the positive symmetrized form is

\[
Q_T=2I-\operatorname{Adj}(T).
\]

We now give the complete elementary classification needed for this route.

### Classification of the definite tree forms

**Lemma 2.** `Q_T` is positive definite precisely for the trees
`A_m`, `D_m`, `E_6`, `E_7`, and `E_8`.

**Proof.** If a vertex has degree at least four, select that vertex and four
neighbors. The resulting principal submatrix has a null vector with weight `2`
at the center and weight `1` at the four leaves. A positive definite matrix
cannot have such a principal submatrix.

If two vertices have degree at least three, choose the path joining them and
two additional neighbors at either end. This selected subtree has a null vector
with weight `2` on the connecting path and `1` on the four additional leaves.
The tree property ensures the selected neighbors are distinct and introduces no
extra edges. Again positive definiteness is impossible.

Therefore a definite tree is either a path or has exactly one trivalent vertex.
For a path with `m` vertices, the leading principal determinants obey
`d_m=2d_(m-1)-d_(m-2)`, with `d_0=1,d_1=2`. Hence `d_m=m+1`, and the form is
positive definite.

For the remaining case, let the three arm lengths be `1<=a<=b<=c`. Each arm
block is a positive definite path matrix. Eliminating those blocks leaves the
central Schur complement

\[
s=2-\frac a{a+1}-\frac b{b+1}-\frac c{c+1}
 =\frac1{a+1}+\frac1{b+1}+\frac1{c+1}-1.
\]

The full matrix is positive definite exactly when `s>0`, and its determinant is
`(a+1)(b+1)(c+1)s`. If `a>=2`, then `s<=0`. For `a=1`, either `b=1`, giving
`(1,1,c)` and the `D` family, or `b=2`, where `s>0` requires `c=2,3,4`.
These three trees are `E_6,E_7,E_8`. If `b>=3`, again `s<=0`. This exhausts
the possibilities. QED.

### Returning from the form to the knot

For the standard arborescent Hopf plumbings, the boundary identifications are
those recorded in [BBG19a, Section 9] and [BBG19b, introduction]. The knot
members are `A_(2g)`, `E_6`, and `E_8`, whose boundaries are respectively
`T(2,2g+1)`, `T(3,4)`, and `T(3,5)`.

There is also a quick necessary algebraic check on the excluded diagrams.
A knot Seifert form has `det(V-V^T)=1`; modulo two, this forces
`det(V+V^T)` to be odd. The `D` forms have determinant `4`, and `E_7` has
determinant `2`, so they cannot be knot fibers. Odd-rank path forms cannot be
knot fibers either; the surviving paths have even rank.

It follows that a hyperbolic knot with an actual standard positive Hopf-tree
fiber cannot have an L-space double cover: definiteness would restrict it to one
of the displayed nonhyperbolic knots.

### Where this attempt stops

Strong quasipositivity does not supply that tree-plumbing model. Stabilizing an
open book changes the binding; its availability does not permit replacing the
original knot by a convenient plumbing. Even an isomorphism of Seifert lattices
does not establish an isotopy of embedded fiber surfaces.

The wider theorem [BBG19b, Theorem 1.5] covers prime strongly quasipositive links
whose Birman--Ko--Lee exponent is at least two. It leaves exponent at most one.
The same paper constructs definite basket links outside the ADE boundary list.
Therefore neither the abstract root lattice nor the existence of a positive
band presentation closes the general gap. This attempt proves a complete
geometric subclass, but no theorem here places every hypothetical counterexample
in that subclass.

## Attempt 4  Floer surgery triangles on the twofold exterior

### Proposed route

Use the nearby non-L-space fillings from Attempt 2 and the Floer exact triangle
to force extra Floer homology at the omitted meridian. To see precisely what is
needed, first compute the homology of all three fillings.

For `M=X_2(K)`, the mapping-torus sequence gives

\[
H_1(M;\mathbb Z)=\mathbb Z\langle\mu_2\rangle
\oplus T,\qquad T=\operatorname{coker}(A^2-I).
\]

The longitude bounds the fiber, so its image in `H_1(M)` is zero. Moreover,

\[
|T|=|\det(A^2-I)|
=|\det(A-I)\det(A+I)|
=|\Delta_K(1)\Delta_K(-1)|=D.
\]

Here `Delta_K(1)=1`, and `Delta_K(-1)` is odd and nonzero. Thus every filling
`M(mu_2+q lambda_2)` has first homology `T`, whereas `M(lambda_2)` has first
Betti number one. This is a calculation of the actual exterior, not a proposed
analogy with surgery on `K` in `S^3`.

Take the distance-one slopes `mu_2`, `mu_2-lambda_2`, and `lambda_2`. After
choosing slope orientations, they give a Floer surgery exact triangle. Write
the dimensions of its terms as `a,b,c`, respectively. The target is `a>D`.
The foliation at `q=-1` gives `b>D`; it does not determine either `b` or `c`.

### Solving the rank constraints exactly

For any exact cyclic triangle of finite-dimensional vector spaces, let the
successive map ranks be `x,y,z`. Exactness and rank-nullity give

\[
a=x+z,\qquad b=x+y,\qquad c=y+z.
\]

Therefore

\[
a\ge b-c,
\]

but the inequality `b>D` does not yield `a>D` without further control on `c`
or on the actual maps.

In fact, for any positive integer `D` and any positive even integer `r`, there
is an exact triangle with dimensions

\[
(a,b,c)=(D,D+r,r).
\]

Take `A=F_2^D`, `B=A direct-sum F_2^r`, and `C=F_2^r`. The maps are
inclusion, projection, and zero. Their ranks are `(D,r,0)`, all composites
vanish, and image equals kernel at every term. This simultaneously allows the
target to have minimal rank and the adjacent rational-homology-sphere term to
have arbitrarily large excess rank. Choosing a larger `r` also accommodates any
fixed lower bound imposed on the zero-filling rank.

These are **abstract rank models**, not asserted Floer groups or manifold
counterexamples. Their role is to prove that the specific rank information
obtained so far cannot imply the desired conclusion.

### Where this attempt stops

A successful triangle proof needs information beyond exactness and the fact
that one nearby filling is not an L-space. Examples of genuinely sufficient
additional information would be `b-c>D`, or Spin-c-refined ranks or cobordism
maps that preclude the displayed algebraic pattern. No such uniform bound or map
calculation has been obtained for all hyperbolic L-space knots. The ordinary
L-space surgery formula for `K` does not compute these fillings of its twofold
exterior cover.

## Attempt 5  Khovanov spectral sequence and surviving classes

### Proposed route

Find extra Khovanov classes and force them to survive to Floer homology of `Y`.
The available spectral sequence has the direction

\[
\widetilde{Kh}(\overline K;\mathbb F_2)
\Longrightarrow\widehat{HF}(Y;\mathbb F_2),
\]

up to the equivalent orientation convention. It gives

\[
D\le\dim\widehat{HF}(Y)\le\dim\widetilde{Kh}(\overline K).
\]

The upper bound must not be read as a lower bound. We therefore tried adding the
survival of a distinguished contact/transverse class to the rank argument.

### Exact cancellation calculation

For any finite-dimensional page `E_r`,

\[
\dim E_{r+1}=\dim E_r-2\operatorname{rank}(d_r).
\]

This follows from `dim ker d = dim E-rank d` and `im d` being contained in
`ker d`. Consequently, if an initial page has dimension `D+2s`, it can still
converge to dimension `D` when the total differential rank is `s`.

This remains true with a specified permanent cycle. Take a filtered complex
over `F_2` with basis

\[
e_1,\ldots,e_D,\ u_1,\ldots,u_s,\ v_1,\ldots,v_s,
\]

and differential `d(u_i)=v_i`, with all other differentials zero. Put `u_i` in
filtration two and `v_i,e_j` in filtration zero, and choose homological degrees
so the differential has degree minus one. The first possible differential is
the filtration-two differential. Its rank is `s`; the preceding page has rank
`D+2s`, and the next page has rank `D`. The class `e_1` is a cycle on every page
and is never a boundary. Thus a single protected class does not prevent every
excess pair from cancelling.

Again, this is a filtered-linear-algebra model, not a purported link
realization or a replacement for the gradings in the actual link spectral
sequence.

There is also an actual topological warning. Baldwin [Bal08, Section 9] computes
the spectral sequence for `T(3,4)`: reduced Khovanov rank `5` drops to Floer
rank `3`, while the distinguished class survives. The branched cover is an
L-space. This knot is not hyperbolic, so the example does not disprove the
target statement; it disproves the proposed inference from excess rank and
one protected class alone.

### Where this attempt stops

To finish this route one needs a **hyperbolicity-sensitive survival argument**:
for example, classes with grading or filtration obstructions to every possible
incoming and outgoing differential whose total surviving dimension exceeds
`D`. Neither Khovanov thickness nor the existence of one contact class provides
that argument. No universal set of such additional permanent cycles has been
constructed here.

## Exact remaining problem

The five attempts neither establish a contradiction nor give a counterexample.
A hypothetical counterexample survives the work here only if, among other
conditions, it has:

- genus at least three and a definite fiber Seifert form;
- finite-order integral homological monodromy and a cyclotomic Alexander
  polynomial, while the geometric monodromy is pseudo-Anosov;
- `0<c(h)<1/2` after the positive mirror choice;
- no standard positive Hopf-tree fiber covered by Attempt 3, and no applicable
  exponent-at-least-two conclusion from [BBG19b];
- Floer rank exactly `D`, consistent with the existing left-orderability result.

These conditions are necessary reductions, not an existence claim. The source
search found no full resolution of Problem 1.22. A negative search result is not
a proof that no later or unindexed resolution exists. The report's status is
**five mathematical attempts completed; general problem unresolved**.

## Reproducibility and interpretation

`verify.py` uses only the Python standard library and exact rational/integer
arithmetic. It reads no source documents, makes no network requests, and does not
need a knot census. It checks invariant Seifert forms and finite monodromy orders;
the cyclotomic companion example; derived polynomial identities for eight
members of the Baker--Kegel family; Schur complements and null vectors for the
tree classification; exact boundary-slope arithmetic; and the two families of
abstract homological models.

The saved run has 878 positive controls and three negative controls. It is
support for the displayed algebra, not a machine verification of the topological
inputs, no certificate of the general conjecture, and no claim of independently
recomputing the published signature formula. The proof of the tree classification
is not restricted to the finite test range. The knot realization and scope of
each imported theorem remain explicit in the text.

## Public references

- [K3] *K3: A New Problem List in Low-Dimensional Topology*, Problem 1.22,
  printed page 30. [Author PDF](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).
- [BBG19a] M. Boileau, S. Boyer, C. McA. Gordon, *Branched covers of
  quasipositive links and L-spaces*, Journal of Topology 12 (2019), 536--576.
  [arXiv:1710.07658v2](https://arxiv.org/abs/1710.07658v2),
  [DOI](https://doi.org/10.1112/topo.12092).
- [BBG19b] M. Boileau, S. Boyer, C. McA. Gordon, *On definite strongly
  quasipositive links and L-space branched covers*.
  [arXiv:1811.08862v2](https://arxiv.org/abs/1811.08862v2).
- [BH19] S. Boyer, Y. Hu, *Taut foliations in branched cyclic covers and
  left-orderable groups*. [arXiv:1711.04578v3](https://arxiv.org/abs/1711.04578v3).
- [BGH24] S. Boyer, C. McA. Gordon, Y. Hu, *Recalibrating R-order trees and
  Homeo+(S1)-representations of link groups*, Journal of Topology 17 (2024),
  e70005. [arXiv:2306.10357v3](https://arxiv.org/abs/2306.10357v3),
  [DOI](https://doi.org/10.1112/topo.70005).
- [BGH-S] S. Boyer, C. McA. Gordon, Y. Hu, *Cyclic branched covers of Seifert
  links and properties related to the ADE link conjecture*, Journal of the
  London Mathematical Society 111 (2025), e70178.
  Inspected preprint: [arXiv:2402.15914v1](https://arxiv.org/abs/2402.15914v1);
  [published DOI](https://doi.org/10.1112/jlms.70178).
- [FRW24] E. Farber, B. Reinoso, L. Wang, *Fixed-point-free pseudo-Anosov
  homeomorphisms, knot Floer homology and the cinquefoil*, Geometry & Topology
  28 (2024), 4337--4381. [arXiv:2203.01402v2](https://arxiv.org/abs/2203.01402v2),
  [DOI](https://doi.org/10.2140/gt.2024.28.4337).
- [BK24] K. L. Baker, M. Kegel, *Census L-space knots are braid positive,
  except for one that is not*, Algebraic & Geometric Topology 24 (2024),
  569--586. [arXiv:2203.12013v3](https://arxiv.org/abs/2203.12013v3),
  [DOI](https://doi.org/10.2140/agt.2024.24.569).
- [MS19] F. Misev, G. Spano, *Tight fibred knots without L-space surgeries*.
  Inspected preprint: [arXiv:1906.11760v1](https://arxiv.org/abs/1906.11760v1).
- [OS03] P. Ozsvath, Z. Szabo, *On the Heegaard Floer homology of branched
  double-covers*. [arXiv:math/0309170](https://arxiv.org/abs/math/0309170).
- [Bal08] J. A. Baldwin, *On the spectral sequence from Khovanov homology to
  Heegaard Floer homology*, especially Section 9.
  [arXiv:0809.3293](https://arxiv.org/abs/0809.3293).
