# Replay instructions

Use Python 3.12 or compatible. This audit used the bundled executable
`/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
All commands run from this family folder with -E -B -P; the code explicitly
adds only its own local dependency directory. No PYTHONPATH or repository
imports are used. Do not use -S for the dependent scripts; use it only for
stdlib-only manifest scripts if desired.

Install missing dependencies locally (not a publication artifact):

    python3 -E -B -P -m pip install --no-compile --target runtime_packages sympy==1.14.0 mpmath==1.3.0

Then run:

    python3 -E -B -P reproduce_submission.py
    python3 -E -B -P optimization_negative_control.py
    python3 -E -B -P exact_certificates.py
    python3 -E -B -P -O exact_certificates.py
    python3 -E -B -P independent_geometry.py --resume
    python3 -E -B -P independent_guard_replay.py
    python3 -E -B -P nonconfocal_negative_control.py
    python3 -E -B -P extreme_resonance_record.py
    python3 -E -B -P replay_extreme_record.py

For the broad grid, --resume reads the 43 original independent shooting
records in independent_geometry_attempt1_stdout.txt. It recomputes every
phase, geometric residual and focal product from those λ values, and
freshly shoots the final extreme case. Without --resume, all 44 target
resonances are freshly shot (180-digit arithmetic, 540 bisections each).
Negative-control resonances are always freshly shot.

Do not use the broad results JSON's 125-digit λ for the final extreme as
a replacement for fresh shooting: its gap from b² is only about 1e-80.
The separate extreme_resonance_record.json holds 175 significant digits
for sufficiently accurate direct replay. The number of serialized digits
is not a claim of that many certified digits; this is ordinary high-
precision numerical evidence, not interval arithmetic.

The original submitted verifier writes verification.json next to its own
script. Its copied replay directories are intentional. Never execute that
original in the immutable original_submitted_head directory. Legacy output
counts under -O are unenforced labels and must not be called passed checks.

All independent check functions use explicit exceptions. The guard replay
requires good geometry to succeed and a deliberate False to fail under
both normal and optimized Python. The exact stdout files from both modes
should match byte for byte.

The original archive is needed only for reproduction and the deliberate
legacy mutation control. Other scripts read only this family directory.
Do not publish runtime_packages: it contains third-party installation
files, not authored findings. MANIFEST.json excludes that cache and itself.
