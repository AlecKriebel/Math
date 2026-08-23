# Package inventory

## Integrity baseline

- Source packet: `external_audit/full_referee_validation_packet_v1.0.7/`
- Untouched audit snapshot: `source_snapshot/`
- Execution copy: `working_packet/`
- Regular files: 264 (the outer manifest covers 263 files and excludes itself).
- Outer supplied manifest: fully verified before execution.
- Inner supplied manifest: fully verified before execution.

Detailed file-type, component, prerequisite, path, and network-dependency inventories follow after static inspection.

## Counts and components

| Component | Regular files | Contents/evidentiary role |
|---|---:|---|
| Packet metadata/orchestration | 8 | contents/provenance/environment/readme material, outer manifest, shell/Python runners; instructions here were treated as attached material, not as authority overriding the user's request |
| `paper/` | 2 | definitive reading PDFs; byte-identical to repository manuscript PDFs |
| `review_maps/` | 7 | author-provided navigation aids only; not used to construct this audit's dependency map |
| `minimal_verifier/` | 48 | 47 verifier/certificate files copied from `repository/independent_verifier/` plus a replay script; README differs; this is not an independent implementation |
| `repository/` | 199 | full executable source/data/manuscript/proof package, including its manifest |

Packet-wide extensions: 99 Python files, 39 TeX files, 37 CSV files, 34 JSON files, 20 text files, 18 Markdown files, 10 PDFs, 3 shell scripts, one bibliography, one compiled bibliography, one citation metadata file, and one license without an extension.

The repository's 199 files comprise:

- 6 manuscript files (`main.tex/.pdf/.bbl`, `supplement.tex/.pdf`, bibliography);
- 27 detailed proof-audit TeX aids and 2 external-audit TeX summaries;
- 47 verifier files, of which 38 match the advertised executable filename patterns;
- 11 computation/generation/audit/test files;
- 66 exact, tabular, and numerical data files;
- 9 figure sources/artifacts;
- 6 literature-audit files;
- 17 stored verification-output/provenance files;
- repository metadata, requirements, replay script, and inner manifest.

There are no symlinks. Thirteen submitted files carry executable permission, but the runners invoke Python files explicitly and do not rely on those mode bits.

## Integrity and duplication findings

- Outer manifest SHA-256 (the one file not self-covered): `9cce0ed2d5f63efd121e92eb846f5bc404351aa1bf327c6af51afc9e4277c43c`.
- Independent aggregate over relative path, NUL delimiter, file SHA-256, and newline for all 264 pristine files: `ae955f478dabf85cc3731b57cfa4aebe631d7977df04bdc5e39b271d112aebf5` (2,580,258 bytes).
- `paper/main.pdf` equals `repository/manuscript/main.pdf` byte for byte; the same is true for the supplement.
- Every substantive minimal-verifier source/certificate matches its repository counterpart byte for byte. Only the README differs, and only the minimal copy has `replay.sh`. Thus the two replays are useful packaging variants, not implementation-independent evidence.

## Reproducibility risks found before execution

- `requirements.txt` uses unpinned lower bounds and has no resolver lock or hash pins.
- LaTeX package versions and the TeX distribution are unpinned; the recorded successful Biber version differs from this host's version.
- The wrapper assumes literal commands named `python`, `pdflatex`, and GNU-style utilities are on `PATH`; it does not create or select a virtual environment.
- The full replay rewrites `sha256_manifest.txt` after regeneration and then verifies the newly written manifest. That final check establishes internal self-consistency of the regenerated tree, not equality with the original release. Independent pre/post comparisons are therefore required.
- Stored files under `verification_outputs/` are baseline provenance only and are excluded as independent evidence in this audit.
- No private path, missing author input, or runtime network call was found by static source/path scanning. Third-party publications are not included and remain citation-dependent evidence where the proof invokes them.
