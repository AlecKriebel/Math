# A credited counterexample to the generalized Saxl common-neighbor conjecture

Problem **30006342 / OWR-14299292-003** is already answered negatively by the September 2026 preprint of **Aluna Rizzoli and Adam R. Thomas**, [Common neighbour conjectures for Saxl graphs fail at every base size, arXiv:2609.01367v1](https://arxiv.org/abs/2609.01367v1). This package reproduces and independently checks one finite counterexample. **No mathematical discovery or novelty claim is made.** The original record is classified `already_solved`, with zero new proof-attempt turns.

## Verified result

For the explicit affine action G=F3^9 semidirect H given in [the certificate](COUNTEREXAMPLE_CERTIFICATE.md), H has order 1152 and acts irreducibly. Hence G is faithful and primitive, of degree 19683. Its minimum base size is exactly two. The two vertices

    0 and (1,1,1,1,1,1,0,0,0)

have no common neighbor in its Saxl graph, which here equals its generalized Saxl graph. Both implementations exhaust all 19683 possible common neighbors. This one instance refutes the original universal conjecture for primitive groups with base size at least two.

The [independent audit](review/COUNTEREXAMPLE_AUDIT.md) passed the exact finite construction, primitivity, minimum base size, common-neighbor obstruction and ancillary diameter-three computation. It uses dense matrix closure and finite-field Gaussian elimination, separately from the first signed-permutation/orbit implementation.

## Reproduce

Requires Python 3 and NumPy. Tested with Python 3.12.14 and NumPy 2.3.5. No GAP, Magma, Lean, IRREDSOL or network access is required. Keep Python assertions enabled; do not use `python -O`.

    python verify_public_packet.py --replay

This verifies the public manifest, runs both exact checkers, and checks their result JSON is byte-identical to the included audited results. Individually:

    python verify_small_counterexample.py
    python review/independent_dense_fixedspace_check.py

## Scope and credit

The source is a September 2026 preprint, not asserted here to be journal-accepted. Approval of this package does not validate the whole preprint, its all-base-size families, classifications, global minimum counterexample degree or Lean formalization. The weaker amended almost-simple-or-diagonal conjecture is a different question.

The authors' literal generator file and MIT license are retained in source/. Its comment calling the example the least-degree counterexample is quoted source content, not a global minimality claim verified by this package. See [sources](SOURCES.md).

This is a public projection of a larger reviewed input, not a complete copy. PDFs, screenshots, corpus caches, repository snapshots, broader unapproved material and coordination records are omitted. The exact finite mathematics, source generator data, executable checks, results and substantive audit are retained. [PUBLIC_PROJECTION.json](PUBLIC_PROJECTION.json) states every file transformation and original digest; PUBLIC_MANIFEST.json binds this package. The public checker was rerun after the portability-only adaptations.
