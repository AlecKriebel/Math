# Reproduce this computational audit

`checks/exact_controls.py` has no third-party dependencies. Run it normally and under optimization; both outputs must match the saved exact-controls JSON files. It uses explicit RuntimeError guards that remain active under optimization.

    python3 checks/exact_controls.py > exact.rerun.json
    python3 -O checks/exact_controls.py > exact.optimized.rerun.json

`checks/replay_and_attack.py` requires Python3 and SymPy1.14.0. Install that pinned requirement in a disposable environment. Its root is resolved relative to this family folder; the unchanged sibling original snapshot must remain available. Run:

    python checks/replay_and_attack.py

This script creates and deletes disposable packet copies beneath the family folder, executes only copied packet scripts, records before/after original inventory, and writes `results/replay_and_attack.json`. It reproduces the author/historical outputs, publication/mutation guards under normal and optimized execution, optimization false-positive fixtures, and independent trust/integrity attacks. Its timestamps, interpreter version and transient paths change on rerun; compare verdicts and individual evidence rather than the complete replay JSON bytes.

The public-manifest pin is taken from the parent's frozen ORIGINAL_SNAPSHOT.json. Agreeing it with an independently trusted PR-description anchor is part of the parent synthesis. Deriving an expected hash from an untrusted downloaded packet does not authenticate that packet.

The full thirty-file source-free packet is not duplicated in these intentional review artifacts. No Git operation, external message, network operation or source retrieval is used by either check program.
