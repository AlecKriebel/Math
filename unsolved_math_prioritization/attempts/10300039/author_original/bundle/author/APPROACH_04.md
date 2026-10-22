# 4. Flow endpoints and the uniform-quasigeodesic route

## Attempt

Exploit the new quasigeodesic Anosov theorem. Rather than infer asymptotic separation from a flow theorem by name, isolate exactly what uniform quasigeodesicity controls on one stable-type leaf.

## Hypotheses

L is a properly embedded plane in H^3, saturated by oriented complete flow lines. All these lines are (K,C)-quasigeodesics for common constants. All have positive ideal endpoint p, and q(a)!=p denotes the negative endpoint of an orbit a. Assume endpoint maps are continuous as functions of a point on L. For the additional proper-map statement, assume the orbit quotient Q of L is homeomorphic to R with its usual topology, and the projection L -> Q is continuous. These conditions are explicit; the theorem is not a claim about arbitrary taut foliations.

We use the standard Morse stability theorem in H^3: uniform quasigeodesics and the geodesics with the same two endpoints are a uniformly bounded Hausdorff distance apart, in both directions.

## Lemma 4: exact endpoint reduction

Let E={q(a): a an orbit in L}. Then Lambda(L)={p} union closure(E), with closure in S^2. Furthermore E is closed in S^2 minus {p}, and the induced map q:Q -> S^2 minus {p} is proper under the quotient hypothesis.

Proof of the limit-set formula. The containment from right to left follows by going to either end of each orbit and then using closedness of Lambda(L). Conversely let x_n in L approach z in S^2. Let a_n be its orbit and q_n=q(a_n). Pass to a subsequence with q_n converging to q. Let g_n be the geodesic with endpoints p,q_n and choose y_n in g_n with d(x_n,y_n) uniformly bounded. Then y_n also approaches z.

If q!=p, geodesic segments g_n converge locally to the geodesic with endpoints p,q. Their boundary accumulation points are p and q. This can be verified by sending p to infinity in the upper-halfspace model: the g_n are vertical lines above the convergent finite points q_n. Therefore z is p or q. If q=p, send a boundary point other than p to infinity; in that chart both endpoints of g_n tend to the same finite boundary point p, and the Euclidean hemispheres containing g_n have diameters tending to zero. Thus z=p. This proves the formula.

For properness, let A be compact in S^2 minus {p}. Every geodesic (p,q), q in A, meets one fixed compact ball: in the upper-halfspace chart with p=infinity, choose the points (q,1), which form a compact set. By the other direction of Morse stability, each corresponding orbit in L meets a common enlarged compact ball B. The set L intersect B is compact because L is properly embedded. The continuous projection of that compact set to Q is compact and contains q^{-1}(A). The latter is closed in Q by continuity of q, hence compact. Thus q is proper. A proper map from R to the locally compact metric space S^2 minus {p} has closed image: for a convergent sequence of image points, its preimages lie in the inverse image of a compact neighborhood and have a convergent subsequence. This also proves the closed-image statement directly without the quotient hypothesis by using convergent points in L intersect B and endpoint continuity.

Consequently, in this model Lambda(L)=S^2 precisely when E=S^2 minus {p}. The attempted proof reduces to non-surjectivity of a particular proper endpoint map.

## Why the reduction is insufficient

A proper continuous map R -> R^2 need not miss a point. For completeness, take a continuous surjection h_n:[n,n+1] -> the closed planar annulus n<=|x|<=n+1, with prescribed compatible endpoint values along the positive x-axis; such maps are obtained from a Peano parameterization of a rectangle, mapping the rectangle onto the annulus, and adjoining paths to fix endpoints. Begin with a surjection of [0,1] onto the unit disk, likewise with compatible endpoints. Concatenation gives a continuous surjection h:[0,infinity) -> R^2 for which |h(t)|>=floor(t)-1. Hence h is proper. The map t -> h(|t|) is a proper continuous surjection R -> R^2.

This is only an abstract endpoint-map countercontrol. It does not construct an embedded foliation or Anosov flow. It proves that the properness conclusion alone cannot close the reduction; further noncrossing, injectivity, or geometric restrictions are necessary.

## Source reconciliation

Fenley's 2026 main theorem supplies quasigeodesicity for non-R-covered Anosov flows; the same revised manuscript's p.85 explicitly discusses the full-sphere question. Buckminster's 2026 manuscript supplies leafwise extension and global universal-circle constructions, but those do not supply the missing non-surjectivity argument above. The inaccessible original behind the older AMS abstract remains a source lead requiring reconciliation. Accordingly this route claims only Lemma 4, not a positive solution even for the full Anosov subclass.
