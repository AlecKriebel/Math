# Golden-radical unit research packet

Queue 1865 / ID 20001341, checked 2026-10-21.

- `RESEARCH.md`: five substantive approaches, scoped proofs, priority/status audit, failed-route ledger, and remaining completion gates.
- `verify_exact.py`: reproducible exact polynomial identities, small-degree minimal-polynomial checks, and high-precision numeric evaluation.
- `exact_checks.json`: successful output of that script. Decimal approximations are not interval certificates; the mathematical bounds are supplied symbolically in the proof.

At n=156, alpha has canonical Minkowski length approximately 17.6636898064 and a ratio to the universal torsion baseline of approximately 1.0000095153046. Its sqrt(2)-weighted logarithmic length is approximately 0.0544865098074. Those are different metrics.

The strongest scoped result is exact optimality outside the relative-norm ±1 kernel for canonical Minkowski length, sqrt(2)-weighted log length, house, height, and (with the degree argument) intrinsic Mahler measure. The rank-155 kernel remains uncertified, and no full unit basis or regulator is computed. The source's undefined notion of “short” remains unresolved. No novelty claim is made.

Independent mathematical review passed the scoped proofs and an independent rerun of the exact checks; see `INDEPENDENT_METRIC_AUDIT.md`. This packet makes no publication changes and does not certify a global shortest unit.

## Reproduction and status

Disposition: UNSOLVED after five approaches. The unspecified objective and the rank-155 norm-exponent kernel remain unresolved. No full basis, regulator, or novelty claim is made.

Run from this directory with Python 3, SymPy and mpmath:

    python3 verify_conversion.py
    python3 -O verify_conversion.py
    python3 verify_exact.py
    python3 -O verify_exact.py
    python3 verify_regressions.py
    python3 -O verify_regressions.py
    python3 verify_replay.py
    python3 -O verify_replay.py
    python3 verify_inventory.py
    python3 -O verify_inventory.py

The exact verifier regenerates exact_checks.json deterministically. Full captured stdout, stderr, commands, dependency versions and deliberate mutation outcomes are consolidated in REPLAY_RESULTS.json. verify_replay.py reruns every recorded command and compares complete stdout, normalized stderr, and exit code. Each listed --mutation case must fail with a mathematical regression diagnostic, under both ordinary and optimized execution. Finite exact checks and high-precision decimals do not replace the symbolic proofs or certify the remaining kernel optimum.

INVENTORY.json lists every regular file recursively except itself. Nested files with that same basename are included; symlinks and unsafe paths are rejected. Run Python with PYTHONDONTWRITEBYTECODE=1 if importing package modules, to avoid adding unlisted cache files.
