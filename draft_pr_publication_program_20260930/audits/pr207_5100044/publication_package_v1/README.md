# A telescoping verification of a focal-inversion area invariant

Alec Kriebel, ORCID 0009-0001-9320-500X. Manuscript dated 16 October 2026.

The note verifies the focal-inversion area product for strict nondegenerate confocal elliptical billiards of **least collision period divisible by four**, including coprime stars. Areas are algebraic shoelace areas in trajectory order; inversion is in a unit circle about an original focus and the inverse vertices are joined by straight segments.

The exact positive theorem and the repeated-list limitation are credited to Alper Ferudun, DOI **10.5281/zenodo.23093706**. That DOI identifies the cited prior preprint. The local/cyclic master identities and generalized Landen transformation are classical and credited in the manuscript. This package makes no theorem or method novelty, firstness, independence, simultaneous-discovery or current-openness claim.

A repeated shorter orbit can have a displayed list length divisible by four while failing the product invariant. The note and exact checker give two least-period-three billiards in one forward family, repeated four times, whose products differ by `-20 sqrt(6)/9`. Their least period remains three.

Contents:

- `focal_inversion_area.tex`: mathematical note, with full local identity and Fourier proof.
- `verification/`: current portable exact checker, Euclidean ray diagnostic, pinned requirements, recorded results and meaningful failure controls. Its README explains every program and the deliberately damaged test fixtures.
- `TIMELINE.json`: exact observed GitHub/Zenodo record dates and their limits.
- `VERIFICATION_REPORT.md`: scope and evidence summary.
- `METADATA.json`: exact intended Zenodo metadata, also supplied separately.
- `LICENSE.txt`: attribution license for this note and its authored support files.

The separately supplied PDF is the reading copy. A TeX installation may build the source; the recorded build used Tectonic with cached resources and shell execution disabled by `--untrusted`. For example:

```sh
tectonic --untrusted --keep-logs focal_inversion_area.tex
cd verification
python -m pip install -r requirements.txt
python verify_exact.py
python diagnose_geometry.py
python validate_fail_closed.py --run-directory my_new_validation
```

The checkers use stdout by default and refuse replacement of existing `--output` files. Exact algebra certificates support finite identities. Numerical diagnostics use reflected Euclidean rays and actual squared-distance focal inversion; they are finite floating-point checks, without interval enclosures or a uniform conditioning theorem. The analytical argument supplies the universal conclusion.

AI tools were used extensively. This is an unrefereed preprint without conventional human peer review or proof-assistant formalization. Full external source papers and private acquisition records are excluded. Broader audit and whole-package review records are maintained in the PR207 case audit in the repository.

Copyright 2026 Alec Kriebel. CC BY 4.0.
