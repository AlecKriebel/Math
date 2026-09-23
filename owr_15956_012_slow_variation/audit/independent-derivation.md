# Independent derivation and boundary audit

Checkpoint: 2026-09-23T04:03:05Z. Completion estimate for the assigned independent verification: 100%. This is a proof audit, not an exhaustive priority certification.

## Exact claim and verdict

Let `f` be a nonzero, nonnegative, real-valued multiplicative function on the positive integers. Put

\[
F(x)=\sum_{n\le x}f(n),\qquad G(x)=\sum_{\substack{n\le x\\n\text{ odd}}}f(n).
\]

If `F(lambda x)/F(x) -> 1` for each fixed positive `lambda`, then

\[
\frac{G(x)}{F(x)}\longrightarrow\left(\sum_{k\ge0}f(2^k)\right)^{-1},
\]

with the reciprocal of infinity defined to be zero. **Verified.** The derivation below uses vanishing boundary mass and tightness of the distribution of the exponent of 2, rather than the candidate's dilation squeeze at `2^K x`.

Nonzero multiplicativity forces `f(1)=1`: choose `n` with `f(n)>0` and use `f(n)=f(1)f(n)`. Hence `F(x)>=G(x)>=1` for `x>=1`, so all ratios are defined. No unboundedness assumption on `F` is needed.

## Independent probability argument

For `x>=1`, sample an integer `N_x<=x` with probability `f(n)/F(x)`. Write

\[
a_k=f(2^k),\quad A_K=\sum_{k=0}^K a_k,\quad A=\sum_{k\ge0}a_k,
\quad r(x)=G(x)/F(x),\quad q_k(x)=\Pr(v_2(N_x)=k).
\]

The unique decomposition `n=2^k m`, with `m` odd, and coprime multiplicativity give

\[
q_k(x)=a_kG(x/2^k)/F(x),\qquad \sum_{k\ge0}q_k(x)=1.
\tag{1}
\]

Set `G(y)=F(y)=0` for `y<1`. Nonnegativity gives the boundary estimate

\[
0\le G(x)-G(x/2^k)\le F(x)-F(x/2^k)=o(F(x))
\tag{2}
\]

for each fixed `k`. Thus `q_k(x)=a_k r(x)+o(1)` for each fixed `k`.

If `A` is infinite, (1) yields

\[
1\ge\sum_{k=0}^Kq_k(x)=A_Kr(x)+o(1).
\]

For each fixed `K`, take the limsup; then let `K` grow. Since `A_K` tends to infinity and `r>=0`, this proves `r(x)->0`.

If `A` is finite, `0<=G(x/2^k)/F(x)<=1` gives the uniform tail bound

\[
\sum_{k>K}q_k(x)\le\sum_{k>K}a_k.
\tag{3}
\]

Consequently the probabilities in (1) are uniformly tight. More explicitly, define

\[
\delta_K(x)=1-F(x/2^K)/F(x),\qquad T_K=A-A_K.
\]

For `0<=k<=K`, (2) is bounded above by `delta_K(x)F(x)`. Summing the difference between `a_k r(x)` and `q_k(x)`, with the remaining differences bounded by `a_k`, proves

\[
0\le Ar(x)-1
=\sum_{k\ge0}a_k\frac{G(x)-G(x/2^k)}{F(x)}
\le A_K\delta_K(x)+T_K.
\tag{4}
\]

The displayed sum is absolutely convergent because `A` is finite; the equality follows from (1). First let `x` tend to infinity with `K` fixed, then let `K` tend to infinity. Equation (4) proves `Ar(x)->1`.

This proof also gives a useful interpretation: if `A<infinity`, the exponent `v_2(N_x)` converges in distribution to the probability law `Pr(V=k)=a_k/A`; if `A=infinity`, every fixed finite set of exponents eventually has probability tending to zero.

## Boundary cases and explicit checks

