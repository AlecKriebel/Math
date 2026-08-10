# Publication Version 1.0 targeted proof audit

**Audit date:** 9 August 2026

**Audited mathematical conclusion:** For every positive rate vector, the
minimal population CTMC of a finite bimolecular weakly reversible
mass-action network with one linkage class is nonexplosive on every closed
communicating class. Each nonabsorbing closed communicating class is positive
recurrent, while an absorbing singleton has the point-mass stationary law.

**Outcome:** **A — the theorem survives.** No invalid implication or
counterexample was found in the targeted interfaces below.

This is a mathematical reconstruction and adversarial audit, not a claim of
independent expert human validation. The immutable Version 0.3 artifacts used
for the audit were byte-identical to their preserved copies:

| Artifact | SHA-256 |
|---|---|
| `main_arxiv_v0.3.pdf` | `2a245221c4d281a0902bbb95c600224aadb2492591b646161baf8bce3eb969e3` |
| `paper_content_v0.3.tex` | `9c58c29b1c53db6734d380dddb1d94b8baa309254e98495113e1db8dc827d42b` |
| `verification_report_v0.3.json` | `08e3c57bbd792ff119def1719ad2fc5151d2e6671e203a0604ab11f22e68b84d` |

## 1. Targeted dependency replay

### 1.1 Marked reaction-channel construction

At a nonabsorbing population state $x$, the embedded chain chooses the
actual labelled channel $r:s\to u$ with probability

\[
  \frac{\kappa_r(x)_s}{\Lambda(x)}.
\]

After it fires, the augmented state is $(x-s+u,u)$. The transition law
depends on the current population and chosen channel, so the augmentation is
Markov, and projection is exactly the population jump chain. Recording the
actual target is essential when different source-target pairs have the same
population displacement.

The irreducibility argument is sound. If $(x',t')$ is reachable, some
channel $s'\to t'$ has predecessor population
$z=x'-t'+s'\in\Gamma$. Population irreducibility gives a channel path from
$x$ to $z$, and appending $s'\to t'$ reaches $(x',t')$. No holding-time
or nonexplosion assumption is used at this stage.

### 1.2 Residual-factorial identity

The carried target is enabled because a preceding channel $s_0\to t$
leaves population $x=z-s_0+t\ge t$. With residual $r=x-t\ge0$, set

\[
  V(x,t)=\sum_i\log((x_i-t_i)!).
\]

If the next channel is $s\to u$, the new residual is exactly $x-s$, and

\[
\begin{aligned}
 \exp\{V(x-s+u,u)-V(x,t)\}
 &=\prod_i\frac{(x_i-s_i)!}{(x_i-t_i)!}\\
 &=\frac{(x)_t}{(x)_s}.
\end{aligned}
\]

Both falling factorials are positive because $s$ and $t$ are enabled.
Thus the logarithmic identity is exact, including zero, unary, pure-binary,
and mixed-binary complexes. A channel sourced at the carried target has
exactly zero reward.

### 1.3 Source-probability entropy identity

For enabled sources, let

\[
 p_x(y)=\frac{\bar\kappa_y(x)_y}{\Lambda(x)}.
\]

Substituting
$(x)_s=p_x(s)\Lambda(x)/\bar\kappa_s$ into the exact expected increment
gives

\[
 d(x,t)=\log p_x(t)-\sum_s p_x(s)\log p_x(s)
 +\sum_s p_x(s)\log\bar\kappa_s-\log\bar\kappa_t.
\]

The entropy is at most $\log|\mathcal C|$, and the rate contribution is at
most $\log(\bar\kappa_+/\bar\kappa_-)$. Hence
$d(x,t)\le\log p_x(t)+C_0$. The zero source causes no exception because
$(x)_0=1$.

### 1.4 Target-following episode recursion

For a fixed directed path
$t=y_0\to\cdots\to y_L=c$, the designated transitions preserve the
residual:

\[
 r+y_0\to\cdots\to r+y_L.
\]

At phases $k<L$, a deviation ends the episode; after reaching $c$, the
episode takes **one final ordinary jump**. This last jump is load-bearing in
the rate-degeneration example below. With
$q_k=\kappa_{y_k\to y_{k+1}}/\bar\kappa_{y_k}$ and
$p_k=p_{r+y_k}(y_k)$, conditioning on the first jump gives exactly

\[
 J_L=d(r+c,c),\qquad
 J_k=d(r+y_k,y_k)+q_kp_kJ_{k+1}.
\]

