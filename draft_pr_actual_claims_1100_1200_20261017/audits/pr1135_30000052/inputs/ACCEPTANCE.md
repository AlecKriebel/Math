# Acceptance: random generalized-lattice discrepancy comparison

**Decision: ACCEPT_FULL_NEGATIVE.** Problem 30000052 / OWR-723-005 is answered negatively by the frozen three-point counterexample.

- Parameters: n = 3, d = 1, p = 4, with independent continuous uniform generator and shift.
- Expected normalized anchored lattice fourth moment: 19/1620.
- Corresponding iid fourth moment: 4/405 = 16/1620.
- Strict excess: 1/540; ratio: 19/16.
- Independent analytic counterexample: at n = 4, the lattice moment is at least 2/315, exceeding iid 11/1920 by at least 5/8064.
- All n,d second-moment equality and all-dimension n <= 2 law equality are correct.

The original source definition, quantifiers, normalization, and parameter measure were checked directly against the rendered original report. Every step of the elementary proof was independently reconstructed. A separate exact shift-first calculation confirms the values without using the author's code. No mathematical correction is needed.

The frozen original proof has minor inline TeX delimiter defects. This separately identified edition repairs those delimiters only; the audited original remains unchanged. No mathematical correction is made. ACCEPTANCE.json records separate original and distributed document identities.

Primary source: Erich Novak, joint work with Aicke Hinrichs, *New bounds for the star discrepancy*, Oberwolfach Report 13/2004, pp. 696–699, especially pp. 697–698: https://doi.org/10.4171/OWR/2004/13.

Audited original proof SHA-256: `7fbb3d20d27cc709ef84fc8106c06472335f892321815921e71019e01e110c7d`.

Acceptance is an independent internal AI-assisted audit. The manuscript and audit are unrefereed; acceptance is not external human peer review, formal verification, or a claim of historical novelty. It settles the displayed universal average comparison, not the separate existence question for good generators. The mathematical proof is self-contained and independent of code.
