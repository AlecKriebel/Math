# Independent adversarial audit: Function Theory Problem 7.31

## Verdict

**The principal mathematical results pass independent audit.** One minor
clarification is required for the literal full-domain integral wording:
local boundedness and eventual monotonicity do not imply measurability on
an initial bounded interval. Use a tail integral, or add measurability.
This does not affect Theorems 1 and 2, the discrete criterion of Corollary 3,
Proposition 4, or the displayed smooth logarithmic family.

The correct broad-target disposition remains **unresolved / partial after
five recorded approaches**, not solved. The results do not classify all
universally admissible functions, settle the extra shape restriction, or
establish novelty or present-day historical priority.

Audit date: 2026-10-05 UTC. Target: 2307031 / AMR-022-7031, rank 689.
The review was independent of the author's mathematical derivation: no
helper agents, no changes to the frozen authored files, and no remote writes.
The independent controls do not import the author's verifier.

## Frozen input binding

- AUTHOR_MANIFEST.json: 1,444 bytes; SHA-256
  `00cc2ffbfcf74549e852fc4bf2af6f7de4596f398339ec726d46c8b563b5ef11`
- AUTHORED_REVIEW_PACKET.zip: 16,226 bytes; SHA-256
  `53368885eec40f19b35d99a029ffadcc8174d7ebdb32bc36f90699d8acc87a39`
- All eight manifest-listed payloads match their listed byte counts and
  hashes. The ninth file is the manifest itself.
- The archive contains exactly those nine authored files. Each decompressed
  entry is byte-identical to the corresponding frozen file.
- The author's integrity/replay command succeeds and matches EXPECTED_CHECKS.json.

The audit conclusion applies to this exact frozen input, with the integral
clarification below. A later change needs a new binding and review of its
impact. No source PDF, copied scholarly source text, dataset contents, or
private coordination material is included in the audit deliverable.

## Primary-source scope

The governing source was independently opened on the public arXiv site,
and the supplied private PDF was rehashed and its relevant rendered page
visually inspected. The sequence assumptions, two successive cumulative
sums, open-ended function question, comparison series, and historical
update match the authored scope. Zero sequence entries are permitted by
the governing assumptions; they are not an artificial extension introduced
by the counterexample.

