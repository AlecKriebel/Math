# A flow reduction for equilibrium uniqueness in rank-one bimatrix games

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X.
Version 1.0, 13 October 2026. Authored work: CC BY 4.0.

This local package contains the complete theorem paper, its editable LaTeX source, and a provenance-preserving evidence supplement. The theorem is UNIQUENESS coNP-complete / NONUNIQUENESS NP-complete for explicitly listed rational variable-dimension bimatrix games with exact rank(A+B)=1, arbitrary degeneracy, and uniqueness of the entire mixed-strategy pair. The reduction starts from nonempty positive-integer PARTITION and supplies a known strict pure default equilibrium. Worldwide priority remains unknown; no firstness or current-worldwide-open assertion is made.

The underlying complete proof was accepted in the root mathematical audit after two fresh mathematical review families. The support package preserves dated independent and adversarial AI review history, with each verdict limited to its frozen input. `evidence/reviews/package_01/` records the first complete manuscript/package review, which found zero P0–P3 issues on its unchanged inputs. The root subsequently recorded an editorial release-wording issue; the repair and subsequent review state are tracked in `STATUS.json`. These records are unrefereed AI review evidence.

Start with `output/pdf/paper.pdf` and `paper.tex`. `SUPPLEMENT.md` describes actual reproducibility interfaces and limits; `EVIDENCE_INDEX.md` locates the original and fresh evidence. `EVIDENCE_COPY_MANIFEST.json` gives exact source-to-package path and hash mappings. `STATUS.json` is the current preparation state; historical statuses inside frozen evidence remain historical. `publication/zenodo.json` supplies publication metadata. The external `zenodo-deposit.json` wrapper exactly embeds that metadata and names the supplied PDF and support archive for the repository tool; it is locally prepared only. Its preparation does not create an uploaded record or reserve a DOI.

The eleven-file original theoretical edition is preserved byte-for-byte at `evidence/original/submitted/`. It contains no executables, fixtures, or check logs. Its references to six-game/39-network computations remain historical prose; those omitted computations have not been replayed. The separately included fresh family scripts and exact receipts are newly authored review evidence, not replacements attributed to those historical scripts.

Build the disk PDF with `tectonic --outdir output/pdf paper.tex`. The built-in standalone LaTeX compiler also reports success. A TeX installation is required to rebuild the PDF; Python 3 is enough to verify package hashes and run the finite exact checks. Run from this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_package.py
PYTHONDONTWRITEBYTECODE=1 python3 build_archive.py
```

`build_archive.py` creates a deterministic candidate support archive with fixed timestamps and records its SHA-256. It includes current integrity and copied evidence, excluding private material and rendering/build intermediates. Its receipts distinguish content hashes from the archive hash. See `SUPPLEMENT.md` before rerunning evidence scripts because they write new time-stamped results beside themselves. Preserve the frozen receipts; use a disposable copy to obtain new runs.

Extensive AI assistance was used for solving, source work, verification, and writing, including independent/adversarial AI review. The preprint is unrefereed: there is no claimed human journal review or proof-assistant verification. Third-party source PDFs, extracted text, page images, raw API discovery responses, and raw/rawprivate folders are excluded. Cited works retain their own rights.
