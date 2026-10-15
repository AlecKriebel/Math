# Five-edge subcubic residual-certificate classification

Authored 12 October 2026 UTC. This is a bounded second-round mathematical and computational report for the finite simple critical-edge-list-coloring problem. It does not resolve the unrestricted conjecture and makes no novelty claim. No remote repository was modified.

## 1. Setting and exact boundary

Let G be finite and simple, with actual maximum degree 3. Suppose G is not 3-edge-colorable but G−e is 3-edge-colorable for every edge e. Fix a three-color palette A. Every edge has a list of exactly three colors, and exactly five edges form the exceptional set X on which the list differs from A. Write O(e)=L(e)\A and d(e)=|O(e)|, so d(e) is 1, 2 or 3.

A strict residual certificate is a nonempty F⊆X with a proper edge coloring from its exterior lists O, such that the total residual deficit ∑(e∈X\F)d(e) is less than 3. It guarantees an L-coloring: ordinarily color G−F with three labels, uniformly permute those labels onto A, and apply the union bound to the remaining list violations. Each residual violation has probability d(e)/3. Exterior and ordinary colors are disjoint, so their colorings combine without cross-conflicts.

Failure of this sufficient criterion is not failure of list-colorability. Nor can an obstruction to all exterior sets and all ordinary colorings be treated as weaker than a true list-coloring counterexample: any full L-coloring itself supplies the exterior set and an ordinary coloring of its complement. In the critical setting the exterior set must be nonempty.

## 2. Complete finite classification of the exterior criterion

Two independently implemented exhaustive searches agree on all 72,700,180 tested cases:

- There are 20 unlabeled line-graph types of five-edge supports in finite simple graphs of maximum degree at most three.
- For each support, there are 3,635,009 generated first-occurrence-normalized ordered exterior-list families with list sizes in {1,2,3}. All exterior palettes are covered, up to the maximum possible 15 colors.
- Exactly 65 generated families fail the strict residual criterion. These reduce to 34 classes under automorphisms of the support line graph and relabeling of exterior colors.
- Every failure has support matching number two and exterior palette size at most three.
- The only sorted deficit profiles of failures are 11111 (20 generated families), 11112 (8), and 11222 (37).
- Every failing family admits exterior coloring leaving residual deficit exactly three. None has minimum residual deficit larger than three.
- For the five-cycle support, the sole failure is five identical singleton exterior lists.

The generated families are complete representatives, not a promised duplicate-free enumeration modulo all color relabelings. The 34 orbit classes, rather than the 65 raw normalized records, are the isomorphism classification. The complete support, failure and orbit records and their multiplicities were checked in the independent audit. Their raw collections are excluded from this prose edition; the aggregate conclusions are retained below.

### Why the finite normalization is complete

Process the five exterior lists in a fixed edge order. At each list, retain the names of previously encountered colors, and give all newly encountered colors the next consecutive names. If p colors have appeared and the next list has size d, choose s previously encountered colors and introduce exactly d−s new colors, where 0≤s≤min(d,p). Every original list family admits such a relabeling. Conversely, each generated list family is a genuine family with the stated sizes.

The independent count recurrence is

    N(i+1,p+d−s) += N(i,p) binom(p,s),
    N(0,0)=1, d∈{1,2,3}, 0≤s≤min(d,p).

The totals after 1 through 5 lists are 3, 36, 960, 46,611, and 3,635,009. There is no arbitrary palette cutoff: fifteen is the maximum total number of list entries.

### Why the support classification is complete

The first generator examines all 1,024 labeled graphs on five vertices, keeps one representative under all 120 vertex permutations, and tests for an edge partition into cliques of size two or three such that every vertex belongs to at most two cliques. Unused incidence slots get private endpoint vertices. This is exactly a construction of a simple subcubic graph whose line graph is the prescribed graph. Its completeness follows directly from the original endpoints of any simple subcubic support: each endpoint induces a clique of incident edges of size at most three, each support edge has two endpoints, and two different support edges share at most one endpoint.

The independent verifier instead enumerates restricted-growth strings for the ten ordered endpoints of five edges. It disallows loops, repeated edges, and endpoint multiplicity greater than three. All 18,745 accepted endpoint partitions produce exactly the same 20 line-graph types. Each stored reconstructed support is also checked directly.

### Independent decision methods

The first author decision method searches partial exterior colorings, choosing a minimum-remaining-options edge and allowing skipped edges only within residual budget two.

The second author decision method instead enumerates every possible omitted edge subset of total deficit at most two, then checks proper exterior colorings of its complement in fixed edge order. Its list-family generator is separately written. It obtains exactly the same per-support failure counts and writes all 65 failures.

A third author method checks every recorded failure. It processes exterior colors one at a time, enumerates their independent edge subsets, and dynamically tracks all covered-edge subsets. Coverage determines a proper partial coloring: if an edge appears in more than one color class, discard all but one of its memberships. This third method proves that each recorded minimum residual is exactly three.

All searches completed without a timeout. A search cutoff is never interpreted as an impossibility certificate. These finite computational conclusions depend on the audited enumeration and exact decision implementations. Executable programs and raw support, failure and orbit collections are excluded from this prose edition, so those calculations cannot be rerun or the omitted records reconstructed from the prose alone. The reported classification is not claimed as a replacement for a short symbolic case classification.

