# Logarithmic Bray sampling in symplectic and orthogonal groups

Alec Kriebel, ORCID 0009-0001-9320-500X. Unrefereed preprint, version 1.0.0, 22 October 2026.

The manuscript proves separate unconditional c/log(n) strong-eigenspace marginals for the even Bray output for every actual fixed strong involution in natural Sp(V), O(V), SO(V), Omega(V), over all odd finite fields, in sufficiently large dimension. It proves generation of a subgroup containing the actual C_G(t)'' with prescribed confidence using O(log(n)*(1+log(1/delta))) independent uniform samples. Read main.tex or paper.pdf for complete hypotheses, proofs, constants, imported theorems, and limitations.

The GL/GU marginal and generation results, and their SL/SU transfer, are existing work credited to Dixon–Praeger–Seress and Glasby–Praeger–Roney-Dougal. This package does not claim them as new. Its claimed contribution is the Sp/O graph-chart calculation, orthogonal four-sector and square-spinor control, and the fully specified bridge to the centraliser target. Prior class-generation and diagonal-escape strategies are credited. Priority remains subject to the bounded-search limitations in PRIORITY.md and independent review.

## Reproduction

Python 3.10 or newer, standard library only:

    python3 -I -S -B exact_checks.py --expected CHECK_RESULTS.json
    python3 -I -S -B -O exact_checks.py --expected CHECK_RESULTS.json
    python3 -I -S -B -OO exact_checks.py --expected CHECK_RESULTS.json

All three emit the same JSON and fail with a nonzero status on a mismatched expected file. Exact enumeration takes approximately one second on the preparation host. No service, authentication, third-party Python package or random seed is used. The tests cover:

* F_3 symplectic A-dimension two graph fibres in B-dimensions two and four, with full-class unconditional denominators, including mass 4/15 and 80/273.
* F_3 orthogonal A=B dimension two of both relevant B discriminants: the zero-complement constraint is retained and the nonempty case has exactly 16 graphs. A one-dimensional F_7 graph check gives mass 1/2.
* F_3 symmetric self-adjoint operators in dimension three: every admissible squarefree polynomial has 24 operators, and the specified simple primary coefficient discriminant is square for exactly half the operators when another primary exists. This is a trace-form weighting diagnostic, not a finite-dimensional test of the full distinguished-degree-four spinor theorem.
* Every monic polynomial of degree at most eight over F_3: squarefreeness, two forbidden roots, all four sign sectors, exact total and character sums. At degree eight the sector counts are 616,616,616,609.
* Natural SL_2(3) and SL_2(5) orders, centers and derived groups. The former is not perfect and the latter is: small exceptions cannot be silently imported into the large-dimensional theorem. Involutions on the natural symplectic plane are scalar, yielding the Sp_4 boundary obstruction. The closed 2:1 intervals are checked for a<=30.
* A correlated, class-weighted product model with target probability 7/12. Conditional first-success laws and independent-block products are checked exactly with rational numbers. Independence is conditional on the pair of classes, not asserted unconditionally. Four deliberate false numerical statements are rejected.

These diagnostics are independent code written during package preparation. The underlying mathematical claims and earlier independent review experiments predate this code; see PROVENANCE.md. Finite checks do not establish the theorem for untested fields or dimensions. The universal proof is in main.tex and relies on the precisely identified published results in DEPENDENCIES.md.

## Rebuild the files for deposit

From the extracted source folder:

    python3 -I -S -B build_release.py --output /an/absent/output/folder

The output folder must not already exist. The builder checks every source member against source-manifest.json, checks ZIP member bytes and CRCs, and produces the same six release files byte for byte. It copies the frozen paper.pdf; it does not recompile TeX or certify the mathematical result. To compile the editable manuscript, use a conventional LaTeX installation with article, T1 fontenc, lmodern, geometry, amsmath, amssymb, amsthm and hyperref. The preparation used the desktop built-in compiler and an existing read-only cached Tectonic export, with SOURCE_DATE_EPOCH=1792627200 and network disabled. No TeX installation or shared cache modification was made.

The scientific deposit consists of bray-sp-o.pdf and bray-sp-o-source-and-verification.zip. The five-member upload-kit ZIP contains exactly these two files, the metadata JSON, deposit JSON and upload README. The six release products include that kit as well. No operational service tool or credentials are included. The repository's existing top-level Zenodo tool may validate the deposit locally with its check subcommand; staging and publication are distinct operations requiring fresh duplicate and integrity checks.

## Disclosure and licenses

AI tools were extensively involved in the mathematical research, proof development, computational verification, manuscript preparation and auditing. This is a preprint and has not undergone formal independent human peer review. Prose and manuscript: CC BY 4.0. Code: MIT. The supplied licenses apply to the newly authored package; no third-party book, article body, private account capture or closed audit-family payload is redistributed. Preparation by itself neither publishes a record nor assigns a DOI. Operational publication readiness remains false until the required fresh reviews and final adoption occur.
