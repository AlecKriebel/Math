# Research record: 9500009 / AMR-094-0009

Date: 2026-10-05 UTC. Outcome: **partial, unresolved**.
Five substantive approach families were explored. The numerical completion
estimates below are subjective estimates toward resolving the *full asymptotic
question*, not probabilities of truth and not validation scores.

## Source and identity gate, 19:20-19:26 UTC

The numeric landing page was requested first but could not be inspected: the web
reader reported it inaccessible and a direct public HTTP request returned 403.
The author-maintained source was successfully read. Its graph, conditioning,
distance normalization, and convergence target agree with the selected record.
Both complete pinned corpus files were hashed against the repository manifest;
the selected statement and complete prior report were inspected. The statement
hash matches the catalog. The catalog's stored review hash was not independently
reconstructed and is not presented as a verified report-content hash.

Read-only exact-ID/code, PR, commit, branch, and topic searches and an inspection
of the main-branch attempts directory found no actual prior attempt on this exact
target. The queue row was still rank 777, queued, 0/5. Related-target groups and
the corpus's labeling-peak titles supplied no second target to merge. These checks
do not exclude unpublished, deleted, or unindexed work.

The current author page lists the problem without a solution notice. Primary
research checked: *Twin peaks*, *Floodings of metric graphs*, *Counting peaks on
graphs*, and *Permutations with Given Peak Set*. A search finding of no resolution
is not a proof that none exists. No outside individuals were contacted.

## Approach 1: exact conditioned enumeration, 19:23-19:27 UTC

Mechanism: descending label order makes each local maximum exactly a vertex
arriving with no earlier neighbor. Allowed-root counts and inclusion-exclusion
produce the exact weight of each pair. A direct-root recurrence and a separate
peak-count recurrence provide cross-checks.

Result: proved recurrences and exact distributions for n=2,3,4. All pair counts
for n=2,3 were additionally checked against every permutation. Arithmetic uses
integers throughout. Finite results are saved, with no large-n extrapolation.

Gap: need a relative asymptotic estimate for distant pairs versus all pairs.
Exponential state growth and finite observations do not provide it.
Full-target completion estimate: 5%.

## Approach 2: local independence and rare conditioning, 19:25-19:28 UTC

Mechanism: realize labels by independent continuous ranks; pack disjoint closed
neighborhoods of interior vertices. This supplies independent Bernoulli peak
indicators before conditioning and an explicit exponential rarity bound.

Result: proved equations (6)-(7) in MATHEMATICS.md. An exact 3x3 certificate shows
that two corner peak indicators with disjoint closed neighborhoods cease to be
independent after conditioning on exactly two total peaks.

Gap: the conditional numerator and denominator both need control on a rare-event
scale. Local independence alone is unavailable under the required law.
Full-target completion estimate: 5%.

## Approach 3: rooted forests and support, 19:26-19:28 UTC

Mechanism: attach every nonroot to a vertex closer to a prescribed independent
root set, and count parent-before-child orders with a forest hook-length formula.

Result: a self-contained admissibility proof and a lower bound for every
nonadjacent pair. Explicit forest and labeling certificates cover all 122 possible
pairs across the tested grids, including maximal separation.

Gap: the bound counts only a subset in which the two roots receive the two highest
labels. No uniform comparison with all two-peak labelings was established.
Support at macroscopic separation is not positive limiting mass.
Full-target completion estimate: 5%.

## Approach 4: completion-weighted growth, 19:27-19:29 UTC

Mechanism: compute the exact continuation count h(S,k), obtaining the conditional
transition law by a ratio of completion counts. Consider whether a simple boundary
growth model could replace these unknown ratios.

Result: exact transition formula (8) and a 3x3 counterexample to uniform boundary
growth, with probabilities 13/56,15/56,1/2 rather than equal thirds. The broad
model distinction was already noted by Burdzy and Pal; this is a finite check.

Gap: estimating h(S,k) over the relevant spatial states retains the central
counting difficulty. No controlled comparison to Eden growth was obtained.
Full-target completion estimate: 5%.

## Approach 5: block reduction and lower-dimensional transfer, 19:28-19:31 UTC

Mechanism: try reducing the square to sub-squares, paths, trees, or subdivisions
where related peak-counting and flooding results are available.

Result: an explicit 4x4 two-peak labeling induces three peaks in its top-left 3x3
block. Thus the required constraint is not inherited by blocks. The torus and
fixed-metric-graph subdivision theorems also fail to match the target graph family;
the square's cycle rank grows as (n-1)². No transfer theorem was found.

Gap: need a new estimate controlling boundary-created peaks, block interactions,
or a uniform change of graph/model. This remains an unsupported bridge, so the
route was stopped rather than asserted.
Full-target completion estimate: 5%.

## Final boundary

The strongest verified deliverables are the exact finite computations and the
proved elementary bounds and counterexamples above. No complete candidate proof
or counterexample to the asymptotic question was produced. Do not mark this target
solved or candidate, infer novelty, or claim author/editor acceptance. The packet
is ready for a fresh independent audit of its limited claims. Repository writes,
queue status changes, and publication were not performed in this investigation.
