# Research log: bounded satellite tangent cone

Started: 2026-08-08 (America/Los_Angeles)

No literature search or external contact.

## 2026-08-08: clique satellites

- Derived the exact `K_s` Bd and dB local fixation probabilities directly
  from their count chains.
- Derived the two rare-gate odds and the normalized dilute correction vector.
- **PROVED:** at fitness `3/2`, `K_2` is the only clique satellite which can
  be balanced by dilute hub pendants.  `K_3` and `K_4` fail by positive
  quadratics; every `K_s`, `s>=5`, is already dB-negative.
- Next target: arbitrary connected internal gadgets with uniform weak core
  bundles, followed by asymmetric/nonuniform portal loads.

## 2026-08-08: arbitrary unweighted gadgets through six vertices

- Derived the general uniform-bundle gate formula from the two update rules.
- Enumerated all 142 connected unweighted unlabeled gadgets on two through
  six vertices.  All four singleton fixation vectors per gadget were solved
  exactly over `QQ` from the full subset chain.
- After clearing the positive scale denominator, the necessary separator is
  a quadratic in the common internal scale.  Exact leading/constant signs
  and discriminants prove that `K_2` is the unique gadget in this finite
  catalogue with a positive simultaneous tangent cone.
- This finite theorem does not exclude larger or weighted/asymmetric
  gadgets.  It is a counter-screen and a precise class-optimal result.

## 2026-08-08: weighted and nonuniform-portal screen

- Extended the gate formula to arbitrary positive portal loads `x_i`.
- Differential-evolution searches over every connected three- and
  four-vertex support, varying all internal weights, all portal loads, and
  the common scale, found no positive balanced tangent at `R_*`.
- **NUMERICALLY OBSERVED:** weighted paths and triangles approach zero from
  below only through singular boundary degenerations.  No candidate exceeded
  `R_*`, so there was nothing to exactify.
- This search is hostile evidence only.  Weighted gadgets of arbitrary size
  and more general core couplings remain open.
