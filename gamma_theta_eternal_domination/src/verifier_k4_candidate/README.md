# Independent order-12, parameter-4 candidate verifier

## Claim boundary

This package checks a **decoded candidate**, not a SAT assignment or an
unsatisfiability certificate.  Acceptance proves directly from the supplied
graph and eternal family that

\[
  \gamma(G)=\gamma^\infty(G)=4<\theta(G)
\]

in the one-guard-moves model.  Rejection proves nothing about the existence
of another candidate.

The checker imports neither `synthesis_k4` nor either existing verifier core.
It uses ordinary set-valued neighborhoods and exhaustive standard-library
enumeration.  The graph order is fixed at 12, so all loops are bounded.

## Strict JSON schema

The root keys are:

- `schema`: `gamma-theta-order12-k4-candidate-v1`;
- `order`: exactly `12`;
- `edges`: unique lexicographically sorted pairs `[u,v]`, with `u<v`;
- `graph6`: the labeled graph6 record encoded by `edges`;
- `graph6_sha256`: SHA-256 of the ASCII graph6 record, without a newline;
- `edges_sha256`: SHA-256 of the compact JSON edge array;
- `claims`: the five fixed values `gamma=4`,
  `independent_domination=4`, `alpha=4`, `eternal_domination=4`, and
  `theta_lower_bound=5`;
- `dominating_set`: a sorted four-set;
- `independent_set`: the synthesis anchor `[0,1,2,3]`;
- `eternal_family`: a nonempty, sorted, duplicate-free array of sorted
  four-sets;
- `nonplanarity_minor`: an explicit `K5` or `K3,3` minor model using
  pairwise-disjoint connected branch sets;
- `imperfection_witness`: an explicitly ordered induced odd hole or
  antihole.

Unknown keys, duplicate JSON keys, Boolean values in integer positions,
non-finite numbers, noncanonical arrays, and files larger than 2,000,000
bytes are rejected.  The labeled graph6 record identifies the graph used for
verification.  This checker makes no canonical-label claim; canonicalization
is deliberately outside the validity path.

## Checks

The verifier independently performs all of the following:

1. recomputes graph6 and both identity hashes;
2. checks connectedness;
3. exhausts all 220 triples and checks the supplied dominating four-set;
4. exhausts all 792 five-sets and checks the anchored independent four-set;
5. checks every selected state dominates and every unoccupied attack has a
   successor obtained by moving exactly one adjacent guard;
6. checks every independent four-set occurs in the supplied eternal family;
7. enumerates all \(4^8=65,536\) anchor-normalized colorings of
   \(\overline G\);
8. directly enumerates all maximal independent sets, hence verifies
   `i=4` and well-coveredness;
9. checks a triangle, a 4-cycle, maximum degree at least four, an explicit
   nonplanarity minor, and an explicit induced odd hole or antihole.

Occupied vertices are deliberately excluded from the attack loop and counted
separately in the report.

The report separates `mathematical_counterexample_verified` from
`campaign_consistency_complete`.  The former depends only on graph identity
and the definition-level checks of \(\gamma\), the one-guard eternal family,
and \(\theta>4\).  Connectedness, the independently recomputed
\(\alpha=i=4\), forced-state redundancy, and the published class restrictions
are consistency checks.  If the definition-level result passes while one of
those checks fails, the status is
`VERIFIED_COUNTEREXAMPLE_WITH_CONSISTENCY_ALERTS`: the graph must be frozen
and the contradiction escalated, not discarded.

## Complete coloring trace

The optional `--color-trace` path is created only if it does not already
exist.  Its `GT4TRACE 1` format contains one deterministic line for each of
the 65,536 color rows.  Each line gives either the lexicographically first
monochromatic complement edge or marks the row proper.  The report binds the
complete trace by SHA-256.

```sh
PYTHONPATH=src python3 -m verifier_k4_candidate \
  candidate.json --color-trace candidate.gt4trace
```

Exit status is 0 whenever a mathematical counterexample is verified,
including the consistency-alert status; it is 1 when no counterexample is
verified and 2 for malformed input or an I/O failure.
