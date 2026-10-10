# Reviewed publication disposition

The fresh independent AI audit `audit/AUDIT.md` is preserved byte-for-byte at SHA-256 `6b32e113331d805a54cd53990342e79058e0e26cf9849d6e8ee7445826cad415`. It passed the full elementary proof without a mathematical repair. Its Appendix B independently establishes the prior-theorem transfer.

## Changes from the audited snapshot

1. The root `ATTEMPT_1.md` changes status and attribution paragraphs only. The explicit construction and all mathematical proof sections are unchanged. The exact reviewed version remains `public/ATTEMPT_1.md`, SHA-256 `bc5f2f6db65d2ee5455904f0f3a852e42ad5621b6a2b36af4520e84edee6aa94`.
2. The root `SOURCE_GATE.md`, `README.md` and `RESEARCH_LOG.md` now report the verified inference from Kucharczyk’s theorem and final classification `already_solved, 1/5`. They do not attribute an explicit statement of the corollary or C_5 example to that paper.
3. `audit/independent_controls.py` changes only its author-results input path, from an executor-specific absolute path to `Path(__file__).resolve().parent.parent / 'public' / 'verify_exact_results.json'`. No mathematical computation changed. The original script SHA-256 was `627867eaa3f168cd71ed1f94ca1b9b9b0daa87d14d6e0d6a502f9c52eb40096b`; the portable version is covered by the current manifests. The unchanged audit report records the original run.
4. `reproduce.py` is a packaging-only hash and subprocess replay wrapper. It compares both programs' output with the recorded bytes and makes no new mathematical assertion.

The `public/` directory preserves all six originally reviewed author files and their original manifest, so the auditor’s frozen-object claims remain directly checkable. The audit manifest is regenerated for the portable script. Corpus files, downloaded third-party papers, screenshots, credentials and private coordination are excluded.

The one author turn is retained honestly: the elementary candidate was written before the earlier-theorem implication was completely verified. Review and packaging do not add turns.
