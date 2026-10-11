# Independent mathematical audit

## Verdict

ACCEPT the mathematical content of the frozen reconstruction, with its stated attribution and scope. No correction to its theorem or proof is required by this audit. The acceptance is an independently reasoned mathematical review, not human peer review or formal proof-assistant verification. The argument establishes the unbounded theorem; the computations below only provide finite regression checks.

The audited candidate is exactly 10,951 bytes, SHA256 975b47b36643e8704f3c3657a177d4286d1d0a32919325c9627c839e2478c14c. The canonical source PDF is 110,570 bytes, SHA256 97c4f88da7fd9e70bb50e4679209ba2c5d5483be2648a31b54e274da0e3d0fb4. Both match the supplied freeze. The candidate and all supplied sources were preserved.

## Statement and source audit

The original AIM item is Problem 9.5 in *Rational subvarieties in positive characteristic*. Its displayed text quantifies over p,d with d≥n+1, asks for a degree-d hypersurface in projective n-space over F_p, and requests either point count not congruent to 1 modulo p or failure of rational connectedness. The displayed formulation has no smoothness condition. The official HTML capture identifies the problem as 9.5 immediately before its text; it was retrieved successfully at 2026-10-11 22:00:06 UTC, and its bytes/hash have been independently rechecked. This audit's fresh web-tool attempts on the AIM page returned 502/timeout errors, so no claim is made of a successful new AIM download.

The 2015 MathOverflow question 220163, read live during this audit, explicitly asks for a smooth hypersurface for each d,p,n in the same degree range. It also observes the classical norm-form examples in the unsmoothed setting. This supports the distinction between the literal AIM wording and the stronger smooth theorem, rather than silently changing the original problem.

Ferudun's Theorem 1.1 on PDF page 1 states exactly: all prime p, n≥2, d≥n+1, geometric smoothness and integrality, congruence failure over F_p, and finite deterministic coefficient selection. Its page-1 footnote labels the manuscript unrefereed. The official EulerSolve record, independently read live, dates it 6 September 2026, version 1.0, and explicitly discloses that publication there or on Zenodo is not peer review and that AI systems assisted. The author's “Complete proof” label was not used as evidence that the proof is correct. No novelty or priority inference is made.

The supplied PDF was directly re-extracted, yielding a byte-for-byte match to the supplied text extraction. All proof sections were read. Rendered PDF pages 1, 6, and 7 were visually inspected to confirm the theorem, the equal-prime equations, characteristic-two formulas, completion, and dimension caveats. Fresh web retrieval of the canonical PDF and metadata endpoint failed in the web tool; this did not affect inspection of the supplied hash-pinned PDF. Source archive and author code were neither downloaded for execution nor executed. Only the audit's own checks were executed.

## Proof obligations examined

1. Counting moment. The polynomial is formed with coefficient parameters still formal. Its constant coefficient really is 1, including p=2. Individual degree p-1 disappears because the corresponding monomial omits a variable. Injectivity on the nonzero coefficient grid uses the strict individual degree bound, not a total-degree bound. The affine/projective sign is N_projective=1+(-1)^m C modulo p. No assumption that C itself is a Hasse-Witt determinant is made.

2. Simultaneous coefficient selection. For odd p not dividing d, the degree-p-2 term in the final coefficient vanishes: the pure-power case misses a coordinate and the Q case has a positive exponent 1 in a different coordinate. The bound is p-3, so two count-good final values remain. At most one can satisfy the necessary singularity condition. It is immaterial whether that condition is also sufficient. The p=3 endpoint and the case p dividing t=d-m+1 are both covered.

3. Diagonal smoothness over the algebraic closure. All boundary strata are excluded directly. The torus calculation uses actual integer exponents v_i before reducing scalars modulo p. Cancellation only occurs with nonzero torus quantities. No d-th root normalization over F_p is assumed.

4. Chain family. The sign in the triangular recurrence is correct because d-1=-1 modulo p. A zero proper prefix excludes torus critical points, while B=0 excludes critical points from F=0. The last pure power must remain in F even though its derivative is zero. The boundary argument covers multiple zeros; a sole zero with exponent at least two; the final-coordinate zero; and the special m=3, middle-coordinate zero where the point is excluded by F rather than the gradient. The use d-2≥1 is valid because d≥m≥3.

5. Positive exponent selection. For d>p, the integer interval for the length k of the p-sum block is nonempty throughout 3≤m≤d, including m=d and p=2. For d=p>m, the B residue formula, exact weighted-sum interval, m=p-1 exception, and factorization of the interval-length inequality all check. No p=3 instance of d=p>m is possible, so p≥5 is legitimate there.

6. Equal-prime boundary. The case d=p=m has odd p and permits a=2≠1. Wilson's theorem and the exact product of chain terms yield x_0=a x_last. The recurrence then forces all normalized coordinates into F_p before Fermat's identity is used. This order is essential for geometric smoothness. The coefficient of P^{p-1} is 1; the alternative exponent equation is impossible even at p=3.

