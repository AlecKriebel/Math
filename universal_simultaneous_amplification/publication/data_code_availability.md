# Data and code availability draft

> **DRAFT — NOT SUBMITTED.** The public versioned release below is the verified
> project archive.  The human author must still approve the wording before
> journal submission.

## Portal-ready statement after archival

No empirical datasets were generated or analyzed in this study. All materials
needed to reproduce the exact computations and manuscript build—including the
LaTeX source, transition builders, symbolic proof certificates, verification
scripts, and audit reports—are available in the versioned release
**No universal death–birth amplifier, v1.0.0** at the version DOI
<https://doi.org/10.5281/zenodo.21753405>, with scoped release assets at
<https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>.
The development repository is
<https://github.com/AlecKriebel/Math>. The relevant project directory is
`universal_simultaneous_amplification/`. The software snapshot is licensed
under the MIT License. The command `make paper1` runs the Paper I verification
suite and rebuilds the manuscript when the pinned Python dependency and the
document compiler described in the repository are installed.

## Short portal variant

No empirical datasets were generated or analyzed. The manuscript source,
exact code, proof certificates, and reproduction instructions are archived in
the v1.0.0 Zenodo record at
<https://doi.org/10.5281/zenodo.21753405>, with scoped assets at
<https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>
and developed at
<https://github.com/AlecKriebel/Math> under
`universal_simultaneous_amplification/`.

## Release facts checked on 2026-08-01

- **Verified:** the configured remote is
  `https://github.com/AlecKriebel/Math.git`.
- **Verified:** the project contains exact transition code, unit tests,
  independent verification scripts, hostile-audit reports, manuscript source,
  `requirements.txt` pinning SymPy 1.14.0, a `Makefile` with the `paper1`
  reproduction target, and an MIT License.
- **Verified:** the manuscript states that no empirical data are used.
- **Verified for project publication:** release
  `universal-db-obstruction-v1.0.0` contains the manuscript PDF, editable
  source, the full reproducibility tree, and an exact checksum manifest.
- **Verified from a clean source archive:** `make paper1` passes with Python
  3.14.6, SymPy 1.14.0, and Tectonic 0.16.9.
- **Separate journal status:** no journal upload or submission has been made.
- **Verified DOI:** `10.5281/zenodo.21753405`; the public Zenodo record reports
  version `universal-db-obstruction-v1.0.0` and links to the exact GitHub tag.
- **Verified concept DOI:** `10.5281/zenodo.21753404`.

## Required human actions before submission

- [x] Review the exact files intended for the publication snapshot.
- [x] Run the complete reproduction suite from a clean source archive.
- [x] Commit and push the final Paper I scope according to the repository's
      research workflow.
- [x] Create and verify the intended versioned release.
- [x] Verify that the GitHub–Zenodo DOI resolves to the correct release tag and
      add the version DOI to this draft.
- [ ] Make the wording in this file, the submission portal, and
      `paper/main.tex` identical after the human approves the final portal
      entry.
- [x] Confirm that the scoped release assets exclude `.venv/`, caches,
      temporary render files, unrelated projects, and sensitive material. The
      automatic Zenodo snapshot separately preserves the public monorepository.
- [x] Confirm the scoped archive includes enough environment information to install
      SymPy and the required LaTeX/Tectonic compiler.

## Scope clarification

The computations replay finite-state algebra and exact certificates. They are
verification materials, not empirical evidence replacing the universal
proofs. The unrestricted six-edge weighted K4 search remains labeled as a
finite observation and must not be described as proving that open case.
