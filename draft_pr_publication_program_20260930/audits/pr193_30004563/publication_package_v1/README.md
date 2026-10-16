# Five outgoing centers in a 16-realization cube move — draft package

Author: Alec Kriebel, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

The draft proves existence of one fixed admissible incoming alpha=16 realization with at least five distinct outgoing centers. It addresses the crossing-allowed realization and common-focus construction-curve setting of Melotti–Ramassamy–Thévenin, published Remark 4.8. The fixed boundary is crossed, excluding every proper embedding for this drawing. The exact total count, a universal maximum and alpha<1 are not determined.

The bounded literature search through 15 October 2026 located no earlier pure-power shared-focus counterexample with at least four intersections in its checked corpus. Historical priority remains unestablished. The draft credits the earlier Ash–Bolker weighted-distance and Bourne–Peletier–Roper/Bourne–Roper p-power families and makes no novelty, firstness, independent-discovery, current-openness or publication-readiness claim. AI was used extensively in the work. It is unrefereed and has not received conventional human peer review.

## Contents

- `five_centers_draft.tex`: self-contained research-note source; not compiled during this draft-preparation assignment.
- `verify_five_centers.py`: standard-library-only exact verifier.
- `exact_certificate.json`: full rational endpoint, algebraic-boundary, determinant, crossing and center enclosures.
- `verification_stdout.txt`: successful default verifier output.
- `SOURCE_REFERENCES.json`: verified primary reference metadata; no primary PDFs or text derivatives are included.
- `AUTHOR_METADATA_DRAFT.json`: provisional title, description, author and license data; not a service upload schema.
- `STATIC_CHECKS.json`: source/TeX structure checks and default-mode read-only verification.
- `PUBLICATION_STATUS.json`, `OPEN_DECISIONS.md`, `RESEARCH_LOG.md`: explicit draft status, pending decisions and preparation record.
- `LICENSE.txt`, `SAFE_ALLOWLIST.txt`, `SHA256_MANIFEST.json`: license and exact package custody.

## Reproduce the exact verification

Run Python 3 with the script path:

```text
python3 verify_five_centers.py
```

The default mode recomputes the complete certificate and compares it to the sibling `exact_certificate.json`. It writes no files, works from any working directory, and succeeds for a read-only package. It prints `PASS_AT_LEAST_FIVE_ALPHA16_WITH_INCOMING_REALIZATION` only after the checks and exact certificate comparison succeed. All data deciding validity are integers or rational `Fraction` values. No external package, network connection, original submission file, audit file or floating-point decision is used. Checks use explicit exceptions and remain active with Python optimization.

For a deliberate regeneration in a writable copy:

```text
python3 verify_five_centers.py --write-certificate
```

That option writes only its sibling `exact_certificate.json`. Root bounds use exact integer eighth-power binary search on a 10^36 lattice. Boundary parameters are enclosed by 128 exact bisections, and each outgoing sign bracket by 100 further bisections. The final cutpoint is **10^16 throughout this package**. Its negative G value is certified by concavity with u=100 exactly, not by subtracting nearly equal radicals.

The manuscript supplies the IVT, root uniqueness, distance equivalence, exact telescope and all six face identities. Interval residuals merely containing zero are never treated as proofs of equality. The five disjoint sign brackets establish at least five centers without asserting uniqueness inside them. Internal condition counts are implementation bookkeeping rather than counts of independent propositions.

The JSON records all exact rationals as strings. `decimal_grid_enclosure` also contains rational strings and is only a concise outward enclosure. No decimal approximation is authoritative over the exact rational intervals.

## License

CC BY 4.0; see `LICENSE.txt`. This license covers this draft and its original support artifacts, not linked third-party works. No source PDFs, rendered primary pages, credentials, external correspondence or unrelated work are included.
