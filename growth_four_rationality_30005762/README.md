# Rationality below growth four: audited partial results

Problem ID 30005762, row 1854. Status: UNSOLVED after five approaches. Target: finitely based hereditary classical permutation classes with strict upper growth less than four. No general solution or research novelty is claimed. The PP2025 sub-Phi result is an announcement with complete proof uninspected.

Read RESEARCH_REPORT.md for proofs and limitations, INDEPENDENT_AUDIT.md for mathematical acceptance, and SOURCE_GATE.md for literature scope. Exact finite computations are regression checks, not proofs of the infinite claims.

Requires Python 3 and SymPy. Run:

    python verify_package.py
    python -O verify_package.py

The verifier rejects extra or missing files recursively, including nested MANIFEST.json files, symlinks, unexpected directories, and unsafe manifest paths. Only the root MANIFEST.json is exempt from self-hashing. It replays both accepted suites under normal and optimized Python and compares complete output and result JSON. The manifest is an integrity inventory, not a digital signature: authenticate its hash separately when distributing the package.
