# Acceptance report for initial odd ear complexity

Date: 20 October 2026. Problem ID: 30002726. Source: OWR-13353-012.
Queue row: 1828. Recorded result: **CLAIMED_SOLVED, 3/5 approaches**.

## Conclusion

The accepted result is NP-completeness of deciding beta(G) >= t for an input
integer t, already for simple 2-vertex-connected cones over connected
bipartite graphs. This resolves the stated general computational-complexity
question conditionally in the usual sense: a polynomial-time exact algorithm
for beta would imply P = NP. It does not prove P != NP.

The acceptance basis is the complete mathematical argument in
`NP_COMPLETENESS_PROOF.md`, with independent adversarial audit PASS in
`AUDIT_HARDNESS.md`. The audited primary manuscript has 10,202 bytes and
SHA-256 `5e7fd90b5ad5178702797896619542aebb179f5056ad9f7426b1d296625ca252`.
The package preserves those proof bytes exactly.

## Exact target

The input graph is finite, undirected, loopless, 2-vertex-connected, and has
at least three vertices. The general definition permits parallel edges;
the hard instances are simple. An open ear decomposition starts with a
circuit and then adds paths whose two distinct endpoints are already present
and whose internal vertices are new. Its ears partition the graph's edges.
Both the initial circuit and one-edge paths count as ears. Beta maximizes
the length of the initial all-odd prefix, stopping before the first even ear.

The established factor-critical characterization uses the maximum of
|E(H)| - |V(H)| + 1 over 2-connected factor-critical subgraphs H. The proof
checks both directions of its application, including extension of the
subgraph's odd ear decomposition and the effect of adding induced edges.

## Proof acceptance checks

1. **Cone identity.** For the cone over connected bipartite B, beta equals
   the maximum number of edges of a connected induced perfectly matchable
   B[S]. Connectivity is retained; a disconnected relaxation is not used.
2. **Explicit reduction.** Set Cover is reduced to the exact problem using
   K_(k,k) blocks and single connector edges. The graph is simple and its
   explicit vertex and edge lists have polynomial size.
3. **Forward direction.** An inclusion-minimal cover has distinct private
   elements, producing a matching, connectivity, and the threshold bound.
4. **Reverse direction.** The threshold forces every block to retain an
   internal edge. Matching balance bounds the number of connectors by the
   cover budget. Connectivity then makes their sets cover every element.
5. **NP membership.** A polynomial certificate supplies a factor-critical
   2-connected subgraph and a perfect matching after every vertex deletion.
6. **Boundary cases.** Trivial Set Cover inputs have fixed yes/no outputs;
   nonpositive target thresholds are handled directly.

The only established external mathematical inputs are Set Cover
NP-completeness and the odd-ear/factor-critical characterization. Their public
citations are in the proof and audit. The source gate verifies the exact
problem's conventions and distinguishes relevant but different objectives.

## Independent computation and replay

`audit_set_cover.py` is a separate standard-library exact implementation;
it imports no other matching or beta implementation. Its shipped expected
result is `audit_set_cover_results.json`.

- 63 small block graphs: every vertex subset is considered, using recursive
  exact perfect-matching tests and connectivity checks.
- 14 corresponding cones: every eligible induced factor-critical,
  2-connected vertex set is considered directly.
- 441 fully covered set systems with 1 <= m,n <= 3: all 1,719 budgets are
  compared with exact Set Cover using the proved saturation-state optimizer.
- Largest constructed cone in the compressed checks: 148 vertices,
  1,455 edges. Zero discrepancies.

These are finite deterministic corroborations. The larger checks use the
saturation invariant explained in the audit; they are not direct enumeration
of every vertex subset in a 148-vertex graph. The proof, not the finite data,
establishes the unrestricted theorem. The packaged replay executes the
checker in isolation and requires exact agreement of both stdout JSON and
the generated result file with the expected result.

## Research accounting

There were three substantive approaches before the accepted resolution:
(1) the cone characterization and investigation of a matching shortcut;
(2) a separate SAT-based hardness route; and (3) the accepted simple-graph
Set Cover reduction. This accounting does not convert the unused SAT route
into a separately accepted theorem. Secondary SAT, multigraph, and
odd-subdivision proof artifacts are excluded from this package.

## Publication and provenance boundaries

The source gate is a chronological literature record from before the proof.
It found no general exact-target resolution in a bounded search; that finding
is not a novelty certificate and does not exclude unseen or later work.
The accepted proof and audit do not claim external peer review.

The public audit retains the mathematical verification in full. Editorial
changes remove publication-workflow commentary, replace a reference to other
implementations' authors with implementation-neutral wording, and state that
the audited manuscript satisfies the required exposition details. The source
gate's historical status is explicitly distinguished from the new result.
No mathematical argument or scope restriction is weakened by these edits.

Included source data are only public bibliographic/retrieval metadata and
authorized corpus hashes, byte counts, and match results. Raw PDFs, extracted
source text, rendered source pages, datasets, private research material,
credentials, and caches are excluded.

No conclusion about fixed-constant threshold hardness, total odd-ear
optimization, closed-ear decompositions, or arbitrary matroid inputs follows
from this package.
