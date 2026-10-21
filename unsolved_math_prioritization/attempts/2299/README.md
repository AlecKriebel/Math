# Erdős 776: acceptance of an existing threshold result

Row 1869, ID 2299. Intended workflow classification: `already_solved`, one turn. This local package makes no novelty claim and changes neither the queue nor any remote repository.

The accepted, explicitly corrected argument gives n0(r)=2r+4 for 4≤r≤10 and n0(r)=2r+5 for r≥11. The convention is strict n>N. Read `audit/THRESHOLD_ACCEPTANCE.md` for the complete acceptance boundary, including the Section 6 isolated-run shadow-index correction; the inspected Lean uses the full state and avoids that typo. The r=2,3 cases remain attributed to He–Tang and outside this audit.

## Trust boundary

No local Lean compilation or `#print axioms` occurred. An external CI record reports successful build and axiom-audit steps, but job-log retrieval returned HTTP 410 and the actual axiom output was not inspected. Bounded `native_decide` computations add compiler/evaluator trust; the full result must not be described as pure kernel reduction. The live official moderation status is unverified. The source gate predates the authored mathematical acceptance and must not be read as a subsequent rejection of that acceptance.

Included content is authored analysis, independently authored arithmetic, its output, and public source identities/hashes/inspection metadata. No third-party source programs, PDFs, dataset contents, private corpus, or coordination material are included. The source manifest names public upstream files only; their names do not imply those files are bundled. Its hashes are provenance, not a fresh retrieval or verification of upstream availability.

## Offline reproduction

Run `python3 -B validate.py` and `python3 -B -O validate.py` from this directory. Python 3's standard library suffices; no network, source checkout, external package, or Lean installation is used. The validator checks the exact recursive inventory before executing the included authored arithmetic, and reruns arithmetic in both normal and optimized modes against the preserved reference JSON. Every mathematical check in the arithmetic remains active under optimization. All original asserts were mechanically replaced by explicit exceptions; original input hashes and the transformation are recorded in `PROVENANCE.json`.

`logs/validation_normal.log`, `logs/validation_optimized.log`, and `logs/negative_controls.log` retain complete output of package tests. These tests preceded final log inclusion and receipt freezing; the final receipt inventories their exact bytes. Negative controls check missing/altered/unexpected files, unexpected empty directory, nested symlink, file symlink, FIFO, and failed arithmetic checks under optimization. These are integrity tests, not adversarial sandboxing or a mathematical proof of the symbolic theorem.

`FROZEN_RECEIPT.json` inventories every regular file except itself and all directories, recursively. It rejects additions as well as deletions/changes. The receipt cannot hash itself; its SHA-256 must be retained externally to detect replacement of both receipt and contents. This is a frozen integrity snapshot, not a signature or tamper-proof provenance system. Concurrent hostile filesystem mutation is outside scope. Do not regenerate the receipt to conceal changes; create a separately identified revision instead.
