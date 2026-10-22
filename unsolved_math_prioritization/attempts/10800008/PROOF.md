# A global three-chart bound for approximate roots of the Vassiliev quadratic family

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance applies only to the stated partial theorem; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and symbolic checks described below occurred in the preceding investigation and audit on 11 October 2026. Editorial preparation authenticated retained bytes without a new scholarly-source inspection or mathematical-program rerun.

Edition status: the original candidate status immediately below is historical. The subsequent audit accepts 2 <= N(epsilon) <= 3 and tolerance independence on all six real coefficients; it does not determine whether the optimum is 2 or 3. The original candidate wording and all mathematical arguments are retained.

Status: authored candidate partial result, awaiting independent mathematical audit. The optimum is NOT determined. No claim of novelty or of a literature resolution is made.

## 1. Target and result

For arbitrary real affine functions

a(x,y)=a1 x+a2 y+a0,  b(x,y)=b1 x+b2 y+b0,

consider the actual real common roots of x²−y²+a(x,y)=0 and xy+b(x,y)=0. Let N(ε) be the least number of open subsets covering ALL of R⁶, each carrying a continuous R²-valued function whose Euclidean distance to at least one actual common root is strictly less than the fixed number ε>0.

The partial result established below is

                    2 ≤ N(ε) ≤ 3.

Moreover N(ε) is independent of ε>0. The remaining exact question is whether its value is 2 or 3. Singular parameters, unbounded coefficients, and the zero-parameter point are included. There is no residual-error surrogate and no restriction to a discriminant complement or compact box.

Source: V. A. Vassiliev, “A Few Problems on Monodromy and Discriminants,” Arnold Mathematical Journal 1 (2015), 201–209, Problem 2B and its antecedent on printed page 205. Public PDF: https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf . The historical formulation check authenticated the published PDF and inspected printed page 205; SOURCES.json records the public-source identity and inspection boundary. The proof below is independently authored.

## 2. Exact reduction from six parameters to four plus a translation

Put z=x+iy, A=a1+2i b1, B=a2+2i b2, and γ=a0+2i b0. Then

f+2ig = z²+α z+β conjugate(z)+γ,
α=(A−iB)/2, β=(A+iB)/2.

This is a real-linear bijection from the six original coefficients to (α,β,γ)∈C³. With z=u−α/2, the root equation becomes

Hβ(u)=w,   Hβ(u)=u²+β conjugate(u),
w=α²/4+β conjugate(α)/2−γ.

The change (α,β,γ)↔(α,β,w) is a homeomorphism on all C³. Translation by −α/2 preserves distances. Thus the covering number in question equals that for the harmonic-quadratic root problem (β,w)∈C²: one inequality follows by pulling a cover back and translating the selectors, and the other by restricting an original cover to α=0. We work on C² until the final pullback.

## 3. Properness, degree, and the central disk

Write b=|β|. Every root of Hβ(u)=w satisfies

|u|² ≤ b|u|+|w|, hence |u| ≤ b+sqrt(|w|).              (1)

For fixed β, Hβ is proper and has Brouwer degree 2: on a sufficiently large circle the homotopy u²+sβ conjugate(u)−w, 0≤s≤1, never vanishes, and u↦u² has winding number 2. In particular every fiber is nonempty. If β≠0, eliminating conjugate(u) gives the monic quartic

(u²−w)²+|β|²β u−β² conjugate(w)=0,

so every fiber is finite. For β=0 this is simply the complex square-root problem.

For β≠0 let Dβ={|u|<b/2}. The real Jacobian of Hβ is

Jβ(u)=4|u|²−b².

The map Hβ is injective even on the closed disk closure(Dβ). Indeed, equality of the images of u and v gives

(u−v)(u+v)+β conjugate(u−v)=0.

If u≠v this forces |u+v|=b. But when |u|,|v|≤b/2, equality in the triangle inequality forces both points to have radius b/2 and the same argument, hence u=v, a contradiction.

