# Live handoff: exact-threshold closure

Checkpoint date: 2026-08-08 dilute-hybrid threshold breakthrough
(America/Los_Angeles)

## Current theorem state

- **PROVED:** `R_sim>=R_hyb=1.5028569127905696...>3/2` by the explicit
  dilute pair--leaf family.  The exact threshold is the isolated root of
  `r^6-8r^5+22r^4-30r^3+21r^2-6r+1`; finite weak-cut trace,
  post-establishment fixation, compact-uniform diagonal, and exact algebra
  are all audited.
- **PROVED:** the inherited center--triangle family is suppressing under
  both rules at `r=3/2`; this statement does not apply to the new hybrid.
- **PROVED CLASS THEOREM:** fixed-finite-rank positive-incidence blade/portal
  families without portal edges cannot work at any fixed `r>=3/2`.
- **EXACTLY FALSIFIED:** the universal endpoint product inequality.  The
  unweighted 36-vertex `G(31,4)=K_32` with four hub pendants has normalized
  product `1.000669371885...>1`, with independent exact rational audits.
- **PROVED GROWING COUNTEREXAMPLE:** `K_(8m+1)` with `m` hub pendants has
  normalized endpoint limits `32/27` and `8/9`, so its product tends to
  `256/243>1`; the post-establishment step is audited, not assumed.
- **EXACTLY FALSIFIED:** the balanced normalized arithmetic separator; the
  same graph has normalized mean `1.006912940840...>1`.
- **FALSIFIED:** universal no-simultaneous endpoint obstruction.  The new
  family eventually amplifies both rules at `r=3/2`.
- **EXACTLY FALSIFIED:** the one-third affine candidate, by the exact
  `(2,20)` complete-support graph with weights `(137,1,1/500)`.
- **FALSIFIED:** every fixed convex affine separator.  The new witness forces
  `theta>1/3`, while clique--pendant rays force `theta<=1/3`.
- **PROVED SHARPNESS:** no universal convex affine separator can give Bd a
  coefficient above `1/3`; explicit clique--pendant rays have crossing
  coefficient decreasing to `1/3`.  An exact rational dB witness forces the
  complementary lower bound `theta>=0.088542283991...`.  The sharp candidate
  holds for every positive weighted triangle; no coefficient in the resulting
  necessary window is proved universal.
- **EXACT FINITE STAR THEOREM:** the unit star is dB-maximal among arbitrarily
  weighted stars through 20 leaves by an exact coefficient recurrence.  The
  recurrence sign for every leaf count remains open.
- **PROVED CLASS OBSTRUCTION:** a unit clique with an unbounded number of
  hub pendants is eventually dB-suppressing even when every pendant has an
  arbitrary positive, size-dependent weight.
- **EXACT ROUTE CLOSURE:** the natural separate `1:2` orientation and
  batching signs are false on an integer-weight six-cycle; only their full
  cancellation retains the one-third inequality there.
- **PROVED REFORMULATIONS:** `T+C` is an exact rankwise Johnson Dirichlet
  pairing, and the reversed-arrow stationary chord is an exact electrical
  two-tree transfer scalar.  Neither final sign is proved.
- **EXACT ROUTE CLOSURES:** scalar and degree-two Green-flow relaxations fail;
  transient/treewise/rank-tail orientation strengthenings fail; the
  `r=2` symmetric-flow split fails on an undirected order-six graph.  All
  witness graphs retain the desired actual fixation comparison.
- **OPEN:** exact fitness-two sign `L<=V` and hence any finite universal upper
  bound on `R_sim`.
- **OPEN:** exact value of `R_sim`; the current rigorous lower bound is
  `R_hyb`.  The exact `r=2` stationary collision inequality remains the
  principal universal-upper-bound route.

## Repository and preservation

The restart base was
`ffe5c89cf41ca3cced5a2e573404baeb2d510897`; the audited restart integration
was pushed as `72289a4a45e4db97ca473bd84e7bd9773ded791f`, and the endpoint
Green--Poisson reduction as `8ef6e0b0` on `main`.  The current public-preprint
commit is `db9c03ec`, following the weighted-star checkpoint `f481e3e6`.
Exact replay reports are under `restart_audit/`.  Do not delete or silently
modify the untracked discovery program
`obstruction/stationary_inequality/explore_target_information.py`; it is
historical and not part of the audited theorem packages.

## Exact live targets

Endpoint (product now refuted):

```text
min(rho_Bd/rho_Bd(K_n), rho_dB/rho_dB(K_n)) <= 1,
```

with the current affine candidate

```text
(rho_Bd/rho_Bd(K_n)+2 rho_dB/rho_dB(K_n))/3 <= 1.
```

