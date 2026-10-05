# Independent negative controls

All tests use exact integer or rational arithmetic. They are diagnostics for
incorrect substitutions, not asymptotic counterexample evidence.

1. **Induced versus ordinary biclique.** K4 has an ordinary spanning K2,2,
   hence ordinary biclique order 4, but its maximum induced biclique has order
   2. Within-side nonedges cannot be omitted from the pattern probability.
2. **Partition versus overlapping cover.** Independent exact dynamic programming
   gives bp(K4)=3 and minimum biclique-cover size 2. The cover optimum cannot be
   substituted for the partition parameter. The candidate's distinct K3 overlap
   witness was also rerun and passed.
3. **Independence versus induced-biclique order; unbalanced parts.** K1,4 has
   alpha=4 and beta=5. A balanced-only count would miss this allowed pattern;
   the actual union bound includes it.
4. **Other edge probabilities.** At p=1/3, fixed K1,3 and K2,2 patterns on four
   labelled vertices have probabilities 8/729 and 4/729, respectively. Their
   equal probability at p=1/2 must not be transferred to other p unchanged.
5. **Empty-side convention.** An edgeless graph on five vertices has beta=0
   under the candidate's nonempty-side convention and beta=5 if empty sides
   are allowed. These finite parameters can differ. The enlarged-family
   first-moment bound works for both and needs no equality between them.

The candidate's three original controls pass without modification. The fresh
suite additionally checks exact partition optima, hereditary reductions, empty
conventions, the explicit deterministic star construction and exact ceiling
arithmetic. Detailed reproducible output is in INDEPENDENT_RESULTS.json.
