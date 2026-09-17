# Second-family residual annihilation

Checkpoint: 2026-09-17T13:29:49.520623+00:00. Completion estimate: **100% of the assigned new-module proof and local validation scope**. This is not a claim that the revised full package, root import, inventory, or archive has been rebuilt.

## Scope and manuscript correspondence

Read the independent review's REPAIR_PLAN.md, operator_review.md and permutation_review.md, then the canonical manuscript's second-family functional, eq:second-sos and thm:second (main.tex lines 915–1015). The review identified a missing explicit all-dimensional residual-zero endpoint, not an error in the existing attainment proof.

The sole proof-source addition is `lean_formalization/CyclicBell/GeneralSecondResiduals.lean`, importing the existing GeneralSecondWitness module. No existing Lean module, umbrella import, inventory, documentation, manuscript or script was edited. No root build, commit, push or outreach was performed.

The main theorem quantifies every dimension d≥2, every permutation κ of ZMod d, and every index l in ZMod d. Its conclusion is literally

```
applyOp (d * generalLambda l • I -
  kron (encoded ((secondPermutationStrategy hd κ).alice l))
    (secondFourier (fun y => encoded ((secondPermutationStrategy hd κ).bob (some y))) l))
  (maximallyEntangled d) = 0
```

Here d*lambda is a complex scalar, I is the identity on the actual joint space indexed by ZMod d × ZMod d, and applyOp is actual matrix action. This is the vector annihilation asserted after the manuscript's Fourier compression, not just zero expectation, scalar attainment, or an abstract existence statement. The supplied permutation strategy is unchanged, including the no-adjoint Fourier convention. The l=0 case and d=2 boundary are included.

## Proof mechanism and new declarations

1. `CyclicBell.General.phi_unitary_conjugate_invariance`: for every nonzero d and actual unitary matrix A, `(A tensor entryConjugate A) Phi_d = Phi_d`. The proof uses the existing vectorization identity phi_apply and A*A†=I. It explicitly uses entrywise conjugation, not an adjoint in the second tensor factor.
2. `CyclicBell.General.secondPermutation_residual_zero`: instantiate the preceding vector identity at the actual encoded secondAlice PVM; simplify its entrywise conjugation twice; use `secondPermutation_compression` to rewrite Bhat_l as `d lambda_l D_l`; factor out the scalar and subtract equal vectors. The proof does not invoke secondPermutation_attains, maximality, a Bell-value equality assumption, or an assumed residual condition.
3. `CyclicBell.General.secondPermutation_aligned_residual_zero`: the actual extra factor `I - kron(A_0,B_none)` annihilates Phi_d. Existing encoding theorems identify both A_0 and B_none with the real cyclic shift X, and the same unitary vector identity proves the result. The manuscript explicitly asserts reduced SOS-factor annihilation and augmented value d+1; this additional vector statement supplies the aligned factor supporting that augmented saturation.

All unitarity needed at the physical endpoints comes from encoded_unitary applied to the already constructed complete PVM. No unitarity, coefficient normalization or maximality premise was added to either physical endpoint.

## Validation

Used PATH prefixed by `~/.elan/bin` and the project environment. The direct command

```
lake env lean CyclicBell/GeneralSecondResiduals.lean
```

completed with exit code 0 and no output, including a recorded repeat after the first successful compile. No project-wide build was run. Compiler: Lean 4.19.0, exact commit `6caaee842e9495688c1567e78c0e68dbb96942aa`.

A separate local audit file contains the exact new source plus #print axioms queries for all three declarations. It also compiles with exit code 0. Each declaration depends only on `propext`, `Classical.choice`, and `Quot.sound`; there is no sorryAx or custom axiom dependency. The new source contains no sorry, admit, axiom declaration or native-decide shortcut.

Artifacts in this folder:

- `second_residuals_validation.json`: exact commands, start times, exit codes and new-source SHA-256.
- `second_residuals_compile.log`: empty successful direct compiler output.
- `second_residuals_lean_version.log` and `second_residuals_lean_githash.log`: pinned compiler identity.
- `SecondResidualsAxiomCheck.lean` and `second_residuals_axioms.log`: exact-source axiom-query evidence.

New module SHA-256: `2d39ed961e289683acafcdc24f557fdfee7233bd27e6c4ba0ad4f409e1c8db23`.

The coordinating agent still owns root import, inventory/manifest updates, full clean validation and repacking. The three fully qualified names above are the complete new declaration list for that integration.
