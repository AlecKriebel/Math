# SIRSN major-road components: a finite exterior-covering family

Problem 9700033 / AMR-096-0033, rank 935. Author disposition: **UNSOLVED; scoped partial result; 3 of at most 5 approaches used.** This is AI-assisted, unrefereed work. Neither a general uniqueness theorem, a SIRSN counterexample, nor historical novelty is claimed.

## 1. Target and hypotheses

The target is uniqueness of the unbounded connected component of E(infinity,1). It is Open Problem 33 in Aldous's long 2012 preprint, and Open Problem 7 in the published 2014 paper, section 8.4.2 [A]. It is not the maximal-route-length problem numbered 9700034.

Write E_r = E(infinity,r). In Aldous's notation [A, equations (2.17)-(2.20)], E(lambda,r) is the union of the routes between points of an independent intensity-lambda planar Poisson sample, with the closed radius-r discs around each route's two endpoints removed. Increasing lambda gives E_r. The r parameter is Euclidean endpoint exclusion, not a speed threshold.

The full planar SIRSN assumptions are: compatible non-self-intersecting feasible routes; consistent measurable finite-dimensional distributions; translation, rotation, and spatial scaling invariance; finite mean length of a unit-displacement route; and finite major-road intensity p(1). The finite-intensity sampled network condition follows. Ergodicity, finite energy, insertion tolerance of roads, a cost metric, and coalescence of all infinite geodesics are not additional assumptions in the result below.

We use these source inputs explicitly: intensity(E_r)=p(1)/r; E_r has the intrinsic sampling-independent version of Proposition 6.3; and equation (6.4) allows a single deterministic root at 0 to be planted without enlarging E_r, almost surely. Only countably sampled routes from that root will be used. No assertion about simultaneously adjoining every deterministic pair of points is needed.

## 2. Partial theorem

**Theorem.** Fix r>0. Almost surely there is a nonempty finite collection C_1,...,C_K of unbounded connected components of E_r and a finite random M such that

dist(x, C_1 union ... union C_K) <= 2r whenever |x|>M.

One can choose these components among those meeting circle(0,2r), and E[K] <= 8p(1). Here distance means infimum distance. We do not assert that a nearest point is attained, that the chosen components are all unbounded components, or that K=1. The probability-one statement is for each fixed r; a countable intersection supplies it simultaneously for positive rational r.

**Proof.** By the stationary isotropic edge-process intersection identity [A, section 2.1], the mean number N_r of points where E_r meets circle(0,2r) is

E[N_r] = (2/pi) intensity(E_r) length(circle(0,2r)) = 8p(1).

This is the curved-boundary version of the line-intersection identity (2.2): integrate the same local intersection intensity along the circle. Equivalently use the coarea formula on each line segment and the translation- and rotation-invariant mean length-direction measure. Tangencies and segment endpoints lying on this fixed circle have probability zero under translation invariance. Consequently N_r is finite almost surely. Distinct connected components meeting the circle use disjoint nonempty subsets of these N_r points; list them as D_1,...,D_J, with J<=N_r.

Couple the Poisson samples as in [A] and put Xi_infinity=union_lambda Xi(lambda). This countable set is almost surely dense and unbounded. Plant 0. At the present fixed r, equation (6.4) identifies the resulting E_r with the original E_r, on a probability-one event. In particular, every part of every route R(0,xi), xi in Xi_infinity, at distance greater than r from both endpoints is already in E_r.

Take xi in Xi_infinity with |xi|>4r. Parameterize R(0,xi) continuously. Let t_1 be its first encounter with the closed disc centered at xi of radius 2r. Let t_0 be its last encounter, before t_1, with the closed disc centered at 0 of radius 2r. These times exist, by continuity and the disjointness of the two closed discs. The subroute from t_0 to t_1 is outside their interiors and meets their boundaries at its endpoints. Every point of this subroute is at distance at least 2r>r from both route endpoints. Thus the whole subroute is in E_r. It starts on circle(0,2r), so lies in some D_i, and ends at distance 2r from xi. Therefore

min_i dist(xi,D_i) <= 2r.                                           (1)

There are only finitely many D_i. Their bounded members, if any, are all contained in one finite random disc B(0,B). For |xi|>B+2r, none of those bounded members can meet the circle of radius 2r about xi. Hence the component supplying the subroute in (1) is unbounded. There must be at least one such member, since Xi_infinity is unbounded.