7. Characteristic two. The derivative of the added x_0^{d-1}x_1 term vanishes in x_0 and contributes x_0^{d-1} in x_1. Both parities of t are covered. For odd t, the boundary t=1 case is handled separately. On the torus, Q=1 and the d-th powers of all coordinates equal 1 force the x_1 derivative to be nonzero. No use of rationality of torus coordinates occurs.

8. Geometric integrality and dimensions. Over the algebraic closure, two distinct positive-degree factors meet in projective space when m≥3, by the height bound for an ideal with two generators. At their intersection, the product rule forces a singular point. A repeated factor is also singular. Thus a smooth hypersurface in this range is geometrically integral. The n=1 supplement is smooth and point-free but not geometrically integral for d≥2, as correctly stated. No n=0 statement is imported.

9. Exhaustion and meaning. The five construction branches cover every prime and d≥m≥3. The chosen form is always homogeneous, nonzero, and has degree d. Smoothness and point-count failure concern the same equation over the specified F_p. No point-freeness, every-extension claim, efficient algorithm, or assertion about weak rational connectedness from K_X is smuggled in.

## Exact checks

The two locally retained audit-authored checking programs use no third-party manuscript code. All checks use exact modular arithmetic. Explicit exception-raising guards are used instead of Python assertions. The original audit and a fresh packet-preparation rerun both passed in ordinary, -O, and -OO modes; numerical content agrees with the audited outputs across all three modes after excluding recorded timing.

The coefficient and composition checker establishes, on its stated finite ranges:

- 79,967 valid prefix compositions for primes p≤101, p-divisible degrees 2p≤d≤300, and all 3≤m≤d.
- 1,084 residue-reachability checks for d=p and all 3≤m<p, using an independent dynamic program rather than the proof's interval formula.
- 142 formal moment-family checks: p in {2,3,5,7,11}, 3≤m≤6, m≤d≤m+6, plus d=m=p for p=7 and p=11.
- The formal expansion confirms constant coefficient 1, every individual degree bound p-2, the diagonal final degree p-3, and C=1 for fixed equal-prime and binary families.
- 134 exact projective point counts, totaling 459,929 projective points, agree with the moment congruence; no rational singularity occurs in those selected examples. Eight large examples receive the formal check without direct point enumeration.

The Jacobian checker uses SymPy 1.14.0 over GF(p) to form the ideal generated by F and all homogeneous partials in every chart x_j=1. All 34 charts from ten selected equations give the unit ideal. This public report retains aggregate findings only; selected equations and their coefficient/exponent data and chart bases are not distributed.

These ten equations cover binary odd t, binary even t, characteristic-two dividing degree, m=d, the equal-prime boundary, the p=3 diagonal selection, a diagonal t divisible by p, a larger dividing-characteristic chain, and both B=0 composition subcases. A unit ideal over GF(p) remains a unit ideal after scalar extension, so these selected checks certify geometric smoothness, not merely the absence of rational singularities.

Four negative controls were detected:

- A diagonal equation satisfying the excluded discriminant relation has no prime-field rational singularity but has geometric singularities, detected by its nonunit projective singular ideal. This verifies that rational-point scanning alone is inadequate for a geometric smoothness test.
- Replacing the allowed parameter in the equal-prime family by the forbidden value produces a singularity, which the exact Jacobian-ideal check detects.
- In dividing characteristic, a common derivative zero outside the hypersurface creates a false singularity signal if F is omitted from the ideal. The control detects that omission.
- Omitting the characteristic-two repair term from the binary cubic produces a singularity, which the exact test detects.

Every positive and negative check passed. Raw coefficient/exponent records, selected equations, witnesses, individual-degree tables, and chart bases remain outside this public packet. None of these bounded checks alone establishes the unbounded theorem or formal proof-assistant verification.

## Deliverables and restrictions

PROOF.md is the full audited proof and is preserved byte-for-byte. SOURCE_PINS.json records public source identities, byte counts, hashes, retrieval and inspection limitations, and manuscript status. CHECK_SUMMARY.json contains only aggregate verification results and artifact pins. ACCEPTANCE.md preserves the mathematical acceptance report. The verdict, source audit, and all nine proof obligations above are unchanged; EDITORIAL_MAP.json describes the limited editorial changes.

The public boundary excludes checking programs and raw outputs, copied source text and images, input locations, and private coordination material. MANIFEST.json lists and hashes every public payload file; it is a boundary aid, not permission to distribute excluded material. Its own hash and validation controls are held outside the public directory.

No queue, Git state, source file, or frozen candidate was modified in preparing this packet. No third party was contacted. No claim is made about acceptance outside this audit. The packet was prepared locally; no publication was performed during preparation.
