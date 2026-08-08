# Research log

## 2026-08-08

- Recovered the exact `(h,i,j)` quotient used in the finite endpoint product
  audit.
- Identified the growing ray `c=8m` at `r=3/2`.
- Derived the slow Bd leaf process.  Its per-particle rates are leaf birth
  `1/4`, leaf death `1/9`, and successful core marking `2/3`.
- Solved the no-mark extinction equation exactly: roots `1/9,4`; the physical
  root gives Bd leaf fixation limit `8/9`.
- Closed the post-establishment gap with uniform core gambler-ruin bounds and
  a high-density absorption argument for both update rules.
- Obtained actual fixation limits `32/81` (Bd) and `8/27` (dB), hence
  normalized limits `32/27` and `8/9` and product `256/243>1`.
- Replayed exact full-chain solutions for `m=1,2,3,4` and sparse solutions
  through `m=50`; all singleton components approach the derived limits.
- Scope: this refutes the endpoint product route by a fixed positive margin,
  but dB suppression means it is not an endpoint simultaneous amplifier.
