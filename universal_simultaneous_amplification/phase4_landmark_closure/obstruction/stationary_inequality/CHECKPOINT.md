# Stationary-inequality and reflected-level checkpoint

Date: 2026-08-02 (America/Los_Angeles)

This folder records a self-contained checkpoint for two related open
questions about the stationary law `pi` of the dB geometric-union dual.
Write

\[
 \theta=r-1,\qquad h_r(x)=\frac{rx}{1+\theta x},
 \qquad \pi_k=\Pr_\pi(|A|=k).
\]

## 1. Main stationary inequality

The target at `r=3/2` is

\[
 \sum_i\frac{\pi(\{i\})}{d_i}
 \ge \frac94 H\left(\frac{E_\pi|A|}{n}-\frac13\right),
 \qquad H=\sum_i\frac1{d_i}.
\tag{S}
\]

Status: **OPEN**.

No counterexample was found in the following numerical screens:

- all connected unweighted graphs through seven vertices;
- broad positive-weight searches through seven vertices, including
  heavy-tailed weights and near-reducible limits;
- exact rational spot checks through five vertices.

These calculations are evidence only.  In particular, no sampled fixation
probability is being used as proof.

There is a useful pointwise Bonferroni reduction.  If

\[
 X(A)=\sum_{i\in A}\frac1{d_i},
\]

then

\[
 \sum_i\frac{\pi(\{i\})}{d_i}
 \ge E_\pi\{(2-|A|)X(A)\}.
\tag{1}
\]

Numerically, (1) was sufficient in every tested graph for which
`E|A|/n>1/3`; it is not itself a proved stationary inequality.

Unrestricted Boolean-cubic Poisson certificates were found numerically for
many complete-support graphs through eight vertices: there was a polynomial
`g` of degree at most three such that the target integrand minus
`Dg` was strictly positive at every nonempty state.  Quadratic certificates
can fail.  The cubic observation is **NUMERICALLY OBSERVED / OPEN**.  A
stronger attempted representation by nonnegative combinations of
intersection functions on sets of size at most three is false already on
`K_7`.

## 2. Exact hierarchy obstructions

The companion file `HIERARCHY_OBSTRUCTION.md` and its exact verifier prove:

1. an exchangeable law on `K_7` at `r=3/2` satisfies normalization, every
   singleton stationarity equation, and the exact first size-moment balance,
   but violates (S);
2. an exchangeable law on `K_9` satisfies normalization, every singleton
   equation, and the first two exact factorial-moment balances, but still
   violates (S).

Neither law is stationary for the full dual chain, so these are not graph
counterexamples.  They prove that a successful moment argument must use at
least third-order information (or a genuinely graph-sensitive weighted
observable).

For reference, if `J_v` is the number of distinct outside additions made by
a burst at occupied `v`, then for every `j>=1`, Vandermonde's identity gives

\[
 \mathcal D\binom{|A|}{j}
 =\sum_{v\in A}\left[
 -\binom{|A|-1}{j-1}
 +\sum_{s=1}^j\binom{|A|-1}{j-s}
 E\binom{J_v}{s}\right].
\tag{2}
\]

This formula is exact.

## 3. Reflected stationary levels

The new candidate inequality is

\[
 k\pi_k\le (n-k)\theta^{2k-n}\pi_{n-k},
 \qquad k>n/2.
\tag{R}
\]

Status: **OPEN**.

It survived exact rational tests on small weighted graphs, incomplete-support
families, and broad numerical searches.  Numerical tests with arbitrary
directed row-stochastic kernels also survived, suggesting that (R), if true,
may be a theorem about the geometric-union mechanism rather than
undirectedness.  This directed extension is only a conjectural diagnostic.

Put

\[
 \widehat\pi(A)=\frac{\pi(A)}{\theta^{|A|}}.
\]

Then (R) is equivalent to

\[
 k\sum_{|A|=k}\widehat\pi(A)
 \le (n-k)\sum_{|A|=k}\widehat\pi(A^c).
\tag{3}
\]

The sum over the full level is indispensable: the corresponding pointwise
inequality is false.

### Exact event-Palm reformulation

Let `G_v(A,B)` be the one-target burst kernel and put

\[
 R(A,B)=\sum_{v\in A}G_v(A,B).
\]

Since every row of `R` sums to `|A|`, continuous-time stationarity gives

\[
 \sum_A\pi(A)R(A,B)=|B|\pi(B).
\tag{4}
\]

Thus the graphical-event chain (choose one occupied target uniformly and
perform its burst) has stationary law proportional to `|A| pi(A)`.  Formula
(R) is exactly reflected-level domination for this event-stationary law
after the tilt `theta^{-|A|}`.

### A sharp reference-law one-event lemma

Define the unnormalized complete-law reference measure

\[
 \lambda(A)=\theta^{|A|}(n-|A|),
 \qquad \varnothing\ne A\ne V.
\tag{5}
\]

Equivalently, augment `A` by a distinguished hole `Z notin A`; conditional
on `Z`, all other vertices are independent Bernoulli variables with
occupation probability `theta/r`, conditioned only by the later choice of
an occupied event target.

Under the event-Palm version of (5), fix the occupied target `v`.  The old
distinguished hole is uniform over the other `n-1` vertices, while the
remaining `n-2` sites are independent with hole probability `1/r`.
Consequently every `u != v` is a hole before the burst with probability

\[
 c_{n,r}=\frac{1+(n-2)/r}{n-1}
 =\frac{n+r-2}{r(n-1)}.
\]

The expected number of outside vertices added by the burst is therefore

\[
 c_{n,r}\sum_{u\ne v}h_r(P_{vu}).
\]

Concavity of `h_r`, the zero diagonal, and the row sum one give

\[
 \sum_{u\ne v}h_r(P_{vu})
 \le(n-1)h_r\left(\frac1{n-1}\right)
 =\frac{r(n-1)}{n+r-2}.
\]

Hence the expected number added is at most one.  The expected cardinality
after one reference-Palm event is no larger than before it, with equality
for the uniform complete row.  This lemma is **PROVED**, and is sharp.

The missing step is important: a one-event extremum under the reference law
does not by itself compare the unknown stationary law with the reference
law.  No semigroup domination, entropy principle, or tree injection closing
that step has been proved.

## 4. Falsified strengthenings

The following statements are false and must not be used:

- pointwise complement reflection;
- pairwise positive association;
- pairwise negative association (an exact `r=2`, four-vertex integer-weight
  counterexample is independently verified here);
- log-concavity of `pi_k/binom(n-1,k)` at `r=2`;
- first-order stochastic domination of all level tails by the complete
  graph at `r=2`;
- derivation of (S) from singleton equations plus one or two unweighted
  factorial size balances.

The mean comparison with the complete graph, the reflected-level inequality
(R), and every cubic Poisson-certificate claim remain **OPEN**.

## 5. Executable files

- `verify_hierarchy_obstruction.py`: exact `K_7` and `K_9` pseudo-law
  hierarchy obstructions;
- `verify_covariance_counterexample.py`: exact positive covariance at
  `r=2`;
- `explore_level_reflection.py`: floating-point discovery screens for (R),
  log-concavity, complete-law tails, and means.  Its output is diagnostic,
  not a proof certificate.
