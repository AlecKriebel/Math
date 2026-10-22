# A known filling with one hyperbolic conformal boundary

Problem 30002692, catalog code OWR-13347-011. Authored verification dated 2026-10-05.

## Conclusion and scope

The existential question printed by Eric Woolgar in the 2014 Oberwolfach report has an affirmative example already described in earlier literature. There is a complete, connected, orientable, smooth three-dimensional Riemannian manifold with sectional curvature identically −1, a smooth compact conformal compactification, and exactly one boundary component. That boundary component carries a smooth metric of sectional curvature −1 and can be chosen to be the closed orientable surface of genus two.

Xi Yin describes the relevant end-swapping construction in §6, equation (6.1), of arXiv:0710.2129v2 (2008), printed page 20. Skenderis and van Rees describe it again in §4.2, equations (44)–(46), of arXiv:0912.2090v2 (2010), printed pages 20–21. This note verifies the geometric requirements directly; it does not claim a new construction or priority.

The 2014 question is existential and does not specify a bulk dimension, parity, filling topology, spin condition, or renormalized-volume constraint. Its surrounding discussion restricts attention to unobstructed asymptotically Poincaré–Einstein metrics. The example below has an exact, smooth even expansion and meets that condition. A problem imposing a separately specified dimension, boundary, topology, or volume is a different assertion and is not settled here merely by the three-dimensional example.

The exact current unsolvedmath page could not be read: both direct retrieval and the cloud browser returned HTTP 403. Consequently this conclusion is tied to the inspected primary statement, with the catalog-to-live-page match expressly unverified.

## Construction theorem

Let (S,h) be a smooth connected closed m-dimensional Riemannian manifold, m≥2, of sectional curvature −1. Suppose τ:S→S is a fixed-point-free isometric involution. Define

    X = R × S,
    g = dt² + cosh²(t) h,
    J(t,p) = (−t, τ(p)),
    M = X / ⟨J⟩.

Then the quotient metric on M is complete, has constant sectional curvature −1 and Ricci tensor −m g, and is smoothly conformally compact with a single conformal boundary isometric to (S,h) for a suitable defining function. If S is oriented and τ reverses orientation, M is orientable.

### Smoothness of the quotient

Because τ is an isometry and cosh is even, J preserves g. The relation τ²=id gives J²=id. A fixed point would require t=0 and τ(p)=p; the latter is excluded. The finite group acts freely and properly, so the quotient is a smooth manifold without an interior boundary, and its metric is smooth. In particular t=0 does not become a reflecting boundary or an orbifold stratum. Its image is a smooth embedded copy of S/⟨τ⟩, with a possibly nontrivial normal line bundle.

### Constant curvature and the Einstein equation

Write f(t)=cosh t. The Levi-Civita connection of dt²+f²h, for vector fields U,V lifted from S, is

    ∇∂t ∂t = 0,
    ∇∂t U = ∇U ∂t = (f′/f) U,
    ∇U V = ∇h_U V − f f′ h(U,V) ∂t.

These formulas follow by applying the Koszul formula to ∂t,U,V, using that the lifted fields commute with ∂t. Substitution into the definition of curvature shows that a plane containing ∂t has sectional curvature −f″/f, a plane tangent to S has curvature (−1−(f′)²)/f², and the curvature components with one radial and three tangential slots vanish. Since f″=f and f²−(f′)²=1, both sectional-curvature expressions equal −1. The tensor components therefore agree with the full constant-curvature tensor, including planes that are not purely radial or tangential. In dimension m+1, summing the sectional curvatures in an orthonormal basis gives Ric(g)=−m g. The local isometry to the quotient preserves these identities.

### Completeness

The product metric g₀=dt²+h is complete because S is compact. The inequality cosh²t≥1 implies g≥g₀. If a sequence is Cauchy for the distance of g, it is Cauchy for g₀, hence has a limit in X. In a sufficiently small relatively compact coordinate neighborhood of this limit, the two smooth positive metrics are uniformly comparable. The sequence consequently converges for g as well. Thus g is metrically complete, and the Hopf–Rinow theorem gives geodesic completeness. Every quotient geodesic lifts locally, and hence along its interval of definition, through the Riemannian covering X→M. The complete lifted geodesic extends for all time, so the quotient is complete too.

### Compactification with one boundary

Set s=arctan(sinh t). Then s ranges over (−π/2,π/2), ds/dt=sech t, and cosh t=sec s. Hence

    g = (cos s)⁻² (ds²+h).

Let Xbar=[−π/2,π/2]×S, let ρ(s,p)=cos s, and let gbar=ds²+h. This is a compact smooth manifold with boundary; gbar is smooth and positive definite all the way to both boundary components. The function ρ is positive on its interior, vanishes precisely at the boundary, and satisfies dρ=−sin s ds≠0 there. It is therefore a smooth defining function, with ρ²g=gbar.

The action extends as Jbar(s,p)=(−s,τ(p)). It remains free, including at s=0, preserves ρ and gbar, and interchanges the two boundary components. Thus Mbar=Xbar/⟨Jbar⟩ is a compact smooth manifold with boundary, its interior is M, and both ρ and gbar descend smoothly. There are no missing ends or extra boundary components.

