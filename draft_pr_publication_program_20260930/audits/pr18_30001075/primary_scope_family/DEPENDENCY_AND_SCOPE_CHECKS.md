# Checkable independent derivations

These are adversarial checks of the frozen candidate's application, not finite numerical tests and not a replacement new proof program.

## Support increment and projection

Let C be a nonempty compact convex subset of R²×R, write p=(x,z), and fix a unit n∈R². Let fᵥ(p)=n·x−z n·v and hᵥ=max_C fᵥ. For an increment δv, set b(p)=−z n·δv. The general maximum inequality

min_C b ≤ max_C(fᵥ+b)−max_C fᵥ ≤ max_C b

follows by bounding fᵥ+b above by fᵥ+max b and evaluating it at a maximizer of fᵥ for the lower bound. Subtracting this inequality from n·δu proves

min_C n·(δu+zδv) ≤ δ[n·u−hᵥ] ≤ max_C n·(δu+zδv).

In particular this estimate is valid for nonsmooth support functions, arbitrary faces, and positive-length contact intervals. A maximizing normal may change under the increment; the estimate itself fixes n and has no hidden differentiation.

Put Pᵥ={x−zv:(x,z)∈C}. It is compact convex. For g=max_|n|=1(n·u−h_Pᵥ(n)), support inequalities give g<0 in int Pᵥ, g=0 on ∂Pᵥ, and g>0 outside Pᵥ, provided Pᵥ has nonempty R² interior. Outside, strict separation supplies g>0. Inside, a small disk around u makes all support inequalities strict with a uniform negative bound. On the boundary a supporting line gives equality and all other inequalities are nonpositive.

A supporting line n·(y−u)=0 of Pᵥ lifts to the plane n·(x−zv−u)=0 containing L(u,v). Attainment in Pᵥ gives an actual intersection with C. Conversely, a plane containing L(u,v) has nonzero transverse normal n and its projected support inequality makes u a boundary point. Thus the precise original tangent convention, including an actual intersection, is recovered. Closedness/compactness is used here to prevent phantom projection contacts at unattained limit points; it has already been supplied by the reduction.

For dimension three, any projection along a line onto R² maps an interior ball to a disk. For dimension two, its restriction to aff C has rank two exactly when the direction is transverse to that plane. If a direction lies in that plane and its line meets the set, the entire line lies in the plane. Those swept points therefore form a null planar exceptional set. The equivalence is never used for projected intervals/points, whose ambient interior is empty.

## Local compact caps and countability

For arbitrary disjoint convex Kᵢ and an actual common tangent, choose contacts aᵢ. Disjointness makes them distinct. Three pairwise disjoint rational closed balls with each contact in its interior exist by rational approximation and a radius smaller than the minimum pairwise contact distance. Cᵢ=closure(Kᵢ)∩Bᵢ is nonempty compact convex. Its intersection with the tangent contains aᵢ. A closed containing halfspace for Kᵢ contains closure(Kᵢ), so the original support plane also supports Cᵢ. There are countably many ball triples in the fixed ambient coordinates. This proves containment in a countable union of compact-case loci, even if original closures intersect and even if the originals are not initially assumed measurable. Empty originals give an empty common tangent locus and need no contact choice.

For a compact body A and contact a in the interior of a cap ball D, projected support normals at a agree for A and A∩D. The inclusion from A to the cap is immediate. For the reverse, if a supporting linear functional for the cap were positive at x∈A after normalizing its value at a to zero, the points a+t(x−a) would belong to the cap for sufficiently small positive t and have positive value, a contradiction. The same local segment argument produces the original affine dimension inside the cap: take affinely independent points of A and move a short positive distance toward them.

