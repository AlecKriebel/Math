# Independent information-loss acceptance: staircase folding

Final shared PASS5, 14 October 2026.

Reviewed: `pass5_collective_windows/FOLDING_ENTROPY_OBSTRUCTION.md`, SHA-256 `3d996f5a49cb7cd9e18c2cfddcc36eea4a80e67d1f22bd2439096704174d3fa0`.

**Accepted as a counterexample to the specified low-turnaround recovery claim.** It gives no asymptotic estimate on the true window gaps and no counterexample under uniform avoidance sampling.

## Orientation and collisions

Reverse-complement of a vertical domino interchanges its upper/lower normalized states through inversion, giving D(A,C)=D(C^(-1),A^(-1)). On the shuffle word it reverses order and exchanges colors. This is the correct directed identity; symmetry under simply swapping A and C is not assumed.

V=12 and V*=231 are fixed by S. The extra singleton is after and below the V block. Each source edge has at most one active endpoint because active levels are nonadjacent. Its prefix ULLU supplies the greedy witness and excludes the interlocked two-color 1324 configuration. Singletons cannot create an ascending pair, and each color's internal forbidden subpatterns are absent. Thus the source paths are genuine canonical paths with distinct state sequences for distinct bit vectors.

Under inversion, skew-sum component order reverses. The two possibilities at an active output level both merge to V skew-sum1 skew-sum V. For either possible output color X, the up-run suffix X^epsilon and transformed down-run prefix X^(1-epsilon) concatenate to a single X. Therefore the two edge possibilities both give w X bar(w). Nonadjacency is precisely what avoids a second independent middle color whose order could record a bit.

Concatenating excursions preserves these identical states and words. Increasing pairs remain within their V blocks; no pair crosses skew components. A forbidden interlocking across different pieces cannot appear. This verifies the unrestricted output path. The fixed guard is a deterministic injection on that already identical output, so it cannot separate its multiple preimages.

## Fiber arithmetic and retained information

There are R(2W-2)+1 source vertices, normally of size two, plus R*a extra singletons. Thus n=R(4W-4+a)+2. The R top turns and R-1 shared bottom turns are duplicated, adding 4R-2 points; the canonical guard adds 2W. The displayed output size follows exactly.

All 2^(R*a) source state sequences have the same output, even with the listed turnaround copies, incident locations and excursion boundaries recorded. These records are equal for every source bit choice. Hence recovering the source requires distinguishing at least that many interior bit choices.

For fixed W, letting R tend to infinity gives fiber entropy per source point a*log2/(4W-4+a), and duplication overhead 4/(4W-4+a). With a=floor((W-1)/2), the subsequent W limit is log2/9 for the first and zero for the second. The guard overhead 2W/n vanishes in the first limit. The order of limits is explicit and legitimate; no width-growing-with-n estimate is inferred from a fixed-width growth statement.

A recoverable fold with genuinely negligible overhead and fiber entropy would compare the full class into a bounded-width class, yielding a lower bound on g_W and therefore an upper bound on delta_W. That direction is correctly distinguished from the lower gaps required by the adaptive criterion. The present map fails because its fiber entropy stays bounded away from zero even when turnaround overhead tends to zero.

The conclusion is limited to this map and its specified retained records. A transformation recording additional interior information, or a different recoverable map, is not ruled out. The witness family may be exponentially negligible in the full class, and no claim about its exact-uniform probability is made.
