# Independent adversarial proof audit

Audit timestamp: 2026-09-23 04:03 UTC. Scope: correctness and source compatibility, not novelty. Checkpoint completion estimate: **100% for verification of the literal slow-variation theorem**; the different, presumed index-one problem is outside the proved claim.

## Exact claim and verdict

Let `f: N -> [0,infinity)` be a nonzero, finite-valued multiplicative function. Put

\[
F(x)=\sum_{n\le x}f(n),\qquad G(x)=\sum_{\substack{n\le x\\n\text{ odd}}}f(n),
\qquad A=\sum_{k\ge0}f(2^k).
\]

If `F(2x)/F(x) -> 1`, then `G(x)/F(x) -> 1/A`, where `1/infinity = 0`.

**PASS.** The proposed proof is complete for this statement. It has no hidden assumption that `F` tends to infinity, no need for complete multiplicativity, no uniformity requirement in the dilation parameter, and no illicit exchange of an infinite sum with a limit. The written all-dilations hypothesis implies the dyadic hypothesis used here. Conversely, monotonicity of `F` makes these two hypotheses equivalent.

This is a proof audit by a separate AI agent, not formal proof-assistant verification or external human peer review.

## Line-by-line proof obligations

1. **Normalization and division.** Pick `m` with `f(m)>0`. Multiplicativity applied to `1*m` gives `f(1)=1`. Therefore `F(x)>=G(x)>=1` for `x>=1`; all denominators are nonzero. In the convention defining multiplicativity with `f(1)=1` this is already part of the definition.
2. **Exact decomposition.** Unique factorization `n=2^k m` with odd `m` and coprimality give
   \[
   F(x)=\sum_{k\ge0}a_kG(x/2^k),\quad a_k=f(2^k).
   \]
   Define `G(y)=0` for `y<1`. Each sum for finite `x` is finite, so rearrangement requires no convergence theorem.
3. **Upper bound.** With `A_K=sum_{k=0}^K a_k`, nonnegativity and monotonicity give `F(2^K x)>=A_K G(x)`. Since `K` is fixed when `x` tends to infinity, `limsup G/F <=1/A_K` is valid. Taking the infimum over fixed `K` yields `limsup G/F<=1/A`; this is an iterated bound, not an unjustified joint limit.
4. **Divergent local mass.** If `A=infinity`, nonnegativity and the preceding bounds force the limit to be zero. No lower estimate beyond zero is needed.
5. **Finite local mass.** If `A<infinity`, monotonicity gives `F(x)<=A G(x)` for every `x>=1`, so `G/F>=1/A`. This and the upper bound prove convergence.

## Independently organized second proof

This proof uses summable domination of increments instead of enlarging the summation cutoff. It is included to expose the only analytic input directly.

For each fixed `k`, the odd integers counted by `G(x)-G(x/2^k)` are a subset of those counted by `F(x)-F(x/2^k)`. Consequently

\[
0\le\frac{G(x)-G(x/2^k)}{F(x)}
\le 1-\frac{F(x/2^k)}{F(x)}\longrightarrow0.
\]

The same ratio is at most one. If `A<infinity`, the exact convolution identity therefore gives

\[
0\le A\frac{G(x)}{F(x)}-1
=\sum_{k\ge0}a_k\frac{G(x)-G(x/2^k)}{F(x)}\longrightarrow0.
\]

The last step follows by first bounding the tail by `sum_{k>K}a_k`, then passing to the limit in the finite initial sum, and finally letting `K` grow. No theorem stronger than convergence of a nonnegative series is needed.

If `A=infinity`, retain only the first `K+1` terms of the convolution and subtract their increments. The same fixed-`k` limit gives

\[
1\ge A_K\frac{G(x)}{F(x)}
-\sum_{k=0}^{K}a_k\frac{G(x)-G(x/2^k)}{F(x)},
\]

so `limsup G/F<=1/A_K` for every `K`, completing that case too.

## Exact sufficiency of dyadic slow variation

For a fixed positive integer `K`, telescope

\[
\frac{F(2^Kx)}{F(x)}
=\prod_{j=0}^{K-1}\frac{F(2^{j+1}x)}{F(2^jx)}\longrightarrow1.
\]

