# Research log: characteristic-two support geometry

## 2026-07-25

- Reconstructed the exact nontrivial characteristic-two factor
  \(K=\mathbf F_{2^{36}}\) directly as
  `F2[x]/(1+x+...+x^36)`.  Implemented multiplication, inversion,
  `x -> x^-1`, the fixed field, exact 37-bit CRT inversion, and independent
  algebraic self-tests.
- Proved that the trivial parity quotient and the rank-four unitary
  projection are Cartesian factors before Hamming margins are imposed.
  Consequently a purely field-equation argument cannot distinguish the
  two binary quotient types.
- Built exact `9 x 18` diagonal incidence tables with the quotient row
  margins and the complete residue/nonresidue column law `(6,3)`.
- Derived and implemented the two-coordinate unitary rotation equation.
  Starting from `E0=Q+eta*(I+J)`, prescribed all nine target diagonal
  field entries exactly for each of the two quotient targets.  Every
  intermediate operation remains in the Hermitian rank-four projection
  variety; the terminal projection is independently squared.
- Initially attempted to tune off-diagonal weights only with diagonal
  phases.  Roughly half the edge domains were empty.  This was not a
  random-search failure: diagonal phases preserve the unitary norm.
- Derived the exact support law

  ```text
  absolute_trace(f*f*) = C(weight(f),2) mod 2.
  ```

  It explains the empty domains and turns them into a one-bit norm gate
  per edge.
- Taking absolute traces in the projection diagonal equation shows the
  target norm-trace graph must be Eulerian.  Audited all 625 quotient
  classes: every one passes.  A quotient-only reduction modulo four proves
  this is automatic.  The edge-count distribution across the 625 classes
  is:

  ```text
  6:4 10:2 12:34 14:78 16:140 18:132
  20:118 22:90 24:26 26:1
  ```

- Added diagonal-preserving exact unitary moves and a norm-trace objective.
  Matching all 36 required norm traces reduces the remaining margin task
  to a cyclic difference CSP over the unit circle of order 262,145.
- Found a complete type-1 support witness.  Independent bit-level replay
  checks 45 margins, star symmetry, the full `(6,3)` trace law, and all
  2,997 coefficients of the group-ring adjacency equation.

  ```text
  text SHA-256
  3f77fc3d39fc6b8dfd33efbba846e61ca835581d15f9ae4c12d8f57a3249e697

  JSON semantic SHA-256
  fc5b7f7bd19250731d148bdbae1200cb64b08851bd8e28d5f0047d5983273dc4
  ```

- Repeated the construction for the second quotient type and obtained a
  second complete witness with the same independent checks.

  ```text
  text SHA-256
  2e5087308dceb18398daaba4b1ca5868d755cecb41ae7892f988ae8083c03c22

  JSON semantic SHA-256
  2f03cbaaf514b4a90bd4aa7ad7f533b8abd9e0b1fddb724aeb40d718db51465c
  ```

- Resource measurements:

  ```text
  type 1 generation   6.4 s, <49 MB RSS
  type 2 generation   9.8 s, <49 MB RSS
  aggregate replay    <0.2 s
  ```

- Strict conclusion: exact characteristic-two support realization is
  feasible for representatives of both parity types.  These witnesses
  prove only adjacency modulo two, equivalently conference core modulo
  eight.  They do not construct the graph or `H(668)`.
- Downstream carry audit (in the neighboring mod-four checkpoint)
  reports 722 of 1,503 independent mod-four defects for the first witness
  and 764 for the second.  These are initial seeds, not optimized
  mod-four approximations.
- Added an exact secondary carry objective to the fixed-diagonal phase
  walk.  A deterministic 200,000-proposal type-1 run preserved every
  mod-two equation, margin, and trace constraint while lowering the carry
  count from `722/1503` to `672/1503`.  Independent replay splits the
  optimized count as 72 diagonal and 600 off-diagonal defects:

  ```text
  optimized text SHA-256
  bb6d7431ace29949e0af8077afdd7377b7dd3c615832e197562018fe18eee060

  optimized JSON semantic SHA-256
  7d6e7d1827a4129fc12916c3007772511e40bd011f6b5193349029de3522aaae
  ```

  This is an attained seed, not a lower bound or a proof that 672 is
  minimal in the phase fiber.
- No external communication occurred.
