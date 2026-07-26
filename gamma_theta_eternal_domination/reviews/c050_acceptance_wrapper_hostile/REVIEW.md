# Hostile audit of the frozen C-050 acceptance wrapper

## Verdict

**`ACCEPT_EXACT_FROZEN_C050_WRAPPER`.**

No blocking defect was found in the exact frozen acceptance record or replay
wrapper audited here.  This verdict binds only:

- `results/order12_frontier_acceptance.json`, 7,726 bytes, SHA-256
  `e3b093085bafd124c228a29ef98c86341a45316dc02e11b565a138afe983d57a`;
- `repro/c050/replay.py`, 13,041 bytes, SHA-256
  `8e3c9f81e4cc38ecf392f44e750128bb108c20f8f1c53c8f72f0b43600405548`;
  and
- `repro/c050/README.md`, 1,067 bytes, SHA-256
  `251e393381eb4e61a9ba906b050207660231e96d5725176af2041fec8f6a240e`.

The independent audit program is
`reviews/c050_acceptance_wrapper_hostile/audit.py`, 25,678 bytes, SHA-256
`8d64392486647de32937e519fc6fa301e43bc8de62ebf3de01072b5efbe99abf`.
Its retained evidence is
`reviews/c050_acceptance_wrapper_hostile/evidence.json`, 11,489 bytes,
SHA-256
`c3b45cd7d00eb48b6e21e8b8d35aef2ded486c785426f4e7ad6f1e85dfe2647c`.

The verdict is deliberately narrower than the mathematical conjecture.  It
accepts the C-050 replay and binding layer for the certified order-12
extension **relative to the published through-order-11 premise**.  It does
not assert a universal proof, a counterexample, a campaign-only enumeration
through order 12, or anything about order 13 and above.

## What was checked

### Frozen trust root and every decisive binding

The replay pins both the exact size and SHA-256 of the acceptance record
before parsing it.  Consequently, changes to prose, scope exclusions,
parameter cases, verdicts, paths, hashes, sizes, or optional fields cannot
silently redefine what the wrapper accepts.

I independently parsed the acceptance record with duplicate-key and
nonfinite-number rejection.  I then checked all 20 ordinary `path`/`sha256`
bindings and the separately named frontier-review `evidence_path` binding.
The result is 21 unique paths, 69,387,613 bytes, with no duplicate decisive
path, no absolute path, no `..` traversal, no symlink endpoint or ancestor,
and no path escaping the campaign directory.  Every actual file size and
SHA-256 agrees with the frozen record.  The complete binding list is in
`evidence.json`.

The previous alternate-evidence gap is closed: the live
`reviews/order12_frontier_second_review/evidence.json` is checked at 13,261
bytes and SHA-256
`ac16ad66c791b06dcfec685ab322d77ad29cc747ebd358318bf81b245d9538e8`
before its JSON verdict and case-coverage fields are trusted.

One direct record,
`reviews/order12_k4_doublelex_publication_hostile_v2/REVIEW.md`, does not
declare `size_bytes`.  Its exact SHA-256 is nevertheless frozen in the
acceptance trust root and checked by the replay.  I independently measured
8,257 bytes and verified SHA-256
`ef48e4d3ca9357001483d9c522f817a9e337d6fd881f645c66750ee2f84ebd9b`.
This is a metadata uniformity limitation, not a trust or correctness gap.

### Exact parameter and publication boundary

The parameter interval is complete.  The frozen sources assert
\(k\geq3\) and \(n\geq2k+1\) for a connected counterexample; at \(n=12\)
the only integral cases are exactly \(k=3,4,5\).  The manifest binds:

1. the accepted complete C-035 order-12 \(k=3\) slice, including its explicit
   disconnected-case marker;
2. the graph-to-parent and DoubleLex theorems, exact formula, exact-CNF
   hostile review, publication verifier and LRAT, and conditional
   graph-transfer review for connected \(k=4\); and
3. the simplicial reduction, its hostile review, and the classical
   domination-bound source for \(k=5\).

It also binds the assembled theorem and its unblocked independent review.
Every status, expected verdict, and review verdict named in the acceptance
record was checked exactly.

