# PR211 physical geometry audit

No physical construction or exact algebra defect was found in the stated odd
least-period domain. This is a bounded independent family audit; Root retains
acceptance of the universal complex proof, complete package, priority and release.

The independently derived tangent solve gives the actual outer vertices and
proves all real intersections transverse, outside E, and away from the original
foci, including reversed outer axes. The actual Euclidean inversion gives the
stated distance factorization and edge kernel with the correct q^4 factor.
Twenty universal exact identities and strict real denominator/positivity
arguments verify the bridge from physical geometry to that kernel. Half-step
indexing, opposite-focus shift, orientation, repetition and spatial scaling
were checked independently.

Exact noncircular triangle constructions at two phases each give products
1/3600 and 81/25600, including the N3 critical triple-angle case. An exact
same-caustic primitive N4 counterexample gives products 1/2 and 9/16.

Fresh caustic-tangent and reflection propagation produced 763 genuine closed
orbits in 109 families, checking 10374 vertices, every coprime star for N3..17
at three moduli, reversed axes, near-circle/near-collapse limits, N31 and N101,
even controls, reversal and threefold repeats. Maximum odd product variation
was 1.56e-79 at 85 digits. Four limiting families were repeated at 130 digits;
all stored 24-digit phase areas/products agree, and the hardest variation drops
to 3.42e-124. These are noninterval numerical diagnostics, not a universal proof.

The exact remaining dependency of this family is the separate complete complex
pole/divisor review for cyclic constancy. No unsupported original-to-outer area
transfer was used. No old review, PASS label, historical checker or related-PR
conclusion was treated as authority. Authenticated original/revised proof
sections2–7 are independently byte-identical. Actual primary pages were
fetched, hashed, rendered and read privately. No external person was contacted;
no Git, provider, ref, PR or publication state changed.

Files:
- DERIVATION.md: complete checkable derivation, primary-source mapping, examples,
  mechanisms, controls and exact scope.
- independent_check.py and precision_probe.py: newly authored computations.
- EXACT_ALGEBRA_RESULTS.json and EXACT_GEOMETRY_RESULTS.json: exact evidence.
- NUMERICAL_GEOMETRY_RESULTS.json and PRECISION_PROBE_RESULTS.json: all cases.
- REPRODUCIBILITY_RESULTS.json: exact semantic replay and precision stability.
- FINDINGS.json, INPUT_PINS.json, PRIMARY_READING_SUMMARY.json, RESEARCH_LOG.md:
  finding ledger, source pins, reading limits and timestamped checkpoints.
- AUTHORED_MANIFEST.json: finite authored selection; EXTERNAL_SEAL.json binds it.

Reproduce with preinstalled Python3.11, Sympy1.14 and mpmath1.3:

    /opt/homebrew/bin/python3.11 independent_check.py exact
    /opt/homebrew/bin/python3.11 independent_check.py numeric
    /opt/homebrew/bin/python3.11 precision_probe.py

These commands write only their adjacent result files. Copy the finite authored
selection to a new isolated folder first to preserve this frozen evidence.
All private primary PDFs, page renders, extracted text, foreign files and
nonselected folders are excluded from AUTHORED_MANIFEST.json.
