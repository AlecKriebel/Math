# Local-to-global medianity: five bounded approaches

## Outcome and scope

**UNSOLVED.** This packet contains rigorous elementary lemmas, obstruction examples, and explicitly conditional routes. It gives neither a proof nor a counterexample to the full question. No novelty or priority claim is made. The mathematical attempt budget is five distinct families; literature inspection and verification are not additional proof attempts.

The target is Bowditch's Problem 12 in *Median Geometry and Applications*, Oberwolfach Report 8/2026, printed p. 533. For a metric d define

I(a,b) = {z : d(a,z)+d(z,b)=d(a,b)},
Med(a,b,c) = I(a,b) ∩ I(b,c) ∩ I(c,a).

Let X be a complete, simply connected path-metric space. Assume that every p has an open neighborhood U such that every triple in U has exactly one median **in X**, with intervals computed using d. Does every triple in X have exactly one median?

Here a path metric means the infimum of lengths of continuous rectifiable paths; minimizing geodesics are not assumed. Simply connected includes path connected. Completeness is metric completeness. There is no properness, local compactness, finite-rank, separability, uniform local scale, or global bicombing hypothesis. A unique interval median is not a unique geodesic and is not merely a minimizer of the sum of distances.

The ambient formulation follows the definition of a good subset in Bowditch's Section 9. One must not silently replace it by either intrinsic-length medianity of a neighborhood or closure of the neighborhood under ambient medians. A sufficiently small triple's ambient median lies in a somewhat larger neighborhood: if its points lie in B(p,r), then its median m satisfies d(p,m)<3r. This estimate does not make B(p,r) median-closed.

The local-median component in record 30006622 is this same target and shares this budget. Its two group-theoretic components remain untouched. Record 30006623's raw extraction contains neighboring Problem 12 text, but its normalized target is different. Raw source concatenation is not authority to add cubulability or residual finiteness to the present question.

## Verified literature boundary

The inspected Bowditch manuscript is dated 12 May 2023. Its Theorem 1.1 assumes uniform local medianity; Proposition 9.1 adds global modularity to local medianity and connected completeness; Lemma 9.2 assumes uniformity on each bounded set; Proposition 9.3 covers local compactness; Proposition 9.4 uses uniform short-path homotopy control, abbreviated USC below. None has the target's full hypotheses alone. The 2026 workshop report repeats the question. Targeted current searches and the author's current preprint listing did not locate a resolution; this is bounded negative literature evidence, not a proof that no later or unindexed result exists.

One source warning matters to proposed shortcuts: the parenthetical uniqueness assertion in manuscript Lemma 2.8 is false literally. In the l1 plane, two different monotone paths connect (0,0) to (h,h) and both have length 2h, for arbitrarily small h. This does not refute the uniform median theorem. The packet never uses unique local geodesics. The assertion was checked against the rendered PDF, not only extracted text.

## Approach 1: compact control and variable-scale continuation

### Lemma 1.1: a continuous local scale

Call a triple good when its ambient median set is a singleton. Set

r(p) = sup {s ∈ (0,1] : every triple in B(p,s) is good}.

Then r is positive and 1-Lipschitz. Indeed, if B(p,s) is good and t<s-d(p,q), then B(q,t)⊂B(p,s), hence r(q)≥s-d(p,q) whenever that number is positive. Pass to the supremum and interchange p,q. The cap at 1 causes no difficulty.

Consequently, if K⊂X is nonempty compact, then η=min_K r>0. If a is within η/4 of K and diam{a,b,c}<η/4, choose k∈K with d(k,a)<η/4. All three points lie in B(k,η/2), which is good because η/2<r(k). Therefore every such triple is good.

Thus any sequence of bad triples with diameters tending to zero must leave every fixed compact set, even in this stronger neighborhood sense. In particular, its first vertices cannot have a convergent subsequence. Completeness does not make that sequence Cauchy.

### Attempted continuation

A chosen path and a chosen nullhomotopy have compact images. Lemma 1.1 therefore supplies a positive usable scale on a neighborhood of each *fixed* image. This permits finite subdivisions of that path or homotopy with good small triples.

The attempted proof then iterates median insertions to make a global tripod. The obstruction is not the first subdivision. It is that newly inserted points and successive fillings have not been shown to stay in one compact controlled region. Even a bounded region need not have a positive infimum of r. Nor has the iteration been shown to have summable displacement. Invoking compactness for the union of all stages is unjustified.

