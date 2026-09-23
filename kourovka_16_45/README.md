# A counterexample to Kourovka Notebook Problem 16.45

Alec Kriebel · ORCID https://orcid.org/0009-0001-9320-500X

Version 1.0.1 · 23 September 2026 · Unrefereed preprint

For the explicit group

    G = F_29^2 semidirect H,
    H = < [[0,28],[1,0]], [[2,7],[12,28]] > <= SL(2,29),

with the natural column-vector action, the manuscript proves

    |G| = 100920,   b_f(G) = b(G) = 3 < 4 = mu′(G).

The base invariant maximizes **inclusion-minimal** base size over **all**
permutation representations, including nonfaithful and intransitive actions.
A base has pointwise stabilizer equal to the action kernel. The invariant
mu′ permits independent subsets not generating G. No minimum-order claim
is made.

## Read first

- `proof.pdf` and `proof.tex`: revised manuscript and editable source.
- `preprint_review_2026_09_23/REVIEW_SUMMARY.md`: current adversarial review and repair record.
- `audit_2026_09_21/VERIFICATION_REPORT.md`: historical initial independent audit.
- `data/group_spec.json`: exact group and witness specification.
- `submission/UPLOAD_GUIDE.md`: complete manual Zenodo deposit instructions.
- `submission/metadata.json`: copy-ready descriptive metadata.
- `CITATION.cff`: citation metadata, without an invented DOI.

Public paper page: https://aleckriebel.github.io/Math/papers/kourovka-16-45/

The upper bound is structural. Every subgroup missing V=F_29^2 has faithful
base invariant at most two. Restriction bounds faithful bases of G by three.
Every nontrivial normal subgroup contains V, so nonfaithful actions factor
through H. The argument covers all actions without enumerating G's full
subgroup lattice.

## Reproduce

Requirements: Python 3.10 or newer (standard library) and a C++17 compiler.
From this directory:

```sh
make verify
python3 audit_2026_09_21/independent_check.py
python3 audit_2026_09_21/structural_check.py
python3 audit_2026_09_21/compare_independent.py
python3 submission/test_package.py
```

Do not use `python -O` for the additional audit scripts: their assertions
perform checks. The principal supplied verifier uses explicit checks even
under optimization. `make verify` writes fresh outputs to `build/` and
compares the Python and C++ subgroup sets. The independent scripts recreate
finite groups from the printed specification; they update their timestamped
result files when rerun. Check archive hashes before rerunning.

The exact checks enumerate all 76 actual complement subgroups, examine
1,215,450 quadruples and 67,525 triples, reconstruct the affine group of order
100920, and verify the independent four-set and faithful three-family.
They also check the characteristic-11 example where the claimed bound fails.
No GAP, Sage, optimizer, group catalogue, or network access is required.

Build the PDF with `make pdf` (pdfLaTeX or Tectonic). The publication PDF was
built with Tectonic. Rebuild the source archive and manual upload kit using
`python3 submission/build_package.py` after preparing the final PDF.

## Audit outcome and correction

Separate AI agents reviewed the structural proof, wrote an additional exact
checker before reading the supplied implementations, and checked primary
sources. No unresolved substantive gap was identified. One numerical error
was corrected: R1 R3 has order **3**, not 6. The generated pair subgroup
has order 12 as claimed, so all theorem statements remain unchanged.
The initial publication added author metadata, a proof overview, Cameron's
2024 account, attribution, and review disclosures. Version 1.0.1 clarifies
which projective pairs generate the dihedral subgroups and explains the
intersection-order argument. It also rebuilds upload kits from explicit file
lists, so stale files from an earlier build cannot enter a new kit.
The new review directory records two sequential fresh adversarial reviews and
the disposition of every actionable finding. The second reviewer found zero
actionable issues in the revised proof and reproducibility package.

The checks are independent AI work lanes in this task, not external human
peer review or complete proof-assistant verification. The source audit found
no earlier resolution in its bounded search; bibliographic priority is not
guaranteed. The mathematical upper bound must be checked in the manuscript,
not inferred merely from passing finite computations.

## Package contents and provenance

`data/certified/` contains the supplied exact certificates. Matrices are
row-major; indices in `finite_certificate.json` reference its matrix array.
The new `audit_2026_09_21/` reports and canonical subgroup set independently
corroborate these certificates. The first audit used UTC timestamps on
22 September (21 September locally); the additional preprint reviews and
version 1.0.1 are dated 23 September.

Original research logs and exploratory data are retained for provenance.
They are historical, not current publication status. Exploratory code uses
NumPy/SciPy but is not a premise of the proof or needed by the final checks.
`audit_2026_09_21/input_*` and `original_proof.tex` preserve the original
bundle metadata and manuscript; the latter contains the corrected-in-current-
edition product-order error. The input metadata does not govern current
publication authorization.

`SHA256SUMS` covers the current source release. `manifest.json` lists the
same payload files and checksums. The source archive excludes temporary
build products, duplicated output archives, and third-party source PDFs.
The manual Zenodo kit contains the revised PDF, self-contained source ZIP,
checksums, citation metadata, deposit description, and upload guide.
No GitHub release, Zenodo deposit, or DOI has been created by this task.
