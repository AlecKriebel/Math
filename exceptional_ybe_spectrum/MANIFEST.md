# Version 1.0.1 release manifest

## Primary paper

- `output/pdf/exceptional_ybe_constraints.pdf` — typeset 20-page paper
- `manuscript/main.tex` — complete TeX source
- `build_paper.sh` — deterministic Tectonic build wrapper

## Logical and verification maps

- `manuscript/THEOREM_DEPENDENCIES.md` — theorem dependency graph and
  scope guards
- `manuscript/VERIFIER_MANIFEST.md` — central exact verifier inventory
- `manuscript/SUPPLEMENT.md` — scoped ansatz results, limitation models,
  and numerical-only evidence
- `verifiers/run_frontier_paper_verifiers.py` — read-only central suite
- `results/frontier_paper_verifier_suite_exact.txt` — retained 10/10
  passing transcript

## Audits and provenance

- `PRIORITY_AUDIT.md` — literature and novelty audit
- `reviews/manuscript_final_hostile_audit.md` — final independent
  adversarial proof audit and repair record
- `reviews/v1.0.1_correction_audit.md` — independent review of the
  correction release
- `CLAIMS.md` — claim-status ledger
- `LEMMA_DEPENDENCIES.md` — full research dependency ledger
- `EXPERIMENTS.md` — commands, seeds, environment, and outputs
- `FAILED_APPROACHES.md` — retained unsuccessful approaches
- `RESEARCH_LOG.md` — timestamped research history
- `RELEASE_NOTES_v1.0.0.md` — preserved history of the original release
- `RELEASE_NOTES_v1.0.1.md` — correction-release notes

## Reproduction

- `requirements.txt` — central suite's third-party dependency
- `scripts/` — discovery and exact calculation programs
- `verifiers/` — independent exact replays
- `results/` — retained raw outputs and search archives
- `notes/` — human derivations and scoped theorem statements

`tmp/` and downloaded literature under `tmp_literature/` are not release
artifacts.
