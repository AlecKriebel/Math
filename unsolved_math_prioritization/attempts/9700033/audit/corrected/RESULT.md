# SIRSN major-road components: a finite exterior-covering family

Problem 9700033 / AMR-096-0033, rank 935. Author disposition: **UNSOLVED; scoped partial result; 3 of at most 5 approaches used.** Corrected derivative after independent AI audit, 2026-10-06; the frozen original is preserved separately. This is AI-assisted, unrefereed work. Neither a general uniqueness theorem, a SIRSN counterexample, nor historical novelty is claimed.

## 1. Target and hypotheses

The target is uniqueness of the unbounded connected component of E(infinity,1). It is Open Problem 33 in Aldous's long 2012 preprint, and Open Problem 7 in the published 2014 paper, section 8.4.2 [A]. It is not the maximal-route-length problem numbered 9700034.

Write E_r = E(infinity,r). In Aldous's notation [A, equations (2.17)-(2.20)], E(lambda,r) is the union of the routes between points of an independent intensity-lambda planar Poisson sample, with the closed radius-r discs around each route's two endpoints removed. Increasing lambda gives E_r. The r parameter is Euclidean endpoint exclusion, not a speed threshold.

The full planar SIRSN assumptions are: compatible non-self-intersecting feasible routes; consistent measurable finite-dimensional distributions; translation, rotation, and spatial scaling invariance; finite mean length of a unit-displacement route; and finite major-road intensity p(1). The finite-intensity sampled network condition follows. Ergodicity, finite energy, insertion tolerance of roads, a cost metric, and coalescence of all infinite geodesics are not additional assumptions in the result below.

We use these source inputs explicitly: intensity(E_r)=p(1)/r; E_r has the intrinsic sampling-independent version of Proposition 6.3; and equation (6.4) allows a single deterministic root at 0 to be planted without enlarging E_r, almost surely. Only countably sampled routes from that root will be used. No assertion about simultaneously adjoining every deterministic pair of points is needed.

## 2. Partial theorem with a measurable witness bound

**Theorem.** Fix r>0. Almost surely there is a measurable finite integer H_r>=1 and a finite measurable random radius M_r with the following property: at most H_r distinct unbounded connected components of E_r together have infimum distance at most 2r from every x with |x|>M_r. Each of these components meets circle(0,2r), and

H_r <= N_r := #(E_r intersect circle(0,2r)),    E[H_r] <= 8p(1).

More explicitly, H_r counts measurably constructed, unbounded path-connected witness sets contained in E_r; different witnesses may be in the same connected component. No measurability of the exact number of topological components is asserted or used. The components need not be all unbounded components, and H_r need not equal one. No nearest-point attainment or closure of E_r is required. This is a probability-one assertion for each fixed r. A countable intersection gives it for all positive rational r, without claiming a common event for all real r.

**Proof.** The stationary isotropic edge-process intersection identity [A, section 2.1], applied along a circle, gives

E[N_r] = (2/pi) (p(1)/r) (4 pi r) = 8p(1).

This curved-boundary application is also the one used in [A, Proposition 6.1]; it follows by integrating the local directional intersection intensity along the circle. The edge-length directional measure is translation invariant and uniform in direction. Segment endpoints, tangencies, and multiple-direction vertices do not contribute additional intersections on a fixed circle almost surely; this follows from stationarity and the countable segment representation. Overlapping segments are counted as a union. Thus N_r is a finite measurable point count almost surely. No assertion that finite local length alone bounds crossings is used.

Couple the endpoint samples by the space-time Poisson process used in [A]. Their union Xi_infinity is countable, dense, and unbounded almost surely. One measurable enumeration is obtained by taking the successive shells of the boxes [-m,m]^2 times [0,m], m=1,2,..., and ordering the finitely many atoms in each shell lexicographically by arrival time and then spatial coordinates. Zero-probability ties can be broken by a fixed rule. There is no first-arrival ordering of the entire infinite plane. Retain only endpoints xi_n with |xi_n|>4r, preserving their order.

Plant the single deterministic root 0. Work on the probability-one event on which equation (6.4) identifies the planted-root E_r with E_r, all the countably many sampled root routes are feasible and compatible, Xi_infinity is dense, and N_r is finite. This uses one deterministic root and a countable family of random endpoints, not an uncountable intersection over deterministic route pairs.

Parameterize each route R(0,xi_n) continuously on [0,1], for example by normalized arclength, as gamma_n. Let t_1,n be its first encounter with the closed disc of radius 2r about xi_n, and let t_0,n be its last encounter with the closed disc of radius 2r about 0 before t_1,n. Both times exist. The discs are disjoint, so t_0,n<t_1,n; continuity gives boundary contact at each time. Set

