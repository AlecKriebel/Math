# Adversarial review of the K2P analytic and restoration layers

This directory is an independent, fail-closed review of
`work/bridge_marginal_closure` and of the logical implication that connects
that analytic layer to `work/restoration_forest`.

The review is deliberately separate from both primary workspaces.  It checks
the bridge action, stabilizers, tree holonomy, the principal-domain serial
section, simultaneous gluing in the principal and continuous-time domains,
and the restoration logic.  It also binds the pointwise directional topology
theorem, audits omitted-role probe coverage, and preserves an exact
counterexample to an unconditional lift from a selected marginal relation.

The bridge/marginal/gluing layer passes after its physical local-product and
fixed-full repairs.  The separately discovered dummy-bearing cycle gate is now
closed by the promotion package in `work/cycle_three_port_closure`.  Global
promotion remains fail-closed here until the all-primitive coherent-probe
package is independently replayed and bound into the theorem.

Run:

```text
.venv/bin/python work/adversarial_proof_review/verify_adversarial.py \
  --output work/adversarial_proof_review/audit_certificate.json
.venv/bin/python work/adversarial_proof_review/test_mutations.py \
  --output work/adversarial_proof_review/mutation_certificate.json
```

Add `--require-pass` to the first command when this review is used as a
promotion gate.  It exits nonzero while any load-bearing blocker remains.

The cycle package has its own complete commands and mutation suite in
`work/cycle_three_port_closure/README.md`.
