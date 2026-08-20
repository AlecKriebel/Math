# Deterministic source-and-certificate bundle

The public scientific archive omits venue-specific metadata, cover letters,
checklists, and their static submission verifier. Those human handoff files
remain in the development package but may contain private author metadata in
a submission copy. Their omission does not remove manuscript source, proof
certificates, replay dependencies, provenance records, or declarations.

Run the following from the Paper I directory:

```sh
./release_bundle.sh
```

The script creates
`output/release/complete_graph_extremality_db_source_and_certificates.tar.gz`
and prints its SHA-256 digest. An alternative output path may be supplied as
the first argument. Before archiving, it checks submission identity, abstract
length, highlights, placeholder scope, and release-provenance wording.

The pinned replay environment is Python 3.14.6, SymPy 1.14.0, and
python-flint 0.9.0. The deterministic PDF toolchain is Tectonic 0.16.9 and
Poppler 26.08.0. See `ENVIRONMENT.md` for checks and the boundary between the
exact replay and document rendering.

The archive deliberately preserves the repository-relative path

```text
universal_simultaneous_amplification/
  phase5_exact_threshold/paper_db_extremality/
```

because `replay.sh` invokes exact certificate families elsewhere under that
project root. The archive contains only the manuscript package and the source,
tests, certificate families, and project support files reached by the replay;
it excludes the legacy manuscript build, discovery scripts, virtual environments, caches,
temporary compiler products, rendered page images, unrelated research
programs, and version-control metadata.

Every regular file is recorded in the archive-root `MANIFEST.sha256`.
Tar-member ownership, timestamps, and ordering are normalized, and the gzip
header has a fixed timestamp and no source filename. Running the bundler twice
over identical inputs therefore yields byte-identical archives.

## Verify after extraction

From the extracted archive root:

```sh
shasum -a 256 -c MANIFEST.sha256
./universal_simultaneous_amplification/phase5_exact_threshold/\
paper_db_extremality/submission/bootstrap_replay.sh
```

On a platform providing `sha256sum`, it may be used instead of `shasum`.
`bootstrap_replay.sh` creates an isolated project-local Python environment,
installs the pinned dependencies, and runs the exact replay. It does not
contact anyone or submit any artifact. Building the PDF additionally requires
Tectonic and Poppler's `pdfinfo` and `pdftoppm` commands.

The exact programs verify finite symbolic and rational identities supporting
the analytic arguments. They do not replace the all-order proofs printed in
the manuscript and certificate notes.
