# Segment mirrors: scoped escape results and the remaining obstruction

Problem 5500031 / AMR-054-0031. Status: **unsolved, 5/5 approaches**.
This is an authored partial-results note, not a solution, novelty claim, or claim of human peer review.

## 1. Target and conventions

The target is TOPP Problem 31: decide whether some finite planar arrangement of two-sided straight mirrors can keep every direction from one point source inside the mirrors' convex hull. The segments are open but their closures must be pairwise disjoint. A ray that reaches an omitted endpoint is not reflected there. The source is outside the mirrors; the source-list wording does not separately exclude an endpoint source. We do not silently replace “every direction” by “almost every direction.”

For the elementary results below, unless an extension is explicitly stated, the source is outside all closed mirrors and a **regular** trajectory never meets an endpoint or travels along a supporting line at a contact. Reflection at an interior point is specular. Speed is one. This restriction is useful for a clean dynamical statement, and the exceptional directions are countable (Section 3). Thus a regular escape already suffices to refute all-direction trapping for the given configuration. Endpoint-source cases remain part of the general target and are not claimed resolved by our regular-source reductions.

Let the mirrors be M_1,...,M_n, let C be their closed convex hull, let L be the largest mirror length, and, for n >= 2, let delta be the minimum distance between two distinct closed mirrors. Then delta > 0. Consecutive effective reflections cannot occur on the same straight segment. Thus the kth collision time is at least (k-1)delta, and no infinite number of reflections can accumulate in finite time. A regular trajectory is trapped exactly when it reflects infinitely often, provided its source lies in C: finitely many reflections leave a final unbounded straight ray, whereas every leg between successive collision points belongs to the convex set C. Sources outside C are already outside the proposed trap.

## 2. Approach 1: angular shadows and an exact obstruction

For a source s outside a closed segment, its set of directly blocked directions is a closed arc of angular length strictly less than pi (or a singleton when s lies on the supporting line). To see this, strictly separate the point s from the compact convex segment. All its direction vectors lie in an open semicircle, with a uniform margin by compactness. Therefore at most two mirrors always leave a nonempty open set of directions with no collision. More generally, if the sum of the shadows' angular lengths is below 2pi, direct escape exists. This is only a sufficient criterion.

**No-direct-escape example.** Take source (0,0), vertical mirrors at x=+1 and x=-1 with -2<y<2, and horizontal mirrors at y=+3/2 and y=-3/2 with -9/10<x<9/10. Their closures are pairwise disjoint. Every initial direction hits a mirror: if the absolute slope is below 2 it intersects a vertical mirror's interior unless it meets a horizontal mirror first; at slope at least 2, including vertical directions, it crosses a horizontal mirror at absolute x at most 3/4. The slope-2 endpoint of the vertical mirror is therefore harmless to this argument.

Nevertheless there is an open interval of **two-reflection escaping directions**. For initial direction (1,m) with

15/31 < m < 15/29,

the two hits are (1,m) and (-1,3m). The outgoing direction is again (1,m). The ray crosses the top supporting line on the second leg if m>1/2 and on the final leg if m<1/2. Those crossing x-coordinates are respectively 2-3/(2m) and 3/(2m)-4, and both are less than -9/10 in the indicated cases. At m=1/2 the crossing is at (-1,3/2), still outside the horizontal mirror. The next crossing of x=1 would have y=5m>2, so no further mirror is met. All bottom mirrors are avoided because y is positive and increasing. These inequalities also prove regularity and openness of this family. For direction (2,1), the exact hit points are (1,1/2), (-1,3/2).

Horizontal and vertical normal rays in the same configuration are periodic. Thus neither a gap between closed segments nor a blocked initial angular circle decides the full problem.

## 3. Approach 2: unfolding and infinite itinerary control

The following elementary arguments are reconstructions of standard unfolding facts already used by O'Rourke-Petrovici and Milovich. They are not new countability results.

**Lemma 3.1 (finite endpoint and periodic coding).** For a fixed source outside the closed mirrors, directions whose trajectories reach an endpoint are countable. Regular periodic directions are also countable.

