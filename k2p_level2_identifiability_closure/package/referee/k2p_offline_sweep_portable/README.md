# Referee-ready resumable K2P four-port sweep

This directory is an optimized, fail-closed derivative of the hash-preserved
portable sweep.  It contains the corrected graph-derived K2P compiler, the
complete four-port descriptor/rank inputs, the exact hand certificate for the
four direct hard relations, and an atomic resumable driver.

The mathematical universe is unchanged.  The optimization keeps one loaded
universe alive for several sources, caches only fixed-source algebra, discards
target-local algebra after each class, prepares the fixed side of exact graph
comparisons once, and checkpoints manifests every 25 records.  The original
download is retained separately by the parent research package.

## Environment and qualification

Use Python 3.11 or newer with the exact versions in `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python verify_package.py
```

The input lock rejects missing or mismatched files and dependency versions.
The verifier checks the six source counts and ranks, binds the four hard cases
to exact finite-atlas classes, exhaustively compares the frozen and prepared
mixed-graph relation routines on every rank-eligible presentation, exercises
atomic resume, and runs adversarial record mutations.

## Resource-safe full sweep

The two pickle files occupy about 110 MB on disk but measured approximately
1.3 GiB resident memory after loading.  Do not equate file size with worker
memory.  The guarded launcher defaults to one low-priority worker, requires 20
GiB free disk at launch, stops below 10 GiB, and terminates safely if aggregate
sweep RSS exceeds 3.5 GiB.  Every completed class remains resumable.

```bash
python guarded_run.py /path/to/k2p_four_port_run \
  --python "$PWD/.venv/bin/python" --workers 1
```

On a machine with demonstrated memory headroom, two long-lived lanes are
available:

```bash
python guarded_run.py /path/to/k2p_four_port_run \
  --python "$PWD/.venv/bin/python" --workers 2
```

The balanced lanes are sources `[1,2]` (1,023 canonical classes) and
`[0,3,4,5]` (908 classes).  Their startup is staggered.  More than two workers
is intentionally unsupported by the packaged runner.

The lower-level, unguarded entry point is:

```bash
PYTHON_BIN="$PWD/.venv/bin/python" K2P_WORKERS=1 \
  bash run_all_sources.sh /path/to/k2p_four_port_run
```

It processes all six sources and writes
`FOUR_PORT_SWEEP_MERGED_STATUS.json`.  Merge qualification reopens every class
record, verifies all hashes and bindings, checks exact ID coverage, and exits
nonzero if a source is incomplete or an unresolved class remains.

## Resume and integrity

Reissue the same command with the same output directory.  Each completed
canonical class is verified and reused.  Records are committed by fsync plus
atomic rename, and one advisory lock protects each source directory.  Logs are
appended rather than truncated.

Each record has two hashes:

- `record_payload_sha256` covers the complete operational record;
- `semantic_record_sha256` excludes only runtime, RSS, platform, and timestamp
  diagnostics, so mathematical output is deterministic across machines and
  worker layouts.

Each source manifest and the final merged result likewise include a semantic
hash/root independent of operational timings and byte-level record hashes.

For an explicit comparison between a frozen baseline sample and an optimized
sample, run:

```bash
python compare_semantic_runs.py /path/to/baseline /path/to/candidate
```

The comparison requires all 1,931 records by default; add `--allow-partial`
only for a declared benchmark sample.

## Output interpretation

Per-class statuses are:

- `separated`: exact quadratic or exact F2/F3/F4 certificate;
- `isomorphic`: exact labelled mixed-graph isomorphism;
- `triangle`: exact ordinary-triangle quotient;
- `restoration_parent`: at least one omitted physical role, with exact direct
  child requests for restoration;
- `unresolved`: a direct no-dummy relation requiring further algebra.

The sweep never infers a larger containment from a smaller marginal.  Every
restoration record retains target dummy attachments and all source
insertion-edge candidates needed to construct direct child marginals.