Every designated edge is actually enabled, every lifted state remains in the
fixed closed class, and the episode has between one and
$|\mathcal C|$ jumps.

### 1.5 Scalar-envelope propagation

For

\[
 F_q(M)=\sup_{0<p\le1}\{\log p+C_0+qpM\},
\]

the Version 0.3 piecewise formula and boundary $M=-1/q$ are correct. The
monotonicity requested for Version 1.0 follows pointwise: if
$M\le M'$, then for every $p\in(0,1]$,

\[
 (\log p+C_0+qpM')-(\log p+C_0+qpM)=qp(M'-M)\ge0.
\]

Taking suprema gives $F_q(M)\le F_q(M')$. Therefore, if
$J_{k+1}^{(n)}\le M_{k+1}^{(n)}\to-\infty$, then

\[
 J_k^{(n)}\le F_{q_k}(M_{k+1}^{(n)})\to-\infty.
\]

Backward iteration through a fixed finite path is valid for arbitrary
positive rate ratios. No numerical calculus claim is needed.

### 1.6 Logarithmic compactification

After fixing the target and extracting a subsequence, every residual
coordinate is either fixed or divergent. With $I$ the set of **all**
divergent coordinates and

\[
 R_n=\sum_{i\in I}\log(r_i^{(n)}+1),\qquad
 w_i=\lim_n\frac{\log(r_i^{(n)}+1)}{R_n},
\]

the weights are nonnegative and sum to one. A divergent coordinate may have
$w_i=0$; retaining it in $I$ is essential because it is a slower
divergent tier, not a bounded coordinate. The binary falling-factorial
asymptotic

\[
 \log(r^{(n)}+c)_y=R_n\,w\cdot y+o(R_n)
\]

is valid for zero, unary, mixed-binary, and pure-double complexes whenever
the fixed source is enabled.

### 1.7 Top-complex alternative and redundant branch

The substantive top-complex alternative is exhaustive. If every complex is
top, $w\cdot X$ is a nonnegative reaction-wise invariant whose value would
diverge inside one communicating class. If a top complex contains two
particles from coordinates in $I$, it is eventually enabled above every
lower terminal. In the remaining case, every top complex contains exactly
one $I$-particle. With $J$ the divergent species occurring in top
complexes, the proof correctly establishes

\[
 y\in T\quad\Longleftrightarrow\quad q_J(y)=1.
\]

The Version 0.3 subcase “every complex has $q_J=1$” is redundant: the
displayed equivalence immediately gives $T=\mathcal C$, already handled by
the all-top case. It is not a false implication and does not affect the
theorem, but it should not appear as an active branch. After deleting it, the
unary-top, shared bounded-companion, and signed-invariant branches remain
exhaustive because $T\ne\mathcal C$ supplies a lower complex with
$q_J=0$.

### 1.8 Exceptional set

For the exact episode drifts $D_c(x,t)$, define

\[
 K=\{(x,t):\min_cD_c(x,t)>-1\}.
\]

If $K$ were infinite, properness of $V$ would supply a divergent sequence
in $K$. Compactification yields either an invariant contradiction or fixed
$s,c$ for which $p_{r^{(n)}+c}(c)\to0$. Scalar propagation then gives
$D_c(x^{(n)},t)\to-\infty$, contradicting membership in $K$. Thus $K$
is finite for every fixed positive rate vector.

Nonemptiness is also valid. Properness supplies a global minimizer $z_*$ of
$V$; every possible episode endpoint stays in the augmented class and has
potential at least $V(z_*)$, so every $D_c(z_*)\ge0$ and $z_*\in K$.

### 1.9 Random-time Foster summation

Let $Y_n$ be the selected episode-endpoint chain, stopped on entering $K$,
and $\sigma_K=\inf\{n:Y_n\in K\}$. With respect to the endpoint filtration,
define

\[
 W_n=V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K).
\]

For $n<\sigma_K$, the selected episode has conditional $V$-drift at most
$-1$; for $n\ge\sigma_K$, the stopped process is constant. Hence
$(W_n)$ is a nonnegative supermartingale. Each $W_n$ is integrable because
after $n$ episodes every coordinate is bounded above by its starting value
plus $2|\mathcal C|n$. Therefore

\[
 \mathbb E W_N\le W_0=V(z),\qquad
 \mathbb E(N\wedge\sigma_K)\le V(z).
\]

