# Independent adversarial proof audit: PR #904 / problem 30000347

Audit completed 2026-10-12 20:21 PDT (2026-10-13 03:21 UTC).
**Assigned proof-audit completion estimate: 100%.** This is not an estimate of
the parent publication program's completion.

## Verdict and independence

**PASS for mathematical correctness. No substantive proof gap, counterexample,
or mandatory mathematical repair found.** The frozen proof establishes the
stated restricted NP-completeness result, conditional only on classical Vertex
Cover NP-completeness. Its optional finite-distance and exact 3-to-4 variants
also follow. A historical source/model check supports that this is the precise
undirected three-demand question from the 2005 report. Novelty and current
priority are separate questions and are not certified by this audit.

Reviewed artifact:
`original/unsolved_math_prioritization/attempts/30000347/frozen_packet/PROOF.md`,
SHA-256 `f31b19b8e4286e0104ed1e272f5cbc4a39e20aea78aa30334466f5b44e5830f7`.
The line numbers below refer to that frozen file.

I reconstructed the proof before implementing a new checker. I did not read
prior independent audits, their code/results, other new reviewers' reports, the
submitted checker's code, or acceptance/gate documents. In addition to the proof,
I read the frozen `SOURCE_AND_MODEL.md` to identify its source and independently
inspected the publisher PDF. No original files were modified. All audit outputs
are confined to this `proof_family` directory.

## Exact mathematical claim and success criterion

The restricted decision language consists of finite simple undirected graphs,
three distinct terminals with all three original pairwise distances exactly 3,
unit traversal lengths and unit edge-deletion costs, and a nonnegative
binary-encoded integer budget. A yes-instance admits a set of at most that many
edges whose removal makes every terminal distance at least 4, with infinity
permitted. The claim is NP-completeness of this language, with consequent
NP-hardness of exact optimization and NP-completeness of the decision version
allowing positive binary-encoded rational deletion costs and rational budgets.
Traversal lengths remain unit lengths in the rational-cost statement.

Success requires a polynomial, two-direction, unrestricted-edge-deletion
reduction from Vertex Cover, complete characterization of all original
geodesics, and polynomial verification of certificates. It must also avoid
assuming that only spokes can be deleted, that endpoints of source edges have
a preferred orientation, or that disconnected residual terminals are forbidden.
Those requirements are all met.

## Independent reconstruction of Lemma 1 (lines 44–84)

Replacing each source edge by a path with two fresh internal vertices produces
the explicitly supplied independent parts A, B, C. Original edges are removed,
so no A–A edge remains. Each gadget contributes exactly one edge of each
cross-part type. For m>0 this supplies the geometric hypotheses of Lemma 2.
The counts n+2m vertices and 3m edges are exact. Choices of orientation do not
affect any of these facts.

For a source cover S, each replacement path can be covered by S and one fresh
internal vertex: when only its initial endpoint is selected, choose the second
internal vertex; when only its final endpoint is selected, choose the first;
when both are selected, either internal vertex suffices. Different gadgets have
different internal vertices. This proves the constructive upper bound
tau(H) <= m+tau(Q).

For any H-cover X, set S=X intersect V(Q), and let q count source edges
uncovered by S. Every gadget contributes at least one internal cover vertex
because its middle edge must be covered. Each of the q uncovered source edges
forces both internal vertices. Thus |X| >= |S|+m+q. Adding an endpoint of each
uncovered source edge gives an actual source cover S' of cardinality at most
|S|+q <= |X|-m. Coinciding selected endpoints strengthen that inequality rather
than invalidating it. This is a direct cover extraction, not a supposition that
S itself already covers Q. Hence tau(H)=m+tau(Q).

The identity also holds for m=0, isolated vertices, disconnected Q, and arbitrary
nonoptimal covers. Only the later terminal-distance hypothesis needs m>0.

## Independent reconstruction of Lemma 2 (lines 86–136)

