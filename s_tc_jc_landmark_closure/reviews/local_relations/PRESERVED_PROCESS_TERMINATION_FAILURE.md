# Preserved clean-room process termination

Status: `EXACTLY OBSERVED — ENVIRONMENTAL INTERRUPTION`

On 2026-08-09, the first exact `n=3` strict-sign audit was launched only in
the reviewer's recorded execution session `29052` (OS PID `35646`). It remained
CPU-active and memory-stable, but exited with status `143` after approximately
eight minutes. The reviewer did not send it a signal and did not signal any
other process.

This is not a mathematical failure. It is preserved because a monolithic run
that loses all work on `SIGTERM` is not release-grade. Subsequent versions must
use deterministic, resumable work units and may control only their own recorded
session/PID. Broad `pkill`/`kill` patterns are prohibited.

The earlier system-Python launch also failed before computation because that
runtime did not contain SymPy. Exact sign work therefore uses the existing
`/usr/local/bin/python` runtime (Python 3.9.6, SymPy 1.14.0); no dependency was
installed and no producer implementation was imported.
