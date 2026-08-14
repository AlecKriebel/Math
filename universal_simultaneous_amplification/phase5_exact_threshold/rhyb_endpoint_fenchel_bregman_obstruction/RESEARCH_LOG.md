# Research log

## 2026-08-13 18:45 PDT — natural endpoint actions

- Restricted the audit to the two proposed endpoint actions and conceptual
  one- and two-state families.  No graph, kernel, parameter, or ansatz search
  was performed.
- Derived both Euler--Lagrange equations and the exact Hessians.
- Proved positive Picone/ground-state representations of both Hessians at the
  active endpoints.
- Found the first structural obstruction: both actions are globally
  nonconvex, already in the homogeneous one-state model, and their homogeneous
  active Hessians fail the inverse-Hessian test for Legendre conjugacy.
- Derived the exact cross stationary remainders.  Each is a genuine scalar
  `Phi`-Bregman node gap minus its kinetic quadratic.
- On the analytic reversible two-state eigenmode tangent, derived exact
  coefficients for `T`, both node Fenchel gaps, and both full variational
  remainders.  Their ratios vary strictly with the kernel eigenvalue.
- Proved exact coefficient-one crossings for each orientation at every
  interior fitness and for the symmetric sum on the closed strip.  Thus the
  direct exact-fixed-representation and coefficient-one routes cannot close
  the support sign.

## Checkpoint assessment

- **Result:** decisive theorem-sized obstruction to the natural
  Fenchel-conjugacy and fixed, kernel-independent scalar Bregman-gap routes.
- **Not proved:** `T>=0`, the endpoint gap, or the exact value of `R_sim`.
- **Estimated completion of this bounded subtask:** 100% after exact replay,
  clean-diff audit, commit, and push.
- **Estimated completion of the surrounding endpoint program:** about 70%.
  The scaled-first upper half is proved, while the lower endpoint sign still
  needs a new coupled estimate.
