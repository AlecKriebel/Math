# Independent audit of the fourth-power Hofstadter plateau bound

## Decision and accepted scope

All logarithms below are natural.

Accepted as a mathematically valid partial lower-bound theorem for the classical Hofstadter consecutive-sum sequence. No correction to the mathematical proof is required in the sealed version identified below. The argument proves the finite plateau bound and its stated explicit consequence for every integer n >= 2:

\[
 a_n-n\geq
 \frac{\log\log n-\log(\log5+(\log2)/3)}{\log4}.
\]

In particular, it improves the displayed double-logarithmic coefficient in Tang's version 2 from 1/log20 to 1/log4. This decision does not certify global novelty, priority, an exact asymptotic, a linear upper bound, density one, or a proof-assistant formalization.

The reviewed candidate manifest has SHA-256 d8305c9503858d2e71313c6a3ce037b471641ddc29f720b94a393b8c4f0ca6e1. Its PROOF.md is 6624 bytes with SHA-256 afd65a9697245e62f25ee9ad9359b893e213d87d6bb46ad17724b73ccbb5297c. All eight manifest members were independently checked against their byte counts and hashes, with exact file inventory and symlink rejection.

## Exact target and source comparison

The target starts with a_1=1 and a_2=2. Each subsequent term is the least integer strictly exceeding its predecessor that is expressible as a sum of at least two consecutive earlier terms. The original printed formulation on page 71 of [Erdős 1977](https://www.renyi.hu/~p_erdos/1977-27.pdf) and the explicit least-exceeding formulation on page 83 of [Erdős and Graham 1980](https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf) were visually inspected. The audited definition preserves these conventions.

[Tang, arXiv:2603.09939v2](https://arxiv.org/abs/2603.09939v2), revised 23 March 2026, states the log20 denominator in Theorem 1.4 and uses a twentieth-power threshold recurrence in Section 4. Its Theorem 1.5 states the exponent 4175/2506+epsilon; Section 6.2 attributes the 688/413+epsilon refinement to the combination of Sothanaphan's observation and Cushman's estimate. Problem 6.1 asks whether a_n=n+o(n). The independently opened arXiv metadata describes a submitted manuscript, not a journal acceptance. The relevant source comparisons were checked against the complete pinned PDF and extracted text; pages 2 and 14 were also visually inspected. This audit does not re-prove the background upper bounds.

The complete Tang PDF is 824110 bytes with SHA-256 0ca63f8c662233b1cf77005a64745ffcbd3d37d439dd9635940d43977d4b2711. The retained primary-source collection's 133 listed files all matched their pinned hashes and sizes. A live problem-tracker request returned 403; no current tracker-status claim is inferred from that failure. Novelty searching in the candidate is explicitly bounded and is not converted into a priority claim here.

## Audit of the plateau lemma

Suppose 3 <= r <= s and a_j=j+B throughout [r,s]. Put T=a_r and V=a_s. Strict increase in positive integers gives T>=3 and places every earlier term in {1,...,T-1}. Therefore the entire earlier prefix has sum

\[
 S=\sum_{j<r}a_j\leq T(T-1)/2.
\]

This bound is valid even if r is not the beginning of a maximal plateau. The proof never assumes such maximality.

Let H=T^2(T-1)^2/2 and choose the least Q=2*4^k strictly above H. Because T>=3, one has H>=18, H>=T, and H>S. A preceding member of the geometric progression exists, so minimality yields Q<=4H. These facts justify the threshold placement and the factor four without a small-T exception.

Assuming V>=Q places Q inside the plateau. Its index n=Q-B is an integer in [r,s], and n>=3. The actual sequence rule supplies a representation

\[
 Q=\sum_{j=p}^{q}a_j,\qquad 1\leq p<q<n.
\]

The strict p<q enforces at least two summands; q<n enforces earlier-only summands. These are not optional conventions.

There are three exhaustive positions for this interval:

1. If q<r, its sum is at most S<Q.
2. If p>=r, all its summands are consecutive positive integers because q<n<=s. Such an interval of length at least two cannot sum to a power of two: the factorization 2Q=ell(2u+ell-1) produces an odd divisor greater than one, whether ell is odd or even.
3. Consequently p<r<=q. With C=sum from p to r-1 of a_j and v=a_q, splitting at r gives

\[
 Q=C+\frac{v(v+1)-T(T-1)}2.
\]

The third case uses q<n<=s to keep the full segment from r through q inside the known plateau. It uses neither future terms nor the next plateau. Its prefix contribution satisfies 0<C<=S; the proof safely relaxes this to 0<=C<=S.

Rearrangement gives

\[
 (2v+1)^2-8Q=K,
 \qquad K=4T(T-1)+1-8C,
 \qquad 1\leq K\leq(2T-1)^2.
\]

The lower bound K>=1 follows exactly from C<=T(T-1)/2. This positive sign is decisive. For the chosen Q, Y=2^(k+2) is an integer with Y^2=8Q. Since K>0, the positive integer 2v+1 is at least Y+1. Thus

\[
 2Y+1\leq K\leq(2T-1)^2,
 \quad Y\leq2T(T-1),
 \quad Q=Y^2/8\leq H.
\]

This contradicts Q>H. It proves V<Q<=4H=2T^2(T-1)^2<2T^4, including strictness of the claimed endpoint inequality. No estimate for general quadratic-exponential equations is needed.

## Audit of the all-index deduction

Existence of the infinite greedy sequence is elementary: the sum of the last two terms is always an admissible integer larger than the current last term. Strict increase gives b_n=a_n-n>=0 and b_(n+1)>=b_n. A bounded nondecreasing integer sequence b_n would eventually be constant. Applying the finite plateau lemma to arbitrarily long finite portions of that tail would bound all its terms, contradicting strict increase. Hence b_n is unbounded.

For every nonnegative integer B, the set defining N(B)=max{n:b_n<=B} is nonempty because it contains the seed indices, and finite by monotonicity and unboundedness. Let M(B)=N(B)+B+2. The first four terms are 1,2,3,5, so N(0)=3 and M(0)=5.

For B>=1 there are two cases, both needed because b_n can skip integer values:

- If N(B)=N(B-1), then M(B)=M(B-1)+1<=2M(B-1)^4.
- If N(B)>N(B-1), every index from r=N(B-1)+1 through s=N(B) has b_j=B. Here r>=4. The lemma starts at T=r+B=M(B-1), and its endpoint is V=N(B)+B=M(B)-2. Therefore

\[
 M(B)<2T^2(T-1)^2+2\leq2T^4.
\]

The final inequality is valid for T>=2: its right-minus-left difference is 2T^2(2T-1)-2>0. The actual starting T is at least 5, so there is considerable slack.

Iterating log M(B)<=4 log M(B-1)+log2 gives

\[
 \log M(B)\leq4^B\log5+\frac{4^B-1}{3}\log2
 <4^B\bigl(\log5+(\log2)/3\bigr).
\]

For each individual n>=2, take B=b_n. The definition of N gives n<=N(B)<M(B). Since log n>0, taking a further logarithm and rearranging yields the claimed lower bound. This is an all-index deduction, not a subsequence argument, and its proof does not depend on numerical testing. The inequality remains valid at n=2 and n=3, where its right-hand side is negative.

## Independent computational checks

The audit used separately authored Python with explicit exception guards, so all checks remain active under normal, -O, and -OO execution. The three runs produced byte-identical reports.

An integer-bitset implementation generated all sequence terms through value 200000. Its bitset for suffix sums is updated by shifting by each newly accepted term; a separate persistent bitset records sums of at least two terms. This implementation differs from the candidate's by-value backward-suffix loop. A second independent implementation uses positive sliding windows to minimize all eligible interval sums at every greedy step. Its first 4000 terms agreed with the bitset generator.

The independent complete finite sequence has 199224 terms, last term 200000, deviation 776, and comma-delimited-with-newline SHA-256 bd298dd4ff229b6577f5bc6e11bbcee67533db430423dc360f435a106ca626be. These values and the entire-sequence hash match the candidate's report.

Additional exact checks covered:

- All 765 observed constant-deviation plateaus, including the final observed partial plateau.
- All 775 threshold recurrences whose endpoints are certified by a later term: 12 skipped-level cases and 763 nonempty-plateau cases.
- All 2604372 allowed integer C values for 3<=T<=250, testing the crossing equation through its exact discriminant.
- Every subset prefix below T for 3<=T<=11: 2044 lists, each searched directly for eligible intervals summing to the selected Q.
- Exact threshold and square-gap arithmetic for 300 much larger T values, up to 10^100+1.
- Separate numerical evaluation of the explicit lower bound throughout the generated finite sequence; its smallest observed margin was about 0.3722026018 at n=3.

Negative controls confirmed that explicit guards reject false conditions and that allowing C beyond the prefix-sum bound can produce a forbidden crossing representation. Ten package-integrity mutations were rejected in all three Python modes, including changed, truncated, missing, extra, and symlinked files; manifest tampering; duplicate entries and JSON keys; and path traversal. The original candidate remained unchanged.

The candidate's own assertion-based verifier now explicitly rejects -O/-OO, resolving a reproducibility risk identified during review. This audit did not rely on its assertions: it used the independently authored implementations above. Finite tests supplement the proof and do not establish an infinite theorem by themselves.

## Boundaries and remaining work

The fourth-power obstruction is valid at its claimed level. The candidate's synthetic family showing a crossing representation with Q of order T^4 is also algebraically correct, but those lists are not established greedy prefixes. It only limits the relaxed single-crossing argument and does not prove the optimality of this plateau theorem or lower-bound coefficient.

This result forces deviations to increase eventually, with a stronger quantitative lower bound than the specific Tang v2 display. It provides no upper control on their frequency. The exact asymptotic, b_n=o(n), and even an O(n) upper bound for a_n remain unproved by this argument. The accepted output should retain those limits and its explicit credit to Tang's plateau and threshold-function strategy.

## Edition and review statement

This prose-only edition preserves the complete substantive mathematical argument
and its qualifications. The AI-assisted work is unrefereed. Acceptance refers
only to the independent internal AI audit of this partial theorem; no external
human peer review, journal acceptance, or formal proof-assistant certification
is claimed. No mathematical correction was required.

The historical finite checks and scholarly-source inspection are described
for provenance. Preparing this edition added no mathematical test execution
and no scholarly-source retrieval or inspection. The original sealed candidate
and audit are unchanged. Programs, raw datasets, detailed execution receipts,
full computational certificates, copied source documents/text/images, and
private coordination material are not distributed. This is a mathematical
prose and verification-metadata edition, not an executable reproduction package.
