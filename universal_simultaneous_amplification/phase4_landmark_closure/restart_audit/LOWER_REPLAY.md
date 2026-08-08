# Restart audit: the `R_sim >= 3/2` construction

Audit time: 2026-08-07 22:19 PDT
Audited checkout: `ffe5c89cf41ca3cced5a2e573404baeb2d510897` (`main`, equal to
`origin/main` at the start of the audit)
Construction-introduction commit:
`9424066a9cb27d4d6889c821b8ad36295275f925`
(`Prove simultaneous amplification up to three halves`)

## Verdict

**PASS / PROVED.**  The frozen lower theorem, the finite-strictness argument,
and the endpoint suppression expansion replay without failure.  No new hidden
assumption or sign error was found in a hostile rereading of the rare-edge
coupling, the two Bd/dB successful-rate ratios, the center-sweep reversal
bounds, uniform singleton averaging, or the order-`N^-2` endpoint terms.

The earlier independent audit found two local issues in a draft: omitted
hypotheses in the generic rare-edge lemma and an overoptimistic Bd
sweep-excursion count.  Both repairs are already present in the current proof
at equations (15)--(18) and (27)--(28).  They do not alter the graph or theorem.

## Exact theorem replayed

For every integer `N>=3`, the graph `G_N` has:

- an `N`-vertex center clique;
- `N^2` disjoint labelled triangles;
- triangle weights `w(AD)=1` and `w(AB)=w(BD)=N^-4`;
- every center edge of weight `N^-3`;
- every center--triangle edge of weight `N^(-N^3)`;
- no edges between distinct triangles.

Thus `|V(G_N)|=N+3N^2`; all weights are positive rational numbers, the graph
is connected, and the family is fitness-independent.  For each fixed `r>1`,

```text
rho_Bd(G_N,r) -> 1/3,
rho_dB(G_N,r) -> 1/3.
```

Since both complete-graph baselines tend to `1-1/r`, for each fixed
`1<r<3/2` both strict comparisons hold for every sufficiently large `N`.
This proves `R_sim>=3/2` with the required order of quantifiers.

At `r=3/2`, the same family satisfies

```text
rho_Bd(G_N,3/2)-rho_Bd(K_(N+3N^2),3/2)
    = -4/(3N^2)+o(N^-2),
rho_dB(G_N,3/2)-rho_dB(K_(N+3N^2),3/2)
    = -16/(81N^2)+o(N^-2).
```

For every fixed `r>3/2`, the limiting comparison is also negative.  Hence
`(1,3/2)` is exactly the amplification interval of this family, not yet a
universal upper bound on `R_sim`.

## Critical files and Git blobs at the audited checkout

```text
construction/CENTER_TRIANGLE_PROOF.md
  4860d0381110bdc3c4d51818c7bfd4da8d70dc41
construction/verify_triangle_module.py
  0f921581e70b59f75daa44b722a8e0d6d4becd0b
construction/verify_center_triangle_lumping.py
  6086085a8a18232e29fc6c2eb7eaeded9e687b3b
construction/scan_center_triangle.py
  0cbac6909f4173f59b501a81a547fc830a8b179e
threshold/CENTER_TRIANGLE_AUDIT.md
  109a425458bd12159a22038f73ce774521a99baf
threshold/triangle_star_lower_bound.md
  ead88d117b3add7687f64827664c6256403b25c9
threshold/verify_triangle_star.py
  87aba2d0bedaf3d48607f7ea3d1150327505b77c
```

The primary proof is `construction/CENTER_TRIANGLE_PROOF.md`; its theorem is
at lines 39--69, exact isolated-module formulas at lines 71--174, center
formulas at 176--204, quantitative separation at 206--277, Bd/dB trace rates
at 279--353, sweep and finite-excursion control at 355--405, strictness at
407--435, and endpoint expansion at 437--530.  The independent hostile audit
is `threshold/CENTER_TRIANGLE_AUDIT.md`.

## Critical replay commands and outputs

All commands were run with the indicated directory as working directory and
exited zero.

From `phase4_landmark_closure/construction`:

```bash
PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python verify_triangle_module.py
```

