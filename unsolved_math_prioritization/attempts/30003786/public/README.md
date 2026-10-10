# Embedding dependence of congruence subgroups

**Problem:** 30003786 / OWR-16160-016, queue rank 440.  
**Result:** complete counterexample candidate for the unrestricted abstract-group formulation.  
**Author attempts:** 1/5. **Review status:** awaiting fresh independent audit.  
**Date:** 2026-10-03 UTC.

There are two faithful embeddings of the same free group G into the same SL_7(Z) whose congruence-subgroup families differ. An index-five subgroup H is the principal level-two subgroup under one embedding and is not congruence under the other.

The first 2-by-2 block uses the classical free matrices A = [[1,2],[0,1]] and B = [[1,0],[2,1]]. One embedding has a trivial 5-by-5 block; the other uses the cyclic permutation representation of the character chi(A)=1, chi(B)=0 in Z/5Z. The full proof shows that no reduction of the original matrix group modulo any positive integer can have a nonzero C_5 quotient.

## Files

- `ATTEMPT_1.md`: complete proof, including the all-moduli argument and source-scope distinction
- `SOURCE_GATE.md`: exact original source, dated literature check, and prior-attempt gate
- `verify_exact.py`: standard-library-only exact finite controls
- `verify_exact_results.json`: deterministic replay output, including witness words for all moduli 1 through 64
- `RESEARCH_LOG.md`: research checkpoints
- `MANIFEST.sha256`: frozen-file hashes

## Replay

Run `python3 verify_exact.py > replay.json`, then compare `replay.json` with `verify_exact_results.json`. The recorded run passes **15,667 exact assertions**, checks all **4,373 reduced words of length at most 7**, verifies odd and mixed modulus images, and produces **64** explicit noncongruence witness words.

The finite checks do not prove the infinite theorem; `ATTEMPT_1.md` does. The construction answers the exact intersection-based question for abstract embeddings. It does not contradict embedding-invariance for a fixed algebraic group under algebraic embeddings.

The basic group-theoretic ingredients are classical and credited. No novelty, first-resolution, human peer-review, or proof-assistant verification claim is made. No repository publication or queue change is part of this local frozen candidate.
