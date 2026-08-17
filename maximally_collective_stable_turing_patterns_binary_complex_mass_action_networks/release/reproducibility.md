# Reproducibility

## Portable public replay

The replay intended for an ordinary third-party download is self-contained:

```bash
cd public/repository
bash replay.sh
```

It has no dependency on historical source archives. It regenerates the current
finite data and printed tables, checks every all-dimensional certificate, runs
the mutation tests and numerical illustrations, rebuilds the figures and
manuscript PDFs, and applies the PDF semantic gate. Use
`FINAL_RELEASE_QUICK=1 bash replay.sh` only as a smoke test; release
qualification uses the full command.

## Full provenance replay and its external prerequisites

The top-level provenance replay additionally verifies five historical-lineage
archives. They are not included in the downloadable final ZIP. Place the files
below in `/mnt/data`, or set `FROZEN_BASE` to the directory that contains them.

| Required filename | SHA-256 |
|---|---|
| `qbio_mass_action_turing_final_flagship.zip` | `e3c116643e566f905ae72aa2556874319db1845d88520e646c2c88f295dd1e0e` |
| `qbio_mass_action_turing_all_spectrum_paper.zip` | `56db8bb8b3e2f23bfa4066a7f1a0c6432f75e50cf71ae742713d23d406cf9b96` |
| `qbio_mass_action_turing_all_spectrum_stable.zip` | `d084e646181f455b80aa336e8448f52cdb9afdb6e3351575f1442595ef65e861` |
| `qbio_mass_action_turing_diffusion_design.zip` | `61d9ff96b0c5bbf74d80bc2b640afcdc23a7f429e8abb0478cd35903b3df0d90` |
| `qbio_mass_action_turing_nonlinear_frontier.zip` | `816dbb043f859d60cf6a32af45bfc7ab2ec46edd75cf51b56eae5bed5345077c` |

Then run, from the corrected project root:

```bash
bash release/one_command_replay.sh
```

The archives are lineage evidence only. The startup preflight hashes them but
does not extract them, and no current proof, data-generation, document-build,
or packaging stage reads them. The preflight checks all five archives and the
required executables and Python dependencies before opening
`release/replay.log`; a missing prerequisite therefore cannot overwrite a
previously successful log. If those external
archives are unavailable, use the portable public replay above.

The repaired release records portable-replay evidence separately from
historical-lineage evidence in `release/REPLAY_STATUS.md`. A full-provenance
claim is made only for a run that actually had all five archives available;
the top-level command is not self-contained in the downloadable repository.

The successful full log contains:

```text
FROZEN_SOURCE_HASHES_PASS
NUMERICAL_PROVENANCE_PASS
MATRIX_THEOREM_GENERALIZATION_PASS
STABLE_DOMAIN_SCOPE_PASS
SCC_EXHAUSTION_PASS
OMISSION_MINOR_PASS
SYMBOLIC_CERTIFICATE_VISIBILITY_PASS
TABLE_REGENERATION_PASS
FIGURE_REGENERATION_PASS
DOCUMENT_BUILD_PASS
SUBMISSION_BUNDLE_FRESHNESS_PASS
CLEAN_ARTIFACT_AUDIT_PASS
ALL_FINAL_RELEASE_REPLAY_CHECKS_PASS
```

## Single source of numerical truth

`data/current_profile_exact.json` is regenerated from the indexed reactions
and current improved diffusion profile. Table 1, normal-form predictions,
simulation metadata, figures, finite examples, and public demonstrations derive
from this file. The mandatory regression is

```text
eta_3 = 143636/7451873
```

## Build and artifact checks

Python dependencies, including tested lower bounds for NumPy and SciPy, are in
`requirements.txt`. The replays reject optimized Python mode because the exact
verifiers deliberately use assertions, and they record the Python package
versions used. The full replay preflight also requires `pdflatex`, `biber`,
`pdfinfo`, `pdffonts`,
`unzip`, `sha256sum`, and `rsync`; the TeX installation must provide TikZ,
`biblatex`, AMS packages, and the fonts used by the sources.

The document stage recreates `release/build_logs/` and
`release/pdf_preflight/`. The PDF audit checks opening, page counts, extractable
text, S-prefixed supplement sections, and known stale rendered phrases. The
final manifest is regenerated only after all bundles and audits are complete,
and an explicit gate requires it to cover `RESEARCH_LOG.md`.

The open-data ZIP, three submission ZIPs, and three specialist-packet ZIPs are
written in sorted order with a fixed timestamp and normalized permissions.
Their bytes are reproducible for unchanged inputs under the same Python/zlib
toolchain; member contents and metadata remain reproducible across compatible
toolchains even if compressed byte streams differ. Numerical integrations are
cosine--Galerkin illustrations reproducible within the recorded solver and
refinement tolerances. BLAS thread counts are fixed by the replay, package
versions are logged, and no numerical integration is used in a proof.
