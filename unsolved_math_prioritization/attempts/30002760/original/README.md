# Adaptive transport-diffusion: qualified partial results

**Problem 30002760 / OWR-13487-001; rank 990. Original broad target unresolved after five distinct author approaches. Independent review pending.**

The important positive literature result is the 2019 Erath-Praetorius stationary SUPG optimal-rate theorem. Its exact scope is preserved in [SOURCE_SCOPE.md](SOURCE_SCOPE.md). A general negative answer, a full parabolic resolution, and a parameter-uniform preasymptotic theorem are not established here. The source itself is a broad research question and does not specify every algorithmic or norm convention.

## Results and exact boundaries

1. [Fixed-space Galerkin analysis](TURN_1.md): a classical quasi-optimality transfer and an exact, smooth single-element quadratic example with squared amplification 1+1/(60 epsilon^2). This only disproves an epsilon-uniform same-space bound for that coarse unstabilized scheme.
2. [Optimal-test minimization](TURN_2.md): an ideal residual isometry; finite-test same-space stability; a certified-tail condition; and an exact stable-trial, zero-restricted-residual blind spot. Computational realization and mesh-rate selection remain separate.
3. [Global mesh selection](TURN_3.md): a conditional nested-overlay rate theorem for certified comparators, with a proof that literal dyadic-tree enumeration is exponential. It does not supply the required comparator or efficient algorithm.
4. [Local marking](TURN_4.md): a complete conditional optimal-rate proof from stated discrete reliability, stability, overlay, closure and R-linear convergence assumptions. A scalar sequence shows why merely converging indicators do not replace contraction. Those robust PDE assumptions are not newly proved.
5. [Parabolic transfer](TURN_5.md): an energy residual estimate, optimal independent-budget allocation by Hölder, and a genuine fixed-time-step obstruction despite exact spatial solves. Joint space-time optimality remains open in this attempt.

These are classical-method reconstructions and scoped diagnostics. No historical novelty, formal proof verification, human peer review, or complete-resolution claim is made. OpenAI tools assisted the research, derivation, writing and checks.

## Replay

Use Python 3's standard library only, from this directory:

- `python verify_math.py` reproduces CHECK_RESULTS.json: 37,329 exact finite controls.
- `python test_fail_closed.py` reproduces FAIL_CLOSED_RESULTS.json. Normal Python, -O and -OO all reproduce the correct output and reject 30 deliberately false claim cases, nine incorrect-computation cases and nine malformed/unsupported-claim cases across those modes.
- `python verify_packet.py` checks the strict file allowlist, lengths, SHA-256 bindings, absence of optimizable assertion statements, all saved receipts and the negative controls. `python test_integrity.py` also reproduces INTEGRITY_RESULTS.json: 24 rejected byte, allowlist and manifest-schema mutations across the same three Python modes. An explicit `--integrity-only` run checks bytes only and reports that narrower scope.

All validation conditions use explicit failures; Python optimization cannot remove them. Finite checks support the written proofs and do not certify infinite-dimensional hypotheses or completeness of the literature search. The packet replay intentionally does not fetch external source documents.

## Provenance and publication boundary

[ATTEMPT_LEDGER.json](ATTEMPT_LEDGER.json) records the chronological author approaches; source searches, duplicate checks, validation and packaging are not additional approaches. [PRIOR_ATTEMPT_GATE.md](PRIOR_ATTEMPT_GATE.md) states the checked repository coverage and limitations. [SOURCE_METADATA.json](SOURCE_METADATA.json) records source identities and actual inspection scope.

This directory contains authored mathematics, verification programs and public provenance metadata only. It contains no source PDFs, extracted source text, screenshots, corpus records, or private coordination. FROZEN_MANIFEST.json binds all other files. Keep its externally recorded digest when reviewing the frozen packet; a manifest cannot authenticate itself.

Recommended queue disposition if this packet is later accepted: `unsolved`, `5/5`, with the substantial existing stationary theorem and the unresolved broad scope made clear. No queue file or remote repository was changed by this author task.