The retained MMV TeX source says both that an attacker selects a vertex with
no guard and that one neighboring guard moves to that vertex.  Observation
5.6 states that there is no counterexample of order at most 11.  The
acceptance record accurately labels this as a published premise, explicitly
says the campaign did not reproduce the all-graph order-10 and order-11
enumerations, and excludes any universal-resolution claim.  No model-variant
or complement/clique-cover scope inflation was found.

### Independent formula census

An independent DIMACS parser recovered:

```text
variables            18,381
clauses              115,507
literal occurrences  1,190,774
maximum variable      18,381
```

This agrees with both the frozen acceptance metadata and the replay's
constants.  The exact file is 4,030,657 bytes with SHA-256
`14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.

### Private baseline and full replay

I copied every direct artifact plus the publication verifier's auxiliary
inputs into a private temporary campaign tree.  No symlink to the working
campaign was used.

Metadata mode exited zero in 0.279 seconds and returned:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS
bound_artifact_count = 21
solver_invoked = false
```

Full mode exited zero in 4.175 seconds and returned:

```text
VERIFIED_ORDER12_FRONTIER_BINDINGS_AND_EXACT_LRAT
VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY
verified_marker_count = 1
solver_invoked = false
```

Static inspection found one child launch in the C-050 wrapper (the exact
hash-bound publication verifier) and two in that verifier (`zstd` and the
fixed `lrat-check`).  No SAT solver is launched by either replay mode.

Full C-050 mode freshly checks the new \(k=4\) LRAT.  It does not rerun the
four older C-035 proof checks; C-035 enters through its frozen prior
acceptance and theorem.  Both the README and returned full-mode verdict say
exactly this.  That is a disclosed composition of accepted results, not a
claim that all historic proofs were rerun.

## Mutation resistance

Seven private corruptions were each required to return nonzero, emit no
success JSON, and contain a fail-closed rejection marker:

| Mutation | Result |
|---|---|
| Change a same-size field in the acceptance record | rejected by trust-root SHA |
| Append one byte to the acceptance record | rejected by trust-root size/SHA |
| Change a bound theorem byte | rejected by artifact SHA |
| Change the DIMACS header/census | rejected by exact-formula SHA; independent census also differs/rejects |
| Change the top frontier verdict | rejected by trust-root SHA |
| Change the nested frontier-review verdict | rejected by the alternate evidence SHA |
| Remove the assembled theorem | rejected as a missing regular file |

Independent strict-JSON probes also rejected duplicate keys and `NaN`.
Thus the earlier scope-mutation, missing evidence binding, stale metadata,
and omitted-artifact attacks do not survive the frozen trust root.

## Fresh-clone boundary

Of 30 files needed for the two replay modes, 29 were tracked or staged at
audit time.  The sole exception is
`tools/drat_trim_2023_05_22/lrat-check`, which is deliberately Git-ignored.
The README explicitly requires `tools/bootstrap_sat.sh` when the pinned
checker is absent.  A fresh clone therefore needs the documented bootstrap,
`zstd`, and a local compiler/toolchain.  The verifier then requires the
resulting checker binary to match its exact accepted binary hash.

This is adequate for the stated same-laptop campaign replay but is a
portability limitation for a permanent cross-platform archive.  A source
level or container/Nix-style reproducible checker build would improve the
eventual publication package.

The full-mode child stdout is parsed with ordinary `json.loads`, not the
duplicate-key/nonfinite hooks used for retained JSON files.  The exact child
generator is itself hash-bound and emits canonical `json.dumps` output, so
this does not open a mutation route in the accepted package.  Reusing the
strict loader there would nevertheless be a reasonable defense-in-depth
improvement.

## Defect ledger

- Blocking mathematical defects: **0**
- Blocking certificate defects: **0**
- Blocking replay/binding defects: **0**
- Blocking scope defects: **0**
- Nonblocking metadata uniformity limitations: **1**
- Nonblocking replay-composition limitations: **1**
- Nonblocking fresh-clone portability limitations: **1**
- Nonblocking defense-in-depth JSON limitation: **1**

The exact frozen C-050 wrapper is therefore accepted within its explicit
published-premise and finite-frontier scope.
