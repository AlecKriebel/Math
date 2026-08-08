# Gate-1 replay: the open fitness-two and fitness-three-halves lemmas

Date: 2026-08-07 22:17 PDT
Audited tracked base: `ffe5c89cf41ca3cced5a2e573404baeb2d510897`
(`main`, equal to `origin/main` at the start of this replay).

## Scope and classification

This was a bounded restart audit, not a new search program.  It replayed the
exact fitness-two collision and entropy reductions, the exact
fitness-three-halves triangle/drift product certificate, a representative
exact local product calculation, and two representative numerical product
screens.  It also inspected and replayed the untracked
`obstruction/product_chain_certificate/` branch.

The conclusion is unambiguous:

* **PROVED:** the saved reductions and their displayed exact
  counterexamples replay.
* **EXACTLY COMPUTED:** the weighted-triangle product certificate, the
  finite-order local Hessians replayed below, and the route-obstruction
  examples replay.
* **NUMERICALLY OBSERVED:** the two finite product screens found no
  violation.
* **OPEN:** the universal product inequality at `r=3/2`, the weaker universal
  no-simultaneous separator at `r=3/2`, and the universal dB maximizer
  inequality at `r=2`.
* **No unintegrated endpoint theorem or endpoint counterexample exists.**
  There are, however, two untracked packages of exact reduction/route-closure
  results that should be integrated after hostile review.

## Repository provenance

The tracked fitness-two collision package was introduced at

```text
c5bf7bda98282146836d57c203fd3c842cd298a8
Reduce dB fitness two to collision inequality
```

and is unchanged in the audited HEAD.  The tracked
fitness-three-halves product package was last touched at

```text
daf403ae6f4f28249c10d4a937c40e52c0ac8852
Audit stationary odds and product checkpoints
```

The following packages were untracked relative to the audited HEAD:

```text
obstruction/r2_entropy_certificate/
obstruction/product_chain_certificate/
```

Checksums of their central note/verifier pairs at replay time were:

```text
9358ec5a2e236619b76af0a64c2dbf53bb1352ba29f0e4c6e837eb32b09babe0  ENTROPY_REFLECTION_REDUCTION.md
576d0a285de020f9ebdc5891a84e0bb3e6b7c3fc674e15c7237b3484a891fa7d  verify_entropy_reflection.py
28a926efd30c88cbf91fa438aca2b749e0f3ec428b9ad2d4f0a87b19aaadda32  PRODUCT_CHAIN_ROUTE_CLOSURES.md
ee61564d6a112220bbbb4aa4f0665e6c966f73b74f253361f5ea194577af65e8  verify_product_chain_barriers.py
```

All commands below used
`/Users/alec/Documents/Math-universal-amplification/.venv/bin/python`
(Python 3.14.6, SymPy 1.14.0, NumPy 2.5.1, NetworkX 3.6.1).

## Replay ledger

### 1. Exact fitness-two Green--collision reduction

Working directory:
`obstruction/r2_collision_bound/`

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_green_collision_reduction.py
```

Exit status `0`.  Output:

```text
PASS n=3: rho=2/5, gap=-2/45, L=2/135, V=8/135
PASS n=4: rho=35/82, gap=-1/574, L=207/22960, V=247/22960
PASS: pair bound is false on P4 and on a positive regular K4; the summed component-odds target is not refuted
PASS: all exact Green, collision, and counterexample checks
```

The verifier independently builds the forward heat-bath chain and exact
geometric-union dual, solves both rational systems, checks Boolean coverage,
the level-flux recurrence, the complete Green comparison, and the displayed
counterexamples.

### 2. Exact fitness-two entropy reflection

Working directory:
`obstruction/r2_entropy_certificate/`

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_entropy_reflection.py
```

Exit status `0`.  Output:

```text
PASS: exact stationary posterior and entropy-reflection identities
PASS: complete-graph cross-level cancellation for 3 <= n <= 12
PASS: exact negative statewise K4 reflection integrand
PASS: exact regular weighted-K4 active entropy contraction
PASS: full weighted-K4 entropy-reflection gap remains positive
OPEN: universal entropy-reflection inequality M >= I(V;B)
```

The two subsidiary exact route-boundary verifiers also passed:

```text
cd chi_square_channel
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_resolvent_identities.py
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_shannon_routes.py
```

Their exact outputs include

```text
path L2 expansion = 2/3
path I2 = 17/9 < 2
(7,1,1)-triangle revealed-flag excess = 168/20165
400 exact normalized-reverse/path checks
path Blackwell obstruction TV expansion = 1/18
triangle convex-order stop-loss gap = -8/327
membership-channel second moment = 2
```

