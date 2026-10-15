# Six unit substitutions: a bounded method classification

Authored 12 October 2026 UTC. This is the complementary accepted method analysis in the fourth research round. Its complete independent audit is distributed as [AUDIT_METHODS.md](AUDIT_METHODS.md). The conclusions concern sufficient methods and their exact limitations, not a counterexample to the full critical-edge-list-coloring conjecture. No novelty claim is made.

## 1. Setting and scope

Let G be finite, simple, and of maximum degree three. Assume G is not ordinarily three-edge-colorable but G−e is for every edge e. Fix a three-color palette A. Exactly six edges X have exceptional lists; all other lists equal A. Here every exception is a one-color substitution:

    L(e)=(A\{a_e})∪{x_e}, with a_e∈A and x_e∉A.

The main computation treats nonconstant omission patterns, meaning the six a_e are not all equal. The exterior colors x_e may coincide arbitrarily. Uniform omission patterns are discussed separately below.

Three sufficient methods are classified, in this order:

1. Strict deficit: exterior-color at least four exceptional edges, leaving at most two unit deficits.
2. Universal three-residual Hall completion: exterior-color three edges F such that every ordinary coloring of the three residual exceptional edges admits a compatible global palette permutation.
3. Deletion-adaptive palette repair: choose an exceptional edge e so that every proper ordinary coloring of the support X−e can be repaired by selecting an exterior set containing e and globally permuting the retained ordinary colors.

A positive local certificate from any of these methods proves colorability on every critical supergraph containing the support. Failure of all three only describes their limitations.

## 2. The deletion-adaptive method and its quantifiers

Fix e∈X and an ordinary coloring φ of G−e. For a permutation π of its three labels onto A, define

    F(e,φ,π)={e}∪{f∈X\{e}:π(φ(f))=a_f}.

These are exactly the edges that must use their exterior colors if the ordinary coloring and permutation are retained elsewhere. The resulting full coloring works if and only if the prescribed exterior colors x_f properly color F. Adding further edges to F cannot repair a conflict already present in this required set.

Let H be the six-vertex support line graph. Thus a graph-order-independent sufficient statement is

    there exists e such that, for every proper three-coloring φ of H−e,
    some permutation π makes F(e,φ,π) exterior-colorable.

Choose that e in G, take the promised ordinary coloring of G−e, and apply the local statement to its restriction. The exterior and base palettes are disjoint, so the two pieces combine properly.

A failed local statement has the opposite quantifiers: for every e there is some local ordinary coloring blocking every permutation. It does not say that all ordinary colorings fail, that those local witnesses all occur in one critical graph, or that the lists themselves are bad.

An additional distinction is essential. Even failure for every ordinary coloring of a particular G−e does not imply that e cannot receive its exterior color in a full list coloring. A full list coloring supplies an ordinary A-coloring of G−F, but that partial coloring need not extend to an ordinary coloring of G−e. Section 6 gives an explicit example and records the failed extension directly.

## 3. Finite normalization and coverage

There are 47 unlabeled line-graph types of six-edge supports in simple subcubic graphs. The first construction examines all 156 unlabeled graphs on six vertices and checks an endpoint-clique representation: graph edges are partitioned into cliques of sizes two or three, with each support vertex in at most two cliques. Empty endpoint slots receive private endpoints. This represents exactly simple subcubic original supports.

A separate endpoint-partition enumeration considers all restricted-growth labelings of twelve ordered edge endpoints, rejecting loops, repeated edges, and vertex multiplicities above three. Its 508,285 admissible endpoint partitions produce 9,463 distinct labeled line graphs, exactly the permutation orbits of the same 47 representatives.

Since every exterior list is a singleton, its complete color-equality information is a set partition of six positions. There are Bell(6)=203 such partitions. No arbitrary exterior palette cutoff is used; at most six exterior colors can occur.

The omissions are a partition of six positions into at most three blocks. There are S(6,1)+S(6,2)+S(6,3)=1+31+90=122 patterns up to relabeling A. Removing the constant pattern leaves 121. Thus the exhaustive normalized domain has

    47×203×121 = 1,154,461 cases.

