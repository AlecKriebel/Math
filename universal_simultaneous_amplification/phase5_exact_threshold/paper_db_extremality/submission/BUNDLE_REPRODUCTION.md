# Deterministic source-and-certificate bundle

The public scientific archive omits venue-specific metadata, cover letters,
checklists, and their static submission verifier. Those human handoff files
remain in the development package but may contain private author metadata in
a submission copy. It also omits prior review verdicts, research diaries, and
saved successful output so that a fresh referee is not anchored by earlier
assessments. Their omission does not remove manuscript source, proof
documents, independent audit programs, certificates, replay dependencies,
provenance records, or declarations.

Run the following from the Paper I directory:

```sh
./release_bundle.sh
```

The script creates
`output/release/complete_graph_extremality_db_source_and_certificates.tar.gz`
and the adjacent detached checksum file with suffix `.sha256`; it also prints
the digest. An alternative output path may be supplied as the first argument.
Before archiving, it checks submission identity, abstract length, highlights,
placeholder scope, and release-provenance wording.

The pinned replay environment is Python 3.14.6, SymPy 1.14.0,
python-flint 0.9.0, and mpmath 1.3.0.  The Python wheels are SHA-256-bound in
`requirements-lock.txt`. The deterministic PDF toolchain is Tectonic 0.16.9,
the content-pinned standard v33 bundle, and Poppler 26.08.0. See
`ENVIRONMENT.md` for checks and the boundary between the exact replay and
document rendering.

The archive deliberately preserves the repository-relative path

```text
universal_simultaneous_amplification/
  phase5_exact_threshold/paper_db_extremality/
```

because the internal verifier stage invokes exact certificate families
elsewhere under that project root. The archive contains only the manuscript
package and the source,
tests, certificate families, and project support files reached by the replay;
all seventeen verifier/cross-check programs are invoked directly, without the
project Makefile. It excludes the legacy manuscript build, discovery scripts,
virtual environments, caches,
temporary compiler products, rendered page images, unrelated research
programs, and version-control metadata.

Every other regular archive member is recorded in the archive-root
`MANIFEST.sha256`.
The adjacent `.sha256` file binds the compressed archive as a whole without
creating a self-reference inside that archive.
Tar-member ownership, timestamps, and ordering are normalized, and the gzip
header has a fixed timestamp and no source filename. Running the bundler twice
over identical inputs therefore yields byte-identical archives.

## Certified replay

The sole certified end-to-end command is run from the root of the enclosing
reproducibility package:

```sh
./run_all_referee_checks.sh
```

That launcher verifies exact file and directory sets and every hash, rejects
links, special nodes, and bytecode/cache entries, safely extracts the already
verified regular-file archive into a disposable tree, provisions a fresh
private environment and cache outside the source tree, invokes
`bootstrap_replay.sh` and `replay.sh` as internal stages, rebuilds the PDF, and
requires byte identity with the delivered manuscript.

For manual inspection, `shasum -a 256 -c MANIFEST.sha256` (or `sha256sum -c`)
checks the bytes of listed payloads. It does not reject extra files or
directories and is not a substitute for the certified package launcher. The
bootstrap's explicit `--development` mode is a convenience rather than a
certificate; `replay.sh` is internal-only and rejects standalone invocation.
Neither lower-stage status establishes package identity or execution of the
delivered source. The launcher does not contact anyone or submit any artifact.
Building the PDF additionally requires Tectonic and Poppler's `pdfinfo` and
`pdftoppm` commands.

The exact programs discharge the finite symbolic and rational ranges
explicitly identified in the manuscript and check ingredients of the analytic
arguments.  The universal directed and all-order antisymmetric conclusions are
proved in the manuscript, not inferred from finite executable ranges.
