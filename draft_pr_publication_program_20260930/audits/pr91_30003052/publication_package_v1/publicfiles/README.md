# The mixed point spectrum of a matrix contraction on its closed unit ball

Alec Kriebel, independent researcher. [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Research note dated 2026-10-05.

The note classifies the point and full spectra of `K_A f = f composed with A` on all continuous complex functions on the closed unit ball of a finite-dimensional complex normed space, for an arbitrary complex norm and a matrix with induced norm at most one. Its precise contribution is an explicit answer to the mixed point-spectrum converse left open after Kari Valentina Küster's 2015 Theorem 3.1.14(i), printed p. 43 / PDF p. 52, and stated only as an inclusion in her 2016 *Pure Koopmanism* Theorem 5(ii), printed p. 321 / PDF p. 25.

The proof makes the peripheral spectral projection contractive in the original norm, factors every unimodular eigenfunction through that projection, and excludes additional peripheral eigenvalues by polynomial approximation and Cesàro averages. This is a short specialization of the classical Jacobs–de Leeuw–Glicksberg mechanism. The all-peripheral, open-disk, stable-only and nilpotent point-spectrum cases are prior work. The full closed disk when a nonzero stable matrix eigenvalue exists already follows immediately from Küster's open-disk inclusion, closedness of spectrum and the operator norm bound. The complete table includes those facts and routine full-spectrum consequences for completeness.

A bounded source audit located no earlier explicit completion in its examined scope. No historical firstness, exhaustive absence, or continuous 2015–2026 openness claim is made. See [PR91_PRIORITY_AUDIT.md](PR91_PRIORITY_AUDIT.md) for the exact target, inspected source families, classical mechanism and ordinary coverage gaps.

## Files and reproduction

The package uses these stable filenames:

- `pr91_note.pdf`: the research note.
- `pr91_note.tex`: standalone LaTeX source with an embedded bibliography.
- `pr91_support.zip`: source, supporting notes, license, and the `verification/` controls, provenance, retained results and reproduction instructions.
- `PR91_PRIORITY_AUDIT.md`: bounded priority comparison and read scope.
- `README.md`: this file.
- `LICENSE.txt`: package license and source-attribution terms.
- `SHA256SUMS.txt`: payload digests.

After extracting `pr91_support.zip`, run from its extracted root, using Python 3.9 or later and SymPy 1.14.0:

```sh
python3 verification/run_all.py --output-dir /a/new/empty/directory
```

Use a new empty output directory for each run. The verification instructions in the archive explain the ordinary and Python `-O` runs and their negative controls. Per mode, the package has **2,720 unique finite controls**: 473 original author controls, 907 independent replay controls, 774 exact/discrete boundary controls, and 566 floating controls. Repeating the same controls in ordinary and optimized modes does not create 5,440 distinct controls.

These checks test finite examples, algebraic identities, projection and nilpotent constructions, and selected numerical boundaries. Floating controls are numerical evidence. Neither exact nor floating finite controls establish an infinite-dimensional spectrum or global literature absence. The self-contained analytic proof in the note establishes the theorem.

The LaTeX source uses standard `article`, AMS, `geometry`, `lmodern`, `microtype` and `hyperref` packages, with no external bibliography or third-party source PDFs required. Referenced source PDFs remain at their primary hosts; they are not redistributed in the package.

## Assistance and review

Extensive AI assistance was used in solving, drafting, literature comparison and adversarial verification. Independent AI tasks checked the peripheral projection, full-spectrum cases and computational controls. The work has not undergone conventional human peer review. This statement does not assert that package assembly, compilation, deposit or subsequent review has already completed.