Set Ωβ=Hβ(Dβ). This is an open Jordan disk containing 0, its boundary is the image of the critical circle, and Hβ maps the closed disk homeomorphically onto closure(Ωβ). These assertions follow from the just-proved compact injectivity together with invariance of domain and the Jordan curve theorem. Set Ω0=empty. Define

Ω={(β,w): β≠0 and w∈Ωβ}.

It is open: at its unique disk root the Jacobian is strictly negative, so the implicit-function theorem supplies a root remaining in Dβ for all nearby parameters. The unique disk root σ(β,w) is continuous on Ω and satisfies |σ|<|β|/2.

## 4. Critical roots and their local degrees

All critical roots for β≠0 lie on |u|=b/2. The critical-circle injectivity shows that any parameter has at most one critical root.

Locally choose θ with β=b exp(3iθ), and substitute u=b exp(iθ)ζ, w=b² exp(2iθ)η. This reduces the map to H(ζ)=ζ²+conjugate(ζ), with orientation-preserving coordinate changes. A critical point is ζ0=exp(it)/2. Write the displacement as exp(−it/2)(x+iy) and rotate the target by exp(−it/2). The local expression is exactly

2x+k(x+iy)²,  k=exp(−3it/2)=A+iB.

Its real and imaginary parts are

F=2x+A(x²−y²)−2Bxy,
G=B(x²−y²)+2Axy.

Because Fx(0)=2, solving F=0 gives x=A y²/2+O(y³). If B≠0, the remaining scalar map is G=−B y²+O(y³), so its local degree, and hence the planar local degree, is 0. If B=0, A=±1 and G=y³+O(y⁴), so the local degree is +1. The first case is a fold and the second a cusp. The cusps are exactly exp(3it)=1.

A regular root in Dβ has local degree −1; a regular root outside closure(Dβ) has local degree +1. Additivity of Brouwer degree therefore gives:

- inside Ωβ: one negative root and three positive roots;
- outside closure(Ωβ): two regular positive roots;
- at a noncusp boundary point: one critical degree-zero root and two regular positive roots;
- at a cusp: one critical degree-one root and one regular positive root.

In the boundary cases there is no disk-interior root because the closed-disk map is injective. All other roots are regular; degree additivity gives exactly the stated count. For an additional direct check, at the normalized cusp w=3/4 the elimination polynomial is (u−1/2)³(u+3/2).

We use the elementary persistence consequence of nonzero local degree: if a root has nonzero local degree, any sufficiently small disk about it contains a root for all sufficiently nearby (β,w). This follows by preserving nonvanishing on the disk boundary and the Brouwer degree under parameter perturbation.

## 5. The exterior, including its caustic, has a two-sheeted root covering

Let

E={(β,w): w∉Ωβ} \ {(0,0)}.

On E, distinguish exactly two roots: at ordinary exterior or fold parameters take the two regular positive roots; at a cusp take the regular positive root and the degree-one critical root. For β=0,w≠0 take the two square roots. The resulting root relation is a two-sheeted covering over E with its relative topology.

Here are the details at singular parameters. At a fold the two distinguished simple roots extend by the implicit-function theorem. The critical root is a fold whose two local roots occur on the Ωβ side: one is the unique negative disk root and the other positive. It therefore contributes no distinguished exterior sheet. At a cusp, isolate the critical root and the other simple root in disjoint disks. The simple root extends continuously. At every nearby E parameter exactly one of its two distinguished roots remains in the critical disk; no root can escape the two isolating disks after the parameter neighborhood is reduced, by (1), compactness, and continuity. That unique distinguished root is continuous, again by the same compactness argument. Thus both sheets extend continuously at the cusp. Their distinctness at every E parameter is already established in Section 4. This proves the covering assertion, including changes in β and not merely a fixed-β slice.

For clarity about the topology of E, the normalized critical curve is

