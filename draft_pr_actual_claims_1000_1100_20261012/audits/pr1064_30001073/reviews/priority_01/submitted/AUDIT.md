# Independent audit of the Frobenius permanent bound

## Verdict and publication edition

**PASS.** The candidate proves the requested asymptotic upper bound for OWR 44/2008, problem 9 (corpus identifier 30001073 / OWR-2090-026). No mathematical correction is required. Its stronger row-stochastic theorem is also valid. This is a mathematical acceptance, not a claim of novelty, publication priority, or formal verification.

The distributed publication edition is `PROOF.md`, 8,060 bytes, SHA-256:

`fe83f40d5c6d96a526457eaae290e8b3f0a725b43a91286f818c4fb248db7205`

The independent audit was completed on 2026-10-10 UTC against a frozen original proof. This edition updates only its opening status sentence; its complete mathematical and prior-work text is unchanged. The identity above binds the distributed edition, not the earlier frozen file. The original input identity and the editorial difference were checked during edition preparation.

This audit independently reconstructed each proof step. Source material was inspected directly, rather than treating the candidate's description as verification.

## Exact target and quantifiers

The primary source is Alexander Barvinok and Alex Samorodnitsky's problem 9, *Permanent of doubly stochastic matrices with bounded Frobenius norm*, in *Discrete Geometry*, Oberwolfach Report 44/2008, printed pages 2549-2550. Both original pages were visually inspected. The original question fixes a constant gamma at least one, assumes a nonnegative square matrix with every row and column sum equal to one, and bounds the **unnormalized** sum of squared entries by gamma. It asks for permanent of order exp(-n) up to a polynomial factor. The source explicitly distinguishes a stronger entrywise hypothesis, which the candidate does not assume.

The candidate establishes, for every positive integer n and nonnegative row-stochastic A, with S = sum(a_ij^2),

    per(A) <= exp(-n + e^4 sum(a_ij^2 log(e/a_ij)))
           <= exp(-n + e^4 S(1 + log n)).

Thus for fixed gamma and S <= gamma,

    per(A) <= exp(e^4 gamma) n^(e^4 gamma) exp(-n).

For n >= 2 this implies the stated pure-power bound with exponent 3e^4 gamma. This exponent depends only on the fixed parameter gamma, as required. The known van der Waerden lower bound supplied in the source completes the polynomial-factor order for the doubly stochastic class. No lower bound for arbitrary row-stochastic matrices is claimed or needed.

The candidate correctly treats n = 1 separately: a literal upper bound n^C exp(-n) would give exp(-1) < per([1]) and is false. The all-n bound with a gamma-dependent constant factor remains valid. The source's asymptotic notation supports this treatment.

## Entropy lemma

Let X be an arbitrary random permutation and b_ij its marginals. The proof uses an independent uniform continuous priority for every row. This gives a uniform reveal order and permits the entropy chain rule for each fixed order.

At a realized history, the conditional law q of X_i is supported on unused columns. Every positive q_j has positive marginal b_ij. Consequently the restricted marginal mass Z_i is positive, and the reference law b_ij/Z_i on unused columns is a valid probability law with support containing that of q. Relative entropy therefore gives the claimed local inequality. Averaging recovers

    H(X) + sum(b_ij log b_ij) <= sum_i E log Z_i.

There is no need to define a sequential sampling algorithm on histories outside the support of X. Such a construction could require extra care for sparse matrices; the candidate's local conditional argument avoids that issue. Finite permutation support also makes the positive marginal entries bounded away from zero for each fixed law, so the logarithms along realized histories are integrable.

Conditioning on the complete permutation and T_i = t is legitimate: the other priorities remain independent uniforms. Every column occurs exactly once among X_1,...,X_n, and the i-th marginal row sums to one. Hence

    E[Z_i | X,T_i=t] = b_i,X_i + (1-t)(1-b_i,X_i).

Jensen is used in the correct upper-bound direction. Direct substitution u = b + (1-t)(1-b) gives

    integral_0^1 log(b + (1-t)(1-b)) dt
        = -1 - b log(b)/(1-b),          0 < b < 1.

The limit at b = 1 is zero. Averaging over the sampled value of X_i multiplies the correction by another factor b. This yields exactly

    H(X) <= -sum(b_ij log b_ij) - n + sum g(b_ij),
    g(b) = -b^2 log(b)/(1-b),  g(0)=0,  g(1)=1.

No factor of b, sign, dimension factor, or conditioning term is missing. The deterministic-permutation endpoint gives equality H = 0, which also checks the g(1) convention.

## Gibbs specialization and KL bookkeeping

If per(A) = 0 the upper bound is immediate. Otherwise the Gibbs law on positive-weight permutations is a probability law, and its marginal B is doubly stochastic. An entry b_ij > 0 forces a_ij > 0. The exact Gibbs entropy identity gives

    log per(A) = H(X) + sum(b_ij log a_ij).

Combining it with the entropy lemma gives

    log per(A) <= -n + sum g(b_ij) - D(B||A).

Both A and B have total entry sum n. Therefore D(B||A) equals the sum of the nonnegative scalar divergences

    d(b,a) = b log(b/a) - b + a.

