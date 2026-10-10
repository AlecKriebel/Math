# Isolated transversals: explicit lower bound and open gap

Problem 30001066 / OWR-2090-019. Version 1-reconstructed, 2026-10-06.

**Partial result, not a full solution.** A family of `3d-3` compact, full-dimensional, pairwise disjoint boxes minimally pins a line in `R^d`. This refutes the suggested `2d-1` bound for `d>=3`. Existence of some larger dimension-dependent bound remains unresolved here. The six-object obstruction is known; no novelty claim is made.

- `proof.md`: complete general proof, continuous deletion witnesses, conditional first-order bound
- `approach_audit.md`: five approaches and the exact remaining gaps
- `certificate.json`: authored rational six-box geometry and deletion motions
- `verify.py`: exact rational certificate verifier, standard library only
- `test_verifier.py`: semantic/input mutations, optimization and relocation tests
- `source_audit.json`: public source metadata and explicitly historical corpus pins
- `results.json`: fresh verification outcomes
- `MANIFEST.json`, `verify_package.py`: file inventory, sizes and SHA-256 validation

Run with Python 3:

    python verify_package.py
    python verify.py
    python -O verify.py
    python test_verifier.py

The code certifies whole real motion intervals using exact rational endpoint inequalities. Tested dimensions check the implementation; the written proof establishes the result for every dimension.

This is a reconstructed author packet. An interrupted earlier working directory was unavailable; no byte-identical old freeze is claimed. Scholarly PDFs were retrieved again. The earlier full-corpus checks are labeled historical and have not been repeated against unavailable data. Fresh independent mathematical and package review remains required.

Only authored proof/code/certificates and public verification metadata are included. Scholarly PDFs/extracts, corpora and private coordination are excluded.
