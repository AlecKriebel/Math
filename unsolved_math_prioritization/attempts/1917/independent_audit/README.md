# Chordal clique partition independent audit

This packet records an independent mathematical acceptance of the main result in Okechukwu's arXiv:2609.20871v1 as a prior resolution of Erdős Problem 81. Read ACCEPTANCE.md for the precise accepted statement and the separate source-status qualification.

The substantive proof audit is split between FRACTIONAL_AUDIT.md and INTEGRAL_AND_RIGIDITY_AUDIT.md. The original author packet remains unchanged and is identified by an external SHA-256 pin. No corrected manuscript or new solution is claimed. No repository or problem-queue changes, publication, or external communication were performed in preparing this audit.

SOURCE_INSPECTION.json records public source identities, retrieval outcomes, and inspection boundaries. PROVENANCE.json records complete corpus and target identity metadata without reproducing dataset contents. The independent checks.py enumerates all labelled graphs through order five, checks exact edge partitions and rooted/chordal equivalence there, checks finite arithmetic, and rejects the invalid claim that fractional and integral clique partition values always coincide. It is not a proof checker.

Run `python checks.py` for the source-free finite replay, or `python -O checks.py` to ensure checks do not depend on assert statements. Optional `--catalog`, `--problems`, `--reports`, and `--pdf` accept separately supplied pinned source files; all three corpus arguments must be supplied together. Optional `--author-archive` and `--author-manifest` replay the preserved author freeze.

The ZIP is accompanied by an external archive-and-member manifest and an external receipt. Hashes, sizes, member names, and read-only member modes are pinned there. The archive contains only authored audit material, public-source verification metadata, and verification programs/results. It contains no third-party manuscripts or scans, dataset rows, or private coordination material.
