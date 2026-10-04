# Complete invariance of singular-value basins

## Verdict and exact scope

**Unsolved in this attempt. Five substantive approaches were completed; no full proof or counterexample was obtained.** The conclusions below are restricted facts and reductions, not a resolution or a claim of novelty.

The target is UnsolvedMath 30001393, OWR-4137-010, *Complete Invariance of Singular-Value Basins*. The primary source is W. Bergweiler's Problem 4 on printed p. 2959 of Oberwolfach Report 54/2009, DOI [10.4171/owr/2009/54](https://doi.org/10.4171/owr/2009/54). In the dynamical part, the source specifies the immediate basin of an **attracting fixed point**. The catalogue's shorter wording omits this qualification. The second part concerns any region, meaning a nonempty connected open subset of the plane, without an assumption of simple connectivity.

Write C(f) for the set of finite critical values, A(f) for the finite asymptotic values, and T(f)=C(f) union A(f). Write S(f)=closure(T(f)) in the finite plane. The two questions are:

1. If D is the immediate basin of an attracting fixed point of an entire function f and T(f) is contained in D, must f^{-1}(D)=D?
2. If D is any region containing T(f), must f^{-1}(D) be connected?

The closure in S(f) is important. Containment T(f) subset D does not, merely because D is open, imply S(f) subset D. Neither boundedness of S(f) nor compact containment in D is in the source. Infinity is not one of the asymptotic values required to lie in a plane region.

The second assertion, if proved universally, implies the first. A counterexample only to the second would not settle the first. We have neither kind of counterexample.

## 1. A self-contained finite-degree result

**Proposition.** If P is a nonconstant polynomial and D is a region containing every critical value of P, then P^{-1}(D) is connected.

Proof. Let n=deg(P). The n=1 case is immediate. For n>=2, connect the finitely many critical values by an embedded finite tree contained in D, and take a sufficiently small regular neighbourhood of that tree. Its interior G is a bounded Jordan domain with analytic or smooth boundary, closure contained in D, containing every critical value. The boundary can be chosen to contain no critical value.

Every component V_j of P^{-1}(G) is bounded, and P:V_j -> G is a proper map of some positive degree n_j. Each V_j is simply connected: if gamma is a Jordan curve in V_j and a is outside G, the winding number of P(gamma) about a is zero because G is simply connected. By the argument principle P-a has no zero inside gamma. This holds for every a outside G, so the interior of gamma lies in P^{-1}(G), and thus in V_j. Regularity of the boundary and properness now make the closures topological discs.

Let k be the number of components. Properness gives sum_j n_j=n. Riemann-Hurwitz on each disc gives total ramification n_j-1 in V_j. All n-1 critical points of P, counted with multiplicity, lie in these components. Therefore

    n-1 = sum_j (n_j-1) = n-k,

so k=1.

Finally each component W of P^{-1}(D) maps onto D. Indeed the restriction is proper: inverse images of compact subsets of D are compact under P, and their intersections with W are closed in those inverse images. Its image is consequently both open and closed in D. Every W therefore meets the connected set P^{-1}(G), which is contained in a single component of P^{-1}(D). There can only be one W. QED.

For a constant map f=c, the critical-value hypothesis forces c in D and the inverse image is the whole plane. For an affine nonconstant map, inverse images of regions are homeomorphic copies of those regions. Thus the polynomial boundary cases do not produce a counterexample.

**Dynamical corollary.** The dynamical assertion holds for polynomials. More generally, whenever f^{-1}(D) is connected for an immediate attracting basin D, it equals D. Forward invariance gives D subset f^{-1}(D), and f^{-1}(D) lies in the full basin of the same fixed point. Since D is a connected component of that full basin, connectedness forces equality.

**Limit of this mechanism.** For a transcendental entire map there is no finite global degree n or finite global ramification budget n-1. An infinite-degree component can involve asymptotic curves or infinitely many critical points. Cancelling infinities in n-1=n-k is invalid.

## 2. The compact-singular-set case is established prior work

