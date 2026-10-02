# Turn 3: an exact abstract square/cube separation

Problem30003973 remains unresolved. This third turn follows the failed formal approach from Turn2 and finds a genuine obstruction to that *abstract* approach: equal squares of downward-closed families need not have equal cubes. The example does not satisfy the single-forbidden-graph structure required by the Ramsey problem, and it is not presented as a graph counterexample.

## 1. Explicit seven-element certificate

Work on U={0,1,2,3,4,5,6}. Encode a subset by the sum of2^i over its elements. Define A and B as the downward closures of the following lists of maximal sets, called facets:

    A: 7,9,10,18,20,24,33,36,65,76,96
    B: 3,14,17,20,34,36,40,66,69,72,80.

For example,7={0,1,2},14={1,2,3},69={0,2,6}. Both families contain all singletons and the empty set. Their sizes are both25.

With family multiplication defined as all unions, their squares agree. The common square D has102 members and the following19 facets:

    31,43,46,51,53,54,57,60,79,83,85,89,94,103,106,109,114,116,120.

The certificate file TURN_3_CERTIFICATE.json supplies, for each of these19 facets, an exact A-pair and B-pair whose union is that facet. To check equality of the squares, it remains only to verify that each of the121 facet-pair unions from each family is contained in at least one listed D-facet. Downward closure then gives both inclusions. The portable checker performs these finite integer/set checks and also independently expands all family members and all pairwise unions.

Nevertheless,

    A³ = 2^U,             B³ = 2^U \ {U}.

For A the partition with masks7,24,96 belongs to A and covers U, proving A³=2^U. The checker verifies that B³ has as facets the seven six-element sets63,95,111,119,123,125,126, and omits U. Thus the cube difference is exactly one subset.

## 2. A short direct reason B has no three-set cover

The only B-facets of size3 are T={1,2,3} (mask14) and T'={0,2,6} (mask69); all others have size2. Any three B-members can be enlarged to facets, so it suffices to consider three facets.

If none is a triple, their union has at most six elements. If both distinct triples are used, their union omits{4,5}; no B-member contains that pair (mask48), so a third member cannot finish the cover.

Suppose just T is the distinct triple used. Its complement is{0,4,5,6}. Within this complement, the allowed B-pairs form the triangle on{0,4,6}; element5 is isolated. Two B-pairs cannot cover the four-element complement: a pair containing5 covers at most one point of that complement, and the other pair covers at most two. Reusing T contributes nothing to its complement. Hence a cover is impossible. For T', the complementary set is{1,3,4,5}; its allowed pairs form the triangle on{1,3,5}, with4 isolated, giving the same argument.

On the other hand, B has the four-set cover with masks14,17,32,64. Therefore the minimum covering numbers of U by A-members and B-members are exactly3 and4. Their common square omits U, so neither has a two-set cover.

This supplies a fully exact finite obstruction to a general inference A²=B²⇒A³=B³. The earlier bounded scan through five ground elements could not justify that inference.

## 3. Why this is not a Ramsey-equivalent graph pair

Fix a finite host graph G with its edge set as the ground set. For a *single* target graph H with e≥1 edges, define the H-avoiding family to consist of those edge subsets whose spanning subgraph contains no ordinary H. If any copy of H exists in G, every minimal forbidden edge subset has exactly e elements:

- Any forbidden subset contains the edge set of an H-copy, which has e edges
- Minimality forces equality with such a copy edge set
- A proper subset of those e edges has fewer than e edges and cannot contain H

If H has isolated vertices, the same statement holds whenever the fixed host has enough vertices for a copy; otherwise the avoiding family is the full power set and has no minimal forbidden subsets. Turn1 already allows removal of isolated targets when searching for a genuine counterexample.

The minimal nonfaces of the constructed families have mixed cardinalities. For A, mask17={0,4} is a minimal forbidden pair, whereas mask11={0,1,3} is a minimal forbidden triple; all its pairs lie in A. For B, mask9={0,3} is a minimal forbidden pair, whereas mask7={0,1,2} is a minimal forbidden triple. These four claims can also be read directly from the facet lists.

Consequently neither A nor B can be exactly the edge-avoidance family of a single fixed graph target on any finite host edge set. Relabeling the ground set does not remove the different forbidden cardinalities. In addition, a true Ramsey-equivalence counterexample would need equal squares uniformly over *all* finite host graphs, not merely a chosen ground set. These are two independent obstacles to promoting this certificate to a resolution of the source question.

## 4. Search and validation scope

An integer-programming formulation using SciPy/HiGHS was used only to find candidate facet lists. The final certificate requires no numerical tolerance, optimizer or SciPy installation: verify_turn3.py uses standard-library exact integer/set operations. The final claim does not rely on the optimizer's status messages.

Exploratory infeasibility at ground size6 is not promoted to a minimality theorem because no standalone exact infeasibility certificate was retained. This turn claims an example of size7, not optimality of7. A simple general lower bound is still available: if A²=B², both contain every singleton, and U∈A³\B³, then in any disjoint A-three-cover each part has size at least2. Otherwise the union of the other two parts lies in B², and the singleton or empty remaining part lies in B, yielding U∈B³. Thus such an example has at least six ground elements.

## 5. Remaining work

The purely formal square-root route is blocked by an exact counterexample. A positive Ramsey theorem must use more of graph-copy avoidance than arbitrary downward closure. A negative Ramsey construction would have to replace this certificate by uniform minimal-nonface systems that arise from copies of single graphs, and also establish the uniform all-host two-color equality.

No source counterexample, universal2-equivalence certificate, or complete proof has been obtained. Completion estimate for the original problem remains15%; the obstruction is useful route elimination rather than a full target advance. Two substantive author turns remain after this checkpoint.
