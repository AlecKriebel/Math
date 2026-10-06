# Independent audit of short cusp coefficient detection

Problem 30006464, rank 831, OWR-14299577-017. Audit date: 2026-10-06.

## Verdict

**Accept the frozen packet as a scoped partial report, with the nonblocking zero-dimensional convention in PRECISION_ADDENDUM.md. The original problem remains unresolved after five approaches.** No substantive mathematical defect was found in the oldform theorem, linear-cutoff obstruction, finite-frame criterion, stated countermodels, or family-level horostrip equivalence. This is an independent mathematical and computational audit, not formal proof certification, human peer review, or a novelty determination.

The audit preserves all 12 author files byte-for-byte. It does not promote any family theorem to the entire cusp space. It does not turn a cancellation model or a fundamental-domain area calculation into a counterexample to the requested positive-epsilon inequality.

GRAM_ZERO_DIMENSION.patch is an operative, separately supplied correction, with exact before/after hashes in CORRECTION.json. The patch was actually applied to a separate author copy; that corrected copy passed normal, optimized, relocation, and author-mutation replay. Acceptance applies to the unchanged partial results interpreted with this d=0 correction, not to an unperformed future edit.

## Frozen object and dataset identity

The author archive has 16,713 bytes and SHA-256 29e8aa1e0ffe71c40132a437da8ce8d442032aaf330a73d144048899fc78b675. Its MANIFEST.json has SHA-256 8c9aa06e0920943b23c258c8b426408f8d18435f0dec32d454f5f47473650184. The archive has exactly 12 distinct regular flat members, with no PDF, data corpus, source extract, symlink, cache directory, or private coordination material.

All three complete supplied corpora were independently read and hashed. Counts are 15,458 catalog records, 15,458 problem records, and 6,701 research-result entries. The unique target is rank 831 and has no research-result entry. The missing report was represented by {}, not null. Python's default json.dumps([full_problem_record, reports.get(problem_number,{})], sort_keys=True), encoded as UTF-8, gives 4,313 bytes and SHA-256 73ff2584746c1f75184a94669e67aea3ff3000e90e8c2b54cb6bac17cb33a395. The statement digest also matches. Only hashes, counts, and match outcomes are retained in this public audit.

## Primary source and normalization check

