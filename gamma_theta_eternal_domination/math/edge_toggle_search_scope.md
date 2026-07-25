# Complete one-edge-toggle search around extension near-misses

## Status

This document specifies a finite, resumable search.  It does not claim that
the search has run, that no candidate exists, or that the universal
\(\gamma\)–\(\theta\) conjecture is resolved.

## Exact seed universe

The source is the byte-bound `results/extensions_unique.csv` with SHA-256

`e7f0ffa459d74a67a3a647e19ee5669652ff1679302b3b62daaef299ee02945e`.

The engine also requires the passed independent extension coverage audit
`results/extension_coverage_audit.json` with SHA-256

`523b3a57ef9afac2b8c921564afcf3fcd8fdbe7719984014f3b0f8e80da8e7cb`,

and checks that this audit binds the unique table.  Exactly 391 canonical
source rows have category
`private_obstruction_eternal_false` (106 rows) or
`eternal_false_without_private_obstruction` (285 rows).  There are 15
order-11 seeds and 376 order-12 seeds.  Every selected seed is connected and
has the stored conditions \(\gamma=\alpha=3\) and no eternal family at
\(k=3\).

## Coverage proof

For a seed \(H\) on the canonical vertex set
\(\{0,\ldots,n-1\}\), enumerate the lexicographically ordered set

\[
  \binom{V(H)}2=\{\{u,v\}:0\leq u<v<n\}.
\]

For each pair, complement exactly that adjacency bit: delete \(uv\) when it
is an edge and add \(uv\) otherwise.  Thus every graph at edge-edit distance
exactly one from that labeled seed appears exactly once in its raw stream.
The full labeled-origin count is

\[
  15\binom{11}{2}+376\binom{12}{2}
  = 15\cdot55+376\cdot66
  = 25\,641.
\]

Pinned nauty `labelg` canonicalizes each raw graph.  Global deduplication
controls only repeated evaluation; the ledger retains every
`(seed_id,pair_index,u,v,action)` origin, so isomorphic collisions cannot
remove coverage.

The canonical extension seeds no longer identify which vertex was the added
extension vertex.  No attempt is made to reconstruct that provenance.
Toggles that happen to be incident with that vertex are included along with
all other pairs.  They may duplicate earlier extension coverage, but this is
harmless redundant coverage and is never used to prune the universe.

## Exact candidate test

Disconnected toggles are recorded and pruned using the proved connected
reduction.  For each globally new connected canonical graph, the engine
recomputes:

1. \(\gamma\) independently with verifier A and verifier B;
2. \(\alpha\) independently with verifier A and verifier B;
3. the first winning one-guard eternal family independently at every
   \(k\geq\gamma\), requiring both decisions and greatest families to agree;
4. \(\theta\) with verifier B's exact complement-coloring solver, cross-checked
   against verifier A's exact clique-partition dynamic program.

It checks \(\gamma\leq\alpha\leq\gamma^\infty\leq\theta\).  A graph is a
candidate precisely when

\[
  \gamma(G)=\gamma^\infty(G)<\theta(G).
\]

Before any later graph is evaluated, an atomic frozen artifact records the
seed, toggled pair and action, raw and canonical graph6 strings, edge list,
parameters, and both eternal-family representations.  Search then returns
`candidate_review_pending`.  A frozen search artifact is not a certified
counterexample until the standalone counterexample protocol, including a
checkable clique-coloring lower-bound trace, is complete.

## Resume and source guarantees

The SQLite ledger is authoritative.  Each batch transaction commits origins,
new canonical evaluations, multiplicities, and the next pair index together.
On a seed's final batch, its `complete` status and ordered canonical-stream
SHA-256 are in that same transaction.  Schema, configuration metadata, all
391 seed rows, and schema version are also created in one transaction.

Candidate state is redundant: a frozen marker, a canonical candidate row, or
a provenance candidate row independently blocks every resume and completion.
There is no continuation override.

The configuration binds the seed table, extension audit, exact local
`labelg` executable, nauty archive, Python runtime, engine, imported
canonicalization code, and both evaluator stacks.  Writable path roles are
resolved before opening: outputs cannot alias each other, a candidate
directory, a bound input, or runtime source, including through symlinks.
The derived `<checkpoint-stem>.seeds` directory and all 391 per-seed JSON
targets are produced by the same helpers used during validation; their
resolved equality and ancestor/descendant relationships are checked against
the database, main checkpoint, both CSV exports, candidate directory, bound
inputs, and runtime sources.  Thus a per-seed atomic JSON replacement cannot
replace or nest within the authoritative SQLite ledger or another artifact.
NaN, infinity, Boolean, and non-integer gate values fail closed.

JSON snapshots are atomic human-readable mirrors.  Completed-seed snapshots
contain stream hashes.  Full completion additionally requires the internal
coverage audit to verify all 25,641 pair indices and multiplicities and the
absence of candidate state, then atomically exports origin and unique-graph
CSVs.  A publication-grade finite claim still requires a separately written
coverage/isomorphism checker.

## Launch gate

The implementation is single-process, bounded, and resumable.  Its CLI
refuses to start without `--validation-gate-open`.  No full 25,641-toggle
search was launched while implementing this lane.
