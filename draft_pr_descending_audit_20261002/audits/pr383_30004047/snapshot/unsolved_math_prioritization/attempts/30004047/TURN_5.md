# Author turn 5: disjoint maximal neighborhoods, stability, and an uncrossing obstruction

## 1. An unbounded-size positive class for the full asymmetric question

Work with positive weights alpha, beta, gamma on the three finite parts, each of total weight one. Let S_b=N_A(b). Assume that the distinct inclusion-maximal nonempty members of the family {S_b:b in B} are pairwise disjoint. In particular this holds whenever the entire family is laminar: any two neighborhoods are disjoint or one contains the other.

**Theorem.** For every integer k>=1, if

    x+ky>1 and kx+y>=1,

some C-vertex reaches A-weight at least 1/k.

There is no size bound on any part. Only the first-incidence family has the stated structural restriction; no extra reverse degree assumptions are added. The theorem proves the exact asymmetric implication on this class, not on arbitrary graphs.

## 2. Proof by maximal blocks

The k=1 case is the known elementary full-graph fact, also primary Theorem 5.2: average the B-to-C degree inequalities to find a c whose B-neighbor beta-weight is at least y. Every a has B-neighbor weight at least x, and x+y>1 forces an intersection. Thus c reaches all of A.

Let k>=2 and suppose every c reaches strictly less than 1/k of A. Write the maximal neighborhoods as M_1,...,M_m. They cover A because every a has a middle neighbor and every occurring nonempty finite neighborhood lies in a maximal one. They are disjoint by hypothesis.

Every nonempty S_b belongs to exactly one maximal block. Let beta_i be the total middle weight of the types assigned to block M_i. Since any a in M_i has all its middle neighbors in this group, beta_i>=x. Empty middle types need not be assigned. Consequently

    mx<=sum_i beta_i<=1.                                        (1)

Each M_i itself occurs as S_b for a middle vertex, which has some C-neighbor. Hence alpha(M_i)<1/k. Since their weights sum to one, m>=k+1.

We also have y<1/k. Indeed, every a lies next to a middle vertex, and therefore is reached by C-weight at least y. Averaging the reached A-weight with respect to gamma gives a value at least y. Every individual reached A-weight is strictly below 1/k, so the average is strictly below it.

If m>=k+2, then

    kx+y < k/m+1/k <= k/(k+2)+1/k <=1,

where the last inequality holds for every k>=2. This contradicts kx+y>=1. Thus m=k+1.

Any two distinct maximal blocks have combined alpha-weight greater than 1/k: the other k-1 blocks each have weight strictly below 1/k. Choose a middle representative b_i of each M_i. The C-neighborhoods of these representatives are pairwise disjoint; otherwise a common C-vertex would reach both entire blocks and exceed 1/k. Since each representative has C-neighbor weight at least y,

    (k+1)y<=1.

Together with (1), this gives x+ky<=1, the other required contradiction. The theorem is proved. Notice that a C-vertex may reach partial portions of several blocks; the proof only asserts disjointness for the C-neighborhoods of the maximal representatives.

## 3. Quantitative stability under deletion of exceptional middle weight

The class theorem has a direct robust form. Suppose one can delete a set E of middle vertices, of beta-weight epsilon, so that the remaining nonempty A-neighborhoods have pairwise disjoint maximal members. Assume k>=2 and

    0<=epsilon<x,
    epsilon < (x+ky-1)/(ky),
    epsilon <= (kx+y-1)/(k+y-1).                                (2)

Then the original graph has a C-vertex reaching A-weight at least 1/k.

To prove this, renormalize beta on B minus E; it has positive total weight because epsilon<x<=1. Each a retains normalized degree at least

    x'=(x-epsilon)/(1-epsilon)>0.

The B-to-C degree lower bound y is unchanged. The second and third inequalities in (2) are exactly

    x'+ky>1 and kx'+y>=1,

after multiplying by 1-epsilon. Apply the structural theorem to the smaller graph. Every reached A-vertex there is also reached in the original graph, so its conclusion transfers.

For a strict diagonal point x=y>1/(k+1), the two numerator gaps in (2) are positive. Thus a definite amount of exceptional middle weight can be tolerated. This is a conditional stability theorem, not a claim that every graph admits such a small deletion. At the weak boundary kx+y=1 the third bound forces epsilon=0, as it must for this argument.

## 4. Why ordinary union/intersection uncrossing does not give a general reduction

The next attempted step would be to replace two crossing equal-weight middle neighborhoods S_1,S_2 by S_1 union S_2 and S_1 intersect S_2. This preserves each A-degree exactly, since the two incidence indicators have the same sum. It does not automatically preserve the B-to-C requirement while preventing an increase in maximum reach.

Use the ordinary 396-vertex graph from turn 1: A is all nine-subsets H of [11], B all four-subsets b, C=[11], with H adjacent to b iff b is contained in H, and b adjacent to c iff c belongs to b. This is (4/11,4/11)-constrained. Every c reaches exactly 45 of the 55 first vertices.

Choose disjoint middle labels

    b_1={1,2,3,4}, b_2={5,6,7,8}.

Their A-neighborhoods S_1,S_2 each have size binomial(7,5)=21, their intersection has size binomial(3,1)=3, and their union has size 39. They cross properly.

Replace the two A-neighborhoods by their union and intersection, keeping both middle weights unchanged and leaving every other edge fixed. Delete the old C-edges incident to these two middle vertices; they may now be reassigned. For every c, the other 328 middle vertices still reach exactly the old 45 first vertices. Indeed, each nine-set H containing c has 56 four-subsets containing c, and removing at most two leaves at least 54. A nine-set not containing c is not reached through any unchanged middle vertex adjacent to c.

Now the new union middle vertex cannot be given even one C-neighbor without increasing the old maximum reach:

- if c belongs to b_1 union b_2, then (S_1 union S_2) adds six new first vertices to the old 45, making 51;
- if c belongs to neither b_1 nor b_2, each S_i adds six and their overlap outside the old reach set has size two, so the union adds ten, making all 55.

For the first count, the six added nine-sets contain the other four-label but omit c, giving binomial(6,5)=6. For the second overlap count, they contain both four-labels but omit c, giving binomial(2,1)=2.

The new union middle vertex must have at least four C-neighbors to maintain y=4/11. None is possible while keeping maximum reach at most 45/55 and holding the other edges fixed. Any new intersection edges can only add reach; they cannot repair this obstruction.

This is a precise failure of that **local monotone uncrossing operation** at a strict diagonal point. It does not rule out all global rearrangements or reweightings. The example itself has reach 9/11 and is not an original counterexample. The conclusion is that the disjoint-maximal class cannot be assumed universal via this naive degree-preserving compression.

## 5. Final five-turn disposition

The original bundled question remains unresolved after all five substantive turns. The strongest completed scopes are:

- exact evaluation and the full integer-k implication for the complete-uniform middle templates;
- the rank-two weighted incidence theorem, with sharp endpoint controls;
- cardinality-sensitive maximal-type inequalities and the symmetric threshold through |A|<=5k;
- the full asymmetric implication for pairwise-disjoint maximal neighborhoods, including laminar first-incidence families, and its quantitative deletion stability.

The fixed-template LP formulation, sharp charge relaxation, failed small cover and failed local uncrossing examples identify exact gaps rather than supplying a universal proof or a source counterexample. Arbitrary large overlapping higher-rank incidence remains unhandled. No sixth proof-search turn is taken. All claims are offered for independent review without historical novelty certification.
