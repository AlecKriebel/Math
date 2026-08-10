# A common-entropy physical-time gluing lemma

## 1. Purpose

Local source-rate charts do not need different Lyapunov functions to be
patched across their seams.  It is enough that every exceptional physical
episode has negative drift for the same globally proper factorial entropy.
Generator-good motion between exceptional charts can then be appended by
Dynkin's formula.  This note records the precise random-time statement used
by the one- and two-active repairs.

It does not assert that any particular chart supplies the required local
episode.  That remains the analytic obligation of the corresponding carrier
or phase theorem.

## 2. The stopping theorem

Let \(Z\) be a nonexplosive continuous-time Markov chain on a countable
state space \(E\), with extended generator \({\cal L}\).  Let
\(\Phi:E\to[0,\infty)\) be proper.  Split

\[
 E=K\mathbin\cup G\mathbin\cup B,                       \tag{2.1}
\]

where \(K\) is finite.  Think of \(G\) as the generator-good region and
\(B\) as a finite union of physical source-rate tubes.  Assume:

1. for some \(a>0\),
   \[
    {\cal L}\Phi\le-a\qquad\hbox{on }G;                 \tag{2.2}
   \]
2. there are \(\eta\in(0,a]\) and \(\delta>0\) such that, for every
   \(z\in B\), one can choose a strong-Markov stopping time
   \(\tau_z>0\) satisfying
   \[
   \mathbb E_z\!\left[
      \Phi(Z_{\tau_z})-\Phi(z)+\eta\tau_z
   \right]\le-\delta.                                  \tag{2.3}
   \]

All expectations in (2.2)--(2.3) are understood through localization; in
particular, the stopped endpoint and duration must be integrable enough to
remove the localization. A local episode is allowed to visit \(K\) before
its displayed endpoint. In that event the first such visit is already the
desired target time, while the episode may be completed virtually for the
drift accounting.

> **Theorem 2.1 (common-entropy gluing).**  Under these hypotheses,
> \(\mathbb E_z\tau_K<\infty\) for every \(z\in E\), where
> \(\tau_K=\inf\{t:Z_t\in K\}\).  More precisely, the number of exceptional
> episodes used before \(\tau_K\) has mean at most
> \((\Phi(z)+\delta)/\delta\), and
> \[
>  \eta\,\mathbb E_z\tau_K\le \Phi(z)+\delta.            \tag{2.4}
> \]

### Proof

From \(z\in G\), run until
\[
 \sigma=\inf\{t:Z_t\in B\cup K\}.                       \tag{2.5}
\]
Localized Dynkin and (2.2) give
\[
 \mathbb E_z\{\Phi(Z_\sigma)-\Phi(z)+\eta\sigma\}\le0.  \tag{2.6}
\]
The same inequality shows \(\mathbb E_z\sigma\le\Phi(z)/a\), so
\(\sigma<\infty\) almost surely and localization can be removed under the
stated integrability hypothesis.

If \(Z_\sigma\in K\), stop.  If \(Z_\sigma\in B\), append the selected
episode \(\tau_{Z_\sigma}\).  Starting directly in \(B\), use that episode
without the good segment.  If \(K\) is visited during a local episode,
record the target hit but complete that one episode for the sole purpose of
summing its drift inequality; its full duration only upper-bounds the
actual target time.  Thus every macroepisode begun before the first target
hit contains exactly one exceptional episode.  The strong Markov property
and (2.3)--(2.6) give
\[
 \mathbb E\!\left[
    \Phi(Z_{S_{n+1}})-\Phi(Z_{S_n})
    +\eta(S_{n+1}-S_n)
    \mid{\cal F}_{S_n}
 \right]\le-\delta                                    \tag{2.7}
\]
whenever the \(n\)-th macroepisode is begun before the target hit, including
the final episode which may contain that hit.

Stop (2.7) after \(m\) macroepisodes.  Since \(\Phi\ge0\),
\[
 \delta\,\mathbb E(m\wedge N)
 +\eta\,\mathbb E S_{m\wedge N}
 \le\Phi(z)+\delta,                                    \tag{2.8}
\]
where \(N\) is the first terminal index.  Monotone convergence proves the
episode bound, (2.4), and \(N<\infty\) almost surely. \(\square\)

For a closed irreducible population class of a finite-reaction CRN, apply
the theorem to the restriction of \(Z\) to that class.  Every population
state has only finitely many outgoing reaction successors.  Finite mean
hitting of a nonempty finite set, followed by one ordinary jump and the
finite mixture of return bounds from those successors, gives a finite mean
positive return time.  Hence the class is positive recurrent.  The local
finiteness qualification is needed for this final corollary at the stated
level of abstraction.

