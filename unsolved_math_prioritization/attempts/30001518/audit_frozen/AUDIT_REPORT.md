# Independent audit: perfect billiard retroreflectors

Problem 30001518, OWR-4412-008, rank 976. Audit date: 7 October 2026.

## Decision

**Accept the five scoped partial approaches. Retain `unsolved`, `5/5`.** No proof of existence or nonexistence for the complete bounded, connected, piecewise-smooth specular-billiard class is established. No erroneous mathematical step requiring a correction patch was found in the frozen five turn documents. The additional precision below is part of the acceptance scope, not an extension to a solution.

This is a separate computational/mathematical audit of the identified author freeze, not human peer review or a priority certification. All sixteen author files were inspected; the proofs were reconstructed independently rather than inferred from the author's successful checks. No original author file or archive was modified. No remote write or publication was performed. No additional mathematical approach is charged for this audit.

## Frozen input and authenticity

The author manifest is externally anchored at SHA-256 `802e09153108d1ca826841748adfe751aec2fb2c1fe6718bca1083b0e56eb610`; the complete author archive is 26,403 bytes with SHA-256 `164e5736afdf41580386741079a6ee5b05ea5041b56036def48f379970f3042b`. Its sixteen `packet/` members agree byte-for-byte with the author directory. All declared file hashes, byte counts, and the checksum list agree. They were checked again after the adversarial tests.

The author's replay is an internal consistency check. A deliberately false extra proof sentence, accompanied by a coordinated manifest/checksum refresh, still passes that replay because the finite verifier does not mechanically check arbitrary prose. The audit's externally anchored checker rejects the modified packet. This expected limitation does not invalidate the genuine frozen proofs; it explains why an external freeze anchor and independent proof review are indispensable. No claim of digital signing or formal proof certification is made.

## Exact problem and source boundaries

The complete Plakhov contribution in the publisher's Oberwolfach report, printed pages 1855–1857, was read. The exact retroreflection passage on p. 1856 was freshly rendered and visually inspected. It uses informal all-ray language. Its mathematical normalization is supplied by Plakhov's *Mathematical retroreflectors*, arXiv:1005.3466v1, especially Definition 1 and Sections 2.1–2.4. The complete 32-page version was read, including its construction proofs and appendix; the definition and notched-angle regularity pages were freshly rendered and inspected.

The relevant bounded problem asks for a connected body with piecewise-smooth boundary and exterior specular billiards such that the final asymptotic unit velocity exists and equals minus the incoming velocity for almost every incident ray. The incidence measure is joint position-and-direction flux, not a measure on one selected beam direction. On a transverse boundary section it has density `(-v dot n)_+ dS dv`, restricted to rays actually interacting with the body. A positive-flux open failure set suffices to disprove perfection. Isolated normal rays, individual corners, and null grazing sets do not.

Boundedness is essential: the source supplies unbounded examples. The optical dimensions under discussion are at least two; in one dimension a compact interval trivially reverses the two incoming directions. The author's geometric exclusions and branch arguments are planar. No source-wide fixed collision count, convexity, simple connectivity, finite-polygon hypothesis, or everywhere-smooth boundary has been introduced.

At a regular collision the law is `w = v - 2(v dot n)n`. Singular collisions, grazing, and accumulation of infinitely many collisions cannot be assigned arbitrary outgoing values. The source excludes null pathological sets under its billiard hypotheses and states the bounded scattering velocity almost everywhere. The finite-itinerary lemmas in the packet instead make explicit local transversality and clearance assumptions. Neither those lemmas nor the finite checker prove a general trapping theorem for arbitrary nonsmooth sets. A positive-measure failure of the required asymptotic velocity would itself defeat perfection.

The source's infinite notched-angle construction is explicitly outside its piecewise-smooth hollow class because of accumulating singular vertices. Its truncations are genuine finite hollows. It is each such infinite construction, not merely a formal final parameter limit, whose boundary requires that warning. No blanket assertion about every possible convention for “piecewise smooth” is needed for acceptance.

