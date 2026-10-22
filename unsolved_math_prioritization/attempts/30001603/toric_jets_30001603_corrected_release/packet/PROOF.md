# A prior counterexample to jet spanning from invariant-curve positivity

Problem 30001603 / OWR-4527-007. This is an attributed verification of a published counterexample, not a new discovery. The bundle is due to Sandra Di Rocco, Kelly Jabbusch and Gregory G. Smith, *Toric vector bundles and parliaments of polytopes*, Examples 4.2 and 5.3, Trans. Amer. Math. Soc. 370 (2018), 7715–7741, DOI [10.1090/tran/7201](https://doi.org/10.1090/tran/7201). The explicit argument below reconstructs its chart gluing, curve restrictions and missing jets. The journal PDF and [arXiv v3](https://arxiv.org/abs/1409.3109v3) were inspected; their polygon coordinates agree. See SOURCE_GATE.md for all reading limits.

## 1. The precise implication being refuted

In Kelly Jabbusch's contribution to [Oberwolfach Report 45/2010](https://ems.press/content/serial-article-files/46305), printed pp.2640–2641, the base field is algebraically closed and the toric variety is smooth and complete. The jet definition is introduced for smooth projective varieties. For a toric vector bundle E, write its restriction to an invariant curve C, isomorphic to P¹, as a sum of O(a_j). The number τ(E) is the minimum of all these integers over the invariant curves (equivalently, the minimum of the corresponding minima at fixed points). The conjectured implication is

    τ(E) ≥ k  ⇒  E is k-jet spanned, for integers k ≥ 1.

At x, k-jet spanning means that H⁰(X,E) → H⁰(X,E ⊗ O_X/m_x^(k+1)) is onto. The paragraph does not assume global generation. Its earlier distinction between nefness and global generation at k=0 does not remove the k=1 case. We use X=P²_C, which satisfies both the smooth-complete and smooth-projective hypotheses. C is an allowed algebraically closed field; no assertion concerning every positive characteristic is needed or made.

**Result.** There is a toric vector bundle F of rank three on P²_C that is nef, has τ(F)=1, and whose evaluation at one fixed point has rank two. Consequently it is not 1-jet spanned. This refutes the displayed universal conjecture at its permitted integer k=1. The same published bundle is in fact ample, by the ampleness half of Hering–Mustaţă–Payne's criterion; the proof below only needs, and proves, nefness.

For the last implication, the quotient O_X/m_x² → O_X/m_x induces a surjection on sections of the resulting sheaves supported at x. Thus a surjective first-jet evaluation would give a surjective value evaluation. Failure of the latter suffices; it is not being substituted for the original jet assertion.

## 2. An explicit bundle, without an existence guess

Let M=Z², with Laurent characters x^a y^b, and let the fan rays be

    v₁=(1,0),  v₂=(0,1),  v₃=(-1,-1).

Take σ₁=pos(v₂,v₃), σ₂=pos(v₁,v₃), σ₃=pos(v₁,v₂). These are the usual fan and three charts of P². Their rings are

    R₁=C[y/x,1/x],  R₂=C[x/y,1/y],  R₃=C[x,y].

In the common rational vector space C(x,y)³ choose, on chart i, the three frame columns b_ij x^(-u_ij,1)y^(-u_ij,2), where the following lists are ordered together:

- Chart 1: b=(e₁−e₂,e₂−e₃,e₃), u=((-1,-2),(-2,0),(-2,3)).
- Chart 2: b=(e₁,e₁−e₂,e₂−e₃), u=((4,-3),(0,-3),(-1,-1)).
- Chart 3: b=(e₁,e₂,e₃), u=((4,-2),(0,0),(-1,3)).

Call the resulting frame matrices F_i. Their constant column matrices B_i have determinant ±1. The modules F_i R_i³ are free of rank three. To prove that they glue, put G_ij=F_i⁻¹F_j. Direct multiplication gives

    G₃₂ = [ y    x⁴y    0   ]
           [ 0    -y³   xy  ]
           [ 0     0   -y⁴  ],

    G₃₁ = [ x⁵    0     0  ]
           [-xy²   x²    0  ]
           [ 0    -xy³   x  ].

These matrices and their inverses are regular on U₃∩U₂=Spec C[x,y,y⁻¹] and U₃∩U₁=Spec C[x,x⁻¹,y], respectively: their determinants are y⁸ and x⁸, units on the indicated overlaps.

On U₂∩U₁ use s=x/y and t=1/y; its ring is C[s,s⁻¹,t]. The third matrix is

    G₂₁ = [ 0  0   s⁶    ]
           [ s  0  -s²t⁴ ]
           [ 0  s  -st³  ].

Its determinant is s⁸, again a unit. Each inverse is regular by the adjugate formula. All cocycle identities follow from G_ij=F_i⁻¹F_j inside the same rational vector space. This constructs a locally free sheaf F. The action of (C*)² on rational functions, acting trivially on the constant vectors e_i, preserves each of these monomial-generated modules. It therefore glues to the required torus action on F: the bundle is toric.

The verifier checks all six ordered transitions, their inverses and all distinct-chart cocycles, rather than just matching an informal filtration diagram.

## 3. Invariant-curve restrictions and the exact number τ

There are three invariant curves C_r corresponding to the rays v_r.

On C₁, set x=0 in G₃₂. The resulting transition is diag(y,-y³,-y⁴). On C₂, set y=0 in G₃₁; the transition is diag(x⁵,x²,x). On C₃, set t=0 in G₂₁; after a constant permutation of the columns, the transition is diag(s⁶,s,s).

For clarity about the sign: on P¹ with coordinate z near zero and coordinate z⁻¹ near infinity, frames related by f_infinity=z^a f_zero define O(a). Indeed the rational section f_zero has a zero of order a at infinity, since f_zero=(z⁻¹)^a f_infinity. A nonzero constant multiplying the transition has no effect. Hence

    F|C₁ ≅ O(4) ⊕ O(3) ⊕ O(1),
    F|C₂ ≅ O(5) ⊕ O(2) ⊕ O(1),
    F|C₃ ≅ O(6) ⊕ O(1) ⊕ O(1).

Every integer is positive, and the smallest is exactly one. This is exactly the invariant in the report, so τ(F)=1. No Seshadri-constant normalization or estimate is being used in its place.

Here is the needed nefness argument, specialized from Hering–Mustaţă–Payne, *Positivity properties of toric vector bundles*, Theorem 2.1, [DOI 10.5802/aif.2534](https://doi.org/10.5802/aif.2534). We use the quotient convention P(F)=Proj Sym(F), with tautological line bundle L=O_P(F)(1). Each F|C_r is generated by sections: each O(a) for a≥0 is generated by its homogeneous monomials. Thus L on P(F|C_r) is globally generated and has nonnegative degree on every curve. On a fiber P² over a point, L is O(1), also nef.

For any integral curve Z in the projective variety P(F), take its limit under the first coordinate one-parameter torus, then the limit of that effective cycle under the second. Projective cycle-space compactness gives effective one-cycles, and degree against any fixed line bundle is unchanged by these degenerations. The second limit preserves invariance under the first torus because the actions commute. The final cycle is T-invariant. Each of its finitely many irreducible components is invariant (the connected torus cannot permute a finite set nontrivially), so its image in P² is either a fixed point or an invariant curve. L has nonnegative degree on every such component, as just proved. Additivity and invariance of degree give L·Z≥0. This holds for every curve Z, proving F nef.

The geometric inputs here are the standard existence of limits of effective cycles in a projective variety and invariance of intersection degree in that degeneration. This is the nef half of the inspected proof of HMP Theorem 2.1; it is explicitly credited, not a new foundational theorem. The stronger word “ample” above uses the other half of that theorem and is unnecessary for refuting the conjecture.

## 4. Why a value is missing

The preceding local frames give the following three decreasing subspace filtrations of V=C³. Their ray-height thresholds are obtained by taking the scalar products of the listed u with the rays:

- A(j)=V for j≤−1; A(0)=span(e₁,e₂); A(j)=span(e₁) for 1≤j≤4; A(j)=0 for j≥5.
- B(j)=V for j≤−2; B(j)=span(e₂,e₃) for −1≤j≤0; B(j)=span(e₃) for 1≤j≤3; B(j)=0 for j≥4.
- C(j)=V for j≤−1; C(j)=span(e₁−e₂,e₂−e₃) for 0≤j≤2; C(3)=span(e₁−e₂); C(j)=0 for j≥4.

For any u=(a,b), a Laurent monomial section v x^(-a)y^(-b) is global exactly when

    v ∈ A(a) ∩ B(b) ∩ C(-a-b).                       (1)

This formula can be checked directly, without importing a global-generation criterion: on chart i its coefficient in frame position j is (B_i⁻¹v)_j times the monomial with exponent u_ij−u. That coefficient is regular precisely when every nonzero term has nonnegative scalar product with both rays of σ_i. The corresponding spans are exactly the three spaces in (1). Checking all three charts gives (1). Any section on the torus is a finite Laurent sum in the constant basis. Distinct Laurent weights cannot cancel a forbidden monomial after the constant changes of basis, so the same test applies separately to every weight of a global section.

At u=(0,0), the first two spaces intersect in span(e₂). The third space is the plane of vectors whose three coordinates sum to zero. That plane does not contain e₂. Thus the weight-zero space of global sections is zero.

Let p be the origin of U₃=Spec C[x,y]. Its frame is (e₁x⁻⁴y²,e₂,e₃xy⁻³). A Laurent-weight section can have a nonzero coefficient in the middle frame direction at p only at weight u=(0,0): every other regular monomial coefficient vanishes at the origin. The weight-zero space was just shown to vanish. Therefore the image of H⁰(P²,F)→F_p misses this middle direction. The sections e₁x⁻⁴y² and e₃xy⁻³ are global by (1), and supply the other two independent directions. The value evaluation has rank exactly two out of three.

Combining this failure with τ(F)=1 and nefness proves the result in Section 1. There is no remaining mathematical obstruction to refuting the primary conjecture.

## 5. Complete finite section and jet certificate

For replay and a stronger diagnostic, all nonzero weight spaces in (1) are one-dimensional. They are the following four groups (signs of spanning vectors are immaterial):

- Span(e₁), at (3,-2), (4,-3), (4,-2).
- Span(e₁−e₂), at (-1,-2), (0,-3), (0,-2).
- Span(e₂−e₃), at (-2,0), (-1,-1), (-1,0).
- Span(e₃), at (-2,3), (-1,2), (-1,3).

Here is an exhaustive derivation, not an unbounded search. If a>0, A(a) forces e₁, B(b) then requires b≤−2, and C(-a-b) requires a+b≥1; also a≤4. These are exactly the three e₁ weights. If b>0, B(b) forces e₃, A(a) requires a≤−1, and C requires a+b≥1, with b≤3; these are exactly the three e₃ weights. In the remaining case a,b≤0:

1. For a≤−1,b≤−2, the first two spaces are V; the third is nonzero only when -a-b≤3. This gives (-1,-2) and span(e₁−e₂).
2. For a≤−1,b∈{-1,0}, the intersection is span(e₂−e₃) exactly for -a-b≤2; it is zero when the third space is its smaller line. This gives (-1,-1),(-2,0),(-1,0).
3. For a=0,b≤−2, the intersection is span(e₁−e₂) exactly for b=-2,-3.
4. For a=0,b∈{-1,0}, the first two spaces intersect in span(e₂), which the third excludes.

Values outside the displayed filtration ranges vanish. This proves that the twelve sections exhaust H⁰(P²,F).

On U₁ the local coordinates are y/x and 1/x. Each of its three frame vectors, multiplied by 1 and each of these two coordinates, occurs among the twelve sections. On U₂ the corresponding statement holds for x/y and 1/y. Their first-jet evaluations therefore have rank nine, the dimension 3·dim C[x,y]/(x,y)².

On U₃ the e₁-frame and e₃-frame directions each have their value, x term and y term. The global section (e₂−e₃)x has jet x times the e₂-frame, since its e₃-frame coefficient has order three in y. The remaining e₁−e₂ sections contribute no e₂ terms of degree ≤1; the other e₂−e₃ sections contribute only terms of degree ≥2 there. Thus the first-jet image is exactly the span of these seven distinct frame monomials. The missing rows are the e₂ value and its y derivative. This proves first-jet ranks (9,9,7) and value ranks (3,3,2) at the three fixed points.

VERIFY.py reconstructs the Laurent transition identities, invariant-curve restrictions, complete section spaces and jet matrices using exact rational arithmetic. It also checks a deliberately incompatible local weight, the false section produced by omitting the third ray, O³, O(1)³, O(-1)³ and a synthetic polygon-coordinate sign error. Finite checks corroborate these explicit proofs; they are not a substitute for nefness or an inference about arbitrary bundles.

## 6. Source agreement and attribution boundary

The journal's printed p.7728 and arXiv v3 p.13 both give (-1,-2) as a vertex of the polygon indexed by e1-e2. Its second-ray upper height is -2, so every permissible vertex has b <= -2. The remaining bounds give the other vertices (0,-3) and (0,-2). These coordinates agree with the explicit frames. Replacing (-1,-2) by (-1,2) is used only as a deliberate synthetic negative control; no printed sign discrepancy was found in the inspected sources.

The contribution of this record is an auditable verification and connection to the older jet conjecture. The counterexample itself and its positivity properties are prior work of Di Rocco–Jabbusch–Smith; the toric nefness criterion is Hering–Mustaţă–Payne. No claim of novelty, formal proof-assistant certification, exhaustive historical priority, or conventional human peer review is made.
