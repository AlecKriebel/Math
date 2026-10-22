# Counterexamples to Satoh's SL(2) representation-filtration conjecture

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.
Unrefereed preprint, version 1.0, 15 October 2026. AI tools were used extensively in development, verification, source investigation and writing. Internal AI reviews are not independent human peer review. No independent human peer review has occurred.

The paper proves explicit counterexamples to the equality stated in Satoh's 2018 Oberwolfach report. With A_n(k) defined using the integral free-group lower central series and D_n(k) acting on the whole quotient J/J^(k+1) in the rational SL(2,C) matrix-entry algebra, it proves D_n(5) != A_n(5) for every n >= 4 and D_n(6) != A_n(6) for every n >= 3. The two families together refute universal equality for each rank n >= 3 in that source's range. Degree 5 at rank 3, failure in every degree, SL_m with m > 2, character/trace algebras, and the ordinary lower-central-series conjecture for IA_n are outside the claim. See CLAIM_SCOPE.json and the paper for exact definitions and proof.

The polynomial P is classical. The directly inspected source is Dietrich Burde, *Derivation double Lie algebras*, arXiv:1411.0950v2, equation (4) and Theorem 4.14. Its historical attribution to Razmyslov is reported through that inspected source. Q is a weighted substitution in P. The paper claims neither a new polynomial identity nor a new general PI method. The contribution assessed here is the explicit free-group, augmentation-ideal and automorphism application to the stated equality.

## Reproduce the checks

Extract this ZIP into a dedicated directory with a ZIP extractor that retains regular Unix file modes, then run the following from that directory. Do not place environments, outputs or extra files inside it: integrity verification requires an exact file and directory inventory.

```sh
python3 -I -B verify_package.py
```

This integrity-only command uses the Python standard library. It checks the complete manifest, immutable snapshot/gate/family pins, all 23 original native files (byte size, SHA256, Git blob and 100644 mode), exact claim scope, metadata, author-input visual-QA bindings, and the absence of unknown files, empty directories, symlinks or special files. It does not run mathematical controls.

Exact replays were checked with Python 3.12.14 and SymPy 1.14.0. Prepare an environment outside the extracted tree. If installation must also be offline, provide a local wheelhouse containing SymPy 1.14.0 and its dependencies. Replace the wheelhouse path below with its real location. The verifier itself never accesses the network.

```sh
python3.12 -m venv ../satoh-venv
../satoh-venv/bin/python -m pip install --no-index --find-links /path/to/local-wheelhouse -r requirements.txt
../satoh-venv/bin/python -I -B verify_package.py --replay --selftest
../satoh-venv/bin/python -I -B -O verify_package.py --replay --selftest
```

The expected top-level JSON status is PASS. `--replay` copies the verified packet into a temporary directory and reproduces the frozen native results: 5 author negative controls and 12 original independent negative controls. The native wrapper always runs with assertions enabled; its subprocess environment forces PYTHONOPTIMIZE=0 even if the outer verifier uses -O. The four fresh mathematical/priority controls run in both ordinary and optimized Python and must produce bytes identical to their frozen outputs: 21 matrix/ideal checks; 20 free-group check families including 489 exact integral coefficient-path evaluations; 12 classical-identity/source controls; and 8 component-versus-character scope controls. Native, free-group and scope controls use only the standard library; the matrix and classical controls use the pinned SymPy version.

`--selftest` creates thirty distinct hostile temporary packets and requires their rejection under both ordinary and optimized Python (60 rejections). Cases include altered PDF/code/scope/native controls, recomputed manifest hashes for frozen alterations, stale receipts and QA bindings, malformed or duplicate JSON, nonfinite numbers, unsafe paths, unexpected/missing files, empty directories, symlinks, a FIFO, changed native modes and invalid manifest records. It executes a separately captured trusted verifier against these packets, never their corrupted code. Original and extracted input trees must remain byte-identical, with no added files or bytecode caches.

For a deterministic rebuild from the extracted directory, run:

```sh
../satoh-venv/bin/python -I -B build_package.py
```

The archive and external PACKAGE_BUILD_RECEIPT.json are written to the directory above the extracted package. In the research audit layout they are written beside build_package.py. The builder checks captured input bytes before and after, verifies a staging tree, sorts names, fixes ZIP timestamps to 2026-10-15 00:00:00, uses Unix regular-file mode 100644 and deflate level 9, then replaces prepared outputs atomically. The same source bytes and zlib runtime reproduce the archive bytes. The manifest excludes itself; the archive excludes its own build receipt and mutable implementation/review logs. The builder performs integrity checks only; use the verifier for replays. PDF compilation is separate: the self-contained TeX source is included, and ROOT_PAPER_QA.json binds the four-page PDF that was rendered and visually inspected. Recompiling it with another TeX environment need not produce identical PDF bytes.

## Contents and evidentiary limits

The package contains nine publication inputs, the strict unchanged original 23-file candidate under native/, four independently developed mathematical/priority review families with derivations, source-hash ledgers and frozen executable results, and an explicit set of root snapshot, mathematical/priority acceptance, replay and paper-QA records. Later whole-package reviews and operational helpers/receipts are outside this archive to avoid circular hashing and mixing scientific evidence with publication operations. Raw third-party PDFs, HTML, downloaded API records, extracts, rendered source pages, caches and research temporary files are not redistributed. Source-access receipts contain authored metadata and hashes only; referenced outside raw files are not archive members.

The archive preserves historical reports, including classical-priority finding M1. M1_ATTRIBUTION_REPAIR.json records its repair in the current paper, scope and metadata; this README supplies the same explicit credit. Earlier reports describe the evidence and state at their own timestamps. They do not override the current claim scope or imply publication approval.

The bounded literature audit located no verified older complete application to this exact equality in its inspected sources. It does not certify historical firstness, exhaustive novelty clearance or current openness. Complete final 2017 and 2021 Satoh journal texts and some related 2025/2026 journal full texts remained inaccessible. Public preprints, shorter sources, abstracts and final journal metadata are distinguished in CURRENT_PRIORITY_AND_STATUS.md and the source ledgers; metadata does not establish identical text. These are significant limits on priority conclusions.

An integrity manifest is not a digital signature: replacing the entire packet and verifier can replace its assertions. Compare the archive/PDF hashes with an independently obtained publication record when available. Computation checks supplement the written universal proof; they are not a formal proof or a novelty certificate. The original head is e92320ea5979c812089780a982fbd88136a26522, PR 681, problem 30003703. This package alone is not authorization to publish or merge, and no review in it constitutes human peer review.