Publisher metadata independently confirms report volume 7(3) (2010), pages 1827–1884, publication 2 March 2011, DOI [10.4171/OWR/2010/31](https://ems.press/journals/owr/articles/4412). This explains the 2010 workshop/problem year and the corpus's 2011 bibliographic date.

## Turn 1: resistance defect and exposed boundary

Let `mu` be a probability measure and let incoming/outgoing velocities be unit vectors defined almost everywhere. Expansion of the square gives

    1 - r = integral |v+w|^2 dmu / 4.

A nonnegative measurable integrand has zero integral precisely when it vanishes almost everywhere. If `Delta` is the angle between `w` and `-v`, its defect is `sin^2(Delta/2)`. Restricting the integral to `Delta >= delta` gives the stated angular-error bound for `0 < delta <= pi`. The factor 1/4 is necessary. No trajectory-existence result is hidden in this algebra.

For a compact connected planar body with nonempty incident phase space, projection onto a transverse line is an interval. The projection of its convex hull is the same interval. Hence an oriented line entering the hull meets the body, apart from boundary/singular exceptions treated in the regular incidence model. On the convex-hull boundary, integration of inward flux over angle gives total mass `2P`.

At a regular common hull/body boundary point, the tangent is supporting and both exterior half-rays of a nontangent one-reflection orbit lie outside the supporting half-plane. The outgoing direction escapes immediately. Its defect is `sin^2(phi)`, where `phi` is measured from the inward normal. The exposed contribution is therefore

    L0/(2P) * integral[-pi/2,pi/2] sin^2(phi) cos(phi) dphi
      = L0/(2P) * 2/3 = L0/(3P).

This proves the claimed lower bound and gives `r=2/3` for convex planar bodies. The audit uses the normalized flux calculation directly, rather than relying on potentially inconsistent unnormalized factors in intermediate source notation.

**Accepted scope:** exact equality criterion, tail bound, and the planar exposed-regular-length obstruction. **Gap:** the lower bound can vanish. Supremal resistance 1 neither implies an attained maximum nor supplies a regular limiting body. The rotating-vector counterexample correctly concerns this inference only, not a billiard realization.

## Turn 2A: a regular support point

The neighborhood clearance step is valid. In support coordinates the whole body lies below `y=0`, and near the support point the entire body is the subgraph of `g`, with `g(0)=g'(0)=0`. Choose a graph rectangle of width/height `rho` on which `|g'|<1/10`. Restrict the collision point `p=(x,g(x))` to `|x|<rho/4` and `-rho/8<g(x)<=0`.

For an upward vector `u` with `|u_x|<=u_y`, the horizontal displacement before reaching `y=0` is at most `-g(x)<rho/8`; the ray stays in the graph rectangle. Along it, vertical height above the graph increases at least at rate `u_y-(1/10)|u_x|>0`. Once above the support line, global disjointness follows. If `g(x)=0`, the crossing is immediate and the same conclusion holds.

Let `n` and `t` be orthonormal normal/tangent vectors at `p`. Taking reversed incoming direction proportional to `n+epsilon*t` gives outgoing direction proportional to `n-epsilon*t`. For a small nonzero interval of `epsilon`, both lie in the clear upward cone uniformly over a small arc of `p`. They differ because `epsilon != 0`. The flux density is bounded away from zero there, so this is a positive joint-flux family, not just a single normal ray.

A compact body with globally C1 embedded boundary has a regular support maximum. The same local argument excludes it, regardless of nonconvexity away from that point.

**Accepted scope:** the stated regular-support-point lemma and globally C1 planar-body corollary. **Gap:** an arbitrary source-admissible singular boundary has not been reduced to that local subgraph/support configuration.

## Turn 2B: finite simple polygons

At a genuine convex-hull vertex `q`, a finite simple polygon with nonempty interior agrees locally with a wedge `W` of positive angle at most the hull cone angle `beta<pi`. In angular coordinates write the hull cone as `[0,beta]` and the local wedge as `[a,b]`.

The edge outward normals have angles `a-pi/2` and `b+pi/2`. If `a<pi/2`, the first is strictly outside the hull cone. If `a>=pi/2`, then `b+pi/2>pi` and is also outside the cone. This includes the endpoint case `a=pi/2` by using the second normal.

Choose that edge direction `t` and a small closed cone `D` around its outward normal, wholly outside the hull cone and wholly in the outward half-plane of the edge. There is a uniform positive distance `eta` between the unit directions in `D` and the hull cone. Homogeneity and the distance inequality give

    distance(t + u*d, hull cone) >= u*eta - |t|.

Thus a uniform `K` exists with `t+u*d` outside the hull cone for every `u>=K` and `d in D`. For `p=q+delta*t`, take `delta` sufficiently small. The initial part `0<s<K*delta` of `p+s*d` is inside the disk where the body equals `W`, and is outside `W` by the outward half-plane condition. The remaining part is outside the global hull cone. The choice remains valid for an interval of `delta` and an open cone of directions.

Choosing the paired directions `n +/- epsilon*t` produces the same positive-flux, non-normal, one-bounce failure family as above. This establishes the finite-polygon statement, including nonconvex polygons; it is not restricted to edges lying along a whole hull face.

**Accepted scope:** finite simple planar polygonal bodies. **Gap:** the proof requires a finite local sector and does not by itself cover arbitrary curved singular endpoints, accumulating pieces, or the whole source class.

## Turn 3: regular two-reflection rigidity

Reflection in a planar tangent line with angle `theta` has a direction-linear reflection matrix. The product at two collisions is rotation by `2(theta2-theta1)`. A planar rotation takes a nonzero vector to its negative only when it equals `-Id`; hence the tangent lines are perpendicular at each regular retroreflecting trajectory.

The remaining independence step is justified. Put `u=(q2(t)-q1(s))/|q2(t)-q1(s)|`. At the second collision,

    partial_t arg(u) = det(u,q2'(t)) / |q2(t)-q1(s)| != 0

by transversality. Together with the first collision parameter `s`, this gives local coordinates on the incoming ray chart, after reflection in the first tangent. A sufficiently small product neighborhood of the endpoint parameters stays within the regular open itinerary chart. Perpendicularity on that product implies that fixing one endpoint forces the other tangent angle to be constant. Both arcs are locally straight and perpendicular.

An almost-everywhere reversal identity extends to every point of a regular chart by continuity and positive smooth flux density. A failure point would have an open, positive-flux neighborhood of failure. The converse for an actually realized itinerary in perpendicular lines is immediate from the product `-Id`.

**Accepted scope:** regular open planar two-bounce branches on the stipulated C2 arcs. **Gap:** positive measure alone is not an open chart; fixed-direction pencils are not two-dimensional ray families; higher collision counts and global branch assembly remain untouched.

## Turn 4: symplectic branch constraints

At a horizontal aperture, use physical tangential components `p` and `P` for incoming and outgoing velocity. Varying the finite reflected path length cancels all interior mirror terms by the reflection law and gives

    d ell = -p dx + P dX.

Taking the exterior derivative yields `dX wedge dP = dx wedge dp`, with the sign stated in the packet. Exact reversal is `P=-p`, so `X_x=-1` and `X=A(p)-x` on a subchart with connected horizontal slices. Substitution gives `d ell=-p A'(p)dp`, independent of `x`.

The full-strip consequence is conditional and correct: requiring `0<A(p)-x<L` for every `0<x<L` forces `A(p)=L` by the two endpoint limits. This makes length constant on a connected full strip. Those global hypotheses do not follow from a local chart.

The perpendicular-mirror example with intersection `(c,-h)` gives `A=2c-2hp/sqrt(1-p^2)` and `ell=2h/sqrt(1-p^2)`, and differentiation verifies the identity. Only trajectories which actually hit both mirrors and return through the opening belong to that branch.

For reversibility, the return map with the outgoing velocity reversed again has coordinates `(x,p) -> (A(p)-x,p)` and is an interval reflection/involution. It is important not to confuse this map with the physical scattering coordinates `(X,-p)`. Interval reflection branches are compatible with the required flux and time reversal. The sign argument therefore yields no nonexistence theorem.

**Accepted scope:** the C2 branch/C3 mirror hypotheses, local affine constraint, length identity, and explicitly conditional full-aperture conclusion. **Gap:** neither a contradiction nor a global billiard realization of every abstract branch system is supplied.

## Turn 5A: conditional finite-itinerary stability

At each limiting regular collision, the line/graph intersection is a simple root by transversality. Local C1 convergence of the corresponding complete boundary graph preserves a unique nearby intersection and its normal. Reflecting the incident vector therefore gives convergence of the next flight direction. Induction works over a fixed finite itinerary.

Here “boundary graph” must describe the body's boundary in the collision neighborhood, not an arbitrarily selected sheet in front of additional unaccounted-for pieces. Uniform strict clearance from other pieces away from those neighborhoods excludes earlier collisions and late exit collisions. A common bounded enclosing region handles the otherwise infinite incoming/outgoing half-rays. These are precisely the local-graph and clearance hypotheses on which acceptance rests; bare convergence of selected mirror points would not suffice.

For almost every ray on one specified fixed probability space, this yields pointwise convergence of scattering velocities. The resistance integrand is bounded between 0 and 1, so dominated convergence applies. A varying incident measure cannot be silently replaced by that fixed measure.

**Accepted scope:** the conditional finite-regular-itinerary result. **Gap:** the necessary compactness/clearance/normal convergence for a family with resistance approaching 1 has not been proved.

## Turn 5B: exact sawtooth counterexample

The bodies `Bn` are genuine connected finite simple polygons; their lowest notch level is `-1/(2n)`, above the bottom `-1`. They are contained in the rectangle `B` and every missing point of `B` is within vertical distance `1/(2n)` of `Bn`. Thus the stated Hausdorff bound is correct.

Scale a cell to width 1, with entry `(r,0)` and velocity `(a,-1)`, `0<a<1`. The left side has equation `y=-x`; the right side is `y=x-1`.

- If `r<(1-a)/2`, the first point has `x=r/(1-a)`, and reflection gives `(1,-a)`. The second point on the right side has `x=(1-r)/(1+a)`. The second reflection gives `(-a,1)`, and the aperture exit is `1-a-r`.
- If `r>(1-a)/2`, the first point has `x=(r+a)/(1+a)`, and reflection gives `(-1,a)`. Extrapolation to the aperture has coordinate `(r+a-1)/a`. This is positive exactly when `r>1-a`, yielding a one-bounce trajectory. If instead `r<1-a`, the second hit is on the left side with `x=(1-a-r)/(1-a)`; the final vector is `(-a,1)` and the exit is again `1-a-r`.

The equality `r=(1-a)/2` hits the apex, and `r=1-a` reaches a cell endpoint on exit. These singular cases are not assigned ordinary reflection data. All other exits lie strictly within the same cell and point upward. Since the entire body lies below `y=0`, there is no later collision with any neighboring cell or side/bottom edge. The exact two-bounce fraction at fixed `a` is `1-a`.

The flat limiting body returns `(a,1)`. After unit-speed normalization the horizontal difference from either sawtooth output is at least

    2a/sqrt(1+a^2) >= 2a0/sqrt(1+a1^2) > 0

on every closed band `0<a0<=a<=a1<1`. The incoming flux in these coordinates has density `dx da/(1+a^2)^(3/2)`, strictly positive on the band. For each `n`, the exceptional entry sets are finitely many curves in the joint `(x,a)` strip; Fubini gives zero two-dimensional flux measure. Their union over the countably many `n` is still null.

Thus the difference is uniformly bounded below on a full-measure subset of a fixed positive-flux strip for every `n`. This is a genuine failure of convergence in measure, not merely failure for a single illumination direction. The family is not asymptotically perfect. It refutes the proposed Hausdorff-continuity step only; its nonconverging normals also explain why it does not contradict the conditional C1 stability lemma.

## Credited constructions and later literature

The complete 18-page arXiv:0911.1984v1 *Perfect Retroreflectors and Billiard Dynamics* was read. Its semi-infinite tube is a parameterized construction. Theorem 1 gives finite exit almost everywhere for each positive parameter; Theorem 2 gives exact reversal with arbitrarily small displacement with probability tending to one as the parameter vanishes. The almost-everywhere finite-exit statement is not an assertion that reversal already has probability one for one fixed tube. In Plakhov's treatment, further truncation/thickening and diagonal choices yield bounded asymptotic families, not a single bounded perfect body. Publisher metadata is [JMD 5 (2011), 33–48](https://www.aimsciences.org/article/doi/10.3934/jmd.2011.5.33). No byte identity with a revised journal edition is claimed.

The complete Almeida–Neves–Plakhov paper was read, including its construction and resistance arguments, and its formal Theorems 1–2 on printed p. 14 were freshly rendered. The precise theorem uses infinitesimal angular error outside an infinitesimal-measure exceptional set. The hyperfinite exceptional boundary parameters mentioned in its abstract must not be confused with a finite ordinary piecewise-smooth boundary or with exact standard probability-one reversal. Taking a standard part of the geometry would need an additional scattering-continuity argument, which is exactly the kind of inference Turn 5 invalidates in general. Source: [official 2009 article PDF](https://mag.ilt.kharkov.ua/index.php/jmag/article/download/jm05-0012e/574/585).

Plakhov's mushroom result is weak convergence of scattering measures and allows small nonzero angular errors; the tube and notched-angle families have stronger exact-direction probabilities tending to one. The helmet's high resistance is a numerical near-perfect result. These distinct senses of approximation are kept separate.

The [2012 book chapter](https://link.springer.com/chapter/10.1007/978-1-4614-4481-7_9) was checked at publisher abstract/metadata level only; its complete text was not available in this audit. The 2013 CMUP seminar abstract is historical supporting context, not proof of current open status. The 2015 Cruz–Plakhov chapter DOI `10.1007/978-3-319-20352-2_2` remained unavailable in full text; the [official 2016 conference abstract](https://comum.rcaap.pt/bitstream/10400.26/22335/1/Livro_Resumos_ENSPM2016.pdf) identifies its efficiency comparison as concerning asymptotic devices with imperfect reflection. No uninspected theorem from that chapter is used.

A separate possible confusion was checked against the primary [2016 periscope-theorem abstract](https://arxiv.org/abs/1602.07961): realizations of maps between selected parallel or normal ray families are not realizations of one bounded retroreflector for the full incident phase space. Later invisibility statements concern a different target map, and wave/metasurface devices use a different model.

Fresh bounded searches for perfect bounded specular/billiard retroreflectors and nonexistence did not identify an inspected later resolution. The complete supplied PDFs of the 2021 and 2026 open-problem collections were independently NFKC-normalized and text-scanned for `retro`, with zero matches. This is a limited negative search, not a full thematic review or evidence proving present worldwide openness. The disposition is **unsolved by this packet**.

## Computational evidence and its limits

The untouched author replay succeeds with all seven source PDFs and both complete corpus files supplied. Its 9,280 controls and recorded deliberate failures reproduce. The source/corpus hashes, unique target problem match, and absence of the joined research-result key were checked independently. Only public hashes, byte counts, titles, URLs, and match booleans are included here; no corpus contents or source copies are included.

The new verifier contains no Python `assert` statements. Its explicit checks execute under ordinary Python, genuine `-O`, and genuine `-OO`, with observed optimization flags 0, 1, and 2 and identical mathematical results:

- 77,613 independent exact checks per mode
- 9,450 nonsingular sawtooth trajectories: 5,292 two-bounce and 4,158 one-bounce cases
- 756 independently detected predicted singular cases
- Near-threshold and near-endpoint rational incidence, including `a=1/997` and `a=996/997`
- Separate `a=0` and `a=1` endpoint controls, apex and grazing rejection, and a finite reflection cap that is never reported as escape
- Eighteen hull-vertex polygon escape-cone controls, curved support-graph cone controls, and rotated/scaled/translated itinerary controls

Four mathematical fault variants are rejected in all three optimization modes. The author's own `verify.py` and `replay.py` explicitly reject both `-O` and `-OO`. Frozen-input corruption, missing/extra files, symlinks, malformed inventory changes, coordinated rehashing, archive truncation, source truncation, and a relocated author replay are separately exercised. Exact recorded results are in `audit_results.json`.

These are finite exact rational controls, not floating-point optimization or a mechanized proof of the analytic statements. They do not settle measure-zero claims, compactness, arbitrary collision counts, arbitrary singular boundary classes, or the complete existence question. Those analytical steps were checked in the reconstructions above.

## Remaining gaps and stopping point

1. No reduction of every admissible boundary to a regular support point or finite polygonal sector.
2. No exclusion or construction of all higher-bounce branches and their global compatibility.
3. No stable compactness class containing a known asymptotically perfect family.
4. No exact standard bounded perfect body extracted from a nonstandard or asymptotic construction.
5. No exhaustive later-literature or historical-priority certification.

The five approaches are genuinely mathematical and distinct as written. The audit verifies those delivered approaches, not undocumented historical timestamps. The accepted conclusion is unchanged: **scoped partial progress; full problem unresolved.**
