# The arbitrary-polytopal barycentric residual: five mathematical approaches

Date: 2026-10-21. Authored calculations and proofs; no claim of a new general solution. This note concerns only the first component of OWR-1782-017. It does not analyze or accept the separate 2026 manuscript claiming the integer-polynomial/g-theorem component.

## Target and notation

For a convex polytope P of dimension d, put

H_P(t) = h(sd(∂P);t).

Here sd(∂P) is the order complex of the nonempty proper faces of P, and h is its ordinary simplicial h-polynomial. It is not the toric h-polynomial of P. Write C_P(z) for the chain polynomial of those nonempty proper faces, including the empty chain. Then

H_P(t) = (1-t)^d C_P(t/(1-t)).

The question is whether H_P has only real roots for every convex P. Since its coefficients are nonnegative and its constant term is 1, any real roots are negative. No simpliciality hypothesis is imposed on P.

The five approaches below are completed deductions or explicitly checked obstructions. The general case remains unproved. They are not five independent proofs of the conjecture, nor five unperformed research proposals.

## Approach 1. The cd-index and a complete low-dimensional reduction

### Exact reduction

Let Ψ_P(a,b) be the ab-index of the face lattice, with ab-degree d, and Φ_P(c,𝔡) its cd-index. The letter 𝔡 is distinguished from the dimension d. Flag-h specialization gives

H_P(t) = Ψ_P(1,t) = Φ_P(1+t,2t).

Let δ_P(z) = Φ_P(1,z) = Σ_k δ_k z^k, where δ_k sums the coefficients of cd-words containing k letters 𝔡. Homogeneity yields

H_P(t) = Σ_k 2^k δ_k t^k(1+t)^(d-2k)
       = (1+t)^d δ_P(2t/(1+t)^2).                         (1)

In particular, the ordinary gamma coefficients of H_P are γ_k = 2^k δ_k. This factor of two matters in discriminants and numerical examples.

**Root-equivalence proof.** If δ_P has degree m and negative roots r_1,...,r_m, factoring the right side of (1) gives a positive multiple of

(1+t)^(d-2m) Π_j [2t-r_j(1+t)^2].

For r<0, the quadratic 2t-r(1+t)^2 has positive leading and constant coefficients, negative sum of roots, and discriminant 4(1-2r)>0. Thus its two roots are negative, reciprocal, and lie on opposite sides of -1. Conversely, a nonreal root r of δ yields solutions of 2t=r(1+t)^2, none of which can be real. Because δ has nonnegative coefficients and constant term 1, it has no nonnegative real roots. Therefore H_P is real-rooted if and only if δ_P is real-rooted. This is a reduction, not a proof of real-rootedness.

### Proved scope: all dimensions d ≤ 5

Murai–Nevo, Theorem 1.1, realizes δ_P as the face polynomial of a floor(d/2)-colored simplicial complex when ∂P is S*-shellable; polytopal boundaries satisfy this hypothesis. For d≤3, δ has degree at most one, so positivity settles the assertion.

For d=4 or 5, the realizing complex is a bipartite graph, with A=δ_1 vertices and B=δ_2 edges. If the two color classes have u and v vertices, then

B ≤ uv ≤ (u+v)^2/4 = A^2/4.

Consequently δ_P(z)=1+Az+Bz² has discriminant A²-4B≥0. Its roots are negative when B>0; the B=0 case is linear or constant. By (1), H_P is real-rooted. This gives a short complete proof of the known d≤5 case, not a new general theorem. The 2023 chain-enumeration paper explicitly lists this low-dimensional result among known cases.

### Exact nonsimplicial example: the 24-cell

Its face numbers are (24,96,96,24), its two-faces are triangles, and its facets are octahedra. The elementary chain recurrence in Approach 3 gives

H_24(t) = 1+236t+678t²+236t³+t⁴,
δ_24(z) = 1+116z+52z².

The discriminant is 116²-4·52 = 13248>0. This example is neither simple nor simplicial, so it tests the genuinely polytopal part of the reduction.

**Outcome:** full coverage through d=5 and an exact dimension-halving root test. **Obstacle:** colored face-vector realizability alone ceases to force real-rootedness at three colors, as Approach 2 shows.

## Approach 2. Exact cubic tests and a realizability barrier in dimensions 6 and 7

For d=6 or 7, write δ_P(z)=1+Az+Bz²+Cz³. If C>0, all coefficients are positive and cubic real-rootedness is equivalent to

D(A,B,C) = A²B² - 4B³ - 4A³C - 27C² + 18ABC ≥ 0.        (2)

