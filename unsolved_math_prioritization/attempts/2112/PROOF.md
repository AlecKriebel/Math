# An elementary fourth-power plateau bound for Hofstadter's consecutive-sum sequence

## Status and scope

This is an authored partial result, not a solution of Erdős Problem 423. It strengthens the coefficient in the lower bound stated in Theorem 1.4 of Quanyu Tang's arXiv:2603.09939v2 (23 March 2026): the denominator `log 20` can be replaced by `log 4`. The proof below is self-contained and uses only integer arithmetic. Global novelty has not been established. No claim of an exact asymptotic, a linear upper bound, or `a_n = n + o(n)` is made.

All logarithms are natural.

## Definition and result

Let `a_1 = 1`, `a_2 = 2`; for `n >= 3`, let `a_n` be the least integer strictly greater than `a_(n-1)` which is a sum of at least two consecutive earlier terms. Put `b_n = a_n - n`.

**Theorem.** For every integer `n >= 2`,

\[
 b_n \geq \frac{\log\log n - \log(\log 5 + (\log 2)/3)}{\log 4}.
\]

In particular,

\[
 a_n \geq n + \frac{\log\log n}{\log 4} - O(1).
\]

The mechanism is the following finite statement.

**Plateau lemma.** Suppose `3 <= r <= s` and, for an integer `B`,

\[
 a_j=j+B \qquad(r\leq j\leq s).
\]

Write `T=r+B=a_r` and `V=s+B=a_s`. Then

\[
 V<2T^2(T-1)^2<2T^4.
\]

More precisely, if `Q` is the least integer of the form `2*4^k`, `k >= 0`, strictly greater than `H=T^2(T-1)^2/2`, then `V<Q`.

## Proof of the plateau lemma

First, a power of two cannot be the sum of two or more consecutive positive integers. Indeed, a sum of length `ell >= 2` starting at `u >= 1` gives

\[
 2N=\ell(2u+\ell-1).
\]

If `ell` is odd, it is an odd divisor greater than one of `N`. If `ell` is even, `2u+ell-1` is an odd divisor greater than one of `N`. Either possibility excludes a power of two.

Since the `a_j` are distinct positive integers less than `T` for `j<r`, their sum `S` satisfies

\[
 S=\sum_{j<r}a_j\leq\frac{T(T-1)}2.
\]

We have `T >= 3`, so `H >= T` and `H > S`. The least `Q=2*4^k > H` exists and satisfies `Q <= 4H`, because consecutive members of this geometric progression differ by a factor of four.

Assume for contradiction that `V >= Q`. The plateau contains every integer from `T` through `V`; hence `Q=a_n` for `n=Q-B` with `r <= n <= s`, and `n >= 3`. By the defining representation property, there are `p<q<n` such that

\[
 Q=\sum_{j=p}^{q}a_j.
\]

If `q<r`, the sum is at most `S<Q`, impossible. Thus `q>=r`. If also `p>=r`, this representation is a sum of consecutive positive integers, impossible because `Q` is a power of two. Therefore `p<r<=q`.

Set

\[
 C=\sum_{j=p}^{r-1}a_j,\qquad v=a_q=q+B.
\]

The earlier-only condition `q<n<=s` is essential here: all indices from `r` to `q` still lie in the plateau. Consequently

\[
 Q=C+\sum_{t=T}^{v}t
   =C+\frac{v(v+1)-T(T-1)}2.
\]

Define

\[
 K=4T(T-1)+1-8C.
\]

Since `0 <= C <= S <= T(T-1)/2`,

\[
 1\leq K\leq4T(T-1)+1=(2T-1)^2.
\]

On the other hand,

\[
 (2v+1)^2-8Q=K.
\]

Our choice `Q=2*4^k` makes `8Q` an exact square: put `Y=2^(k+2)`, so `Y^2=8Q`. Because `K>0`, the integer `2v+1` exceeds `Y`. Hence

\[
 K=(2v+1)^2-Y^2\geq(Y+1)^2-Y^2=2Y+1.
\]