The added terminals have disjoint neighborhoods and no terminal-terminal edges.
This excludes paths of lengths 1 and 2. A cross-part edge gives a length-3 path
for its corresponding terminal pair. Conversely, any length-3 path between
terminals a and b must have first interior vertex in a's own part, last interior
vertex in b's own part, and one H-edge joining those two vertices. Neither a
third terminal nor a vertex from its part can appear in such a path. Therefore
there is exactly one geodesic edge set {e_u,uv,e_v} for each H-edge uv, and these
are the entire geodesic family across the three pairs.

Deleting the spokes indexed by an H-cover hits all these paths, proving
opt(G_H) <= tau(H). Edge deletion cannot create a shorter path; hitting every
original geodesic is consequently equivalent to increasing all three original
distances. Longer paths, cycles, and alternative geodesics arising only after
deletion cannot invalidate this implication.

For the lower bound, take an arbitrary feasible deletion set F. For every
deleted spoke include its H-endpoint in X; for every deleted H-edge include
either endpoint. Duplicates are merged, so |X| <= |F|. Every H-edge uv indexes
one of the original terminal geodesics, which F necessarily hits. Each possible
hit inserts u or v into X. The arbitrary choice for a deleted middle edge
therefore works in every case, independently of choices made for other edges.
Thus X is an H-cover. There are no other edge types in G_H, no undeletable
edges, and no omitted deletion strategies. Equality opt(G_H)=tau(H) follows.

Isolated vertices of H merely give useless spokes; allowing them does not affect
the result. The constructed G_H is initially connected: all terminals are
mutually linked, and every H-vertex is joined to its part's terminal.

## Reduction, degeneracies, encoding, and NP membership (lines 21–39, 138–170)

Composition gives opt(G_H)=m+tau(Q). With B=m+k, the source answer is yes exactly
when the target answer is yes. In the reverse direction, a target blocker yields
an H-cover of no greater size and then a Q-cover of size at most |F|-m <= k.
No numerical assumption about k is used.

For m=0 and k>=0 the source is always yes. A fully concrete fixed target
yes-instance is an H-triangle with one vertex in each part and its three
terminal spokes, with budget 2. All original terminal distances are 3 and
deleting two suitable spokes blocks them. Thus the stated handling of edgeless
instances can be implemented as a total many-one reduction. Source graphs of
orders 0 and 1 are covered by the same case. The m>0 branch has nonempty parts
and three fresh distinct terminals. Negative k is outside the specified source
language, and no handling of it is needed.

The graph has n+2m+3 vertices and 3m+(n+2m)=n+5m edges. Distinct fresh vertices
ensure simplicity even when source edges share endpoints. The construction has
polynomial representation size and depends on n and m, not the magnitude of k.
Adding m to binary k increases its bit length only polynomially. Consequently
large budgets do not introduce pseudo-polynomial expansion.

A certificate lists at most all graph edges. Validity, cost/cardinality, and
three original and residual distances can be checked by BFS and elementary
arithmetic. For rational costs, multiplying the input denominators yields a
common denominator whose bit length is at most the sum of their input bit
lengths. Numerators and their sum likewise have polynomial bit length; adding
and comparing with a rational budget therefore remains polynomial. General
positive rational costs include the already-hard all-unit instances. No
weighted version of the cover identity is asserted or required.

These arguments establish NP-completeness without assuming P differs from NP.
An exact polynomial optimization algorithm would decide the budget problem,
which justifies the NP-hardness statement.

## Optional finite and exact-increment variant (lines 172–192)

The three fresh length-4 paths use nine distinct new internal vertices. Each
internal vertex has degree 2 and no additional incident edges. A simple path
between old terminals that uses such a vertex must traverse its entire chain
between old terminals. It therefore has length at least 4. Combining chains or
passing through the third terminal cannot produce a new path of length <=3.
All original geodesics are unchanged.

Any augmented blocker still hits each original geodesic using original edges,
because backup edges occur on none of those geodesics. Ignoring deleted backup
edges and applying the existing extraction gives an H-cover of size at most
the original deletion count. Conversely, spoke deletions from any H-cover leave
all backup paths intact and kill every length-3 path. Every terminal pair then
has distance both at least and at most 4, hence exactly 4. This proves equality
of the unrestricted, finite-terminal-distance, and exact-3-to-4 optima with
tau(H), and supplies the same many-one reduction for those budget variants.
BFS also verifies the extra requirements in polynomial time.