Indeed a real cubic has three real roots, counting multiplicity, exactly when its discriminant is nonnegative. Positive coefficients exclude positive roots, and the nonzero constant term excludes zero. If C=0, the quadratic criterion from Approach 1 applies instead. Formula (2) gives a sharp finite numerical target for actual face-poset data in the first unsettled dimensions.

The Newton necessary inequalities in the cubic case are

A² ≥ 3B,      B² ≥ 3AC.

They are weaker than (2). This can be demonstrated while retaining a pure balanced-complex realization, not merely by choosing arbitrary positive numbers.

Take the disjoint union of two full triangles as an abstract simplicial complex, color both triangles with the same three colors, and count its faces. Its face polynomial is

δ(z) = 1+6z+6z²+2z³ = 2(1+z)^3-1.

It is a pure, three-colored, two-dimensional simplicial complex. It satisfies A²≥3B (36≥18) and B²≥3AC (36=36), but its cubic discriminant is -108. It has one real root and two nonreal roots. The associated degree-six lift is

(1+t)^6 +12t(1+t)^4 +24t²(1+t)^2 +16t³
= 1+18t+87t²+156t³+87t⁴+18t⁵+t⁶,                     (3)

which is not real-rooted by the root equivalence.

A formally nonnegative homogeneous cd-polynomial with this δ is

c^6 +6𝔡c^4 +6𝔡²c² +2𝔡³.

**Important non-counterexample warning:** no convex polytope, Eulerian poset, or Gorenstein* poset with this cd-index is exhibited. The example does not satisfy every known polytopal constraint; for example its small coefficients should not be confused with the polytopal simplex lower bounds. It refutes only an attempted deduction from nonnegative cd-coefficients, a balanced face-vector realization, and these Newton inequalities alone. Even purity of the auxiliary complex is insufficient. It is not a counterexample to the target conjecture.

**Outcome:** an exact necessary-and-sufficient test in d=6,7, together with a concrete reason the successful low-dimensional proof stops there. **Obstacle:** one must prove (2) from additional polytopal structure, or produce actual polytopal data violating it. No exhaustive polytope search or realizability search is claimed here.

## Approach 3. Chain recurrences, interval products, and the missing interlacing hypothesis

Two exact identities expose what an inductive proof would need.

### Maximal-face decomposition

Every nonempty chain has a unique maximal face F. The subchain below F is a chain of nonempty proper faces of F. Thus

C_P(z)=1+z Σ_(∅≠F⊊P) C_F(z).

For a k-dimensional F, convert C_F to H_F to obtain

H_P(t)=(1-t)^d + t Σ_(∅≠F⊊P) (1-t)^(d-1-dim F) H_F(t). (4)

For a cube, vertices contribute 1, edges contribute 1+t, and square facets contribute 1+6t+t². Consequently

H_cube(t)=(1-t)^3+t[8(1-t)²+12(1-t)(1+t)+6(1+6t+t²)]
         =1+23t+23t²+t³.

This derivation uses the actual face incidences through the lower interval types, not an inappropriate simplicial transformation.

### Marked-face decomposition

Differentiating a chain polynomial marks one face in each chain. The parts below and above that face vary independently. If P/F is a face figure, of dimension d-dim(F)-1, then

C'_P(z)=Σ_(∅≠F⊊P) C_F(z) C_(P/F)(z).

Since C_P(z)=(1+z)^d H_P(z/(1+z)), this becomes

d H_P(t)+(1-t)H'_P(t)=Σ_(∅≠F⊊P) H_F(t)H_(P/F)(t).    (5)

For a cube, the sum is

8(1+4t+t²)+12(1+t)²+6(1+6t+t²)=26+92t+26t²,

which agrees identically with 3H_cube+(1-t)H'_cube. The vertex figures here are triangles; the facets are squares.

### What shellings really provide

For a shelling of ∂P, barycentric subdivision decomposes into relative complexes R_i. Additivity gives H_P=Σ_i h(R_i;t). If the relative h-polynomials form an interlacing family, every nonnegative combination, including their sum, is real-rooted. This is the criterion stated by Hlavacek–Solus, Theorem 3.1. It is a valid sufficient condition, not automatic from ordinary shellability.

The required compatibility cannot be discarded, even for symmetric, nonnegative, negative-real-rooted summands. For example

p(t)=(1+t)^4,       q(t)=(1+4t+t²)^2

are both real-rooted, but

p(t)+q(t)=2+12t+24t²+12t³+2t⁴
        =2(1+t)^4+4t(1+t)²+4t²

has gamma polynomial 2+4z+4z², with discriminant -16. The sum is not real-rooted. Thus neither the induction hypothesis that all proper faces and face figures have real-rooted H, nor positivity of their local contributions, by itself closes (4), (5), or the shelling sum.