The map S→∂Mbar, p↦[(π/2,p)], is a diffeomorphism. Every boundary orbit contains a point on the positive component, and contains exactly one such point because the nonidentity element switches the sign of s. Restricting the descended gbar to this boundary gives precisely h. In particular the boundary is S, not S/⟨τ⟩. It is compact, connected, and has sectional curvature −1. The conformal infinity is its conformal class [h]; this construction additionally supplies h itself as a representative.

### Orientation and the expansion at infinity

If S is oriented and τ reverses orientation, J reverses both the R factor and S. The two signs multiply to +1, so the product orientation descends to M. The same holds for Mbar. Nothing in the construction requires the central hypersurface S/⟨τ⟩ to be orientable.

For an explicit geodesic defining function, choose the positive-end representative of a quotient collar and put x=2e^(−t). Direct substitution gives

    g = x⁻² [ dx² + (1+x²/4)² h ],
    (1+x²/4)² h = h + (x²/2)h + (x⁴/16)h.

This is an exact smooth even expansion with no logarithmic terms; |dx|² for x²g is 1. The corresponding function at the negative end is 2e^t, and the end interchange identifies these collar functions. No use is made of e^(−|t|) across t=0, where that formula would fail smoothness. The global smooth defining function is ρ=cos s. The metric is exactly Einstein, stronger than an asymptotic Einstein condition. This establishes the construction theorem.

## An explicit supply of admissible surfaces

For completeness, there is an elementary way to obtain S and τ without assuming a free involution on an arbitrary prescribed surface.

Take a regular geodesic hyperbolic hexagon with interior angle π/3. Such a polygon exists: divide it into twelve congruent right triangles, each with angles π/6, π/6, π/2; these angles have sum 5π/6<π, so the hyperbolic triangle exists. Reflecting the triangle across successive radii and side bisectors assembles the polygon.

Label the consecutive oriented sides a,a,b,b,c,c and identify each equally labeled pair in the direction of traversal. Equal side lengths make these isometric identifications. All six vertices are identified, and the corner link is a single circle. At the identified vertex the six angles sum to 2π; there is therefore no cone singularity. Across a glued geodesic edge the two half-disks give a smooth hyperbolic disk. The quotient N is consequently a closed connected smooth hyperbolic surface. It has one face, three edges and one vertex, so χ(N)=−1. The same-direction side pairings make it nonorientable; equivalently the polygon is the usual presentation of the connected sum of three projective planes.

Take the orientation double cover π:S→N and pull back the hyperbolic metric. Because N is nonorientable and connected, this double cover is connected. Its nonidentity deck transformation τ is fixed-point-free and isometric, and reverses the canonical orientation of S. Since χ(S)=2χ(N)=−2, the orientable closed surface S has genus two.

Apply the construction theorem with m=2. The resulting M is an orientable complete hyperbolic three-manifold, Ric(g)=−2g, with a smooth conformal compactification and one genus-two hyperbolic boundary. Topologically its compactification is the interval bundle (S×[−π/2,π/2])/((s,p)∼(−s,τp)) over N. Retraction to s=0 shows that its central closed nonorientable surface is an interior core, not a second boundary. This supplies the desired example.

## What has and has not been established

The printed existential question is answered by a construction documented before 2014, and the proof above verifies the complete Riemannian and conformal-compactness claims. No claim is made about all prescribed hyperbolic boundaries, every dimension, a specified filling topology, a spin structure, a volume extremum, or a globally current open-problem classification. The exact live aggregator statement is unreadable in the present environment. The argument does not infer existence from numerical ODE solutions or from a truncated formal Einstein expansion.

The accompanying exact controls verify algebraic identities and the polygon's finite gluing combinatorics. Completeness, smoothness, the existence of the hyperbolic triangle, and the quotient geometry are established by the written proof, not by the controls. This is an AI-assisted, unrefereed verification note; independent audit remains a separate step.

## Primary references

1. Eric Woolgar, “The evolution of APEs,” in *Mini-Workshop: Einstein Metrics, Ricci Solitons and Ricci Flow under Symmetry Assumptions*, Oberwolfach Reports 11 (2014), pp. 2549–2550; question on p. 2550. https://doi.org/10.4171/OWR/2014/45 . Inspected institutional PDF: https://publications.mfo.de/bitstream/handle/mfo/3435/OWR_2014_45.pdf?sequence=1&isAllowed=y .
2. Xi Yin, *Partition Functions of Three-Dimensional Pure Gravity*, arXiv:0710.2129v2, revised 30 May 2008, §6, p. 20, equation (6.1). https://arxiv.org/abs/0710.2129v2 .
3. Kostas Skenderis and Balt C. van Rees, *Holography and wormholes in 2+1 dimensions*, arXiv:0912.2090v2, revised 1 September 2010, §4.2, pp. 20–21, equations (44)–(46); Commun. Math. Phys. 301 (2011), 583–626. https://arxiv.org/abs/0912.2090v2 .