A_n = gamma_n([t_0,n,t_1,n]),    q_n = gamma_n(t_0,n).

The compact subpath A_n stays at distance at least 2r>r from both route endpoints, so A_n is contained in E_r by (6.4). It contains q_n in circle(0,2r) and has a point at distance 2r from xi_n. First/last contact times with these closed discs, the evaluation q_n, and the maximum norm a_n=max{|z|: z in A_n} are measurable functions of the countably many continuous routes. For clarity, first contact is determined by minima of the continuous distance function over compact time intervals; last contact is first contact for the time-reversed restricted path. Evaluation and compact-interval maxima are measurable for the usual continuous-path Borel structure.

Group the indices n according to equality of q_n, choosing the first occurring index of each group as its representative. There are finitely many groups because their distinct q-values belong to the N_r-point set. Equality of points and the first-occurrence rule are measurable. For a representative j set

G_j = union{A_n: q_n=q_j},    b_j = sup{a_n: q_n=q_j}.

Each G_j is path-connected: all its constituent subpaths contain q_j. Its radius b_j is a measurable extended nonnegative random variable, being a countable supremum with measurable equality tests. The group is unbounded exactly when b_j=infinity, equivalently when for every integer L some n in that group has a_n>L. Define H_r as the number of first-occurrence representatives with b_j=infinity. This is a measurable integer and H_r<=N_r.

There are finitely many bounded groups. Set B_r=0 if there are none; otherwise let B_r be the maximum of their finite radii b_j. This is a finite measurable random variable. If |xi_n|>B_r+2r, A_n cannot belong to a bounded group, since its endpoint at distance 2r from xi_n has norm at least |xi_n|-2r>B_r. Since Xi_infinity is unbounded, at least one group is unbounded, so H_r>=1.

Let G be the union of the unbounded G_j and take M_r=max(4r,B_r+2r). For every sampled endpoint with |xi_n|>M_r, dist(xi_n,G)<=2r. For any x with |x|>M_r, density supplies sampled endpoints tending to x while staying outside that disc. Distance to any nonempty set is 1-Lipschitz, so dist(x,G)<=2r.

Each unbounded connected set G_j is contained in a unique connected component of E_r. Those components are unbounded and meet circle(0,2r). Discard repeated components purely as a pathwise set operation; their number is at most H_r. This final step asserts existence of a covering family and does not take the expectation of its exact cardinality or require a measurable enumeration of the components. Since H_r<=N_r, E[H_r]<=8p(1). QED.

This is a finite exterior-covering result. It neither captures every unbounded component nor merges the covering components. The change from the author's expected exact component count to a measurable witness bound removes an unstated component-measurability step while retaining a quantitative expected upper bound on the size of an available cover.

## 3. Why spatial symmetries and mean length alone cannot prove uniqueness

Here is an explicit auxiliary random edge process. It is **not a SIRSN**, and is not a counterexample to the target.

Choose a uniform direction theta modulo pi. Independently take a Poisson process of marked offsets (t,s) in R x (0,infinity), with intensity dt ds/s^2. If n_theta is the normal vector, associate the entire line {x: x dot n_theta=t} to (t,s). For each r>0 let F_r contain exactly the lines with s>=r.

The following claims have direct proofs:

- Stationarity: a translation shifts t by a constant, preserving dt ds/s^2. Uniform theta supplies rotation invariance.
- Nesting: F_b is contained in F_a whenever b>=a.
- Scaling covariance: (t,s) maps to (ct,cs) under spatial scaling by c. The measure dt ds/s^2 is unchanged. Thus c F_r has the distribution of F_(cr), jointly in r.
- Mean length density: projecting the marks s>=r gives a Poisson process of offsets of rate integral_r^infinity ds/s^2=1/r. Fubini's theorem gives expected line length in any bounded Borel set A equal to area(A)/r. There are finitely many relevant offsets in any bounded transverse interval, so local total length is finite.
- Components: at a fixed r the offset process is locally finite and has infinitely many atoms almost surely. Its individual parallel lines are precisely the connected components of F_r. Each is unbounded.

The circle calculation is sharp for this auxiliary example: the number of components meeting a radius-R disc has mean 2R/r, and the number of boundary intersections has mean 4R/r. Increasing R does not give a contradiction. The randomized-direction law is not translation-ergodic: its global direction is translation-invariant. With the direction fixed, the marked Poisson process is ergodic under transverse translations, so stationarity plus ergodicity plus finite length also fail by themselves to force uniqueness. The latter fixed-direction variant is not isotropic.

