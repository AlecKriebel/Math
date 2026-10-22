# Continuous-time Derrida–Retaux: audited partial results

Problem 30004541 / OWR-2654828-006, rank 754. **Unsolved, budget exhausted (5/5).** No full resolution and no novelty claim.

The full arbitrary-initial-law zero-free-energy characterization and the implication from zero free energy to convergence in probability remain unresolved in this work. The finite-mean stationary-law uniqueness result only gives convergence conditional on existence of a whole-trajectory limit. Tightness and subsequential limits do not close that gap. The pinned Exp(5/2) example refutes a proposed conjunction of initial tests; it is not a counterexample to the original extinction question.

## Mathematical convention

All general-law time differential identities in the frozen author packet are understood almost everywhere, or in their equivalent integral form; the observables concerned are locally absolutely continuous under their stated hypotheses. Deterministic atoms reaching zero can prevent a classical derivative at an isolated time. This wrapper makes the audit's optional precision note explicit without editing the audited bytes.

## What is preserved

- `author/`: the complete, unchanged ten-file author freeze, with six retained partial propositions and five approach records.
- `audit/`: the complete, unchanged nine-file independent audit. PASS is scoped to this no-resolution checkpoint, with no mandatory corrections.
- `frozen_archives/`: canonical base64 encodings of the two exact safe ZIP freezes. They contain only the same authored text, code, and public verification metadata; no source PDFs, extracts, or raw datasets.
- `SOURCE_BINDING.json`: publication-time source and current-record binding, including the precise cache-versus-fresh-read distinction.

Historical statements such as “independent audit pending” or “no remote write” inside the immutable freezes describe their preparation stage. The independent audit and publication-time binding are supplied alongside them. No author or audit file was silently updated. Completion toward the full research goal remains the author's subjective 10% estimate; it is not a probability of proof.

## Reproduce

Use Python 3 and SymPy 1.14.0. From any working directory:

    python /path/to/packet/verify_publication.py
    python /path/to/packet/test_publication_integrity.py

The verifier checks the exact recursive file/directory allowlist and hashes, verifies both archive identities and every archive member, runs both frozen manifest validators, reproduces all 27 author controls, and reproduces the independent audit's 54 named checks, 780 rational-tree cases and seven stationary negative controls. ZIPs are decoded only into a temporary directory. Nothing in the packet is modified. These tests do not certify analytic arguments or solve extinction. The readable proof and independent audit remain essential.

Optional source-gate replay, with complete externally obtained files:

    python /path/to/packet/verify_source_binding.py --catalog /path/catalog.json --problems /path/problems.json --research-results /path/research_results.json

This offline command verifies the pinned complete-file bytes and recomputes the selected statement/review hashes. Source files are deliberately not distributed here.

## Repository change

Only this target row's Status (`queued` to `unsolved`) and Turns (`0/5` to `5/5`) change in QUEUE.md. Every other byte, including Findings, Chat, DOI and the existing stale embedded header, is preserved. This is a reviewable draft PR, with no merge, release, DOI creation or external outreach. The exhausted research budget is recorded here and in the frozen five-approach ledger; no generated catalog/state files are altered.

No hosted-CI pass is claimed. Local portable and relocated replay results are verification evidence, not a substitute for absent hosted checks.
