# Entanglement testers: reviewed scoped results

Problem 30004865 / OWR-8415352-007. **Full source bundle remains unsolved: exhausted/scoped partial, 5/5 author turns consumed.** This is the current publication entrypoint; the earlier entrypoints and dispositions are preserved checkpoint history.

## Central result

The complete negative answer to the central all-local-tester completeness question has passed a fresh independent full mathematical audit. On two qutrits the full-rank entangled state

    rho = (19 I - 9 F)/144

(where F swaps the two qutrit factors) has optimized tester value exactly one over all complex-linear local Schatten-1-to-Hilbert contractions, with arbitrary unequal finite output dimensions. [TURN_1.md](TURN_1.md) proves the stronger Werner-interval result.

The theorem fixes the original local matrix-factor partition. Read the binding [scope clarification](PUBLICATION_SCOPE_CLARIFICATION.md): local-transpose precomposition is included, while added nonlocal input-index reshufflings and regroupings are excluded. This clarification changes no theorem, proof, turn count, or scoped-partial status.

## Supporting results and remaining questions

The independently audited supporting results are mixed multipartite realignment/SIC incomparability, exact Schmidt-correlated and specified noisy-GHZ norm formulas, and a three-qubit detector/separability comparison. See the [reviewed summary](README_REVIEWED.md) and [full review's exact claim scope](review_independent_20261003/REVIEW.md#2-exact-defensible-claim-scope). These are full complex individual-factor projective norms and strict detection above one. Actual SIC existence remains conditional outside the explicit qubit examples. Non-full-separability is distinct from genuine multipartite entanglement; realignment detects every genuinely tripartite entangled state in the specified GHZ family but also detects some biseparable states. Established separability results retain their attribution. No historical novelty certification is claimed.

Unrestricted mixed-state detection classification, broader quantitative comparison, and the output-dimension/computational-efficiency trade-off remain unresolved. The source-wide queue entry is therefore unsolved at 5/5. There is no sixth author search.

## Independent review and replay

- [Fresh full mathematical audit: PASS](review_independent_20261003/REVIEW.md)
- [Narrow scope/packaging verification: PASS, with replay instructions](review_additive_20261003/NARROW_REVIEW.md)
- [Narrow verification receipt](review_additive_20261003/NARROW_REVIEW_RECEIPT.json) and [frozen narrow manifest](review_additive_20261003/NARROW_REVIEW_MANIFEST.json)
- [Current publication disposition](PUBLICATION_DISPOSITION.json) and [complete publication manifest](PUBLICATION_MANIFEST.json)

The full audit reproduced all five author programs and their 507,443 exact assertions with byte-identical outputs, and passed 3,778 additional independent assertions, with numerical controls clearly labeled. Finite control counts supplement, rather than replace, the analytic proofs. The unavailable earlier historical review was not used as evidence.

The five standard-library author scripts run directly from this directory:

    for n in 1 2 3 4 5; do python verify_turn$n.py; done

The independent audit additionally binds nine source files. Its portable replay, with NumPy and SymPy available, is:

    python review_additive_20261003/replay_independent_review.py --attempt . --sources /path/to/manifest-bound-sources

The source-manifest URLs and SHA-256 hashes identify the required editions. Source files are obtained separately and are not redistributed here. Omitting --sources produces exit code 2, **NOT_RUN_MISSING_SOURCES**, and independent_audit_run=false with the missing-file list. This is explicitly not a pass. See the separately recorded [with-source PASS](review_additive_20261003/REPLAY_WITH_SOURCES.json) and [source-absent NOT_RUN](review_additive_20261003/REPLAY_WITHOUT_SOURCES.json).

## Preservation and administration

The original [author manifest](TURN_5_MANIFEST.json), [full-review manifest](review_independent_20261003/REVIEW_MANIFEST.json), [additive-package manifest](REVIEWED_PACKAGE_MANIFEST.json), and all their bound files remain unchanged. The new narrow-review packet and this publication entrypoint are additive. Historical pending-review labels are superseded by the two successful current reviews linked above. The parent publication gate was approved after both reviews.

The publication branch is based on current main. Outside this problem's attempt directory, only its existing QUEUE.md status and turn cells change, from queued / 0/5 to unsolved / 5/5. No queue generator or global-state replay was run. Raw PDFs, source screenshots, private source material, merges and releases are excluded.
