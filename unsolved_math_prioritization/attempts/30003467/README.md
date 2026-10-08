# Prior negative resolution: pseudo-disk three-coloring

Problem 30003467 / OWR-15427-009, queue rank 998. Disposition: **already_solved, negative, 0/5 author approaches**. Publication checkpoint: 2026-10-08 UTC.

The decisive theorem is due to Gábor Damásdi and Dömötör Pálvölgyi, [*Realizing an m-Uniform Four-Chromatic Hypergraph with Disks*](https://doi.org/10.1007/s00493-021-4846-5), Combinatorica 42 (2022), 1027–1048. It supplies an exactly-m monochromatic disk trace in every three-coloring, for each positive integer m. At m=4 this refutes the primal threshold-four conjecture in [OWR 19/2017, printed p.1173, Conjecture 2](https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1). A single fixed finite family suffices. The elementary finite-family reduction and open-to-closed incidence transfer are in [the deduction](public/PROOF.md).

The published metadata and abstract were verified. The complete relevant proof through Section 3 of [arXiv:2011.12187v1](https://arxiv.org/abs/2011.12187v1) was inspected. The journal PDF was not obtained; byte identity with that version is not asserted. Geometric existence is imported from the credited theorem. The diagnostics do not independently certify a geometric coordinate realization.

## Packet

- `public/`: unchanged, source-free author packet, including proof, provenance, exact claim, zero-turn ledger and diagnostics
- `audit/`: unchanged independent AI acceptance audit and its controls
- `PUBLICATION_ACCEPTANCE.md`: accepted scope and replay limitations
- `VERIFY_PUBLICATION.py`: strict source-free wrapper
- `TEST_MUTATIONS.py` and `MUTATION_RESULTS.json`: disposable-copy adversarial tests and their actual receipt
- `PUBLICATION_MANIFEST.json`: exact inventory; its SHA-256 must be trusted externally

No copied PDFs, extracted source text, images, dataset contents, private sources, personal data, or coordination files are included. The historical audit receipt records source-byte checks performed using separately supplied sources; portable replay never fabricates those checks.

## Reproduction and trust boundary

Python 3.10+ and its standard library suffice. Run as a normal non-root user. First authenticate `VERIFY_PUBLICATION.py` against its separately obtained SHA-256 before executing it; the publication manifest cannot authenticate the program that reads it. Obtain both pins from a trusted receipt or immutable commit. For example, compare `sha256sum VERIFY_PUBLICATION.py` with the trusted wrapper pin, then run:

```sh
python3 -I -B VERIFY_PUBLICATION.py --packet . --expected-manifest TRUSTED_MANIFEST_SHA256
python3 -I -B TEST_MUTATIONS.py --packet . --expected-manifest TRUSTED_MANIFEST_SHA256 --expected-wrapper TRUSTED_WRAPPER_SHA256
```

The first command replays normal, `-O`, and `-OO` diagnostics, full historical adverse controls, and actually unwritable 0444/0555 relocations. The second verifies malformed copies through an external bootstrap that checks wrapper bytes before execution. Repeat the outer commands with `-O` and `-OO` for the full outer-mode matrix. No assertions serve as integrity guards. Files, directories, types, duplicate JSON keys, symlinks, hashes, byte counts, and modes are checked strictly. Only normal baseline 0644/0755 or explicit `--filesystem-profile readonly` 0444/0555 layouts are accepted.

Without `--source-root`, the replay reports `NOT_RUN_NO_SEPARATELY_SUPPLIED_SOURCES`. The historical independent-audit receipt has three source replay runs; the portable expected result differs only by setting that field to zero. If all eight actual external files listed in `public/PROVENANCE.json` are separately supplied, append `--source-root /path/to/sources`. That activates actual complete-file and selected-record byte checks. Missing or mismatched supplied sources cause failure. `--check-only` always reports the source stage as not run.

The finite controls test elementary transfer, small combinatorial cases, scope guards and packet integrity. They do not formally verify the published geometric proof, establish a new result, certify exhaustive literature coverage, or replace human peer review. Replacing both externally trusted anchors and their verifier lies outside this trust model.
