# Current archive comparison — retrieved 21 September 2026 UTC

This comparison uses the files downloaded directly from the Zenodo record file-content endpoints, not website descriptions. `archive_current/manifest.json` records each URL, byte count, SHA-256, declared Zenodo MD5, and retrieval timestamp. All declared MD5s matched. The corresponding latest-version API endpoints were queried separately and still identify the same four records at the recorded time.

| Artifact | Directly retrieved record | Current file |
|---|---|---|
| Publication PDF | [21699161](https://zenodo.org/records/21699161) | version 1.1.0, 238,228 bytes |
| Review PDF | [21699069](https://zenodo.org/records/21699069) | version 1.1.0, 251,541 bytes |
| Manuscript source | [21699181](https://zenodo.org/records/21699181) | version 1.1.0 source tar, 36,142 bytes |
| Software | [21699224](https://zenodo.org/records/21699224) | version 1.1.0 ZIP, 633,606 bytes |

The downloaded software ZIP contains **zero `.lean` files**; its full membership is saved in `archive_current/software_file_list.json`. Therefore the new local Lean development and its expanded bridges are not part of that currently retrieved software artifact. This is a statement about the checked records/files at retrieval, not all possible archives or later updates.

The downloaded source and PDFs precede the corrected explicit Lorentz-signature condition and the new verification/model-convention exposition. The source comparison at fetch is recorded in `archive_current/source_comparison_at_fetch.json`; the retained fetched files permit independent comparison with the final staged source. Current changes are summarized in [VERSION_2.md](../VERSION_2.md).

The local version 2 candidate includes the newly checked principal formalization and model bridges, aligned manuscript/PDFs, fresh run-specific receipts, and source/package hashes. The existing records and their version-specific DOIs remain historical. No new version has been uploaded and no future DOI is represented as assigned.
