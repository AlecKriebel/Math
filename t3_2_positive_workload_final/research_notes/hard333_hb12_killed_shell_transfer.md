# A killed-shell common-factorial transfer target for the hard H_b twelve

## 1. Status and exact scope

This note isolates the smallest stopped theorem that could remove the
potential switch on the exact twelve H_b pairs in the hard 333 family.  It
uses the same rate-adjusted factorial potential on the all-active curvature
seam and on the repaired hard boundary.  It does **not** use an additive
power of the linear workload, a global shell Poisson corrector, or a
shell-wide entropy mark.

The theorem below is a claim-neutral audit target.  Its finite support
certificate and five focused tests pass, but none of its analytic or
recurrence flags is true.  The exact pair fingerprint is

```text
7fcbd17c5571534a7e1bd50d218cfc56389c73a136c2fe0a73d3478ac2cf14fb
```

There are sixteen curvature incidences.  Their curvature-excess histogram
is twelve of excess one and four of excess two.  The repaired hard rows have
resistance histogram ten of resistance one and two of resistance two.

## 2. The exact reversible shell

Every selected pair has the same top support

\[
                         T=\{2A,B+C\}.                 \tag{2.1}
\]

The top orientation is necessarily reversible.  Write its rates as
\(\kappa_+\) for \(2A\to B+C\) and \(\kappa_-\) for the reverse edge.  Choose
\(\ell\in\mathbb R^3\) so that

\[
 \exp\{-\ell\mathbin\cdot((0,1,1)-(2,0,0))\}
 ={\kappa_+\over\kappa_-},                             \tag{2.2}
\]

and put

\[
 F_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\mathbin\cdot x,
 \qquad W_\ell=F_\ell^4.                              \tag{2.3}
\]

On each finite top shell, parameterized by one integer coordinate \(k\),
the birth and death rates are

\[
 \lambda_k=\kappa_+A_k(A_k-1),\qquad
 \mu_k=\kappa_-B_kC_k.                                \tag{2.4}
\]

Detailed balance gives the exact identity

\[
                 \pi_q(x)=Z_q^{-1}e^{-F_\ell(x)}.      \tag{2.5}
\]

The shell invariants are total population and any applicable

\[
 H_b=2A+bB+(4-b)C,\qquad 0<b<4.                       \tag{2.6}
\]

Thus a top excursion never changes the hard workload or total population.
More importantly, its factorial cost is exactly a one-dimensional
log-concave birth--death potential, not an uncontrolled redistribution.

## 3. Three shortcuts that are not available

Three tempting compositions are false and are excluded from the target.

First, normalizing a shell Poisson solution by zero stationary mean can
reverse the lower averaged sign.  The exact unit-rate example at \(N=4\)
has

\[
 \bar g=-455.777293518\ldots,qquad
 \mathcal L_R\chi=472.748697241\ldots,                 \tag{3.1}
\]

so the corrected drift is \(16.971403723\ldots>0\).

Second, many top jumps before the first lower reaction do not imply shell
mixing.  On the passing state \((N^6,N^{10},N^{11})\), the top-to-lower
rate ratio diverges but the first-lower-reaction endpoint satisfies

\[
 \mathbb E\{F_\ell(X_{\tau_R})-F_\ell(x)\}
 =\log N+O(1)>0.                                      \tag{3.2}
\]

Third, fixed-shell factorial redistribution can cost \(O(n)\), whereas one
hard service endpoint supplies only \(-\Theta(\log n)\) in \(F_\ell\).
A single hard episode therefore cannot repay an arbitrary shell-wide mark.

The proposed episode is local to the kinetic center.  Equation (3.2) is
kept on the ordinary pointwise-entropy branch, and no shell-wide mark is
ever created.

## 4. The central-core split

Let \(x_q^\star\) be a mode of (2.5), and define the shell entropy
displacement

\[
                  D_q(x)=F_\ell(x)-F_\ell(x_q^\star). \tag{4.1}
\]

The exact ratios in (2.4) are monotone through the mode.  If \(s_q^2\) is
the local shell variance, then throughout a fixed multiple of the central
width,

\[
 D_q(x)\asymp {|k-k_q|^2\over s_q^2},
 \qquad
 {\rm gap}(Q_q)\asymp {\lambda_{k_q}+\mu_{k_q}\over s_q^2}.           \tag{4.2}
\]

For the sixteen curvature descriptors, every center coordinate diverges.
The recorded curvature excess says that the relaxation scale in (4.2)
beats the lower-linkage firing scale by a positive polynomial power.

Choose the core constant \(K_0\).  Let \(c_0>0\) be the exponential
shell-tail constant and let \(C_*\) bound the polynomial exponent in the
number of relaxation blocks before killing.  For any requested endpoint
power \(K>0\), put

\[
                     L_K={K+C_*+1\over c_0}.           \tag{4.3}
\]

The bad core and its \(K\)-guard are

\[
 {\cal C}_q=\{D_q\le K_0\},\qquad
 {\cal G}_{q,K}=\{D_q\le L_K\log s\},                 \tag{4.4}
\]

where \(s\) is any fixed proper scale comparable with the largest center
coordinate.

### 4.1 Outside the core

The exact top entropy drift is the negative flux-imbalance term plus its
discrete curvature remainder.  Once \(K_0\) is sufficiently large, the
flux-imbalance term absorbs that remainder outside \({\cal C}_q\).  The
lower linkage already has strict factorial descent on every passing tier.
The required sequential statement is therefore

\[
 \mathcal L W_\ell(x_n)\longrightarrow-\infty         \tag{4.5}
\]

for every divergent all-active sequence outside the finite union of the
cores.  This branch retains the directed transport that was incorrectly
discarded in the counterexample (3.2).

