# Research log: minimal product to BDM lift

All times are America/Los_Angeles.  No external communication or graph
search was used.

## 2026-08-13 -- weak-core compound theorem

- Proved that the four local module coordinates
  `(rho_Bd,rho_dB,q_B,q_D)` do not determine reciprocal singleton outputs
  after compounding.  The outer portal support, absolute cut clock, and core
  pre-crossing excursion law are additional macro data.
- Identified the useful singular direction: weak-cut rescaling preserves the
  separated original-fitness response packet, while a reciprocal-fitness Bd
  core mutant exports across the cut before local absorption with probability
  tending to zero.  This remains true for ordinary leaves because export uses
  the core row; no analogous dB claim is required.
- Derived the exact one-sided response-scale projection

  ```text
  rho_B^out = p+p delta V_B+o(delta),
  rho_D^out = p+p delta V_D+o(delta),
  q_B^out = o(delta^2),  0 <= q_D^out <= 1.
  ```

  for every finite paired separated response packet `V` on a suitable
  connected weak-cut diagonal.
- Made the singular quantifiers explicit: the separated theorem is applied
  first to the sequence of finite Schur-trace limits.  At each already fixed
  finite stage, a positive cut clock is then chosen to approximate that
  stage's trace and to suppress reciprocal Bd export.  No uniform-in-stage
  perturbation modulus is assumed.
- Combined this with the exact leaf/tangent-`K_2` convexification.  A strict
  BDM violation produces `V_B,V_D>0`, which contradicts the portal-general
  minimal stationary product inequality on the compound graph.  Therefore
  universal MP implies BDM for every bounded separated module at `R_hyb`.
- The minimal two-copy MPER/Schur sign remains **OPEN**.  The global
  bulk/trace-compactness alternative also remains open.
- Best-guess completion of this bounded-module implication: **100%**.
  Best-guess completion of the exact-threshold program: **75%**; the local
  stationary obligation is now MPER rather than an independent MPER plus
  BDM pair.
