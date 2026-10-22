# Acceptance: partial local-cycle packing

Problem 30002668 / OWR-13110-017. Edition date: 10 October 2026.

Accept the exact packing bound M²/(M + sum_f d(f)²), the uniform planar-zone deduction sum_f d(f)² <= (C_z+4)N², and their consequence: every general-position arrangement with n lines in each of three colors has Omega(n²) pairwise vertex-disjoint properly colored dual four-cycles. General position excludes parallel pairs and triple concurrence. The proof counts all faces, including unbounded faces and their genuine boundary rays.

The quadratic single face-simple path target remains unresolved. Aggregate length in disjoint cycles or paths is not a single-path bound. The source-derived single-path guarantee is at least 3n edges, obtained by coarsening colors and applying Aichholzer et al., Theorem 3.2. There is no accepted counterfamily to the exact balanced three-color target and no novelty claim.

The cited 3k:2k two-color obstruction is restricted to every odd positive integer k. This infinite subsequence suffices to refute the color-insensitive joining inference, while its two colors and unequal balance prevent it from being a counterexample to the actual target. REPORT_CORRECTION.patch documents the exact source-scope correction, already incorporated in MATHEMATICAL_REPORT.md.

The note and independent internal AI audit are unrefereed. Acceptance is limited to the above partial statements and is not external human peer review, journal acceptance, or formal proof-assistant certification. The zone theorem and cited two-color obstruction are expressly credited external dependencies. Finite diagnostics are supplementary; no longest-path search or finite computation is used as a substitute for the all-order packing proof.
