# Low-twist branch-integral symmetric differentials

Problem **30003253**, source key **OWR-15170-020**, queue row **1830**.

**Overall disposition: UNSOLVED after 5/5 research avenues.** This package contains precise partial results and computational audits, not a resolution of the original open-ended surface criterion, a novelty claim, or external peer review.

## Source and scope

The authentic target is Natalia Garcia-Fritz's Question 1, printed p. 2841 in *Definability and Decidability Problems in Number Theory*, Oberwolfach Reports 13 (2016), no. 4, published 2017: [official record](https://ems.press/journals/owr/articles/15170), [official PDF](https://ems.press/content/serial-article-files/46652).

It asks for geometric hypotheses under which a differential of sufficiently favorable twist, integral along every plane branch component, can control curves upstairs of bounded geometric genus. The catalogue's scalar-section rewrite is not equivalent and is not used as the target. `SOURCE_GATE.md` explains the distinction and the bounded literature check. That report describes source recovery before this publication package was assembled.

## Results at the accepted scope

- A finite exact algorithm computes the minimum **absolute twist**, over all positive symmetric orders, for an effectively specified nonempty reduced plane branch divisor of degree b: test 2 ≤ k ≤ b+1 and 1 ≤ r ≤ floor(k/2).
- A smooth irreducible plane branch of degree b has minimum absolute twist b+1 over every order.
- Every reduced plane branch divisor attains minimum normalized twist k/r = 2, with a dual-polynomial description of all threshold forms. This is not an optimal upstairs genus criterion.
- First-order SNC results, sharp conic-tangent examples, pencil families, and a conditional finite genus/ramification-budget criterion are proved with their stated hypotheses and exceptions.
- The code implements rational coefficients only. Effectivity over algebraic-number fields is proved, but that backend is not implemented.

The classical transfer and residue arguments, algebraic-web framework, and the conic-tangent cover example are credited. General upstairs positivity, arbitrary exceptional-divisor corrections, and complete integral-curve classification remain outside the result.

## What to read

1. `RESEARCH_REPORT.md`: complete five-avenue synthesis and proofs.
2. `HIGHER_ORDER_AUDIT.md`: detailed mathematical audit of higher-order forms and finite optimization.
3. `PENCIL_COVER_AUDIT.md`: full pencil proofs, exact exceptional corrections, and the distinction between finite and generically finite morphisms.
4. `AUDIT_LOW_TWIST.md`: final scoped audit, including the discovered computational defect and its repair.
5. `ACCEPTANCE.md`: publication acceptance, limits, and provenance.
6. `checks/`: final checkers, authored examples, witnesses, regenerated results, and controls.
7. `SOURCE_GATE.md`, `SOURCE_METADATA.json`, `CORPUS_VERIFICATION.json`: authored source/status analysis and public verification metadata only.

`FIVE_AVENUE_LOG.md` and `RESULT.json` preserve the final research disposition. Their “publication performed” and “queue modified” flags describe the research stage, not a statement about any later repository operation.

## A defect found before publication

An initial implementation and the first independent formulation shared SymPy `Poly.rem`. That operation was not the linear multivariate normal-form map required for the matrix construction. A transformed smooth conic incorrectly had dimension 2 instead of 3. The agreement of two formulations sharing that primitive did not make the result reliable.

The main implementation was repaired using Gröbner normal forms. A separate horizontal-tensor implementation uses its own sparse lexicographic division. A third method uses coefficient blocks E(P)−FQ and no polynomial division. The final 49 spaces and 12 witnesses were regenerated and checked. Obsolete pre-repair outputs are not included. This regression remains part of the public record, not hidden behind the final PASS.

## Reproduce without changing the evidence

Recorded environment: Python 3.12.14 and SymPy 1.14.0. The dependency is pinned in `requirements.txt`.

From this directory:

```sh
python replay.py --output ../low_twist_replay.json
```

The replay verifies the package manifest, creates fresh temporary copies, deletes copied result files, and runs the main generator, both independent formulations, the full 49-space/12-witness checker, and publication controls. It runs every stage in ordinary and optimized (`-O`) Python, checks output bytes against the saved evidence, and deliberately corrupts saved dimensions, coverage, and witnesses to verify rejection. It leaves the package unchanged. A different SymPy release is intentionally rejected for byte-exact replay.

The 19 optimization-removable assertions originally present in three independent audit scripts have been replaced by explicit runtime guards in this package. `GUARD_HARDENING.diff` shows the entire code change; `GUARD_REVIEW.json` records exact AST equivalence under that transformation. The mathematical tests and diagnostics are preserved, while `-O` can no longer remove them. `checks/branch_integrality.py` is unchanged from the final audited generator.

## Hash provenance and packaging boundary

- `ORIGINAL_AUDIT_RECEIPT.json` is the exact original audit receipt.
- `AUDIT_RECEIPT.json` preserves every original field and adds explicit hash-scope metadata. Its `files` mapping identifies the **audited originals**, not edited publication copies.
- `PUBLICATION_EDITS.json` gives original-to-publication hashes and the exact edit scope.
- `MANIFEST.json` identifies the final publication files, excluding itself to avoid a self-hash cycle.
- `REPLAY_REPORT.json` records the isolated computational acceptance run before manifest freeze. A new replay verifies the frozen manifest before recomputing.

The three proof manuscripts are byte-identical to the originals. `AUDIT_LOW_TWIST.md` has only a package-relative source-gate link replacement. No raw third-party PDF or extraction text, corpus contents, obsolete computation, credentials, private source, or coordination material is included. No queue edit, repository push, or PR operation is performed by the replay.
