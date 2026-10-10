# Scoped acceptance: sparse low-rank zero squares

Problem **30006403**, rank **1213**, alias **OWR-14299518-027**. Mathematical review: 10 October 2026 UTC.

**Verdict: accepted without mathematical correction as a partial-result report. The original arbitrary-real-matrix conjecture remains UNRESOLVED. Approach 1 of 5.**

## Exact distributed editions

- APPROACH_1.md: 15984 bytes; SHA-256 `15e17af915d2f9445a6ed368f3c50c35bb2c2d753757c41f40d9913ce93d6b24`.
- INDEPENDENT_AUDIT.md: 11660 bytes; SHA-256 `5d8540680d345ad6526de48c9e0a7cd783faa537a6c4b4718d02dd61aac7b645`.

The report retains the complete mathematical exposition, every proof, source qualification, example and exact stopping point. The independent audit retains all substantive mathematical and source checks. Computational descriptions and out-of-edition administrative material are omitted; PROVENANCE.md records the boundary. The audit's previously incomplete inline-math opening delimiters were repaired before edition preparation without changing mathematical content. These identities bind the actual distributed editions; MANIFEST.json binds the other distributed members.

## Accepted mathematical scope

For an n by n matrix over any field, with n≥1, rank r and E nonzero entries, z(M) denotes the maximum integer side of an all-zero submatrix with independently chosen rows and columns. A zero square need not be principal. Put h=z(M)/n and δ=1−E/n².

1. The sparse-row-basis lemma proves z(M)≥max{0,ceil(n−sqrt(rE))}. It includes rank zero, integer rounding and the exact rank-one support-rectangle boundary.
2. For each integer k>r≥1, the with-replacement column-span argument proves δ^k≤h+[k/(k−r)]h(1−h), hence h≥[(k−r)/(2k−r)]δ^k. With E≤εn², the same bounds hold after replacing δ by 1−ε. The discrete sampling inequality holds for 0≤ε≤1; rank zero is treated separately for its exact answer z=n.
3. Under the target density range 0<ε<1/2, the resulting uniform estimate is z(M)≥ceil(n exp(−6 max{sqrt(εr),εr})). The audit also verifies the endpoints 0≤ε≤1/2. The square-root target holds with C=6 for εr≤1 and C=2 for εr≤1/4. More generally a bounded εr range admits a constant depending on that range.
4. For each integer d≥1, the F₂ dot-product array indexed by F₂^d has rank d, n=2^d, density (1−2^(−d))/2 and z=2^floor(d/2). This is a field-independent-method obstruction only. Its real rank is 2^d−1, so it is not a counterexample to the real-rank target.
5. For integers d≥2 and 1≤k≤d/2, the real k-set intersection family has rank d, n=binom(d,k), density p=1−binom(d−k,k)/binom(d,k), and z=binom(floor(d/2),k). The report's exact bounds for d≥4k² show the necessity of square-root-exponent order for this real family; they do not prove the universal conjecture.
6. The report correctly excludes replacing support density by entry mean, assuming that entrywise squaring preserves rank, or identifying the Boolean support matrix's rank with the original real rank. The sampling proof's Jensen inequality, adapted indicators, dependent-step count and integer maximal-square implication require none of those reductions.

## Attribution, conditions and claims not granted

Singer–Sudan Section 3 / Theorem 1.7 is the prior probabilistic dimension-drop method. The report is an elementary adaptation/refinement, with no original-discovery or best-known-bound claim. HMST Conjecture 1.8 states the real target; its Lemma 4.7(2) is a prior small-density result. The comparison of 1/(16r) and 1/(4r) is a parameter comparison, not a novelty certification.

The exponential corollary retains its density restriction. Without it, a fully nonzero rank-one matrix rules out any positive lower bound for a zero square. HMST's nonnegative-entry/mean-based theorem, including its logarithmic rank term in the inspected body statement, is not an arbitrary-real support-density result. The source inspections are bounded and do not certify exhaustive present-day literature status.

For unbounded εr, the proved exponent is linear in εr, while the original conjecture demands one absolute constant multiplying sqrt(εr). That gap remains open within this work. No proof or counterexample to the full original conjecture, no novelty claim, and no mathematical correction or new proof-search approach is asserted by this edition.

AI-assisted and unrefereed. The independent check is an AI-assisted mathematical audit, not external human peer review or formal proof-assistant verification. Substantive mathematical changes require fresh review.
