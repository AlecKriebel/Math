# Portable verification

Run `python3 -B verify_all.py` in this directory with Python3.9 or later and no third-party packages. It checks the exact declared file inventory, safe paths, absence of symlinks and hashes of all other members; MANIFEST.json excludes its own hash. Authenticity of the manifest needs a trusted external pin, supplied by the PR/package receipt. Integrity is distinct from mathematics.

It executes verify_symbols.py and diagnose_norm.py in ordinary and optimized modes. Their complete positive outputs must match the frozen expected JSON bytes. It runs all nine wrong-result modes twice and requires the actual computed ValueError check diagnostic, rejecting the script's unexpected-success fallback. The18 process failures concern algebra/differential representatives, not arbitrary algorithm-mutation coverage or a decision of class inequality.

The universal proof is the field, cohomology and norm/residue argument in COUNTEREXAMPLE.md. Finite algebra controls supplement that proof. Old13/25 diagnostic programs were not distributed with the original inputs and were not rerun.
