# Attempt 4: Exact finite search for pairing obstructions

Timestamp: 2026-10-03 13:58 UTC. Budget: 4/5. Exact-target completion estimate: 5%.

Following the fixed-matching obstruction, search both the matching and order. A recursive search contracts two original singleton parts at a time, recomputes red adjacency directly from the original graph, and rejects prefixes exceeding D. Once ceil(n/2) parts remain, arbitrary completion is safe at D=floor((n-1)/2). Failure is memoized only by the current partition, which suffices because the quotient depends on that partition, not its history.

Exhaustive results: all 33,867 labeled graphs with 1<=n<=6 admit the required bound. Tight bounds were also verified for n<=3 using D=0. Consequently the exact maxima for n=1,...,6 are

0, 0, 0, 1, 2, 2.

The upper bounds are finite exhaustive certificates; P4 and C5, together with C5 plus an isolated vertex, give the last three matching lower bounds. The values are verification results, not claimed as novel mathematical discoveries.

A second implementation verifies each returned sequence by incremental nonedge/black/red trigraph updates, rather than recomputing from the original partition. All certificates pass. The deterministic certificate-stream hash and graph counts are in checks/verification_results.json. The stream can be regenerated with the scripts; no external graph library or downloaded solver is used.

A reproducible seed-481 sample of 250 labeled graphs at each order n=7,...,12 (1,500 total) also had a pair-first sequence at the conjectured ceiling. This is a sample, not an exhaustive result or statistical certificate for the conjecture. A sample's returned sequence need not be optimal.

Attempted disproof route: find a small graph where no matching and order attains the conjectured ceiling. No such graph was found within the stated finite scope. This leaves the all-orders problem unchanged. Finite agreement cannot supply a uniform invariant; the cyclic obstruction from Attempt 3 still rules out selecting an arbitrary individually good matching.
