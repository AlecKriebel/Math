# KP-4.69: partial endpoint analysis

**Unresolved. Five mathematical approaches completed; no full solution claimed.**

The target is a diffeomorphism of a closed 3-manifold that admits a topological, but no smooth, pseudo-isotopy to the identity. The two cylinder endpoints remain fixed as prescribed, and the cylinder map need not preserve levels.

The principal candidate deduction is that the Friedman–Witt separating twists admit zero-Casson–Sullivan cylinder representatives, using relative realization on the punctured prism factors. A smooth map with the same boundary restrictions follows after finitely many interior S²×S² stabilizations. Removing those summands is unproved and is essential to the original problem.

Other proved reductions explain why endpoint derivatives, split fillings, the natural finite cover, and classical mapping-torus invariants do not detect this family. For the explicit Dic_3 pair, the natural 144-sheeted cover is #121(S²×S¹), and the lifted twist is smoothly isotopic to the identity without deck-equivariance.

Files:

- `MATHEMATICAL_REPORT.md`: precise conventions and proofs, with external dependencies identified
- `APPROACH_LEDGER.json`: exactly five substantive approaches; literature and computation count zero
- `SOURCE_MANIFEST.json`: public citations, retrieved-paper hashes, inspection history, source limitations
- `CORPUS_BINDINGS.json`: identity and hash verification metadata only
- `verify_exact_checks.py` and `EXACT_CHECKS.json`: reproducible exact finite checks with a negative control
- `REVIEW_CHECKLIST.md`: the precise points requiring independent review

Run `python verify_exact_checks.py` from this directory. The script uses only the standard library. Its finite arithmetic is not a proof of a smooth pseudo-isotopy.

This directory contains authored work and verification metadata only. It includes no copied source papers, source text extracts, dataset records or private coordination material.
