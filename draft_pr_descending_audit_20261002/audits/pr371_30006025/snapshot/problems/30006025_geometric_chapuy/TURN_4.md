# Turn 4: an angle-independent perimeter obstruction for direct hyperbolic realizations

## Target and scope

The original source is Baptiste Louf's Question 4 in OWR 41/2024, printed page 2405: a geometric adaptation of Chapuy's bijection in the context of random surfaces. It does not formally define the required adaptation. Its one-face metric-map ensemble has face perimeter **12g**, meaning twice the sum of edge lengths. The comparison surfaces are closed, smooth, orientable surfaces of genus g with curvature **−1**. These normalizations cannot be interchanged with an area normalization of a metric graph: a graph is one-dimensional and its length measure is not the surface area.

This turn proves a necessary condition for a specific direct realization: embed the input one-face graph in such a surface, with the assigned lengths equal to the arclengths of its piecewise geodesic edges, and with the complement a disk. Unlike turns 1–2, the obstruction does not prescribe angles or require algebraicity. It does not rule out geometric adaptations that change the lengths, topology, curvature, or sense of comparison.

## Credited geometric input and applicability

Ivan Izmestiev, *A simple proof of an isoperimetric inequality for euclidean and hyperbolic cone-surfaces*, arXiv:1409.7681v1 (26 September 2014), Theorem 1, states the intrinsic hyperbolic disk inequality

    P² ≥ 4π A + A².

The theorem is for a hyperbolic cone-metric on a topological disk with negative curvature at every interior cone point. Its definitions explicitly allow boundary sectors of any positive angle. Thus reentrant corners are allowed. In our application there are **no interior cone points**, so the interior restriction is vacuous. This is a theorem about an intrinsic disk, not merely a convex polygon or an injectively developed domain in H². Its applicability does not require an injective developing map. The first page was visually checked. The paper credits earlier Alexandrov inequalities and, in its Riemannian formulation, Bol's theorem. We use this established inequality; we do not claim a new isoperimetric theorem.

Let G be a finite graph cellularly embedded with one face in a smooth closed hyperbolic surface S of genus g≥2. Assume its edges are positive-length, embedded piecewise geodesic arcs whose interiors are disjoint, and its finitely many incident branches determine positive sectors at vertices. Subdivide any edge bends if needed. The intrinsic cut surface D is obtained by separating the two sides of each edge and the incident sectors at vertices. Because the embedding is cellular and has one face, this compact cut surface is a topological disk. A repeated appearance of a vertex in the face word gives distinct boundary occurrences in D. In particular, boundary identifications in the original surface cause no singular interior point of D.

Each point of the interior of D has the original curvature −1. Each boundary corner is a positive sector in a smooth neighborhood of S; sectors can be greater than π, and at an isolated leaf can be 2π. The cut object is therefore precisely an allowed intrinsic hyperbolic cone-disk, with no interior cone singularities. The graph has surface area zero, while each edge has **two boundary copies**, including a bridge whose two sides belong to the same face. Consequently

    A(D) = area(S) = 4π(g−1),
    P(D) = 2 ∑e length(e).

The area identity is Gauss–Bonnet at curvature −1. No convexity, equal-angle condition, or planar development has been assumed.

## Theorem 4.1: necessary perimeter and the first excluded genus

Every direct realization just described satisfies

    P ≥ 4π √(g(g−1)).                                  (1)

In particular, an input face perimeter P=12g cannot be preserved for any integer g≥12.

**Proof.** Substitute A=4π(g−1) into the credited inequality:

    P² ≥ 16π²[(g−1)+(g−1)²] = 16π² g(g−1).

Both sides of (1) are nonnegative. For P=12g, (1) would imply

    π²(g−1) ≤ 9g.                                      (2)

At g=12 the opposite strict inequality follows already from π>157/50. The difference π²(g−1)−9g is increasing in g because π²>9. Thus (2) fails for every g≥12. Conversely, π<22/7 shows 10π²<99 at g=11, and monotonicity then shows (2) holds for every integer 2≤g≤11. This only says the **bound** does not exclude those genera; it asserts no existence there. ∎

The rational bounds for π are independently certified in the verifier using Machin's identity and alternating arctangent series. The geometric argument is valid for all genera, not established by a finite scan.

## Theorem 4.2: quantitative unavoidable metric change

Suppose an input map of genus g has edge lengths ℓe>0 with

    ∑e ℓe = 6g,

and a direct realization with the same edge correspondence uses output lengths ℓ′e>0. Put

    s_g = (π/3) √(1−1/g),       δ_g = s_g−1.

Then

    ∑e ℓ′e / ∑e ℓe ≥ s_g,                              (3)
    ∑e (ℓ′e−ℓe) ≥ 6g δ_g,                             (4)
    ∑e |ℓ′e−ℓe| / ∑e ℓe ≥ δ_g,                        (5)
    max_e (ℓ′e/ℓe) ≥ s_g.                              (6)

For a cubic one-face map, E=6g−3 and hence

    max_e |ℓ′e−ℓe| ≥ 6g δ_g/(6g−3).                    (7)

When δ_g is negative the corresponding lower bounds are merely vacuous; for g≥12 they are positive. In the large-genus limit, (5) and (7) have the same strictly positive lower limit **π/3−1**. In particular no such realization can preserve all lengths with a uniform relative error tending to zero, nor have vanishing relative total absolute error.

**Proof.** Inequality (1) gives 2∑ℓ′≥12g s_g, proving (3)–(4). The triangle inequality yields ∑|ℓ′−ℓ|≥∑(ℓ′−ℓ). The left side of (3) is the weighted mean of ℓ′e/ℓe with positive weights ℓe/(6g), proving (6). Finally ∑|ℓ′−ℓ|≤E max|ℓ′−ℓ|, giving (7). The limits follow from s_g→π/3. ∎

The same limiting ratio obstruction holds if the input perimeter P_g satisfies P_g/(12g)→1: divide (1) by P_g. For later use, for every g≥100 there is the convenient exact estimate

    δ_g > 1/25.                                        (8)

Indeed s_g² > (157/150)²(99/100) > (26/25)²; all terms are positive, and s_g increases with g.

## Relation to earlier turns and the original problem

This rules out more than a prescribed equal-angle polygon: arbitrary admissible corner angles cannot repair a **total perimeter deficit** in a direct one-face smooth curvature−1 realization. It does not contradict the regular-polygon construction in turn 3, whose perimeter is different and larger. It also does not prove that a graph metric cannot approximate a random surface in a weaker metric or probabilistic sense. A Gromov–Hausdorff comparison, for example, need not control the total arclength of an embedded one-face graph. Nor does this claim cover cone surfaces with a changed area formula, multiple-face embeddings, nongeodesic boundaries outside the stated category, or a different curvature normalization.

The source's broad geometric construction problem is still unresolved. This is the fourth substantive author turn. The fifth direction will quantify the necessary length changes under the actual Dirichlet length law, rather than reiterate this deterministic obstruction.

## Verification scope

`verify_turn4.py` uses exact rational arithmetic only. It checks Machin's arctangent bounds, the exact threshold inequalities, the all-g monotonic coefficients, the later 1/25 bound, the symbolic polynomial coefficient identity in the area substitution, and independent rational examples of the elementary deformation inequalities. It is supplementary; neither finitely many genera nor finitely many vectors constitute the proof of the geometric theorem above.

Primary input: https://arxiv.org/abs/1409.7681
Original source: https://ems.press/journals/owr/articles/14298589
