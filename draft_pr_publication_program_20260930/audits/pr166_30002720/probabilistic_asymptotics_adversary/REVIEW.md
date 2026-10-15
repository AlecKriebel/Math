# Independent adversarial review: probability and asymptotics

**Outcome: PASS within the assigned mathematical/source-definition scope.** The original theorem survives this independent review. No unresolved probability, asymptotic, cost-definition, or tightness-quantifier gap was found. Historical priority, publication wording, and other ranks are outside this verdict.

Target: PR166, problem 30002720, original claimed_solved1/5. Assigned exact head: efc3f35a72543ad9ae76fd31a860116f1ffd4a32. The original candidate is 13938 bytes with SHA256 c72a38099e93b4d593be231e8f0c4ad726a399c3d61283da9f7b1f7e55801a5c. Its bytes were verified. The head itself is assignment provenance; no repository, branch, ref, checkout, index, remote, or publication operation was performed.

## Strongest verified result

For the stated independent stationary binary Markov strings with persistence probability 3/4, the explicit fixed rank t=F(v), whose ones occur at square positions j^2 for j>=2, is interior, not a cylinder boundary, and a continuity point of m composed with h. For every deterministic real sequence c_n, the singleton-stopping selection cost at rank floor(nt)+1, centered by c_n and divided by sqrt(n), is not tight. Each fixed cost has finite expectation, so the expectation is a valid center covered by this assertion.

The independent proof is in [DERIVATION.md](DERIVATION.md). It reconstructs the probability argument without using the author's checker as proof. The precise obstruction is two deterministic cost bands of asymptotic probability rho>0, separated by an amount whose ratio to sqrt(n_j) tends to infinity. A center may depend arbitrarily on n and on the deterministic bands; the band geometry remains uniform over that center.

## Adversarial issues resolved

| Mechanism | Independent evidence | Status / exact gap |
|---|---|---|
| Uniform empirical-CDF grid bound | Bernoulli cumulant bound, grid union bound, two-sided monotone interpolation; exact rational sample controls | Valid. Mesh term is essential and its omission is detected. No gap. |
| Height / pair-collision event | Independent two-string recursion gives exact collision probability (1/2)(5/8)^(H-1), stronger than the candidate envelope | Valid. Pair independence is unnecessary. No gap. |
| Singleton stopping and uniform cost error | Exact identity L 1[L>1]-L=-1[L=1], truncated before a common separating height; independent operational sample allocation | Valid. Summing untruncated counts forever would be wrong, but the candidate does not do that. No gap. |
| Moving boundaries and local error | Geometric cylinder lengths, endpoint continuation sums, fixed-t remainder bound | Valid. Inclusion is required only eventually. No gap. |
| Integer subsequence and scale | Exact rational ceiling controls and block growth ratio; analytic all-large-index envelope | Valid. n_j strictly increases; rounding disappears at the stated scale. No gap. |
| Triangular binomial / order-statistic CLT | Characteristic-function expansion uniform for parameters near fixed interior t; exact binomial indexing | Valid for the moving endpoints used. No gap. |
| Same-data event dependence | P(E intersect G)>=P(E)-P(G complement), with an explicit counterexample to a product bound | Valid. No independence assumption is hidden. No gap. |
| Arbitrary deterministic centers and tightness | Uniform deterministic interval argument; epsilon=rho/2 gives failure of the definition for every radius | Valid, including expectation centering. No gap. |
| Finite diagnostics versus universal conclusions | Finite controls separated from the analytic all-index proof | Correctly limited. Finite checks alone do not prove any limiting law. |

A useful independent strengthening is an explicit error envelope. With q=3/4 and K_j=floor(j/2), the relative band error is at most

    q^K_j + 976 j^3 q^j + 61 j^2 q^(2j)
        + (61/2) j^2 q^(4j) + q^(10j)/256.

The exact rational value at j=80 is below 1/8, and elementary monotonicity proves that bound for every j>=80. This gives a concrete all-large-index certification rather than an extrapolation from finite diagnostics. It does not give a universal finite-n non-tightness statement; the positive side-window mass still comes from the proved CLT.

## Independent diagnostics and negative mutations

[independent_diagnostics.py](independent_diagnostics.py) implements empirical-CDF and operational cost checks using rational source coordinates with odd denominators, rather than importing the author checker or repeating its finite-word test driver. It also computes collision probabilities through a two-string transition recursion and binomial tails through an exact integer recurrence.

Both [DIAGNOSTICS_NORMAL.json](DIAGNOSTICS_NORMAL.json) and [DIAGNOSTICS_OPTIMIZED.json](DIAGNOSTICS_OPTIMIZED.json) report PASS with 12,235 explicit-exception checks. All seven false variants are detected in both modes:

1. Shift the collision exponent from H-1 to H.
2. Omit the empirical-CDF grid mesh.
3. Continue charging a singleton.
4. Drop the rank's plus one and permit rank zero.
5. Shift the binomial tail threshold by one.
6. Replace variance t(1-t) by unit variance.
7. Substitute an unsupported product bound for dependent events.

The two modes have identical check counts, groups, negative results, and mathematical receipts. No check relies on Python assertions. The provided verify.py was inspected only after the sealed first assessment and was neither imported nor executed. Its check helper uses assert, which is disabled under -O; that is a nonblocking robustness limitation of its finite diagnostic receipt, not a defect in the mathematical proof. The independently produced receipts remain effective under -O.

## Source-definition validation and independence

An independent retrieval of [the primary arXiv v2 manuscript](https://arxiv.org/pdf/1605.02352v2) produced 3160050 bytes with SHA256 0f6a41c3f2acf55026cd9131cc825c77dd02b81f7f6ed8329aacb3ad59ca659e. Printed pages 3-4 were extracted, rendered, and visually inspected. The cost, rank identity, prefix probabilities, and mean profile correspond to the candidate model. This confirms the relevant model definitions; the final publisher-typeset text was not checked. Third-party bodies, extraction, rendered pages, and web capture remain under private/.

[FIRST_ASSESSMENT.md](FIRST_ASSESSMENT.md) and [FIRST_ASSESSMENT_SEAL.json](FIRST_ASSESSMENT_SEAL.json) were sealed at mode 0444 before reading verify.py or obtaining primary secondary evidence. Only the original candidate and the neutral problem.json and source_manifest.json were read before sealing. No author review, gate/status/frozen verdict, root notes, sibling verdict, or operational review was read. Both first-seal files remain byte-identical to their original receipt.

## Final scope and artifacts

Completion estimate for this assigned adversarial mechanism: **100%**. Exact remaining mathematical gap: **none identified**. The conclusion is a reviewed theorem for the stated model, not a novelty certification or a classification of all nonboundary ranks. The interior-t assumption matters for the CLT; endpoint ranks and data-dependent centers are excluded as stated. Small-n and early-j controls are not substituted for the eventual argument.

The machine verdict is [RESULT.json](RESULT.json), the input provenance is [INPUT_IDENTITIES.json](INPUT_IDENTITIES.json), and checkpoints are in [RESEARCH_LOG.md](RESEARCH_LOG.md). FILE_MANIFEST.json records the exact SHA256, byte count, and mode of every retained own/private file, excluding only that manifest itself. Its explicit public own-output allowlist excludes all source bodies and private/scratch contents. No external human communication or outreach was prepared or initiated.