## 3. Obtaining a finite exceptional set from sequence theorems

Tier arguments naturally prove their estimates along arbitrary divergent
sequences, after taking a subsequence with fixed support flags and limiting
within-tier ratios.  The following elementary compactness step is the
correct way to turn such results into (2.3).

> **Lemma 3.1 (bad-sequence contradiction).**  Suppose \(B\) is countable
> and \(\Phi\) is proper.  Assume that for every sequence
> \(z_n\in B\) with \(\Phi(z_n)\to\infty\), some subsequence admits physical
> stopping rules for which
> \[
>  \mathbb E_{z_n}\!\left[
>    \Phi(Z_{\tau_n})-\Phi(z_n)+\eta\tau_n
>  \right]\le-\delta                                  \tag{3.1}
> \]
> eventually.  Then all but finitely many states of \(B\) admit a rule
> satisfying (3.1).

Indeed, otherwise choose one distinct counterstate outside each finite
\(\Phi\)-sublevel.  Properness makes this a divergent bad sequence, and its
promised subsequence contradicts the definition of the counterstates.
Because \(E\) is countable, choose one valid stopping rule for each
remaining state.  No uniform finite phase box or occupation
diagonalization is involved.

## 4. What is required to convert a workload episode

Let
\[
 \Phi(x)=\sum_i\{x_i(\log x_i-1)+1\}.                   \tag{4.1}
\]
An exact D-tier specifies monomial order and finite-positive ratios inside
each displayed tier.  Its representative integer weight does **not** in
general imply
\(\log x=\lambda w+O(1)\).  Subpower separation between different tiers is
allowed.  Consequently
\[
 \mathbb E\{w\cdot X_\tau-w\cdot x\}<0                 \tag{4.2}
\]
alone does not imply negative factorial-entropy drift.

The local theorem must instead prove one of the following stronger facts.

1. Directly,
   \[
   \mathbb E\{\Phi(X_\tau)-\Phi(x)\}
      +\eta\mathbb E\tau\le-\delta;                    \tag{4.3}
   \]
2. the endpoint displacement is bounded, its successful part contains an
   edge \(y\to z\) from a maximal monomial tier to a strictly lower one,
   and every positive exceptional edge satisfies the usual
   \(g e^{-g}\) propensity-times-log bound; or
3. a fixed, pair-dependent linear correction
   \(\Phi+\ell\cdot x\) controls the fast phase and the correction has the
   same value at every gluing endpoint.

In alternative 2, factorial expansion on the successful edge gives
\[
 \Phi(x+z-y)-\Phi(x)
   =\log(x\vee1)\cdot(z-y)+O(1)\longrightarrow-\infty,  \tag{4.4}
\]
while the integrated-hazard uniform-integrability estimate makes the
positive exceptional contribution \(o(1)\).  Endpoint second moments and a
tail bound are needed if the total endpoint jump is not pathwise bounded.

Thus descriptor-local workload descent is useful for identifying the
service edge, but it is not the common-potential hypothesis of Theorem 2.1.
The physical carrier theorem must retain the logarithmic endpoint reward
before it can be globally glued.

## 5. Neutral phases and augmented debts

Some one-active phases have no service cycle.  If their active reward is a
bounded coboundary, augment the physical chain by deterministic scalar
debts
\[
 D_i'=(D_i+\Delta X_i)^+,\qquad H_i=X_i-D_i.             \tag{5.1}
\]
Then \(0\le D_i\le X_i\) and \(H_i\) is pathwise nonincreasing.  Start from
a class reference state with every \(D_i=0\).  At a neutral base return
with \(D_i=0\),
\[
 X_i=H_i\le X_i(0).                                     \tag{5.2}
\]
If the inactive coordinates are in a bounded phase set, these neutral
returns belong to a genuinely finite classwise target.

This device is only a target construction.  It does not replace (2.3) for
a phase in which persistent debt can be created.  In that case a physical
service block must supply strict entropy drift.

## 6. What the lemma excludes

The proof uses one global potential at every endpoint.  It therefore has
none of the unbounded switch tolls that invalidate a patch of unrelated
local Lyapunov functions.  It also measures physical duration, not the
number of fast embedded jumps.  The load-bearing inputs remain:

1. a complete local episode for every bad tube, with all physical reactions
   retained;
2. endpoint uniform integrability sufficient for (3.1) and (4.4); and
3. a genuinely finite target in each closed irreducible class.

Absent any one of these, Theorem 2.1 does not certify recurrence.