**Proof.** Fix the finite reflection word preceding a positive-time endpoint contact, and unfold these reflections. Each reflection is an affine isometry, so the terminal endpoint has one determined unfolded image e'. An unfolded ray starts at s and reaches e' after positive length. If e'=s this is impossible; otherwise its direction is uniquely (e'-s)/|e'-s|. There are finitely many endpoints and countably many finite words. A grazing contact reached from outside a segment must first reach an endpoint, so it introduces no uncountable exception.

For a periodic ray, reversibility implies that its initial state belongs to the periodic orbit even if periodicity was first detected later. Choose the finite word describing one full return to the same position and direction. The unfolded image F(s) of the return point satisfies F(s)-s=T v, where T>0 is the period length and v is the initial unit direction. This fixes v for the word, unless F(s)=s, in which case no positive-length straight unfolded return exists. Countability follows. Repeated mirror labels are allowed; the proof uses all finite words, not permutations. QED.

**Lemma 3.2 (quantitative finite-prefix shrinking).** If two regular rays from the same source share the first k>=2 mirror labels, then their initial unit directions v,w satisfy

|v-w| <= L / ((k-1)delta).

In particular, two infinite trapped rays with the same entire itinerary have the same initial direction.

**Proof.** After unfolding the common prefix, the kth collision points s+t v and s+r w lie on the same unfolded kth mirror, hence their distance is at most L. Both t and r are at least (k-1)delta. The identity

|t v-r w|^2 = (t-r)^2 + t r |v-w|^2

gives the inequality, and k tending to infinity gives uniqueness. QED.

**Exact remaining gap.** Countably many finite words do not imply countably many infinite words. There can be uncountably many infinite itineraries, even though every itinerary determines at most one direction and its finite-prefix direction sets shrink to diameter zero. Binary coding of an interval has precisely this phenomenon. The number of available length-k words can grow exponentially; the O(1/k) per-word diameter bound gives no vanishing union measure. A full all-trapping configuration, if one exists, would require uncountably many aperiodically trapped regular directions. No argument here rules that out. The published aperiodic examples also rule out the shortcut “all infinite rays are periodic.”

## 4. Approach 3: conserved observables

### 4.1 Concurrent supporting lines

**Theorem 4.1.** Suppose every supporting line passes through a common point c. Every regular ray escapes; no rational-angle hypothesis is needed. More precisely, at all times t,

|q(t)-c|^2 = |s-c|^2 + 2(s-c).v_0 t + t^2.

**Proof.** Between reflections the derivative of (q-c).v is |v|^2=1. At a reflection, write q-c=lambda u along that mirror's supporting direction. Reflection preserves the u-component of velocity, so (q-c).v has no jump. Collision times do not accumulate. Integrating gives (q(t)-c).v(t)=(s-c).v_0+t. The derivative of |q-c|^2 is twice this quantity; integrate again. The right-hand side tends to infinity, so the ray leaves every bounded set, in particular C. QED.

If C and s lie in the closed disk of radius R about c, set a=(s-c).v_0 and

T=-a+sqrt(a^2+R^2-|s-c|^2).

Then the ray lies outside that disk for every t>T. The number N of effective reflections satisfies (N-1)delta<=T when N>=1. This is a geometric bound, not a finite simulation inference. With transparent endpoints and the additional explicit convention that collinear grazing continues straight, the same identity extends across those events as well: neither changes velocity. Under that extension every ray from a source off the open mirrors escapes. This extension is not asserted for an endpoint-absorbing model.

### 4.2 Parallel supporting lines

**Theorem 4.2.** If all mirrors are parallel to a common unit vector e, every regular direction v_0 with e.v_0 nonzero escapes. At most the two normal directions can be trapped.

**Proof.** Reflection preserves e.v, so e.q(t)=e.s+t(e.v_0). A nonzero slope is unbounded. In the normal case, restrict to the line through s perpendicular to e. Its intersections with open mirrors form a finite ordered set. If two adjacent intersections bracket s, the normal rays bounce periodically between them; otherwise the ray escapes after at most one reflection. Endpoint intersections are omitted in the transparent model. QED.

These special classes do not exhaust arbitrary configurations. In particular, “all supporting lines have rational coordinates” is not the rational-angle hypothesis of Milovich's theorem.

## 5. Approach 4: rational approximation and finite-path stability