Negative powers follow by taking reciprocals at rescaled arguments. For any fixed `lambda>0`, choose fixed integers `u<=v` with `2^u<=lambda<=2^v`. Monotonicity places `F(lambda x)/F(x)` between two ratios tending to one. Thus the dyadic condition is equivalent to slow variation for all fixed positive dilations in this setting.

## Adversarial boundary cases

| Case | Check |
|---|---|
| Identically zero function | If permitted by a nonstandard multiplicativity convention, it makes `G/F=0/0` undefined. The explicit nonzero hypothesis is necessary; it does not remove any meaningful instance of the ratio problem. |
| `f(1)=1`, all other values zero | `F=G=1` for `x>=1`; `A=1`; conclusion is exactly one. |
| `f(n)=n^{-s}`, `s>1` | `F` is bounded and slowly varying; `A=(1-2^{-s})^{-1}`; the limit is `1-2^{-s}`. No divergence hypothesis may be inserted. |
| `f(n)=1/n` | `F(x)` grows logarithmically; `A=2`; the limit is `1/2`. This also disproves the printed weighted prediction. |
| Indicator of powers of two | Completely multiplicative, `F(x)=floor(log_2 x)+1`, `G(x)=1`, `A=infinity`; the limit is zero. Handles divergent local mass explicitly. |
| `a_0=1,a_1=2,a_k=0` for `k>=2`, all odd prime-power values zero | Multiplicative but not completely multiplicative. For `x>=2`, `F=3,G=1`; `A=3`; no bound `f(2)<=1` is valid in the general theorem. |
| Sparse, irregular or vanishing `a_k` | Only nonnegativity and the value of their total sum enter. No regularity of `a_k` is assumed. |
| Nonintegral `x` and exact powers of two | The finite convolution uses inequalities `n<=x`, so floor discontinuities introduce no endpoint error. |

The hypothesis is essential: for `f(n)=1` one has `A=infinity` but `G/F ->1/2`, while `F(2x)/F(x)->2`, not one. This is not a counterexample to the proved theorem; it directly prevents applying its conclusion to index-one regular variation.

## Source compatibility and promotion boundary

The primary source is *Oberwolfach Report 51/2017*, DOI [10.4171/OWR/2017/51](https://doi.org/10.4171/OWR/2017/51), Problem 3 on printed p. 3066 (PDF page 32). The [EMS report PDF](https://ems.press/content/serial-article-files/46710) was retrieved on 2026-09-23; its text explicitly uses `F(lambda x)=(1+o(1))F(x)`, defines `G` as the odd summatory function, and prints the different predicted reciprocal `1/sum_k f(2^k)/2^k`. It also gives the completely multiplicative expression `1-f(2)/2+o(1)`. The supplied unsolvedmath URL could not be retrieved by this agent's web tool; the original report was accessible. The report is enough to verify the published wording.

The mismatch is mathematically decisive, not just a typographic suspicion. For the strictly positive completely multiplicative function `f(n)=1/n`, write `H_N=sum_{n=1}^N 1/n`. Then

\[
F(x)=H_{\lfloor x\rfloor},\qquad
G(x)=H_{\lfloor x\rfloor}-\frac12H_{\lfloor x/2\rfloor}.
\]

Since `H_N=log N+O(1)`, `F` has the printed slow-variation property and `G/F ->1/2`. The printed weighted reciprocal is instead `1/(sum_k 4^{-k})=3/4`.

In the completely multiplicative case the exact identity is `G(x)=F(x)-f(2)F(x/2)`. Slow variation makes its limit `1-f(2)`; regular variation of index one makes it `1-f(2)/2`. Thus the source's surrounding formulas are consistent with changing the printed dilation factor from one to `lambda`. That is an inference about a possible intended statement, not documentary proof of authorial intent or an established erratum.

**Safe promotion:** a complete elementary resolution of the existence question *under the printed slow-variation hypothesis*, together with a correction to its printed predicted value. **Unsupported promotion:** a resolution of the presumed index-one formulation, a verified statement of authorial intent, or a claim of research priority. Those require separate evidence.

## Exact remaining gaps

- Mathematical correctness of the literal theorem: none found after the checks above.
- Novelty or priority: not decided by this audit; the proof is elementary enough that classical related results and prior corrections need independent investigation.
- Presumed index-one problem: this argument does not prove it. Replacing the hypothesis while retaining this proof is invalid.
- Formal machine verification: not supplied. Numerical scripts may check examples and finite identities but cannot establish the universal asymptotic theorem.
