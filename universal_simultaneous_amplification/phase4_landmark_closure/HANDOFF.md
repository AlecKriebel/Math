# Live handoff: exact-threshold closure

Checkpoint date: 2026-08-07 (America/Los_Angeles)

## Current theorem state

- **PROVED:** `R_sim>=3/2` by the explicit rational center--triangle family.
- **PROVED:** the same family is suppressing under both rules at `r=3/2`.
- **PROVED CLASS THEOREM:** fixed-finite-rank positive-incidence blade/portal
  families without portal edges cannot work at any fixed `r>=3/2`.
- **OPEN:** universal endpoint product inequality.
- **OPEN:** weaker universal no-simultaneous endpoint separator.
- **OPEN:** exact fitness-two sign `L<=V` and hence any finite universal upper
  bound on `R_sim`.
- **OPEN:** exact value of `R_sim`; current rigorous information is only the
  lower bound `R_sim>=3/2`.

## Repository and preservation

The restart base is
`ffe5c89cf41ca3cced5a2e573404baeb2d510897` on `main`, equal to
`origin/main` before restart integration.  Exact replay reports are under
`restart_audit/`.  Do not delete or silently modify the untracked discovery
program `obstruction/stationary_inequality/explore_target_information.py`;
it is historical and not part of the audited theorem packages.

## Exact live targets

Endpoint:

```text
rho_Bd(G,3/2) rho_dB(G,3/2)
<= rho_Bd(K_n,3/2) rho_dB(K_n,3/2),
```

or at least

```text
min(rho_Bd/rho_Bd(K_n), rho_dB/rho_dB(K_n)) <= 1.
```

Fitness two:

```text
rho_dB(G,2)-rho_dB(K_n,2)=L(G)-V(G),
```

so the exact missing sign is `L<=V`.

## Immediate next action

After committing and pushing the restart/audit integration, open three
independent branches of work within this task:

1. a vertex-sensitive product-chain/variational certificate at `r=3/2`;
2. hostile exact endpoint optimization of both product and minimum ratios;
3. a two-particle stationary/capacity proof of `L<=V` at `r=2`.

The first exact theorem, exact endpoint counterexample, or universal
fitness-two sign should stop broad exploration and trigger theorem
extraction.  A finite endpoint amplifier alone is not a threshold result; it
must be converted into one growing fitness-independent family.

## Publication boundary

No phase-4 paper or release exists yet.  The inherited fixed-graph paper is
under `universal_simultaneous_amplification/paper/`.  Under the independent
research policy, no specialist outreach may be prepared or initiated; a
future external-review step may only be recorded as human-only.
