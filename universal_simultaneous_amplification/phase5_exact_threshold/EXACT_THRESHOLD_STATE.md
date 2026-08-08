# Exact-threshold state

Last updated: 2026-08-08 08:48 PDT.

## Frozen starting point

Repository checkpoint at phase start:

```text
91d1f03b7e44e3d91cd86756117850ed0cabfa08
```

on `main`, equal to `origin/main`.  Three pre-existing untracked discovery
packages are preserved and are not theorem inputs.

Let

\[
P(R)=R^6-8R^5+22R^4-30R^3+21R^2-6R+1.
\]

The unique root in `(3/2,151/100)` is

\[
R_{\rm hyb}=1.5028569127905696267\ldots .
\]

The dilute pair--leaf family proves

\[
\boxed{R_{\rm sim}\ge R_{\rm hyb}}.
\]

This is the exact threshold of that two-generator leading family, not a
universal upper bound.

## Gate-1 replay

The frozen construction replay passed on 2026-08-08:

- exact sextic root, tangency, and monotonicity algebra;
- exact labelled hybrid lumping: 512 masks and 108 fibres;
- rational endpoint margins `232/17361` (Bd) and `65/12123` (dB);
- optimized and rational-family threshold certificates.

The fitness-two structural replay passed:

- exact marked stationarity and collision identity;
- exact two-step sum-of-squares theorem;
- exact Perron and forward-active factorization;
- exact hostile witnesses closing rank-tail, temporal-monotonicity, and
  radial-PGF strengthenings.

The exact promotion corpus also passed on all 54 audited order-three, 624
order-four, 48 deterministic order-five, and the frozen order-six graphs.
This is finite evidence only.

## Current theorem frontier

### Proved

1. `R_sim>=R_hyb>3/2` by one fitness-independent family.
2. The endpoint product, disjunctive, and every fixed convex affine
   obstruction at `r=3/2` are false.
3. The complete graph is a strict two-step minimum for the exact marked
   fitness-two collision observable, with an explicit sum-of-squares gap.
4. The scoped class obstructions listed in the phase-4 claims ledger.

### Open

1. Whether every graph satisfies
   `rho_dB(G,2)<=rho_dB(K_n,2)`.
2. Whether one family amplifies both rules for every fixed `1<r<2`.
3. Any finite universal upper bound on `R_sim`.
4. The exact value of `R_sim`.

## Working exact-threshold hypothesis

`R_sim=2` is a hypothesis to prove or refute, not an assumption.  The upper
route is `ACTIVE_R2_LEMMA.md`; the lower route is the response-cone and
diagonal program in `MODULE_RESPONSE_LIBRARY.md`.

## Branch ownership

- `r2_determinant/`: tree/determinant proof branch;
- `r2_hostile/`: exact counterexample branch;
- `lower_to_two/`: module-response and diagonal-family branch.
