# Independent mathematical audit: three-terminal shortest-path blocking

Date: 7 October 2026.

Problem: 30000347 / OWR-1111-001.

## Verdict

**PASS. The frozen manuscript proves the claimed full NP-completeness result.**

No mathematical correction is required. The decision problem is NP-complete for
finite simple undirected graphs with unit traversal lengths, unit edge-deletion
costs, and three specified terminals whose original pairwise distances are all
3. The corresponding exact optimization problem is NP-hard. The stated
positive binary-encoded rational-cost extension and the optional finite-distance
strengthening are also valid.

This verdict is about mathematical correctness and the stated historical-model
match. It is not a novelty, priority, or exhaustive current-literature finding.
It is an independent audit, not a journal acceptance or a formal proof-assistant
certificate. No other audit report was used.

## Frozen object and integrity

The audited proof is `PROOF.md`, 11,661 bytes, SHA-256:

`f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7`

The supplied `FROZEN_MANIFEST.json` has SHA-256:

`b13c9cee3e806a263ba0e24b2838599692727ea48d26977d4fca714e1e30d273`

Every one of the six file hashes and byte counts declared in that manifest was
recomputed and matched. The audited packet was not modified. The author checker
was rerun from a separate copy so its output could not alter the frozen result
file. Companion source/model statements and recorded computational claims were
checked as described below.

## Source and exact problem match

