# Order-13 k=3 production referee follow-up log

## 2026-07-26T17:34:48Z — final repaired freeze reviewed

- Bound only the final repaired hashes:
  - `production.py`:
    `0d4ab4e0bcd8d7175a2ba5339bd861c1ffac5da011d119a51565f0f8dc9e789b`
  - `normalize_bdrat.py`:
    `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c`
  - `PRODUCTION_PROTOCOL.md`:
    `b1e1cbd45a6388a2437be4ba490cd8b5163b12ddec8e36020380c09b99294e62`
  - `tests/test_order13_k3_production.py`:
    `5ac5f1a071d02db17c14d4e2a0f7715422c28ee4d9fa3099ee0531b00a4f1a8b`
- Verified before and after replay that all five original REJECT artifacts
  retained their exact hashes.
- Replayed F1 through F4 with fresh synthetic runs:
  - coherent attempt-CNF substitution rejected against the frozen formula;
  - post-check LRAT substitution rejected first at conversion output, and
    still rejected at lrat-check input after refreshing the conversion record;
  - forged before/after phase bindings rejected independently;
  - extra certificate key, false boundary, and extra outcome detail rejected;
  - ordinary and successful uncheckpointed durable outcomes quarantined to
    `RETRYABLE_NONCLAIM`, with a fresh attempt subsequently numbered 2.
- Adjacent producer/consumer probes rejected raw-proof, normalized-proof,
  solver-result, and normalization-report substitutions.
- All six preserved malformed-metadata v1 regression cases rejected.
- Positive controls passed for phase-record roles, SAT CNF/direct semantics,
  tools, resource gates, source binding, normalization, interruption recovery,
  and read-only audit honesty.
- Twenty repaired upstream tests that do not edit repository sources passed.
  The excluded source-mutation test was covered in an isolated source mirror.
- The final evidence generator ran twice with identical `evidence_v2.json`
  SHA-256
  `2e3650cf0f83908088dcac5e90218b4d7ef5cd18fb74f1dec362746666626073`.
- Partial outcome bytes and precheckpoint orphan directories still require
  manual remediation, but both fail closed and expose no claim or silent-resume
  path.
- No real SAT solver or proof checker was executed.
- Verdict: **ACCEPT** at the documented structural/cryptographic, non-fresh
  replay boundary.
- Best-guess completion: 100%.

## 2026-07-26T17:39:25Z — adjacent pre-RUN_STARTED audit

- Supersedes the provisional ACCEPT checkpoint above after the parent referee
  requested explicit injection at every durable prefix before `RUN_STARTED`.
- Added four process-loss injections:
  - after creation of the empty attempt directory;
  - after the instance copy and file fsync;
  - after durable `attempt-config.json` write;
  - immediately before `_append_checkpoint(... event="RUN_STARTED")`.
- At every prefix, `checkpoint-000000.json` remained byte-identical, no child
  launched, and no outcome appeared.
- Read-only audit, ordinary retry, and `--recover-interrupted` each rejected
  every prefix with
  `attempt directory count differs from checkpoint`.
- These states are fail-closed nonclaims, but the supported recovery interface
  cannot record a retryable nonclaim or permit a fresh attempt.  Manual durable
  tree editing is required.
- The behavior implements the protocol's narrow orphan-as-audit-failure rule,
  but does not realize its blanket interrupted-attempt recovery/fresh-retry
  statement.  It also leaves the adjacent pre-`RUN_STARTED` case expressly
  required by the original F4 recommendation unresolved.
- The exact F1, F2, F3, and post-outcome F4 regressions remain repaired.
- Revised verdict: **REJECT** for lack of complete interruption
  restartability.
- No real SAT solver or proof checker was executed.
- Best-guess completion: 100%.