This family reaches exactly the hypotheses of the established bounded-set theorem if a positive lower scale on each bounded set is supplied. It does not derive that hypothesis. The bounded example in Approach 5 shows why the derivation cannot ignore simple connectivity. No full-target conclusion follows.

## Approach 2: variational modularization

[The separately derived quantitative argument is incorporated in VARIATIONAL_AND_BICOMBING.md.]

## Approach 3: global bicombing and auxiliary nonpositively curved metrics

[The separately derived metric-compatibility argument is incorporated in VARIATIONAL_AND_BICOMBING.md.]

## Approach 4: normalize the radii by changing the metric

One might replace d by a weighted path metric, making very small local radii larger, and then apply the uniform theorem. The missing premise is preservation of local medianity. The following exact calculation disproves that premise even for a bounded smooth factor.

### Proposition 4.1: a conformal change destroys local medianity

On S=[0,1]×R give absolutely continuous paths length

L(γ)=∫(1+x(t))(|x'(t)|+|y'(t)|)dt,

and let d_w be the induced length metric. The unweighted metric d_1 is l1 distance. Since d_1≤d_w≤2d_1, S with d_w is complete and has its usual, simply connected topology.

Write F(x)=x+x²/2. If P=(x,y), Q=(u,v), and k=|y-v|<2, then

d_w(P,Q)=|F(x)-F(u)|+(1+min{x,u})k.                 (4.1)

Proof. For any path from P to Q let z be its minimum x-coordinate. The horizontal contribution is at least F(x)+F(u)-2F(z), and its vertical contribution is at least (1+z)k. For 0≤z≤min{x,u}, the derivative with respect to z of their sum is k-2(1+z)<0. The lower bound is minimized at z=min{x,u}. A horizontal segment plus a vertical segment at the smaller x-coordinate attains it. The same argument applies to all rectifiable paths by arclength parametrization, since d_w and d_1 are bilipschitz equivalent.

Take A=(a,0), B=(b,0), C=(b,k), where 0≤a<b≤1 and 0<k<2. The interval I(A,B) is precisely the horizontal segment y=0, a≤x≤b. Indeed, for every W=(x,y), the sum d_w(A,W)+d_w(W,B) is at least |F(a)-F(x)|+|F(b)-F(x)|+2|y|. This exceeds F(b)-F(a) if y is nonzero or x is outside [a,b], and equality is attained on the horizontal segment. This uses lower bounds on the distance infimum and does not assume a minimizing path exists. For W=(x,0) on this segment,

d_w(B,W)+d_w(W,C)-d_w(B,C)
=2(F(b)-F(x))-(b-x)k
=(b-x)(2+b+x-k).

It vanishes only at x=b. Hence I(A,B)∩I(B,C)={B}. But

d_w(A,B)+d_w(B,C)-d_w(A,C)=(b-a)k>0,

so B∉I(A,C). This triple has no median. By taking b-a and k arbitrarily small, such triples occur in every neighborhood of every interior point, and also in relative neighborhoods of either boundary line.

The constant-weight control is the usual l1 strip, which is median. Thus topology, completeness, bilipschitz equivalence, bounded positive weights, and smoothness do not preserve the needed interval identities. This rules out automatic conformal uniformization, not the original conjecture. A special weight preserving the relevant wall-additive structure might work, but no such construction is supplied.

## Approach 5: construct and repair counterexamples

### Proposition 5.1: bounded complete local medianity can be nonuniform

Start with a root o and countably many disjoint unit intervals [o,v_n], identified only at o. At v_n attach a circle C_n of circumference 1/n. Use the path metric. Call the result X_c.

X_c is bounded (distance from o is at most 3/2) and geodesic. Each branch consisting of its spoke and circle is compact. If a Cauchy sequence is eventually in a finite union of branches it converges there. Otherwise, given ε>0, the Cauchy condition gives a tail of pairwise distances below ε. For any tail term one can choose another tail term in a different branch; their distance is the sum of their distances from o. The original term therefore lies within ε of o. Thus the sequence converges to o. This proves completeness.

