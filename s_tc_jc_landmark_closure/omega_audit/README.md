# Exact bounded Omega audit

This directory contains the one permitted audit of the immutable historical
Omega pair.  Its terminal disposition is `OMEGA-PASS-ALL-(n)`; see
`reports/OMEGA_GATE_REPORT.md`.

- `frozen_input/`: immutable historical certificate, original verifier, and
  prior clean-room audit inputs, with SHA-256 manifest.
- `independent/verify_omega_release.py`: active clean-room release verifier.
- `independent/output/omega_release_audit.json`: complete rooting, topology,
  stochastic, rank, propagation, and mutation record.
- `transcripts/`: exact primary and independent replay output.

The audit contains no Omega-chain search, modified gadget, alternative
labelling census, or richer-model calculation.