q(t)=exp(2it)/4+exp(−it)/2 = exp(−it)(2+exp(3it))/4.

It never meets 0, has radii between 1/4 and 3/4, and

d(arg q)/dt = 2(cos(3t)−1)/(5+4cos(3t)).

Its argument decreases strictly over every nontrivial interval and changes by −2π in one circuit. Consequently each ray from 0 meets the boundary exactly once. The central disk image is star shaped, with continuous radial boundary function rβ(v), v∈S¹. It satisfies

b²/4 ≤ rβ(v) ≤ 3b²/4  (β≠0),  r0(v)=0.

Continuity also at β=0 follows from the upper bound; continuity elsewhere follows from the strictly monotone argument parametrization, using any local choice of θ in the normalization.

Take I1=S¹\{−1} and I2=S¹\{+1}. Let Oj={(β,w):w≠0,w/|w|∈Ij}, and Ej=E∩Oj. Each Ej is closed in the metric space Oj, and the coordinate map

(β,v,t) ↦ (β, [rβ(v)+t]v)

is a homeomorphism from Ij×K onto Ej, where K=(C×[0,infinity))\{(0,0)}. The set K is contractible by the straight-line contraction to (0,1); Ij is an open interval. Hence Ej is contractible and locally path connected. The two-sheeted covering is therefore trivial over Ej. Choose one continuous exact root section sj:Ej→C for each j. The choice need not be canonical. The two sets Ej cover E.

## 6. A rigorous open approximate collar for each exterior chart

Apply the real-valued Tietze extension theorem to the real and imaginary parts of sj, since Ej is closed in the normal metric space Oj. Obtain a continuous Fj:Oj→C with Fj|Ej=sj. This uses the standard unbounded-valued version of Tietze; no compactness of Ej is assumed.

For every p0∈Ej the root sj(p0) has local degree +1. By persistence, all parameters p sufficiently near p0 possess a root within ε/3 of sj(p0). By continuity of Fj, shrink this neighborhood so |Fj(p)−sj(p0)|<ε/3. Thus Fj(p) has distance less than 2ε/3 from an actual root throughout that neighborhood.

Let Vj be the union, over p0∈Ej, of such open neighborhoods chosen inside Oj. Then Vj is open in C², contains Ej, and Fj|Vj is an ε-approximate root selector. This is a genuine global open-cover construction. Neighborhood sizes may vary with p0, as is allowed in an open cover; the approximation tolerance remains the SAME fixed ε everywhere. In particular the construction works at β=0,w≠0, at folds and cusps, and with arbitrarily large coefficients. No uniform collar width is asserted or needed.

## 7. One additional chart covers the entire interior and the origin

Write R(β,w)=|β|+sqrt(|w|). Choose a continuous cutoff χ:[0,infinity)→[0,1] equal to 0 on [0,ε/4] and to 1 on [ε/2,infinity). Put

U0=Ω ∪ {R<ε/4}.

On Ω set s0=χ(R)σ; on {R<ε/4} set s0=0. The definitions agree on the overlap and give a continuous function on the open set U0. Where χ=1 it is an exact root. Where χ≠1 on Ω,

|s0−σ| ≤ |σ| < |β|/2 ≤ R/2 < ε/4.

On the small set {R<ε/4}, (1) and nonemptiness of the fiber show that 0 is within ε/4 of an actual root. Hence s0 is an ε-approximate selector on U0.

Every parameter is in Ω, in E, or is (0,0). The three open sets U0,V1,V2 therefore cover all C². Pull them back through Section 2 and translate the selectors by −α/2. This proves N(ε)≤3 on the exact original all-R⁶ problem.

## 8. Independent approximate lower bound and tolerance invariance

