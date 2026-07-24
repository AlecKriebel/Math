# Catalog k=2 delete-two/add-three constructive pilot

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

**REPRODUCIBLE COMPUTATIONAL OBSERVATION, not a certified negative.**
The preregistered persistent-worker pilot executed all 32 selected
`(catalog line, deleted-left, deleted-right)` cores. The solver reported
UNSAT for all 32, with no SAT model, limit, error, or coverage failure.

| status | count |
|---|---:|
| `OBSERVED_UNSAT_UNCHECKED` | 32 |
| `DUAL_VERIFIED_SAT_CONSTRUCTION` | 0 |
| `LIMIT_NO_CONCLUSION` | 0 |
| `SAT_MODEL_VERIFICATION_FAILED` | 0 |
| `PILOT_ERROR` | 0 |

No negative proof was generated or replayed, and
`negative_certified_count=0`. These statuses concern only the 32 selected
fixed induced 40-vertex cores. They do not certify nonextendibility, do not
classify the other 282,376 catalog/deletion pairs, and do not imply global
`(5,5;43)` nonexistence or change any Ramsey bound.

## Encoding and sample

Deleting two vertices from one pinned, dual-verified 42-vertex catalog graph
leaves a fixed 40-vertex core. Three new vertices A, B, C use 123 variables:

```text
0..39    A--core
40..79   B--core
80..119  C--core
120      A--B
121      A--C
122      B--C
```

Clauses forbid homogeneous 5-sets formed by:

- one new vertex and a homogeneous core 4-set;
- two new vertices and a homogeneous core triple; or
- all three new vertices and one core pair.

Independent Python reconstruction matched the C++ variable, clause, and
sign counts. Three semantic/producer tests pass, including completed-graph
equivalence on deterministic assignments.

The sample uses 16 evenly spaced catalog lines. Each contributes one
long-span deletion pair and one adjacent pair. The immutable plan is:

```text
results/benchmark_plans/core_completion_catalog_k2_pilot_v1.json
SHA-256 65f65254a4f8ca482c4f48ef0af2b3a9c4920695702dd34a4cb6b61c24c70b39
```

Limits were four persistent workers, 0.5 seconds and 100,000 nodes per core,
300 seconds total wall time, an 8 MiB output cap, and a 2 GiB free-space
reserve.

The first launch attempt failed closed before creating an output directory
because the disk preflight did not pass. After free space rose, the exact
same frozen command passed with 2,307,055,616 bytes available, exceeding the
required 2,155,872,256 bytes.

## Measurements

| measure | minimum | median | maximum | total |
|---|---:|---:|---:|---:|
| solver internal seconds | 0.049034 | 0.081378 | 0.132965 | 2.778875 |
| search nodes | 691 | 1,290 | 1,869 | 41,718 |
| clauses | 13,275 | 13,345.5 | 13,461 | — |

Pilot wall time was 0.740735 seconds. Every worker produced exactly eight
records, returned zero, and had empty stderr.

The compact summary used 42,021 bytes before the audit; the final directory
occupies 48 KiB, far below both the 8 MiB cap and 50 MB ceiling. Free disk
after the run remained 2,306,867,200 bytes.

The SAT path was armed to stop a worker immediately, atomically preserve its
raw model, reconstruct graph6 and canonical artifacts, and require both the
exhaustive Python and independent C++ bitset verifiers. No SAT status
occurred, so no candidate artifact was created.

## Exact audit

The independent coverage/status audit passed:

```text
expected pairs       32
actual pairs         32
duplicates            0
exact coverage     true
records valid      true
resource checks    true
negative certified    0
```

Persistent artifacts:

| artifact | SHA-256 |
|---|---|
| `results/core_completion_catalog_k2_pilot_v1/summary.json` | `635eb6812440986ab9368099635f3b9ad1d8f661c170d66121ea020480bbdf77` |
| `results/core_completion_catalog_k2_pilot_v1/coverage.json` | `6d44097fedd40c0d72cbb5432ecc7a535941bb10508f3a59f6848a2ea3b65f39` |
| `src/core_completion_k2_persistent_solver.cpp` | `216ab01bb398975873668757bdc7dad900a65e8f59ccce879b03cf4c7712952f` |
| solver binary | `52cf1dbbb5875013aa49a7237474dd7eb4d98e0b44a23879047b3941f9bb6811` |
| `src/core_completion_k2.py` | `dfbb16bd1d5dec18aa2fa3b4b90c579b1ba64d50d37bd7fe6d46606c6bb4a1fd` |
| `src/core_completion_k2_pilot.py` | `794a00f83f46b3af8cc2be081edaef313b19f8686ab5b6631bf6f0a0df9934ec` |
| `verify/core_completion_k2_pilot_coverage.py` | `1181b459a15ee5e3c87901a5a8fff976fbc33de8e94e53693bb2f02f5f5d3131` |