and leave both `I2<=2` and `M-I(V;B)>=0` open.

### 3. Exact additive-odds route obstruction

Working directory:
`obstruction/r2_collision_bound/aggregate_odds/`

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_linear_potential_farkas.py
```

Exit status `0`.  It reconstructs the 31-state rational dual and certifies
the positive-support five-vertex Farkas obstruction.  The short certified
quantities replay as

```text
degrees = [10, 207, 204, 8, 9]
H^T y-y = [73127/1841125, 1/7070, 49/162800,
           16829/666250, 291331/10865000]
y^T r lower bound = 9977/2000000 > 0
```

Every component-odds slack on that graph remains positive.  Thus this kills
only the nonnegative additive/singleton certificate, not the odds
inequality.

### 4. Exact `r=3/2` triangle product and drift bridge

Working directory:
`obstruction/cross_sum_three_halves/`

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_product_and_drift.py
```

Exit status `0`.  Output:

```text
PASS: exact Bd and dB triangle absorbing chains constructed
PASS: product numerator equals 24-atom nonnegative certificate
PASS: positive triangle equality occurs only at equal weights
PASS: complete dB harmonic recurrence checked for 2 <= n <= 20
PASS: arbitrary-graph drift decomposition checked on 50 states
```

Thus the product inequality is replayed as an exact theorem for every
positive weighted triangle only.  The general drift identity is also exact,
but its row-cut remainder has no universal pointwise sign.

### 5. Exact local log-product calculation

In the same working directory:

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python exact_log_product_hessian.py
```

Exit status `0`.  The exact log-product Hessian was negative on both
irreducible edge modes for `n=4,5,6`; the cycle-mode Bd second variation was
exactly zero.  The printed log-product second variations were

```text
n=4: degree -15788308/94533075, cycle -12/703
n=5: degree -1562589371275/8674813909008, cycle -24064/2086695
n=6: degree -300027077249040432/1676853191732140625,
     cycle -10171336/1239786837
```

The recorded `n=7` calculation was deliberately not rerun in this critical
replay.  This is a finite-order local result, not global concavity.

### 6. Exact untracked product-chain route closures

Working directory:
`obstruction/product_chain_certificate/`

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python verify_product_chain_barriers.py
```

Exit status `0`.  Output:

```text
PASS: exact five-atom radial/overlap Poisson Farkas obstruction
PASS: exact order-four rank-convolution domination counterexample
PASS: exact order-four all-z coverage-product counterexample
PASS: every underlying fixation product remains below complete
```

This is a completed exact **route-closure theorem**, but not an endpoint
product theorem or counterexample.  In particular:

* on the unweighted three-path a positive five-atom pseudo-law annihilates
  the product generator on every function of
  `(|A|,|B|,|A intersection B|)` but has target expectation
  `571/852>0`; the actual normalized-arithmetic slack is nevertheless
  `19/504>0` in the conjectured direction;
* stationary rank-sum stochastic domination is exactly false on one
  weighted order-four graph, while its endpoint mean sign is correct;
* all-`z` Bernoulli-coverage product domination is exactly false on another
  weighted order-four graph, while its `z -> 1` fixation-product endpoint is
  correct.

Therefore any surviving product-chain Poisson certificate must retain
graph-sensitive within-rank information, and any coverage-transform proof
must be local near the fixation endpoint rather than valid for all `z`.

### 7. Representative numerical product screens

The untracked sparse product search was replayed with the exact saved
command

```text
/Users/alec/Documents/Math-universal-amplification/.venv/bin/python search_sparse_product.py --n 6 --evaluations 100 --seed 1 --span 8 --edge-probability 0.55
```

It reported

```text
NO VIOLATION; best -0.011476020103095078
```

An independent inline atlas driver using the saved
`db_maximizer/search_db.py` fixation builders evaluated all 112 connected
unweighted order-six graphs.  It found zero simultaneous endpoint
amplifiers.  The maximum product excess was
`4.163336342344337e-17`, attained by `K_6` and therefore consistent with
floating-point zero; the minimum was `-0.0212295140688233`.

Both items in this subsection are **NUMERICAL DIAGNOSTICS ONLY**.

## Exact minimal open inequalities at fitness two

Let `P_vu=w_vu/d_v`, `N=n-1`, and let `Pi` be the stationary law of the
exact dB geometric-union dual at fitness two.  For `A~Pi`, put `H=A^c`,

