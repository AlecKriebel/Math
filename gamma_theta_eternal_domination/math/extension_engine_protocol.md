# One-vertex-extension engine: coverage and certificate protocol

## Status

This document links the finite coverage proof in
[`extension_search_scope.md`](extension_search_scope.md) to the executable
engine in `src/search/extension_killtest.py`.  It specifies a search; it does
not claim that the search has run or that its universe contains no
counterexample.

## Covered universe

The engine joins the byte-certified MMV Table 9 catalog with its independently
recomputed parameter table.  It accepts a host exactly when

\[
  \alpha(H)=\gamma^\infty(H)=3<\theta(H).
\]

It refuses to start unless this selects exactly 55 distinct, connected hosts
with distribution

\[
\begin{array}{c|c|c}
 |V(H)| & \gamma(H) & \text{number of hosts}\\ \hline
 10 & 2 & 2\\
 11 & 2 & 51\\
 11 & 1 & 2.
\end{array}
\]

For each host on vertices \(0,\ldots,n-1\), the engine creates one extension
for each integer mask \(s=1,\ldots,2^n-1\).  The new vertex \(n\) is adjacent
to vertex \(v\) precisely when bit \(v\) of \(s\) is one.  Hence the raw stream
contains

\[
  2(2^{10}-1)+53(2^{11}-1)=110\,537
\]

records, with no empty neighborhood.  This is the labeled cover proved
complete in `extension_search_scope.md`.

Every raw graph is passed to the pinned nauty/Traces 2.9.3 `labelg`.  The
canonical record is used only as a deduplication key: the ledger retains the
host, neighborhood mask, and raw graph6 string for every one of the 110,537
origins.  Therefore deduplication cannot discard coverage information.

## Exact filter

Each globally new canonical graph receives exact values of \(\gamma\) and
\(\alpha\).  A graph with \(\gamma<3\) is rejected.  A graph with
\(\gamma=3,\alpha=4\) is rejected.  The bounds
\(\gamma\leq3\) and \(3\leq\alpha\leq4\) are checked as invariants of the
selected-host extension construction.

For every graph with \(\gamma=\alpha=3\), the engine:

1. computes and directly checks the maximum-independent-state private-region
   obstruction;
2. runs verifier A's bitset greatest-fixed-point decision at \(k=3\);
3. runs verifier B's set-based colored-configuration-digraph decision at
   \(k=3\);
4. requires both decisions and both greatest closed families to agree.

The private obstruction is logged but never substitutes for either eternal
decision.  If both decisions are positive, the inherited induced host gives
\(\theta(G)\geq4\), so the graph is a search candidate.  Before any subsequent
graph is evaluated, an atomic frozen artifact records the raw extension,
canonical graph, exact provenance, edge list, and both eternal families.
Search then stops for independent certificate review.  A frozen search
candidate is explicitly not labeled a resolved counterexample.

Candidate state is represented redundantly by the frozen-artifact marker and
by every canonical or provenance ledger row categorized as
`candidate_eternal_3`.  Any indicator, even if the others are missing or
malformed, puts all later resumes in `candidate_review_pending` without
processing another origin.  Summaries retain a non-null artifact path or an
explicit unrecorded-candidate digest.
There is deliberately no `continue-after-candidate` option.  A future
reviewed-state transition requires a separate, authenticated protocol; the
search engine cannot clear or bypass candidate state.

## Interruption safety and audit data

The SQLite ledger is the authoritative checkpoint.  Each batch is one
transaction containing:

- every `(host_id, neighborhood_mask)` origin;
- its raw and canonical graph6 strings;
- the canonical graph's exact category and parameter values;
- origin multiplicity and \((\Delta\gamma,\Delta\alpha)\);
- the host's next unprocessed mask.

Initial schema creation, configuration metadata, all 55 host rows, and the
schema-version marker are likewise one explicit transaction, so an
interruption cannot publish a versioned but empty or partial ledger.
A crash before commit changes none of these; a crash after commit leaves all
of them.  The primary key on `(host_id, neighborhood_mask)` prevents replay
from double-counting.  JSON snapshots are written atomically after commits,
and a separate completed-host snapshot contains the SHA-256 of that host's
ordered canonical stream.  On a final host batch, the completed status and
canonical-stream hash are committed in the same transaction as the final
origins and next-mask value.  Resume also validates every completed host and
repairs the legacy crash state in which the hash alone is NULL; inconsistent
counts or a non-NULL hash mismatch fail closed.

The run configuration hashes the two input CSVs; the engine; the private
obstruction module; both evaluator A/B runtime modules and package glue; the
Python implementation, version, and executable; the active host list; and the
batch and resource limits.  The ordered runtime-source manifest and its
aggregate digest are part of the configuration digest, so a database cannot
mix evaluations made by different campaign source versions. Canonicalization accepts
only the exact audited local `labelg` executable with SHA-256
`ae8b1e7ef173c1665725e708bd7abd00b08ee4230ba2bd04117ec63d441274a0`,
in addition to the nauty 2.9.3 source-archive pin, and binds that hash into the
configuration.  The source archive must be present as well as hash-correct;
archive absence fails closed rather than merely recording the expected hash.
A later independent isomorphism/canonicalization audit remains
required for a certified finite result.  A database cannot be resumed under a
different configuration.
On full completion the engine atomically exports:

- a provenance CSV ordered by catalog host and neighborhood mask;
- a globally unique canonical-graph CSV with exact categories and
  multiplicities.

The final coverage audit must check that the provenance table has 110,537
rows, each host has exactly \(2^{|V(H)|}-1\) distinct masks, origin
multiplicities sum to 110,537, and all 55 host checkpoints are complete.  It
rejects completion if either a candidate marker or any canonical/provenance
`candidate_eternal_3` row exists, including inconsistent marker-only and
row-only states.

## Resource gate and launch gate

The executable is single-process and invokes one single-threaded `labelg`
subprocess per bounded batch.  Its defaults are 256 raw graphs per
transaction, 45 minutes of process wall time, and a 1 GiB resident-memory
gate.  A wall-time overrun drains the current host and stops at its completed
checkpoint; a memory overrun stops sooner at the last committed batch for
machine safety.

Before opening a writable file, the engine resolves every path role.  The
database, JSON checkpoint, provenance export, and unique-graph export must be
pairwise distinct and non-overlapping; the candidate directory cannot contain
or be contained by one of those file roles.  No writable role may resolve to
the catalog, parameter table, engine source, or pinned `labelg`, including
through a symbolic link.

The command line refuses to process even a sample unless
`--validation-gate-open` is supplied.  That flag is an explicit campaign
acknowledgment, not evidence that the gate was validly opened.  No execution
of the full 110,537-case campaign occurred while this engine was implemented.
