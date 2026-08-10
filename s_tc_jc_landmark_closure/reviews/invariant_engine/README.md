# Clean-room JC invariant-engine audit

This directory audits only the exact Fourier/invariant/sign engine used by the
primary bounded atlas.  It does **not** certify that the finite topology atlas
is exhaustive and does **not** certify the global identifiability theorem.

The independent algebra in `cleanroom_engine.py` imports no project Fourier,
graph, invariant, or sign code.  `run_review.py` first derives the expected
objects independently and then imports the current primary modules strictly as
the system under test.  Historical code is never executed; its six coefficient
templates and the seventh JSON table are parsed as inert integer data.

Run from the repository root:

```bash
/opt/homebrew/opt/python@3.11/bin/python3.11 \
  s_tc_jc_landmark_closure/reviews/invariant_engine/run_review.py
```

The run deterministically regenerates `certificate.json`,
`mutation_transcript.json`, `failure_log.json`, and `hashes.json`.

The first attempted replay under the shell's default Homebrew Python 3.14 is
preserved in `failure_log.json`: that interpreter lacks SymPy and stopped
before the sign-certificate gate. The pinned Python 3.11 runtime provides
SymPy 1.14.0.