Let C_1,...,C_K be all the unbounded members of this finite list. Then K<=J<=N_r, and (1) holds with these C_i whenever |xi|>max(4r,B+2r). The distance to a nonempty set is a 1-Lipschitz function, whether or not the set is closed. Density of Xi_infinity therefore extends that inequality to every x outside the same disc. Taking expectations proves the claimed bound. QED.

This strengthens the bare statement that at least one unbounded component exists: finitely many of them together stay within a fixed Euclidean distance of every sufficiently remote location. The bound counts a selected family only, not every component in the plane.

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

2. **All-pairs routing and finite crossings.** This gives the finite exterior-covering theorem. The missing implication is from finitely many unbounded components collectively within 2r of all remote points to one unbounded component. It is not legitimate to replace the theorem's selected family by the set of every unbounded component, or to replace K<=N_r by K=1.

3. **Infinite geodesics and special-model confluence.** A sufficient additional route to uniqueness would be both (a) every unbounded component of E_r contains a tail from some common coalescing family of singly infinite geodesics, and (b) every pair of those tails eventually coincides. Then two allegedly distinct components would share a tail and hence be the same component. Neither (a) nor (b) follows from the proofs here. A connected path can switch between distinct finite routes; it need not itself be a geodesic. Aldous separates unique infinite geodesics and coalescence as additional questions in section 7. Results for the specific Poisson-road metric do not automatically transfer to every SIRSN.

The stopping point is sharp: no argument supplied merges the finite exterior-covering family or captures every unbounded component by coalescent geodesic tails. Further attempts without a new input would repeat these gaps. The original uniqueness question is unresolved by this packet.

## 5. Source audit and scope

[A] David Aldous, *Scale-invariant random spatial networks*, Electronic Journal of Probability 19 (2014), paper 15, 1-41. Published text: https://emis.de/ft/43138 . DOI: https://doi.org/10.1214/EJP.v19-2920 . Long preprint: https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf . Locations inspected: sections 2.1-2.3, 6.3, 7, 8.4.2; corresponding long-preprint Open Problem 33.

[B] Jonas Kahn, *Improper Poisson line process as SIRSN in any dimension*, Annals of Probability 44 (2016), 2694-2725, https://doi.org/10.1214/15-AOP1032 ; author version https://arxiv.org/abs/1503.03976 . This establishes the Poisson-road construction; it is not a general uniqueness result for E_r.

[C] Guillaume Blanc, Nicolas Curien, Jonas Kahn, *Geodesics in planar Poisson road random metric*, Proceedings of the London Mathematical Society 131 (2025), e70070, https://doi.org/10.1112/plms.70070 . The inspected author version is https://arxiv.org/abs/2407.07887 (v1, 10 July 2024), with readable full text https://arxiv.org/html/2407.07887 . Its main results concern absence of interior speed pauses, the geodesic frame, and local confluence in a particular model. They do not state the full general-SIRSN target. Publisher full-text retrieval failed; its public bibliographic record was available.

[D] Aldous's maintained problem page, https://www.stat.berkeley.edu/~aldous/Research/OP/sirsn.html , inspected 2026-10-06. It links the foundational and subsequent construction papers. This finite literature pass found no general resolution; absence of a hit is not a proof of present literature openness or novelty.

The exact live UnsolvedMath page https://www.unsolvedmath.com/problems/9700033 and two URL variants failed in the available web reader. The inherited exact-ID statement was therefore checked against primary source [A], not represented as live-site confirmation. The inherited report was literature-only, despite an inaccurate speed-scale gloss; all canonical corpus hashes matched. Current GitHub exact-ID searches were empty and the current main-branch queue showed queued 0/5. Nearby 9700034 is a different question with existing draft PR 372; its authored argument was not reused.

## 6. Verification limits

The accompanying program checks exact rational intensity/scaling identities, finite last-exit/first-entry controls, and strict package membership and hashes. These are diagnostics and reproducibility checks, not a formal proof of the continuum theorem or a simulation-based uniqueness claim. The mathematical proofs above require independent review. Source documents, copied extracts, corpus records, and private coordination material are excluded from this safe packet.
