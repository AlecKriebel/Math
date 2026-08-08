# Restart state for exact-threshold closure

Restart date: 2026-08-07 (America/Los_Angeles)

Status vocabulary in this file is literal: **PROVED**, **EXACTLY COMPUTED**,
**RIGOROUSLY BOUNDED**, **NUMERICALLY OBSERVED**, **FALSIFIED**, or **OPEN**.

## Repository state

- repository: `/Users/alec/Documents/Math-universal-amplification`;
- branch: `main`;
- clean tracked base at restart:
  `ffe5c89cf41ca3cced5a2e573404baeb2d510897`;
- `origin/main` at restart: the same commit;
- base subject: `Close unequal-load rank-one portal regime`;
- latest fixed-graph paper commit:
  `cf61bfdffb1531b328fb0dcd147714782932036b`;
- lower-construction commit:
  `9424066a9cb27d4d6889c821b8ad36295275f925`;
- exact-dual framework commits:
  `13ec490d15062d025a3bf44f5b02d4d4798632b8` and
  `9c12949443a0b340954dd0d38af0f1f9d50e850c`;
- exact three-halves product checkpoint commits:
  `a4d4d3e7e4bbcfc2750028ca6e57d90d21a71a0c` and
  `daf403ae6f4f28249c10d4a937c40e52c0ac8852`;
- fitness-two Green--collision commit:
  `c5bf7bda98282146836d57c203fd3c842cd298a8`;
- rank-one portal commit:
  `ffe5c89cf41ca3cced5a2e573404baeb2d510897`.

At restart, three completed but untracked exact packages were preserved for
audit: the fixed-finite-rank portal theorem, the product-chain route
closures, and the fitness-two entropy-reflection reductions.  They are not
part of the clean base hash above.

## Frozen theorem statements

### Fixed finite graphs

**PROVED / INHERITED.**  Every fixed finite nonbaseline connected loopless
undirected weighted graph is dB-suppressing for all sufficiently large
fitness.  This is Paper I and is not rederived in phase 4.

### Constructive lower bound

**PROVED.**  For every `N>=3`, let `G_N` have an `N`-vertex center clique and
`N^2` disjoint triangles.  Triangle weights are

```text
w(AD)=1,  w(AB)=w(BD)=N^-4,
```

center-clique weights are `N^-3`, and every center--triangle edge has weight
`N^(-N^3)`.  Then `|V(G_N)|=N+3N^2`, the graph is connected, all weights are
positive rational and independent of fitness, and for every fixed `r>1`,

```text
rho_Bd(G_N,r) -> 1/3,   rho_dB(G_N,r) -> 1/3.
```

Therefore one family eventually strictly amplifies both rules for every
fixed `1<r<3/2`, with the required nonuniform-in-`r` quantifier order.  Hence

```text
R_sim >= 3/2.
```

At `r=3/2` this same family satisfies

```text
rho_Bd(G_N,3/2)-rho_Bd(K_(N+3N^2),3/2)
    = -4/(3N^2)+o(N^-2),
rho_dB(G_N,3/2)-rho_dB(K_(N+3N^2),3/2)
    = -16/(81N^2)+o(N^-2).
```

Thus `(1,3/2)` is the exact interval of this family only.

### Fixed-finite-rank separated portals

**PROVED AFTER HOSTILE AUDIT, WITH FIXED SCOPE.**  Fix `Q,T`, positive
limiting blade proportions `pi_t`, and positive finite incidences
`lambda_at`, all independently of the blade count `s`.  Take `s` disjoint
unit blade edges, join both endpoints of each type-`t` blade to portal `a`
with weight `lambda_at/s`, and include no portal--portal edges.  For every
fixed `r>=3/2`, at least one update rule is eventually strictly suppressing.
For `3/2<=r<=2`, the exact stopped-trace establishment bounds obey

```text
alpha_B+alpha_D < 2(1-1/r).
```

This does not cover growing `Q` or `T`, vanishing types, zero or size-dependent
incidences, other relative scalings, positive-proportion portals, or direct
portal edges.  It is a class theorem, not a universal graph theorem.

### Fitness-two exact reduction

**PROVED REFORMULATION.**  For every admissible finite graph,

```text
rho_dB(G,2)-rho_dB(K_n,2) = L(G)-V(G),   V(G)>=0,
```

with `L` the exact stationary cut-surplus/internal-pair functional and `V`
the exact subset-dispersion functional in
`obstruction/r2_collision_bound/R2_GREEN_COLLISION_REDUCTION.md`.  The
remaining sign `L<=V` is **OPEN** and is equivalent to finite complete-graph
maximality at fitness two.

### Fitness-three-halves exact results

