# v1.0.8 package inventory and dependency boundary

The immutable tagged project contains 1,064 regular files. Top-level counts
are:

| Area | Files | Role |
|---|---:|---|
| `external_audit/` | 495 | v1.0.7 full referee packet, proof aids, specialist packets, and their packaged copies |
| `public/` | 212 | self-contained portable repository plus data archive |
| `data/` | 66 | exact source, finite instances, generated tables, and numerical illustrations |
| `submission/` | 54 | journal, bioRxiv, and arXiv PDFs/source packages/checklists |
| `release/` | 52 | orchestration, manifests, stored provenance, build logs, and replay reports |
| `independent_verifier/` | 48 | four support modules and 39 direct entrypoints, including the new generic cubic bridge |
| `proof_audit/` | 27 | human-readable algebraic and nonlinear proof aids |
| `computation/` | 27 | exact generators, audits, exporters, simulations, and 25-test suite |
| prior independent audit | 23 | committed v1.0.7 report, controls, and command records; disposable packet copies are intentionally ignored |
| `source_audit/` | 15 | source/PDF visual-audit records |
| `figures/` | 14 | reproducible figure programs and rendered figures |
| `manuscript/` | 7 | main/supplement TeX/PDF, bibliography, and Biber output |
| `literature/` | 6 | citation and closest-work audit notes |
| `environment/` | 3 | tested-environment description, checker, and TeX interface lock |
| root metadata/other proof notes | 16 | changelog, citation, decisions, license, requirements, and project state |

The portable repository contains 211 files and has its own valid shipped
manifest. The journal source ZIP contains 11 allowlisted files: `main.tex`,
`main.bbl`, `supplement.tex`, `references.bib`, four generated TeX tables, one
TikZ network source, and two PDF figures. It contains no audit notes, private
workflow paths, credentials, caches, or local build products.

## Inputs and prerequisites

- No theorem, generator, verifier, simulation, PDF build, or portable replay
  requires network access at runtime.
- The top-level lineage preflight requires five separately held historical ZIP
  archives at `FROZEN_BASE`; they were unavailable in this rereview and are not
  used by any current proof or build stage.
- The exact qualification runtime is not vendored. Direct Python package
  versions are pinned but wheel hashes and all transitive/system libraries are
  not; the dated TinyTeX distribution itself is described but not bundled with
  an archive checksum. Numerical work is consequently tolerance-certified,
  not byte-certified.
- System utilities (`bash`, `git`, `unzip`, `rsync`, GNU-style checksum/text
  tools, and Poppler) are prerequisite-checked but generally not version-pinned.
  Their roles are orchestration, archive integrity, and document inspection,
  not mathematical algebra.
- The release replay contains no hidden private path apart from the documented
  default `/mnt/data` historical-archive location; the portable replay is the
  documented self-contained alternative.

Stored `PASS` files and build logs are provenance only. They were not counted
as current execution evidence.
