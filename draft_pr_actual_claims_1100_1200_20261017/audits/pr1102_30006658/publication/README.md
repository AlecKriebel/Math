# Vanishing of the cellularization map for non-p-nilpotent component groups

Alec Kriebel, independent researcher. ORCID: 0009-0001-9320-500X. Version 1.0.0, 17 October 2026. AI-assisted, unrefereed research note. No external human peer review or formal proof-assistant certification is claimed.

## Exact result

For every prime p, every characteristic-p field k and compact Lie group G with non-p-nilpotent component group, the canonical k-cellularization map of C_*(Ω((BG)^p-completed);k) is zero on all homotopy groups. Completion precedes looping. This answers Greenlees's OWR 9/2026 Question 2.2, printed p. 594. No null-derived-morphism conclusion or coefficient-ring extension is asserted.

## Files and reproduction

Paths below refer to the extracted source/verification archive. The outer upload kit contains the PDF, that archive, and the matching upload metadata and deposit manifest.

- main.tex: complete analytic proof and bibliography.
- output/pdf/cellularization-vanishing.pdf: four-page preprint.
- verification/check_bosonization.py: exact standard-library convention tests on the infinite noncommutative free tensor Hopf superalgebra, with bounded tested input words and untruncated operations.
- verification/expected_results.json: expected output.
- audits/: independent mathematical and priority reviews and source locators, included in the source/verification archive.
- SOURCE_MANIFEST.json in the archive: SHA-256 hashes and lengths of its other members.

Run `python3 verification/check_bosonization.py` with Python 3.10 or later; compare JSON with verification/expected_results.json. All assertions must be enabled; optimized Python (-O) is explicitly rejected. There are tests over F2, F3, F5 for associativity, coproduct multiplication, coassociativity, counits, both antipodes, both ideal sides and a negative control detecting loss of odd signs. Finite tests support conventions; the analytic proof in main.tex proves the infinite theorem and has no computational dependency.

To rebuild the PDF, run `tectonic main.tex` in this folder, or use a standard LaTeX distribution with the packages listed in main.tex. Different TeX versions/timestamps may change PDF bytes while preserving the source and mathematics. The distributed PDF hash identifies this edition.

## Source and priority controls

The source question is credited to J. P. C. Greenlees. Classical finite-ideal, proxy-smallness and compact-approximation inputs are credited to Sweedler/Lomp, Dwyer-Greenlees-Iyengar and Briggs-Iyengar-Stevenson. Greenlees's finite and restricted compact-Lie results are credited prior work. The priority report documents a dated bounded search, not exhaustive proof of bibliographic absence. No new Hopf-algebra finiteness theorem or new Morita theory is claimed.

The distributed materials contain authored text, code, outputs and public bibliographic/source-integrity records. Third-party source bodies, reading copies, credentials, sheet rows and internal coordination files are excluded. Extensive AI use in solution development, checking, literature inspection and drafting is disclosed in the paper.

License: Creative Commons Attribution 4.0 International (CC BY 4.0).