At a boundary contact of a two-dimensional projection, take an interior disk centered at w of radius r. Every outward normal n has n·w≤−r, so e=−w/|w| satisfies n·e≥r/|w|>0. The strict lower bound is stable for all maximizing normals near the reference line by compactness of S¹ and continuity of the gap. A thin cap confines its heights, making the own displacement bounded below and the cross displacement uniformly small. The elementary increment estimate above is sufficient; it supplies a strictly monotone scalar coordinate without a differentiable normal field.

The implicit-zero argument has an explicit elementary hypothesis map. If g(a,b,r) is Lipschitz and increases at least m h under a positive h in a, then its unique zero ρ(b,r), whenever bracketed, has |Δρ|≤Lip_(b,r)(g)|Δ(b,r)|/m. Bracketing persists on sufficiently small boxes by continuity and g(0,0,0)=0. For two such roots with cross constants k_A,k_B<1/4, the map (a,b)↦(ρ_A(b,r),ρ_B(a,r)) is a contraction in the maximum norm with constant k=max(k_A,k_B)<1. Because it is zero at the origin when r=0, continuity makes a smaller r-ball map a chosen square into itself. The fixed-point comparison gives

|x(r)−x(r′)|∞ ≤ [L/(1−k)]|r−r′|,

where L bounds its parameter dependence. Thus a Lipschitz graph follows without a nonsmooth implicit-function theorem or an assumption on the unknown tritangent subset.

Countability must be taken for fixed cap pairs, not by merely covering the original common tangents by neighborhoods whose graph concerns a different cap. For each fixed pair, let T be the subset of cap-common tangents where a construction exists. An arbitrary cover of T by open line-space neighborhoods has a countable subcover since line space is second countable: for every point choose a basis element containing it and lying inside its construction neighborhood; select one neighborhood for each basis element. Each covered point is a simultaneous cap zero in the chosen neighborhood, hence in its graph. Countably many cap pairs complete this countable cover. This is the countability mechanism written in the candidate; no stronger global smooth stratum is imported.

## Borel selection, density, and Jacobian

For compact C, if tangent lines Lⱼ converge in a finite line chart, choose contact points pⱼ∈C and unit support normals νⱼ. Subsequences converge to p∈C and ν with |ν|=1. The equations placing pⱼ on Lⱼ and νⱼ perpendicular to their directions pass to the limit. The containing-halfspace inequalities pass to the limit for every x∈C. Consequently the limit line still meets C and has a support plane. Tangency is closed in line space. Lines contained in a fixed affine plane form a closed subset; a line identical to a fixed supporting affine line is a closed singleton. Preimages under a continuous chart and removal of those exclusions are Borel. The candidate's E is therefore Lebesgue measurable.

Here is the full density-sampling justification. If q₀ is a density-one point of measurable E⊂R², then for each fixed h∈R²,

dist(q₀+τh,E)=o(τ) as τ↓0.

Otherwise there are η>0 and τⱼ↓0 with an open disk of radius ητⱼ/2 centered at q₀+τⱼh missing E. That disk is contained in a disk about q₀ of radius (|h|+η)τⱼ, yielding a fixed positive missing-area fraction and contradicting density one. Choose qⱼ∈E within o(τⱼ) of the center. Differentiability of the full Lipschitz chart at q₀, rather than of a path in E, gives its prescribed first-order displacement. The same argument works for every needed h, and does not assume that E has interior or contains any curve.

For an interior ball B(c,r) of a full-dimensional C and contact a=(0,zᵢ), the points (1−τ)a+τB(c,r) form a ball of radius τr in C. An onto transverse differential A+zᵢB allows a parameter direction whose first-order transverse displacement equals c_x. At height zᵢ+τ(c_z−zᵢ), the nearby selected tangent enters that ball up to an o(τ) error. A support-plane tangent cannot enter the interior of a full-dimensional C. For a planar C transverse to the reference line, use a relative interior disk and the smooth unique intersection with aff C instead. Its first-order height is fixed by its planar equation, so the same disk comparison produces a forbidden relative interior contact. At a relative interior point the only support plane is aff C, which cannot contain a transverse line.

