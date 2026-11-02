# Divisible-difference sets: restricted results and bounded checks

Erdős 635 / ID 2225 / row 1867. Disposition: UNSOLVED, five approaches, for the sharper unrestricted excess. The fixed-t half-density result is already recorded as solved, not a new claim here.

Read RESEARCH_REPORT.md, RESTRICTED_TRANSFER_STRUCTURE.md, INDEPENDENT_AUDIT.md, and SOURCE_STATUS.md for the mathematical arguments and their limits. Accepted results include exact all-odds compatibility, the restricted powers optimum, the spaced-valuation lower bound, a rational finite-state restricted asymptotic, a weak doubling-forest upper bound, and the matching obstruction. None is an unrestricted sharp upper bound or a novelty certificate.

The original author computed 300 finite optima and five additional sampled cases. The separate audit verified 305 witnesses, independently exhausted 108 cases with N<=18, and reconstructed 232 spaced-valuation constructions. These counts are different tasks, not interchangeable. Finite testing does not establish a general theorem.

Reproduce the checks with Python 3, standard library only:

    python -B exact_check.py
    python -B independent_audit.py
    python -B structure_checks.py
    python -B verify_inventory.py

Run python -B run_controls.py on a working copy to reproduce all normal/optimized and negative controls and regenerate the manifest/log. It prints a fresh receipt; compare the frozen receipt separately. Repeat individual checks with -O after -B. The first two commands regenerate their JSON outputs; they should be byte-identical. CHECKER_PROVENANCE.json records full AST equality for replacement of original asserts by explicit guards, so optimization does not disable validation. COMMAND_OUTPUTS.json consolidates the full normal/optimized command outputs and negative controls. Mutation tests are bounded detection demonstrations, not proof completeness. Only the t=2 cycle mean is numerically checked.

INVENTORY.json covers every recursive package file except itself. Its digest is anchored by the separate local freeze receipt. The inventory checker rejects extra/missing files, symlinks, byte-count or digest changes. No copied papers, dataset records, private paths, or private coordination artifacts are included. Publication is not part of this local preparation.