Suppose a single global ε-approximate selector existed. Restrict to α=β=0 and w=L² exp(it), 0≤t≤2π, where L>ε. The two roots are ±L exp(it/2). Dividing the selector value by L exp(it/2) gives a continuous path lying in the disjoint open disks of radius ε/L about +1 and −1. Its component is constant. But periodicity of the parameter and selector makes its endpoint the negative of its starting point, in the other disk. Contradiction. Thus N(ε)≥2. This is an approximate-root argument on a large circle, independent of any exact-selection statement in the source.

Finally, (β,w)↦(λβ,λ²w) is a global parameter homeomorphism, and its roots are exactly λ times the original roots. Pulling selectors through this homeomorphism and dividing their values by λ turns tolerance ε1 into ε1/λ. Taking λ=ε1/ε2 and reversing the roles proves N(ε1)=N(ε2) for all positive tolerances.

## 9. Scope caution and the precise unresolved step

Under the literal all-R⁶ formulation, the exact-root problem 2A has no local exact section at zero parameters: restriction to the complex square-root subfamily on any sufficiently small circle about w=0 gives the same sign contradiction without a tolerance. Any open cover of all parameters would have a member containing zero and therefore an impossible local exact section. This elementary scope caution concerns the literal antecedent; it is not a claim about the author's intended modification and does not solve Problem 2B. In particular the source's exact-selection lower-bound remark is not imported as an approximate obstruction.

The established candidate partial bound leaves one discrete gap: a global two-chart approximate construction, or an obstruction to every such construction. Local cusp failures of exact selection cannot by themselves furnish that obstruction because arbitrarily small root clusters may be bridged within the permitted ε. Neither the three-chart construction nor the large-circle obstruction distinguishes 2 from 3.

The proof uses standard elementary results of topology (invariance of domain, Jordan separation, Brouwer degree, covering lifting over a simply connected space, and Tietze extension). The computational checks accompanying it check identities and provenance only; they are not a replacement for an independent audit of these topological arguments.

## Appendix: accepted expanded topology and singular-fiber details

The following Sections 4–8 of the subsequent accepted audit are reproduced verbatim. They make explicit the cusp mixed derivative, covering continuity on a whole neighborhood with varying beta, the phase-chart homeomorphism and contraction, the unbounded Tietze extension and nonzero-degree persistence, and the origin gluing. Section labels in this supplement refer to AUDIT.md. The full audit also supplies the reduction, Jordan-disk proof, lower bound, scaling, quantifier audit and standard dependencies.

## 4 Local critical degrees and all actual root counts

Locally in beta != 0 choose theta continuously so beta=b*exp(3i*theta). The orientation-preserving domain and target changes

    u=b*exp(i*theta)*zeta, w=b^2*exp(2i*theta)*eta

reduce to H(zeta)=zeta^2+conjugate(zeta). A critical point is zeta_0=exp(i*t)/2. For displacement delta=exp(-i*t/2)*(x+i*y), subtract H(zeta_0) and multiply the target by exp(-i*t/2). The resulting germ is

    2*x + k*(x+i*y)^2, k=exp(-3i*t/2)=A+i*B,

whose real and imaginary parts are

    F=2*x + A*(x^2-y^2) - 2*B*x*y,
    G=B*(x^2-y^2) + 2*A*x*y.

All these coordinate changes preserve orientation. Since F_x(0)=2>0, (x,y)->(F,y) is an orientation-preserving local diffeomorphism. The equation F=0 has a unique solution x=h(y) with h(y)=A*y^2/2+O(y^3). In these coordinates, the local planar degree is the one-dimensional local degree of g(y)=G(h(y),y).

If B != 0, then g(y)=-B*y^2+O(y^3), and its one-dimensional local degree at zero is 0. The nonzero second derivative is the fold condition. If B=0, then A=+1 or -1 and

    g(y)=2*A*h(y)*y=y^3+O(y^4).