For a segment in the line a+λ(d_x,d_z), a retained reference tangent is different from that line, hence d_x≠0. Nearby intersections satisfy u+zᵢv=(d_x−d_zv)λ. Dotting with d_x proves λ=O(|u|+|v|), with a denominator tending to |d_x|²>0. Against a perpendicular n, n·(u+zᵢv)=−d_z(n·v)λ is second order along density samples. The first-order image lies in span(d_x). For a point, u+zᵢv vanishes on E and the first-order image is zero. Thus the rank restriction does not require full dimension or a single-contact assumption.

Disjointness makes any selected contact heights z₁,z₂,z₃ distinct. The determinant det(A+zB) is a polynomial of degree at most two with three distinct roots, so is identically zero. Multiple contacts cause no difficulty: any three chosen contacts, one in each disjoint set, suffice.

On a bounded chart patch Q and |z|≤M, boundedness of v and the estimate

|(u(q)+zv(q))−(u(q′)+z′v(q′))| ≤ (Lip u+M Lip v)|q−q′|+sup_Q|v||z−z′|

make the sweep G(q,z)=(u(q)+zv(q),z) Lipschitz. At each differentiability point q of the chart, it is differentiable for every z, and its 3×3 Jacobian determinant is det(Du+zDv). By Rademacher and density, the bad q inside E have two-dimensional measure zero. Their product with a finite height interval has three-dimensional measure zero by Fubini, and a Lipschitz map sends an equal-dimensional null set to a null set. Alternatively the area formula includes that exceptional set in its almost-everywhere assertion.

For measurable H=(E∩Q)×[−M,M], the equal-dimensional area formula gives

L³(G(H)) ≤ ∫_H |det DG| dL³ = 0,

since the image multiplicity is at least one on the image. Injectivity is irrelevant. One can choose countably many relatively compact open cubes in the parameter domain and finite height intervals. The locally Lipschitz area formula applies directly on their open neighborhoods; a coordinatewise scalar Lipschitz extension supplies a global-map version if needed. This proves outer nullness, as any subset of a Lebesgue-null image is null. No smooth Sard theorem or C¹ structure is used.

## Lower-dimensional coverage and limiting cases

If a point is among the objects, any common tangent line passes through it and directions have finitely many ordinary R² charts on the direction sphere modulo sign. If no point is present and at most one set has dimension≥2, two compact segments remain. The line through a(s),b(t) depends smoothly on their endpoints as long as they differ. Compact disjointness gives min|a−b|>0. On a chart whose nonzero direction component stays bounded away from zero, the intercept/slope coordinates are Lipschitz; endpoint parameters can be extended slightly into open intervals while still distinct. A finite or countable chart cover then works, selecting only actual tritangents in E.

Lines in planar affine hulls or identical to segment affine hulls sweep finitely many planes/lines. They remain null even when tangency there has large dimension in line space. Unbounded/nonclosed originals have already been reduced by contact-local compact caps, so global separation, attained global support maxima, and closedness of the original common-line locus are never assumed.

## Independent source-scope counterexample

Let Kᵢ={(i,y,0):0<y<1} for i=0,1,2. Every horizontal line { (x,t,0):x∈R } with 0<t<1 intersects all Kᵢ and lies in their common support plane z=0. Therefore pₙ=(0,1/n,0) belongs to S for n≥2. If a line through p=(0,0,0) met K₀, it would contain p and some (0,y,0) with y>0, so would be exactly {(0,y,0):y∈R}. This line misses K₁. Thus p∉S and S is not closed. This analytically falsifies the broad historical closedness extrapolation while leaving nullness intact because this example's entire S lies in z=0.

The source's designation of Conjecture 4 as weaker than its 2-manifold question is recorded as source intent. This audit does not rely on unspecified regularity of the word manifold to infer nullness. In particular nothing here promotes the candidate to a proof of Conjecture 3.
