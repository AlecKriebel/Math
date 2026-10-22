# Problem 30000203: minimal subdegrees of twisted-wreath groups

**Status: unsolved. Five substantive approaches exhausted.** No complete solution, verified prior resolution, or novelty claim is asserted.

The exact question asks whether MinSubDeg(G) < k MinSubDeg(H) for every finite primitive twisted-wreath group with its natural primitive component. The package contains:

- PARTIAL_RESULTS.md: full proofs of the reduction, two sufficient mechanisms, their obstructions, exact minimum 15 in the A5/A6 example, and the A8 class-size correction;
- APPROACH_LOG.md: five distinct approaches, outcomes, completion estimates, and exact remaining gaps;
- SOURCE_STATUS.md and SOURCE_PROVENANCE.json: primary-source locations, bounded literature search, pinned corpus checks, duplicate checks, and version-specific cautions;
- controls.py and CONTROL_RESULTS.json: independent standard-library exact controls;
- RESULT.json and readiness.json: scoped disposition and source-bound readiness;
- REPRODUCIBILITY.md and ENVIRONMENT.json: commands and computational limits;
- SHA256SUMS: frozen public-package hashes.

The strongest finite result is MinSubDeg(A5 twr A6) = 15, proved without the subgroup enumeration and independently verified over all 501 subgroups of A6. A shortest component class alone would only yield 72, so that tempting restriction genuinely misses the minimum. The general strict inequality is still unproved here.

The source PDFs, corpus files, extracted source text, and coordination records are not part of this package. Public citations are provided instead. No external researcher was contacted, and no remote write was made. Publication is contingent on a fresh independent audit and the campaign's publication gate.
