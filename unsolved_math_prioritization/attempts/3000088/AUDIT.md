# Independent audit: weighted bipartite coloring, problem 3000088

## Decision

This AI-assisted manuscript is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed.

The complete analytical proofs, parameterized construction formulas, and the full frozen b=3 construction are retained. This is not a computational reproduction package: raw assignment tables, certificate packages, detailed instance records, generated grid realizations, checker programs, copied source documents and images are omitted. The seven central graph instances are mathematically specified by the retained all-b families and frozen construction, but the stored certificate realizations and the other finite grid/control inputs cannot all be reconstructed from this edition alone. Historical finite checks support the proofs; no universal theorem depends on those computations.

**ACCEPT for the restricted results and method obstructions only.** No correction patch is needed. The unrestricted Chung–Ross target remains unresolved by this work. Acceptance is not a novelty claim, a current-openness claim, or an endorsement of uninspected proofs in the cited literature.

The mathematical note is 15,088 bytes, SHA256 `73f9313dd0aa34e855caff385d39cff882938a18784faa4935b94265eba3cced`. The result summary is 2,729 bytes, SHA256 `b2bf823aa95b867c6ce23291c84985fc601f71c9779df14137c912e959c02240`. All 23 candidate inventory members were independently authenticated before and after each exact run. The inventory is 5,275 bytes, SHA256 `2ec25615a1757afc347130f0931c7acd556f3aa68b75588d5c255358d0e07b2f`.

## Target and supplied input

The target is 2b−1 colors for finite bipartite multigraphs with weights in [0,1], where b is the maximum optimal local unit-bin count and b≥1. Feasibility means total incident weight of each color is at most one; adjacent edges may share a color.

The constructive statements receive B≥1 and feasible local partitions into at most B bins. Taking B=b gives an existential result, without claiming an efficient algorithm to compute b. The parameter is not the ceiling of weighted degree: three weights of 3/5 require three bins although their total has ceiling two. All arguments use only finite sums, comparisons, partitions, minima and averaging, so arbitrary real weights are allowed. Computations use rational weights and do not establish that generality by enumeration.

## Proof review

### Lemma 1: simple forests

Accepted. At a non-root vertex there is exactly one already colored edge. Label its local bin with that edge's color and injectively label the other bins using remaining colors. Earlier edges are unchanged, and each child has only one colored incoming edge of weight at most one. Induction gives B colors. Any coloring restricted to a vertex is a local packing, proving the lower bound b. Simplicity is essential; several parallel parent edges could impose incompatible bin-label constraints.

### Theorem 2: forest support and arbitrary parallel multiplicity

Accepted. The rooted support forest gives each non-root vertex exactly one previously processed neighbor. Each incoming bundle uses at most B color names, because its parent used distinct colors on at most B outgoing bins. Restrict the vertex's supplied bins to outgoing edges. If q incoming color names and r outgoing bins satisfy q+r≤2B−1, assign distinct absent colors to all outgoing bins.

The only remaining case is q=r=B. Let x be the minimum incoming load and y the minimum outgoing-bin load. Then

    x+y ≤ (total incoming load + total outgoing load)/B ≤ 1.

The numerator equals all incident weight and is at most B by the supplied packing. Merge this outgoing bin into the minimum-load incoming color and give the other B−1 bins the B−1 absent colors. Outgoing bins still have distinct names. Each child receives, in any color, a subset of one feasible parent bin. Thus interim feasibility and the incoming-bundle invariant propagate. Zero loads and unbounded finite multiplicity do not affect any step.

The argument does not cover cyclic support: colors contributed by multiple previously colored neighbors need not have union of size at most B. That missing invariant is explicitly acknowledged and cannot be replaced with a weighted-degree bound.

### Proposition 3: all-b parallel family

Accepted for every b≥2. Its support is a bipartite tree. At u, b−1 unit edges require distinct bins and the two 2/5 edges occupy one additional bin. At v, b−2 unit edges are separate and each remaining bin pairs 2/5 with 3/5. Hence the maximum local optimum is b.

In b colors the b−2 parallel unit edges exclude their colors from all other positive edges at both centers. Only two colors remain. The unit pendant at u forces both 2/5 edges to share the other color. At v the two 3/5 edges need distinct colors, so one joins a load of 4/5 and produces 7/5. The explicit b+1 coloring is feasible. The claimed index b+1 and sharpness of 2b−1 only at b=2 are correct.

### Lemma 4: a cycle-breaking matching

Accepted. A simple cactus has bridge and simple-cycle blocks, whose incidence graph with all original vertices is a forest. Root a component at a vertex. Each cycle block has one parent-side attachment, and a simple cycle has an edge avoiding that attachment.

If distinct cycle blocks share x, at most one is parent-side of x. Every other such block has x as its attachment, so its chosen edge avoids x. Consequently no chosen pair meets, including when many cycles share a cut vertex. Exactly one edge is removed from each cycle block, and every cycle belongs to such a block, leaving a forest. Isolated vertices merely give isolated incidence nodes. A two-edge parallel cycle has no edge avoiding its attachment; it is correctly excluded by simplicity.

### Theorem 5: cactus bound and all-b sharpness

Accepted. Restricting the supplied packing after deleting the matching preserves at most B bins. Lemma 1 colors the remaining forest with B colors, and the matching takes one additional color. Bipartiteness is unnecessary for this upper bound. If b=1, all edges can share a color because each total incident load is at most one.

The sharpness graph is simple, bipartite and unicyclic. At v0,v2,v3 the cycle edges fit in one bin besides b−1 unit bins. At v1 the two 3/5 edges need two bins besides b−2 unit bins. Thus all cycle vertices have local optimum b. In b colors the first three vertices each force equality of their two cycle-edge colors; together these force all four edges to agree, overloading v1 to 6/5. Alternating two colors on the cycle and assigning the unit pendants distinct colors among the remaining b−1 names gives b+1 colors. This proves the exact maximum for every b≥2, independently of the b=2,3,4 finite checks.