[OWR 51/2025, printed page 2756](https://ems.press/content/serial-article-files/52435?nt=1) uses the unnormalized Petersson integral and the expansion f(z)=sum a_f(n)n^((k-1)/2)e(nz). Its question covers all cusp forms and every positive epsilon, with constants depending only on k and epsilon. The squarefree simultaneous Atkin--Lehner-eigenfunction case is reported separately.

[Assing--Li--Wang--Xia, version 1](https://arxiv.org/pdf/2503.05685v1), Section 3, uses raw Fourier coefficients and the Petersson integral divided by the level index. Theorem 3.5 is the general N^(2+epsilon) result. Multiplication by I_N and substitution b_f(n)=n^((k-1)/2)a_f(n) give the attribution in the frozen report exactly. Theorem 3.5 is not the announced squarefree N^(1+epsilon) result. Its nonzero-form hypothesis causes no exception because the zero case is immediate.

Local source PDF hashes and sizes match all three author pins. The OWR problem page and manuscript pages 11, 15, and 16 were visually inspected. A web PDF-screenshot cache failure for the manuscript was resolved by rendering the hash-verified local copy. Public web checks confirmed the source pages remain available. The [arXiv record](https://arxiv.org/abs/2503.05685) shows version 1, submitted 7 March 2025; [the author's publication page](https://www.math.uni-bonn.de/people/assing/) lists this work as a 2025 arXiv preprint. These observations support the stated manuscript status, without asserting the absence of any later unpublished work.

## Mathematical findings

1. **Gram criterion.** The coefficient map and Hermitian Gram formula are correct. Rank deficiency gives an exact obstruction. Valence gives injectivity at floor(kI_N/12), but not a level-uniform least eigenvalue. For a zero-dimensional cusp space the inequality is vacuous; the least-eigenvalue phrase should be restricted to d>0. The addendum states the equivalent quadratic-form version covering d=0.

2. **Norm and coefficient scaling.** The determinant-normalized slash factor for diag(N,1) is N^6. Its conjugate subgroup is Gamma^0(N), of index I_N. The powers N^(-12) in H_N and N^(-11) in coefficient squares are correct, leaving the factor I_N/N. These formulas hold at every positive integer level, not just squarefree levels.

3. **Fixed-linear-cutoff obstruction.** For any fixed C>=1, the denominator at X=CN is a fixed positive finite sum. Along primorial levels, product_(p|N)(1+1/p) diverges by the harmonic lower bound. If 0<C<1, the sampled sum is zero. The resulting failure is restricted to the stronger epsilon=0 requirement. It cannot refute the original positive-epsilon question.

4. **Uniform positive-epsilon family theorem.** Real normalized Delta coefficients satisfy the prime-square identity. Completing the square gives the claimed 3/4 lower bound. Prime indices and prime-square indices do not collide. The dyadic Bertrand argument is valid for real cutoffs, including N=1, and the harmonic upper bound on the level product is uniform. The cutoff 4N^(1+epsilon) and constant H_1(Delta)max(1,8log(2)/(3epsilon)) are correct for all c in C and all levels. No Deligne estimate or Rankin--Selberg asymptotic is used here. The result covers only c Delta(Nz), not arbitrary oldform mixtures.

5. **Rejected shortcuts.** The two-eigenline map is a valid cancellation countermodel, not a modular-form counterexample. The arithmetic cusp sum is correct. The p=101 construction has distinct tiles and certified area at least 12 below height 1/101, exceeding the proposed bound 2 for that domain. Domain choice and the range of a cusp-tail estimate remain essential. The calculation neither refutes the cited theorem nor proves a prime-level improvement.

6. **Horostrip equivalence.** The incomplete-gamma weight, its (4pi)^(-(k-1)) factor, and both directions are correct. Norm conversion in the coarse coefficient estimate is correct. The reverse direction uses eta=epsilon/2, permitting the logarithm to be absorbed. The addendum gives explicit constants and an all-N tail absorption, and distinguishes equivalence of exponent families from an exponent-preserving assertion at one fixed eta. The horostrip integral may exceed the quotient integral; the proof never requires the opposite inequality.

## Replay and independent controls

The author's verifier returns 790 exact finite controls. Its test suite rejects all 18 advertised corruptions in both normal and optimized Python, for 36 rejection runs, and reproduces normal, optimized, and relocated output. The author's corpus verifier also passes against the complete inputs.

The audit additionally computes Delta coefficients through a truncated product expansion rather than using the author's logarithmic-derivative recurrence; checks prime-square identities, coefficient scaling, rational cutoff boundaries, divisor sums, coset distinctness, rectangle geometry, and gamma-polynomial identities; and runs its own resealed-mutation suite. The independent implementation passes 7,769 finite controls; its 26 corruption cases are rejected in both modes (52 executions). Exact coverage and execution results are in AUDIT_RESULTS.json. These computations are supplementary finite controls. The general deductions were reviewed analytically; a numerical pass is not their proof.

The audit manifest checks a strict recursive regular-file inventory. An independent source pin precedes execution in the replay harness. The immutable author manifest digest is checked before executing any author code. All runs use -B, and any __pycache__, .pyc, unlisted directory, symlink, added file, or missing member fails inventory verification. A fresh extracted audit archive is also replayed normally, under -O, and after relocation.

The archive and manifest hashes are integrity anchors, not an external signature or proof of mathematical correctness. A malicious actor allowed to replace all external anchors can replace a self-contained verifier; no stronger authenticity claim is made.

## Remaining obligation

For the full target, establish a uniform positive least-Gram-eigenvalue bound at C N^(1+epsilon), or the equivalent uniform horostrip lower bound, for every form at every level. Neither the author packet nor this audit supplies it. No remote repository action, publication, or third-party outreach was performed in this audit.
