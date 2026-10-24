# Independent adversarial audit: compact-special parabolic intersection

Reviewer: `/root/p21126_superexp/double_adversary`; UTC: 2026-10-24T21:23:37.731431+00:00. Input: `../../root_filters/COMPACT_SPECIAL_INTERSECTION_BARRIER.md`; exact hash in REVIEWED_INPUTS.json.

**Outcome: PASS after a minor signed-link wording clarification.** No outstanding mathematical objection at the stated hypothesis scope. This is a second, independently reconstructed presentation of the compact local-isometry filter, not a new unrestricted result.

## Precise checks

The local isometry hypothesis gives injective FULL maps of vertex links. Restriction to directions whose underlying generators lie in Λ is again full, so the base component Y of the inverse-image cubical subcomplex is compact and locally convex. All incident Λ-labelled cubes at a vertex in Y lie in that same component: their edges connect to that vertex. No global assumption that all other Λ-components are glued is needed.

The CAT(0) lifts of X and S_Λ through the standard vertex are convex subcomplexes. Their intersection is convex, nonempty, and connected; it is exactly the lifted base component Y. For h∈G∩P, the standard vertex and h times that vertex lie in the intersection, so a path there projects to a loop in Y. Conversely every loop in Y represents both a G-element and a P-element. This proves equality π1(Y)=G∩P, not only an inclusion or a conjugate subgroup. Compactness makes H finitely presented, and the cocompact isometric universal-cover actions give undistortion in G. The CAT(0) filling theorem yields the claimed quadratic intrinsic bound for H.

The target double Salvetti complex has no cubes involving exclusive vertices from both copies, because those vertices have no cross-edge in the doubled graph. The link at a glued vertex in the source is the union of the two old links along the entire Λ-direction sublink. All duplicate shared directions are glued. Any target simplex containing an exclusive direction lies in one copy, where fullness supplies its lift; an entirely shared simplex lies in Y. Thus the link map is injective and full. Van Kampen and π1-injectivity identify its group with the intended amalgam, and compactness plus nonpositive curvature gives quadratic intrinsic Dehn upper bound for the double.

## Adversarial boundary checks

- Λ=∅: the inverse image component is the base vertex, and the double is a wedge corresponding to a free product.
- Λ=Γ: connectedness gives Y=X and the double is X.
- H trivial with nontrivial contractible Y: the same local-link proof applies; it does not assume that Y consists of a single vertex.
- Disconnected Λ and additional components of the inverse image do not change the full-link argument.
- An abstract compact-special G with an arbitrary distorted algebraic embedding into a different RAAG is outside this proof. The note states this restriction explicitly.

A minor initial phrase described simplices by 'commuting distinct directions'. I requested that it explicitly exclude the two opposite signed directions of one generator, which are not adjacent in a Salvetti link. The final reviewed revision says that distinct underlying generators span a clique and excludes that opposite-sign pair. This fixes a presentation ambiguity; the local-isometry proof already used the standard link correctly.

Dependencies are standard convex lifting of cubical local isometries, the link criterion, van Kampen, and the CAT(0) quadratic filling bound. The independently inspected Fioravanti Lemmas 2.8 and 3.22(3) corroborate the convex/parabolic scope. No complete originality audit, full 21.126 resolution, or publication status is certified.
