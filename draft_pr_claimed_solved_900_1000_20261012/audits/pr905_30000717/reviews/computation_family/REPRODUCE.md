# Reproduce this computational audit

`checks/exact_controls.py` has no third-party dependencies. Run it normally and under optimization; both outputs must match the saved exact-controls JSON files. It uses explicit RuntimeError guards that remain active under optimization.

    python3 checks/exact_controls.py > exact.rerun.json
    python3 -O checks/exact_controls.py > exact.optimized.rerun.json

`checks/replay_and_attack.py` itself uses Python's standard library; its replay children require SymPy1.14.0. Install that pinned requirement in a disposable environment. The packet path is resolved relative to this family folder: it prefers archive-root `original_packet/` next to `reviews/`, and otherwise falls back to the historical workspace `original/unsolved_math_prioritization/attempts/30000717`. Both the public manifest and proof have fixed hashes enforced before replay. Run this supplemental diagnostic in a disposable archive copy:

    python checks/replay_and_attack.py --result-name replay_new.json

Alternatively, invoke from any Python3 while choosing the pinned child interpreter explicitly:

    python3 checks/replay_and_attack.py --python /path/to/pinned-venv/bin/python --result-name replay_new.json

This script creates and deletes disposable packet copies beneath the family folder, executes only copied packet scripts, records before/after original inventory, and writes `results/NAME.json`. It reproduces the author/historical outputs, publication/mutation guards under normal and optimized execution, optimization false-positive fixtures, and independent trust/integrity attacks. Its timestamps, interpreter version and transient paths change on rerun; compare verdicts and individual evidence rather than the complete replay JSON bytes. Results are written to the diagnostic copy, so keep the accepted extraction available for hash verification.

The public-manifest pin was taken from the parent's frozen ORIGINAL_SNAPSHOT.json and independently confirmed from the live PR description by the parent audit; see `PR_DESCRIPTION_ANCHOR.json`. Deriving an expected hash from an untrusted downloaded packet does not authenticate that packet.

The full thirty-file source-free packet is not duplicated in these intentional review artifacts. No Git operation, external message, network operation or source retrieval is used by either check program.

For ordinary release reproduction use archive-root `verify_package.py`, which validates the new package and runs supported exact controls in disposable copies without changing release files. Raw historical assertion-based scripts under optimization remain unsupported. The original packet and initial completed review seal are preserved; the portable runner's full archive-layout test is separately recorded in `results/PORTABILITY_CHECK.json`.
