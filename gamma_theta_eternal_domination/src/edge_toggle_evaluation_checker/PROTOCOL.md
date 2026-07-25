# Third mathematical audit of the edge-toggle ledger

## Scope and claim boundary

This checker proves, independently for every canonical graph in the completed
edge-toggle unique ledger,

\[
  \gamma(G)<\gamma^\infty(G)
\]

in the ordinary-set, one-guard-moves model.  It does not generate edge
toggles.  The separately bound coverage report certifies that the search's
25,641 labeled toggle origins map to exactly the 19,136 canonical ledger
rows.

Passing this audit therefore rules out a counterexample among that finite
edge-toggle ledger.  It is not an enumeration of all graphs of order 11 or 12
and does not resolve the universal \(\gamma\)--\(\theta\) conjecture.

## Independence and byte binding

The checker imports neither `search.edge_toggle_killtest`, verifier A,
verifier B, nor the earlier `evaluation_checker`.  Its domination and eternal
game routines are new integer-bitmask implementations.  The only reused graph
code is the strict, order-at-most-12 graph6 parser and immutable `Graph`
container in `src/coverage_checker/graph.py`.  That exact file has an embedded
SHA-256 pin and is also listed in the checker-source manifest.

The certificate header and final report bind:

- the completed edge-toggle SQLite database and checkpoint;
- the provenance and unique CSV exports;
- the completed independent edge-toggle coverage report;
- the coverage report's own binding digest and origin-chain digest;
- the frozen graph6 parser; and
- every checker, protocol, and test source file.

The database is opened `mode=ro&immutable=1` only after rejecting WAL,
shared-memory, and rollback-journal companions.  Its integrity, foreign keys,
schema version, exact table/column sets, and every unique CSV field are
checked.

## Per-row domination proof

The graph is parsed independently from its stored canonical graph6 string.
The checker ignores the stored domination value while constructing a proof.
It scans subsets in increasing size until it finds the first dominating set
and requires the resulting value to be two or three.

Each certificate row contains:

1. an explicit dominating set of size \(k\); and
2. for every \((k-1)\)-vertex subset, in lexicographic order, an explicit
   vertex not dominated by that subset.

The replay verifier checks every blocker literally.  Monotonicity of
domination then excludes every smaller set as well, proving
\(\gamma(G)=k\).  Only after this proof is established is the independent
value compared with the two stored gamma fields.

## Complete one-guard deletion proof

At \(k=\gamma(G)\), the initial family is recomputed as every dominating
ordinary \(k\)-subset.  It must be nonempty.

For a current family \(F\), a configuration \(D\) is deleted precisely when
there is an **unoccupied** attacked vertex \(r\notin D\) for which no guard
\(u\in D\cap N(r)\) has

\[
  (D-\{u\})\cup\{r\}\in F.
\]

Every tested successor removes exactly one guard, moves it along the edge
\(ur\), adds the attacked vertex, has exactly \(k\) distinct occupants,
dominates the graph, and remains in the current family.

Deletion is simultaneous.  Each certificate stores every deleted
configuration and its first failing attack in every round.  The replay
implementation does not call the generator's successor predicate: it
independently recomputes the complete doomed set for the current round and
requires exact equality with the record.  All initial configurations must
eventually be deleted.  The resulting empty greatest fixed point proves
\(\gamma^\infty(G)>k=\gamma(G)\).

## Certificate installation and replay

The certificate is canonical ASCII NDJSON with one header, one independently
replayable record per ledger row, and one footer.  The footer records a hash
of the exact row lines and aggregate counts.

Generation proceeds as follows:

1. write and fsync a temporary certificate in the destination directory;
2. replay the complete temporary stream;
3. atomically replace the installed certificate;
4. replay the complete installed stream;
5. rehash every bound input and source; and
6. atomically write the passing JSON report.

The separate `--verify-only` invocation performs another complete replay and
requires the installed report's certificate hash, binding, and summary.

Production commands:

```text
PYTHONPATH=src python3 -m edge_toggle_evaluation_checker
PYTHONPATH=src python3 -m edge_toggle_evaluation_checker --verify-only
```

## Stored-field reconciliation and limitations

For every row, the independently proved gamma must equal both stored gamma
fields.  Both stored one-guard eternal values must agree and exceed the
independent gamma, and the stored category must be
`gamma_below_eternal`.  The report records the full stored
`(gamma, alpha, gamma_infinity, theta, category)` census.

The exact stored alpha, theta, and gamma-infinity values are not independently
proved by this checker.  They are reconciliation data only.  The mathematical
conclusion uses only the independently proved equality
\(\gamma(G)=k\) and strict lower bound \(\gamma^\infty(G)>k\).