```text
C_partial(A) = sum_(v in A,u in H) P_vu.
```

Define `mu_0=mu_n=0` and, for `1<=k<=n-1`,

\[
 \mu_k={ (n+k)/(2n)-2^{k-n}\over
 n\binom{n-2}{k-1}(1-2^{1-n})},\qquad c_k=\mu_k+\mu_{k+1},
\]

and

\[
 U_s=\sum_{k=1}^s c_k{2N^2\over(N+k)^2}\binom{s-1}{k-1}.
\]

The exact comparison is

\[
 \rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_n,2)
 =\mathcal L(G)-\mathcal V(G),
\]

where

\[
 \mathcal L(G)=E_\Pi\!\left[
 U_{|H|}\left(C_\partial(A)-{|A||H|\over N}\right)\right]
\]

and

\[
 \mathcal V(G)=E_\Pi\sum_{v\in A}\sum_{k=1}^{|H|}
 c_k{2\over(1+k/N)^2}
 \sum_{\substack{S\subseteq H\\|S|=k}}
 {(P_{vS}-k/N)^2\over1+P_{vS}}.
\]

Every atom of `V` is nonnegative.  The **single exact sign needed for the
finite complete-graph maximizer theorem** is

\[
 \boxed{\mathcal L(G)\le\mathcal V(G).}
\]

It is equivalent to
`rho_dB(G,2)<=rho_dB(K_n,2)`, not merely sufficient.  Proving it for all
finite connected undirected weighted graphs would give the desired
universal upper bound `R_sim<=2`.

There is a strictly weaker surviving collision target.  With

\[
 Z(A)=C_\partial(A)-{|A||H|\over N},\qquad
 S_1(A)=\sum_{v\in A,u\in H}{(P_{vu}-1/N)^2\over1+P_{vu}},
\]

stationarity gives the identity

\[
 E_\Pi(Z-S_1)={n\over N^2}
 \left(E_\Pi|A|^2-{n\over2}E_\Pi|A|\right).
\]

Thus

\[
 \boxed{E_\Pi Z\le E_\Pi S_1}
\]

is equivalent to the stationary second-moment inequality
`E|A|^2 <= (n/2)E|A|`, equivalently to the recorded second-collision
condition

\[
 E B_2\ge(n/2-1)E|A|.
\]

It implies the half-density ceiling `E|A|/n<=1/2`, but it does **not** by
itself give the finite complete-baseline inequality: the complete dB
baseline is below `1/2` at every finite `n`.

The component-odds inequality

\[
 \boxed{{p_i\over1-p_i}\le2\sum_vP_{vi}p_v\quad\hbox{for every }i}
\]

and its summed version also remain open and would imply half density.  They
are not established as equivalent to `L<=V`.

## Exact minimal open entropy inequalities at fitness two

In the stationary target experiment, choose the update target `V` uniformly,
let `B` be the stationary output, write `k=|B|`, `h=n-k`, and let
`tau_B` be the posterior law of `V` on the holes.  The exact reflection gap
is

\[
 M-I(V;B)=E_\Pi\left[
 {k\over n}\log{h\over k}
 -D\!\left(\tau_B\middle\|\operatorname{Unif}(B^c)\right)
 \right],
\]

where `M=E h_2(k/n)=H(C|B)`.  The sole Shannon sign is

\[
 \boxed{M\ge I(V;B).}
\]

If true, it implies half density by
`I(V;B)>=-log(1-Ek/n)` and `M<=h_2(Ek/n)`.  The saved work does **not** prove
that this entropy inequality is equivalent to the Green--collision sign
`L<=V`; it is currently only a sufficient route to the weaker half-density
ceiling.

The order-two analogue

\[
 \boxed{I_2(V;B)=1+{E k\over n}
 +{1\over n}E\sum_{v\notin B}e_v(B)^2\le2}
\]

is likewise open and likewise only a half-density route in the present
package.

## Exact minimal open inequalities at fitness three halves

The preferred endpoint target remains

\[
 \boxed{
 \rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
 \le
 \rho_{\rm Bd}(K_n,3/2)\rho_{\rm dB}(K_n,3/2).}
\]

This is sufficient, but stronger than necessary.  The actual threshold
separator needed is only

\[
 \boxed{\min\left\{
 {\rho_{\rm Bd}(G,3/2)\over\rho_{\rm Bd}(K_n,3/2)},
 {\rho_{\rm dB}(G,3/2)\over\rho_{\rm dB}(K_n,3/2)}
 \right\}\le1.}
\]

