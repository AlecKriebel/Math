# The Sperner property of Artinian complete intersections in characteristic zero

Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X

This concise note records the immediate characteristic-zero consequence of OpenAI's Artinian EGH theorem and Harima–Wachi–Watanabe's previously published EGH-to-Sperner theorem. For every standard graded Artinian complete intersection A over a characteristic-zero field, the maximal minimal-generator count over all ideals equals the largest coefficient of ∏(1+t+⋯+t^(d_i−1)). Equality is attained by a power of the maximal ideal at a maximal Hilbert layer. The empty/all-linear case A=k has maximum 1, attained by A.

The upstream EGH breakthrough, known conditional implication and known reductions are explicitly inherited. This package claims no first priority, new EGH proof, weak/strong Lefschetz theorem, nongraded extension or unrestricted positive-characteristic result. AI tools were used extensively. Automated adversarial audits are not conventional human peer review; this preprint has not undergone conventional human refereeing at publication. No formalization is claimed.

## Files and reproduction

The intended Zenodo payload consists of three separately downloadable files: paper.pdf, source.zip and verification.zip. The upload kit's outer directory is an organizer, not an additional upload.

Extract both archives into the same empty directory. The source archive contains the standalone manuscript/main.tex (inline bibliography), supplied citation metadata, this README and the project license. The verification archive contains exact integer examples, independent bounded auxiliary checks, source hashes, the dependency ledger and scoped audit/priority notes. It excludes credentials, third-party PDFs, caches and local compiler scratch files.

Run `python3 verification/reproduce.py --compiler tectonic` from the extracted package. Python 3.10+ and Tectonic 0.16.9 are sufficient; the computations use the standard library. For arithmetic alone use `--skip-pdf`. Tectonic may download its normal TeX bundle when uncached. Compilation creates its PDF only in a clean temporary directory and verifies that no overfull boxes or undefined references occur. PDF bytes may vary with compilation timestamps; the deposited PDF's exact hash is in the payload inventory. The reproducibility run checks all reported finite computations, which are illustrations and bounded falsification checks, not proofs of EGH.

The manuscript compiled successfully with the Codex built-in editor and Tectonic 0.16.9, and all five pages were rendered and visually inspected. Verification environment: Python 3.14.6; Poppler 26.08.0. The code remains compatible with Python 3.10+.

## Exact dependencies and provenance

HWW: Harima, Wachi and Watanabe, Proc. Amer. Math. Soc. 145 (2017), 1497–1503, Theorem 11; DOI https://doi.org/10.1090/proc/13347; arXiv:1601.06928v1, submitted 2016. Primary arXiv full text was checked; publisher PDF access returned 403. The note reproduces the required argument and filtration reduction directly.

OpenAI: *Commuting Division-Coefficient Forms and the Artinian Eisenbud–Green–Harris Conjecture*, Corollaries 1.2–1.3, and *The Artinian Lex-Plus-Powers Betti Theorem*, Theorem 1.1/Corollary 1.2. Both manuscripts are dated September 23, 2026 and are attributed to OpenAI using supplied manuscript-specific citations. Sources used are pinned at https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a; SHA-256 inventory is in receipts/pinned_sources.json. Official public collection release evidence is October 6, 2026, not the manuscript date. The full-length Hilbert-function theorem is sufficient; stronger Betti/general-length claims are unnecessary. No later official revision appeared at the audit date.

The central unrefereed input was scrutinized across independent approach families, with exact mechanisms and audit limits recorded. No material gap was identified. Builds of upstream multi-file sources used pinned local copies and a cosmetic wrapper for pdfTeX metadata primitives under XeTeX/Tectonic; their original TeX was not modified. A successful source build is not proof verification. There is no applicable family 200 formalization in the pinned catalogue and no claimed Lean verification.

The original-source copies and other researchers' primary papers are not redistributed in these archives. Exact URLs, authors, versions and hashes permit independent retrieval. Scoped audit reports preserve their original conclusions; review records and publication receipts are separately retained in the public project repository.

## License

Original note, code and project-authored supplement: CC BY4.0, https://creativecommons.org/licenses/by/4.0/. Third-party works cited retain their own rights. This does not relicense the upstream repository or the cited papers.