It follows that

\[
 Y\leq\frac{(2T-1)^2-1}{2}=2T(T-1),
\]

and therefore

\[
 Q=\frac{Y^2}{8}\leq\frac{T^2(T-1)^2}{2}=H.
\]

This contradicts `Q>H`. Thus `V<Q<=4H=2T^2(T-1)^2`, proving the lemma.

## From plateaus to the explicit lower bound

The sequence is defined indefinitely: after any stage containing at least two terms, the sum of the last two terms is an admissible integer larger than the last term. It is strictly increasing, so

\[
 b_{n+1}-b_n=a_{n+1}-a_n-1\geq0.
\]

If this nondecreasing integer sequence were bounded, it would eventually be constant. Fix a starting index `r>=3` of that constant tail. The plateau lemma would then bound all later terms by a fixed number, contradicting strict increase. Thus `b_n` is unbounded. This recovers a known conclusion only to make the argument self-contained.

For every integer `B>=0`, define

\[
 N(B)=\max\{n\geq1:b_n\leq B\},\qquad M(B)=N(B)+B+2.
\]

These quantities are finite by unboundedness. The first four greedy terms are `1,2,3,5`, so `N(0)=3` and `M(0)=5`.

We claim, for every `B>=1`, that

\[
 M(B)\leq2M(B-1)^4.\tag{1}
\]

If `N(B)=N(B-1)`, then `M(B)=M(B-1)+1`, which implies (1). Otherwise monotonicity and integrality give

\[
 b_j=B\quad\text{for }r=N(B-1)+1\leq j\leq s=N(B).
\]

Here `r>=4` and the plateau lemma applies. Its starting value is

\[
 T=r+B=N(B-1)+B+1=M(B-1).
\]

Its endpoint is `V=N(B)+B=M(B)-2`. Thus

\[
 M(B)<2T^2(T-1)^2+2\leq2T^4,
\]

where the last inequality holds for `T>=2`; this proves (1) in the second case too.

Iterating the logarithm of (1) yields

\[
 \log M(B)\leq4^B\log5+\frac{4^B-1}{3}\log2
 <4^B\left(\log5+\frac{\log2}{3}\right).
\]

For any `n>=2`, set `B=b_n`. Then `n<=N(B)<M(B)`. Taking logarithms twice and rearranging proves the stated theorem. Every logarithm taken here has positive argument; in particular `log n>0`.

## Relation to prior work and the remaining problem

Tang's Section 4 bounds a constant-deviation plateau by a twentieth power using a general quadratic-exponential estimate. The replacement above restricts to powers `2*4^k`, for which the relevant exponential is a square, and uses the sharper one-sided bound `-((2T-1)^2) <= D <= -1` for Tang's quadratic error `D=-K`. This is an elementary modification of the public manuscript's plateau strategy, with full credit to that strategy.

Tang's unbounded-deviation result and the recorded upper bounds are prior work. The upper exponent `4175/2506 + epsilon` is Theorem 1.5; his Section 6.2 credits Sothanaphan and Cushman for `688/413 + epsilon`. These upper estimates are not independently re-proved here. The current partial theorem changes only the coefficient in a double-logarithmic lower bound.

The exact residual is to control omissions from above. In particular, proving `b_n=o(n)`, or even `a_n=O(n)`, is untouched by this argument. A finite bound on the length of a plateau limits how long omissions can stop; it gives no upper bound on how often omissions occur. Computation cannot bridge that logical gap.

## References

1. P. Erdős, *Problems and results on combinatorial number theory, III* (1977), pp. 43–72, original question on p. 71. https://www.renyi.hu/~p_erdos/1977-27.pdf
2. P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), p. 83. https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf
3. Q. Tang, *The Hofstadter consecutive-sum sequence omits infinitely many positive integers*, arXiv:2603.09939v2, 23 March 2026, especially Sections 3–4 and 6. https://arxiv.org/abs/2603.09939v2

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
