# Turn 2: escape cones and regular support points

The aim of this second substantive attempt was a geometric nonexistence argument from a visibly exposed part of the body. It excludes two familiar subclasses. It does not identify those subclasses with every body admitted by the source's piecewise-smooth terminology.

## 2A. A regular support point prevents perfection

Let B be a compact planar body which, near a point q, is the closed subgraph of a C¹ function. Suppose a line through q supports B and is tangent to this graph. Then an open positive-flux set of incident rays makes exactly one reflection and is not retroreflected.

Proof. Translate and rotate so q=(0,0), the support line is y=0, B⊂{y≤0}, and the local boundary is y=g(x), with g(0)=g′(0)=0. Shrink the coordinate rectangle until |g′|<1/10. For boundary points p sufficiently close to q, every upward direction u with u_y>0 and |u_x|≤u_y leaves the subgraph immediately and crosses y=0 while still in the coordinate rectangle. Indeed, until that crossing the vertical increase strictly exceeds the maximum possible increase of g along the horizontal displacement. After crossing y=0 it cannot hit B again.

Normals at p are close to (0,1). Choose incoming v close to the downward normal, but in a small open interval avoiding exact normal incidence. Both −v and the specular outgoing vector w=v−2(v·n)n belong to the preceding upward cone. The reversed incoming half-ray and outgoing half-ray therefore meet B only at p. Since v is not normal, w≠−v. Varying p in an interval and v in an angular interval gives positive flux measure. ∎

Corollary. A compact planar body with a globally C¹ embedded boundary is not a perfect retroreflector. A supporting maximum exists by compactness and is regular, so the proposition applies. The argument is local and does not require global convexity.

## 2B. A finite simple polygon cannot be perfect

Here a polygonal body is the closure of the interior of a simple polygon with finitely many nonzero edges and nonempty interior. This is an explicit subclass assertion.

Let q be a vertex of its convex hull. The entire translated body B−q lies in a closed cone T of angle β<π. For a sufficiently small r>0, B inside the radius-r disk about q is precisely a sector W with angle 0<α≤β. In angular coordinates write T=[0,β] and W=[a,b], where 0≤a<b≤β. The outward normals to the two incident edges have angles a−π/2 and b+π/2 (modulo 2π). At least one normal n lies strictly outside T: if a<π/2 the first does, while if a≥π/2 the second has angle greater than π and less than 3π/2, hence lies outside T.

Let t be the unit edge direction from q for that normal. Because n lies strictly outside the closed cone T, there exists K>0 such that t+u n lies outside T for all u≥K. At p=q+δt, the ray p+s n, s>0, lies outside W while it stays in the small local disk, because n points to the exterior side of the edge. Choose δ so small that δ(1+K)<r. For s≤Kδ the ray is in that local disk and outside B; for s≥Kδ it is outside q+T and hence outside B globally. Thus the outward normal ray is unobstructed.

This argument is stable when p is varied in a sufficiently small open subinterval of the edge and the outward direction is varied in a small cone about n: choose the cone with closure disjoint from T, contained in the outward edge half-plane, and choose K uniformly on that closure. Take incoming v slightly off −n. Both −v and w=v−2(v·n)n lie in this clear cone. They define a one-reflection trajectory with w≠−v. These trajectories fill a positive-flux open set. ∎

## Remaining gap

These arguments do not establish that an arbitrary source-admissible body has a regular support point or the finite local sector used above. In particular, this packet does not silently replace piecewise smooth by globally C¹, finite polygonal, C¹ up to every singular endpoint, or a fixed number of hollows. Source §4 itself separates an infinite notched-angle boundary from a genuine piecewise-smooth hollow and uses truncation for the latter. No inference from the two special-class obstructions to the full source target is made.

The lemmas are elementary local geometry. Historical priority is not claimed. They are included as explicit attempted routes and proved scoped results, not as a claimed solution of the open existence question.
