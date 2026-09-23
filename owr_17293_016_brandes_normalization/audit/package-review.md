# Publication package review

Checkpoint: 2026-09-23 04:22 UTC. Completion estimate: **100% of the bounded
content and archive review**; deployment and the final rebuild are root-agent
release checks.

**Verdict:** no required mathematical, attribution, metadata, privacy, or
archive-content correction was identified. The source archive must be rebuilt
after the ongoing builder edit and after adding this review. This is a release
synchronization requirement, not a mathematical defect.

## Scope and content consistency

Reviewed the project README, verification report, website source, Zenodo upload
instructions, metadata object, API-wrapper JSON, citation file, licensing,
research log, package builder, and both generated archives. No new literature
search was performed in this review.

The public statements agree with the independently verified theorem: real
positive-definite homogeneous polynomials of positive degree, a real invertible
basis, symmetric ordered tensor coefficients, unit diagonal, and strictly
positive mixed entries below one. The qualification about multinomial factors
is prominent. Pure equality and the distinction between a real basis and an
integral unimodular or well-conditioned basis are handled correctly.

The universal result is attributed to the analytic proof; finite rational
checks are consistently presented as supplemental rather than formal
verification of the existence theorem. I reran the exact verifier successfully:
12 certificates, 120 coefficient classes, 110 polarization cross-checks, degrees
2 through 24 in the finite symbolic check, and two negative controls. These
numbers agree with the README, report, site, and verifier documentation.

The priority language matches the bounded audit: no earlier full resolution
was found, but first priority is not established. The 2015 precursor is credited,
the 2019 primary problem is identified, AI assistance is disclosed, and external
peer review is not claimed. The metadata and upload instructions contain no
invented DOI, Zenodo deposit ID, journal acceptance, funding, or external review.

Title, author, version 1.0, publication date 2026-09-23 (UTC), and ORCID
0009-0001-9320-500X are consistent across the paper-facing files. The metadata
copies agree exactly as JSON objects; the API wrapper contains the same object
under `metadata`. Existing DOI references identify the two cited antecedents,
not this preprint. Licensing distinguishes CC BY 4.0 prose from MIT code.

The metadata was checked for internal consistency and absence of spurious
identifiers. No deposit was submitted as part of this audit; remote API/form
acceptance is not being certified.

## Archive and link checks

The inspected source archive had 39 files, including its manifest; its SHA-256
was `adf0ce285176c000359170d202271f6ebd293d2e9626fb8b50c36b8cf7f920b1`.
The inspected outer kit had eight files; its SHA-256 was
`a54c9ec36982926e382aeec62b8a9ba2a0ee7a47aec86f794389cb5457e50691`.
These identify the **pre-final-build snapshot**, not the archive that will include
this review.

- Both ZIP CRC checks passed. All 38 source-manifest entries and all seven
  kit-manifest entries matched the archived bytes. No unmanifested payload file
  was present.
- The kit's nested source archive matches the standalone source archive, and
  the paper is included both as a convenient upload file and in the source
  archive.
- All five local website-download checksums passed. Every local download link
  from `site/index.html` resolves in the generated website directory.
- Archive member paths are relative and have no parent traversal. No Git
  metadata, temporary render files, caches, unrelated project files, third-party
  PDFs, account credentials, or private correspondence were included.
- The builder uses an explicit project-file selection plus constrained audit,
  source-metadata, and verifier globs. It does not execute an upload, publish a
  release, or contact any individual.

The source archive intentionally contains website source rather than a recursive
copy of its own downloadable ZIPs. Its documented rebuild command generates
the website downloads and Zenodo kit after extraction. The paper, verifier,
examples, proof reviews, source inventory, and upload metadata are usable without
rebuilding. The outer kit clearly tells the user to upload `paper.pdf` and
`source-and-verification.zip` and explains that uploading JSON does not populate
Zenodo's metadata form.

At inspection, the only mismatch between the source manifest and the current
working files was `build_package.py`, which was being edited during the release
checks. A final rebuild must refresh the source manifest, both archives, and
website copies after this review and the final research-log checkpoint are
complete. Root should confirm the resulting checksums and actual public URL;
those live deployment checks are outside this content audit.
