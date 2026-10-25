# Direct Sequence Laws under the Network Multispecies Coalescent: A genealogy equivalence, canonical coalescent-response behavior, and finite determination with an epoch-complexity obstruction: public reproducibility materials

Alec Kriebel. Version 1.0.0, 5 September 2026. DOI: https://doi.org/10.5281/zenodo.22729537. See the main paper and technical supplement for the exact model, observation, parameter domain, quantifiers and theorem proofs.

Companion preprint: [Raw Strongly Tree-Child Level-2 Species Networks from Metric Genealogy Laws under the NMSC: Signed pair co-occupancy, rooted graph reconstruction, and demographic fibers](https://doi.org/10.5281/zenodo.22729545).

This archive contains an explicit technical subset: mathematical implementations, declarative inputs, exact certificates, independently implemented finite checks, and locked dependency records. Original script and mathematical input bytes are retained. Legacy fixture/node names are identifiers, not statements of current theorem scope. Bounded checks support the proofs; they do not certify universal completeness, Borel inversion, analytic continuation or statistical consistency.

## Verify and replay

Extract into a new directory and run the following with Python 3.10 or newer:

```bash
python3 -B verify_public_reproducibility.py
```

For integrity alone, add `--inventory-only`. The runner checks the complete file inventory and every hash before executing research code. Mathematical checks and regenerated outputs run in a new temporary copy, preserving delivered bytes. Write `--report /path/outside-this-directory/result.json` outside the extracted archive.

Add `--full --exact-python /path/to/python-with-pinned-dependencies` to run the canonical exact and negative/mutation suites. The exact dependency versions are in `paper/requirements.lock`; the previously used full environment is in `paper/environment.lock`. No dependencies are downloaded or installed automatically. The full rooted-graph symbolic checks can take several minutes.

The source ZIP is a separate upload file. To rebuild it and compare both main and supplement PDFs byte for byte, provide its download directory and the locked Tectonic runtime:

```bash
python3 -B verify_public_reproducibility.py --build-source \
  --submission-dir /path/to/downloaded-zenodo-files
```

The directory must contain `NMSC_Paper_A_Source.zip`, `NMSC_Paper_A_Main.pdf` and `NMSC_Paper_A_Supplement.pdf`. Their hashes are bound by this archive. The source ZIP contains all four TeX documents and bibliography plus its standalone build script. Source-date epochs are fixed by the runner. Exact PDF byte comparison requires the recorded typesetting environment. The standalone source script uses Tectonic `--only-cached`; the recorded bundle must already be populated in its cache. The supplied replay does not claim a cold-cache build, and no cached dependencies are redistributed.

CC BY 4.0 applies as described in LICENSE.txt. External dependencies are not redistributed.
