# Research log: one-root Kac likelihood obstruction

## 2026-08-13 17:54 PDT — exact event formulas and active obstruction

- Isolated the one-root target on the active branch as
  `r^3 psi_B,i psi_D,i <= 1`.
- Derived honest event-epoch formulas for both signed Kac rewards.  Bd uses
  the graphical-attempt clock `r T(A)`, while dB uses the exact exit clock
  `|A|`.  The resulting denominators are respectively `T(A)` and `|A|`.
- Derived the corresponding first-departure renewal formulas, retaining all
  negative singleton and positive higher-rank occupation reward.
- Audited the weighted path with edge ratio `1:17` and centre root.  Exact
  absorbing-chain formulas prove that both Bd and dB stationary density
  excesses are strictly positive for every
  `3/2 <= r <= 151/100`, hence at `R_hyb`.
- Proved that the unmarked return-cycle laws are singular at the first dB
  multi-source burst.
- On the canonical target-locked expansion, derived the general repeated-
  source likelihood moment.  On the same active `1:17` path its second
  moment is infinite because its exact geometric ratio is
  `9(r-1)/(2r)>1`.
- Derived the exact signed-Hellinger remainder.  It is indefinite for a
  signed reward even when both reward means are positive; for a nonnegative
  reward it gives a lower bound, not the required upper bound.
- Scoped conclusion: canonical scalar Radon--Nikodym/Hölder/Hellinger
  optional stopping through unmarked cycles, endpoint/rank coboundaries, or
  the target-locked history expansion is closed.  The diagonal theorem
  itself is not refuted.  A signed full product-chain Poisson, marked-matrix,
  or forest certificate remains possible.
- No graph enumeration, kernel optimization, literature search, or external
  communication was used.
- Best-guess completion: **100% for this exact obstruction checkpoint; 0%
  for the still-open universal sign of D-KAC.**
