# Low-exponent free arrangements: candidate proof and exact checks

Status: **claimed_solved**, pending independent review.

This packet proposes a complete characteristic-zero proof of the conjecture attached to UnsolvedMath numeric ID **30004609**, source code **OWR-4990374-015**. It does not assert established novelty, peer review, or independent verification.

## Result

A finite central free arrangement over a characteristic-zero field, with nonzero exponents consisting of 1s and 2s and at most one 3, is supersolvable. Products and nonessential arrangements are included. Multiarrangements and arbitrary-characteristic generalizations are not claimed.

The argument uses standard factorization and formality theorems. The new proposed mechanism is a classification of the incidence graph of rank-two relations: a tree, a tree with a unique four-point pencil, or a single K4 relation core with trees attached. Terminal-pencil removal produces modular flats.

- `PROOF.md`: full candidate, all hypotheses, reductions, and modular-extension argument.
- `check.py`: exact rational/symbolic diagnostic computations.
- `RESULTS.json`: deterministic output of the checker.
- `SOURCE_AUDIT.md`: target matching, primary-source status correction, and bounded novelty check.
- `RESEARCH_LOG.md`: attempts, checkpoints, and explicit budget stopping condition.
- `SOURCE_METADATA.json`: public-source hashes, byte counts, and retrieval/inspection history; no source text or dataset records.
- `STATUS.json`: machine-readable scope and candidate status.

## Reproduce

Run `python check.py` from this directory with Python 3 and SymPy 1.14.0 available. Output should equal `RESULTS.json`. The lattice, graph, and finite enumeration routines use only the standard library. SymPy is used for the Saito determinant, tangency substitutions, and degree-one derivation equations. No network or dataset input is required.

The checks are finite diagnostics, not a computational proof of the all-ranks claim. The proof is in `PROOF.md`.

The test suite covers 11 explicit configurations, including rank-six trees and K4 attachments, a reducible product, nonessentialization, the historical withdrawal example, and the nonsupersolvable non-Fano boundary with two cubic exponents. It also checks 1,716 six-subsets of a fixed 13-point rational pool and 4,845 four-triple supports.

## Important bibliographic correction

The source manuscript arXiv:1707.07091 was withdrawn in January 2022. Its public notice flags gaps in the small-rank case enumeration and the inductively-free proof. This packet does not reuse those results as established premises. The withdrawal example is supersolvable and is a counterexample to an inference in the earlier proof, not to the conjecture.

No scholarly PDF, downloaded full text, raw dataset record, private source, or private coordination file is included here. No merge, release, DOI, or outside communication is requested by this packet.