Monotone convergence applied to $N\wedge\sigma_K$ yields
$\mathbb E\sigma_K\le V(z)$. No convergence assertion about the $V$-term
is required.

### 1.10 Finite trace-chain closure

Starting from $k\in K$, take one ordinary jump. There are finitely many
successors, each has finite expected hitting time of $K$, and therefore
$\mathbb E_kT_K^+<\infty$. Successive visits to finite $K$ form an
irreducible finite trace chain. The geometric-block argument gives finite
mean positive trace return to a chosen $k_*$. If $M$ is that trace-return
count and $L_j$ are the original-chain excursion lengths, then with
$B=\max_{k\in K}\mathbb E_kT_K^+$,

\[
 \mathbb E\sum_{j<M}L_j
 \le B\sum_{j\ge0}\mathbb P(j<M)
 =B\mathbb EM<\infty.
\]

Projection gives a positive population return no later than the marked
return. The proof correctly distinguishes hitting a finite set, positive
return to that set, trace return to one state, and return in original jumps.

### 1.11 Embedded chain to CTMC

In an infinite nonabsorbing class every population state enables a genuine
channel. Since a positive falling factorial is an integer,
$\Lambda(x)\ge\kappa_{\min}>0$. A finite-mean embedded return count $N$
therefore gives

\[
 \mathbb E\sum_{j<N}H_j
 =\mathbb E\sum_{j<N}\frac1{\Lambda(X_j)}
 \le\frac{\mathbb EN}{\kappa_{\min}}<\infty.
\]

Nonexplosion is not inferred circularly. The recurrent embedded state is
visited infinitely often, and the holding times following those visits are
independent exponentials with the same finite rate. Their sum diverges almost
surely, so total physical time cannot accumulate.

### 1.12 Stationary occupation formula

Let $T=T_{x_*}^+$ and

\[
 \mu(y)=\mathbb E_{x_*}\int_0^T\mathbf 1_{\{X(t)=y\}}\,dt.
\]

The earlier trace argument gives a finite expected number of jumps before
$T$, so transition-count compensators may be stopped at $T$. For
$z\ne y$, the expected number of $z\to y$ jumps during the cycle is
$\mu(z)q(z,y)$. Expected arrivals minus departures at $y$ equal
$\mathbf 1_{\{X(T)=y\}}-\mathbf 1_{\{X(0)=y\}}=0$. Thus

\[
 \sum_z\mu(z)q(z,y)=0.
\]

Also $\sum_y\mu(y)=\mathbb E_{x_*}T<\infty$. Consequently
$\pi(y)=\mu(y)/\mathbb E_{x_*}T$ is a stationary probability distribution;
irreducibility gives uniqueness. This supplies a short self-contained
justification for the displayed occupation formula.

## 2. Exact rate-degeneration calculation

For the directed cycle

\[
 0\xrightarrow{\kappa_0}A
 \xrightarrow{\kappa_1}A+B
 \xrightarrow{\kappa_2}0,
\]

start from population $x=(m,0)$, $m\ge2$, with carried target $A$, and
follow $A\to A+B\to0$, then take the required terminal ordinary jump. Put

\[
 \alpha_m=\frac{\kappa_1m}{\kappa_0+\kappa_1m},\qquad
 \beta_m=\frac{\kappa_2m}{\kappa_0+(\kappa_1+\kappa_2)m}.
\]

The three one-jump expected rewards are

\[
\begin{aligned}
 d_A(m,0)
 &=\frac{\kappa_0}{\kappa_0+\kappa_1m}\log m,\\
 d_{A+B}(m,1)
 &=\frac{\kappa_0}{\kappa_0+(\kappa_1+\kappa_2)m}\log m,\\
 d_0(m-1,0)
 &=-\frac{\kappa_1(m-1)}{\kappa_0+\kappa_1(m-1)}\log(m-1).
\end{aligned}
\]

The exact episode recursion is therefore

\[
 D_0(m,A)=d_A(m,0)+\alpha_m
 \bigl[d_{A+B}(m,1)+\beta_m d_0(m-1,0)\bigr].
\]

For fixed positive rates,

\[
 \alpha_m=1+O(m^{-1}),\quad
 \beta_m=\frac{\kappa_2}{\kappa_1+\kappa_2}+O(m^{-1}),\quad
 d_0(m-1,0)=-\log m+O((\log m)/m),
\]