A usable further statement would have to prove compatibility for the actual interval or relative-shelling polynomials. The individual real-rootedness of the products in (5) would not suffice. No such general compatibility theorem is established in this note.

**Outcome:** exact local recurrences, explicit checks on a nonsimplicial polytope, and a precise sufficient interlacing criterion. **Obstacle:** global compatibility, not just local real-rootedness or shellability.

## Approach 4. The classical subdivision transform, polarity, and the one-versus-two distinction

For a (d-1)-dimensional simplicial or Boolean-cell complex K, the barycentric transformation has the form

h(sd K;t)=Σ_(k=0)^d h_k(K) p_(d,k)(t),

where the refined Eulerian polynomials may be normalized recursively by

p_(0,0)=1,
p_(d,k)=t Σ_(i<k) p_(d-1,i)+Σ_(i≥k) p_(d-1,i),          (6)

with i ranging from 0 to d-1. The sequence is interlacing, so nonnegative h_k imply real-rootedness. This is the mechanism behind the Brenti–Welker theorem, in its proper domain.

### A concrete failure of the naive nonsimplicial substitution

If one mechanically applies the ordinary f-to-h formula to the cube's cell counts (1,8,12,6), one gets 1+5t-t²+t³. This is not a simplicial h-vector. Substituting it into (6) gives

1+23t+11t²+t³,

whereas the actual answer is 1+23t+23t²+t³. The error can also be seen before transforming to h: a square has eight nontrivial vertex-edge incidences, not the six incidences in a triangle. The Boolean transformation counts the wrong chains. The negative input coefficient is an additional warning, not the only defect.

Replacing this input with the toric h-vector does not repair the proof: no identity equating the desired ordinary barycentric h with that substitution has been supplied.

### Polarity gives all simple polytopes

The proper face posets of P and its polar P* are opposite posets. Reversing a chain gives an isomorphism of their order complexes, so

H_P(t)=H_(P*)(t).

Therefore the simplicial theorem also covers every simple polytope. This is a known equivalence, also recorded in the 2023 chain-enumeration paper.

### Every convex boundary is settled after two subdivisions

For arbitrary convex P, K=sd(∂P) is a simplicial sphere and hence Cohen–Macaulay, with nonnegative ordinary h-vector. Apply Brenti–Welker to this K. It follows that

h(sd²(∂P);t)

is real-rooted for every convex P, and so are all further iterates. This is a genuine universal partial result, but it does not answer the single-subdivision question. For the cube, applying (6) to (1,23,23,1) yields 1+143t+143t²+t³.

There is no valid reverse implication from a subdivision to the original h-polynomial. The boundary of a triangle already shows this: its h-polynomial is 1+t+t², which is not real-rooted, while its first barycentric subdivision has h-polynomial 1+4t+t², which is real-rooted.

**Outcome:** all simplicial and simple P, plus two and higher subdivisions for every convex P. **Obstacle:** removing the extra subdivision is a mathematically unjustified inversion; the first subdivision of a nonsimplicial cell complex is not the Boolean transformation of its ordinary cell counts.

## Approach 5. Pyramid/prism differential operators and closed families

The pyramid and prism identities for the ab-index use the derivation D with D(a)=D(b)=ab+ba:

2Ψ_Pyr(P)=Ψ_P(a+b)+(a+b)Ψ_P+DΨ_P,
Ψ_Prism(P)=Ψ_P(a+b)+DΨ_P.

These standard identities are recorded in Athanasiadis–Kalampogia-Evangelinou, Theorem 2.2, crediting Ehrenborg–Readdy. Since Ψ_P is homogeneous of ab-degree d and H_P(t)=Ψ_P(1,t), specialization gives

(DΨ_P)(1,t)=2dt H_P(t)+2t(1-t)H'_P(t).

Consequently

H_Pyr(P)=(1+(d+1)t)H_P+t(1-t)H'_P,                    (7)
H_Prism(P)=(1+(2d+1)t)H_P+2t(1-t)H'_P.                (8)

These formulas are consistent with the known preservation theorem in that paper. The following elementary proof checks the operator property directly for the polynomial class here.

### Root-preservation proof

For λ>0 define

T_(d,λ)H=(1+(λd+1)t)H+λt(1-t)H'.

For d=0, H is a positive constant and T_(0,λ)H=H(1+t), so the assertion holds directly. Now assume d≥1 and H has degree d, positive leading coefficient, positive constant term, and d distinct negative roots r_1<...<r_d. At each r_i,

T_(d,λ)H(r_i)=λr_i(1-r_i)H'(r_i),