### 4.2 Inside the core

Start only from \({\cal C}_q\), retain every top and lower clock, and stop at

\[
 \tau=\tau_R\wedge\tau_{\partial{\cal G}_{q,K}},       \tag{4.6}
\]

the first lower-linkage reaction or the first guard exit.  Before \(\tau_R\)
the state stays on one reversible top shell.

The load-bearing birth--death estimate needed here is

\[
 \sup_{x\in{\cal C}_q}
 \mathbb E_x\!\left[
  \{F_\ell(X_{\tau-})-F_\ell(x)\}_+^p;
  \tau_R<\tau_{\partial{\cal G}_{q,K}}
 \right]\le C_p                                      \tag{4.7}
\]

for one integer \(p>8\), together with

\[
 \sup_{x\in{\cal C}_q}
 \mathbb P_x\{\tau_{\partial{\cal G}_{q,K}}<\tau_R\}
 \le C_Ks^{-K}.                                      \tag{4.8}
\]

The intended proof does not assert instantaneous stationarity.  Apply the
generator to even powers of \(k-k_q\).  Monotonicity of \(\lambda_k-\mu_k\)
gives a mean-reverting term of order
\({\rm gap}(Q_q)|k-k_q|^{2j}\), while the jump remainder is one lower even
power.  The exponential standardized-displacement version has a uniform
deterministic-time bound.

Inside the guard, every coordinate differs from its center by at most
\(O(\sqrt{r_q\log s})\), where \(r_q\) is the smallest center coordinate.
Since \(r_q\to\infty\), every positive lower source propensity, and hence
the total lower rate, changes by a factor \(1+o(1)\).  Comparison with an
independent exponential clock therefore transfers the deterministic-time
moment bound to the killed resolvent and gives (4.7).  The number of
relaxation blocks before killing is only polynomial in \(s\), by the
recorded positive curvature excess.  The choice of \(L_K\) in (4.3)
absorbs that polynomial factor and turns the exponential shell tail into
the requested guard-exit estimate (4.8).

At a state before the lower reaction, let \(q_R(x)\) be the total lower
propensity.  Conditional on the lower clock firing there, its exact mean
factorial jump is

\[
 \mathbb E\{\Delta_R F_\ell\mid x,\ R\text{ fires}\}
 ={\mathcal L_RF_\ell(x)\over q_R(x)}.                \tag{4.9}
\]

The forced maximal-tier exit used in the all-active factorial theorem is
uniform throughout the guard.  Hence

\[
 \sup_{x\in{\cal G}_{q,K}}
 {\mathcal L_RF_\ell(x)\over q_R(x)}
 \le-g(s),\qquad g(s)\longrightarrow\infty.          \tag{4.10}
\]

Equations (4.7)--(4.10) would give

\[
 \mathbb E_x\{F_\ell(X_\tau)-F_\ell(x)\}
 \le-cg(s)                                            \tag{4.11}
\]

uniformly in the core.  The rare guard endpoint has only \(O(\log s)\)
entropy toll, already multiplied by the arbitrarily small probability in
(4.8).  It is stopped there; it is not charged to one hard service word.

## 5. Common-W endpoint and lower-dimensional routing

Because \(F_\ell(x)\to\infty\), Taylor expansion of the fourth power and
the \(p>8\) endpoint estimate give the target inequality

\[
 \mathbb E_x\!\left[
  W_\ell(X_\tau)-W_\ell(x)+\tau
 \right]
 \le-cF_\ell(x)^3g(s).                                \tag{5.1}
\]

All error terms have at most three powers of the stopped factorial jump;
the guard event is controlled at a still higher polynomial order.  Thus no
positive \(H_b^q\) term and no potential-switching cost appears.

The central theorem explicitly assumes that all three kinetic-center
coordinates diverge.  A core trajectory hits its logarithmic guard while
that remains true, so the central proof makes no all-active-to-hard
handoff.

Lower-dimensional starting sequences use the already exhaustive
common-\(W_\ell\) menu.  On the twelve pairs its exact incidence split is

\[
\begin{array}{c|c|c}
\text{dimension}&\text{route}&\text{incidences}\\ \hline
\text{two-active}&\text{closed rank-one top}&36\\
                 &\text{dormant top}&12\\ \hline
\text{one-active}&\text{generalized Family II}&36\\
                 &\text{direct physical }C&2.
\end{array}                                           \tag{5.2}
\]

Thus there are 48 two-active and 38 one-active starts.  The single dormant
hard episode is only one part of this menu and is not asserted to cover
every degenerating shell.

## 6. Audit gate

Before any flag changes, an independent replay must prove all of the
following uniformly over the sixteen descriptors and arbitrary fixed
positive rates:

1. the pointwise entropy complement (4.4), with a core large enough to
   absorb every discrete curvature remainder;
2. the stopped even-moment induction (4.7) for an integer \(p>8\);
3. the guard-exit estimate (4.8), including state-dependent lower killing;
4. the uniform terminal reward (4.10), including every lower reaction;
5. the fourth-power event-weighted expansion (5.1); and
6. the exact 48-row two-active and 38-row one-active routing menu (5.2).

Failure of any item leaves all twelve pairs unresolved.  In particular,
the present finite checks do not certify recurrence.

## 7. Reproduction

```text
PYTHONPATH=src python3 -B src/hard333_hb12_killed_shell_transfer.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hb12_killed_shell_transfer.py -v
```

The frozen row hash is

```text
6a5240865b78898be273738bb2e227ede2bcc3db46936864af995010bd53e572
```

and the frozen payload hash is

```text
e9d113351e2d67db0d93595b5adb351814834459f77b23d840c55f4eef9042f7
```