For a three-edge residual set R, universal Hall completion holds precisely when its omitted colors use exactly two values, or when they use three values and R contains an incident pair. This follows from the exact three-unit equality classification: a selected ordinary coloring fails only when all three labels agree and omissions are distinct, or when labels are distinct and omissions agree. If omissions are constant, assigning three distinct labels is always a local obstruction. If omissions are distinct and R is a matching, assigning one label to all three is a local obstruction.

Two separately written programs agree on every aggregate count and every remaining obstruction. The second program enumerates all proper residual colorings and all permutations directly, rather than using this Hall classification. It also enumerates all labeled ordinary deletion colorings, rather than the first program's color-normalized ones.

The disjoint phase counts are:

- Strict deficit: 1,095,050 cases
- Universal three-residual Hall completion: 56,674 additional cases
- Deletion-adaptive repair: 2,725 additional cases
- Not settled by these three methods: 12 normalized cases

All searches completed. There is no timeout interpreted as impossibility.

## 4. Exact remaining support patterns

Every one of the 12 remaining cases has one common exterior color. Four are equivalent under support automorphisms and occur on K4. That support cannot occur in a graph satisfying the critical hypotheses: its vertices are saturated, so it is an isolated edge-containing component, and K4 itself is ordinarily three-edge-colorable. A critical graph has exactly one edge-containing component.

The remaining eight patterns lie on seven support types:

- C6: two patterns
- C5 with one pendant edge
- C4 with pendant edges at two adjacent cycle vertices
- A triangle with one pendant edge at each vertex
- C4 with pendant edges at two opposite cycle vertices
- The theta graph with path lengths 1, 2, and 3 between its two degree-three vertices
- A diamond with a pendant edge at one degree-two vertex

The C6 patterns are particularly simple. In cyclic edge order, the omissions either alternate two colors, or repeat three colors twice. Both have the same sole exterior color on all six edges.

The author-generated verification records contain all 12 patterns and, for every deleted support edge, an explicit ordinary coloring blocking all six permutations. Their symmetry reduction gives nine support/color orbits, one of which is the impossible K4 case. Every witness was independently checked for propriety and every claimed permutation conflict was checked. The raw pattern, orbit and witness collections are excluded from this prose edition; their finite classification is reported with aggregate verification, not as a rerunnable certificate collection.

This is a method classification. It is not a classification of bad assignments, and none of these patterns is asserted uncolorable.

## 5. Uniform omissions and the small structural frontier

For comparison, suppose all omissions equal a. If an exceptional edge e has at most two exceptional neighbors, ordinarily color G−e, choose a label t absent from those neighbors, and exterior-color e together with all other exceptional edges of label t. They form a matching. Map t to a; every residual exception receives a permitted base color. This works for any number of exceptions and for arbitrary exterior singleton colors.

For six edges, if no exceptional edge has at most two exceptional neighbors, every support vertex has degree two or three, and the degree-two vertices are independent. An edge with an endpoint of degree one, or with two degree-two endpoints, would have at most two exceptional neighbors.

Let n2,n3 count the support vertices of degrees two and three. Then 2n2+3n3=12. The degree-two vertices are independent. The all-degree-two possibility is excluded; the remaining possibilities are n3=2,n2=3, giving K2,3, or n3=4,n2=0, giving K4. The latter cannot occur in a critical supergraph as noted above.

Uniform omissions on K2,3 also admit a direct boundary construction. Its three degree-two vertices have at most one boundary edge each. Pad missing boundary labels arbitrarily and call the three labels q1,q2,q3. Choose a most frequent label and globally map it to the omitted base color a. The retained boundary colors then occur at most once each. Temporarily identify all exterior colors as x and put B=(A\{a})∪{x}.

Prescribe the missing B-color at every leaf whose boundary color lies in B to equal that boundary color. Complete these prescriptions to three different missing colors m1,m2,m3, a permutation of B. In a cyclic ordering of B, color one three-edge star by the successors of m_i and the other by their predecessors. Both stars use all three colors, the two colors at each leaf differ, and the boundary is respected. Finally restore each x-colored edge's actual exterior color; those edges form a matching. All 27 boundary words are explicitly checked.

