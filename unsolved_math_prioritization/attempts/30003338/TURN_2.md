# Turn 2: universal one-coordinate monotone coupling and exact induction obstructions

2026-10-02. Second substantive author turn for 30003338. **Original target unresolved, 2/5.** This turn derives a universal scoped correlation statement and an exact preimage formula explaining why the natural pinning induction fails. A separate bounded exact search found no target counterexample. The underlying Kempe method is classical; no novelty claim is made.

## 1. A universal one-coordinate conclusion

Let Z=f^(-1)(0)∩A for a uniform proper q-coloring of an arbitrary finite bipartite graph, q≥3. For every a∈A, the conditional law of Z given f(a)=0 stochastically dominates the unconditional law, and also the law given f(a)≠0. Consequently

    Cov(1_(f(a)=0), X(Z)) ≥ 0                                 (1)

for every increasing real function X, not just for another coordinate or a conjunction. By linearity the same holds with any nonnegative linear combination of the zero indicators in the first argument. This is still weaker than association of two arbitrary increasing functions.

**Proof by a monotone Kempe bijection.** Fix a color c≠0 and a coloring with f(a)=c. In the subgraph induced by vertices colored 0 or c, take the connected component containing a and interchange the two colors there. The coloring remains proper. Because G is bipartite, every A vertex in this component has color c before the interchange and color 0 afterward. Thus its A-zero set can only increase.

The operation is a bijection from colorings with f(a)=c to colorings with f(a)=0: the induced two-color component is unchanged and the same operation reverses it. Uniformity in each conditional color class is therefore preserved. Color-permutation symmetry makes the original law a uniform mixture of these q conditional laws; use the identity operation when c=0. Mixing the monotone bijections proves the asserted dominance. It also couples each nonzero conditional color class below the zero class, hence their mixture below it. This proves (1).

This is an explicit use of the standard Kempe-chain mechanism behind the singleton/conjunction observation credited in Peled–Spinka, arXiv:2001.11566v2, p. 48. It does not imply that the same coupling is uniform after other vertices are pinned.

## 2. Exact multiplicity after positive pins

Let S⊂A and a∈A\S. Write Ω_S for proper colorings with every vertex of S colored 0. For f∈Ω_S, force a to 0 by swapping its (0,f(a))-Kempe component, doing nothing if it is already 0. This still maps Ω_S to Ω_(S∪{a}) and increases Z. Indeed, if f(a)=c≠0, its two-color component cannot contain a pinned S vertex: all its A vertices have color c.

However, this map need not push forward the uniform measure to the uniform pinned measure. For a target coloring g∈Ω_(S∪{a}), define

    r_S,a(g) = 1 + #{c≠0 : K_(0,c)(a;g)∩S is empty},          (2)

where K is the indicated two-color component. Then g has **exactly r_S,a(g) preimages**. One is g itself. For each nonzero c, reversing the swap gives one allowed preimage precisely when its component avoids S; if it meets S, reversing would break the pin. These alternatives are distinct because they have different colors at a, and exhaust every possible preimage.

Thus the monotone pushforward of the uniform law on Ω_S assigns probability

    r_S,a(g) / |Ω_S|                                         (3)

to g, while the desired uniform pinned law assigns 1/|Ω_(S∪{a})|. The target can only be obtained by an additional reweighting proportional to 1/r_S,a. Its effect on increasing functions is not controlled by the monotonicity of the swap. When S is empty, r=q is constant and Section 1 is recovered. This identifies a precise bias rather than assuming an unsuccessful induction works.

## 3. The obstruction is genuine, not just a missing normalization estimate

Use the published dreidel graph from turn 1, with A=(u,v,w,left-top,right-top), B-neighborhood masks (25,14,22,6), and q=3. Exact enumeration gives 336 proper colorings, 112 with v=0, and 88 with v=w=0. Its probabilities are

    P(u=0 | v=0)=23/56,
    P(w=0 | v=0)=11/14,
    P(u=w=0 | v=0)=9/28.

Therefore

    Cov(1_(u=0),1_(w=0) | v=0) = −1/784.                    (4)