Fitness two:

```text
rho_dB(G,2)-rho_dB(K_n,2)=L(G)-V(G),
```

so the exact missing sign is `L<=V`.

## Immediate next action

Continue three independent live branches:

1. formalize and publish the dilute pair--leaf theorem and its independent
   labelled/Schur verification, replacing the now-superseded endpoint
   narrative in preprint v1.0.0;
2. optimize the general dilute bounded-gadget tangent cone.  The exact
   `K_s` formulas and finite searches currently single out `K_2`, but no
   universal gadget theorem or global upper bound is proved;
3. prove the direct stationary collision sign at `r=2`.  The marked
   one-sample lift and its uniform two-step sum-of-squares inequality are
   proved; the sole new obstruction is promotion to the stationary marked
   law.

Do not retry rank/overlap-only, vertex-bilinear pointwise, statewise,
fixed-rank, separately signed, or first-change-balanced endpoint
certificates.  Also do not retry finite-degree Green relaxations, transient
orientation domination, treewise reversal, rank-tail domination, or the
`L<=S<=V` split: exact witnesses now close all of them.

The endpoint counterexample has already been converted into one growing
fitness-independent family with an exact interval.  Do not reopen the
universal endpoint-obstruction or fixed-affine programs.

## Publication boundary

The hostile-audited 18-page lower-bound manuscript, deterministic PDF, and
exact replay package are committed at `db9c03ec` under
`paper_lower_threshold/`.  Public preprint v1.0.0 is live at
`https://github.com/AlecKriebel/Math/releases/tag/simultaneous-amplification-below-three-halves-v1.0.0`.
The PDF SHA-256 is
`cfd9eb2755a4f9296eae8209adff6f6b41708425a4a4f186e647184ec6617672`;
the source/certificate archive SHA-256 is
`3499314496f905fd8c89a285e3c1cb91189450d7e2f7898f1db90fc1e330be27`.
The archival hook minted version DOI `10.5281/zenodo.21850042` (verified
through the Zenodo record and DOI redirect); its concept DOI is
`10.5281/zenodo.21753404`.  No journal submission or external outreach
occurred.  Under the independent research policy, only the human researcher
may initiate external communication.

## 2026-08-08 latest exact checkpoint

- **PROVED CLASS THEOREM:** fixed `Q=2,T=1` direct-portal strong-pair
  systems, including arbitrary unequal positive loads and any positive
  portal edge, cannot cross `3/2`.  Commit `f4956bd0`.
- **PROVED GROWING-CLASS THEOREM:** diffuse regular portal networks with
  `Q_s->infinity`, `Q_s=o(s)`, and exchangeable incidence fail simultaneous
  establishment for every `r>1`.  Commit `ece03514`.
- **PROVED REDUCTION / OPEN SIGN:** endpoint batching is exactly the paired
  rooted-arborescence/coverage covariance (G) in `ACTIVE_LEMMAS.md`.
  Persistence, timing, and rootwise signs are each exactly false.  Commits
  `5ff48ffb`, `eda895fe`.
- **PROVED SHARP LEMMA / OPEN SIGN:** the rank-weighted posterior reflection
  (H)--(H1) retains the finite complete baseline at `r=2`.  Local Cayley,
  target, edge, and cycle shortcuts are exactly closed.  Commit `425fa927`.
- **EXACTLY FALSIFIED:** endpoint product and balanced arithmetic separators,
  by the independently audited `G(31,4)` witness in commits `02335bb0` and
  `21601879`.
- **STILL OPEN:** endpoint disjunction and one-third affine separator, the
  exact `r=2` stationary mean bound, and the value of `R_sim`.

The active proof cycle is global: combined endpoint forest transport and
full-tree complement reflection at `r=2`.  Further construction work must
leave both the fixed-rank and diffuse-growing portal scopes and must control
fixation after establishment.

## 2026-08-08 landmark correction

The preceding historical checkpoint is superseded as follows.

- Commit `a660aa3f` exactly refutes the one-third separator and, together
  with the clique--pendant sharpness theorem, every fixed convex affine
  separator.
- Commit `9c37b436` supplies an independently derived dilute pair--leaf
  construction beyond `3/2`; the canonical full theorem and constructive
  diagonal are in `threshold/dilute_pair_leaf_hybrid/` pending final
  integration commit.
- The exact class threshold is `R_hyb=1.5028569127905696...`, the isolated
  sextic root recorded above.  The global exact value of `R_sim` remains
  open.
- Commits `3e65e0b7` and `c6e60ca5` reduce the `r=2` fallback to a stationary
  marked-chain promotion after proving the universal uniform two-step
  sum-of-squares comparison.