while the first two rewards are $O((\log m)/m)$. Hence the requested claim
is correct, with the stronger remainder

\[
 \boxed{
 D_0(m,A)=-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
 +O\!\left(\frac{\log m}{m}\right).}
\]

The coefficient is strictly negative for each fixed positive rate vector but
can be arbitrarily close to zero as $\kappa_2/\kappa_1\downarrow0$. The exact
consequence for the proof's exceptional set is recorded in
`supplement/quantitative_limitations.md`.

## 3. Replacement-ready mathematical wording

The following insertions can be used verbatim or lightly styled in the
canonical manuscript.

### Scalar-envelope monotonicity

> The map $F_q$ is nondecreasing: if $M\le M'$, then for every
> $p\in(0,1]$, $\log p+C_0+qpM\le\log p+C_0+qpM'$, and taking suprema
> preserves the inequality. Thus $J_{k+1}\le M$ implies
> $J_k\le F_{q_k}(M)$, which is the inequality iterated in the backward
> induction.

### Slower divergent tiers

> **Remark (zero normalized weight does not mean bounded).** A coordinate may
> diverge while its normalized logarithmic weight $w_i$ is zero. Such a
> coordinate remains in $I$: it belongs to a slower divergent tier and must
> still be counted when deciding whether a complex is eventually enabled.

### Redundant top-complex branch

> In the remaining case $T\ne\mathcal C$. Since
> $y\in T\Longleftrightarrow q_J(y)=1$, not every complex can have
> $q_J=1$; otherwise $T=\mathcal C$, the all-top case already handled.

The unary-top, bounded-companion availability, and signed-invariant branches
then follow without a separate all-$q_J=1$ subcase.

### Random-time summation

> Define
> $W_n=V(Y_{n\wedge\sigma_K})+(n\wedge\sigma_K)$. The selected episode has
> conditional $V$-drift at most $-1$ before $\sigma_K$, and the stopped
> chain is constant afterward; hence $(W_n)$ is a nonnegative
> supermartingale. Taking expectations gives
> $\mathbb E(N\wedge\sigma_K)\le V(Y_0)$, and monotone convergence yields
> $\mathbb E\sigma_K\le V(Y_0)$.

### Absorbing singleton

> Absorbing singleton classes are handled separately: their stationary
> probability is the point mass at the absorbing state. Henceforth positive
> return times are discussed only for nonabsorbing irreducible classes.

### Occupation measure

> The expected number of jumps before $T_{x_*}^+$ is finite. Therefore the
> expected return-cycle occupation measure
> $\mu(y)=\mathbb E_{x_*}\int_0^{T_{x_*}^+}\mathbf 1_{\{X(t)=y\}}dt$
> satisfies $\sum_z\mu(z)q(z,y)=0$: expected arrivals and departures at
> $y$ balance over a cycle beginning and ending at $x_*$. Since
> $\sum_y\mu(y)=\mathbb E_{x_*}T_{x_*}^+$, normalizing $\mu$ gives the
> displayed stationary probability distribution.

## 4. Pre-release deterministic audit evidence

Before the Version 1.0 release freeze, the expanded verifier passed on both
tested Python versions and produced byte-identical canonical reports. The
replay covered the exact residual-factorial and entropy identities,
scalar-envelope branches and pointwise monotonicity, the certificate-validated
top-complex atlases, the rate-degeneration recursion, the stopped-Foster
calibration, a two-state regenerative occupation formula, and the absorbing
singleton calibration.

Counts and digests from that intermediate replay are intentionally omitted
because subsequent release-metadata changes alter the canonical report. The
final packaged verification report and clean-clone transcript are the
authoritative reproducibility records. These computations are regression and
falsification checks; they do not replace the analytic proof of finiteness of
$K$.

## 5. Final mathematical disposition

No theorem defect was found. In particular:

- the rate-degeneration cycle confirms a qualitative, rate-dependent
  limitation rather than defeating recurrence;
- the redundant top branch can be deleted without changing the exhaustive
  alternative;
- scalar propagation is valid once monotonicity is stated explicitly;
- the stopped random-time process is a legitimate nonnegative
  supermartingale with finite-time integrability;
- absorbing singletons are cleanly separated from positive-return notation;
- the stationary occupation formula follows from finite expected jump count
  and return-cycle balance.

Accordingly, this audit supports Outcome A, subject to ordinary external peer
review and the remaining bibliographic, editorial, and clean-reproduction
checks in the Version 1.0 directive.
