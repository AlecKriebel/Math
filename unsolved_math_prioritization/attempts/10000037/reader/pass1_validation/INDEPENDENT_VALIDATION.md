# Independent validation: opposite-quadrant subdivision construction

14 October 2026 UTC. Authored mathematical audit. This report validates the construction and constants; it does not establish novelty or a literature priority claim. The exact source scope remains the separate construction contract.

## Verdict

**PASS for a counterexample to supercritical almost-sure bond-percolation uniqueness in the contract's quasi-isometry sense.** The same example also refutes the stronger all-parameter normalization. No statement about critical percolation or every dimension is needed to refute either universal assertion: one admissible graph in dimension two suffices.

Use the nearest-neighbor square lattice, with

- A = {(x,y): x >= 1 and y >= 1};
- B = {(x,y): x <= -1 and y <= -1};
- a strong lattice edge precisely when both endpoints are in A or both endpoints are in B;
- every other lattice edge replaced by a path of exactly L = 100 edges, with all inserted vertices distinct between different paths;
- iid bond percolation on the resulting graph G at p = 19/20.

The graph is infinite, countable, connected, simple, and has maximum degree four. The following argument proves

p_c(G) <= 9/10 < 19/20,

and

P_(19/20)(N_infinity >= 2) >= 2200741829/6461571200 > 1/3.

The explicit lower bound is conservative. It is established by infinite-event arguments below, rather than inferred from the accompanying computations.

## 1. Metric and effective-model checks

Every original vertex has degree four; every inserted vertex has degree two. Distinct original edges have internally disjoint replacement paths. No loops or parallel edges are introduced.

Project each inserted vertex to a nearest original endpoint of its replacement path, resolving the unique middle tie in any fixed way; original vertices project to themselves. Write this map as f. Every edge of G has endpoint images at lattice distance at most one. Hence

d_Z2(f(u),f(v)) <= d_G(u,v).

Every vertex is at distance at most 50 from its image. A lattice path between original vertices can be lifted at a cost of at most 100 edges per lattice step. Therefore

d_G(u,v) <= 100 d_Z2(f(u),f(v)) + 100.

The map is surjective. The contract's single rough-isometry constant C = 100 works. No constant depends on the position or scale.

Under iid probability p on physical edges, declare a weak original edge effectively open exactly when all 100 constituent edges of its chain are open. Its probability is q = p^100. Strong edges have probability p. These effective states are independent because they depend on disjoint sets of physical edges. Original-vertex connectivity is exactly preserved, by expanding effective paths and by suppressing the degree-two inserted vertices in physical paths.

An infinite physical cluster cannot consist of inserted vertices in one replacement chain. Moreover, finitely many original vertices meet only finitely many inserted vertices. Thus infinite-cluster connectivity statements involving the original vertices transfer without an additional infinite-path assumption.

## 2. A complete elementary quadrant survival bound

Translate A to Q = {(x,y): x,y >= 0}. Let C be the root's finite open cluster. Every edge in the primal edge boundary of C, within Q, is closed.

Construct the finite dual graph D consisting of the dual edges crossing these primal boundary edges. Dual vertices have coordinates (i+1/2,j+1/2) with i,j >= -1. The corner (-1/2,-1/2) is never incident to an edge of D.

The following parity facts prove the needed crosscut lemma, without any assumption about a smooth or simple outer boundary:

1. Every interior dual vertex has even degree (zero, two, or four). Around the corresponding primal unit square, membership in C changes an even number of times.
2. Every boundary dual vertex on the bottom or left side has degree one if it occurs in D.
3. Along the bottom primal ray, membership begins at one because (0,0) is in C, and is eventually zero because C is finite. Thus there are an odd number of membership changes, equivalently an odd number of bottom dual endpoints.
4. Some connected component of D therefore contains an odd number of bottom endpoints. The handshaking lemma forces the total number of odd-degree vertices in that component to be even. All its other odd-degree vertices lie on the left side. Consequently that component also has an odd, and hence positive, number of left endpoints.

It follows that D contains a simple path of closed dual edges from

(a+1/2,-1/2) to (-1/2,b+1/2), for some integers a,b >= 0.

If the path has m edges, its endpoint distance is a+b+2, so m >= a+b+2 >= 2. In particular, there are at most m possible bottom starting positions for a length-m path. There are at most 4*3^(m-1) simple paths of length m from each start: at most four first steps and three subsequent nonbacktracking choices. This is deliberately loose; boundary restrictions only lower the count.

Each simple dual path crosses m distinct primal edges, so its probability of being closed is (1-s)^m for percolation parameter s. A union bound gives

P_s(the quadrant root cluster is finite)
 <= (4/3) sum_(m>=2) m [3(1-s)]^m.

At s = 9/10, write r = 3/10. Since sum_(m>=1) m r^m = r/(1-r)^2, the right side is

(4/3) [r/(1-r)^2 - r] = 102/245 < 1.

Thus the quadrant root survives with probability at least 143/245 at s = 9/10. The argument applies to reflected B as well. It proves p_c(G) <= 9/10 because G contains either unchanged quadrant. Monotonicity gives the same survival lower bound at p = 19/20.

