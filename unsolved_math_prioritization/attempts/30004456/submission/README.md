# 30004456: an existing 2026 resolution

Proposed outcome: **already_solved, 1/5**, for the nonzero-character Gardam–Kielak conjecture. The unrestricted zero-character wording needs correction; it is not covered by a canonical HNN exponent map.

The resolving source is Jaikin-Zapirain–Kudlinska–Sánchez-Peralta, arXiv:2606.31774v2 (31 August 2026), Corollary 1.5 and Theorem 3.3. The source is a preprint. This packet verifies applicability and gives all conversions required to recover the catalogue's negative-Euler-characteristic/base-group formulation, including nonprimitive and rank-zero conventions.

- `PROOF.md`: exact scope and complete theorem-application proof
- `SOURCE_PROVENANCE.json`: immutable identifiers, source locations, retrieval limitations
- `THEOREM_AUDIT.md`: dependency and adversarial-scope checks
- `RESEARCH_LOG.md`: the one substantive literature-resolution turn
- `STATUS.json`: proposed scope-specific disposition and budget accounting
- `verify.py`: deterministic, bounded controls and optional source-hash verification
- `CHECK_RESULTS.json`: captured control output, with private sources present
- `MANIFEST.sha256`: hashes of all other public payload files

Run: `python3 verify.py`

Optional source verification: `python3 verify.py --sources /path/to/independently/downloaded/source-pdfs`. Expected filenames and hashes are in `SOURCE_PROVENANCE.json`. Missing or changed sources fail in this explicit mode. The default mode does not pretend to have verified unavailable PDF bytes.

The controls check finite Schreier-graph computations, primitive normalization, signs, degenerate boundaries, and package consistency. They do not certify the general theorem, preprint correctness, novelty, or worldwide literature coverage.

Source PDFs, extracted full text, pinned full datasets, raw repository snapshots, and private coordination are intentionally excluded. No remote writes were performed by the investigator. Publication requires a fresh independent review and a separate root acceptance decision.

AI tools assisted source retrieval, mathematical exposition, and local checks. This is a literature-resolution verification packet, not a new research discovery.
