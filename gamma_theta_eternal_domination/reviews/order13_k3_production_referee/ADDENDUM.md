# Independent referee addendum: repaired order-13 k=3 workflow

## Verdict

**REJECT**

The final repaired bytes close the four exact attacks demonstrated in the
original review.  In particular, an uncheckpointed durable success outcome is
now quarantined as a retryable nonclaim and never promoted.  However, the
analogous crash window before `RUN_STARTED` remains unrecoverable.

At each of four durable prefixes between creation of the attempt directory and
the `RUN_STARTED` checkpoint, `audit`, ordinary `run`, and
`run --recover-interrupted` all reject the orphan with
`attempt directory count differs from checkpoint`.  This is fail-closed and
cannot create a SAT or UNSAT claim, but there is no supported operation that
records the interruption as a retryable nonclaim or starts a fresh attempt
without manual modification of the durable tree.  The workflow therefore does
not yet meet the restartability requirement stated in the original review.

No real SAT solver or proof checker was run.  All proof-like executions were
deterministic in-process synthetic fixtures.

## Scope and frozen target

This addendum applies only to the following final repaired bytes:

| File | SHA-256 |
| --- | --- |
| `src/search/order13_k3/production.py` | `0d4ab4e0bcd8d7175a2ba5339bd861c1ffac5da011d119a51565f0f8dc9e789b` |
| `src/search/order13_k3/normalize_bdrat.py` | `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c` |
| `src/search/order13_k3/PRODUCTION_PROTOCOL.md` | `b1e1cbd45a6388a2437be4ba490cd8b5163b12ddec8e36020380c09b99294e62` |
| `tests/test_order13_k3_production.py` | `5ac5f1a071d02db17c14d4e2a0f7715422c28ee4d9fa3099ee0531b00a4f1a8b` |

The original `REVIEW.md`, `evidence.json`, `referee_regressions.py`,
`run_readonly_upstream_tests.py`, and `RESEARCH_LOG.md` remain unchanged
byte-for-byte.  Their REJECT verdict remains the historically correct review
of the earlier frozen bytes; this addendum does not rewrite that record.

## Disposition of the original findings

| Finding | Repaired-byte result | Disposition |
| --- | --- | --- |
| F1 — attempt formula not tied to frozen formula | A coherently rehashed substituted attempt CNF is rejected with `attempt configuration differs from frozen inputs`. | Repaired |
| F2 — phase records do not bind proof inputs | Post-check LRAT substitution, independently forged before/after bindings, and adjacent producer/consumer substitutions are rejected. | Repaired |
| F3 — extra or altered claim metadata accepted | Extra certificate keys, a false claim boundary, extra success details, and an extra normalization-report claim are rejected by exact-shape checks. | Repaired |
| F4 — durable outcome before terminal checkpoint cannot recover | Both ordinary and synthetic-success durable outcomes are quarantined by `UNTRACKED_OUTCOME_QUARANTINED` as `RETRYABLE_NONCLAIM`; a fresh attempt is numbered 2. | Exact reported window repaired |
| F4 adjacent requirement — orphan before `RUN_STARTED` | Every tested durable prefix fails closed, but explicit recovery and fresh retry are unavailable without manual tree editing. | **Not repaired** |

The six preserved malformed-metadata v1 cases are still rejected, as are all
four adjacent output-crosslink mutations.  Positive synthetic controls pass
for all six phase-record roles, the conversion-to-checker-to-certificate LRAT
crosslink, complete SAT-model CNF and direct graph/game replay, tool/source
bindings, resource gates, proof normalization, ordinary checkpointed
interruption recovery, and read-only audit honesty.

## Decisive remaining finding

### A1 — Every pre-`RUN_STARTED` durable prefix strands the run

Severity: **high**

`run` creates `attempts/attempt-000001`, copies and fsyncs the formula, durably
writes `attempt-config.json`, and only then appends `RUN_STARTED`
(`production.py:2378-2426`).  Recovery is reachable only after `_load_run`
accepts the checkpoint/attempt relation and reports
`RUNNING_UNFINISHED_NONCLAIM` (`production.py:2357-2369`).  An orphan attempt
directory makes `_audit_attempts` reject the directory count before that
recovery branch can execute.

Fresh process-loss injections produced these exact durable states:

| Injection point | Durable attempt entries | `audit` | `--recover-interrupted` | ordinary retry |
| --- | --- | --- | --- | --- |
| after attempt `mkdir` | none | rejects | rejects | rejects |
| after instance copy and file fsync | `instance.cnf` | rejects | rejects | rejects |
| after durable attempt-config write | `instance.cnf`, `attempt-config.json` | rejects | rejects | rejects |
| immediately before checkpoint append | `instance.cnf`, `attempt-config.json` | rejects | rejects | rejects |

For every row, `checkpoint-000000.json` remained byte-identical, no outcome
was written, no child was launched, and all three operations rejected
`attempt directory count differs from checkpoint`.  Thus all four states are
safe nonclaims, but none has an explicit durable retryable-nonclaim transition.

The protocol says that an interrupted attempt can be explicitly recovered and
that a later `run` starts a fresh exclusive attempt
(`PRODUCTION_PROTOCOL.md:63-66`).  It also says orphan directories are audit
failures (`PRODUCTION_PROTOCOL.md:68-77`).  The implementation realizes the
latter rule, but not a resumability path for the former statement in these
ordinary write-order windows.  This is also the adjacent case expressly called
out in the original F4 recommendation.

A repair should recognize only a tightly bounded canonical next-attempt
prefix, validate every file that is present, and durably seal it as a nonclaim
before permitting the next attempt.  Alternatively, attempt reservation can
be made a checkpointed state before the visible attempt directory is created.
Unknown files, noncanonical paths, malformed configurations, and any claim
metadata must continue to fail closed.

## Audit boundary

The positive complete-chain audit is a structural and cryptographic audit of
the local records.  It launches no child and reports
`proof_freshly_replayed: false`; this review therefore does not assert that a
real LRAT proof was freshly replayed.  Local hashes also provide integrity
crosslinks, not authentication against an actor able to rewrite every record
and its hash chain.  Neither limitation changes the interruption finding.

## Deterministic evidence

| Artifact | SHA-256 |
| --- | --- |
| `referee_regressions_v2.py` | `aa69db3f287fea20fa9de426e406c8843f47abd65a94fa09966bd6333e841fa7` |
| `run_readonly_upstream_tests_v2.py` | `07029364acff8acca83918841db82ad66951e419e93c2e3fee609b23b3a90bc4` |
| `evidence_v2.json` | `f9e1ad4fcc5e7ddaa8c446a7b28527622b0f78d790d2b15746668462400d489b` |

The repaired upstream suite contains 21 focused tests.  The independent
read-only wrapper passed the 20 tests that do not edit repository source
files; the excluded source-mutation behavior passed against an isolated source
mirror.  The v2 evidence generator uses only temporary fixtures below this
review directory and verifies the frozen target and preserved-v1 hashes both
before and after execution.

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
  python3 reviews/order13_k3_production_referee/referee_regressions_v2.py \
  --output reviews/order13_k3_production_referee/evidence_v2.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests_v2.py

shasum -a 256 \
  reviews/order13_k3_production_referee/referee_regressions_v2.py \
  reviews/order13_k3_production_referee/run_readonly_upstream_tests_v2.py \
  reviews/order13_k3_production_referee/evidence_v2.json \
  reviews/order13_k3_production_referee/ADDENDUM.md \
  reviews/order13_k3_production_referee/RESEARCH_LOG_V2.md
```