The entry conventions are correct. When b = 0 and a > 0, the original KL summand is zero but d(0,a) = a; the total-mass cancellation, over **all** entries, is what makes the sums equal. When a = 0, necessarily b = 0, and d(0,0) is defined as zero. No inadmissible infinite term is used.

Only row stochasticity of A is needed: it implies 0 <= a_ij <= 1 and total mass n. No hidden column-sum assumption enters the upper-bound proof.

## Scalar absorption

The key scalar claim is valid on its complete stated domain:

    g(b) - d(b,a) <= e^4 a^2 log(e/a).

The endpoints (a,b) = (0,0) and b = 0 are immediate. For positive a,b, the inequality b log(1/b) <= 1-b gives both g(b) <= b and

    g(b) <= h(b) = b^2 log(e/b).

For b >= e^2 a, one has log(b/a) >= 2 and d(b,a) >= b+a >= g(b). The scalar claim follows with a nonpositive left side.

For b < e^2 a, use d >= 0. The derivative h'(b) = b(1 + 2 log(1/b)) is positive for 0 < b <= 1. Thus b <= a gives h(b) <= h(a). If a < b < e^2 a, the two separate inequalities b^2 < e^4 a^2 and log(e/b) <= log(e/a) give h(b) <= e^4 h(a). The endpoint b = 1 is covered by continuity. This proves the advertised constant without an unproved optimization or limiting argument.

Importantly, the divergence is retained until this absorption step. The Frobenius control is applied to the input A, not to its possibly much more concentrated Gibbs marginal B. This resolves the principal potential gap in a naive use of marginal entropy.

## Frobenius conversion and sharpness check

Row-wise Cauchy-Schwarz yields S >= 1. With p_ij = a_ij^2/S, the exact identity is

    sum a_ij^2 log(1/a_ij) = (S/2)(H(p) - log S).

There are at most n^2 entries, so H(p) <= 2 log n. Since log S >= 0, the last display is at most S log n. This establishes the second main inequality. Zero entries are handled by the continuous convention, and S cannot vanish.

For n >= 2, 1 + log n <= 3 log n, so the stated exponent 3e^4 gamma is valid. The constant is loose but does not affect the conclusion.

For k equal uniform blocks of size m, n = km, the candidate correctly computes S = k and per(A) = (m!/m^m)^k. Stirling's formula gives a factor asymptotic to (2pi/k)^(k/2) n^(k/2) in front of exp(-n). Thus a gamma-dependent constant prefactor alone cannot work, and an exponent valid at gamma = k must be at least k/2. This is a valid sharpness obstruction, not a claim that the candidate's exponent is optimal.

## Prior work and limits of acceptance

Anari and Rezaei's *A Tight Analysis of Bethe Approximation for Permanent*, arXiv:1811.02933v2, section 4, equations (1)-(6), pages 11-12, was inspected directly; page 12 was also visually inspected. Their equation (6) contains the Gibbs-marginal random-order comparison before the present conditional Jensen simplification. The candidate credits this prior comparison correctly and supplies a self-contained derivation including zero entries.

The inspected PDF itself identifies version 2 and a December 2019 revision. The candidate's use of the versioned arXiv identifier is accurate. The recent related preprint *Beyond the Bethe Approximation of the Permanent*, arXiv:2608.28031v2, was checked at its title/version page, section 4, Lemma 7 on pages 9-10, and the full-text occurrences of the term Frobenius. Those occurrences concern numerical optimization estimates. This corroborates the candidate's bounded description; it does not establish that no consequence or other literature already gives the theorem.

This audit does not certify novelty. The classical entropy method, the van der Waerden lower bound, and the source's entrywise special case must remain attributed to prior work. The candidate already makes these distinctions. No theorem in the proof depends on novelty-search success or on the recent preprint.

## Inspected source metadata

Public original source:

- DOI: https://doi.org/10.4171/owr/2008/44
- Publisher page: https://ems.press/journals/owr/articles/2090
- Original PDF: https://ems.press/content/serial-article-files/46191?nt=1
- 731,001 bytes; SHA-256 `3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35`.
- Printed pages 2549-2550 are PDF pages 73-74, counted from one.

Direct prior comparison:

- https://arxiv.org/abs/1811.02933v2
- 248,293 bytes; SHA-256 `c6d22620c7963ead242068941ef05562c8c72c40accea40cd3304705d546b405`.
- Equation (6) is on printed/PDF page 12.

Recent related preprint:

- https://arxiv.org/abs/2608.28031v2
- 349,123 bytes; SHA-256 `e166fb3d448e33307396df4eb6d00bef8b804c6387d8aba56c959ea7ff942927`.
- Lemma 7 is on pages 9-10; Frobenius text occurrences are on pages 29-31.

The audit independently hashed and inspected the retained local primary PDFs. Attempts to reopen the DOI and older arXiv abstract using the web tool did not return page contents, so this report does not claim a fresh independent PDF retrieval. The retained PDFs, their identifiers, page contents, and hashes are the inspection evidence.

## Acceptance conditions

The frozen proof is accepted as a complete solution to the exact asymptotic source question. Preserve the stated n = 1 qualification and the prior-work attribution. Do not convert the acceptance into a priority claim or a claim of a sharp exponent. Any mathematical change to the frozen candidate requires renewed review.

This report contains authored analysis and public bibliographic metadata. Source PDFs, rendered source pages, and copied source text are not part of the acceptance deliverable.