The local degree is +1. In the coordinates (s,y)=(F,y), the mixed derivative of the second component with respect to s and y is A != 0 at the origin. Together with the nonzero cubic coefficient and the nondegenerate transversal coordinate F, this gives the cusp case. In fact the parameter-free degree calculation, rather than a catastrophe-classification theorem, is all the proof uses. B=0 is equivalent to exp(3i*t)=1, giving exactly three cusps of the critical circle.

At regular roots the sign of J is the local degree: -1 inside D_beta, +1 outside its closure. Additivity of degree over the finite fiber now establishes the counts without numerical sampling:

- If w is inside Omega_beta, it has exactly one negative root in D_beta, no critical root, and therefore exactly three positive roots.
- If w is outside closed Omega_beta, it has no negative or critical roots, and therefore exactly two positive roots.
- At a noncusp boundary target it has one degree-zero critical root and no negative root, and therefore exactly two positive regular roots.
- At a cusp target it has one degree-one critical root and no negative root, and therefore exactly one positive regular root.

The absence of a negative root on the boundary follows from closed-disk injectivity, not a generic-fiber limit argument. The local degrees are topological integers, not polynomial multiplicities. As an optional identity check, the eliminated polynomial at the normalized cusp target w=3/4 factors as (u-1/2)^3*(u+3/2); the triple algebraic root has local topological degree +1.

## 5 The selected exterior roots form a two-sheeted cover

Define

    E = (C^2 \ Omega) \ {(0,0)}.

For beta != 0 and an exterior or fold target, select the two regular positive roots. At a cusp select its degree-one critical root and its regular positive root. For beta=0,w != 0 select both square roots. Each parameter of E consequently has exactly two distinct selected roots, each of local degree +1. This is a specially selected relation, not the full root relation on the caustic: a fold's degree-zero root is deliberately omitted.

Here is a detailed proof that the relation S inside E x C, with its subspace topology, is a two-sheeted covering of E.

**At ordinary exterior points and beta=0,w != 0.** The two roots are simple. Their implicit-function branches over a sufficiently small parameter neighborhood are separated by disjoint root disks. At all nearby E parameters their positive Jacobians make them selected. Since each such fiber has exactly two selected roots, these are all the selected roots.

**At a fold.** The two selected roots at the central parameter are also simple and positive. The same implicit-function argument supplies two separated selected branches and exhausts all selected roots at every nearby E point. It cannot be obstructed by the additional unselected critical root. Thus no branch need cross or continue the fold root itself.

For completeness, the fold's disappearing pair lies on the Omega side. The two selected simple branches remain present on both sides. Nearby interior parameters have exactly four roots, including one negative disk root. As parameters tend to the fold, neither additional root can tend to the two fixed simple roots, by local uniqueness. Both therefore tend to the fold root. Nearby exterior parameters have only the two continuing positive roots. Equivalently, the one-variable reduced quadratic germ creates a pair of opposite degrees on precisely the side containing the negative root. This reasoning also permits beta to vary.

**At a cusp.** Let c be the critical root and r the other, simple root at p_0. Choose disjoint isolating disks around c and r. After shrinking a full parameter neighborhood, every root lies in their union. Indeed a contrary sequence of roots outside the union has a bounded subsequence, whose limit would be a root of p_0 outside the two disks. The branch near r is unique in its disk after a further shrink, by the implicit-function theorem and the same compactness argument, and remains selected and positive. Since an E fiber has exactly two selected roots, exactly one selected root remains in the disk around c.

The latter selected root is continuous at p_0: any sequence approaching p_0 has bounded chosen roots, and every limit in the critical disk must equal c. To verify continuity throughout a local neighborhood, use the ordinary/fold argument at its regular selected points and this cusp argument at any cusp selected points. More explicitly, selected roots cannot converge to an unselected fold root, because the two regular positive roots at that fold already persist and exhaust the selected roots nearby. At an ordinary point or beta=0 all roots are selected; at a cusp both actual roots are selected. Thus the selected relation is sequentially closed over E, and isolating disks identify continuous local branches at all its points. This closes the possible gap between continuity only at the central cusp and a genuine covering trivialization on a neighborhood.

