# Exact crossing optimality certificates for two complete bipartite families

This reader contains the full accepted mathematical proof, independent acceptance report, source-scope review, and reproducible supplemental checks for the specified balanced integer-coordinate four-ray drawings of K(3,n) and K(4,n), for every integer n >= 3.

The proof establishes Székely's exact set-system inequality for every simultaneous assignment of the sets A_e. Writing q(n) = floor(n/2) floor((n-1)/2), the drawings have q(n) and 2q(n) crossings, respectively. The direct argument uses a K(3,3) parity identity, Mantel's triangle-free bound, and an exact restriction-counting step. It does not substitute an ordinary-crossing or pair-crossing optimum for the all-assignment inequality. All details, including integer coordinates and the absence of triple intersections, are in the unchanged [full proof](PROOF.md).

The accepted scope affirmatively addresses the original existential question, OWR-822-007 / 30000215 (queue rank 1782). Its recorded disposition is `claimed_solved`, 1/5, at this family-specific scope. The literal existence question already had known nonplanar positive cases. No novelty, first-solution, full-classification, arbitrary-drawing, or all-K(m,n) claim is made. No additional mathematical pass was used to assemble this reader.

## Reading order

1. [PROOF.md](PROOF.md): the complete theorem and uniform proof, unchanged from the accepted version.
2. [ACCEPTANCE.md](ACCEPTANCE.md): the independent mathematical review and final proof-version binding.
3. [SOURCE_SCOPE_AND_PRIOR_ART.md](SOURCE_SCOPE_AND_PRIOR_ART.md): the final original-source interpretation, prior-art boundary, and qualified disposition.
4. [SOURCE_VERSION_NOTES.md](SOURCE_VERSION_NOTES.md): which source versions were inspected and how to read the earlier clarification alongside the final review.
5. [CHECKS.md](CHECKS.md) and [VERIFICATION.md](VERIFICATION.md): finite supplemental coverage and the safe replay instructions.

The proof needs no computation. The finite checks support geometric and implementation details; sampled assignments and exhaustive enumeration of a single small switching image cannot establish the infinite-family theorem.

## Attribution and limits

Székely's published *An Optimality Criterion for the Crossing Number*, Theorem 1, supplies the exact criterion and its independent-odd interpretation: [AMC 1 (2008), 32–37](https://amc-journal.eu/index.php/amc/article/download/43/30), [DOI](https://doi.org/10.26493/1855-3974.43.506). The original existential question is on printed p. 983 of [OWR 17/2005](https://ems.press/content/serial-article-files/45990?nt=1).

The four-ray construction and crossing counts are classical Zarankiewicz mathematics. Kleitman's parity and local-subgraph arguments are relevant antecedents, and the triangle-free bound is Mantel's theorem. The proof and final source review explain the relation to Eppstein's pair-crossing treatment without relabeling it as an independent-odd theorem. Pelsmajer, Schaefer and Štefankovič record the already-known K5 and K(3,3) independent-odd values in *Removing Even Crossings*, [author manuscript, Theorem 1.2 and Remark 1](https://ovid.cs.depaul.edu/documents/tutte.pdf).

The September 2026 general complete-bipartite manuscript was screened for its publicly stated ordinary-crossing scope only. It is not a premise of this proof, was not mathematically audited here, and is not treated as an unrestricted all-A_e certificate. The bounded source search certifies neither novelty nor global current openness.

## Integrity and replay

Use Python 3.10 or later, standard library only, from this directory:

    python validate_packet.py
    python replay_checks.py
    python -O replay_checks.py
    python -OO replay_checks.py
    python test_packet.py

The original `verify_exact.py` is byte-preserved and contains assertions. Running it directly with `python -O` or `python -OO` removes those assertions. For every mode, use `replay_checks.py`, which checks the source pin, compiles the unchanged checker explicitly with `optimize=0`, runs it in a temporary directory, and compares both output bytes and the reported counts. `test_packet.py` performs targeted negative tests showing that all sixteen original assertion sites remain active in that compiled replay under normal, -O, and -OO interpreters. It also tests malformed or tampered packets. See [VERIFICATION.md](VERIFICATION.md) for exact coverage and limitations.

[PRESERVATION_MAP.json](PRESERVATION_MAP.json) records the byte counts and SHA-256 values of all twelve preserved authored inputs, including the proof (15940 bytes; SHA-256 6ec0d8fbf2e583e02fd775e24be762144d09ae3e8de9a835a80856e27527746e). The strict manifest covers every public file except itself. These are integrity checks, not digital signatures, mathematical formalization, or independent external peer review.

This directory contains authored mathematical and source-scope reports, executable checks, and verification metadata. No third-party source PDF, extracted source document, dataset contents, private personal information, or private coordination file is included. Public source URLs and source-file hashes identify inspected material without redistributing it.

## Independent integration review

[INTEGRATION_ACCEPTANCE.md](INTEGRATION_ACCEPTANCE.md) accepts this reader's packaging and replay contract after an independent integration review. It adds no mathematical pass. [INTEGRATION_EVIDENCE.json](INTEGRATION_EVIDENCE.json) records fresh replays, assertion-enforcement checks, metadata-tamper regressions, link checks, and preservation checks. [REVIEW_CHANGE_MAP.json](REVIEW_CHANGE_MAP.json) maps every input file to its reviewed counterpart. [SOURCE_LINK_REVIEW.json](SOURCE_LINK_REVIEW.json) separates freshly checked public sources, locally rechecked pinned public-source bytes, and retrieval limits.

Run the independent review checks with:

    python review_checks.py

The original REPLAY_REPORT.json and TEST_REPORT.json remain unchanged historical records for the prepared 22-file reader (21 manifest entries). Fresh results for this expanded reader are in INTEGRATION_EVIDENCE.json. Their historical scope is preserved rather than relabeled. The validator now pins the complete historical report and preservation-map bytes, preventing resealed mode or provenance changes that its earlier field checks did not reject. The original checker and both original replay/test entry points are unchanged.