whose sign is opposite that of H'(r_i). Therefore signs alternate at successive r_i. The leading coefficient of T is the leading coefficient of H, because (λd+1)-λd=1. Its sign near -∞ is opposite its sign at r_1. At r_d it is negative, whereas T(0)=H(0)>0. The intermediate value theorem therefore finds one root in each of

(-∞,r_1), (r_1,r_2), ..., (r_(d-1),r_d), (r_d,0).

These d+1 distinct negative roots exhaust its degree. Repeated roots of H follow by approximating the negative roots with distinct negative roots and using closedness of the real-rooted cone. Taking λ=1 and λ=2 proves (7) and (8) preserve real-rootedness.

### Exact examples and scope

Starting with the square, H=1+6t+t², (7) gives the square pyramid's polynomial 1+15t+15t²+t³. Starting with the cube gives

H_Pyr(cube)=1+50t+138t²+50t³+t⁴,
H_Prism(Pyr(cube))=1+159t+1040t²+1040t³+159t⁴+t⁵.

These identities were checked exactly, and their roots certified by rational root isolation. Repeated pyramid and prism operations starting from any proved seed generate real-rooted examples in arbitrarily high dimension. Polarity extends these families further, including the dual bipyramid operation. Such examples need not remain simple, simplicial, or cubical.

This does not justify a multiplication formula for arbitrary Cartesian products. Even the Cartesian product of two segments is a square: the input H-polynomials multiply to (1+t)², whereas H_square=1+6t+t². The incidence chains in a product are interleavings, not independent choices. Likewise, barycentric subdivision must not be assumed to commute with polytope join as an ordinary simplicial join. No closure assertion for general products or joins is proved here.

**Outcome:** exact root-preserving operators and infinite dimension-unbounded families, agreeing with an existing theorem. **Obstacle:** arbitrary polytopes are not known to be generated from the proved seeds by these operations, and a general product formula requires more than multiplication.

## Status and reproducibility

The five routes establish several precise partial results but do not resolve arbitrary convex P in a single subdivision. In particular:

- d≤5 is covered by a known theorem and the explicit short argument above.
- d=6,7 reduce to the cubic inequality (2), which is not proved for all polytopes here.
- The formal balanced examples are not polytopal counterexamples.
- The interlacing hypothesis is genuinely needed in a sum-based strategy.
- All convex boundaries have real-rooted h after two subdivisions, which does not settle one.
- Polarity, pyramids and prisms provide rigorous closed families, not all polytopes.

The companion authored script verify_residual.py checks the main displayed numerical examples, their stated discriminants, and real-root counts with exact rational root isolation. It does not enumerate polytopes or test unknown realizability. Its successful run ends with “PASS: symbolic identities, exact discriminants and rational root-isolation counts.” Numerical approximations are not used as proof certificates.

## Primary references and credit

1. F. Brenti and V. Welker, *f-Vectors of Barycentric Subdivisions*, Math. Z. 259 (2008), 849–865. https://arxiv.org/abs/math/0606356 ; https://doi.org/10.1007/s00209-007-0251-z . The theorem applies to simplicial/Boolean-cell complexes with nonnegative h-vector.
2. S. Murai and E. Nevo, *On the cd-index and gamma-vector of S*-shellable CW-spheres*, Theorems 1.1 and 1.2. https://arxiv.org/abs/1102.0096 . Theorem 1.1 supplies the colored-complex δ-realization used in Approach 1.
3. C. A. Athanasiadis and K. Kalampogia-Evangelinou, *Chain enumeration, partition lattices and polynomials with only real roots*, Combinatorial Theory 3 (1) (2023), #12. https://arxiv.org/abs/2205.03796 . The introduction records the known low-dimensional, simple and simplicial cases; Theorem 2.2 gives the ab-index identities, and Theorem 1.4 proves pyramid/prism preservation. These results are credited, not presented as new discoveries.
4. M. Hlavacek and L. Solus, *Subdivisions of Shellable Complexes*, FPSAC 2021 extended abstract, Theorem 3.1 and Section 4. https://www.mat.univie.ac.at/~slc/wpapers/FPSAC2021/29Hlavacek.pdf . The shelling/interlacing criterion is used only with its stated hypothesis.
5. C. A. Athanasiadis, *Face numbers of barycentric subdivisions of cubical complexes*. https://arxiv.org/abs/2009.02272 . This separately covers cubical convex polytopes. This theorem is not replaced here by the weaker stable-shelling cases.

The derivations and examples in this note are authored expositions of these tools and their limits. No assertion of priority is made for the low-dimensional consequence, duality observation, two-subdivision consequence, or differential-operator argument.
