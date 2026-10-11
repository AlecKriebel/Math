# Metric rigidity at the boundary of cubic compactifications

Version 1.0. Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X . Manuscript date: October 6, 2026.

The separately downloadable `paper.pdf` is the manuscript. `source-and-verification.zip` contains the original self-contained LaTeX source, explicit dependencies and source pins, scoped mathematical audits, exact-arithmetic verification scripts, licensing, and package provenance. Extract the source archive into a fresh directory. Its top-level `README.md` is this static deposit readme; it is not the live repository's publication-status page. `SOURCE_SHA256SUMS.txt` hashes every other member of the source archive. The archive does not include third-party manuscripts or reading caches, personal research instructions, credentials, Git helpers, or full-package review reports that would create a review self-reference.

The note's general result is a sharp singular Cartier-index rigidity criterion: if a positive-dimensional projective klt Fano carries the specified weak Kahler–Einstein metric and an actual ample Cartier root `-K_X = rL` with `r > dim(X)/2 + 1`, its tangent sheaf remains stable on finite quasi-etale covers and every parallel orthogonal complex structure equals the given one or its negative. Equal-dimensional products of projective spaces show sharpness at equality. The proof explicitly uses Druel–Guenancia–Paun's established singular decomposition theorem, a Hilbert-polynomial index bound, and local positive-Ricci curvature.

For cubic n-folds with n at least 5, the application identifies ordinary metric GH moduli, including the singular boundary, with cubic GIT modulo coefficientwise conjugation. This application assumes OpenAI's cited ordinary-double-point upper gap theorem at the pinned commit below. That principal input is not reproved in this note. The complex-preserving GH/GIT comparison uses Li–Liu's global Reeb minimum and Spotti–Sun's established transfer, and Kong–Shen–Zhao–Zhao already publicly state a stronger complex algebraic comparison. The smooth stability and rigidity precursors and the conjugation convention are credited in the manuscript. No first-solution claim, scheme or stack comparison, or formal verification is asserted.

## Reproduction and verification limits

`main.tex` is standalone and includes its bibliography. Open it in the Codex built-in LaTeX editor and compile, or use an existing LaTeX installation with the packages declared in that file. The repository's export used Tectonic 0.16.9. The included `reproducibility/build_paper.py` copies the source into a clean temporary directory before compiling; run `python3 reproducibility/build_paper.py --output rebuilt.pdf` from the extracted archive. LaTeX compilation verifies the document build, not its mathematics. The package helper copies the selected final PDF byte for byte and does not recompile it; a fresh PDF build may differ in metadata or engine-dependent bytes.

With Python 3.10 or later, run:

```text
python3 reproducibility/verify_constants.py
python3 reproducibility/verify_boundary_examples.py
```

These scripts use the standard library. The first verifies exact rational tail and fourfold constants from the scoped upstream audit. The second verifies explicit polynomial identities and line incidence used for boundary examples. Neither script verifies weak KE existence, a cited classification theorem, the complete gap proof, or mathematical priority. The manuscript and scoped proof notes give the logical arguments and their hypotheses.

`sources/PINNED_MANIFEST.json` records upstream commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a` and exact source hashes. Obtain that public commit from https://github.com/openai/math to inspect or rebuild the two cited upstream manuscript families. The original authors' build instructions apply. `publication/SOURCE_PROVENANCE.json` supplies version-specific primary links and inspected hashes. Source pinning and scoped audits are evidence, not formal certification.

## Licensing and review status

The original paper, prose, and audit material are CC BY 4.0. Original code is also available under MIT; see `publication/LICENSES.md`. External material remains under its authors' rights and is linked rather than redistributed or relicensed.

AI tools were used extensively in research, drafting, and verification. Internal adversarial AI audits and complete-package reviews are not conventional human peer review. This preprint has not undergone conventional human peer review. Full-package review reports and their frozen-payload acceptance receipts are kept separately in the repository; their exclusion from the source archive prevents review self-reference. No external individual was contacted on behalf of this project.

This file describes the fixed payload and makes no assertion about whether a public deposit has already occurred. Any public record identifier and immutable owned-source checkpoint belong in the accompanying exact frozen metadata or external publication receipt.
