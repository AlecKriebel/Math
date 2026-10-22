# Calegari Question 10.1: accepted corrected-v2 scoped partials

Problem 10300039 / AMR-102-0039, rank 1007. **Unsolved; 5/5 substantive approaches.** Publication checkpoint: 2026-10-08. Extensive AI assistance; no human peer-review or formal proof-assistant claim.

The accepted corrected-v2 author distribution and independent audit are preserved byte-for-byte. The superseded initial version was not accepted and is not included. The author files' “independent review pending” wording is an immutable historical checkpoint; the later verdict is [accept_corrected_v2_scoped_partials](audit/ACCEPTANCE.json). No post-acceptance mathematical correction is applied.

## Mathematical scope

Read [the result](author_original/bundle/author/RESULT.md), all five APPROACH files beside it, and [the full independent audit](audit/AUDIT.md). They establish an exact side-domain/halfspace criterion and a horosphere obstruction, compact actual-leaf stabilizer reductions, a Holder exponent strictly above 1/2 criterion, conditional uniform-quasigeodesic endpoint and proper-map reductions, and finite-cover/isotopy/ordered-product-blowup construction obstructions.

The global proper-leaf-limit-set dichotomy is credited to the inspected Calegari source and used only in the closed setting. The missing general implication is exclusion of full-sphere leaf limit sets from arbitrary taut two-sided branching. No general asymptotic-separation theorem, valid counterexample, novelty certificate, Anosov-subclass resolution, or worldwide current-openness certification is claimed. The printed question does not explicitly say closed; the broader noncompact reading is not resolved.

The original full proofs in two 1998 Fenley papers were not completely verified. The apparent discrepancy between the old AMS abstract and Fenley's 2026 discussion remains unreconciled. Public source titles, URLs, hashes, sizes, inspection history, and dated manuscript status are metadata; original PDFs, extractions, screenshots, datasets, and private coordination material are excluded.

## Trust boundary and replay

Authenticate BOOTSTRAP.py against its SHA-256 and size stated outside this distribution (the draft PR), then run:

    python -I -S -B BOOTSTRAP.py
    python -I -S -B -O BOOTSTRAP.py
    python -I -S -B -OO BOOTSTRAP.py
    python -I -S -B TEST_MUTATIONS.py

The bootstrap pins VERIFY_PUBLICATION.py and PUBLICATION_MANIFEST.json before executing code. The publication verifier authenticates every file and directory, all 21 files in the accepted author boundary, all 9 independent audit files, the exact original archives, and their external manifests. Authenticated code runs from a temporary frozen copy. Neither replay nor controls write to the supplied publication. Run as an unprivileged user; the controls verify actual permission denial, not mode bits alone. The three trust files are excluded from the manifest to avoid a circular hash and authenticated by the external bootstrap chain instead.

The source-free default replays the 4,760 author finite diagnostics, all 51 author negative controls, and the independent audit's 2,773 exact-rational diagnostics. It separately checks the full 21-file distribution. These are executable diagnostics and integrity checks; they do not mechanically prove the geometric arguments. Historical full-source and corpus receipts are preserved as historical evidence. The current default source and corpus rehash fields are each NOT_RUN. The original full independent external-binding replay is NOT_RUN unless all optional inputs below are supplied; this is distinct from the fresh source-free independent finite replay.

Optional current rehash of retained originals (not a new web retrieval or new source inspection):

    python -I -S -B BOOTSTRAP.py --source-dir /path/to/pdfs --problems /path/to/problems.json --research-results /path/to/research_results.json

Sources and corpora may be supplied separately, but both corpora are required together. Supplied files must actually match the frozen full-file hashes. With all inputs present, the original independent full audit also runs, including fresh PDF-to-text equality against the retained inspected text. Its input directory therefore needs all five PDFs and matching .txt files and pdftotext on PATH. Missing, damaged, or mismatched inputs fail; historical receipts never promote an absent input to PASS.

`--integrity-only` authenticates all bytes and acceptance scope but performs no diagnostics or external rehash. The publication tests use a separate already trusted original bootstrap for damaged candidate trees, including hostile executable replacements. External pins authenticate a particular publication; self-reported hashes alone do not authenticate anything.

No merge, release, DOI deposition, or external outreach is part of this publication. GitHub CI is reported separately for the exact PR head; zero checks are not a pass.
