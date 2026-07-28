# Research log: separated-core order-14 attack

## 2026-07-27 PDT

- Reconstructed the tight static 14-vertex realization
  `MFzvvn{feBKbM{gZ_}` and classified its five nonneutral witnesses.
- Confirmed that all 14 selected direct seed states dominate, while the
  three-guard greatest kernel is empty after deletion rounds \(140,60\).
- Built a bounded one-attack SAT probe.  Discovery formulas showed that
  the exact core is already impossible at one attack round, and that four
  direct states at the overlapping lists of \(q\) and \(v_1\) suffice.
  The SAT output is discovery provenance only.
- Extracted a human argument from the one-attack obstruction:
  a neutral two-response vertex forces a pure omitted-color pair and
  replicates its two positive responses at a physical nonedge terminal.
- Combined two overlapping response pairs to prove a six-witness bound,
  giving the human exact-pattern floor \(n\geq15\) without using the full
  response at \(x\).
- Added a clean-room verifier for the static control, exact parameters,
  greatest kernels, response seed, and four explicit failed first attacks.
