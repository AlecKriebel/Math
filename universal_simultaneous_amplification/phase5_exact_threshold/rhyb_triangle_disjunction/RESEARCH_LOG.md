# Research log: the `R_hyb` disjunction on weighted triangles

Started: 2026-08-13 (America/Los_Angeles).

## Objective

Let `rho_B`, `rho_D` be uniform-singleton Bd and dB fixation on a connected
weighted triangle, and let `rho_B^K`, `rho_D^K` be the corresponding complete
triangle values.  A sufficient exact finite disjunction is

\[
                         \rho_D\le\rho_D^K.             \tag{1}
\]

This is a sharply scoped base-class test for a possible matching upper bound
at `R_hyb`.  It is not an all-graph or asymptotic theorem.

## 2026-08-13: generic factorization and dB certificate

- Built both six-state absorbing chains directly at symbolic fitness `r` and
  symbolic edge weights `(a,b,c)`.
- After clearing the positive denominators, the two separate deviations have
  homogeneous symmetric numerators of degree twelve (Bd) and six (dB).
- The product of the two deviations is **not** a correct encoding of the
  disjunction: both rules may be suppressing.  This logical error was caught
  before any theorem claim or checkpoint.
- The dB degree-six form has an exact positive exchange-square decomposition
  for every `r>1`.  Writing `tau=r+1/r` and

  \[
  E_{ijk}=\sum_{(x,y,z)\in S_3(a,b,c)}
           x^i y^j z^k(x-y)^2,
  \]

  the cleared form is

  \[
  r^2\{(\tau-2)^2A+(\tau-2)M+H\},
  \]

  where

  \[
  A={3\over2}E_{112},\quad
  M=6E_{121}+{11\over2}E_{112}+2E_{013},
  \]

  \[
  H=2E_{220}+20E_{121}+4E_{112}+4E_{004}.
  \]

  Every coefficient is positive and `tau-2=(r-1)^2/r>=0`.  The factor
  `E_004` gives equality rigidity for positive weights.  Since the dB gap
  has the negative of this form over a positive denominator, every weighted
  triangle is a strict dB suppressor unless it is equal-weighted.

Status: **PROVED for the weighted-triangle dB/disjunction theorem.**

## Independent hostile audit

An independent derivation verified the exact sign orientation

\[
 \rho_{dB}-\rho_{dB}(K_3)
 =-{r(r-1)F\over3(r+1)D},
\]

where `D` has eighty strictly positive coefficients, checked the sixfold
permutation normalization of every `E_ijk`, and confirmed rigidity from
`E_004`.  The replay was then hardened to assert the two scalar numerator
factors `r` and `r-1` explicitly.

Best-guess completion toward the all-graph `R_sim` problem: **12%**.  This is
an exact base class, not an induction theorem.
