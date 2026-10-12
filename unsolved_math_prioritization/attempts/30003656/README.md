# Wraith redundancy for algebraic theories

**Problem:** 30003656 / OWR-15958-003, rank 506 at the start of this investigation.
**Author-stage result:** a complete candidate negative answer to the explicit, consequence-based question, pending independent audit. **No historical-priority claim.**

Take the one-sorted algebraic theory of a pointed object, with its sole constant c. The sentence

    α = ¬∀x ¬¬(x=c)

adds no geometric consequences to the theory, but the generic pointed object forces its negation. The proof compares finite pointed sets with all pointed maps against the same objects with only pointed injections. Restriction is conservative and preserves geometric interpretation. Two direct forcing calculations give opposite truth values; a second finite-equality-quotient argument independently establishes the needed geometric completeness.

## Files

- `PROOF.md`: full definitions, theorem, proofs, convention checks, source-scope caveat.
- `SOURCE_GATE.md`: primary-source and bounded literature checks, duplicate checks, precise publication caveats.
- `RESEARCH_LOG.md`: two substantive approaches, validation work, completion estimates, and remaining review issues.
- `check_exact.py` and `exact_results.json`: executable finite forcing and equality-quotient sanity checks.
- `FROZEN_AUTHOR_MANIFEST.json`: SHA-256 hashes of the frozen author package.

Run the checks with Python 3:

    python check_exact.py

The checks enumerate 1,279 pointed maps and 89 pointed injections on five finite objects, plus 64 finite equality-premise sets and 1,024 atomic-consequence comparisons. They all pass. They are not a finite substitute for the unbounded category-theoretic proof.

## Scope warning

The literal Wraith question is already known to have elementary excluded-middle counterexamples; Blechschmidt explicitly records that warning. The present sentence is not classically valid and the conservativity argument is constructive, but this does not establish novelty or identify every refinement an author might intend. The independent audit must check both the mathematics and whether an extra condition omitted from the displayed source question changes its intended scope. Nothing is represented as independently verified or first solved here.
