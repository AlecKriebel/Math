# A(affine A2): five attempts on the Helly-group question

**Final mathematical status: unresolved, 5/5 substantive attempts.**

The target is AIM *Geometry and topology of Artin groups*, Problem 4.2:
does A=<a,b,c | aba=bab, bcb=cbc, cac=aca> admit a proper cocompact action
on some Helly graph? The catalogue's character-twist title names only an
older model-specific partial result.

## Results and boundaries

- The specific Haettel–Huang weakly modular Cayley graph Q, with nine positive
  dual-simple generators and their inverses, is not Helly. The radius-one
  balls at 1, a^2, (ab)^2 have pairwise but no common intersection.
- Its powers Q^2 and Q^3 are also not Helly. Small exact certificates use
  images of at most 2,089 vertices, with no faithfulness assumption.
- Every fiber-preserving repair over the Deligne complex with nonempty
  complete real-tree fibers at the maximal-parabolic vertices is nonproper.
  This covers arbitrary line-isometry cocycles as well as character twists.
- The general inference “G x Z Helly implies G Helly” is false, as explicitly
  illustrated by the affine Coxeter group and its product with Z. This is
  established-literature context, not a new counterexample.
- Published hull theorems give A a proper action on the locally finite Helly
  graph H(Q). Cocompactness of this action is equivalent to Q being coarsely
  Helly. That condition remains undecided here.

These are model-specific obstructions and literature-based reductions. None
is a negative answer to the original group-level question. No novelty or
first-resolution claim is made. Independent adversarial review is required
before any publication is treated as final.

## Files

- SOURCE_GATE.md: exact source, current literature, and bounded prior-attempt audit
- ATTEMPT_1.md through ATTEMPT_5.md: the five written mathematical attempts
- verify_local_obstruction.py: dependency-free exact finite certificate
- checks_turn2.json: current successful certificate output for n=1,2,3

Run: python3 verify_local_obstruction.py

No source PDFs, archived source HTML, bulk corpus data, or private conversation
records belong in this public package.

## Independent audit and release clarification

The original frozen nine-file package received an independent adversarial
PASS as an explicitly unresolved partial-results package. The full mathematical
audit is in audit/REPORT.md, with an independent verifier and its output.
The audit's three nonblocking recommendations are addressed by this release:
an exact weak-modularity citation, explicit intrinsic rank-two normalization,
and explicit image-distinctness/empty-triple assertions. The original package
is preserved separately; its manifest is audit/FROZEN_AUTHOR_MANIFEST.json.

The audit predates these narrow additions. They require their own narrow
review before publication approval. RELEASE_CHANGES.md records every release
change. The status remains UNSOLVED, 5/5; no sixth attempt or group-level
resolution is claimed.
