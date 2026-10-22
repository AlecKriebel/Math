# Source-based independent review request

Review the exact part(3) iid-coordinate statement and the credited Cai–Han–Zhang moment-lemma corollary in KNOWN_RESULT.md. Proposed classification: known-source resolution0/5 **under the explicitly stated standard ranges**. Do not infer a general OSNAP theorem or silently remove the range qualifications.

Critical checks:

1. Exact distribution, transposition to d×m unscaled signs, variance s/m, and centered Gram normalization by s
2. Published Lemma5.4's applicability: independent, symmetric, entrywise bounded variables; inspect its full proof, including scalar mixed-moment signs and rounded dimensions
3. Lemma2.6 and the dimension factor cancellation from d/r times an r-dimensional Gaussian trace; no hidden log(m)
4. Even q, rounding boundq≤7log(d/δ), constant choices10,000 and70,000, and the strict Markov tail inequality
5. d=1 and δ close to1; standard lower sparsity convention versus the explicitly recorded subunit-s literal counterexample
6. The complete source separates iid-coordinate part(3), arbitrary-U iid part(1), and fixed-column-count part(2); later general embedding bounds must not be conflated with this result
7. Credit and disposition: the core moment comparison is published prior work. No new concentration theorem, optimal constants, novelty or full-resolution claim outside the stated range

Primary files are bound separately by SOURCE_MANIFEST.json. In the published Cai–Han–Zhang PDF, statements are on p5 andp24; the relevant bounded-comparison proof is pp24–26, Gaussian moment proof pp18–19. Bandeira's exact full contribution is pp76–77. All these relevant sections were read and key pages visually verified. The source's auxiliary part(1) normalization issue is disclosed and not imported into the unambiguous part(3) law.

The finite checker gives2,652 exact controls, including36 exhaustive sparse trace-moment comparisons to Gaussian moments counted by Wick pairings. No raw datasets or copyrighted full sources are included in the public packet. Publication requires a separate gate.
