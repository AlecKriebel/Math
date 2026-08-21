# Four-port optimization report

Date: 2026-08-20 PDT

The optimization pass was capped at 60 minutes and stopped within budget.
The frozen package was never edited.  All optimized code is in
`package/referee/k2p_offline_sweep_portable`.

## Measured resource profile

| Check | Wall time | Maximum RSS | Result |
|---|---:|---:|---|
| Quick locked census | 3.96 s | 1,388,380,160 B | pass |
| Exhaustive prepared/frozen graph audit (4,012 presentations) | 12.23 s | 1,501,200,384 B | pass |
| Full referee qualification | 45.61 s | 1,507,999,744 B | pass |

The 110 MB of pickle files expand to roughly 1.3–1.5 GB per independent
process.  Six-process parallelism is therefore unsafe on the 16 GB M1 Pro.

## Implemented changes

- one universe load per multi-source lane;
- one-worker default and two-worker maximum, with staggered balanced lanes;
- fixed-source quadratic and exact-graph preparation;
- target-local cache release and rank-map compaction;
- reuse of input-lock digests after pre-unpickle validation;
- manifest interval 25 instead of 1 (estimated writes 2.20 GB to 95 MB);
- exact dependency locking and single-threaded numerical-library environment;
- fail-closed semantic record/resume/merge validation;
- deterministic semantic record, manifest, and sweep hashes;
- guarded low-priority launch with disk, RSS, and signal propagation controls;
- repaired zero-column sparse-kernel handling and rational exact-oracle input.

## Equivalence and safety

Frozen and optimized mathematical fields matched on four hard cases plus four
ordinary source-5 classes.  Combined semantic SHA-256:

```text
74663db39da3e87bd3042ed16e1da7bf1cc72adcd5cc5414fb09ef3cf3913d59
```

The full verifier passed the exact-kernel differential suite, all 4,012
prepared/frozen graph comparisons, source counts/ranks, hard-case bindings,
interruption/resume behavior, and fail-closed mutations.

Production launch was attempted through the guard and stopped at preflight:
2.61 GiB free versus 20.00 GiB required.  This is a resource blocker, not a
mathematical or program failure.  The sweep was not started unsafely.
