Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Independent proof and implementation review

Row 1754 / problem 3276. Fourth substantive pass, 12 October 2026 UTC.

This review concerns the exact candidate manifest `[verified undistributed artifact identity]` and search source `[verified undistributed artifact identity]`. It does not independently recertify the entire cited paper, establish an unrestricted conjecture, or assert novelty.

## Primary hypotheses and credited reduction

The independently inspected primary source is Agelos Georgakopoulos and Philipp Sprüssel, *On 3-coloured tournaments*, [arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2). The arXiv version marker is 17 April 2009; the recovered PDF also prints 16 November 2018 on its title page. These are recorded separately rather than silently conflated. The recovered PDF and text hashes were independently matched, and PDF pages 3–5 were freshly extracted. No scholarly source text or PDF is redistributed in this audit.

Conjecture 1.2 is about a directed cyclic rainbow triangle or an outgoing monochromatic source. The path color may depend on its destination. A rainbow transitive triple is not the forbidden configuration. Section 2 explicitly fixes an induced-minimal counterexample to that general conjecture. It does not impose the later special condition that each vertex misses a color.

Lemma 2.1, credited to Shen, gives a directed Hamilton cycle such that each vertex fails monochromatic reachability exactly to its predecessor. Proposition 2.4, under those section-wide hypotheses, excludes a vertex whose incoming edges all have one color, and also excludes the outgoing analogue. The Hamilton cycle supplies an incoming and an outgoing edge at every vertex, so there is no empty-set ambiguity: at least two distinct colors occur in each direction. Theorem 3.1 explicitly concerns a minimal counterexample to Conjecture 1.2 and requires every vertex to meet all three colors. Thus both incidence requirements apply to the candidate's reduced minimal-counterexample class.

Lemma 2.5 requires a monochromatic path from the first to last vertex inside every proper forward cycle interval. Its following warning matters: an arbitrary globally reachable color need not have an interval-local witness. The implementation does not assume that it does. An independent reconstruction of the lemma is short: the proper induced interval has some monochromatic source by minimality; every vertex except its first has its forbidden predecessor inside the interval, so only the first can serve as the source.

## Actual-state invariant

At every search state, fix any genuine reduced completion compatible with the assigned actual arcs and all stored colored reachability assertions. Each actual assignment must agree with that completion. Each stored reachability assertion must be realized by a positive-length same-colored path in it. This invariant supports all deductions below.

An unordered chord has six possible values, covering both directions and all three colors. The `add` function rejects exactly when the new actual arc closes an actual directed rainbow triangle, or when its colored transitive closure acquires a forbidden predecessor pair. The triangle test reads only `arc`; it does not interpret virtual reachability as edges. Rejected additions modify neither actual assignments nor relation entries.

For a transitive relation, adding one link `u -> v` gives its old closure union the Cartesian product of old ancestors of `u` (including `u`) and old descendants of `v` (including `v`). Repeated occurrences of the new link in a walk do not create additional endpoint pairs: the prefix before its first occurrence and suffix after its last are already in the two endpoint sets. This remains correct when the link creates a positive cycle. The separate Warshall implementation recomputes the same positive-length closure after insertion. No blanket reflexivity convention is inserted.

## New incidence filter

For each currently unassigned pair, the initial domain contains every value passing `add`. Every actual pair value from a compatible genuine completion passes that test, so these domains overapproximate compatible completions.

At each vertex, the filter forms the union of possible incoming color categories and the union of possible outgoing categories. It requires their combined union to contain all three colors, and each directional union to have at least two colors. These unions are deliberately a necessary relaxation. Different possible categories might require incompatible choices for the same edge; the code does not assert joint realizability.

To test a value `q` on pair `{u,v}`, the implementation removes the entire contribution of that pair's current domain, adds only `q`, tests both endpoints, removes `q`, then restores the retained domain. An oriented color contributes once to its tail's outgoing category and once to its head's incoming category. Contributions are per pair and category, not per path. The six-valued encoding makes direction/color alternatives on the same pair explicit. The fresh code diff has been inspected in full; in particular, testing one candidate does not leave its incompatible alternatives in the support counts.

