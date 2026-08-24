# Adversarial audit of the unified 36-record direct closure

Date: 2026-08-20 (America/Los_Angeles)

## Verdict

The mathematical direct-residual claim passes independent exact replay.  The
production run contains exactly 36 unresolved records, every unresolved record
is in the direct/no-dummy stratum, and the independent obstruction overlay
covers them with the census

- 22 theta0 repair-1 quintic port-orbit obstructions;
- 12 lower-theta quartic obstructions; and
- 2 theta3 cubic obstructions.

For every record, an implementation distinct from the unified verifier
recompiled the graph map through the production atlas compiler and obtained an
identically zero target pullback, a nonzero source pullback over the rationals,
and a nonzero value at the stated strict physical K2P point.  The latter check
includes the four selected pendant edges and the multihomogeneous pendant
factor.  The exact direct-residual set after this overlay is empty.

This establishes the advertised noncontainment of each of the 36 strict source
images in its directed target variety.  It does not, by itself, certify the
restoration children or the other global gates needed for the final network
classification theorem.

## Production census reconstructed independently

- Raw records reopened and self-hash checked: 1,931.
- Source class counts: 536, 747, 276, 276, 64, 32.
- Status counts: separated 843, isomorphic 20, triangle 35,
  restoration-parent 997, unresolved 36, error 0.
- Recomputed six semantic manifest roots: all agree with the production
  manifests and merged status.
- Recomputed semantic sweep root:
  `33b894a62f4bb993e580a03527d2d3509122ba4e84f1056ca70f4991ce04b899`.
- Exact residual source census: source 1 has 22, sources 2--4 have 4 each,
  and source 5 has 2.

The audit also independently reconstructed each source graph, selected target
graph, graph hash, target descriptor, target port match, and production record
binding for all 36 records.

## Exact replay and resource measurements

The current unified verifier replayed byte-identically to its checked-in
certificate:

- verifier SHA-256:
  `0b379d2631d97de5804eaf31511544d3d77368bfcc9df1381b12127c107b2f36`;
- certificate SHA-256:
  `35c52cfd3e9822c5f3ac88d4cd07c81e80218fc181368fb88be6449e8dcd9d19`;
- payload SHA-256:
  `396ef2939762d94570dd90dbf3cea13309f6c53b135ed1c560ab3b8ed52d4740`;
- measured wall time: 4.66 seconds;
- measured maximum resident set size: 87,556,096 bytes.

The independent full-census/compiler replay is deterministic on repeat:

- audit script SHA-256:
  `b98b1d1995c23d4336acb3e50fe71a3b12f15182402c2177183450df52a3659a`;
- audit certificate SHA-256:
  `c110ab2b0099f1d7c7f36fc40e0a10fe8cfab461e509c5d0bd3cce8a280e6f38`;
- payload SHA-256:
  `4b6a76de7199ba3d7a9a5b0426fdce2c14e86126117d075684082fdd44e317b9`;
- measured wall time: 2.75 seconds;
- measured maximum resident set size: 89,030,656 bytes.

## Adversarial mutation results

The black-box suite ran ten cases.  In ordinary Python execution the unified
verifier rejected all seven corruptions directed at its declared 36-record
inputs:

- a changed quintic coefficient;
- a changed quartic transport mapping;
- a changed cubic coefficient;
- a missing expected residual record;
- swapped expected residual records;
- a changed expected record port mapping; and
- a missing expected residual manifest entry.

Local independent checks also rejected dropped or duplicated coverage, a
changed record binding, a changed quartic coefficient, and invalid family
swaps (including F113 or the cubic assigned to source 2, class 112).

The mutation harness and report hashes are

- harness:
  `100326a2789734432a2c12f7a1bf1bba9550723c59b60b6c0f53cbcc6101dff7`;
- report:
  `2a4697f45f522bcd9e94550bce409abb5b21af838f9b13c5ff827099926d71df`.

## Referee-package gaps to repair

Two black-box cases expose fail-closed gaps in the harness, not failures of the
36 mathematical certificates.

1. The verifier implements its checks with Python `assert`.  Running it with
   `python -O` removes those checks and accepted the deliberately corrupted
   quartic transport artifact.  The package should explicitly reject
   `not __debug__` at startup or replace load-bearing assertions with explicit
   exceptions.

2. The unified verifier checks the 36 expected residual records but does not
   reconstruct the complete manifest census or semantic sweep root.  Deleting
   a nonresidual production record left stale completion/root fields and the
   unified verifier still passed.  Before release, either invoke a full
   integrity validator or validate the exact ID lists and summaries in all six
   manifests, recompute their semantic roots and the merged sweep root, and
   then reopen the 36 residual records.  The independent audit proves that the
   current production snapshot is internally consistent; this is a packaging
   hardening requirement.

The release must also move or copy the proof inputs currently under `work/`
and `runs/higher_degree/` into the locked referee package, bind the independent
audit certificate (not merely its script), and avoid relying on this machine's
absolute run path.