The conditional measure after a single positive pin is not positively associated. By contrast the original covariance of u,w is 13/504 > 0, and turn 1 checked full association for this particular unconditioned graph. Equation (4) is not a counterexample to the original problem, which imposes no pins.

For S={v} and a=w, the target colorings in (2) have the following exact multiplicities:

    r=1, u≠0: 38;     r=1, u=0: 26;
    r=2, u≠0: 14;     r=2, u=0: 10.

These sum to 88 targets and to 112 preimages when weighted by r. The monotone pushforward has u-zero mean (26+2·10)/112=23/56, while the uniform target has mean (26+10)/88=9/22, which is smaller. Thus the nonuniformity in (3) matters even for a single indicator. The conditional drop is already implicit in the source's known FKG obstruction; it is credited, not presented as a newly found target counterexample.

## 4. A second simple sorting mechanism also fails

A standard two-copy attempt would swap colors between two proper colorings on connected components of their conflict graph. An edge is conflicting if a color at one endpoint in one copy equals the color at the other endpoint in the other copy. Swapping one endpoint's copy choice but not the other's creates a monochromatic edge in one copy, so any valid swap must be constant on conflict components.

Such a component need not have all its A-zero discrepancies aligned. On the five-vertex path, with A at positions 0,2,4, take

    f=(0,2,1,0,2),       g=(1,0,2,1,0).

Both are proper 3-colorings. Every edge is conflicting, so the whole path is one component and only swapping none or all vertices preserves both proper colorings. The A-zero sets are {0} and {4}. Swapping whole components cannot place their union in one copy and their intersection in the other. The 32 possible pointwise swap choices are checked exactly; only the two constant choices work.

The graph is a forest and its true marginal is positively associated by turn 1. This example only blocks the naive component-sorting proof, not association. Any successful two-copy construction must do more than independently swap these conflict components.

## 5. New finite search: repeated neighborhoods and larger A

The separate portable C++ search integrates out B exactly as in (1) of turn 1. It uses a fixed mt19937 seed 30003338 and tests 1,200 graphs for each of

    (|A|,q) = (5,3),(6,3),(7,3),(8,3),(9,3),
              (5,4),(6,4),(7,4),(8,4),(5,5),(6,5).

Each graph has 2 through 20 B vertices, degrees from 2 through min(5,|A|), and repeated neighborhoods are explicitly allowed. For each graph it checks every pair of nonempty principal upsets, then 48 fixed-seed sampled upward events, each a union of one through five principal upsets, against one another. All event masses and covariance numerators are exact.

No negative covariance was found among 13,200 graph/q cases, 261,997,200 principal-event comparisons and 14,889,600 sampled-upset comparisons. This is a bounded witness search, not an exhaustive graph classification or a theorem. In particular it does not cover every increasing event when |A|>5, and it does not justify extrapolating the finite successes.

All counts are below signed 64-bit capacity: the largest crude bound used is 5^26 < 2^63, while for q=4 it is 4^28 and for q=3 it is 3^29. Products are below signed 128-bit capacity (5^52 < 2^127 is the largest of these bounds). There are no floating comparisons. The deterministic source and output are turn2_search.cpp and TURN_2_SEARCH.json.

The independent-from-that-search Python controls enumerate all 336 dreidel colorings, verify each single-coordinate Kempe bijection and monotonicity, check the multiplicity formula (2), the conditional probabilities and both covariance signs, and enumerate all 32 path swaps. All 1,819 exact assertions pass. Files: turn2_kempe_controls.py and TURN_2_KEMPE_CHECKS.json. These are author controls, not independent review.

## 6. Exact remaining problem

The universal one-coordinate dominance does not settle covariance of two nonlinear increasing observables. Positive-pin induction is false, and conflict-component sorting does not align the required zero sets even on a path. The finite search found no full-target counterexample. Original target: **unresolved 2/5**.

For a different next mechanism, investigate the indicator distribution on degree-two subdivision vertices of a general graph, where integrating the other side gives a ferromagnetic Potts model but the observed indicators live on the subdivided edges. This may expose either a useful cluster-coupling theorem or an exact higher-order obstruction. It must not be conflated with turn 1's already-proved degree-two condition on the opposite, integrated-out side.