For the preservation proof, take the pair value from any compatible full model. After replacing the domain by that value, every other actual incident edge in that model is still represented by its own domain or fixed arc. Each required color in the actual model therefore remains in the relevant possible-color set. Neither endpoint test can reject that value. Induction over the sequential deletions proves that no model value is removed and no domain is emptied while such a model exists. Infeasible alternatives may survive because union support is weaker than realizability; this weakens pruning and does not imperil exclusion soundness.

Every successful changing sweep removes at least one of finitely many values, so filtering terminates. Within the current invariant, support counts are nonnegative. Fixed actual arcs and unassigned pair domains are disjoint, and domain masks contain no repeated value. Virtual relations are never read by `filter_incidence`. The independent domain harness explicitly varies arbitrary virtual relations without changing its expected output.

## Interaction with proper intervals

The candidate rebuilds each possible actual-edge graph from fixed actual arcs and the incidence-filtered domains. For a required interval `xCy`, each compatible completion supplies an actual path in at least one color. Its edges survive domain filtering, so that color has a path in the possible graph restricted to the interval. Adding its true global endpoint relation cannot generate forbidden predecessor reachability in a genuine completion. Consequently at least one feasible color survives the two tests.

If only one color survives, every compatible completion must realize that colored endpoint relation. Storing and closing that virtual relation preserves the invariant. If none survives, no compatible completion exists. The possible graph can become stale after a virtual relation is added during one sweep. Its old domains remain supersets of compatible values, so staleness can only miss deductions. The graph is recomputed on a restart.

Forced singleton domains are committed as actual arcs. Every outer propagation restart adds an actual chord or a previously missing relation entry. There are finitely many of both. Domain recomputation may restore previously removed relaxed values, but it does not affect this strict finite measure. If no new commitment occurs, propagation returns a branch domain instead of restarting.

At a completed leaf the incidence check uses only fixed actual arcs, the possible graph equals the actual colored adjacency, and every interval has an actual local path. Thus leaf acceptance has no unchecked dependence on virtual edges. For an exclusion result, the essential direction is nevertheless preservation of every genuine completion, not a claim that intermediate survivors are certificates.

## Search coverage and symmetry

The recursion picks an unassigned chord of smallest surviving domain and explores every retained one of its six values. Every recursive edge reduces the number of unassigned pairs. Candidate-word initialization assigns the whole directed cycle; remaining unordered pairs are exactly its chords, including the wraparound exclusion. With at least three vertices this is a genuine directed cycle with distinct pairs.

Color normalization in first-occurrence order enumerates one representative per global color permutation. The candidate then keeps the least normalized rotation. Global color renaming and cycle rotation preserve actual rainbow triangles, predecessor indices, local intervals, and vertex-incidence requirements. Reflection is not assumed. The independent literal group oracle tests all six permutations and every rotation on all 88,560 raw words of lengths 3–10; length ten has 59,049 words and 1,002 orbits.

Every labeled fixed-cycle completion at order `n` comprises a raw three-color cycle word and six choices per chord. The independent complete-matrix oracle enumerates this class through order five, with totals 27, 2,916, and 1,889,568. It is not enumeration of every labeled tournament at order five. Separate raw tournament enumeration ends at order four. The large-order result uses the reduction, reviewed preservation proof, and complete reduced search rather than an inaccurate raw-enumeration claim.

## Finite theorem and stopping boundary

If a counterexample had at most ten vertices, choose an induced-minimal one. Orders one and two have immediate outgoing monochromatic sources. At every remaining order, the credited Hamilton-cycle, interval, and incidence results place that minimal counterexample into an enumerated reduced word class. The preserved actual values would survive every sound deletion and occur in an exhaustive DFS branch. Complete zero searches at each general order 3–10 contradict its existence.

This inference uses every general order, not only order ten or a periodic subcase. Periodic cycle words of lengths 3, 6, and 9 are separately checked controls. The interrupted periodic-twelve runs provide no result. Neither periodic twelve, a general order above ten, an all-size strict-periodic statement, nor the unrestricted conjecture is accepted by this argument. The two large engines share the same surrounding search; their differing closure updates are corroboration, not fully independent algorithms. No human review, proof-assistant verification, or formal unsatisfiability certificate is claimed.
