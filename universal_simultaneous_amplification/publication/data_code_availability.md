# Data and code availability draft

> **DRAFT — NOT SUBMITTED.** The public versioned release below is the verified
> project archive.  The human author must still approve the wording and add a
> Zenodo DOI if one has been issued before journal submission.

## Portal-ready statement after archival

No empirical datasets were generated or analyzed in this study. All materials
needed to reproduce the exact computations and manuscript build—including the
LaTeX source, transition builders, symbolic proof certificates, verification
scripts, and audit reports—are available in the versioned release
**No universal death–birth amplifier, v1.0.0** at
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
the versioned release at
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
- **DOI status:** a GitHub-triggered Zenodo DOI, if any, must be independently
  checked before it is added to journal metadata.

## Required human actions before submission

- [x] Review the exact files intended for the publication snapshot.
- [x] Run the complete reproduction suite from a clean source archive.
- [x] Commit and push the final Paper I scope according to the repository's
      research workflow.
- [x] Create and verify the intended versioned release.
- [ ] If the repository's GitHub–Zenodo integration is used, verify the
      resulting DOI resolves to the correct snapshot and add it to the journal
      metadata.
- [ ] Make the wording in this file, the submission portal, and
      `paper/main.tex` identical after the human approves the final portal
      entry.
- [ ] Confirm that the public archive excludes `.venv/`, caches, temporary
      render files, and any unrelated or sensitive material.
- [ ] Confirm the archive includes enough environment information to install
      SymPy and the required LaTeX/Tectonic compiler.

## Scope clarification

The computations replay finite-state algebra and exact certificates. They are
verification materials, not empirical evidence replacing the universal
proofs. The unrestricted six-edge weighted K4 search remains labeled as a
finite observation and must not be described as proving that open case.