The two graph pieces over each such neighborhood are relatively open in S, as they lie in separated open root disks. Projection restricts to a homeomorphism on each graph. These are the required covering neighborhoods. All neighborhoods above are full neighborhoods in parameter C^2 before intersection with E, and root bounds were uniform there. The assertion therefore includes varying beta and is not merely a fixed-beta slice argument.

## 6 Star-shaped caustics and the exact topology of exterior phase charts

The normalized critical curve is

    q(t)=exp(2i*t)/4+exp(-i*t)/2
        =exp(-i*t)*(2+exp(3i*t))/4.

It never vanishes and 1/4 <= |q(t)| <= 3/4. The factor 2+exp(3i*t) stays in the right half-plane, so a continuous argument lift of q changes by exactly -2*pi in a full period. Direct differentiation gives

    d(arg q)/dt = 2*(cos(3*t)-1)/(5+4*cos(3*t)).

The denominator is at least 1, and the derivative is nonpositive, vanishing only at the isolated cusp parameters. Its integral on every nontrivial interval is strictly negative. Hence the argument lift is strictly decreasing, even though its derivative vanishes at cusps. The induced argument map from the critical circle to the direction circle is a continuous bijection and therefore a homeomorphism. Each ray from zero meets the boundary exactly once.

Since 0 is in the Jordan interior, this unique boundary intersection implies that the interior on each ray is exactly the interval from radius 0 up to that intersection. This establishes star-shapedness rather than assuming it from the visual deltoid shape.

For beta != 0 write the boundary as w=r_beta(v)*v, v in S^1. The inverse direction map above makes r_beta continuous in v. With the local beta normalization from Section 4,

    r_beta(v)=b^2*r_1(exp(-2i*theta)*v).

This proves joint continuity locally in every beta != 0. Different cube-root choices of theta parametrize the same physical critical curve and hence the same uniquely defined radial value. Set r_0(v)=0. The bound

    b^2/4 <= r_beta(v) <= 3*b^2/4

proves joint continuity also as beta tends to zero, uniformly over v. Thus r is a single global continuous function on C x S^1, despite the lack of a global cube-root phase choice.

Let I_1=S^1\{-1}, I_2=S^1\{+1}, and

    O_j={(beta,w): w != 0 and w/|w| in I_j},
    E_j=E intersect O_j.

Each O_j is open in C^2. Since (0,0) is not in O_j,

    E_j=O_j \ Omega,

so E_j is closed relative to the metric space O_j. It need not be closed in C^2, and the proof neither claims nor needs that stronger statement.

All points of E have w != 0: for beta != 0 the target zero lies in Omega_beta, and beta=w=0 was explicitly removed. Consequently E_1 and E_2 cover E.

Define K=(C x [0,infinity))\{(0,0)}. The map

    (v,(beta,t)) -> (beta,(r_beta(v)+t)*v)

is a homeomorphism I_j x K -> E_j. Its inverse is

    (beta,w) -> (w/|w|,(beta,|w|-r_beta(w/|w|))).

Star-shapedness gives nonnegativity of t. When beta != 0, r_beta(v)>0, including at t=0. When beta=0, deleting (0,0) from K enforces t>0. These facts ensure w != 0 throughout, so all formulas are defined and continuous, including the beta=0 boundary behavior.

K is contractible by

    (beta,t) -> ((1-s)*beta,(1-s)*t+s), 0 <= s <= 1.

For s>0 its second coordinate is positive; at s=0 it is the original allowed point. Thus this contraction never hits the removed origin and ends at (0,1). Every point of K has a sufficiently small relative ball avoiding the removed origin; that ball is a convex Euclidean ball or half-ball. Hence K is locally path connected. Each I_j is homeomorphic to R, so E_j is contractible, path connected, and locally path connected.

