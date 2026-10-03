# Entanglement testers: final five-turn packet

Problem 30004865, source OWR-8415352-007. **5/5 author turns consumed. Full source bundle: exhausted/scoped partial; no claim that all source questions are solved.**

## Strongest result

TURN_1.md gives a complete negative candidate for completeness of unreshuffled local Schatten-1-to-Hilbert testers. The full-rank entangled two-qutrit state (19I-9F)/144 has optimized tester value exactly one across all allowed local tester pairs. This includes arbitrary unequal finite output dimensions.

## Supporting scoped results

- TURN_2.md: mixed multipartite realignment/SIC incomparability; even-party noisy-GHZ formulas.
- TURN_3.md: exact full complex projective norms for the Schmidt-correlated family.
- TURN_4.md: exact tester norms and detector regions for a noisy/dephased three-qubit GHZ family.
- TURN_5.md: comparison with credited full-separability and biseparability boundaries, with explicit decompositions. Realignment detects entanglement of every genuinely tripartite entangled state in this family, but also detects some biseparable states.

Actual SIC statements retain the existence qualifications in turn 2; explicit qubit comparisons have no such existence gap. The source's unrestricted mixed-state classification, broader quantitative comparison, and output-dimension efficiency agenda remain unresolved.

## Verification

Run with Python 3.10+ and its standard library:

    for n in 1 2 3 4 5; do python verify_turn$n.py; done

All five author scripts pass 507,443 exact assertions. These controls supplement the analytic proofs. SOURCE_SCOPE.md, SOURCE_MANIFEST.json, and SOURCE_ADDITION_T*.json document sources and qualifications. TURN_5_MANIFEST.json binds the frozen review input. Raw third-party sources are omitted from the public checkpoint.

Fresh independent full-packet review is pending. The prior central review was reported favorably but its artifact could not be recovered, and is not substituted for this audit. No result PR has been opened. WIP preservation does not constitute the publication gate. No sixth author search is permitted. See CURRENT_STATE_T5.json and TURN_5_LOG.md for status and administrative recovery limits.
