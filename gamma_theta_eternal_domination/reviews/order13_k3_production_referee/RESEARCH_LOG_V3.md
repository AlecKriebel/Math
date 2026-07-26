# Order-13 k=3 production referee v3 log

## 2026-07-26T17:57:22Z — final-v3 frozen replay

- Preserved the original v1 REJECT bundle and the complete v2 REJECT addendum
  bundle byte-for-byte.
- Bound the new final target:
  - `production.py`:
    `e7052cd2d758ac653948c2231d3c556dcff822b1a511299ae43026a1de55e811`
  - `normalize_bdrat.py`:
    `a09f67d39932b6c3bb19b31a0792e4f47f515820c642e9418d3e374f555de18c`
  - `PRODUCTION_PROTOCOL.md`:
    `f5b6aa63c36fae363fdc2b0c6663f207bab09ad9bf70c525eb75fc4fc3805a34`
  - `tests/test_order13_k3_production.py`:
    `99308d0002712b91427f655d46b1a7f93d467bf63af28b218644df64f38557a5`
- Replayed the exact F1, F2, and F3 attacks; all rejected.
- Injected process loss after attempt mkdir, after instance copy/fsync, after
  durable config write, and immediately before `RUN_STARTED` append.
  All four orphans were moved intact to no-claim quarantine with zero child
  calls; the main tree audited again and fresh retry used attempt 1.
- Repeated orphan recovery after an existing retryable attempt; fresh retry
  correctly used attempt 2.
- Confirmed opaque structural-envelope policy:
  - unknown binary, malformed nested JSON, and nested symlink were preserved
    and quarantined without parsing or following them;
  - root symlink, regular file, wrong number, two extras, latest RUNNING, and
    latest frozen states rejected unchanged.
- Recovered malformed partial and complete-success uncheckpointed outcomes as
  opaque data.  Original bytes were preserved externally, a canonical
  recovered nonclaim replaced them, and success was never promoted.
- Injected seven process-loss prefixes during orphan/outcome quarantine.
  Every original payload remained present and every run had a safe nonclaim
  continuation.  A post-rename/pre-record crash can leave an unrecorded
  external quarantine directory; this does not affect trusted run state.
- Replayed all six v1 malformed-metadata cases and all four adjacent v2
  producer/consumer mutations; all rejected.
- Positive complete-chain, phase crosslink, SAT semantics, tool/source,
  resource, normalization, ordinary interruption, and read-only audit controls
  passed.
- Independent upstream wrapper: 22/22 passed.  The source-writing test was
  covered in the isolated mirror.  Author A reported 23/23 passed twice.
- Final v3 generator hash:
  `6b906927eb38736d19db3bc05c8320611940379c579f62501abf70aa1f52f0f7`.
- `evidence_v3.json` was identical on two final consecutive runs:
  `7e86ee0692125e6782e4a9e7c5ff673f6a0dc92bdb73cae52aa7f8329b75a23f`.
- No real SAT solver or proof checker was executed.
- Verdict: **ACCEPT** at the documented structural/cryptographic,
  non-fresh-replay boundary.
- Best-guess completion: 100%.