Neither statement is proved or refuted for arbitrary graphs.

For the exact drift bridge, if `S` has size `k`,
`x_i=sum_(j in S)P_ij`, `T_S=sum_i x_i`,
`B(S)=sum_(i notin S)x_i`, and
`B_0(k)=k(n-k)/(n-1)`, the surviving identity is

\[
 \mathcal D(S)+C_M\{A(S)-B(S)\}
 =-(C_M-C_R)\{B(S)-B_0(k)\}-\mathcal E(S),
\]

with `C_M-C_R>0` and `E(S)>=0`.  The minimal obstruction to a pointwise
closure is the signed row-cut deviation `B(S)-B_0(k)`: it can be negative.
Any global proof must cancel or control it after path/stationary averaging.

The independent product-dual arithmetic strengthening

\[
 {m_{\rm Bd}\over m_{\rm Bd}^K}
 +{m_{\rm dB}\over m_{\rm dB}^K}\le2
\]

also remains open.  It would imply the product inequality by AM--GM, but the
five-atom certificate proves that no pointwise product-Poisson potential
depending only on the two ranks and their overlap can establish it.

## Falsified-route boundaries that must be preserved

The following exact failures were replayed or are directly included in a
replayed verifier.  None is a counterexample to the surviving universal
endpoint claims.

### Fitness two

* `R_k<=0` level by level is false: a regular weighted `K_4` has
  `R_2=1/205>0`.
* `L<=0` is false: the weighted three-path `(1,2)` has `L=2/135>0`.
* Statewise complete-Poisson forcing domination is false: the same path has
  residual `-16/4455` at `{0,1}`.
* The pairwise crossing estimate behind component odds is false on the
  unweighted `P_4` and on positive-support regular weighted `K_4`.  The
  **summed component odds is not refuted**.
* The nonnegative additive/singleton odds certificate is infeasible on an
  exact positive-support weighted `K_5`.  The odds inequalities themselves
  are strictly satisfied there.
* Entropy reflection is not pointwise in rank; even complete `K_4` has a
  negative upper-rank integrand.
* Separate active-channel entropy expansion, fixed-reference `L^2`
  contraction, revealing the effective/null flag, Blackwell garbling, and
  full likelihood-ratio convex order all have exact counterexamples.  The
  aggregate Shannon and order-two information signs remain open.

### Fitness three halves

* A common pointwise Bd/dB harmonic correction and its baseline-weighted
  tangent variant are infeasible already on weighted paths.
* Radial monotonicity toward `K_n` and the natural balancing step are not
  globally monotone.  This does not refute the endpoint product.
* A pointwise product-chain Poisson potential using only ranks and overlap is
  impossible on the unweighted three-path.
* Rank-convolution stochastic domination and all-`z` coverage-product
  domination are exactly false.  Their fixation endpoints retain the
  conjectured sign on the counterexample graphs.

## Unintegrated result assessment

1. `r2_entropy_certificate/` contains a completed exact reduction and exact
   counterexamples to several proof architectures.  It does **not** contain
   a proof or counterexample for `M>=I`, `I2<=2`, `L<=V`, or the finite dB
   complete-maximizer theorem.
2. `product_chain_certificate/` contains a completed exact theorem excluding
   three coarse product-chain/transform architectures.  Its independent
   exact verifier passes.  It does **not** contain a product violation, an
   endpoint simultaneous amplifier, a universal product proof, or a weaker
   universal endpoint separator.
3. These two packages merit integration as exact route closures after a
   second hostile derivation, but neither changes the current bracket for
   `R_sim`.

## Remaining audit boundaries and next executable tasks

Not replayed in this bounded pass: the historical million-instance product
searches, the separately recorded exact `n=7` Hessian, or the random directed
entropy screens.  Those items are evidence/local checks and are not required
to state the open universal signs.

The next three executable mathematical tasks, without reopening falsified
routes, are:

1. formulate a graph-sensitive product-chain Poisson/variational dual that
   retains vertex identities within each rank, and exact-screen its dual
   feasibility on the recorded three-path Farkas instance before attempting
   an all-graph proof;
2. attack the weaker `r=3/2` disjunctive separator directly, allowing a
   nonlinear or graph-dependent functional rather than assuming the product
   conjecture;
3. in parallel, prove or refute the exact full fitness-two sign `L<=V` using
   stationary likelihood stability; do not mistake either entropy reflection
   or half density for the finite complete-baseline theorem.