The family F_r fails the all-pairs-route consequence in section 2: no finite collection of parallel lines can remain within 2r of every point outside a bounded disc. Moreover its union over all r still has countably many parallel lines and contains no path connecting points with different normal coordinates: the continuous normal projection of any connected path would be an interval contained in a countable set, hence a singleton. No compatible complete routing is being asserted. Thus the construction isolates the information lost by a symmetry-and-intensity-only proof; it does not dispose of the SIRSN problem.

## 4. Three approaches and the exact remaining gap

1. **Mass transport / local modification.** The nested marked-line construction above refutes an argument using only stationarity, isotropy, scaling, and the 1/r length intensity. A Burton-Keane-style argument would additionally have to justify a permissible modification and its positive probability within the law of the route system. The external Poisson sample consists of endpoint probes, not independently resampled road edges. Indeed Proposition 6.3 says additional endpoint sampling leaves E_r unchanged. No finite-energy premise has been established.

2. **All-pairs routing and finite crossings.** This gives the finite exterior-covering theorem. The missing implication is from finitely many unbounded components collectively within 2r of all remote points to one unbounded component. It is not legitimate to replace the theorem's selected family by the set of every unbounded component, or to replace the witness bound H_r<=N_r by a singleton claim.

3. **Infinite geodesics and special-model confluence.** A sufficient additional route to uniqueness would be both (a) every unbounded component of E_r contains a tail from some common coalescing family of singly infinite geodesics, and (b) every pair of those tails eventually coincides. Then two allegedly distinct components would share a tail and hence be the same component. Neither (a) nor (b) follows from the proofs here. A connected path can switch between distinct finite routes; it need not itself be a geodesic. Aldous separates unique infinite geodesics and coalescence as additional questions in section 7. Results for the specific Poisson-road metric do not automatically transfer to every SIRSN.

The stopping point is sharp: no argument supplied merges the finite exterior-covering family or captures every unbounded component by coalescent geodesic tails. Further attempts without a new input would repeat these gaps. The original uniqueness question is unresolved by this packet.

## 5. Source audit and scope

[A] David Aldous, *Scale-invariant random spatial networks*, Electronic Journal of Probability 19 (2014), paper 15, 1-41. Published text: https://emis.de/ft/43138 . DOI: https://doi.org/10.1214/EJP.v19-2920 . Long preprint: https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf . Locations inspected: sections 2.1-2.3, 6.3, 7, 8.4.2; corresponding long-preprint Open Problem 33.

[B] Jonas Kahn, *Improper Poisson line process as SIRSN in any dimension*, Annals of Probability 44 (2016), 2694-2725, https://doi.org/10.1214/15-AOP1032 ; author version https://arxiv.org/abs/1503.03976 . This establishes the Poisson-road construction; it is not a general uniqueness result for E_r.

[C] Guillaume Blanc, Nicolas Curien, Jonas Kahn, *Geodesics in planar Poisson road random metric*, Proceedings of the London Mathematical Society 131 (2025), e70070, https://doi.org/10.1112/plms.70070 . The inspected author version is https://arxiv.org/abs/2407.07887 (v1, 10 July 2024), with readable full text https://arxiv.org/html/2407.07887 . Its main results concern absence of interior speed pauses, the geodesic frame, and local confluence in a particular model. They do not state the full general-SIRSN target. Publisher full-text retrieval failed; its public bibliographic record was available.

[D] Aldous's maintained problem page, https://www.stat.berkeley.edu/~aldous/Research/OP/sirsn.html , inspected 2026-10-06. It links the foundational and subsequent construction papers. This finite literature pass found no general resolution; absence of a hit is not a proof of present literature openness or novelty.

The exact live UnsolvedMath page https://www.unsolvedmath.com/problems/9700033 and two URL variants failed in the available web reader. The inherited exact-ID statement was therefore checked against primary source [A], not represented as live-site confirmation. The inherited report was literature-only, despite an inaccurate speed-scale gloss; all canonical corpus hashes matched. Current GitHub exact-ID searches were empty and the current main-branch queue showed queued 0/5. Nearby 9700034 is a different question with existing draft PR 372; its authored argument was not reused.

## 6. Verification limits

The accompanying program checks exact rational intensity/scaling identities, finite last-exit/first-entry controls, and strict package membership and hashes. These are diagnostics and reproducibility checks, not a formal proof of the continuum theorem or a simulation-based uniqueness claim. Section 2 incorporates an independent AI audit correction; this is not human peer review, formal verification, or a novelty certificate. Source documents, copied extracts, corpus records, and private coordination material are excluded from this safe packet.