A covering over a path-connected, locally path-connected, simply connected base is trivial, by the covering homotopy/path-lifting theorem. Contractibility supplies simple connectedness here. Applying this to S restricted to E_j yields a continuous exact section s_j:E_j->C. No compatibility between s_1 and s_2 on their overlap is needed for an open-cover selection problem.

## 7 Why unbounded Tietze extension supplies valid open collars

The following elementary lemma isolates the key approximate step.

Let B be a metric parameter space for a continuous family of maps R^2->R^2, O an open subset of B, and A closed relative to O. Suppose s:A->R^2 is continuous, selects an isolated actual root at every point, and every selected root has nonzero local Brouwer degree. For every fixed epsilon>0 there are an open neighborhood V of A inside O and a continuous epsilon-approximate root selector on V.

Proof: metric spaces are normal, and the unbounded real-valued Tietze extension theorem extends the two coordinate functions of s from A to all of O. Let F:O->R^2 be the resulting continuous extension. Given p_0 in A, choose an isolating root disk centered at s(p_0) with radius rho<epsilon/3. Its boundary has no zero. On this compact boundary the norm of the defining map has a positive minimum, and parameter continuity gives a neighborhood of p_0 on which the straight homotopy from the old map to the new one remains nonzero there. The local degree persists and is nonzero, so every nearby parameter has an actual root inside this disk. Shrink the neighborhood so |F(p)-s(p_0)|<epsilon/3. Then F(p) is at distance less than 2*epsilon/3 from such a root. The union of these open neighborhoods over p_0 in A is the desired V. The same F works on every neighborhood, so there is no patching inconsistency on overlaps.

For the present family, apply the lemma with B=C^2, A=E_j and O=O_j. All selected roots have degree +1, including the critical cusp roots. Thus the exact sections yield continuous F_j on open sets V_j containing E_j with the required strict epsilon bound.

The Tietze theorem used here permits unbounded continuous real-valued functions on a closed subset of a normal space. A bounded-only extension statement would not be enough unless supplemented by its standard unbounded extension corollary. There is no boundedness assumption on s_j, no compactness assumption on E_j, and no assertion of a uniform-width geometric collar. Each p_0 may have its own root-isolation radius and parameter-neighborhood width; the error allowance epsilon is the same fixed number everywhere. The sets V_j are open in C^2 because their constituent neighborhoods were chosen inside the open sets O_j.

This distinction is essential: a degree-zero fold root would not enjoy the same persistence statement. The selected exterior relation was designed to avoid exactly that issue.

## 8 The third chart and continuity across the added origin region

Let R(beta,w)=|beta|+sqrt(|w|). Fix a continuous cutoff chi:[0,infinity)->[0,1], with chi=0 on [0,epsilon/4] and chi=1 on [epsilon/2,infinity). Define the open set

    U_0=Omega union {R<epsilon/4}.

On Omega put s_0=chi(R)*sigma. On the open origin region {R<epsilon/4} put s_0=0. On their overlap the two definitions agree exactly, so the open-set gluing lemma proves continuity on all of U_0. No extension of sigma to an unselected boundary root is being asserted.

On Omega where chi=1 the selector is exact. Where chi != 1, necessarily R<epsilon/2, and

    |s_0-sigma| <= |sigma| < |beta|/2 <= R/2 < epsilon/4.

On the additional small region, every actual root has modulus at most R<epsilon/4 by Section 2, and a root exists by degree. Thus the zero value is also within epsilon/4 of an actual root there. All inequalities needed for the requested strictly-less-than-epsilon convention are strict with room to spare.

Every parameter lies in Omega, in E, or equals (0,0). The first and last types lie in U_0. The second lies in E_1 or E_2 and hence in V_1 or V_2. Thus U_0,V_1,V_2 are three open sets covering C^2, each with a valid continuous approximate selector. Section 1 pulls them back to all R^6 isometrically in the root coordinates.

End of accepted audit supplement.
