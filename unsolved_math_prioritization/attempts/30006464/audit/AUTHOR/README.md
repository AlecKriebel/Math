# Short coefficient detection: five-approach partial report

**Problem 30006464 / OWR-14299577-017. Original target unresolved.**

This packet contains authored mathematical deductions and exact arithmetic controls, prepared 2026-10-06. It does not establish novelty, a full solution, an actual counterexample to the positive-epsilon question, or human peer review.

The main positive partial is a uniform proof for the one-dimensional oldform families `c Delta(Nz)`, at every level, including nonsquarefree levels. The same family disproves the stronger fixed-linear-cutoff variant. The two conclusions are compatible.

Read `PROOFS.md` for complete hypotheses, derivations, and the remaining gap; `APPROACHES.md` records the five attempted routes. `SOURCES.json` contains public citations and pinned PDF metadata. No source document, extract, dataset content, or private coordination material is included.

Offline checks, Python 3.10+ standard library only:

    python3 -B verify.py
    python3 -B test_packet.py

`SOURCE_PIN.json` fixes verifier sources before execution. `MANIFEST.json` fixes the complete payload inventory and bytes. The checks are supplementary exact controls, not a proof assistant or certification of all analytic arguments. `verify_corpora.py` optionally accepts three explicitly supplied corpus paths, in catalog/problems/research-results order, and verifies their identity without publishing their contents.