This closes the six-edge uniform-omission case, but it does not remove the variable-omission method obstructions in Section 4. The separate accepted shared-two-color theorem in [THEOREM.md](THEOREM.md) applies beyond this six-edge setting. That stronger theorem is not needed for this method classification, and its proof does not depend on the classification.

## 6. Actual critical graphs distinguish the methods

All eight non-K4 patterns are realized as exceptional supports in the first three previously verified small critical fixtures. The present certificate rechecks criticality independently: their seven or ten edges exceed three times the maximum matching size on five or seven vertices, and explicit ordinary colorings after every edge deletion are verified.

Each realized pattern has a selected ordinary deletion coloring blocking every palette repair. Two of those selected colorings become repairable after one explicit Kempe-component switch. In the other six examples, **every** ordinary coloring of the selected G−e blocks deletion-derived palette repair. The author-generated certificate collection contains all those ordinary colorings and a conflicting exterior-edge pair for every permutation; it was independently checked by Cartesian enumeration. That raw collection is excluded from this prose edition. The explicit small example below preserves a complete symbolic demonstration of the same distinction.

Nevertheless, all eight assignments have explicit proper full list colorings, including colorings in which the selected edge e receives the common exterior color. Thus none is an obstruction to that precoloring request, much less a counterexample to the conjecture.

### Explicit small example

Use the ordered edges

    e0=01, e1=02, e2=13, e3=14, e4=23, e5=24, e6=34.

This is K4 with one edge subdivided once. Put A={0,1,2}. Give e0,e2,e4 the list {1,2,3}; give e1,e3,e6 the list {0,2,3}; and give e5 the list A. There are six one-color exceptions, all with exterior color 3.

Delete e1. Up to relabeling, the unique ordinary coloring of G−e1 is

    (e0,e2,e3,e4,e5,e6)=(0,1,2,2,1,0).

To see uniqueness, color e6 with 0. Its endpoints force the pairs e2,e4 and e3,e5 to use 1,2; the incidence of e2,e3 forces opposite choices, and e0 must then use 0. All six labeled colorings were independently checked; the raw collection is not distributed here.

Suppose a palette permutation π could be repaired by exterior-coloring a set containing e1. Edges e0 and e4 meet e1 and cannot also be exterior; since both omit 0, this forces π(0)≠0 and π(2)≠0, hence π(1)=0. Edge e2 therefore violates its list and must be exterior. If π(0)=1, edge e6 must also be exterior and meets e2. If π(2)=1, edge e3 must also be exterior and meets e2. These exhaust the two remaining choices, so every deletion-derived palette repair fails.

But the full color sequence

    (e0,e1,e2,e3,e4,e5,e6)=(1,3,2,0,1,2,3)

is a proper list coloring, with e1 exterior as requested. Its exterior set is F={e1,e6}. The remaining A-coloring on G−F cannot extend to G−e1: to restore e6=34, the ordinary color missing at vertex 3 is 0, whereas the ordinary color missing at vertex 4 is 1. There is no common available ordinary color.

This supplies an explicit certificate of the missing extension property. Searching harder among ordinary colorings of G−e1 cannot find this completion, even though a suitable ordinary coloring of G−F exists.

## 7. Correction history and precise stopping point

A stronger inference was considered during verification and rejected: failure of every deletion-derived repair was initially treated as if it implied that the selected edge could not receive the exterior color in any full coloring. That implication is false. The counterexample above and the positive selected-edge-exterior colorings for all eight cases explicitly disprove it. The corrected scope is retained throughout the accepted proof, independent audit and [explicit correction](SCOPE_CORRECTION.md).

The completed outcome is a finite, independently verified six-unit method classification and actual critical-graph examples showing where deletion-derived palette repair loses solutions. The remaining mathematical question is how to select and color G−F without assuming its coloring extends to a preselected G−e, or how to prove the remaining cases directly. No claim is made that six arbitrary exceptional lists, or even every six-unit pattern, have been settled by these methods.
