# Independent reconstruction before prior verdicts

Target frozen head: `967e8e489aa4599f712d5ddcde62e591827f7e38`.

The original target is the mono-constrained statement in EMS printed pages 46–47 (physical 42–43) and EJC 29(2) (2022), P2.47, Conjecture 5.1, p.21. It quantifies over all real x,y in (0,1] and integer k>=1, with strict x+ky>1 and weak kx+y>=1. The conclusion counts distinct first vertices reachable by at least one two-edge path. The published mono definition has only the A-to-B and B-to-C lower degree bounds; the reverse bounds define a different function, psi. The diagonal x>1/3 half-reach claim is a special case. EJC p.8 gives nonnegative weighted equivalents normalized separately on the three parts. The candidate Turn 5 theorem states positive weights on finite parts and directly includes ordinary graphs.

## Reconstructed proof, without a size bound or equal-A premise

For k=1, weighted averaging of B-to-C incidence finds a C vertex whose B-neighbor weight is at least y. Its neighbor set intersects every A vertex's B-neighbor set because x+y>1. Hence its distinct reach is all A. No reverse lower degree is used.

For k>=2, negate the required conclusion: every C-reach has alpha-mass strictly less than 1/k. Distinct nonempty inclusion-maximal middle neighborhoods M_1,...,M_m cover A, because every A vertex has a B neighbor, and the finite family has maximal elements. Under the stated disjointness premise they partition A. Each nonempty middle type lies inside one unique M_i. Its group mass beta_i is at least x, since every A vertex in M_i receives all its B-neighbor mass from that group. Empty middle types may carry arbitrary positive mass and contribute only slack. Thus mx<=sum beta_i<=1.

Each M_i actually occurs as a middle neighborhood; its representative has positive C-neighbor mass at least y. One of those C neighbors reaches all M_i, so alpha(M_i)<1/k. Summing the block masses gives m>=k+1. Also each A vertex reaches C-mass at least y via any one of its B neighbors, so the gamma-weighted average C-reach is at least y. The negation makes that average strictly below 1/k. Thus y<1/k.

If m>=k+2, then kx+y<k/m+1/k<=k/(k+2)+1/k<=1. The last inequality holds for every integer k>=2, because its difference from 1 is (k-2)/(k(k+2)). The strictness remains essential at k=2, where that difference is zero. This contradicts the weak condition kx+y>=1. Consequently m=k+1.

For two blocks, the sum of the other k-1 block masses is strictly below (k-1)/k; their complement, the two-block union, has mass strictly above 1/k. Two maximal representatives therefore cannot share a C neighbor. Their C-neighborhoods are pairwise disjoint and each has gamma-mass at least y, yielding (k+1)y<=1. Together with (k+1)x<=1 this yields x+ky<=1, contradicting the strict condition. Arbitrary positive alpha, beta, gamma and unbounded finite part sizes were retained in every step. Partial reach into multiple blocks is permitted; only maximal representatives' C-neighborhoods are forced apart under the counterexample assumption.

A laminar family has disjoint distinct maximal elements: two intersecting maxima would be comparable, hence equal. This is a direct corollary; no general graph is shown to admit laminarization. The disjoint-maximal class is strictly broader than laminar families, because subsets inside one maximal block can cross.

## Exact deletion hypotheses

Delete exceptional B mass epsilon and normalize the remaining B mass. The retained A degree is at least x'=(x-epsilon)/(1-epsilon). The conditions 0<=epsilon<x<=1 make x' in (0,1] and keep the normalization denominator positive. B-to-C lower degree y is unchanged. Since k>=2 and y>0, both divisors ky and k+y-1 are positive. Direct multiplication gives exactly

- x'+ky>1 iff epsilon*ky<x+ky-1;
- kx'+y>=1 iff epsilon*(k+y-1)<=kx+y-1.

These are sufficient conditional deletion bounds, with the stated strict/weak endpoints. Their satisfaction already implies the original wedge. At kx+y=1 they permit only epsilon=0. They do not assert that any small exceptional set exists, nor that the bounds are necessary for the original conclusion. The original graph contains all remaining paths, so reach transfers monotonically. The theorem does not need Turns 3–4.

## Local uncrossing reconstruction

The ordinary graph has A the 55 nine-subsets of [11], B the 330 four-subsets, and C=[11]. Edges are actual containment A-B and membership B-C. Its A degree is 126/330=21/55, which is at least the stated lower parameter 4/11; every B has C degree 4/11. Every C reaches 45 distinct A vertices, while the number of two-edge paths per C is 2520. These distinct reach and path counts must not be substituted for each other.

For disjoint labels b_1 and b_2 of size four, the A neighborhoods have sizes 21,21, intersection 3, union 39. Equal B weights 1/330 make replacement by union and intersection preserve every A weighted degree exactly. Removing the original C edges of those two vertices leaves 328 fixed middle vertices, whose reach is still exactly the old 45 at every C. A union edge to a C label in b_1 union b_2 produces 51 reached A vertices; one to a label outside produces 55. Intersection-only additions produce 45 or 47, so cannot repair the union's increase.

The independent control enumerates all 108900 ordered pairs of four-element C-neighborhoods for the changed union and intersection vertices. Since adding further C neighbors cannot lower any reach, this also checks the optimum among all admissible reassignments having at least four neighbors. The minimum maximum reach is exactly 51/55, achieved when both changed vertices use four labels within b_1 union b_2. This strengthens the finite local obstruction check but makes no claim about global rearrangements or reweighting. The graph's original reach 9/11 is far above the half-reach target, so it is not a counterexample to the original question.

## Scope controls

Turns 3–4 use equally weighted A vertices and integer cardinality r=floor((n-1)/k); their finite first-part-size theorems are not unrestricted weighted-mass theorems. Turn 5's argument independently replaces this cardinality mechanism with a block-mass partition and covers the complete asymmetric wedge on its structural class. The original arbitrary overlapping higher-rank family remains unhandled. Finite checks do not prove the original universal conjecture or a universal support reduction. No historical novelty or paper DOI is certified here.

This reconstruction and the new exact controls were completed before reading the old review or disposition files.