Every point has an ambient-good neighborhood. At o a ball of radius less than 1/2 is a metric tree. Away from o and the circle attachment points, sufficiently small neighborhoods are intervals. At an attachment point choose radius less than one eighth of that circle's circumference; the neighborhood is a tripod and any route around the rest of the circle is strictly longer between its points. Similar small choices at the other points ensure ambient intervals agree with the local tree intervals. Trees have unique medians.

Nevertheless, the three equally spaced points of C_n form a bad triple of diameter 1/(3n): their pairwise intervals are the three short circle arcs and have no common point. Excursions down the spoke return to the same attachment point and cannot shorten a circle distance. Thus no uniform median radius exists, even on this bounded space. The attachment vertices v_n have pairwise distance 2, so no compactness argument forces them together.

This is **not** a counterexample to the target. For each n there is a continuous retraction X_c→C_n: collapse the rest to v_n and restrict to the identity on C_n. Hence π1(X_c) contains a nontrivial circle loop, and X_c is not simply connected.

### Proposition 5.2: the direct filling repair restores medians

Replace each C_n by the entire l1 square Q_n=[0,1/(4n)]², identifying one corner with v_n. Its boundary has the former circumference, but the intrinsic boundary metric is not retained after filling: crossing the square creates new shorter intervals.

The resulting space X_s is complete by the same Cauchy argument and contractible. For continuity of a simultaneous contraction, first shrink every square to its attachment corner by linear coordinate contraction, keeping spokes fixed; then shrink every spoke to o. Both stages are continuous in the path metric, including at o, and uniformly continuous in the time parameter because all branches have uniformly bounded diameter.

It is globally median. More generally, a point wedge of median spaces is median: if three points are in one factor, use its median; if two are in factor A and one outside A, use the median of the first two and the wedge point inside A; if they lie in three different factors, use the wedge point. Distances between different factors add through the wedge point, directly verifying the three interval conditions and uniqueness. First apply this to each spoke-plus-square, then to their wedge at o. Infinite valence does not change the three-point verification.

Thus adding the most natural median filling removes the global obstruction. To obtain a genuine counterexample by this family one still needs simply connected fillings that preserve *every* local good neighborhood while keeping a bad triple. None has been constructed.

### Proposition 5.3: completeness cannot be omitted

Let Y=R²\([0,∞)×{0}) with its intrinsic l1 path metric. Polar coordinates identify its topology with (0,∞)×(0,2π), so Y is simply connected. Small enough rectangular neighborhoods have their ordinary l1 distances and ambient intervals, so Y is locally median.

Take A=(-1,0), B=(1,1), C=(1,-1). Then d(A,B)=d(A,C)=3 and d(B,C)=4. The last value is an infimum: any B-to-C path crosses y=0 at x<0 and has length at least 4-2x>4; paths crossing at x=-ε approach length 4.

A point in I(A,B)∩I(A,C) must have y=0 and -1≤x<0, by the ordinary coordinatewise lower bounds on path length. For any such point W=(x,0), d(B,W)+d(W,C)=4-2x>4. Hence Med(A,B,C) is empty. The sequence (-1/n,0) is Cauchy and has no limit in Y, so metric completeness fails. This example isolates exactly the omitted hypothesis and is not a target counterexample.

## Final boundary

The full question remains unanswered after five families. A complete proof still needs, for example, a global construction of approximate medians with controlled convergence, a globally compatible bicombing/auxiliary metric, or a replacement for uniform short-homotopy control. A negative answer needs a complete simply connected locally median space with an explicitly verified bad triple. None of the examples here meets those four requirements simultaneously.

The exact-check program tests elementary identities and finite controls; it cannot certify the infinite-dimensional or topological missing steps. Known special-case theorems are credited dependencies, not new resolutions. No source body, corpus record, private coordination material, or unrelated queue content belongs in this authored packet.

## Public references

- Brian H. Bowditch, *A Cartan-Hadamard theorem for median metric spaces*, manuscript revised 12 May 2023: https://bhbowditch.com/papers/ch-median.pdf
- *Median Geometry and Applications*, Oberwolfach Report 8/2026, Problem 12, printed p. 533: https://ems.press/content/serial-article-files/53603 ; DOI https://doi.org/10.4171/owr/2026/8
- Brian H. Bowditch, *Some properties of median metric spaces*, Groups, Geometry, and Dynamics 10 (2016), 279–317: https://bhbowditch.com/papers/medianmetrics.pdf
- Author's current manuscript listing, checked 8 October 2026: https://bhbowditch.com/preprints.html
