# K2P Level-2 Identifiability Closure

This directory contains the exact four-port K2P relation sweep and its
referee-reproducible verification package for the generic-identifiability and
directed-containment classification of binary strongly tree-child level-2
semi-directed networks.

The program is being continued from the ChatGPT research conversation
`6a83c53c-d49c-83e8-9506-b0da8de1c534`.  The finite four-port
dummy-role/restoration sweep is the remaining load-bearing gate.  All
optimization changes must preserve exact arithmetic, canonical class IDs,
input locks, atomic per-class records, resume semantics, and mutation-test
coverage.

## Layout

- `archives/original/`: every downloaded archive produced by the referenced
  conversation, retained unchanged.
- `package/original/`: extracted checkpoint and four-port files, retained
  unchanged.
- `package/referee/`: optimized, referee-facing sweep and verification code.
- `runs/`: local resumable outputs (ignored by Git except for small final
  manifests selected for publication).
- `benchmarks/`: reproducible profiling and equivalence results.
- `RESEARCH_LOG.md`: chronological decisions, findings, and checkpoints.

The original four-port package is under
`package/original/four_port/k2p_offline_sweep_portable`.  The qualified runner
is under `package/referee/k2p_offline_sweep_portable`.

## Qualified local invocation

The exact matching interpreter currently available on this machine is

```text
/Users/alec/Documents/Math-lalonde20/lalonde20_quantum_coloring/.venv/bin/python
```

From the referee package, qualification is:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  /Users/alec/Documents/Math-lalonde20/lalonde20_quantum_coloring/.venv/bin/python \
  verify_package.py
```

The guarded, resumable production command is:

```bash
/Users/alec/Documents/Math-lalonde20/lalonde20_quantum_coloring/.venv/bin/python \
  guarded_run.py ../../../runs/four_port_full \
  --python /Users/alec/Documents/Math-lalonde20/lalonde20_quantum_coloring/.venv/bin/python \
  --workers 1
```

Qualification passed.  Production preflight currently refuses to launch
because only 2.61 GiB disk is free; 20 GiB is required.  The safety gate is
intentional because another exact research computation is active and the
machine already has substantial compressed memory and swap pressure.
