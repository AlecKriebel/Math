# Disposition of the 2026-08-27 fresh adversarial referee report

## Scope of this response

The report was treated as evidence to scrutinize, not as an instruction set.
Both blocking findings were independently reproduced against the v1.0.3
package before any repair.  Neither attack changed or contradicted a clean
graph record, rank decision, polynomial certificate, restoration edge,
transport, probe relation, theorem statement, or weak-sharpness witness.

## Finding 1: duplicate names in compressed JSON evidence

**Disposition: valid; repaired.**

The reported probe attack was reproduced after a coherent local certificate
reseal: Python's default JSON decoder accepted an earlier conflicting
`parent_anchor_id` and retained the later value.  The repair adds a bounded,
recursive duplicate-aware syntax boundary for plain JSON, gzip JSON, and gzip
JSONL.  Compressed documents and rows must also equal their compact sorted-key
UTF-8 serialization, including exactly one terminal line feed.  The boundary
rejects duplicate names at any nesting depth, non-finite values (including
overflowing numeric exponents), malformed UTF-8, noncanonical bytes, blank or
unterminated rows, oversized compressed inputs, oversized expanded documents
or streams, and oversized individual rows.

All load-bearing current producers and semantic verifiers that interpret
bound compressed evidence, including the independent finite replays, are
routed through the strict boundary.  Mutation constructors may use permissive
decoding only to demonstrate that an attack preserves Python's last-value
semantics; the strict production verifier must then reject that attack.  The
outer referee-bundle checker retains a separately implemented decoder so that
its syntax and canonicality check is independent of the producer's
implementation.

The mutation coverage now includes same-valued and conflicting duplicate
names for all three supported suffixes, a nested duplicate, noncanonical
compressed JSON and JSONL, missing terminal line feeds, all size limits,
`NaN`, `Infinity`, and `1e999`.  The exact reported probe-family attack is
installed into an isolated copy, coherently layer-resealed, and rejected by
the production verifier for `STRICT_JSON_DUPLICATE_NAME`, with no success
artifact.  Outer compressed mutations are likewise installed with a valid
outer reseal and passed through both complete bundle programs rather than
testing only a helper function.

## Finding 2: optimized Python erased certificate assertions

**Disposition: valid; repaired.**

The pristine portable verifier was confirmed to run under both `python -O`
and inherited `PYTHONOPTIMIZE=1`.  The referee's mechanism was real: a false
kernel vector could bypass an `assert`-based target-zero condition and produce
a successful-looking separator record.

Every documented release entry point and every portable sweep production
entry point now rejects optimized mode before doing work.  The shell launcher
performs the same preflight.  All 22 assertions in the portable atlas were
replaced with explicit invariant failures, including graph validity,
physical-domain, rank, source-nonzero, and target-zero checks.  An automated
entry-point matrix attacks both optimization mechanisms, requires the exact
guard diagnostic, and proves that no output, report, manifest, or record is
created.  A false-kernel negative control is rejected identically in normal,
`-O`, and environment-optimized execution.

The earlier README sentence claiming that every entry point in the entire
archive rejected `-O` was broader than the tested interface.  It is narrowed
to the documented release and enumerated portable production surfaces.  Some
historical or mutation-control scripts deliberately exercise optimized
execution and are not described as supported production entry points.

## Finding 3: absent legacy protocol names

**Disposition: not a defect; no code change.**

The package already maps every legacy name to its current authority, states
that the old names are absent, and runs every mapped current gate.  Adding
duplicate wrappers would create another interface without strengthening the
proof or reproducibility boundary.

## Finding 4: one underfull TeX box

**Disposition: harmless presentation note; no change.**

The box is not overfull, clipped, unresolved, or mathematically ambiguous.
Changing the source solely to suppress it would trigger another evidence and
PDF reseal without improving the rendered document.

## Fresh mathematical-projection check

The hardened compiler was run from scratch over all six four-port sources
with two workers.  It regenerated all 1,931 classes with the unchanged census

`845 separated + 20 isomorphic + 35 triangle + 997 restoration parent + 34 unresolved + 0 error`.

After removing only byte/provenance hashes, the combined projection root of
all 1,931 manifest summaries is
`6b6659a67a2a02d20c9865c891e84bf02cb1d4a2a9a198ba14e630bf907ad9ee`
for both the v1.0.3 baseline and the fresh run.  On the 19 mathematical fields
used by `compare_semantic_runs.py`, the 36 complete direct-record projection
root is
`201a616ee636d075f12d276585a66d88bebbeb73ad03018b11e61b18c6dc697d`
for both.  The fresh direct cubic, quartic, and quintic overlay and all eleven
direct mutation cases pass.

## Final qualification

An initial detached qualification exposed two additional output-interface
defects in the new evidence machinery: the direct mutation runner checked its
optimized-mode guard before removing a stale caller-owned report, and its
portable source-root policy assumed a fixed extraction depth.  Both were
repaired before promotion.  A subsequent independent audit found the
symmetric alias case in which a lexical source-tree output name was a symlink
to an external target.  Every affected routine report validator now rejects
an output when either its normalized lexical location or resolved target is
inside the source tree.  The focused regressions exercise both symlink
directions, hardlinks, late swaps, stale outputs, arbitrary-depth standalone
portable extraction, and optimized execution.  These repairs concern only
the qualification interface and changed no mathematical evidence.

The release is promoted only after the recursive lock, theorem crosswalk,
source documents, PDFs, deterministic source package, and referee archive are
resealed; the quick and full primitive replays and all controlling mutation
suites pass from a clean committed checkout; and two differently named clean
archive extractions agree.  Final commit, replay, archive, and tag identifiers
are recorded in the generated release metadata and final handoff.  No GitHub Release,
Zenodo deposit, or DOI is created by this repair cycle.
