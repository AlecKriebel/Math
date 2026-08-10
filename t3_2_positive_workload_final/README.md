# T3-2 positive-workload final repair

This directory is an adversarial repair workspace for the proposed theorem
that every finite bimolecular weakly reversible stochastic mass-action network
with at most three dynamically active species and at most two active linkage
classes is positive recurrent on each closed communicating class.

The inherited candidate release is preserved under `inherited/`. Its finite
atlas and local aggregate-debt calculation remain useful, but its global
certification claim is withdrawn while the tight-environment and
trace-to-physical-time interfaces are reworked.

The active research record is `RESEARCH_LOG.md`; the current certification
state is `STATUS.md`. Three new exact-scope physical-time results are recorded
in `research_notes/certified_exact_shielded_seam.md`,
`research_notes/signed_service_seam_full_proof.md`, and
`research_notes/residual_pair_full_proof.md`. The remaining support interface
and its twelve canonical asymptotic gates are recorded in
`research_notes/global_atlas_interface_closure.md`.
The certified classwise affine filter is in
`research_notes/stoichiometric_gate_feasibility.md`. The current one-active
stopped-kernel gap and the exact two-/three-active structural decompositions
are recorded in `research_notes/one_active_physical_phase_theorem.md`,
`research_notes/two_active_promotion_phase.md`, and the accompanying finite
certificates; none of those structural decompositions is itself a global
recurrence theorem.
The only classwise interpretation of “dynamically active” compatible with
the inherited three-coordinate atlas is stated in
`research_notes/classwise_scope_reduction.md`.

## Read-only finite replay

The current recurrence-interface regressions, exact finite algebra, and global
support/tier certificates can
be replayed without external packages or writes to the project:

```bash
python3 -I -B verify_read_only.py
```

See `RELEASE_ENGINEERING.md` for their exact scope and the final-release
requirements. Passing these tests does not computationally certify the
analytic physical-time proofs, and it is not a T3-2 certification.
