# Independent adversarial audit: parabolic-intersection doubles

Reviewer: `/root/p21126_superexp/double_adversary`; UTC: 2026-10-24T21:20:45.492500+00:00. Input: `../PARABOLIC_DOUBLE_ROUTE.md`, exact hash in REVIEWED_INPUTS.json.

**Outcome: PASS for the stated embedding mechanism and the canonical compact-special obstruction.** No unrestricted construction or solution of 21.126 follows.

## Algebraic construction

The RAAG on two copies of Γ glued exactly along the induced full subgraph Λ has defining presentation A_Γ *_A_Λ A_Γ. For a reduced word in G *_H G, each interior syllable outside H remains outside P in the ambient factor because H=G∩P. Its image is therefore a reduced ambient amalgam word and is nontrivial. A length-one word is handled by the original inclusion of G. This proves injectivity without a separability or quasiconvexity assumption. Finite presentability uses finitely many generators of H, not a finite presentation of H.

The centralizer extension has the same correct criterion. Britton reduction in the ambient HNN extension is preserved because every G-syllable outside H is outside P. Adding a new RAAG vertex commuting precisely with Λ gives the advertised ambient HNN extension. Finite generation of H supplies finitely many commutation relations. Arbitrary distorted H≤G does not meet this criterion merely by being a subgroup; exact equality with the parabolic intersection is essential.

## Independent convex-intersection proof

Let Y be the G-cocompact convex subcomplex containing the standard vertex 1, and Z the standard P-subcomplex. For z∈Y∩Z choose g∈G and p∈P uniformly near z. There are only finitely many possibilities r=g^{-1}p. Fix (g_r,p_r) for each. Then

    g g_r^{-1}=p p_r^{-1}∈G∩P.

Consequently z is uniformly near an H-orbit point. The nonempty intersection is convex, so it is connected and edge-geodesics yield finite generation and an intrinsic word metric bounded linearly by ambient distance. Properness and finite generation supply the reverse bound. This proves undistortion in G. The finite-ball argument uses the finite defining graph and the standard proper cubical action, both explicitly present.

I independently read the cached primary text of Fioravanti, arXiv:2108.13212v4: Lemma 2.8 gives convex-cocompact intersection (via the gated projection, equal to the intersection when the sets meet), and Lemma 3.22(3) gives convex cocompactness of G-parabolic subgroups. This corroborates the stated scope; the elementary based proof above does not depend on an unproved generic combination theorem.

## Local-isometry double

For a based compact local isometry X_G→S_Γ, its universal-cover image is convex. The full inverse image of Λ-labelled cubes is locally convex, and the base component is finite. Its lifted component is the intersection with the standard P-subcomplex, so its fundamental group is exactly G∩P. This proves equality in the chosen embedding, not only inclusion up to conjugacy.

At a vertex of that component, EVERY incident Λ-direction edge belongs to the component. Thus the two copies in the double identify every shared link direction; no duplicate direction survives. An edge or simplex of the target link cannot mix exclusive directions from the two different copies, since the doubled graph has no edge between them. A simplex lying on one side lifts by the original fullness condition, while one containing only shared directions lies in the glued subcomplex. This proves both injectivity and fullness of the link map, including mixed cliques involving shared directions. Compactness and nonpositive curvature then give quadratic intrinsic Dehn upper bound.

Boundary cases Λ=∅, Λ=Γ, trivial H, disconnected Λ, and additional unglued Λ-components all satisfy this check. For Λ=Γ the base component is all of connected X_G and the double is just G. The proof does not generalize to an arbitrary algebraic embedding of an abstractly compact special group: the local-isometry/convex-core hypothesis is essential. The note preserves that distinction correctly.

No high-distortion parabolic intersection with a qualifying intrinsic lower bound has been produced. The negative filter blocks the canonical local-isometry construction only. This review is not a complete novelty audit and approves no solved status or publication.