### Proposition 6: frozen optimal b=3 root packing

Accepted with its precise scope. The root packing has three exactly full bins. Its incoming child loads are 41/100,41/100,1/100. Each outgoing edge weighs 60/100 and cannot join either of the first two colors. A four-color palette leaves the third incoming color and one fresh color, but three outgoing edges need three distinct colors since every pair sums to 120/100. Thus the specified frozen coloring cannot extend. Five colors extend it as claimed.

Recoloring all five parallel edges together is valid because their total is 83/100. The three pendants at each center use the other three colors, giving a four-coloring.

The full graph is not three-colorable. Its three root pendants need distinct colors, leaving capacities 41/100,41/100,1/100. The four larger parallel edges sum to 82/100, cannot share the 99/100 pendant, and fill the first two capacities exactly. The 1/100 edge must use the remaining color. Up to permutation, the child consequently receives the same frozen load pattern. Only one of those three colors can admit a 60/100 edge, while the three such edges need distinct colors. Therefore the exact index is four. This is a method obstruction, not a counterexample to the conjectured five-color bound.

## Boundary cases

- Empty graphs have index zero. The target is explicitly restricted to b≥1, and algorithms with supplied B≥1 color no edges when the graph is empty.
- A nonempty all-zero graph has local optimum one under the stated convention of assigning every edge to a bin, and uses one color. Zero-weight edges can stay in bins. Nonempty zero-load bins and used zero-load color names still count, and all inequalities remain valid.
- Disconnected components reuse a common palette; isolated vertices impose no constraint.
- Parallel edges are permitted in Theorem 2 and excluded from Lemma 1 and the cactus theorem.
- Supplied packings may be non-optimal. All constructive inequalities use B; no step secretly computes b.

## Exact independent verification

For the historical audit, a new standard-library verifier was written from the proofs, definitions and certificate schema. Candidate source code was not inspected as implementation material, imported or executed. Integrity hashing reads its bytes but supplies no implementation dependency. Exact subset dynamic programming computes local bin optima; independent weighted-coloring DFS computes global feasibility; a separate full labeled enumerator cross-checks both on small domains. All numerical feasibility checks use `fractions.Fraction`, and rejection conditions use explicit exceptions rather than assertions.

All 224 stored rejection rows passed exact load, domain, completeness and uniqueness checks: 32 parallel assignments, 128 cactus assignments and 64 frozen extensions. All seven stored graph instances have the asserted local optimum and exact weighted index; their local packings, positive colorings and load maps passed. The frozen root packing and its five-color extension also passed.

Independent constructors reproduced all 10,976 rooted colorings on 2,744 support-path instances and all 2,187 cactus weight-grid colorings. A general cactus matching implementation additionally passed on every cactus among all 33,868 labeled simple graphs with zero through six vertices: 10,026 cacti, tested at 59,377 root choices. This includes non-bipartite cacti and shared cut vertices.

Separate full labeled enumeration cross-checked 210 local-weight multisets and 1,536 global palette decisions. Nineteen semantic tampering tests rejected wrong loads, duplicate or missing assignments, invalid colors, nonexistent witness vertices, an altered frozen prefix, invalid local packings and an infeasible positive coloring. Further explicit edge-case controls passed. Normal, -O and -OO runs passed with identical results. VERIFICATION.json records public aggregate coverage and reproduction limits. The detailed test-domain report and executable checker are not distributed in this edition.

The candidate's historical merge-event count is tie-breaking dependent and was not reproduced. Its finite graph/root/coloring counts and mathematical certificate conclusions were independently reproduced. Historical generator execution itself is not being independently attested.

## Sources and attribution

- [Khan–Singh 2015](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2015.136): the publisher record and retained PDF were independently inspected. Printed page 137 states the bin-packing conjecture; page 138 states 20b/9+o(b) progress and an explicit ceiling-2.2223b algorithmic theorem. Both pages were independently rendered and visually inspected. Their algorithmic proof was not audited.
- [Feige–Singh, *Edge Coloring and Decompositions of Weighted Graphs* (2008)](https://www.microsoft.com/en-us/research/wp-content/uploads/2008/09/edgecoloring.pdf): the retained PDF was independently extracted on pages 1–4; PDF page 2 was visually inspected. It distinguishes bin-count and total-weight formulations. No general bound from that paper is a dependency of the accepted restricted proofs.
- [Sannyasi, arXiv:2012.15056v1](https://arxiv.org/abs/2012.15056v1): direct primary-PDF text inspection confirms the definitions and Theorems 10 and 11, respectively b+1 for simple edge-disjoint-cycle graphs and 1.693b+12 for multigraph trees. Adjacent proof text was inspected, but no full-paper proof audit is claimed. The candidate's matching-deletion proof stands independently.
- [Huc 2011](https://doi.org/10.1142/S0219265911002861): the [indexed abstract](https://sonar.ch/global/documents/62885) was independently read. It describes a tree-support multigraph result, but its formula is omitted and its prose parameter is total weight. The retained primary-publisher receipt reports HTTP 403. No denied origin was bypassed. The exact theorem and proof remain unverified. This is grounds for avoiding novelty claims, not for importing a precise unverified theorem.

The historical source inspection supports attribution and scope only. Preparation of this edition performed editorial and byte-integrity checks, with no new scholarly-source retrieval, source-text extraction, visual inspection, literature survey, or mathematical execution. No full-target result, novelty claim, comprehensive current-literature conclusion, or formal theorem-prover certification follows.
