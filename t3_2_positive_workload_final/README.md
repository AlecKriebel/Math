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
state is `STATUS.md`. The former smallest seam is now proved at its exact
scope in `research_notes/certified_exact_shielded_seam.md`. The next exact
gate is recorded in `research_notes/remaining_fast_phase_corrector.md`.
The only classwise interpretation of “dynamically active” compatible with
the inherited three-coordinate atlas is stated in
`research_notes/classwise_scope_reduction.md`.

## Read-only finite replay

The current recurrence-interface regressions and exact-seam finite algebra can
be replayed without external packages or writes to the project:

```bash
python3 -I -B verify_read_only.py
```

See `RELEASE_ENGINEERING.md` for their exact scope and the final-release
requirements. Passing these tests does not computationally certify the
analytic exact-seam proof, and it is not a T3-2 certification.
