# Planar Delone ambient extension: credited prior resolution

Problem **6600014 / AMR-065-0014**, queue rank **734**. Status **already_solved**, **1/5** approaches, **zero original-solution credit**. Independent audit: **PASS**.

Michael Dymond and Vojtěch Kaluža, *Planar bilipschitz extension from separated nets*, Journal of the London Mathematical Society **113(4) (2026), e70540**, [DOI 10.1112/jlms.70540](https://doi.org/10.1112/jlms.70540), resolve Navas's exact planar question. Applying their extension theorem to the inverse lattice bijection and then inverting the ambient extension proves the desired rectification.

- [Complete reduction and surjectivity argument](author/RESOLUTION.md)
- [Scope and elementary negative controls](author/SCOPE_AND_CONTROLS.md)
- [Independent audit](audit/AUDIT_REPORT.md)
- [Current classification](release_status.json)

The theorem is imported as a published result. Neither this package nor its audit independently verifies the full 34-page published proof. Finite exact checks support the stated controls; they do not prove the universal extension theorem.

Both frozen packages and their archives are unchanged. Pre-audit pending/no-remote-write statements inside the author freeze describe its historical preparation stage. The independent audit and current classification supersede those historical status fields without rewriting the freeze.

Source metadata records six independently retrieved PDF hash/size matches, inspection limits, the live-catalogue HTTP 403, and the publication-date discrepancy: publisher/Birmingham 23 April 2026 versus ISTA 1 April 2026. PDFs and extracted source text are not redistributed.

## Reproduce

Run `python verify_release.py` from any working directory. It checks all publication bytes, archive membership, frozen manifests, current classification, the author checks in ordinary Python mode, and the independent audit. It uses only the standard library and performs no network requests or writes. The release wrapper and audit also work with `python -O verify_release.py`; the assertion-based author script is always launched separately with assertions enabled. An optimized author run is never treated as verification.

`PUBLICATION_MANIFEST.json` binds the safe publication files except itself; its external hash is recorded with publication verification. Hashes prove byte consistency, not the mathematical theorem or authorship.
