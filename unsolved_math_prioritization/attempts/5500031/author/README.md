# Trapping Light Rays with Segment Mirrors (5500031)

**Disposition: unsolved, 5/5 approaches.** This package contains scoped elementary escape results and a precise obstruction to one proof strategy. It does not solve TOPP Problem 31, establish novelty, or claim human peer review.

Main results:
- Concurrent supporting lines force radial-square growth and escape, without rational-angle assumptions.
- Parallel mirrors leave at most the two normal directions potentially trapped.
- A positive-definite quadratic whose directional derivative never decreases at every two-sided reflection exists only for concurrent supports.
- A four-mirror example blocks every direct ray but admits an explicit open interval of two-reflection escapes.
- Finite-prefix angular shrinking does not control the uncountable set of infinite itineraries.

Known rational-angle escape results and known aperiodic traps are credited in SOURCES.md. Endpoint conventions and all-versus-almost-all quantifiers are explicit in PROOF.md.

Run with Python 3, standard library only:

    python verify.py > replay.json
    cmp replay.json check_results.json

The frozen author check has 20,012 exact assertions. Independent review is pending and must be performed on these frozen bytes before publication. Source PDFs, extracts, rendered images, imported datasets, and private coordination records are excluded from this package.
