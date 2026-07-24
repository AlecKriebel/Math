# Full delete-two/add-three compact catalog screen

Status: **INCOMPLETE — RESOURCE-GATED STOP**

Evidence category: **REPRODUCIBLE COMPUTATIONAL OBSERVATION**

This track screens the Cartesian product of all 328 pinned
\((5,5;42)\) catalog graphs and all \(\binom{42}{2}=861\) deleted vertex
pairs.  Each fixed induced 40-vertex core is completed by three new
vertices.  An unchecked negative result concerns only that fixed core; it
is not a proof of global order-43 nonexistence and does not change a Ramsey
bound.

## Frozen plan and compact representation

The immutable production plan is
`results/benchmark_plans/core_completion_catalog_k2_full_screen_v1.json`
(SHA-256
`7f9d6dfe31e80f186d77d74703961e851b74f2c636c7acf68d98cc77e5ad2334`).
It fixes:

- four balanced contiguous 82-line shards, with 70,602 cores per shard;
- 282,408 cores in exact catalog-line/deleted-pair lexicographic order;
- 0.5 seconds and 100,000 search nodes per core;
- four simultaneous persistent workers and a 10,800-second wall cap;
- a 2,147,483,648-byte free-space reserve and a 50,000,000-byte hard
  retained-output cap;
- immediate atomic SAT-model preservation, reconstruction, and both
  exhaustive Python and independent C++ bitset verification;
- no proof generation or negative certification for UNSAT statuses.

Each `K2SCRN01` shard has a 64-byte header and one fixed 48-byte record per
core.  The complete four-shard binary payload is exactly 13,555,840 bytes.
Including the frozen metadata allowance, the ordinary retained-size
projection is 16,055,840 bytes, below the hard cap.

The preregistered line-1 benchmark independently parsed all 861 records,
all as `OBSERVED_UNSAT_UNCHECKED`, in 71.828832 seconds.  Its compact file
was exactly 41,392 bytes.  The benchmark result is
`results/core_completion_catalog_k2_compact_benchmark_v1/result.json`.

## Production attempt

The hash-pinned run launched only after its fresh preflight passed.  After
450.566053 seconds, the live watchdog observed free space below the
2 GiB reserve and terminated all four workers.  The atomic stop record is
`results/core_completion_catalog_k2_full_screen_v1/STOP_1784862461491121000.json`
(SHA-256
`0f62f4f4ee3e6ed6b688634b11f35cf309e95aa47841b5998f588ae20ed79ad2`).
The stop reason is `FREE_DISK_RESERVE_BREACHED`; there was no SAT,
per-instance limit, or solver error before the stop.

No all-or-nothing production shard was promoted.  Therefore final
production coverage remains **0 of 4 promoted shards** and there is no
complete 282,408-core result.

The four interrupted files were retained rather than deleted.  The
independent prefix audit
`results/core_completion_catalog_k2_full_screen_v1/partial_prefix_audit.json`
(SHA-256
`1bc1d57c81aa36537c14dab252f96e36d1ad8d7142d6498d9b8a7b14878ca4f7`)
validated 20,485 physically complete fixed-width records before the
interrupted trailing bytes:

- 20,485 `OBSERVED_UNSAT_UNCHECKED`;
- 0 `LIMIT_NO_CONCLUSION`;
- 0 negative certificates;
- no proof generation or replay.

These prefix records are diagnostics only.  They do not satisfy the frozen
full-coverage condition and are not used to make an aggregate negative
claim.

Free space later recovered above the unchanged resume threshold.  The
runner validated the same plan and binary hashes, preserved all four first
attempt partials under `diagnostics/`, and restarted the four missing
shards.  After 220.970668 seconds, a second abrupt free-space loss again
triggered `FREE_DISK_RESERVE_BREACHED`.  The second atomic stop record is
`results/core_completion_catalog_k2_full_screen_v1/STOP_1784863072906019000.json`
(SHA-256
`403ca50f53542427895882dcdc8769912006714414c379aca6b2aa9ab592fb09`).
There was again no SAT, per-instance limit, or solver error.

The independent second-prefix audit
`results/core_completion_catalog_k2_full_screen_v1/partial_prefix_audit_attempt2.json`
(SHA-256
`4e7ad801781e8a973a5ff74b7cb5e928edc0c4918f81e78fa345cccb5365e4b9`)
validated 8,764 complete fixed-width records, all
`OBSERVED_UNSAT_UNCHECKED`, with zero limits and zero negative
certificates.  These overlap work from the first interrupted attempt and
must not be added to the first prefix count as distinct coverage.

The consolidated diagnostic
`results/core_completion_catalog_k2_full_screen_v1/cumulative_resource_stop_diagnostics.json`
(SHA-256
`204a0fb646e3114cfa22a75cb40262ac892f7dd5c949d9f5c76b4048db8963a9`)
hash-checks both stop records, both prefix audits, and every retained
partial.  Across the two attempts there were 29,249 validated record
executions.  The second attempt recomputed 8,764 exact pair-order prefixes
contained in the first attempt, leaving 20,485 distinct diagnostic pair
observations rather than 29,249 distinct pairs.

## Resume state

The run identity and immutable plan remain valid.  On a later invocation
of the same frozen command, the runner will preserve the four old partials
under `diagnostics/`, validate and reuse any future atomically promoted
complete shard, and run every missing shard.  Immediately before the
consolidated diagnostic was written, the output directory contained
1,414,852 bytes, so the unchanged resume preflight required at least
2,196,068,796 free bytes.  Observed free space was 2,128,330,752 bytes,
67,738,044 bytes short and below the 2 GiB reserve itself; another
immediate resumption was therefore not authorized.

The final exact-coverage checker remains
`verify/core_completion_k2_full_screen_coverage.py`.  It must accept all
four complete shard files and all 282,408 ordered records before any full
screen summary can be reported.
