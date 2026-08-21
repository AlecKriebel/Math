# K2P Level-2 Identifiability Closure

This directory contains the exact four-port K2P relation sweep, its optimized
referee runner, and the proof-first closure of all 36 direct candidate
relations for binary strongly tree-child level-2 semi-directed networks.

The program continues the ChatGPT research conversation
`6a83c53c-d49c-83e8-9506-b0da8de1c534`. The downloaded checkpoint archives
are preserved unchanged; every later optimization and proof artifact lives in
this dedicated research folder.

## Current exact milestone

The final current-lock sweep processed all 1,931 canonical four-port classes
with zero errors. Its raw status census is:

- 845 separated;
- 20 mixed-graph isomorphic;
- 35 ordinary-triangle-related;
- 997 restoration parents; and
- 34 direct rows unresolved by the runner's quadratic/cubic pass.

An independent exact proof overlay closes those 34 rows and replays the two
cubic rows already found by the runner. The 36 named direct candidates are
therefore all separated: 22 by a transported quintic, 12 by quartics, and 2 by
a cubic. Each proof is a direct graph-switch substitution with a strict
positive-domain K2P witness; it is not an inference from a numerical rank or a
larger atlas search.

This is a complete **direct four-port residual** milestone, not yet the final
global theorem. The remaining theorem gates are listed in [STATUS.md](STATUS.md).

## Layout

- `archives/original/`: every downloaded archive from the referenced
  conversation, retained unchanged.
- `package/original/`: extracted original checkpoints and four-port package,
  retained unchanged.
- `package/referee/k2p_offline_sweep_portable/`: optimized sweep, frozen
  current-lock result subset, exact proof certificates, and release verifier.
- `runs/`: local resumable outputs, ignored by Git except selected release
  inputs copied into the referee package.
- `work/` and `analysis/`: proof discovery, independent replays, and
  adversarial audit artifacts.
- `benchmarks/`: profiling, qualification, and proof replay transcripts.
- `RESEARCH_LOG.md`: chronological decisions and findings.

## Referee qualification

Create the pinned environment described by the package's `requirements.txt`,
then run from the referee package:

```bash
python verify_direct_closure_release.py
```

This qualifies the immutable sweep engine, checks both release locks,
recomputes the six complete manifest roots, replays all 36 exact obstructions,
and requires byte identity with the committed certificates. Detailed
regeneration commands and scope boundaries are in
`package/referee/k2p_offline_sweep_portable/README_DIRECT_CLOSURE.md`.

On the local M1 Pro, the fully current cubic-aware sweep took about six minutes
with one low-priority process and peaked near 1.5 GB RSS. The earlier
94-second run was legitimate but narrower: it classified a precompiled finite
universe only through its then-enabled quadratic/direct-hard/graph stages.
