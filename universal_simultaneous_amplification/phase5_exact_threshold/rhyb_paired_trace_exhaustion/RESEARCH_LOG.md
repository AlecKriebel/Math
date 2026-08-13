# Research log: paired Schur-trace exhaustion

## 2026-08-13 15:09 PDT

- Began a proof-first audit of the global endpoint compactness obligation.
- Read the exact-threshold state, BDM reduction, paired trace-cone lift,
  neutral pair Schur decomposition, separated cone normal form, and the new
  minimal-product-to-BDM weak-core lift.
- Identified that weak-* compactness of separated module measures is not
  required once BDM supplies the common affine support
  `D+(r-1)B<=0`: it can be integrated at each finite stage.
- Isolated the exact residual object.  If
  `Delta=int v dmu+tau` with common physical coefficients, every
  simultaneous amplifier forces
  `L(tau)>=(r-1)epsilon+int g dmu` and hence
  `||tau||_infty>=(r-1)epsilon/r`.
- Lifted the standard Schur identity directly to the finite-fitness
  fixation committor.  Its retained load is exactly the probability of
  starting in, or hitting, the unresolved trace before absorption.
- Derived the quantitative event alternative
  `beta_D+(r-1)beta_B >= (r-1)epsilon-o(epsilon)`.
- No theorem has yet been committed.  The note awaits hostile audit.

## 2026-08-13 15:24 PDT

- Hostile audit accepted the conditional reduction and committor estimate.
- Made explicit that the initial Schur load is normalized (or divided by
  its mass), the complete-baseline normalization is rule-specific, and the
  Bd/dB retained sets may differ.  Only the already separated packet
  coefficients must remain physically common.