1. **Only the unit has positive weight.** Let `f(1)=1` and `f(n)=0` for `n>1`. Then `F=G=1`, `A=1`, and the ratio is exactly 1.
2. **Bounded total mass.** For `f(n)=n^{-s}`, `s>1`, one has `F(x)->zeta(s)` and `G(x)->(1-2^{-s})zeta(s)`. The predicted ratio is `1-2^{-s}`, since `A=(1-2^{-s})^{-1}`. Slow variation holds because the positive limit is finite.
3. **Divergent total mass with a finite 2-factor.** For `f(n)=1/n`, the harmonic-number asymptotic gives `F(x)=log x+O(1)`, and the exact even/odd decomposition gives `G(x)=F(x)-(1/2)F(x/2)`. Hence `G/F->1/2`, agreeing with `A=sum 2^{-k}=2`.
4. **Infinite 2-factor.** Let `f(n)=1` if `n` is a power of 2, and zero otherwise. This function is completely multiplicative. For `x>=1`, `F(x)=floor(log_2 x)+1` and `G(x)=1`; slow variation holds and the ratio tends to 0, agreeing with `A=infinity`.
5. **No complete multiplicativity assumption.** A multiplicative function can have `f(2)=0` but `f(2^k)=1` for every `k>=2`, while vanishing at odd prime powers. Its summatory function grows like `log_2 x`, and the ratio still tends to zero. An argument based only on `f(2)` would fail, whereas both proofs correctly use the whole 2-factor.

These are analytic checks, not evidence substituted for the proof.

## The printed prediction is contradicted under the printed hypothesis

The primary report's Problem 3 places a slow-variation assumption beside the different proposed reciprocal `1 / sum_{k>=0}(f(2^k)/2^k)` and a completely multiplicative special-case calculation. The discrepancy is present in the primary source itself: [MFO Report 51/2017, Problem 3, report pp. 31–32](https://publications.mfo.de/bitstream/handle/mfo/3615/OWR_2017_51.pdf?isAllowed=y&sequence=1), DOI [10.4171/OWR/2017/51](https://doi.org/10.4171/OWR/2017/51). Source checked on 2026-09-23 UTC.

The examples above yield two explicit contradictions to that proposed value:

| Function | Verified actual ratio | Printed weighted-factor prediction |
|---|---:|---:|
| `f(n)=1/n` | `1/2` | `1/(sum 4^{-k})=3/4` |
| Indicator of powers of 2 | `0` | `1/(sum 2^{-k})=1/2` |

These establish a mathematical incompatibility; they do not establish which wording the proposer intended.

For a completely multiplicative function, the exact identity is

\[
G(x)/F(x)=1-f(2)F(x/2)/F(x).
\]

Under slow variation its limit is `1-f(2)`. Under regular variation of index one, namely `F(lambda x)/F(x)->lambda`, its limit is instead `1-f(2)/2`. Thus the index-one hypothesis explains the source's special-case calculation, but changing that hypothesis changes the question.

## Why the independent argument does not settle index one

Under index-one regular variation,

\[
\frac{F(x)-F(x/2^k)}{F(x)}\longrightarrow1-2^{-k},
\]

which is positive for `k>=1`. The decisive negligible-boundary estimate (2) is therefore lost. The current proof cannot infer a limit for `G(x)/F(x)` in that setting. Merely expecting `G(x/2^k)/F(x)` to behave like `2^{-k}G(x)/F(x)` would assume the central unresolved ratio behavior. That route is blocked without a new theorem or mechanism.

## Priority interpretation and optional generality

This reconstruction is an elementary positive-convolution/tightness argument. It requires no nontrivial Tauberian theorem. The same mechanism works at every fixed prime `p`, with `G` summing over integers coprime to `p` and `a_k=f(p^k)`. Its conceptual relation to removal of an Euler factor is direct, but calling that relationship a new Tauberian theorem would overstate what has been established.

A small web search for multiplicative summatory functions, slow variation, and Euler-factor removal found the primary report but did not identify an earlier exact statement of this elementary result. This is not an exhaustive priority search and cannot certify originality. The main task's separate priority audit should determine publication wording. The defensible mathematical scope is an affirmative resolution of the literal slow-variation existence question, together with a correction to its accompanying predicted constant. It is not a resolution of the different index-one formulation or a certification of the proposer's intention.

No external person was contacted or outreach prepared.
