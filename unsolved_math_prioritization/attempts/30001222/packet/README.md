# Quantum complete intersection rigidity investigation

Target: rank 668, ID 30001222, OWR-3400-006.

**Disposition: unresolved after five substantive approaches.** This packet does not claim a solution, a counterexample satisfying all hypotheses, or mathematical novelty. It is an authored research record awaiting fresh independent audit.

## Results

- The commutative case follows immediately from the center and dimension assumptions.
- Derived-equivalent local finite-dimensional algebras are isomorphic; the missing step is a derived lift of the given stable equivalence.
- Split-local equivalence bimodules satisfy a rank congruence, but stable self-equivalences already show why their image of the simple need not be simple.
- Two explicit 36-dimensional symmetric quantum complete intersections over F11 are nonisomorphic but have isomorphic centers, identical radical layers, and identical HH1 dimensions. No stable equivalence between them is asserted.
- An explicit characteristic-three socle deformation preserves the center and radical layers, but its HH1 dimension changes from 8 to 7. This excludes it as a counterexample of stable Morita type.
- Kessar's established affirmative special case is retained with its algebraic-closedness, characteristic-three, and precise presentation hypotheses.

## Files

- `PROOF_AND_PARTIALS.md`: complete authored statements, proofs, source-scope corrections, and remaining gap.
- `APPROACH_LOG.md`: five distinct attempts and their individual stopping obstructions.
- `LIMITATIONS.md`: exact boundaries of the conclusions.
- `verify.py`, `verification_results.json`: reproducible exact finite-algebra controls.
- `SOURCE_VERIFICATION.json`, `DATA_PROVENANCE.json`: public-source metadata and inspection history, with no source PDFs/text or dataset contents.
- `MANIFEST.json`, `verify_manifest.py`: frozen byte-count and SHA-256 inventory.

## Reproduction

Use Python 3.8 or later with no third-party dependencies:

    python verify.py > replay.json
    cmp replay.json verification_results.json
    python verify_manifest.py

Run replay outside the frozen packet or remove the generated `replay.json` before manifest verification. The test script only prints its results; it makes no network requests or remote changes. The recorded result is 204,097 exact assertions passing. These are arithmetic checks of specific partial results, not 204,097 independent proofs of the general question.

## Primary references

The original question is on printed p.941 of [Oberwolfach Report 17/2009](https://doi.org/10.4171/owr/2009/17). The known special case is [Kessar, Theorem 1.2](https://arxiv.org/abs/1012.0534). The stable-Hochschild obstruction uses [Briggs and Rubio y Degrassi, Theorem 1](https://arxiv.org/abs/2006.13871). Further references and exact scope distinctions appear in the proof and source-verification record.

No remote repository writes were performed in this investigation.
