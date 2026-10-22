# A sufficient incidence count certificate for unexpected curves

Problem 30004608. This packet accepts a corrected, credited sufficient criterion for a reduced arrangement of distinct complex projective lines that is independently known to be plus-one generated. It does not resolve a full combinatorial classification or claim novelty.

For d lines, let t_k count their k-fold intersections, m be the maximum multiplicity, and tau=sum (k-1)^2 t_k. Define Delta(r)=(d-1)^2-r(d-r-1)-tau and S={r in Z: 2<=r<=floor(d/2), 1<=Delta(r)<=r-1}. If S is nonempty and every r in S satisfies m<=r+1<d/2, the dual point set admits unexpected curves. The actual minimal syzygy degree belongs to S by published exponent and Tjurina results, so Dimca’s criterion applies.

The optional lower bound Delta(r)>=2 requires an independently known non-nearly-free arrangement (d3>d2). “Strictly plus-one generated” is insufficient under Abe’s definition. The known 18-line example has S={7} and unexpected degrees 8 and 9; its arithmetic and mdr=7 were checked exactly. Malara–Pokora–Tutaj-Gasinska Example 5.12 at n=7 demonstrates that the test is not necessary.

## Contents

- [Corrected proof](CORRECTED_PROOF.md): complete accepted mathematical argument, hypotheses, degree ranges, and limitations
- [Mathematical audit](AUDIT.md): theorem and grading checks, known-example attribution, exact arithmetic, and nonnecessity
- [Correction note](CORRECTION_NOTE.md): exact terminology defect and the valid extra hypothesis
- [Primary source pins](PUBLIC_SOURCE_PINS.json): eight public source records, hashes, byte counts, version information, inspection history, and theorem/page locators
- [Arithmetic verification](ARITHMETIC_VERIFICATION.json) and [aggregate check summary](CHECK_SUMMARY.json): results without raw coefficients, matrices, or syzygy witnesses
- [Acceptance binding](ACCEPTANCE_BINDING.json) and [publication manifest](PUBLICATION_MANIFEST.json): exact artifact hashes, scope, and review disclosures

## Review status

The proof, audit, correction, and packaging are AI-assisted. No external human mathematical review, referee certification, or formal proof-assistant verification has been obtained. “Accepted” denotes the limited mathematical assessment in the audit, not journal acceptance. Source inspection is selective; the imported published theorems have not all been independently reproved. Exact computation and byte-level verification support the stated checks but do not certify every mathematical claim.

The corrected proof, source metadata, and arithmetic report preserve their accepted input bytes. The public audit includes six recorded wording changes, one of which clarifies that r=d1, rather than every generator degree, enters S; the argument is unchanged. The audit is not byte-identical to its input. Review-status disclosure is appended. This directory contains authored mathematical work and public verification metadata; it includes no copied source bodies, datasets, raw coordinates, or verification scripts.
