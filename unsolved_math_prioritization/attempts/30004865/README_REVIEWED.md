# Reviewed entanglement-tester results: current entrypoint

Problem 30004865 / OWR-8415352-007. **Five of five author turns consumed. Full source bundle: exhausted/scoped partial.**

## Current mathematical disposition

The fresh independent full audit gives **PASS for the stated mathematics**, with an additive scope clarification required before publication. Read [PUBLICATION_SCOPE_CLARIFICATION.md](PUBLICATION_SCOPE_CLARIFICATION.md) before interpreting the input operations covered by the theorem. In particular, local-transpose precomposition is included in the universal tester bound; nonlocal reshufflings and regroupings are excluded.

The central completeness question has a complete, independently validated negative answer: the full-rank entangled two-qutrit state (19I-9F)/144 has optimized value exactly one over all complex-linear local Schatten-1-to-Hilbert contractions on the original matrix-factor partition. Arbitrary unequal finite output dimensions are covered.

The independent review also validates the specifically scoped supporting results in TURN_2.md through TURN_5.md: multipartite fixed-test incomparability, Schmidt-correlated and noisy-GHZ norm formulas, and the three-qubit detector/separability comparison. Those are full complex individual-factor projective norms. Detection requires a value strictly greater than one. Actual SIC results retain existence qualifications outside the explicit qubit examples. Non-full-separability remains distinct from genuine multipartite entanglement. Realignment detects every genuinely tripartite entangled state in the specified GHZ family, but also detects some biseparable states. The prior results retain their attribution, and this packet makes no novelty-certification claim. The convex-mixture parameter in TURN_2.md's eta_p example is 0<=p<=1.

The unrestricted mixed-state classification, broader quantitative comparison, and output-dimension/computational-efficiency trade-off remain unresolved. No sixth author search is authorized.

## Review and reproducibility

- [Full independent review](review_independent_20261003/REVIEW.md), including exact defensible scope and section 9 presentation safeguards
- [Review metadata](review_independent_20261003/AUDIT_METADATA.json) and [frozen review manifest](review_independent_20261003/REVIEW_MANIFEST.json)
- [Original frozen author manifest](TURN_5_MANIFEST.json), preserved unchanged
- [Current administrative disposition](REVIEWED_DISPOSITION.json) and [additive package manifest](REVIEWED_PACKAGE_MANIFEST.json)

The reviewer independently reproduced all five author scripts and their 507,443 exact assertions with byte-identical outputs. Its additional check script passed 3,778 symbolic, exact and numerical audit assertions, with numerical controls explicitly labeled. Universal statements rest on the analytic proofs, not finite sample counts.

## Historical labels and publication gate

This current entrypoint supersedes the unrecovered historical-review provenance in TURN_3.md and CURRENT_STATE_T2.json through CURRENT_STATE_T4.json, and the then-pending fresh-review labels in README_CURRENT.md and CURRENT_STATE_T5.json. Those frozen files remain unchanged as chronology. The fresh audit was performed independently and did not use the unavailable earlier favorable review as evidence.

This is additive administrative packaging after the five author turns, not a new proof attempt. All original author and review bytes remain intact. The new clarification and administrative rebind still require the reviewer's narrow verification, followed by the parent's publication gate. No result PR has been opened. This checkpoint does not itself authorize a PR, merge, release, or deployment. Raw third-party sources and private source screenshots are excluded.