## 3. Exact Hall failures at total residual deficit three

Fix F and an ordinary coloring φ of G−F. A permutation of its three labels into A respects all residual lists precisely when the allowable images of the labels have distinct representatives.

### Three residual unit deficits

Let residual edges e1,e2,e3 have labels i1,i2,i3 and omitted A-colors a1,a2,a3. No palette permutation works if and only if one of these two alternatives holds:

1. All three ordinary labels agree and the three omitted colors are distinct.
2. The three ordinary labels are distinct and all three omitted colors agree.

Proof. Each bad event π(ij)=aj contains two of the six permutations. Their union is all six exactly when the three events are pairwise disjoint. Two events are disjoint precisely when their constraints are in a common row with different columns, or a common column with different rows, of the three-by-three permutation matrix. Three pairwise-disjoint single-entry events must therefore be one full row or one full column. This yields precisely the two alternatives. ∎

Every one of the 3^6=729 label/omission combinations was independently checked against all six permutations; 36 fail, exactly as characterized.

### Residual deficits two and one

Let e have deficit two and sole permitted A-color a, and let f have deficit one and omitted A-color b. A palette permutation fails if and only if φ(e)=φ(f) and a=b.

If the labels agree, their common image must be a and must differ from b. If the labels differ, assign a to the label of e; among the two remaining colors at least one differs from b, and can be assigned to the label of f. This proves the claim. In particular, an incident residual pair always permits completion, regardless of its interior list choices. All 81 label/color cases were checked, with exactly nine failures.

### A useful elimination among the exterior obstructions

Of the sixteen obstruction classes with deficit profile 11222, fourteen admit an exterior coloring leaving an incident residual pair of deficits two and one. The preceding Hall argument therefore overcomes those fourteen classes for every interior list choice and every critical supergraph containing the support.

The two remaining classes have a line graph consisting of a disjoint triangle and single edge. The three pairwise-incident edges have one common two-color exterior list, and the other two incident edges have one common singleton exterior list. That singleton color may belong to the two-color list or may lie outside it. There are no incidences between these two support parts. These are two distinct support/color orbits, distinguished by whether the singleton exterior color belongs to the common two-color exterior list. Here the disjoint triangle and single edge describe the line graph; the original three pairwise-incident support edges may instead form a three-edge star. The present packet makes no assertion that these two remaining classes yield uncolorable assignments.

## 4. Smallest strict-method obstruction and a one-step Kempe repair

Consider the graph with ordered edges

    e0=04, e1=41, e2=02, e3=03, e4=12, e5=13, e6=23.

It is K4 with one edge subdivided once. It has five vertices and seven edges; every matching has size at most two, so it is not 3-edge-colorable. Its criticality can be checked explicitly. Swapping vertices 0 and 1 and swapping vertices 2 and 3 partition the edges into three deletion types. The following partitions into three matchings give ordinary three-edge-colorings for representatives:

- Delete 04: {41,23}, {03,12}, {02,13}.
- Delete 02: {04,13}, {41,23}, {03,12}.
- Delete 23: {04,13}, {41,02}, {03,12}.

These automorphisms cover all seven edge deletions. This familiar critical graph is a test fixture, not a newly established case of the conjecture.

Put A={0,1,2}, X={e0,e1,e3,e4,e6}, and give every edge of X the list B={0,1,3}. Give the other two edges A. The support X is a five-cycle, and every exterior list is {3}. Thus every exterior-colored set is a matching of size at most two. At least three unit deficits remain, so no strict residual certificate exists. This is smallest by exceptional support size in degree three, because the accepted four-exception argument always supplies a strict residual certificate in that degree.

Take F={e3,e4}, colored exteriorly with 3, and use the ordinary coloring

    φ(e0)=0, φ(e1)=1, φ(e2)=1, φ(e5)=0, φ(e6)=2.

The three residual exceptional edges have three distinct ordinary labels and all forbid A-color 2. No permutation completes this particular coloring.

However, the (0,2)-Kempe component containing e0 consists only of e0. Swap its color from 0 to 2, then relabel ordinary colors by π(0)=2, π(1)=0, π(2)=1. The final full coloring, in edge order, is

    (1,0,0,3,3,2,1).

Every color belongs to its edge's list and all incident edges differ. The verifier independently checks the original failure, the exact Kempe component, the switched ordinary coloring, and the completed list coloring. Thus this explicit method obstruction is repaired by a single Kempe change, with the exterior set held fixed.

## 5. Remaining scope

This packet isolates the five-edge subcubic strict-certificate frontier and records exact equality-Hall tests. It does not show that every remaining obstruction class is colorable on every critical supergraph. It does not establish a five-arbitrary-exception theorem for all supports or degrees. In particular, failure of a selected ordinary coloring, or failure of the strict numerical certificate for every exterior subset, must never be reported as a counterexample to the target list-coloring conjecture.

## Companion mathematical results

The complete symbolic five-cycle theorem and the varying-omission five-substitution theorem are in FIVE_CYCLE.md, with their separate independent acceptance in AUDIT_FIVE_CYCLE.md. They are not consequences of the finite classification alone. The first-round four-exception proof is in [FOUR_EXCEPTIONS.md](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md).
