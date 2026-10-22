# Approach 3: Recover absorption from complete closeness and invariants

Z-absorption gives the similarity control used by Perera–Toms–White–Winter to transfer complete closeness and scaled Cuntz semigroups. Their Corollary 4.15 prints the radius 1/6422957. That statement is cited as published, with an unresolved parameter discrepancy in its proof chain.

The original exact-integer check of the printed Proposition 4.13 is arithmetically correct: its remainder is 3427616. Independent inspection found that Lemma 4.12 has a leading factor k in β which Proposition 4.13 omits. At k=5/2 the retained coefficient is 3962640, rather than 1585056. Keeping it gives a conservative sufficient radius 1/16000000 for the common-unit unital subcase, verified in §2.4 of `MATHEMATICAL_AUDIT.md`; the positive integer remainder is 1066385760000. The larger published radius is not independently certified by these calculations. No counterexample to that radius is asserted.

The missing step remains a theorem forcing Z-absorption from the available Cuntz-semigroup information under the full nonnuclear hypotheses. The 2026 survey's §27 retains that question. No proof can silently insert nuclear classification hypotheses.

Outcome: credited invariant transfer, corrected quantitative verification, and an explicit source-level caveat. No absorption conclusion, improved radius, or novelty claim.
