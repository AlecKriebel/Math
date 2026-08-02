# Research log: geometric batching versus the reversed-arrow dual

## 2026-08-02 08:42 PDT

- Began an independent attack on the proposed `r=3/2` split

  \[
  \frac{\mathbb E_D|A|}{\mathbb E_C|A|}
  \leq
  \frac{m_D(K_n)}{m_C(K_n)}.
  \]

- Reconstructed both generators directly.  In the forward picture, `C` is
  the biased link process, while dB multiplies every flip at target `v` by
  `1/(1+x_v/2)`, where `x_v` is the row-`P` mutant-neighbour mass.
- The exact complete-graph constant is

  \[
  R_n=\frac{n-1}{n}\,
      \frac{1-(2/3)^n}{1-(2/3)^{n-1}}.
  \]

- Existing exact rational screens on positive weighted graphs of orders three
  and four, together with the hand-selected order-five case, show no
  violation.  Targeted floating-point optimization through order five also
  returns the complete graph as the apparent maximizer.  This is discovery
  evidence only.

## 2026-08-02 09:18 PDT

- [EXACTLY FALSIFIED ROUTE] The most direct committor comparison is false
  statewise, despite the exact monotone-submodular coverage representation of
  the `C` committor.  For

  ```text
  [[0, 7, 3, 17],
   [7, 0, 15, 6],
   [3, 15, 0, 5],
   [17, 6, 5, 0]]
  ```

  and mutant mask `0b0110`, the exact dB drift of the `C` fixation committor
  is the strictly positive rational

  \[
  \frac{19320943980314880741118267311163716984393}
       {1350751487384526329949760252671364412445376}.
  \]

  Thus `D F_C<=0` cannot prove even the unquantified comparison.  The script
  `verify_committor_sign_counterexample.py` independently solves the
  `C`-harmonic equations and reconstructs the same function from the exact
  stationary-dual coverage law before checking the positive drift.

- [EXACT STRUCTURAL REFORMULATION] Observing both set chains only at global
  neutral events gives the same geometric number of intervening selective
  arrows.  In `C`, every selective arrow resamples an occupied target; in
  `D`, all selective arrows and the final neutral arrow are locked to one
  target.  The desired theorem is therefore a sharp comparison between
  resampled-target and locked-target geometric episodes.  This reformulation
  is exact, but the required invariant-measure inequality remains open.

## 2026-08-02 09:46 PDT

- [PROVED] Introduced the symmetric edge-slowing interpolation

  \[
  q_s^+(e)=\frac{(3/2)x_e}{1+sx_e/2},\qquad
  q_s^-(e)=\frac{1-x_e}{1+sx_e/2}.
  \]

  It is itself additive for every `s`: use a replacement geometric-OR burst
  of mean `r_s=1+s/2` at rate one and a retention/add burst with the same law
  at rate `(3/2-r_s)/r_s`.  Thus the entire interpolation has an exact set
  dual and stationary-density representation.

- [PROVED] On `K_n`, the fixation curve telescopes to

  \[
  \rho_s(K_n)=\left[1+A_n+sB_n\right]^{-1},
  \]

  where `A_n=sum_(l=1)^(n-1)(2/3)^l` and
  `B_n=[2(n-1)]^-1 sum_l l(2/3)^l`.  Therefore the endpoint ratio conjecture
  follows from the open normalized derivative bound

  \[
  \partial_s\log\rho_s(G)
  \le -B_n/(1+A_n+sB_n).
  \]

- [PROVED] Derived the exact occupation-current formula

  \[
  -\partial_s\log\rho_s
  =\rho_s^{-1}\sum_e
   \frac{x_e/2}{1+sx_e/2}J_e\Delta h_e.
  \]

  The net current through every rank cut `k -> k+1`, `k>=1`, is exactly
  `rho_s`.  However individual currents need not be positive.  On the exact
  triangle with weights `(1,1,100)` at `s=0`, the edge `001 -> 011` has
  current `-4317/186944`.  Any proof must control weighted circulations rather
  than only aggregate rank flux.

- [NUMERICALLY OBSERVED / OPEN] Direct differentiation of the finite linear
  system, random screens through order seven, all unweighted connected graphs
  through order seven at the endpoints, and differential-evolution searches
  through order five found no violation of the normalized derivative or
  endpoint ratio.  Complete weights were returned as the optimizer in the
  direct searches.  These computations are falsification evidence only.

- Wrote `BATCHING_RATIO.md` and exact verifier
  `verify_interpolation_certificates.py`.  Both exact verifiers pass.

## 2026-08-02 09:52 PDT

- [PROVED] Converted the zero-batching derivative to a positive-semidefinite
  overlap problem.  If `psi` is the stationary Poisson potential of the
  additive `C` dual and `kappa_psi` its submodular curvature, define `C3` from
  two iid row samples and `C2` from the neutral-swap target/sample pair.  Then

  \[
  m'_0=(r-1)(C_2-rC_3).
  \]

  Each curvature is the time integral of a Gram coverage kernel.  For a
  fixed ancestry hyperedge `H`, `q_v=P_v(H)`, the two densities reduce exactly
  to

  \[
  \sum_{v\notin H}q_v^2\Pr(v\in A,A\cap H=\varnothing)
  \]

  and

  \[
  \sum_{v\in H}q_v(1-q_v)\Pr(A\cap H=\{v\}).
  \]

  Integrating these densities over the forward singleton occupation measure
  recovers the current formula.  This explains exactly why PSD curvature is
  insufficient pointwise.

