# Independent audit: square-grid random-labeling peaks

Problem 9500009 / AMR-094-0009, rank 777. Audit date: 2026-10-05 UTC.

**Verdict: PASS for the stated finite computations and elementary partial results.
The full asymptotic problem remains UNRESOLVED after the five authored approaches.**
There is no candidate solution, novelty clearance, or publication-acceptance claim.
This audit performs verification, not an additional substantive proof-search turn.

## Scope and freeze

The author ZIP was preserved byte-for-byte: 27,286 bytes, SHA-256
`63b176e779846f2c99b1526c80fc57445dcc6495f614b498341f0514a109fbe4`.
All nine manifest-listed payloads and the manifest itself match their recorded
hashes. The author's default verifier passes. See `FREEZE_INTEGRITY.json`.

The graph is the Cartesian product of two n-vertex paths, with ordinary boundary,
not the torus. Peaks include boundary vertices. The audited random variable is
the Manhattan graph distance divided by n, conditional on exactly two peaks.
This agrees with [Burdzy's Problem 9](https://sites.math.washington.edu/~burdzy/open_mathjax.php).

## Independent numerical reconstruction

Fresh C++ code assigns labels in increasing order. On adding vertex v to the
already labeled set, it is a final peak precisely when every neighbor has already
been labeled. Equivalently, for a nonempty subset S and a prescribed peak set R,
the predecessor recurrence sums g_R(S without v) over v in S satisfying

    (v belongs to R) if and only if (all neighbors of v belong to S).

Start with g_R(empty)=1. A vertex outside S will receive a larger label, which
explains the test; deleting the last vertex of an order gives its unique
predecessor. Earlier vertices' peak decisions remain valid because all vertices
not yet present are understood to have larger labels. A parallel histogram tracks
the number of such peaks. This code was written independently of the author's
descending-order implementation.

All 162 unordered-pair counts, 29 singleton counts, and three full peak-count
histograms agree with the frozen results. Every histogram sums to (n squared)!.
Unsigned 64-bit integers suffice: each subset count is at most its permutation
count, and 16! is below the type's limit.

| n | Two-peak labelings | E[distance/n] | E[distance] |
|---|---:|---:|---:|
| 2 | 8 | 1 | 2 |
| 3 | 143,808 | 666/749 | 1998/749 |
| 4 | 779,299,174,080 | 377754599/463868556 | 377754599/115967139 |

Distance distributions, tail probabilities, and complete pair weights are in
`results/ascending_counts.json` and `results/independent_verification.json`.
These are exact finite integers and fractions, with no sampling or extrapolation.

Two further independently implemented checks apply for n=2,3:

1. Direct comparison of labels in every permutation, including all 362,880
   labelings for n=3.
2. Partition by lower-to-higher edge orientation and count topological orders of
   each orientation. Peaks are precisely sinks. The 16 and 4,096 orientations
   contain 14 and 2,398 acyclic orientations respectively. All peak sets and
   their counts agree with direct enumeration.

Thus agreement is not based only on rerunning one program or summing totals.

## Proof and certificate review

- **Descending-order recurrences:** A peak is exactly a birth with no earlier
  neighbor. Allowed-root subtraction removes the two disjoint singleton-peak
  classes. Every nonempty finite graph labeling has a maximum, so no zero-peak
  correction is missing. The exact-root and full birth-count recurrences follow
  from the same bijection and are valid as stated.
- **Admissibility:** A peak set is nonempty and independent. Conversely, on a
  connected graph, put the highest labels on any nonempty independent root set
  and assign the rest by increasing distance from it. Every nonroot has a larger
  neighbor, while all neighbors of each root have smaller labels. This proof
  includes the one-vertex case. As a finite check, direct enumeration on all 772
  connected labeled graphs with one through five vertices confirms 7,503
  nonempty independent root sets and no other possible peak sets.
- **Forest bounds:** The roots get the highest two labels, in either order;
  every nonroot has a higher-labeled forest parent. Additional square edges
  cannot create a nonroot peak or destroy a root peak. Removing the roots leaves
  a forest poset whose extension count is (N-2)! divided by the product of the
  nonroot descendant-subtree sizes. Every one of the 122 frozen certificates was
  checked for graph edges, root reachability, absence of cycles, subtree sizes,
  labels, and the exact peak set. Independent poset dynamic programming gives
  exactly the hook-length lower bound, which never exceeds the full pair count.
- **Rare conditioning:** Independent continuous labels produce uniform ranks.
  The selected interior centers have pairwise disjoint closed neighborhoods,
  giving m=floor(n/3) squared independent Bernoulli(1/5) indicators. Exactly two
  total peaks implies at most two selected peaks. The binomial tail expands to
  (4/5)^m times [1+m/4+m(m-1)/32]. This also holds for m=0,1. For n>=6,
  m>=n squared/36, yielding a polynomial prefactor times an exponential in
  minus a positive constant times n squared. The packing and tail algebra were
  additionally checked for n=2,...,50. The stated unconditional expected number
  of peaks also agrees with every finite histogram.
- **Conditional dependence:** The two opposite-corner peak events on the 3x3
  square have disjoint closed neighborhoods before conditioning. Direct
  enumeration under exactly two peaks gives joint probability 41/749 and
  marginal product 130321/2244004, with covariance -7485/2244004. This validates
  the counterexample without asserting a general correlation sign.
- **Growth weighting:** Completions of any fixed descending prefix are equally
  likely before conditioning; counting valid continuations therefore gives the
  stated transition ratio. Direct enumeration of all 7! suffixes after (0,1)
  on the 3x3 square gives 156, 180, and 336 one-peak completions for next vertices
  2, 3, and 4. Their normalized probabilities are unequal.
- **Restriction:** Direct comparison on the stated 4x4 example gives peaks
  {7,8}; its top-left 3x3 restriction has peaks {2,8,10} in the original indexing.
  Standardizing labels preserves comparisons, so the example is valid.
- **Asymptotic equivalences:** The distance/n is nonnegative and below 2.
  Markov's inequality and the usual bounded-variable split justify equivalence
  of mean convergence to zero and the required tail convergence. Positive
  finite support at maximum separation does not imply positive limiting mass.

## Sources and provenance

The four cited scholarly PDFs were independently retrieved and match the
author's complete byte counts and SHA-256 values. Relevant definitions and
theorem statements were inspected; three scope-sensitive pages were also
visually checked. This is not a full independent audit of those papers.

- [Twin peaks](https://arxiv.org/abs/1606.08025v2) formulates the negative
  conjecture on a torus. Theorem 4.2 is for a square with one peak;
  Proposition 6.5 and Theorem 7.2 concern trees with two peaks.
- [Floodings of metric graphs](https://arxiv.org/abs/1708.03825) fixes the base
  metric graph and refines its subdivisions. The square's growing cycle rank
  prevents direct application without additional uniform estimates.
- [Counting peaks on graphs](https://par.nsf.gov/servlets/purl/10130403)
  excludes peaks of degree less than two. This differs on leaves and isolated
  vertices, but not on the squares n>=2 used here.
- [Permutations with Given Peak Set](https://cs.uwaterloo.ca/journals/JIS/VOL16/Billey/billey2.pdf)
  uses one-dimensional interior peaks and omits endpoints.

The current author page still has no solution notice for Problem 9. A bounded
targeted literature search located no resolution. This is neither a universal
absence statement nor a novelty claim.

Both complete pinned corpus files were independently rehashed against the
immutable repository manifest. The catalog's Git blob and selected statement
hash match. The previously unreconstructed review hash is now independently
verified from the complete selected problem and report using the repository's
exact serialization algorithm:

`51bb0e2df33c9b416b7547bb1a8b2e4b27443f66463c1dff7a5d25a5bf85a806`.

Fresh exact-ID/code/topic PR searches, commit and branch searches, code searches,
the pinned 62-entry attempts directory, related-target groups, and the corpus
title scan found no prior attempt or duplicate target within those scopes.
The observed repository snapshot remains queued 0/5; that is the pre-attempt
state, not the mathematical disposition after the five authored approaches.
All retrieval and comparison limits are stated in `SOURCE_PROVENANCE_AUDIT.json`.

## Nonblocking verifier hardening

The author verifier relies on Python assertions. In a temporary copy, a corrupted
reference pair count is rejected in normal mode but is not rejected with Python
`-O`. The frozen default run is valid, and the mathematics is unaffected.
For robust replay use this audit's explicit-exception verifier, which rejects
the same negative control both normally and under `-O`. No frozen author file
was changed. See `results/harness_controls.json`.

## Final disposition

Accept the exact finite results, elementary proofs, and stated limitations.
Retain **unresolved, five approaches used**. No estimate comparing distant-pair
weight with total two-peak weight uniformly as n grows has been proved. The
conditioning rarity bound controls only the unconditional denominator from
above and does not close that gap. No remote repository writes, external
communications, source redistribution, or new solution claim were made.
