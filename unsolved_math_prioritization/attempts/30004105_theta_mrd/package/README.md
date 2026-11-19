# Theta invariants: one scoped audit

Problem 30004105 / OWR-16775-009, queue row 1912. This is one audit, not five independent attempts. The original research direction remains unresolved and underspecified. A prospective queue disposition is unsolved, 1/5; this package does not edit the queue or publish anything.

Read AUDIT.md and INDEPENDENT_REVIEW.md for the complete authored mathematics and source attribution. Both explicit q=3, n=m=7, k=3 codes have 4,785,157 projective representatives, minimum rank five, and the recorded exact histograms. They collide for a fixed generator but theta squared separates them. No obstruction for all-generator profiles, universal characterization, novelty claim, or present-day openness certificate follows. The equivalence conventions and cautiously limited Giuzzi–Zullo printed-statement issues are retained in full.

## Offline reproducibility

Use Python 3.8+ and a C++17 compiler invoked as g++. No third-party Python modules, data downloads, credentials, network, or sockets are required. Run with PYTHONDONTWRITEBYTECODE=1 to keep the frozen inventory unchanged:

    PYTHONDONTWRITEBYTECODE=1 python3 validate.py
    PYTHONDONTWRITEBYTECODE=1 python3 replay.py
    PYTHONDONTWRITEBYTECODE=1 python3 -O replay.py
    PYTHONDONTWRITEBYTECODE=1 python3 mutation_tests.py
    PYTHONDONTWRITEBYTECODE=1 python3 -O mutation_tests.py

replay.py performs full enumeration twice, with and without -DNDEBUG, then runs each Python checker normally and under -O. Exact flags are -std=c++17 -O2 -Wall -Wextra -pedantic, optionally -DNDEBUG. Compilation and transient outputs stay outside the frozen tree in temporary directories. REPLAY.json records the exact compiler version, Python version, flags, full outputs and byte comparisons. The recorded machine used g++ (Debian 14.2.0-19) 14.2.0 and Python 3.12.14. Programs use runtime checks, not Python/C++ assertions that disappear with optimization.

The validator inventories every entry with lstat, including MANIFEST.json, before reading any manifest or payload content. It rejects nonregular entries, directories, symlinks and hardlinks, then enforces exact inventory, strict integer types, safe names, sizes and SHA-256 hashes. Mutation tests use only writable disposable copies; malformed-inventory tests prove zero content reads, with no actual sockets created. The hashes provide integrity, not independent mathematical proof or authenticity without a trusted external receipt.

The original independent checker is deliberately narrow. exact_checks.py adds strict finite/profile schemas, exact expected histograms and profiles, and an independently implemented rank/nullity/orthogonality oracle on 1,000 deterministic matrices. These checks supplement, not replace, the complete enumeration and authored reasoning.

rank_checks.py also compiles the verbatim production C++ helper prefix with a new independent Gaussian-elimination oracle. It checks 20,000 deterministic matrices and all 128 coordinate-subspace bases, both with and without -DNDEBUG. RANK_CHECKS.json retains full successful outputs. replay.py reruns this harness in both Python modes.
