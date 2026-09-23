# A coefficient normalization for positive definite forms

Alec Kriebel · version 1.0 · 23 September 2026 (UTC)

**Verification verdict:** the supplied candidate is a complete analytic proof of the real change-of-basis assertion in Brandes's Problem 11, Oberwolfach Report 50/2019, p. 3182, under the symmetric ordered-coefficient convention. The paper proves the stronger conclusion that diagonal entries can be one and all mixed entries lie strictly between zero and one. The original report includes absolute values.

**Priority verdict:** no earlier full resolution was found in a bounded public-literature audit. Brandes (2015) is an essential precursor. This is an unrefereed AI-assisted preprint; neither external peer review nor first priority is claimed.

- [Read the three-page paper](output/pdf/paper.pdf).
- [Public project page](https://aleckriebel.github.io/Math/papers/brandes-coefficient-normalization/).
- [Verification report and proof map](audit/verification-report.md).
- [Priority audit](audit/priority-audit-independent.md).
- [Independent Cauchy–Schwarz proof](audit/independent-geometry.md).
- [Zenodo upload instructions and copyable metadata](zenodo/UPLOAD.md).

## Fresh preprint review

Three fresh adversarial review rounds reassessed the paper and supporting calculations. An auxiliary negative-control coefficient introduced in Round 2 was corrected and checked by direct evaluation and polarization; the paper and original verifier were unaffected. The final fresh review found no actionable remaining findings; the paper remains version 1.0. The [review decision](audit/preprint-readiness.md) records all findings and dispositions. The refreshed verification archive and Zenodo kit include the reports and runnable supplementary checks.

## Verify in seconds

```
python3 verification/verify.py
```

Python 3.9+; no third-party dependencies. The exact checks cover 12 rational examples and 120 symmetric coefficient classes, with 110 independent polarization cross-checks, 23 finite symbolic identity checks, and two rejection controls. See [the verifier's scope](verification/README.md): the script verifies finite proposed bases, while the short analytic proof establishes existence for every positive definite form.

## Read the proof

The paper gives a complete proof by expanding a polynomial gap near a sphere-minimizing direction. For each mixed tuple its quadratic coefficient is strictly positive. Finitely many inequalities therefore hold for one sufficiently small perturbation of a basis. The separate geometric proof replaces this expansion with positive definite bilinear slices, Cauchy–Schwarz and a finite maximum argument.

The assumptions are m >= 1, positive even degree d >= 2, and p(x) > 0 away from zero. The matrix is real and invertible. Ordinary monomial coefficients include multinomial multiplicities; they are not the ordered tensor entries. No conditioning bound or integral-unimodular assertion is made.

## Rebuild

With Tectonic installed, run `tectonic --outdir output/pdf manuscript/paper.tex` from this folder. Then `python3 build_package.py` rebuilds the deterministic source archive, manual Zenodo kit, and local website downloads. With a conventional TeX installation, compile `manuscript/paper.tex` twice using pdfLaTeX into `output/pdf` instead.

For repository maintainers, `python3 build_package.py --deploy-docs` also copies the site to this repository's `docs/papers/brandes-coefficient-normalization/`. It does not commit, push, contact anyone, upload to Zenodo, or create a GitHub release.

## Contents and provenance

`manuscript/` holds editable LaTeX; `verification/` has the standard-library script and rational certificates; `audit/` holds the original-proof review, independent derivation, final review and priority search; `sources/` authenticates the original report by URL and hash; `zenodo/` contains deposit fields and generated files. Third-party PDFs are not redistributed. The original candidate came from generative AI supplied by the user; AI assisted the independent internal checks, research and writing.

Paper and prose: CC BY 4.0. Code: MIT. [Licenses](LICENSES.md). Author ORCID: https://orcid.org/0009-0001-9320-500X. No DOI is assigned in this package.