Public source: W. K. Hayman and E. F. Lingham, *Research Problems in Function
Theory (New Edition)*, arXiv:1809.07200v2, Problem 7.31, printed page 169,
PDF page 170: https://arxiv.org/pdf/1809.07200v2 .
The PDF has 1,706,228 bytes and SHA-256
`8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
The supplied second private PDF copy has the same hash.

The source's no-progress update is a historical statement. Neither that
update nor this audit proves current openness. The cited Borwein paper is
not needed for any audited proof; this review does not certify its proof
or the author's bounded literature-search completeness. The supplied
catalog identification agrees with the assigned target, but the full
upstream dataset and repository-preflight history were not independently
reconstructed by this audit.

## Theorem 1: single-sequence, single-function counterexample

**Pass.** The proof is an infinite construction, not merely a sequence of
unrelated finite examples.

### Exact ratio and positive state

For a fixed m >= 2, write b and c for the values immediately before an
active index and define a = (c+b)/(m^2-1). Updating gives b' = b+a and
c' = c+b+a = m^2 a. Hence the active ratio is exactly m^2. All states and
active entries stay positive when the old mass is positive.

A separate diagonalization corroborates the block dynamics. If
U = c+mb and V = c-mb, then

    U' = [m/(m-1)] U,
    V' = [m/(m+1)] V.

After r active steps, with q=m/(m-1) and p=m/(m+1),

    c_r = (q^r U_0 + p^r V_0)/2,
    b_r = (q^r U_0 - p^r V_0)/(2m).

These formulas were checked independently against the defining sums,
including non-power-of-two choices of m. They also give an independent
endpoint check of the first two genuine recursive blocks.

### Choice of scales and the cap

After filling the gap to m-1 with zeros, the old mass B is unchanged and
c_{m-1} = sum_{k<m}(m-k)a_k < mB. Thus U_0 < 2mB.
The derivative of x log(x/(x-1)) is negative for x >= 2, which proves
q^m <= 4, including the equality endpoint m=2.

For L_j=2^j m_j active entries, the maximal estimate used in the proof is

    a_n <= 2m_j B_j 4^(2^j)/(m_j^2-1).

The stated scale choice m_j^2 >= 16 B_j 4^(2^j) bounds this by
m_j^3/[8(m_j^2-1)] <= m_j/6 <= n. The constants and inequality directions
are correct. No cap is repaired retrospectively, and arbitrary previous
mass is correctly included in the budget.

Each stage is finite, so a suitable next integer exists. Specifying the
least suitable integer removes any choice ambiguity. Its endpoint exceeds
the previous endpoint, and each new block has positive length, so endpoints
tend to infinity and every index is eventually assigned. The initial
entry is a_1=1, the gap entries are zero, and every other entry is rational
and within the required cap. This yields one admissible infinite sequence.

### Analyticity and signs

The proposed function is one fixed mixture attached to those same blocks:

    f(z) = sum_{j>=1} 2^(-j) m_j^(-1) exp(-z/m_j^2).

For |z|<=R and derivative order k>=0, each summand has absolute value at
most 2^(-j) 2^(-2k-1) exp(R/4). This is summable in j, for every fixed R
and k. Local uniform convergence therefore supplies an entire function
and justifies termwise differentiation. Every term in (-1)^k f^(k)(t)
is strictly positive for t>=0, proving strict complete monotonicity,
positivity, strict decrease, and strict convexity. Dominated convergence
with bound 2^(-j)/m_j proves f(t) tends to zero.

### The two series

The decreasing Gaussian gives

    sum_{n>=1} exp(-n^2/m^2) <= integral_0^infinity exp(-x^2/m^2) dx
                                  = m sqrt(pi)/2.

All mixture terms are nonnegative on the real axis, so Tonelli is
applicable. The total geometric weight is exactly 1, yielding the stated
upper bound sqrt(pi)/2 for the comparison series.

In block j, its own mixture component contributes at least
2^(-j)/(e m_j) per active term. The block has 2^j m_j entries, hence
contributes at least 1/e. Disjoint infinitely many blocks prove divergence.
Other components only increase these sums. The quantifiers are consequently
correct: a single admissible sequence and a single entire, completely
monotone function produce the comparison failure.

## Theorem 2: global count

**Pass.** This is a bound on all eligible indices, not on their locations.
For real m=sqrt(T)>=2, define W_n=c_n+m b_n and P_n=W_n/(n+m).
Direct subtraction gives

    P_n-P_{n-1}
      = [(n-1)b_{n-1}-c_{n-1}+(n-1+m)(m+1)a_n]
        /[(n+m)(n-1+m)].

Since c_{n-1} <= (n-1)b_{n-1}, P is nondecreasing; P_1=a_1>0.
At a good index, (m^2-1)a_n >= c_{n-1}+b_{n-1}. Hence W_n>=qW_{n-1}.
For n>=ceil(m), n+m>=2m, and therefore

    P_n/P_{n-1} >= q(1-1/(n+m))
                    >= (2m-1)/(2m-2) >= 1+1/(2m).

At that good index, b_n<=c_n<=m^2 a_n<=m^2 n, so
P_n<=m^2(1+m). The multiplicative lower bound combines with this upper
bound at the K-th good index. Using log(1+x)>=x/(1+x) gives
K<=(2m+1)log(m^2(1+m)/a_1). The at most ceil(m)-1 earlier indices account
for the remaining term in the theorem. Bounding every finite initial
count also bounds the global count, even if good indices are very far
apart. This reasoning covers nonintegral thresholds without rounding gaps.

## Corollary 3: sufficient condition and integral wording

**Discrete criterion: pass.** Once f is nonincreasing, each dyadic shell
(2^k,2^(k+1)] contributes at most f(2^k)N_a(2^(k+1)). The count has the
required O_{a_1}((k+1)2^(k/2)) bound. Every finite initial ratio range
contains finitely many indices, and local boundedness controls the part
before monotonicity begins. The zero-denominator convention contributes
nothing. Dyadic endpoints are included exactly once.

**Literal integral wording: minor clarification needed.** A nonnegative
locally bounded function may be nonmeasurable on [2,3] and identically zero
for t>=4. It then satisfies the eventual monotonicity and limit assumptions
and the discrete criterion, but its Lebesgue integral starting at 2 is
undefined. Eventual monotonicity alone supplies measurability only on a
tail. This does not undermine dyadic summation or the intended sufficient
condition.

A precise replacement paragraph is:

> For f satisfying the assumptions of Corollary 3, choose A>=2 such that
> f is nonincreasing on [A,infinity). Condition (11) is equivalent to
> integral_A^infinity f(t)(1+log t)/sqrt(t) dt < infinity. If f is also
> measurable on [2,A], local boundedness makes this equivalent to the
> integral starting at 2.

On the monotone tail, the endpoint sandwich is valid and the shell weights
are comparable to (k+1)2^(k/2). Shifting an index changes these weights by
bounded factors, which proves both directions of the equivalence.
The functions 1/[sqrt(t)(log(e+t))^p], p>2, are continuous and decreasing;
the integral criterion applies directly. Their weighted integrands have
asymptotic order 1/[t(log t)^(p-1)], yielding convergence for p>2.
For every alpha>1/2, t^alpha f(t) tends to infinity, so they genuinely go
beyond an O(t^(-alpha)) power condition. No necessity or sharp logarithmic
threshold follows from this argument.

## Proposition 4, obstructions, and conventions

**Pass.** For m>=8, h=floor(log_4(m^2/16)) is a positive integer and
q^(mh)<=(q^m)^h<=4^h<=m^2/16. The same cap estimate, with B=1, validates
all mh active terms. Each has ratio m^2. Since mh has order m log m,
the upper bound's logarithmic factor cannot be uniformly omitted. The
sequence depends on m, exactly as the proposition and scope document say.
This does not prove simultaneous extremality for one fixed sequence.

The isolated-spike control has c_N=(N-1)+1+N=2N, so r_N=2 at arbitrarily
large N; it validly excludes a universal pointwise quadratic lower bound.
For the geometric spikes at n_j=2*3^(j-1), mass just before the j-th spike
is 1+sum_{i<j}2*3^(i-1)=3^(j-1); after it, b_{n_j}/a_{n_j}=3/2.
This invalidates the proposed first-factor summability route without
contradicting a theorem about the different ratio c_n/b_n.

Because a_1>0, c_n>0 for every n. Setting r_n=infinity when a_n=0 and
f(infinity)=0 is therefore unambiguous and is the natural extension for
the f used here. Finite ratios are at least 1. These conventions must
remain explicit when stating the results. A counterexample for strictly
positive a_n at every index is not asserted or needed for the source's
allowed class.

## Independent computational coverage and limits

The separate standard-library script verifies:

- The frozen manifest, all payload hashes, the complete archive membership,
  and decompressed byte equality.
- 21,504 admissible finite-sequence/threshold combinations, including several
  noninteger m values and three distinct positive a_1 values.
- 129,024 index-level checks of the potential identity and budget; 36,588
  qualifying large-index checks of the multiplicative increase.
- 108 two-eigenvalue block cross-checks against direct sum definitions.
- Both initial genuine recursive blocks: m_1=16, L_1=32; m_2=177, L_2=708.
- Sharp-count endpoint controls for twelve m values, including nonpowers
  of two and values immediately around logarithmic boundaries.
- Negative controls for the wrong constant-ratio denominator, omitted
  previous-mass budget, and wrong potential denominator.

All pass. These checks are finite, and do not replace the analytic,
quantifier, or infinite-series arguments audited above. No claim of
machine-formal proof is made.

## Publication and status recommendation

The principal subresults can be described as independently audited authored
partial results, with this audit's integral clarification attached or
incorporated into a separately frozen revision. The frozen author directory
was not altered. Do not label the broad classification solved, claim a
current-literature resolution, claim historical priority, or generalize
the counterexample to every possible additional regularity/shape condition.