**PROVED / EXACTLY COMPUTED / EXACTLY REFUTED GLOBALLY.**  Every positive
weighted triangle satisfies the fixation-product inequality at `r=3/2`,
strictly unless all weights are equal.  The complete graph is an exact strict
local log-product maximizer on both irreducible edge modes for the audited
orders.  Nevertheless the full all-graph product inequality is false:
`G(31,4)=K_32` with four hub pendants has exact normalized product
`1.000669371885...>1`.  Its dB ratio is below one, so the weaker disjunctive
separator remains **OPEN**.  The balanced normalized arithmetic separator is
also exactly false on this graph.

The failure persists asymptotically.  For `G_m=K_(8m+1)` with `m` leaves
attached to one hub, an audited post-establishment argument and exact rare
branching limit give normalized endpoint limits `32/27` and `8/9`; hence the
product tends to `256/243>1`.  More generally, varying the limiting leaf
proportion proves that every graph-independent convex affine separator must
give Bd coefficient at most `1/3`.  The sharp one-third separator remains
**OPEN**, but is proved for every positive weighted triangle.

## Critical replay ledger

| Package | Result | Exact replay |
|---|---|---|
| lower construction/module | PASS | `verify_triangle_module.py` |
| lower construction/lumping | PASS | `verify_center_triangle_lumping.py` |
| independent lower chain | PASS | `threshold/verify_triangle_star.py` |
| endpoint suppression | PASS | included in the module and independent audits |
| higher-rank separated portals | PASS | `verify_higher_rank_separation.py` plus independent Bernstein evaluation |
| fitness-two Green--collision | PASS | `verify_green_collision_reduction.py` |
| fitness-two entropy reflection | PASS AS REDUCTION ONLY | `verify_entropy_reflection.py`, `verify_resolvent_identities.py`, `verify_shannon_routes.py` |
| three-halves triangle/drift | PASS | `verify_product_and_drift.py` |
| local product Hessian | PASS for `n=4,5,6` | `exact_log_product_hessian.py` |
| product-chain route closures | PASS AS ROUTE CLOSURES ONLY | `verify_product_chain_barriers.py` |
| representative endpoint screens | no violation observed | order-six atlas and saved sparse search; numerical only |

Full commands, outputs, hashes, and scope boundaries are in
`restart_audit/LOWER_REPLAY.md`, `restart_audit/PORTAL_AUDIT.md`, and
`restart_audit/OPEN_LEMMA_REPLAY.md`.

## Claims that remained unaudited at Gate 1

No theorem used by the restart failed replay.  The following historical
diagnostics were deliberately not rerun because they are not proof inputs:

- million-instance weighted endpoint searches;
- the separately recorded exact order-seven product Hessian;
- broad directed entropy screens;
- every old candidate-family scan;
- a resource-heavy `N=3` floating center--triangle quotient solve.

The phase-4 exact-threshold paper does not yet exist.  The only completed
paper in the repository is the inherited fixed-graph paper under `paper/`.

## Genuinely open proof obligations

1. Prove or refute the weaker statement that at least one of
   the two normalized fixation probabilities is at most one at `r=3/2`.
2. Prove or exactly refute the surviving one-third affine separator
   `(x+2y)/3<=1`, which would imply the disjunction.
3. Prove or refute the exact fitness-two sign `L(G)<=V(G)`.
4. If an endpoint simultaneous amplifier is found, convert its mechanism
   into one growing, fitness-independent family and prove a strict interval
   beyond `3/2`; a finite graph alone is insufficient.

## Next three executable mathematical tasks

1. Attack the one-third affine separator using the exact weighted
   Green--Poisson identity while respecting the four-star Farkas obstruction.
2. Search targeted weighted clique--pendant and related two-scale families
   for a true endpoint simultaneous amplifier, exactifying any candidate.
3. Attack `L<=V` through a two-particle stationary likelihood/capacity
   inequality, keeping the finite complete-baseline correction; the Shannon
   and chi-square reductions alone yield only half density.

## 2026-08-08 continuation checkpoint

The audited committed checkpoint after the latest construction cycle is
`ece03514` on `main`; its immediate theorem/reduction milestones are:

- `5ff48ffb`, `eda895fe`: exact endpoint event--Palm and rooted-arborescence
  batching reductions;
- `f4956bd0`: exact two-portal direct-network obstruction for all
  `r>=3/2` in the fixed `Q=2,T=1` scope;
- `425fa927`: sharp rank-weighted posterior-reflection reduction at `r=2`;
- `ece03514`: all-fitness obstruction for growing diffuse regular portal
  networks with exchangeable incidence.

All associated exact verifiers replayed successfully from the repository
root.  The historical untracked stationary-discovery script remains
preserved and is not part of any theorem package.

The next three executable tasks are now:

1. combine the orientation and batching arborescence formulas into one
   full endpoint-product forest sign, allowing their indefinite pieces to
   cancel;
2. attack the exact `r=2` stationary mean through complement/root-moving
   path reversal on full Markov-chain trees, rather than another local Brier
   split;
3. test the remaining construction regimes outside the proved portal
   obstructions: fixed-degree portal networks, portal-dependent incidence,
   and singular/mesoscopic scaling, with post-establishment fixation control
   required before any positive claim.
