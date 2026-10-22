# Corrected release: tree modules, problem 30001721

Mathematical status: **unsolved**, five substantive approaches. This is correction C1 only; no mathematical claim, support total, endomorphism histogram, or indecomposable count has changed.

- `author/` is the corrected research packet.
- `original-author/` preserves the entire first frozen author packet, byte for byte.
- `original-audit/` preserves the full independent audit, byte for byte, including its C1 correction request and its binding to the original hashes. References inside this historical audit retain their original context; its original-author reproduction commands should be run against `original-author/` when replaying the historical snapshot.
- `validation/` contains fresh corrected-author and full independent replay outputs.
- `changes/` contains the exact patch and the correction/replay ledger.
- `SHA256SUMS` binds every file in this release other than itself.

C1 changes the enumeration key `tested_basis_permutation_orbits` to `algebra_cases_evaluated` and adds `basis_permutation_quotient_used`. The case counts remain 32, 12, 1, and 485. The quotient flags are false, false, false, and true. The first three computations evaluate all labelled supports directly; only the fourth uses basis-permutation representatives. No orbit count is substituted for a case count. None of these counts is an isomorphism-class count.

Fresh author replay:

    python author/verify_tree_controls.py --extended-control --output validation/author_replay.json
    cmp author/control_results.json validation/author_replay.json

Fresh independent replay (every labelled support, no orbit cache):

    python original-audit/independent_controls.py --output validation/independent_results.json
    cmp original-audit/independent_results.json validation/independent_results.json

The preserved audit already contains separate independently derived Burnside orbit counts and explains their group action. They are not relabeled as cases evaluated in the corrected author result.

This corrected freeze is awaiting the original reviewer's hash-binding check. No remote publication has been performed for this corrected release.
