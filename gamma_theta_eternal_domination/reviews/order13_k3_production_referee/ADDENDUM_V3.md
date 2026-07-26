# Independent referee addendum v3: final order-13 k=3 workflow

## Verdict

**ACCEPT**

The final-v3 frozen bytes repair the remaining pre-`RUN_STARTED`
restartability gap.  Fresh process-loss injections at all four requested
creation points were explicitly recovered as no-child retryable nonclaims,
with the orphan directory moved intact outside the trusted run tree, the
original checkpoint left unchanged, the run auditable again, and a fresh
ordinary retry using the correct attempt number.

The earlier `REVIEW.md` and `ADDENDUM.md` REJECT verdicts remain unchanged and
historically correct for their older frozen targets.  This v3 acceptance is
bound only to the four hashes below.

No real SAT solver or proof checker was run.  All proof-like executions were
deterministic in-process synthetic fixtures.

## Frozen target

| File | SHA-256 |
| --- | --- |
| `src/search/order13_k3/production.py` | `e7052cd2d758ac653948c2231d3c556dcff822b1a511299ae43026a1de55e811` |
| `src/search/order13_k3/normalize_bdrat.py` | `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c` |
| `src/search/order13_k3/PRODUCTION_PROTOCOL.md` | `f5b6aa63c36fae363fdc2b0c6663f207bab09ad9bf70c525eb75fc4fc3805a34` |
| `tests/test_order13_k3_production.py` | `99308d0002712b91427f655d46b1a7f93d467bf63af28b218644df64f38557a5` |

The v3 generator verifies these hashes and all ten preserved v1/v2 referee
artifacts both before and after every replay.

## Disposition of the findings

| Finding | Final-v3 result | Disposition |
| --- | --- | --- |
| F1 — attempt formula not tied to frozen formula | A coherently rehashed substituted attempt CNF is rejected against the run-level frozen formula. | Repaired |
| F2 — phase records do not bind proof inputs | Exact LRAT substitution, forged before/after bindings, and four adjacent producer/consumer substitutions are rejected. | Repaired |
| F3 — altered or extra claim metadata accepted | Extra certificate key, false boundary, extra success detail, and extra normalization-report claim are rejected. | Repaired |
| F4 — uncheckpointed outcome cannot recover | Partial malformed bytes and a complete synthetic-success outcome are treated as opaque, moved intact to quarantine, replaced by a canonical recovered nonclaim, and never promoted. | Repaired |
| F4 adjacent — pre-`RUN_STARTED` orphan strands run | All four exact creation prefixes recover without a child; the main run becomes auditable and freshly retryable. | Repaired |

All six preserved v1 malformed-metadata regressions and all prior v2 hostile
mutations still reject.  Positive controls pass for the complete six-phase
record chain, LRAT conversion/checker/certificate crosslink, SAT CNF and direct
graph/game semantics, resource gates, tool and source bindings, binary proof
normalization, and read-only audit honesty.

## Pre-RUN_STARTED interruption matrix

The referee injected a `BaseException` into the actual `run` control flow at
each durable prefix:

| Injection point | Durable attempt entries | observed fsync calls | explicit recovery | fresh attempt |
| --- | --- | ---: | --- | ---: |
| after attempt `mkdir` | none | 0 | `RETRYABLE_NONCLAIM`, no child | 1 |
| after instance copy and file fsync | `instance.cnf` | 1 | `RETRYABLE_NONCLAIM`, no child | 1 |
| after durable attempt-config write | `instance.cnf`, `attempt-config.json` | 3 | `RETRYABLE_NONCLAIM`, no child | 1 |
| immediately before `RUN_STARTED` append | `instance.cnf`, `attempt-config.json` | 3 | `RETRYABLE_NONCLAIM`, no child | 1 |

For every row:

- ordinary audit and ordinary run first rejected the uncheckpointed orphan;
- `checkpoint-000000.json` remained byte-identical;
- recovery moved the directory to a new exclusive sibling quarantine;
- every contained byte and mode was preserved;
- the quarantine record had
  `claim_status: NO_SAT_OR_UNSAT_CLAIM`;
- post-recovery audit returned the prior `PENDING` state with attempt count 0;
- a fresh synthetic nonclaim run created attempt 1 and audited normally.

The same relation was replayed after an already checkpointed
`RETRYABLE_NONCLAIM`: orphan attempt 2 was quarantined, the prior attempt count
remained 1, and the fresh retry correctly used attempt 2.

## Opaque quarantine assessment

