# Elementary closed-walk stackings: claimed_solved5

Dataset identity: 30005111 / OWR-10252930-021. Ordered queue row: 1840. Publication classification: claimed_solved5, with the following explicit two-part interpretation. No novelty or literature-priority claim is made.

1. For nonempty primitive combinatorial immersions, immersed_elementary_proof.md proves stacking existence by finite integer-cochain vertex splitting and height descent. It does not invoke Howie's maximal cyclic tower theorem.
2. For arbitrary closed edge walks, the nonrepetition criterion alone is false: ababa excursions on a three-vertex path give a ten-edge obstruction for arbitrary continuous heights. This walk is a cyclic-word nonpower but represents the identity in the fundamental group of the tree. It is not a nonpower group-element counterexample and does not disprove Louder–Wilton.

If the source's intended closed-walk convention includes cyclic reduction, use the immersed proof, not the counterexample. Finite tests corroborate the mathematical arguments rather than replace them. SOURCE_GATE.md is the historical pre-solution source audit; REPORT.md and ACCEPTANCE.md record the subsequent outcomes.

## Exact replay

From this directory, with Python 3 and its standard library:

    PYTHONDONTWRITEBYTECODE=1 python check_cochain.py
    PYTHONDONTWRITEBYTECODE=1 python check_cochain_independent.py
    PYTHONDONTWRITEBYTECODE=1 python audit/check_ababa.py
    PYTHONDONTWRITEBYTECODE=1 python audit/check_star.py
    PYTHONDONTWRITEBYTECODE=1 python audit/independent_backtracking/verify_ababa.py
    PYTHONDONTWRITEBYTECODE=1 python verify_certificates.py
    PYTHONDONTWRITEBYTECODE=1 python verify_manifest.py

Repeat each command using python -O. Explicit guards remain active under optimization. The generators rewrite their deterministic certificates with identical bytes, so manifest verification remains valid. The manifest excludes only itself and Python bytecode caches; do not write additional replay output files inside the package after freezing it.

## Results and audit map

- check_cochain.py: 3,228 primitive rose cases, 64 proper-power negatives, and 372 subdivided cases.
- check_cochain_independent.py: independent validation of 3,292 rose outcomes, 372 subdivisions, six bridge/barbell/theta cases, certificate corruption and invalid-input controls.
- audit/independent_backtracking/verify_ababa.py: 120 central orders and 1,440 full fiber orders, all rejected; 20 rotation/inverse nonpower checks.
- verify_certificates.py: validates all 120 serialized overlap witnesses and 20 periodicity entries; rejects five real mutations, including invalid heights, reversed edge orientation, false periodicity, and malformed witnesses/orders.
- verify_manifest.py: exact complete file inventory, SHA-256 and byte counts; rejects modified, missing, and extra file controls.
- independent_elementary_audit.md and audit/independent_backtracking/AUDIT.md: independent analytic audits.
- independent_package_audit.md: independent review of publication implementation.
- provenance/: exact guard-change records, patches, and path-edit provenance.
- replay/: executed normal and optimized outputs.
