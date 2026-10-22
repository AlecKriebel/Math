# Review check receipts and replay scope

All authored check code is standard-library Python. Run from any directory with `python3 -B CHECKS/<name>.py`. Scripts derive the original publication directory from this review folder. All fixture writes/extractions are confined to this review's ignored `temp/`; primary-source retrieval writes only ignored `sources/`. No script runs a Git/GWS/gh mutation or contacts a person.

- `artifact_replay.py`: fresh extraction, exact input/member/nested-manifest checks, extracted verifier under normal/-O/-OO. It replaces only this review's temporary extraction and updates its own receipts/log; publication input must remain the bound version.
- `corruption_controls.py`: eight actual altered-archive controls, including root-rebound nested and semantic cases. Requires `artifact_replay.py` extraction.
- `independent_algebra.py`: independent Fraction-pair ring oracle; 96 recursion cases,80 radial cases and three executed altered algorithms. It imports no candidate program and proves no infinite property.
- `workflow_guards.py`:17 ordinary guard/recovery cases against isolated fixtures. Every possible external operation is stubbed or forbidden. Its synthetic row/DOI receipts are offline examples, never publication receipts.
- `stale_pr_retry.py`: adverse reproduction of F1. It expects the reviewed vulnerable code to accept stale saved data. After a repair it should stop at the newly added rejection, so it is a reproduction helper, not an unchanged positive regression assertion. Git/PR APIs are completely stubbed, and no real commit/tree is created or read.
- `public_metadata_scope.py`: adverse reproduction of F2. It expects the reviewed checker to accept changed non-title metadata. After a repair it should stop at the newly added rejection. All fetched responses are in-memory fixtures.
- `primary_sources.py`: fresh read-only retrieval of three decisive PDFs, two version records and two DOI metadata records; extracted/rendered source bodies remain ignored. This authenticates current source responses and precisely recorded inspection scope, not historical byte identity or all proofs.

`ANALYTIC_REVIEW.md` gives the independent analytic checks. `INPUT_BINDINGS.json` binds15 supplied publication inputs. `FINAL_INPUT_DRIFT.json` confirms they remained unchanged. `REVIEW_FREEZE.json` binds this review's authored outputs except itself and source/temp bodies. No prior whole-package verdict was read.
