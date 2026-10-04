# Reviewed result: ambient invariance fails

**Disposition: claimed_solved, 1/5 substantive author turns. Independent adversarial review: PASS, no blocking mathematical defect.**

The coordinate subalgebras B and C of C({0,1}²), with the fair perfectly correlated state, have no extremal-exchangeable independence witness. After the state-preserving diagonal embedding into M₄, a pure vector-state extension gives a pure, exchangeable witness by folding. The subalgebras are distinct and proper, and their intersection consists precisely of scalars.

The downstairs proof excludes every candidate witness: positivity and a third copy force all generator vectors to coincide, determining the unique state as a nontrivial mixture of two exchangeable characters. The upstairs construction matches the entire B*C joint law and has the prescribed full marginal.

A separate polynomial-to-Laurent-polynomial inclusion answers the original report's literal non-lifting concern in the unrestricted algebraic category. This is not a C*-state-extension counterexample. The packet carefully distinguishes extension of extreme states from restriction losing extremality.

## Required scope

Extremality is among **all exchangeable states**, as in the printed definition. Requiring the correct full marginal while retaining this extremality convention does not eliminate the example. Changing the convex set to a fixed-marginal slice is a different definition and is not covered. No result for faithful-only or tracial-only variants, or a specified normal W*-free-product theory, is claimed.

Pure folding is an established mechanism, credited to Dykema–Köstler–Williams. Neither the author nor the review certifies historical novelty. This is AI-assisted research and independent AI-assisted review, not formal certification or human peer review.

## Read and reproduce

- [Complete proof](public/PROOF.md)
- [Primary-source and prior-attempt gate](public/SOURCE_GATE.md)
- [Substantive attempt record](public/ATTEMPT_LOG.md)
- [Full independent adversarial audit](audit/AUDIT.md)
- [Audit receipt](audit/AUDIT_RECEIPT.json)

Run from this directory:

    python3 verify_package.py

It checks both frozen manifests and replays all 14,944 exact rational auxiliary controls. The universal all-state, all-word proof is in the mathematical note and audit; finite controls do not certify those quantifiers.

All eight author files, including the author manifest, and all four audit files are preserved byte-for-byte. References in the frozen author packet to a pending audit describe the pre-review checkpoint; the audit above supplies the subsequent PASS verdict. Source PDFs, renders, extracted source text, datasets, and private context are not redistributed.

## Queue provenance correction

The frozen SOURCE_GATE.md labels `c87c275c638939b8008fd58db80657491d14971e` as the fetched queue blob. That string appears in the queue's existing embedded header and must not be used as its actual publication-base blob identity. The fresh GitHub connector response at main commit `1135765a7fe02d6c2bbeca7bc1a3a4a5259650a9` reports actual queue blob `59dba610d333684751e889818d21f66aba29cec9`; direct Git blob hashing of the returned bytes verifies that value. The old checkpoint cannot establish the earlier actual blob SHA from its embedded header alone.

This provenance correction does not change the quoted rank-559 row or the mathematics. Publication preserves that pre-existing header and every unrelated queue byte, changing only this problem's Status, Turns, and previously blank Findings cells.