Bergweiler, Fagella and Rempe-Gillen, *Hyperbolic entire functions with bounded Fatou components*, Comment. Math. Helv. 90 (2015), Proposition 2.9(2), proves the following: if G is simply connected, S(f) subset G, and S(f) is compact, then f^{-1}(G) is connected. Its proof uses homotopy lifting away from S(f). DOI [10.4171/CMH/371](https://doi.org/10.4171/CMH/371), pp. 814-815.

Consequently the dynamical assertion is affirmative under the extra hypothesis that S(f) is compact and contained in D. Here D is simply connected: for a Jordan curve gamma in D, the iterates converge uniformly to the attracting point a on gamma. The maximum principle applied to f^m-a shows that the interior of gamma eventually maps into a small trapping disc about a. That interior belongs to the full basin and, by connectedness, to D. Hence D has no holes. Proposition 2.9 applies, followed by the dynamical corollary above.

For the non-dynamical assertion, the same conclusion follows whenever there is a simply connected subdomain G of D containing compact S(f), using the enlargement lemma cited below. In particular this covers finite S(f), because a finite set in a region can be enclosed in a small neighbourhood of an embedded tree. We do **not** assume that an arbitrary compact set in an arbitrary region can always be enclosed in a simply connected subdomain of that region: a circle in an annulus is a counterexample to that topological shortcut.

These special cases cannot be promoted to the source's general statement. For example, the abstract set {1/j : j>=2} lies in the punctured unit disc, while its closure does not. This is only a set-theoretic control, not an asserted singular set of a constructed entire counterexample.

## 3. What a monodromy proof would need

In the finite-singular-value case one can work over C minus S(f), where f is a covering. The preimage of that punctured plane is the plane minus a closed discrete set of preimages, and is connected. The monodromy action on a regular fibre is therefore transitive. Loops about all the finitely many singular values may be arranged within a thin tree neighbourhood G subset D. Their lifted paths, together with the singular fibres, give the same connection mechanism as the compact case.

For a general entire map the covering is over C minus **S(f)**, not merely over the complement of the actual critical and asymptotic values. If T(f) accumulates at a point of the boundary of D, there need not be an evenly covered neighbourhood of that point, even if that point is neither itself critical nor asymptotic. Thus continuing each individual local inverse along selected arcs is not a proof that a whole homotopy of arcs lifts. In particular, the finite-generator monodromy argument does not establish transitivity using only paths whose images remain in D.

The exact missing statement in this route is: given two points of f^{-1}(D), can their connection in the source plane be replaced by one whose entire image lies in D, under only T(f) subset D? Invoking that replacement without an independent proof would simply restate the non-dynamical question.

## 4. Counterexample search and sharp controls

Three explicit families were tested as mechanisms, analytically rather than by a visual plot.

* For P(z)=z^n, a small disc D=B(1,r), 0<r<1, has n inverse-image components, because it avoids the only critical value 0 and supports n distinct holomorphic roots. This refutes connectedness with the singular-value condition dropped, but is excluded by the actual hypothesis.
* For f(z)=exp(z), a small disc around 1 avoiding 0 has infinitely many disjoint logarithmic inverse branches. If a region D instead contains 0, choose epsilon>0 with B(0,epsilon) subset D. The preimage of that disc is the connected half-plane Re(z)<log(epsilon), and the enlargement lemma gives connectedness of f^{-1}(D). Thus omission of the asymptotic value explains the false candidate exactly.
* For f(z)=exp(z)+z, the critical points are (2j+1)pi i and the critical values are -1+(2j+1)pi i. Rempe-Gillen and Sixsmith construct pairwise disjoint domains with connected preimages for this map. Their construction invalidates a tempting general topological assertion used in Baker's old argument; it does not provide the disconnected preimage required here, and those disjoint domains do not each contain every critical value. Enlarging one of their domains preserves, rather than destroys, its connected-preimage property. Hence this published example cannot be relabelled as a counterexample to our target.

The enlargement fact just used is Rempe-Gillen and Sixsmith, Lemma 8.3: if a connected set A with at least two points has connected full preimage, every domain containing A has connected full preimage. Their proof uses the fact that a component over a domain can omit at most one value. The same paper's Corollary 8.5 records the compact-singular-set criterion, while Section 7 identifies the defective step in Baker's older proof. Reference: *On connected preimages of simply-connected domains under entire functions*, Geom. Funct. Anal. 29 (2019), 1579-1615, DOI [10.1007/s00039-019-00488-2](https://doi.org/10.1007/s00039-019-00488-2); checked accepted version [arXiv:1801.06359v3](https://arxiv.org/abs/1801.06359v3).

No surgery construction with independently verified singular values and disconnected preimage was obtained. Merely drawing several apparent inverse-image components is insufficient; it cannot exclude thin connections outside a finite computational window, and it cannot certify that every finite asymptotic value has been included in D.

## 5. A precise dynamical exhaustion criterion

Choose a small disc B about the attracting fixed point a with f(closure(B)) subset B. Let W_m=f^{-m}(B), and let U_m be the component of W_m containing a. Then

    W_m subset W_{m+1},    U_m subset U_{m+1},
    A(a)=union_m W_m,      D=union_m U_m.

Here A(a) is the full attracting basin. The equality for A(a) follows from eventual entry into B. For the equality for D, join a point of D to a by a compact path in D. Every point of the path eventually enters B. The increasing open cover (W_m) has a finite subcover of that path, so one W_M contains the entire path, placing the point in U_M.

It follows that D is completely invariant exactly when **every component V of every W_m is contained in some U_M** (the index M may depend on V). For the forward direction, if D is completely invariant then repeated pullback of B subset D stays in D. A point of V belongs to some U_M; after increasing M to at least m, the connected set V subset W_M intersects U_M and is therefore contained in U_M. Conversely the component-capture condition gives A(a)=D, and the full basin is completely invariant.

This reformulates the residual dynamical obstruction concretely. Each actual singular value lies in some U_m by hypothesis, but this pointwise statement supplies neither a uniform m capturing all singular values nor a proof that all other pullback components are eventually captured by U_M. An infinite sequence of singular values can have entry times tending to infinity. The compact-singular-set case avoids this issue by a finite-cover argument; the original hypothesis does not.

## Remaining gap and non-claims

The general connected-preimage assertion and the unrestricted immediate-basin assertion remain unresolved by these five routes. The strongest safe conclusion is the finite-degree proof, the compact/finite-singular-value consequences of published results, and the exact pullback-component capture criterion. The attempt does not establish a new theorem settling the source, a counterexample, or historical priority. A bounded literature check through 2026-10-04 did not locate a full resolution; absence from that search is not a proof that no later result exists.

The included exact controls check finite combinatorial identities and boundary examples. They do not certify an infinite-dimensional analytic theorem or replace expert review.
