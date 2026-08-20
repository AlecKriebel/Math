# Deterministic source-and-certificate bundle

The public scientific archive omits venue metadata, cover letters, portal
checklists, and their static validator.  Those human handoff files remain in
the development package and may contain private metadata in a submission
copy.  The archive retains the manuscript source and PDF, exact certificates,
replay dependencies, project license, public release notes, and research log.
Separate proof notes, provenance memoranda, declarations forms, and venue
handoff files remain only in the development tree.

Run from the Paper II directory:

```sh
./release_bundle.sh
```

The default output is
`output/release/simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz`.
An alternative output path may be supplied as the first argument.  Before
archiving, the script runs the exact scientific replay.  The private
submission validator separately checks submission identity, abstract length,
highlights, placeholder scope, dependency pins, and prior-release wording.

The pinned replay environment is Python 3.14.6 with SymPy 1.14.0 and mpmath
1.3.0.  The deterministic PDF toolchain is Tectonic 0.16.9 and Poppler
26.08.0.  See
`ENVIRONMENT.md` for the exact boundary between theorem replay and document
rendering.

The archive preserves repository-relative paths, but the replay is fully
paper-local.  Its exact public whitelist consists of 17 source files:

- the project license;
- the manuscript source and PDF;
- three copied certifiers under `certificates/` and the paper-level integration
  audit;
- pinned requirements and exact replay, PDF build, and archive scripts; and
- the public README, research log, and release notes.

Synthetic bundle metadata and the internal manifest bring the final archive
to exactly 19 regular members.  The manuscript itself is the analytic proof;
older proof notes and wrappers are deliberately absent because they duplicate
the argument and can retain superseded intermediate wording.

It also excludes discovery scripts, sparse numerical diagnostics, the retired
affine workstream, unrelated research programs, all submission handoff files,
virtual environments, caches, temporary compiler products, rendered QA pages,
and version-control metadata.  Because the whitelist names every file, a new
file created under the paper directory cannot leak into the archive.

Every regular file is recorded in archive-root `MANIFEST.sha256`.  Member
ownership, timestamps, permissions, and ordering are normalized, and the gzip
header has a fixed timestamp and no source filename.  Two generations over
identical inputs are therefore byte-identical.

## Verify after extraction

From the extracted archive root:

```sh
shasum -a 256 -c MANIFEST.sha256
./universal_simultaneous_amplification/phase4_landmark_closure/\
paper_hybrid_threshold/bootstrap_replay.sh
```

`sha256sum` may be used instead of `shasum` where available.  The bootstrap
creates an isolated project-local Python environment, installs the two pinned
libraries, verifies versions, and runs the exact replay.  It does not contact
any person or submit any artifact.  Building and rendering the PDF
additionally requires Tectonic and Poppler.

The exact programs verify finite labelled transition aggregation and exact
symbolic/rational identities.  They do not replace the manuscript's analytic
weak-cut or population-asymptotic proofs.