```text
PASS exact alpha_Bd
PASS exact Y_Bd
PASS exact alpha_dB
PASS exact I_dB
PASS exact X_Bd
PASS limit alpha_Bd->1/3
PASS limit alpha_dB->1/3
PASS limit Y_Bd->1
PASS limit 2delta X_Bd->1
PASS limit I_dB->(2r+1)/(2r)
PASS limit J_dB->(r+2)/2
PASS macro thresholds
PASS center reverse ratios
PASS endpoint comparison coefficients
```

This script independently builds and solves both six-transient-state triangle
chains over `Q(r,delta)`.  It checks the exact Bd and dB forward/reverse
quantities, all singular limits, the center formulas, the scale window, and
both endpoint comparison coefficients.

From the same directory:

```bash
PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python verify_center_triangle_lumping.py
```

```text
PASS c=2 M=1 delta=1/5 z=2/7 epsilon=1/13 r=6/5 rule=Bd cells=22
PASS c=2 M=1 delta=1/5 z=2/7 epsilon=1/13 r=6/5 rule=dB cells=22
PASS c=2 M=2 delta=2/9 z=3/8 epsilon=1/17 r=7/3 rule=Bd cells=106
PASS c=2 M=2 delta=2/9 z=3/8 epsilon=1/17 r=7/3 rule=dB cells=106
```

This is the independent exact `Fraction` implementation.  For every subset
of the test graphs, it aggregates the full chain by center count and the
histogram of all eight labelled triangle masks, proves strong lumpability on
those instances, and matches every quotient transition for both rules.

From `phase4_landmark_closure/threshold`:

```bash
PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python verify_triangle_star.py
```

```text
PASS: exact triangle chains, singular limits, and macro identities
```

This separately written implementation rebuilds and solves the triangle
chains directly from the definitions and checks the dB reverse-invasion
factor and macro-threshold identity.  It is independent of the construction
track's symbolic formulas.

A residual-checked finite quotient fixation diagnostic was also replayed on
the prescribed `N=2` parameter values (outside the stated `N>=3` theorem):

```bash
PYTHONDONTWRITEBYTECODE=1 ../../.venv/bin/python scan_center_triangle.py \
  --center 2 --modules 4 --delta 0.0625 --z 0.125 \
  --epsilon 0.00390625 --fitness 1.2
```

```text
Bd rho=0.137821945038 excess=-0.0429223 residual=1.65e-15 states=988
dB rho=0.167113866027 excess=-0.00360399 residual=1.81e-15 states=988
```

This diagnostic is not a theorem certificate and its finite negative signs
are consistent with the eventual, rather than all-`N`, conclusion.  A larger
`N=3` floating solve was deliberately stopped after about 2.5 minutes and
roughly 2 GB of memory because it was non-proof and resource-heavy; this is
not a replay failure.

## Hostile proof checks

1. The rare-edge lemma now explicitly assumes positive internal degree and
   `epsilon<=b`; both hold for every `G_N`.  Its error obeys
   `log eta_N=-N^3 log N+O_r(N log N)`, so `N^10 eta_N=o(N^-K)` for every
   fixed required power.
2. The favorable/adverse first-stage odds rederive directly as
   `A_B~(r-1)N^2/2` and `A_D~6r^2(r-1)N^2/(2r+1)`.
3. The corrected excursion accounting gives total expected excursion count
   `O_r(N^6)` and an `N^10` tail of `O_r(N^-4)`.
4. Center reversal across `N^2` module conversions is bounded by
   `O_r(N^4 r^-N)` for Bd and the analogous `O_r(N^4 r^(2-N))` bound for dB.
5. At the endpoint all omitted paths contribute `o(N^-2)`.  Module starts
   contribute deficits `4/(3N^2)` and `16/(81N^2)`; the center-start dB
   correction contributes `1/(9N^2)`, exactly canceled when the complete dB
   baseline is subtracted, leaving `16/(81N^2)`.

## Scope boundary

The exact verifiers certify finite symbolic components and quotient
transitions; the all-`N` conclusion is discharged by the analytic coupling
and asymptotic estimates, not finite testing.  No explicit numerical formula
for `N_0(r)` is recorded because the proof uses harmless constants `C_r`, but
it rigorously proves existence of `N_0(r)`, which is the required quantifier.
Nothing in this replay proves `R_sim<=3/2`.
