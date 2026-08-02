# Version 1.0.0 frozen release

This directory is the immutable source package for the original exact result
“A reversible three-species mass-action continuum without a common factor.”
It preserves the ten-complex, twenty-reaction integer-rate construction before
any rate-family strengthening.

Public Version 1.0.0 identifier: [DOI 10.5281/zenodo.21753316](https://doi.org/10.5281/zenodo.21753316).
The immutable repository tag is `wr-continuum-v1.0.0`. The Zenodo date is a
public, citable disclosure date; it is not by itself evidence of mathematical
priority or correctness.

## One-command exact verification

From this directory, run:

```sh
./reproduce.sh
```

The command creates a fresh isolated Python virtual environment, installs the
fully version-locked symbolic dependencies, and runs both exact verifiers. No
floating-point calculation is used as evidence for the theorem.

To rebuild the manuscript PDF, install Pandoc and Tectonic and run:

```sh
./build_pdf.sh
```

The frozen rendered manuscript is `output/pdf/manuscript-v1.0.0.pdf`.

## Contents

- `source/MANUSCRIPT.md`: frozen manuscript source.
- `output/pdf/manuscript-v1.0.0.pdf`: visually inspected rendered manuscript.
- `data/network.csv`: complete directed reaction table.
- `data/original_rates.json`: explicit original twenty-rate vector.
- `data/theorem.json`: machine-readable theorem statement.
- `verifiers/verify_construction.py`: original exact verifier.
- `verifiers/verify_independent.py`: independent clean-room verifier.
- `verifiers/STRUCTURAL_PROOF_AUDIT.md`: independent audit of the three
  structural lower-bound arguments.
- `verifiers/AUDIT_RESULTS.md`: itemized disposition of all twenty audit
  requirements.
- `PRIORITY_AUDIT.md`: targeted post-solution priority audit.
- `AI_AND_HUMAN_VERIFICATION.md`: contribution and verification statement.
- `requirements.lock` and `environment.txt`: locked reproduction environment.
- `ZENODO_METADATA.json`: exact public-record metadata.
- `RELEASE_NOTES.md`: scope and status of the frozen release.
- `SHA256SUMS`: hashes of every payload file other than the checksum file
  itself.
- `dist/`: complete, source, and verifier archives; `dist/SHA256SUMS` hashes
  each archive.

The manuscript is licensed under CC BY 4.0 and the verifier code under the MIT
License.  See the two license files in this directory.
