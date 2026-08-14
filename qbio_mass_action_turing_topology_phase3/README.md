# Phase III: adversarial validation of the mass-action stationary-Turing decision theorem

This directory is the independent validation and publication-hardening record for the candidate theorem developed in the frozen T-ALG archive. The historical STOP archive and the inherited T-ALG archive are copied under `frozen_inputs/` and verified against their inherited SHA-256 values. They are never edited by the Phase III scripts.

## Outcome

**VALIDATED-TALG.** Every load-bearing mathematical claim was reconstructed from definitions, checked by an implementation that imports no inherited project code, attacked by exact bounded enumeration and random rational falsification, and compared with the closest literature located through August 13, 2026. No publication-significant strengthening reached proof, so the theorem was not upgraded.

The validation outcome is an internal mathematical audit, not peer review. Three concise specialist inquiries are prepared under `priority_audit/expert_questions.md` but were not sent automatically.

## Primary artifacts

- `manuscript/main.pdf`: submission-grade journal manuscript.
- `manuscript/supplement.pdf`: independent proofs, validation record, and exact software scope.
- `external_audit/theorem_summary.pdf`: two-page theorem summary.
- `external_audit/proof_skeleton.pdf`: five-page proof skeleton.
- `release/FINAL_REPORT.md`: formal Phase III outcome.
- `release/one_command_replay.sh`: complete independent replay.
- `CLAIM_LEDGER.md`: claim-by-claim audit status.
- `DEPENDENCY_GRAPH.md`: proof dependency structure.

## Replay

```bash
cd /mnt/data/qbio_mass_action_turing_topology_phase3
bash release/one_command_replay.sh
```

The replay verifies the frozen inputs, runs the independent exact tests and red-team campaigns, rebuilds all four PDFs, checks page counts and references, audits the required tree, and regenerates `release/sha256_manifest.txt`.

## Scope discipline

The theorem concerns existence of a nonzero mode with a strictly positive real eigenvalue after positive all-species diagonal diffusion, while the homogeneous mass-action equilibrium is stable relative to its stoichiometric class. It does not require that stationary loss of stability occurs first, that the crossing is simple or transverse, that wave instability is absent, or that a nonlinear patterned state exists.
