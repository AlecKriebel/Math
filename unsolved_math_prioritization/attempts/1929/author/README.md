# Erdős Problem 100 (UnsolvedMath ID 1929)

**Outcome: unresolved; five approach families exhausted. No full solution, counterexample family, novelty, or priority claim.**

The exact target is a linear lower bound on the diameter of planar point sets whose minimum distance and gaps between unequal positive distance values are all at least one. Equal distances may repeat, and values need not be integral.

## Retained results

- Complete elementary closest-pair/circle counting and packing proof of an explicit lower bound of order n^(3/4), reconstructing an already known exponent
- Linear estimates under an extra bounded-minimum-distance or bounded-strip-width assumption
- A two-perpendicular-lines structure when minimum distance is exactly one, plus a counterexample to rescaling general instances into that special case
- Exact proof that square grids require linear-size diameter after valid gap normalization
- Complete exact reconstruction of Piepmeyer's credited nine-point example, with four distance values and diameter in (4.663,4.664)
- Source-grounded explanation that Guth-Katz yields n/log n, still short of the full target

The current indexed problem tracker marks the general question open. Direct live tracker access failed, so this packet does not certify the tracker state or comment count at the exact inspection time. A bounded current literature search found no verified full resolution. The current accessible formal-conjecture declaration also marks the general question open; a statement containing `sorry` is not a formal proof.

## Reproduction

Run with Python 3.10 or later, standard library only:

    python verify_math.py
    python verify_manifest.py

Compare the first output with CONTROL_RESULTS.json. All decisive computations use integers, rational arithmetic, exact biquadratic-field arithmetic, and certified rational intervals. Numerical bounds printed as decimal-style rational endpoints are not floating-point tests. Read PROOFS.md for universal statements and exact hypotheses.

## Files

- PROOFS.md: nine proved reductions/restricted results/construction statements, imported theorem boundary, and remaining gap
- RESEARCH_LOG.md: five counted approaches, mechanisms, outcomes, limitations
- SOURCE_VERIFICATION.json: provenance hashes, retrieval/inspection metadata, bounded prior-attempt and literature checks
- CONTROL_RESULTS.json and verify_math.py: reproducible exact controls
- MANIFEST.json and verify_manifest.py: exact file allowlist, sizes and hashes, with tamper controls

Only authored analysis, code, exact check results, and public bibliographic/verification metadata are included. Source PDFs, extracted source text, the raw dataset, and coordination material are excluded. The packet is an unrefereed AI-assisted research audit; independent mathematical audit is still required before publication.
