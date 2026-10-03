# Polar-zonoid intersection bodies

**Partial research checkpoint. The full AIM/Schneider Baire-category conjecture remains unresolved here.**

Original record: [20001306](https://www.unsolvedmath.com/problems/20001306), AIM-CONVEX_GEOMETRY-0038, [AIM Problem 10](https://aimath.org/WWN/fourierconvex/fourierconvex.pdf).

The original problem asks for generic non-polar-zonoidality of the actual intersection body IK of an origin-symmetric convex body K in every fixed dimension n >= 3. The record's existing title describes an older partial result.

This package establishes and distinguishes:

- A finite rational refinement of the standard signed-measure certificate, with exact polyhedral validation and a quantitative perturbation margin.
- An explicit certificate for the three-dimensional cube, with exact finite checks through dimension 64 and an exact zero at dimension four for that particular witness. These implement a published Schneider obstruction.
- The exact harmonic first variation and the unresolved convexity/nonlinear control required for a universal perturbation proof.
- An open dense non-polar-zonoid class within the separately defined space of four-dimensional bodies of revolution about a fixed axis. This follows by cap truncation from Alfonseca's published flat-top theorem; a normalized inverse-transform calculation verifies the strict negative density.
- An exact six-dimensional cylinder calculation explaining why the same sufficient cap test does not extend automatically.

The restricted genericity theorem is not substituted for the full question. It is a simple corollary of prior work, not presented as a first discovery. No complete resolution or absolute novelty is claimed.

Files:

- `PROOF.md`: precise statements, full derivations, and remaining gaps
- `SOURCE_GATE.md`: source recovery, literature, duplication checks, and scope
- `RESEARCH_LOG.md`: five bounded substantive approaches
- `check_exact.py` / `exact_results.json`: standard-library exact rational checks

Run `python3 check_exact.py`. Computations are finite checks; the universal statements rely on the written arguments. A fresh independent audit is required before publication. No external researcher was contacted.
