# Verification of the odd-period focal inversion area product

Alec Kriebel, independent researcher. ORCID: https://orcid.org/0009-0001-9320-500X . Dated 16 October 2026. Version 1.0. Authored materials: CC BY 4.0.

This attributed, unrefereed research note gives a self-contained flag-curve proof of the historical k903,a claim in Reznik--Garcia--Koiller, arXiv:2004.12497v11, Table 10 p. 12, and Conjecture 1 following Proposition 7 in Reznik--Garcia--Helman, arXiv:2012.03020v2 p. 6. Ferudun, *Products of the Two Focal Inversion Areas in Elliptic Billiards*, version 1.0, [DOI 10.5281/zenodo.23096994](https://doi.org/10.5281/zenodo.23096994), proves the same theorem by substantially the same meromorphic divisor mechanism. The note explicitly credits that exact overlap and the established general method. It makes no novelty, first-proof, certified independent-discovery, absolute-priority, or current-openness claim.

## Mathematical scope

For a>b>0 and 0<lambda<b², fix the outer ellipse with squared axes a²,b² and the proper inner confocal ellipse with squared axes a²-lambda,b²-lambda. Invert the original ordered orbit vertices in unit circles at the original foci ±sqrt(a²-b²). The observable is the signed straight-edge shoelace area of each image polygon. For every primitive odd-period billiard actually admitted by this pair, including admitted coprime star windings and reversal, their product is phase constant and positive. Repeating a primitive cycle r times multiplies each area by r and the product by r². Arbitrary vertex reorderings and circular/degenerate/hyperbolic caustics are outside the strict theorem.

The proof is analytic and self-contained: a normalized compact genus-one flag curve, four common isotropic tangents, disjoint odd-order translation grids, a same-coordinate bound at adjacent poles, reversal oddness, opposite-focus zeros, and compactness. Real inversion is nonsingular. The finite programs do not prove this universal statement.

## Files

* `focal_inverse_area_product.pdf` and `.tex`: the paper and its complete TeX source.
* `verification/portable_exact_verifier.py`: pinned current dependency-free finite exact verifier.
* `verification/results_normal.json` and `results_optimized.json`: actual explicit receipts, identical to raw successful stdout, with Python flags and source SHA-256.
* `verification/run_negative_controls.py` and `negative_control_results.json`: reproducible intentional-failure checks with raw child stdout/stderr and exits.
* `verification/README.md` and `RUN_SUMMARY.json`: execution instructions, arithmetic and guard bounds, counts and limitations.
* `materials/SOURCES_AND_ATTRIBUTION.md` and `EXACT_CONTROLS.md`: exact source contract, overlap/priority limits, and checkable finite examples.
* `zenodo-deposit.json`: intended metadata and upload filenames; it is not a deposit receipt and assigns no DOI to this note.
* `PUBLIC_MATERIALS_MANIFEST.json`, `verification-package.zip`, `PACKAGE_SEAL.json`: final byte-digest records and source archive after freeze. Their presence records a package candidate for review, not external publication or whole-package acceptance.

## Reproduce the finite controls

From this directory, with Python 3.11 or later and no third-party dependencies:

```sh
python3 -E -S -B -P verification/portable_exact_verifier.py
python3 -E -S -B -P -O verification/portable_exact_verifier.py
python3 -E -S -B -P verification/run_negative_controls.py
```

The verifier writes only JSON to stdout by default. To create an explicit new receipt, add `--receipt chosen-new-file.json`; the parent must exist and existing files, directories or symlinks are rejected without overwrite. Do not point this option at the included receipts. Both successful modes perform 245 mathematical checks in 27 fixed nonempty groups. The four checked polygons are convex winding-one trajectories: H and V triangles at lambda=40/9 with product 5/256, and the genuine same-caustic diamond/rectangle at lambda=40/13 with distinct products 1/10 and 169/1600, all on x²/8+y²/5=1. Higher odd periods and stars are covered by the proof, not this finite suite. The negative harness requires every intentional fault to fail and reports 26 attempts, rather than 26 mathematical checks.

Build the paper using an installed trusted TeX compiler, for example:

```sh
tectonic --outdir chosen-build-directory focal_inverse_area_product.tex
```

No build cache or third-party dependency is distributed. See the verification README for exact field arithmetic, sign-enclosure limits, scaling distinctions, and the historical unsafe-assertion qualification.

## Source and priority limits

The literal historical row is dated **10/20** and occurs in expanded arXiv v11, not its shorter journal table. The RGH v2 delta radicand has a defect at the exact axes used here; a plus-b⁴ substitution is checked only at that control. No general corrected formula or journal typography is claimed. The official IMPA book preview lists §8.5 but omits its text, and the complete section was unavailable for this bounded comparison. Full RGH journal typography was also uninspected.

The PR206 server creation timestamp is 2026-10-01T05:36:26Z, and the preserved HEAD committer timestamp is 2026-10-01T05:36:15Z. Ferudun's Zenodo record creation is 2026-10-02T07:08:59.065762+00:00, while the paper declares 2 October 2026. These facts do not certify first public availability of every byte, repository visibility history, intellectual independence, literal simultaneity, or absolute priority. The preserved submission identifier is `488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7`; it is provenance, not a priority certificate.

AI tools were used extensively in research, proof development, drafting, auditing, software, and computation. Separate AI adversaries are not independent human peer review. No conventional human refereeing or formal proof-assistant certification is claimed. External works retain their own rights; no third-party full texts, screenshots, dependencies, credentials, private API responses, or internal repository maps are distributed.
