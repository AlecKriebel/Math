# Reproduce round 2

The check scripts are confined to this review directory and write reports here and scratch under its `tmp/`. They perform no live publication/tracker/PR writes. Toy Git object tests operate only in disposable local repositories.

Use Python 3.12.14 with SymPy 1.14.0; for the optional numerical run also use NumPy 2.2.6 and SciPy 1.15.3. Preserve the environment's executable symlink. Set TMPDIR to this review's `tmp/` and run from this directory:

```text
python -I -B independent_checks.py --numerical
python -I -B -O independent_checks.py
python -I -B operational_checks.py
python -I -B -O operational_checks.py
python -I -B replay_frozen_operations.py
```

The first two commands give 180 checks each, including actual immutable Git reads, deterministic release rebuilds in copies, and exact replays; the first also runs optional uncertified numerical controls. The next two give 76 fresh independent operational controls each. The last checks the exact operational author freeze, copies its sources into this review's scratch, runs its 147 controls in both modes, then runs the real proposed-layout verifier. It does not overwrite author reports.

These scripts expect the repository audit layout, immutable Git objects, and frozen sources beside this review, unlike the published standalone verifier which works from the extracted release. Full third-party originals are not required by the replay scripts; their independent visual inspection and hashes are recorded in SOURCE_CHECKS.json. Exact identities and successful replay supplement the written proof; they are not a formal proof certificate. Numerical replay provides no interval enclosure or extremality certificate.
