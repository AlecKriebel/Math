# Soundness of the hole9 orphan-proof recovery

## Claim boundary

This note covers only the preserved, unreferenced hole9 attempt
`000170.akmx9xl0` at the already audited 170-cut checkpoint.  It explains why
the recovered proof check is logically sound.  It does **not** turn that
attempt into a CEGAR terminal marker, certify another template, prove template
coverage, or certify the whole \((n,k)=(12,3)\) slice.  Promotion remains
pending an independent hostile review.

## The source incident

The production runner generated the exact 170-cut CNF twice.  Both CaDiCaL
runs wrote the exact result line `s UNSATISFIABLE`, and the proof-producing run
wrote a nonempty ASCII DRAT proof.  The frozen protocol then called DRAT-trim
with `-I -f -W`.  It failed closed with exit status 80 because forward mode
warned about a deletion instruction for a pseudo-unit clause.  Consequently,
the runner wrote neither an attempt manifest nor an UNSAT terminal marker.
The raw CNF and proof were preserved as an incident, not accepted as a result.

## Independent reconstruction

The recovery verifier does not import the CEGAR runner or its formula
construction functions.  It independently allocates the edge, common-neighbor
witness, eternal-family, and move variables in the documented order; emits
the hole9 base constraints; and appends the 170 same-color clauses reconstructed
from the atomic checkpoint.

For a coloring \(c:V(H)\to\{0,1,2\}\), its cut is

\[
  \bigvee_{\{u,v\}:\ c(u)=c(v)} e_{uv}.
\]

Every non-three-colorable \(H\) satisfies this clause: otherwise \(c\) would
be a proper three-coloring.  Thus every appended cut is globally valid for
the target universe, independently of how its source SAT model was found.
The verifier also replays the cut hashes, source-attempt bindings, checkpoint
predecessor hashes, and append-only history chain.

The reconstructed DIMACS stream must be byte-for-byte equal to the preserved
CNF.  Merely agreeing on its reported dimensions is not accepted.

## Deterministic deletion stripping

The original proof is parsed as strict LF-terminated ASCII.  Every instruction
must be exactly one of:

- an addition `<literals> 0`;
- a deletion `d <nonempty literals> 0`; or
- a printable ASCII comment beginning `c `.

Literal tokens must be canonical nonzero signed decimal integers in the
DRAT range.  Duplicate literals, complementary pairs, extra zeroes, malformed
spacing, control bytes, blank lines, empty-clause deletions, and a nonfinal
empty-clause addition are rejected.

The derived proof preserves every byte of every addition and comment and
removes only lines that were successfully parsed as deletion instructions.
It is parsed a second time and must contain zero deletions.  Its byte hash,
size, and exact addition/deletion/comment counts are bound in the certificate.

## Why the primary checker flags are sound

The primary command is:

```text
drat-trim instance.cnf addition-only.rup.drat -I -f -W -U -t 60
```

- `-I` forces the proof to be parsed as ASCII rather than relying on format
  autodetection.
- `-f` checks additions in chronological forward order.
- `-W` makes any checker warning fatal.
- `-U` accepts only reverse-unit-propagation (RUP) additions; no RAT-only
  extension is trusted.
- `-t 60` bounds the checker's internal verification time, while the wrapper
  separately enforces wall-clock, CPU, resident-memory, and output-file
  limits.

If a clause \(C\) is RUP with respect to the current formula \(F\), unit
propagation derives a contradiction from \(F\land\neg C\).  Hence
\(F\models C\), so adding \(C\) preserves satisfiability.  Starting from the
preserved CNF, the checker validates every addition in the deletion-free
sequence.  The final validated addition is the empty clause.  A satisfiable
starting CNF could not, through satisfiability-preserving additions, reach a
formula containing the empty clause.  Therefore successful forward RUP
verification proves the preserved CNF unsatisfiable.

This argument uses no deletion semantics at all.

## What `-p` means, and why it is only a cross-check

The recovery also checks the original proof with:

```text
drat-trim instance.cnf original-proof.drat -I -f -p -W -U -t 60
```

In this checker, `-p` sets plain mode: deletion information is ignored.  The
checker therefore verifies the same monotone sequence of additions that is
materialized explicitly in the deletion-stripped proof.  Ignoring a deletion
is sound here because acceptance does not assume that a deletion-bearing
proof remains valid after changing its history.  Instead, DRAT-trim directly
checks each retained addition against the actual no-deletion history, under
`-U`, and reaches the empty clause.

The `-p` run is redundant diagnostic evidence.  The primary certificate is
the stored addition-only proof checked without `-p`; its soundness does not
depend on DRAT-trim's treatment of deletion instructions.

## Fail-closed operational boundary

The verifier checks the pinned checker binary and source-archive hashes,
holds the same campaign-global heavy-child lock as the production runner,
requires 512 MiB of reclaimable-memory headroom beyond the checker ceiling,
and applies process-group wall, CPU, resident-memory, and output-file limits.
It hashes the CNF, both proofs, checker executable, and complete source run
tree before and after checking.  It writes only to a fresh staging directory
outside the run tree, refuses overwrite, atomically installs the completed
package, and makes the package files read-only.

An exit status other than zero, timeout, memory breach, changed input,
nonempty checker stderr, any warning/error/failure text, or anything other
than exactly one `s VERIFIED` status line rejects the recovery.
