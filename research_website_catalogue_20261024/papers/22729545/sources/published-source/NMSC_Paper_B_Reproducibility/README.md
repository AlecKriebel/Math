# Raw Strongly Tree-Child Level-2 Species Networks from Metric Genealogy Laws under the NMSC: Signed pair co-occupancy, rooted graph reconstruction, and demographic fibers: public reproducibility materials

Alec Kriebel. Version 1.0.0, 5 September 2026. DOI: https://doi.org/10.5281/zenodo.22729545. See the main paper and technical supplement for the exact model, observation, parameter domain, quantifiers and theorem proofs.

Companion preprint: [Direct Sequence Laws under the Network Multispecies Coalescent: A genealogy equivalence, canonical coalescent-response behavior, and finite determination with an epoch-complexity obstruction](https://doi.org/10.5281/zenodo.22729537).

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

The directory must contain `NMSC_Paper_B_Source.zip`, `NMSC_Paper_B_Main.pdf` and `NMSC_Paper_B_Supplement.pdf`. Their hashes are bound by this archive. The source ZIP contains all four TeX documents and bibliography plus its standalone build script. Source-date epochs are fixed by the runner. Exact PDF byte comparison requires the recorded typesetting environment. The standalone source script uses Tectonic `--only-cached`; the recorded bundle must already be populated in its cache. The supplied replay does not claim a cold-cache build, and no cached dependencies are redistributed.

## Optional bounded Tier 0

The clean `tier0/` subset includes independent implementations, six small input manifests, dependency locks and twelve mathematical outputs. Run `--tier0 --tier0-python /path/to/compatible-python` for all twelve fresh jobs, without resume. This runtime requires Python >=3.11,<3.14, SymPy 1.14.0 and NetworkX 3.5, distinct from the legacy canonical suite's dependency record. Each regenerated mathematical output must match the archived value. No old checkpoints or execution logs are distributed, and no higher-tier completion is claimed.

CC BY 4.0 applies as described in LICENSE.txt. External dependencies are not redistributed.
