# Multiplicativity of tautological Chow projections

Problem **30006276 / OWR-14299284-004**. Result: **unsolved**.

The question concerns the canonical rational projection
CH*(A_g) -> R*(A_g) on the moduli stack of principally polarized abelian
varieties over C. The latest inspected June 2026 primary source retains
the general assertion as a conjecture.

Five substantive routes were completed:

1. Pairing-kernel algebra and a fixed-fibre counterexample to an automatic
   algebraic shortcut
2. Reduction to algebraic cohomology and finite-degree exclusions
3. Nonsimple support and the precise reach of the known Noether-Lefschetz theorem
4. Torelli intersection tests, including five explicit scalar targets for
   self-products in genera 5, 6 and 7
5. A sufficient compact-restriction criterion and its characteristic-p gap

The fixed-fibre counterexample does not concern A_g. The Torelli left-hand
intersection numbers are not computed. The arbitrary-product obstruction
remains unproved. No novelty or full-resolution claim is made.

## Files

- `PROOF.md`: exact target, reductions, proofs of the controls' mathematical
  interpretation, and the remaining gaps
- `SOURCES.md`: primary-source locations and version distinctions
- `RESEARCH_LOG.md`: timestamped five-route record and completion estimates
- `RESULT.json`: machine-readable outcome
- `verify_controls.py`: Python 3.10+ standard-library exact verifier
- `control_results.json`: deterministic output from the verifier

Replay from this directory:

    python3 verify_controls.py > /tmp/chow-projection-controls.json
    diff -u control_results.json /tmp/chow-projection-controls.json
    sha256sum -c SHA256SUMS

The recorded run passes 5,250 exact assertions and enumerates 215,267
nontrivial partitions in the bounded cutoff check. It does not compute a
general Chow ring or certify the conjecture.

Author attribution: Alec Kriebel,
https://orcid.org/0009-0001-9320-500X.
