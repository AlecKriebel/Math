# Kjellberg's linear-plus-bounded theorem: a verified prior resolution

Problem **2303012 / AMR-022-3012**, queue rank 569, is **already_solved**.
The answer to Hayman–Lingham Problem 3.12 is affirmative in every requested
dimension. This is a literature correction, not a new discovery.

Michael Benedicks proved the exact assertion in **Corollary 3, printed
page 67**, of *Positive harmonic functions vanishing on the boundary of
certain domains in R^n*, Arkiv för Matematik 18 (1980), 53–72,
[DOI](https://doi.org/10.1007/BF02384681).
The [original article](https://archive.ymsc.tsinghua.edu.cn/pacm_download/116/7328-11512_2006_Article_BF02384681.pdf)
was retrieved and checked, including its standing hypotheses and the
proof dependencies. Corollary 3 explicitly identifies Kjellberg's question.

- `PROOF.md`: exact claim, hypothesis bridge, and deduction from the published theorem
- `SOURCE_GATE.md`: source identification, prior-report correction, and bounded duplicate search
- `ATTEMPT_LOG.md`: one substantive investigation and its scope
- `SOURCE_MANIFEST.json`: original-source provenance and hashes
- `STATUS.json`: machine-readable conclusion and limits
- `verify.py`, `CHECKS.json`: reproducible exact consistency checks
- `verify_manifest.py`, `SHA256SUMS.json`: frozen-file integrity

Run `python3 verify.py` and `python3 verify_manifest.py` from this directory.
The scripts check algebra, metadata, and file integrity. They do not
formally verify potential theory or replace mathematical review.

Prepared 4 October 2026 UTC. AI-assisted, unrefereed source verification.
No source PDFs, page images, raw imported reports, or dataset corpus are
redistributed in this packet. No first-priority or novelty claim is made.