- [PROVED] In the symmetric doubly stochastic case, the stationary `C` law
  is conditioned product measure.  The fixed-hyperedge density of
  `rC3-C2` then becomes a positive scalar multiple of

  \[
  1_H^T(P^2-P)1_H.
  \]

  Positive eigenvalues of `P` make this form indefinite.  Thus even the
  regular case requires an occupation-average spectral argument; the
  complete graph is easy because all nonconstant eigenvalues are negative.

- Extended the exact verifier to check the full Poisson-curvature identity on
  the rational triangle.  It passes.

## 2026-08-02 10:08 PDT — occupation transport continuation

- [PROVED] Made the overlap formula an explicit occupation average under the
  forward graphical process generated by `C`.  In the symmetric doubly
  stochastic case, the conditioned-product stationary law and the harmonic
  Doob transform `z(H)=r^(-|H|)` give

  \[
  rC_3-C_2=(p/Z)T(P),\qquad
  T(P)=\sum_x E_{V\setminus\{x\}}\int
  1_H^T(P^2-P)1_H\,dt.
  \]

  Hence `d_s log rho_s|_0=-(r-1)T(P)/n` exactly.

- [PROVED] Derived a neutral-flow/mass-transport identity.  With
  `I(H)=1_H^TP1_H`, `E(H)=1_H^T(P^2-P)1_H`, and
  `B(H)=sum_(v notin H)P_v(H)^2`, one has `Q_1 I=2E` and

  \[
  T(P)=\frac n2[n\phi_{n-1}-(n-2)]-(r-1)B_{occ}(P).
  \]

  Thus complete-minimality of the batching loss is precisely
  complete-maximality of an accumulated collision local time.  Pointwise
  collision bounds fail (the alternating two-set on `C4` has `B=2>8/9`),
  so the occupation average cannot be discarded.

- [EXACTLY COMPUTED] At `r=3/2`, `T(C4)=92/65>T(K4)=88/65`, while
  `B_occ(C4)=208/65<216/65=B_occ(K4)`.

- Added and passed `verify_regular_mass_transport.py`.  Added
  `search_regular_mass_transport.py`; numerical optimization over positive
  symmetric stochastic kernels of orders four through six returned the
  complete kernel.  The general extremal occupation statement remains OPEN.

## 2026-08-02 10:24 PDT — exact regular cases and convexity reduction

- [PROVED] Transposed the accumulated collision local time to the reversible
  `C` chain.  The exact centered source is supported only on sets of sizes
  one, two, and three; its coefficients are `1`,
  `2(P_ij^2-2P_ij)/(r-1)`, and the corresponding two-neighbor triangle
  products.  This yields an exact two-neighbor collision Green function
  `B_occ=sum_x [(-L_C)^-1 b_P]({x})`.

- [PROVED] Solved every connected symmetric stochastic order-four kernel for
  symbolic `r>1`, with extension to the disconnected boundary by continuous
  limits.  If `P` is any such kernel,

  \[
  T(P)-T(K_4)=
  \frac{r(r-1)}{(r+1)(r^2+1)}
  [\operatorname{tr}P^2-4/3]\ge0,
  \]

  with equality only at the complete kernel.  This is a genuine exact
  trace/eigenvalue theorem, though only at the zero-batching derivative.

- [PROVED] Solved the regular complete-bipartite boundary for every `r>1`:
  `T(K_m,m)=(n-1)T(K_n)/n+1/(r+1)>T(K_n)` for `m>=2`.

- [PROVED / EXACTLY COMPUTED] On the two-`K3` modular interpolation at
  `r=3/2`, factored `T(P_epsilon)-T(K6)` as a positive rational function
  times `(5 epsilon-3)^2`.  Its exact disconnected and bipartite endpoint
  limits are `42/19` and `1212/665`; the unique minimum `5676/3325` occurs
  at the complete kernel `epsilon=3/5`.

- Extended `verify_regular_mass_transport.py` to certify the reversible
  Green identity, symbolic order-four theorem, and two-`K3` boundary
  factorization.  All checks pass.

- [NUMERICALLY OBSERVED / OPEN] Thousands of random midpoint and line tests
  through order seven, and across fitness values from `1.01` to `10`, found
  `P -> T(P)` convex.  A proof would settle complete-minimality under the
  zero-batching derivative throughout the regular class.  No variational
  representation proving this convexity has yet been obtained.

- [PROVED REFORMULATION] For a line `P_t=P+t Delta`, wrote the exact Hessian
  as

  \[
  T''(t)=2\nu_t[\|\Delta1_H\|^2-A_\Delta u'_t].
  \]

  The first term is a square.  The second is a nontrivial resolvent response;
  exact rational and numerical tests show it cancels part of the square, so
  convexity is precisely the still-open bound
  `nu A_Delta u' <= nu ||Delta 1_H||^2`.

## 2026-08-02 10:27 PDT — independent integration audit

- Reconstructed the interpolation, complete-graph telescoping product,
  occupation-current sensitivity, regular Doob transform, and
  neutral-flow/Dynkin identity directly from their generators.
- Independently checked the complete-bipartite derivation: the embedded rank
  chain has bias `r`, and Dynkin's formula for the squared side imbalance
  gives `(r+1)T=N_{n-1}+1` exactly.
- Restricted the order-four theorem statement to connected kernels, with the
  disconnected boundary explicitly interpreted only by continuous limits.
- Made both symbolic verifiers compatible with the repository's system
  interpreter and reran all three exact suites.  Every certificate passes.
- No universal conclusion was promoted: all-order regular convexity and the
  original batching-ratio inequality remain open.
