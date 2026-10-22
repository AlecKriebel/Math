# Structural attempt: rainbow-triple propagation and affine pair links

Authored 2026-10-20. This is a substantive partial argument, not a solution, source review, or novelty claim. The target remains an almost-balanced four-coloring of Z/pZ with no rainbow modular four-term AP. All claims here concern p>3 unless a stronger bound is given.

## 1. Attempted propagation from a rainbow three-term AP

Normalize a rainbow three-term AP by an affine change of variable and color relabeling:

c(0)=1, c(1)=2, c(2)=3.

The two evident extensions force c(-1),c(3) to belong to {1,2,3}. One might hope to propagate this exclusion until color 4 has too few possible locations. The following theorem shows exactly why the most direct local-consistency version cannot do so, even when exact balanced cardinalities are enforced.

### Theorem: generalized arc consistency stops immediately

Let p≥17 be prime, and let n_1,...,n_4 be any prescribed balanced class sizes, summing to p, with each size floor(p/4) or ceil(p/4). Consider the constraint satisfaction problem consisting of:

- the three assignments above;
- one non-rainbow constraint for every four-term AP set;
- the exact global color-cardinality constraint |c^{-1}(i)|=n_i.

Start with all four colors allowed at every other vertex. Enforcing generalized arc consistency on each constraint separately, including the single global cardinality constraint, reaches exactly the following fixed point:

D(0)={1}, D(1)={2}, D(2)={3};
D(-1)=D(3)={1,2,3};
D(x)={1,2,3,4} at every other vertex.

Here generalized arc consistency means deleting a value only if it has no satisfying extension within one constraint, with all variables restricted to their current domains. Constraints can be revisited arbitrarily often. This is stronger than propagating only from three already assigned different colors.

### Proof

First, the only four-term AP sets containing all of 0,1,2 are {-1,0,1,2} and {0,1,2,3}. Indeed, if 0,1,2 occupy distinct index positions r,s,t in {0,1,2,3}, then r+t=2s modulo p. Since |r+t-2s|≤6<p, this holds over the integers. The three indices must therefore be consecutive, in either orientation. The two constraints delete color 4 exactly at -1 and 3.

We verify that the displayed domains are a fixed point. All non-singleton domains have size at least three. For any AP constraint and any selected allowed value at one of its variables:

- If the AP contains three seed variables, its fourth variable is -1 or 3 and every allowed value repeats a seed color.
- If it contains two seed variables and the selected value is on a non-seed variable, choose the remaining variable from the intersection of its domain with the colors already used. If three different colors are already used, a size-three domain intersects those colors; if a repetition already occurs, no choice can make the AP rainbow. If the selected variable is itself a seed, choose one free variable to repeat a seed color, possible because a size-three domain intersects the two seed colors.
- With at most one seed variable, after fixing the selected value there are at least two other non-seed variables. Their domains intersect, since each has size at least three in a four-color universe. Give them the same color. The AP is non-rainbow.

Thus every value has support in every individual AP constraint.

For the cardinality constraint, fix any allowed tested value at any vertex. Retain the three seed assignments. Assign each still-unassigned restricted vertex in {-1,3} color 1. No color has been used more than four times: color 1 has its seed, at most the tested vertex, and at most two restricted vertices; all other colors have been used at most twice. Since every n_i≥4, the assignments fit the prescribed capacities. All remaining vertices have unrestricted domains, so fill the residual capacities arbitrarily. This constructs a cardinality-supporting assignment for every allowed tested value.

Consequently no constraint can delete another value. Conversely, the two initial exclusions are compulsory, so the fixed point is exact. QED.

### Meaning and limitation

This is an obstruction for a specified proof/algorithm approach, not a coloring counterexample. The supporting assignments for different constraints need not be the same assignment. It proves that rainbow-triple extension plus any amount of individual-constraint domain filtering, even exact balance filtering, cannot refute a rainbow-free balanced coloring for any p≥17. A successful propagation proof must retain joint relations across constraints, introduce additional structural information, or branch on further assignments. The theorem does not obstruct such stronger methods.

The argument is conditional on having a rainbow three-term AP to normalize; it does not claim to prove that one exists. It shows that even granting this seed does not make the specified propagation approach succeed.

## 2. Exact affine pair-link formulation

A second attempt retains interactions between progressions rather than only unary domains.

Given disjoint subsets A,B of Z/pZ, define a simple undirected graph L(A,B) on V=Z/pZ minus (A union B). For each four-term AP containing an element u of A and an element v of B, add the edge between its other two points if both belong to V. Repeated edges are ignored.

This graph can be generated explicitly using affine maps. For each u in A, v in B, and distinct r,s in {0,1,2,3}, put

d=(v-u)/(s-r), a=u-rd.

If t,w are the other two positions, the candidate edge is {a+td,a+wd}; keep it if both endpoints are in V. This generates exactly L(A,B), and d is nonzero.

### Proposition: balanced subset-sum over connected components

Suppose A,B,C,D partition Z/pZ. There is no rainbow four-term AP if and only if every connected component of L(A,B) is wholly contained in C or wholly contained in D.

Proof. A rainbow AP is precisely an edge of L(A,B) crossing between C and D. Absence of such edges is equivalent to constancy of the C/D label on every component. QED.

In particular, for prescribed remaining cardinalities n_C,n_D, an extension of fixed A,B to a rainbow-free coloring exists if and only if a subset of the component sizes of L(A,B) sums to n_C. This is an exact global criterion, not an asymptotic theorem.

A useful sufficient lemma, if it could be established uniformly, would be:

For every disjoint A,B with cardinalities compatible with an almost-balanced four-way partition, L(A,B) has a component of size greater than ceil(p/4).

Such a component cannot lie in either remaining balanced class and would prove the target. The attempt does NOT prove this lemma. The missing step is a uniform expansion/large-component theorem for these affine pair-link graphs with arbitrary quarter-density anchors. Merely observing that the graph has many candidate edges is not a proof: internal edges and repeated edges can dominate.

### A finite warning against silently assuming connectivity

For p=23, let

A={1,11,14,15,22}, B={0,3,4,5,8,17}.

These have compatible balanced sizes 5 and 6; the remaining two classes would both have size 6. The components of L(A,B) are

{2,7,9,10,12,13,16,18,19,20,21}, and {6}.

Thus full connectivity fails even for compatible quarter-density anchors. This is not a counterexample to the large-component lemma: the component of size 11 already rules out a balanced extension. Nor does this finite example disprove an eventual connectivity assertion for sufficiently large primes. Its purpose is to separate the exact criterion from an unjustified connectivity shortcut.

## 3. Verification and stopping point

The standalone standard-library script structural/check_propagation.py verifies local arc consistency for p=17,19,23,29,31,43 by enumerating every distinct AP set and all values from its displayed domains. It also computes and checks the p=23 pair-link components above. The all-prime propagation theorem rests on the proof, not these finite checks. Exact-cardinality consistency is proved by the explicit filling argument above, rather than inferred from enumeration.

No full proof, asymptotic counterexample, or mathematical resolution is obtained. The concrete advance is a rigorous all-prime barrier to the direct local propagation strategy, together with a global component/subset-sum reformulation identifying a precise stronger statement that would suffice. Neither is claimed to be new in the literature.