The implementation validates the orphan's structural envelope, not its
contents: exactly one extra entry, the exact next-numbered canonical path, a
real directory rather than a symlink, and a latest status in `RUNNABLE`
(`production.py:862-897`, `production.py:2460-2490`).

This is sufficient fail-closed recovery.  The referee placed unknown binary
bytes, malformed nested JSON, and a nested symlink in a canonical orphan.
Recovery moved the whole directory without parsing the bytes or following the
symlink; the external target was unchanged, the quarantine tree was
byte-for-byte and mode-for-mode identical, and the trusted run then audited
and retried normally.  A content-prefix whitelist is not required because no
contained object contributes to a checkpoint, certificate, candidate, or
claim.

The following envelope violations rejected without changing the run tree or
creating quarantine:

- a regular file or root-level symlink in place of the orphan directory;
- a wrong next attempt number;
- two extra attempt entries;
- an orphan while the latest state was `RUNNING_UNFINISHED_NONCLAIM`;
- an orphan while the latest state was frozen success.

## Outcome and quarantine crash behavior

Both malformed partial outcome bytes and a complete uncheckpointed synthetic
success were rejected by ordinary audit/run, moved intact as opaque regular
files, replaced by exact
`INTERRUPTED_ATTEMPT_RECOVERED_NONCLAIM` metadata, and terminally checkpointed
as `RETRYABLE_NONCLAIM`.  Neither path launched a child; each permitted a
fresh attempt 2.

Seven additional process-loss prefixes were injected during quarantine:
three while moving an orphan directory and four while moving an outcome file.
Every state remained a nonclaim, preserved the original opaque payload, and
had a safe continuation:

- before the move, explicit recovery could be retried;
- after a directory move, the main run was already auditable and an ordinary
  fresh run could proceed;
- after an outcome move, explicit recovery wrote the canonical nonclaim;
- after canonical recovery-outcome write but before its checkpoint, a second
  recovery quarantined that untracked outcome and completed safely.

A process loss immediately after `os.replace` but before record creation can
leave an intact sibling quarantine directory without
`quarantine-record.json`.  This is an operational cleanup/forensics
limitation, not a claim-safety or resumability failure: the directory is
outside the trusted run tree, the opaque payload remains present, and the main
run remains nonclaim and retryable.  The referee simulated process loss, not
hardware power loss before the subsequent directory fsync.

## Audit boundary

Acceptance is at the documented structural and cryptographic boundary.  The
positive read-only audit launched no child, changed no durable run bytes, and
reported `proof_freshly_replayed: false`.  This addendum does not claim a fresh
real LRAT replay.  Local hash chains provide integrity crosslinks, not
authentication against an actor able to rewrite every local record and hash.

## Tests and deterministic evidence

| Artifact | SHA-256 |
| --- | --- |
| `referee_regressions_v3.py` | `6b906927eb38736d19db3bc05c8320611940379c579f62501abf70aa1f52f0f7` |
| `run_readonly_upstream_tests_v3.py` | `0ba5734313b739670a75fb279cfa2f03f27346e399fb8230566c6fd720db0f2e` |
| `evidence_v3.json` | `7e86ee0692125e6782e4a9e7c5ff673f6a0dc92bdb73cae52aa7f8329b75a23f` |

The v3 evidence generator produced the same evidence hash on two consecutive
runs after its final edit.  The independent read-only wrapper passed 22/22
upstream tests.  The sole excluded test temporarily edits repository source
bytes; its behavior passed against the referee's isolated source mirror.
Author A separately reported the complete 23/23 focused suite passing twice.

## Exact replay commands

Run from the campaign root:

```sh
cd /Users/alec/Documents/Math-kissing5/gamma_theta_eternal_domination

shasum -a 256 \
  src/search/order13_k3/production.py \
  src/search/order13_k3/normalize_bdrat.py \
  src/search/order13_k3/PRODUCTION_PROTOCOL.md \
  tests/test_order13_k3_production.py

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 reviews/order13_k3_production_referee/referee_regressions_v3.py \
  --output reviews/order13_k3_production_referee/evidence_v3.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests_v3.py

shasum -a 256 \
  reviews/order13_k3_production_referee/referee_regressions_v3.py \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests_v3.py \
  reviews/order13_k3_production_referee/evidence_v3.json \
  reviews/order13_k3_production_referee/ADDENDUM_V3.md \
  reviews/order13_k3_production_referee/RESEARCH_LOG_V3.md
```