This does not prove global residual connectivity, which the frozen proof
correctly declines to claim. Terminal vertices can have intact backup chains
even when H-vertices become isolated.

## New executable adversarial evidence

Run `python3 independent_checks.py` from this directory. It uses only the Python
standard library. `independent_results.json` records a successful run at
2026-10-13T03:17:49.087090+00:00 (5.740 seconds). The checker constructs adjacency
lists and discovers distances and geodesics by BFS/DFS. A generic exact
hitting-set recurrence computes both cover and blocker optima independently of
the claimed identities. Separately, direct BFS on every deleted graph validates
geodesic hitting and extraction over unrestricted deletion subsets.

| Check | Independently observed count |
| --- | ---: |
| Tripartite instances with part sizes (1,1,1), (1,1,2), (1,2,2) | 145 |
| Every edge-deletion subset in those graphs | 165,952 |
| Feasible unrestricted blockers therein | 89,975 |
| Lower- and upper-endpoint extraction checks | 179,950 |
| All admissible tripartite graphs with part sizes (2,2,2), exact optima | 3,375 |
| Source graph/orientation instances through order 5 | 2,808 |
| Forward subdivision-cover constructions | 30,579 |
| All H-cover extractions for source order <=3 | 1,143 |
| Composed budget comparisons, including a 513-bit budget | 21,630 |
| Cover deletions retaining finite distance exactly 4 | 1,718 |
| All deletion subsets of an augmented six-vertex base instance | 262,144 |
| Feasible unrestricted augmented blockers | 184,320 |
| Augmented blockers retaining finite terminal distances | 3,420 |
| Augmented blockers attaining all distances exactly 4 | 90 |

The source suite includes every labelled simple Q through order 5, all
orientations through order 4, and the two opposite orientations for each
nonempty order-5 graph. It includes all 1,094 nonempty source graphs of orders
2–5 and every edgeless/isolated-vertex degeneracy of smaller order. The last
augmented instance has optimum 2 under each of the unrestricted, finite, and
exact-3-to-4 requirements. Arbitrary backup-edge deletions are included.

Two deliberate assumption-removal controls also passed by finding the expected
counterexamples. If H has only edges ab and ac with one vertex in each part,
tau(H)=1 but terminal distances are (3,3,4) and optimum blocker size is 2. Thus
the hypothesis of at least one edge of each cross-part type is necessary for
the stated lemma. If H contains a triangle internal to A plus a separate
cross-part triangle, tau(H)=4 while the blocker optimum is 2: the internal
edges generate no length-3 terminal geodesics. Thus the requirement that every
part be independent is also essential. Both conditions are explicitly stated
and are guaranteed by Lemma 1.

These computations are finite consistency evidence. They supplement, rather
than replace, the universal deductive arguments above. The original checker's
execution provenance and its precise budget-comparison count are not certified
by this separate checker; another reproduction family can audit those artifacts.

## Historical model alignment and exact remaining gap

Independently inspected the [publisher's report](https://ems.press/content/serial-article-files/46024?nt=1),
printed pp. 2856–2858: Krause defines BSP for undirected graphs using edge count
as distance, deletion costs, and blocking every original shortest path. The
three-demand open question uses all pairs of three vertices. This agrees with
the present unit-length construction, including unrestricted edge deletions.
The report separately identifies directed triangle hardness. The claimed
undirected conclusion therefore addresses that historical mathematical question.

**Strongest verified result:** a self-contained polynomial many-one reduction
from simple Vertex Cover proving NP-completeness of unrestricted-edge-deletion
undirected three-terminal BSP even with all original distances 3 and all costs
1, plus correctness of the finite and exact-3-to-4 strengthening.

**Exact remaining proof gap:** none found. **Exact publication gap outside this
audit:** current priority/novelty, the manuscript and publication package, and
the provenance of submitted reproduction artifacts need their own independent
checks. This verdict must not be promoted to a claim of a newly solved open
problem merely from mathematical soundness or from the 2005 source's wording.