Milovich's Corollary 4-20, in his rational-angle setting, supplies countably many nonescaping directions at most. His convention absorbs endpoint hits. Every escaping ray in that stronger absorbing model is endpoint-free, so it is also an escaping ray in the present transparent-endpoint model. We rely on this published theorem; we do not present its long proof as newly derived here.

For a fixed source off the closed mirrors, let R_n be the configurations admitting at least one regular escaping ray. This subset of legal configurations is open. Indeed an escaping ray has finitely many transverse interior collisions. Continue it to a point outside a large closed disk containing all mirrors, with outward velocity. On this compact finite path, each collision has strict interior and transversality margins, and every nonincident mirror is avoided with a positive margin. Small simultaneous perturbations preserve the word, the exit point outside the disk, and the outward final direction. Source clearance is also an open condition.

Rational-angle configurations are dense: perturb the finitely many mirror directions to rational multiples of pi, keeping one common reference direction. Segment endpoints move continuously, so sufficiently small changes preserve disjoint closures and source clearance. Milovich's theorem puts those approximants inside R_n. Hence R_n is an open dense subset. The complement is closed nowhere dense, and any all-trapping configuration would lie in that complement. This observation is already part of Milovich's argument, particularly Corollary 3-8 and the opening of Section 4.

**Gap.** An open dense set need not be the whole space, nor must its complement have measure zero. Escape words, flight times, and endpoint clearances may lose their bounds in the rational approximation limit. No uniform bound is proved here. A finite collection of successful rational examples cannot close that gap.

## 6. Approach 5: a precise limitation of global quadratic escape functions

**Theorem 6.1.** Let V(q)=q^T A q+2b^T q+d with real symmetric positive-definite A. Suppose at every interior point of every two-sided mirror, for every incident velocity from either side, specular reflection never decreases the directional derivative dV/dt. Then all mirror supporting lines pass through the common point c=-A^{-1}b. Conversely concurrent supporting lines admit such a quadratic, namely V(q)=|q-c|^2.

**Proof.** For a unit normal n at a mirror point q, reflection sends v to v-2(n.v)n. The directional-derivative jump is

-2(n.v)(gradient V(q).n).

Both signs of n.v are legitimate incident velocities for a two-sided mirror. Nonnegativity for both signs forces gradient V(q).n=0. Write q=a+t u on an open mirror, where u is a tangent. Since gradient V(q)=2(Aq+b), the identity for all t in an interval gives n^T A u=0 and n^T(Aa+b)=0. In the plane, symmetry of A implies n is an eigenvector: A n=mu n, with mu>0. Substituting b=-Ac gives 0=n^T A(a-c)=mu n.(a-c). Thus a-c is tangent to the supporting line, so that line contains c. This works for every mirror. Conversely the centered squared norm has zero derivative jump at every concurrent mirror, as in Theorem 4.1. QED.

For example, three disjoint mirror pieces supported respectively on x=0, y=0, x+y=1 have no such positive-definite quadratic certificate. One possible selection is {(0,y):2<y<3}, {(x,0):2<x<3}, and {(x,1-x):2<x<3}; their closures are disjoint. Algebraically the first two lines force A_12=b_1=b_2=0; the third then forces A_11=A_22=0. This excludes positive definiteness.

This theorem only limits a global, velocity-independent quadratic with the stated all-incidences monotonicity condition. It does not exclude nonquadratic functions, state-dependent functions, restricted reachable-state conditions, or a different escape argument.

## 7. Disposition and computational role

The unrestricted target remains **unsolved**. Five genuinely different routes were considered: direct shadows; unfolding/coding; conserved observables; rational approximation; and quadratic Lyapunov classification. None proves that every legal nonconcurrent irrational-angle arrangement admits an escaping ray, and no all-direction trap was constructed.

The verifier uses exact rational arithmetic. It checks reflection identities, finite-prefix algebra, 280 concurrent-ray examples (up to 14 reflections), parallel drift, transparent endpoint handling, a universal-claim obstruction example, and the two-reflection certificate. It reports a cutoff as unresolved, never as trapped. Its finite counts validate implementations and examples; the universal scoped claims are justified by the written proofs above. No floating-point search, simulation density, or finite horizon is being promoted to a theorem about all directions.
