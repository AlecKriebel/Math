# Author-side verification scope

Expected commands: `python verify.py`, `python -O verify.py`, and
`python test_fail_closed.py`.

The first two recompute 37 exact 3D hulls, seven quotient-lattice cases,
twenty rational coefficient identities, and 4,900 product-parameter cases.
The normal and optimized runs use explicit exceptions, not removable assert
statements.

The fail-closed harness performs 36 checks: a relocated clean run and
seventeen deliberately corrupted runs, each in normal and optimized modes.
Its thirteen semantic corruptions are rehashed into their manifests before
testing, so they cannot be rejected only for stale file hashes. Four other
tests cover an unhashed proof edit, missing manifest entry, unexpected file,
and symlink. The clean relocated runs use an unrelated working directory.

This is author-side QA. It is not independent mathematical review, exhaustive
polytope enumeration, or a machine proof of the general lemmas. The outer
receipt records the actual execution outcomes and frozen hashes.