I independently read Krause's entire contribution on printed pages 2856–2858
of [Oberwolfach Report 50/2005](https://ems.press/content/serial-article-files/46024?nt=1),
including the two enumerated open problems. Its relevant target is undirected
BSP with unit traversal lengths, arbitrary edge deletion, and an increase of at
least one for every pair among three specified vertices. It explicitly reports
directed triangle hardness. Treating the directed case as an additional open
problem would therefore be incorrect. The frozen manuscript does not make that
mistake.

I also independently read the definition on printed page 2, Section 4.3, and
Theorem 9.3 in [Krause's dissertation](https://webdoc.sub.gwdg.de/ebook/dissts/Braunschweig/Krause2006.pdf).
Its assumptions admit the constructed simple graphs and positive costs. Multicut
solutions are allowed as BSP solutions, confirming that disconnection is
permitted. Section 4.3 leaves the undirected case unresolved there, and Theorem
9.3 concerns the directed case. The triangle refers to the demand pairs, not to
three adjacent terminals in the input graph.

The current-source PDF sizes and SHA-256 hashes agree with `SOURCE_MANIFEST.json`.
I independently re-extracted both available report PDFs using `pdftotext` and
recomputed the normalized contribution hash. Both produced
`80037c2f79bde157b603e243898db7bc03af548072cdf5df985fed306bdc73f0`,
confirming the manifest's content-match statement despite different PDF bytes.

I visually inspected printed page 94 of the cited
[Karp scan](https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf): its Main
Theorem and Node Cover entry supply the standard NP-complete source problem.
No theorem about tripartite vertex cover is being accepted on citation alone;
the manuscript proves the needed identity directly.

The manifest's corpus-dataset provenance and the completeness of the author's
literature search were not independently recertified. Neither is a mathematical
premise of this proof. The explicit absence of a priority claim is appropriate.

## Adversarial proof review

### 1. Twice-subdivision identity

For an original edge with ordered endpoints `u,v`, the replacement path is
`u,b,c,v`, with private new vertices `b,c`. Original vertices form one independent
part, all `b` vertices the second, and all `c` vertices the third. Original edges
are deleted, so no unnoticed same-part edges survive.

The upper bound is correct in each endpoint case. When only `u` is in the
original cover, adding `c` covers both remaining gadget edges; when only `v` is
in the cover, adding `b` does so; when both are selected, either internal vertex
suffices. Exactly one new vertex per gadget is added.

For the lower bound, every gadget requires an internal selected vertex because
of its middle edge. A gadget whose original endpoints are both absent requires
both internal vertices. The private internal vertices make those contributions
additive. If `q` original edges remain uncovered by the selected original
vertices, adding one endpoint for each of those edges creates an original cover
using at most `q` additional vertices. Repeated endpoint choices only improve
the bound. Thus the claimed equality `tau(H)=m+tau(Q)` holds for all inputs,
including isolated vertices and arbitrary endpoint ordering.

### 2. Complete characterization of terminal geodesics

The three new terminals are distinct and have no terminal-to-terminal edges.
Their neighborhoods are the disjoint supplied parts. This excludes paths of
length 1 and 2. An edge of each cross-part type supplies a path of length 3 for
the corresponding pair.

Any length-3 terminal path has precisely two interior vertices. Its first and
last edges must be the respective part spokes, and its middle edge must be the
corresponding edge of `H`. There is no space for a third-terminal detour,
two-edge passage through the third part, or some other unintended shortcut.
This proves exhaustiveness, which is essential: merely exhibiting selected
length-3 paths would not prove the reduction.

Every nonempty original graph contributes all three cross-part edge types, so
the hypothesis is established by the preceding construction. It is not an
unproved promise on the Vertex Cover input.

### 3. Arbitrary deletions and optimum equality

Deleting the spokes of a vertex cover hits every described geodesic, giving
one inequality. For the converse, the proposed extraction handles every allowed
kind of deleted edge. A deleted spoke contributes its unique nonterminal
endpoint; a deleted edge of `H` contributes either one of its endpoints. For
each edge `uv` of `H`, the path consisting of its two endpoint spokes and `uv`
must be hit. Whichever of these three edges is deleted guarantees that the
extracted set contains an endpoint of `uv`. Each deleted edge contributes at
most one vertex, and duplicates lower the extracted cardinality.

Consequently every arbitrary blocker produces a cover of no greater size.
This rules out a cheaper solution exploiting middle-edge deletion. The argument
does not silently protect any edge or terminal spoke, introduce infinite costs,
or switch from edge deletion to vertex deletion. With unit deletion costs it
establishes the exact optimum equality claimed.

### 4. Decision equivalence, budgets, and construction size

The composed optimum is `m+tau(Q)`, so budget `B=m+k` is valid in both directions.
The base problem uses nonnegative `k`. An edgeless input is therefore always a
yes-instance and may be mapped to a fixed target yes-instance. One explicit
choice is the construction from a single original edge with budget 2. For that
same constructed graph, budget 1 is a no-instance. Thus neither `k=0` nor the
edgeless boundary hides an ambiguity in the reduction.

The counts `n+2m+3` vertices and `n+5m` edges are exact. New vertex identities
prevent loops and duplicate edges. Even an isolated original vertex has a
terminal spoke; for `m>=1` the entire constructed graph is initially connected.
Its representation has polynomial size. Adding `m` to a binary-encoded budget
has polynomial bit complexity and does not expand the graph according to the
budget's numerical magnitude. Very large `k` and disconnected original graphs
cause no difficulty.

### 5. NP membership and rational costs

An edge subset has polynomial encoding length. Breadth-first searches before
and after deletion test all three inequalities in polynomial time, using an
unreachable marker for infinity. Since only edges are removed, blocking every
original shortest path is equivalent to the required strict distance increase.
No exponential path enumeration is needed by the certificate verifier.

With binary rational costs, exact summation and budget comparison remain
polynomial in the total input bit length. For example, the bit length of a
common denominator formed by multiplying the supplied denominators is bounded
by their total bit length. Unit costs are a special case, so hardness carries
over without a separate reduction. The distinction between NP-complete decision
and NP-hard optimization is maintained correctly.

### 6. Optional finite-distance strengthening

Each added path has length 4 and private internal vertices of degree 2. Any
simple terminal path using one of those vertices must traverse the whole added
terminal-to-terminal path, so no new path of length at most 3 is created.
For an arbitrary blocker in the enlarged graph, deleting backup-path edges
cannot hit any of the original length-3 paths. Ignoring those deleted edges
therefore preserves the lower-bound extraction.

Conversely, a cover-based spoke deletion leaves every backup path intact. The
original length-3 paths are blocked and length-4 paths survive, so all three
distances equal 4. This proves both the finite-distance and the exactly-one
increase versions, under the same budget reduction. It does not assert
connectivity of all remaining vertices; the manuscript correctly avoids that
stronger claim.

## Reproducibility and independent finite tests

I read and reran the frozen author checker, whose SHA-256 is
`c25c82f6374a5d06b47288b658d40dfc3d0c541669f13424d979449005fa0998`.
All its recorded counts reproduced exactly:

- 165,952 deletion subsets for 145 tripartite graphs;
- 89,975 feasible blockers mapped to no-larger covers;
- 3,375 exact optimum checks on the `(2,2,2)` tripartition;
- 1,094 nonempty labelled original graphs through five vertices;
- 6,484 budget comparisons;
- 66 cover checks for the finite-distance extension.

I separately implemented `independent_check.py`, with no imports from the
author checker. It uses a different edge ordering, a different arbitrary
endpoint choice, direct residual-graph reachability layers, exhaustive vertex
subsets, and a maximum-independent-set recursion for subdivision cover numbers.
It passed:

- The same 165,952 deletions and 89,975 feasible-cover extractions;
- All 1,094 nonempty labelled original graphs through five vertices;
- 6,564 budget checks including `k=0` and a 101-bit budget;
- All 756 nonempty endpoint-ordering configurations through four vertices;
- 1,718 cover-based deletions in the length-4 backup construction.

Neither collection of finite tests substitutes for the written universal proof.
Their role is to challenge implementation, boundary cases, orientations, and
the exact distance claims. No counterexample or failed assertion was found.

## Required changes and use of this verdict

Required mathematical changes: **none**.

The proof may be described as independently audited and mathematically complete
for its precisely stated model. Retain the no-priority qualification. Do not
generalize this verdict to planar graphs, bounded-degree graphs, weighted
traversal lengths, globally connected residual graphs, or subsequent literature
status. The accepted object is the exact frozen proof hash above.