The parity proof actually holds for every finite C containing the origin, whether connected or not. Connectedness is available for an open cluster but is not needed for this lemma.

## 3. Every connection has an all-weak bridge

Let a finite effective open path connect A to B. Stop at its first visit to B, and choose its last visit to A before that time. The segment between those two visits has no internal vertex in A or B. Every edge in that segment is therefore weak. Erasing loops produces a simple all-weak open path from A to B.

This extraction handles arbitrary excursions in the strong regions, arbitrary exits and returns to A, and loops outside the regions. It does not charge strong edges at probability q, and it does not require the whole connection to be a weak path. Loop erasure is necessary before applying a q^m estimate to a path with m edges.

Any such bridge starts at one of the boundary vertices (1,k) or (k,1), with k >= 1. The exact distance from either vertex to B is k+3. The common corner (1,1) may be counted twice in the following upper bound.

Set t = 3q. At any start, the number of simple lattice paths of length m is at most 4*3^(m-1). Therefore, for the event W that some simple all-weak open A-to-B bridge exists,

P(W)
 <= 2 sum_(k>=1) sum_(m>=k+3) 4*3^(m-1) q^m
 = (8/3) t^4/(1-t)^2, provided t < 1.

An equivalent coefficient-by-coefficient count is at most 8(m-3)3^(m-1) bridge candidates of length m >= 4. The nonduplicated boundary gives the slightly sharper expression (4/3)t^4(1+t)/(1-t)^2, but this improvement is not needed.

The strong-edge survival events in A and B and the event W depend on three pairwise disjoint sets of physical edges. They are independent. This is why the bridge probability need only be less than one; there is no need to make it smaller than a square of an unspecified survival probability.

## 4. Exact constants and the final event

The binomial inequality

(20/19)^20 = (1+1/19)^20 > 1 + 20/19 > 2

implies

q = (19/20)^100 < 1/32,

so t < 3/32. The bridge bound is increasing in t on [0,1), and at the endpoint

(8/3)(3/32)^4/(1-3/32)^2 = 27/107648 < 1/1000.

Let S_A and S_B be the events that the respective quadrant roots lie in infinite clusters using only their strong internal edges. On S_A intersect S_B intersect W^c, these two infinite clusters remain disconnected in the full graph. Consequently

P(N_infinity >= 2)
 >= P(S_A) P(S_B) P(W^c)
 >= (143/245)^2 * (107621/107648)
 = 2200741829/6461571200
 > 1/3.

This proves positive-probability nonuniqueness at a strictly supercritical parameter. It makes no assertion that N_infinity is almost surely two or that its law is restricted to 0, 1, and infinity. No transitivity result is invoked.

## 5. Reproducible checks and adversarial cases

Run `python validate_construction.py` in this directory. Python's standard library suffices. The file writes `validation_report.json`. Every check uses an explicit exception rather than `assert`, and the normal, `-O`, and `-OO` outputs were compared byte-for-byte.

The checks include:

- exact rational inequalities for the canonical constants, the contour sum, the bridge sum, and the final lower bound;
- the same weak-edge inequalities for an independently proposed conservative fallback parameter set; this is diagnostic and not needed by the proof;
- all 32,768 subsets of a 4 by 4 quadrant window containing the origin, verifying dual degree parity and the crosscut length bound, including 5,293 connected subsets;
- all square-lattice self-avoiding paths through length ten, confirming the crude branching bound;
- all allowed all-weak simple bridges through length ten, including the exact counts 6, 16, 42, 108, 284, 724, 1864 at lengths four through ten;
- 1,001 deterministic or fixed-seed adversarial walks, including strong excursions, returns to A, loops, and visits beyond the first B;
- all 128 open/closed assignments of a small square with one strong edge and three length-two weak chains, checking original-vertex connectivity equivalence;
- a finite canonical L = 100 graph with 3,193 vertices and 3,208 physical edges, checking simplicity, degree four, all 625 original-vertex metric pairs, and the nearest-endpoint projection on every edge.

The finite checks are implementation sanity checks, not proofs about infinite events. The infinite arguments are Sections 1–4 above.

Important rejected shortcuts:

- Replacing “all constituent edges open” by “at least one constituent edge open” gives the wrong effective probability.
- A non-simple walk cannot be assigned q raised to its length unless repeated edges are removed.
- Bounding only a particular direct corridor misses arbitrary strong excursions; the last-A/first-B extraction is essential.
- Parallel half-planes have infinitely many boundary starts at the same fixed distance. This summability argument does not apply there.
- A survival proof only at the target parameter proves p_c <= p, not p_c < p. The distinct p0 = 9/10 is essential.
- Uniformly bounded subdivision lengths are essential to the stated metric constants; allowing lengths to grow with position is a different graph.

## 6. Scope limits

This report establishes a mathematical counterexample under the supplied source contract. It does not establish that the construction is new, that it was not previously published, or that the source's intended terminology differs from the recovered definition. Source interpretation and independent prior-art review remain separate tasks. No copied source document, private dataset, or private coordination material is needed in this authored mathematical proof.
