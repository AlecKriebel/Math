# Compact special parabolic intersections and their doubles

Candidate partial mechanism filter, October 24, 2026 UTC. This is a standard local-isometry deduction, not a claim of novelty or a resolution of 21.126. Fresh adversarial review is pending.

## Exact hypothesis

Let X be a connected compact cube complex equipped with a cubical local isometry f:X→S_Γ to the Salvetti complex of a finite RAAG A_Γ. Choose a vertex x of X as basepoint. Let Λ be an induced subgraph of Γ, with standard Salvetti subcomplex S_Λ⊆S_Γ and standard parabolic subgroup P=A_Λ. Identify G=π1(X,x) with its injected image in A_Γ. Put H=G∩P.

Let Y be the component containing x of the cubical inverse image f^-1(S_Λ). Then:

1. Y is compact and locally convex in X, with π1(Y,x)=H under the given injections.
2. H is finitely presented, compact special, and undistorted in G. Its intrinsic Dehn function is at most quadratic.
3. The double D=G*_H G is the fundamental group of the compact cube complex Z=X∪_Y X. The evident map Z→S_Γ∪_{S_Λ}S_Γ is a cubical local isometry. Its target is the Salvetti complex of the graph obtained by doubling Γ along Λ. Consequently D is compact special and has at most quadratic intrinsic Dehn function.

These assertions concern the PARTICULAR locally isometric embedding f. They do not assert that every finitely presented subgroup embedding in a RAAG is convex or has such a compact cubical realization.

## Proof of the intersection assertion

The link of every vertex of a Salvetti complex is the flag complex on signed generator directions, with simplices given by signed directions on distinct underlying generators spanning a clique. Opposite signs of the same generator do not span a link edge. The link of S_Λ is the full subcomplex on the Λ directions. A cubical local isometry has an injective full map on each vertex link. Taking the inverse image of the Λ directions therefore gives a full subcomplex of each link of X. Thus Y→X and Y→S_Λ are local isometries. The inverse image is a subcomplex of finite X, so Y is compact.

For completeness, the standard CAT(0) lifting argument identifies the intersection precisely. Lift f to an isometric convex embedding of universal covers into the CAT(0) universal cover of S_Γ, taking a lift of x to the standard vertex. A lift of S_Λ through that vertex is also convex. The intersection of these two convex subcomplexes is convex and connected, and is the lift of the component Y. If h∈G∩P, both convex subcomplexes contain the basepoint and its translate by h, and hence contain the geodesic joining them. This gives a loop in Y representing h. Conversely a loop in Y represents elements of both G and P by its two inclusions. Thus π1(Y)=G∩P, with no finite-generation assumption required for that intersection.

Both universal-cover inclusions are isometric, so cocompactness of the deck actions gives undistortion of H in G. Y is itself compact special because it locally isometrically maps to S_Λ. Its universal cover is CAT(0), giving a quadratic filling upper bound. This also follows by the usual geodesic-combing filling for a compact nonpositively curved cube complex.

## Proof for the double

Since Y is a connected subcomplex and its inclusion is π1-injective, van Kampen identifies π1(Z) with the amalgam D. Distinguish generators outside Λ by which copy of Γ they belong to. The union S_Γ∪_{S_Λ}S_Γ is exactly the Salvetti complex of the doubled graph: a clique can use exclusive vertices of only one copy, so no additional mixed cube is present.

At a vertex of Z outside Y, the map of links is the original injective full link map into one copy. At a vertex in Y, its link is the union of two copies of the link of X, identified along the full Λ-direction sublink. The target link is the corresponding union of two copies of the Γ link, identified along the full Λ sublink. Directions exclusive to opposite copies have no edge between them in either complex. A target simplex entirely on one side lifts by fullness of f; a simplex on only shared directions lies in Y. Hence the doubled link map is injective and full. This proves that Z→S_Γ∪_{S_Λ}S_Γ is a cubical local isometry. In particular Z is nonpositively curved and compact, so D has a quadratic intrinsic Dehn upper bound.

Components of f^-1(S_Λ) other than Y need not be glued. They do not affect the local link argument: at a vertex of Y, all incident Λ-direction cubes already belong to that same connected component. Trivial H or P, disconnected Λ, and Λ=Γ cause no problem. In the last case Y=X and the double is just G.

## Research consequence and exact gap

If a free subgroup H is highly distorted in a compact special group G, it cannot equal G∩P for a standard parabolic P in any embedding induced by a compact cubical local isometry as above. Furthermore even without a distortion claim, the displayed natural parabolic double stays compact special with quadratic fillings.

This blocks a direct use of a highly distorted free fiber from a compact special group as such a parabolic intersection and then doubling to obtain huge intrinsic Dehn growth. An arbitrary algebraic RAAG embedding, a noncompact source without a compact convex core, or a different construction is outside the proved scope. Proving one of those new mechanisms remains necessary; the full existence question is unchanged.

Dependencies are the standard Salvetti/link criterion for a cubical local isometry, its convex CAT(0) universal-cover lift, van Kampen, and the CAT(0) quadratic Dehn bound. The primary source ledger will identify the inspected formulations. The proof must not be used without the compact local-isometry hypothesis.
