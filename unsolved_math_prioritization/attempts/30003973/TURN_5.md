# Turn 5: a minimal non-star host separates the restricted-profile collision

Problem30003973 remains **unresolved after five substantive author turns**. This final turn tests the concrete collision from Turn4 beyond star-forest hosts. It gives an explicit53-vertex,45-edge Ramsey-minimal separator in two colors. It therefore disproves the tempting inference from equality on every star-forest host to universal Ramsey equivalence. It is not a counterexample to2-equivalence implying3-equivalence, because the two targets are already separated in two colors.

## 1. The two targets agree on all star-forest hosts, in every q≥2

Let

    H = K_(1,5) ⊔ K_(1,4) ⊔ K_(1,2) ⊔ K_(1,2) ⊔ K_2,
    H'= K_(1,5) ⊔ K_(1,4) ⊔ K_(1,3) ⊔ K_(1,2) ⊔ K_2.

Their edge counts are14 and15, and their vertex counts19 and20. They are nested, H⊂H', and both have five nontrivial components and no isolated vertices.

Their sequences a_i=k_(i+1)−1 are respectively(4,3,1,1,0) and(4,3,2,1,0). The second sequence is exactly4−i; the first agrees with it except at i=2, where it is one lower. Hence its q-fold max-plus convolution at j is at most4q−j, with equality whenever j is a sum of q members of S={0,1,3,4}.

Now S+S is the full integer interval{0,...,8}. If qS={0,...,4q} for q≥2, then(q+1)S contains both{0,...,4q} and{4,...,4q+4}, by adding0 and4; their union is{0,...,4q+4}. The reverse containment follows from S⊆[0,4]. Thus qS is the full interval for every q≥2.

By the exact canonical-host theorem from Turn4, both targets therefore have the same canonical star-forest q-Ramsey host, with component sizes

    4q+1,4q,...,2,1.

Consequently they have identical Ramsey behavior on **every star-forest host**, simultaneously for all q≥2. This is an all-size statement, not a bounded scan.

## 2. Extending the threshold test to triangle components

For this section there are exactly two edge colors. Let the target be any isolate-free star forest K with component-size counting function τ_K(t). Let the host be a disjoint union of stars and z triangles. Write N_*(d) for the number of its star components having at least d edges; triangles are not included in N_*.

A monochromatic subgraph of a triangle can supply at most one nontrivial star-forest target component. Its capacity is2 when it has at least two edges of that color,1 when it has one edge, and0 otherwise. The possible red/blue capacity pairs of a colored triangle are

    (2,0), (2,1), (1,2), (0,2).

Thus a triangle is forced to cross at least one of the selected thresholds u,v exactly when u≤2 and v≤2. In that case it can be made to cross only either chosen color's threshold by coloring it monochromatically. If u≥3, color it all red to stay below both thresholds; if v≥3, all blue does the same.

The quota argument of Turn4 therefore gives the exact criterion

    G→_2 K  iff
    N_*(u+v−1)+z·1_(u≤2 and v≤2) ≥ τ_K(u)+τ_K(v)−1        (1)

for every u,v among the distinct component sizes of K.

For completeness, if a coloring avoids K, choose a deficient threshold in each color. Every forced star or triangle must spend at least one of the total τ_K(u)+τ_K(v)−2 available large-color-component quotas, so failure of(1) is necessary. Conversely, if(1) fails, assign the forced components to the two colors within those quotas. A forced star can be colored with only its assigned color crossing, exactly as in Turn4; a forced triangle can be monochromatic in its assigned color. Every unforced component has an explicitly described coloring below both thresholds. These independent component choices yield an avoiding coloring. No general graph is being approximated by its degree sequence: the component type is retained throughout.

## 3. A genuine two-color separating host

Take G to be the disjoint union of stars with sizes

    9,8,7,6,5,4,2,1

and one triangle. This replaces the size3 star in the common two-color canonical host by a triangle. It has53 vertices,45 edges and nine components.

For H the threshold set is{1,2,4,5}, with

    τ_H(1)=5, τ_H(2)=4, τ_H(4)=2, τ_H(5)=1.

For the ten unordered threshold pairs(u,v), the left side of(1) and the required right side are equal, as follows:

    (1,1):9; (1,2):8; (1,4):6; (1,5):5; (2,2):7;
    (2,4):5; (2,5):4; (4,4):3; (4,5):2; (5,5):1.

Hence G→_2 H by the exact criterion, covering all2^45 edge colorings without enumerating them.

On the other hand G↛_2 H'. Color the size9 and8 stars red; the size7,6,5,4 stars blue; and the size2 and1 stars and triangle red. In red the available nontrivial component capacities are(9,8,2,2,1), which cannot supply H' because its third-largest required capacity is3. In blue there are only four nontrivial components, while H' requires five. A single monochromatic host star or triangle cannot contain two vertex-disjoint nontrivial target components, so these capacity failures are rigorous noncontainment certificates. Thus H and H' are not2-equivalent.

## 4. The separator is Ramsey-minimal for H

Deleting any edge of a star of size d leaves a star of size d−1 plus an irrelevant isolated vertex; when d=1, that nontrivial component disappears. For each star size choose the following threshold pair:

    d=9:(5,5); d=8:(4,5); d=7:(4,4); d=6:(2,5);
    d=5:(1,5); d=4:(1,4); d=2:(1,2); d=1:(1,1).

In every case u+v−1=d. The relevant equality from the preceding table loses exactly one forced star after the edge deletion, so(1) fails and the remaining graph is not2-Ramsey for H.

Deleting any edge of the triangle turns it into a size2 star. At(u,v)=(2,2), the original triangle contributed one forced component, while the new size2 star contributes none because its edge count is below3. Again the inequality loses exactly one and fails.

Thus deleting any edge makes G non-Ramsey. Since G has no isolated vertices, every proper subgraph either deletes an edge or omits a vertex incident to an edge and is contained in an edge-deleted graph. Ramsey behavior is monotone in the host, so every proper subgraph is non-Ramsey. Therefore G∈M_2(H), while G∉R_2(H').

The exact certificate includes an H'-avoiding coloring of G and an H-avoiding coloring for every one of the45 single-edge deletions. These explicit colorings complement the all-colorings positive proof above.

## 5. Verification and final boundary

TURN_5_CERTIFICATE.json gives the labeled53-vertex graph, target profiles, threshold table, the displayed H'-avoiding coloring and45 deletion colorings. The standard-library checker independently reads each colored graph, reconstructs its connected monochromatic components, checks that each is a star or triangle and applies the exact capacity criterion. It also compares direct coloring enumeration with the extended threshold formula on a bounded family of small star/triangle hosts. No numerical optimization is needed for replay.

The final result is a carefully scoped failure of a proposed recognition method: even agreement on every star-forest host for every number of colors does not certify universal Ramsey equivalence. This concrete collision is excluded, rather than retained as a false counterexample.

The original unrestricted question is still open in this work. The strongest remaining sufficient condition is Turn2's mixed asymmetric Ramsey condition; it has not been proved for every universally2-equivalent pair. A counterexample must have truly universally2-equivalent, isolate-free, incomparable cores and the crossed recoloring configuration from Turn2. The abstract example from Turn3 and the restricted-host collision here meet neither full requirement. No sixth author search will be performed after this freeze. Completion estimate:20%; final disposition proposed as unsolved5/5 pending independent full review.
