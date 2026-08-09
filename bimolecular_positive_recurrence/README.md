# Positive recurrence of bimolecular weakly reversible stochastic reaction networks with a single linkage class

**Version 0.3 — publication-readiness revision — 9 August 2026**

## Status

The adversarial reconstruction and subsequent publication-readiness audit found
no known theorem-breaking defect in the marked-target proof.  Version 0.3
packages the revised manuscript and reproducible verification materials for
journal submission.  The work has not yet been peer reviewed; the supplied
proof and exact artifacts are intended to make detailed checking practical.

The exact theorem is limited to finite weakly reversible stochastic mass-action networks with:

- one linkage class;
- molecularity at most two at every complex;
- arbitrary positive rate constants;
- an arbitrary closed communicating class, including boundary and lattice-restricted classes.

The release does **not** claim the multiple-linkage case, higher molecularity, the full Anderson-Kim positive-recurrence conjecture, exponential ergodicity, or quantitative mixing rates.

## Release map

- `manuscript/main_arxiv.tex` and `main_arxiv.pdf`: public-preprint version.
- `manuscript/main_jap.tex` and `main_jap.pdf`: Journal of Applied Probability initial-submission version with identical mathematical content.
- `manuscript/references.bib`: bibliography.
- `code/`: standalone verification package (version 0.3, the current verifier).
- `audit/independent_proof_reconstruction.md`: the adversarial Gate A1-A12 reconstruction referenced above.
- `supplement/proof_audit.md`: internal adversarial proof reconstruction; the
  legacy filename is retained so existing links continue to resolve.
- `supplement/priority_audit.md`: narrow literature and priority audit.
- `supplement/reviewer_checklist.md`: ten load-bearing reviewer checks.
- `supplement/ai_use_statement.md`: full AI-use declaration.
- `supplement/verification_report.json`: canonical deterministic verifier output, as released.
- `supplement/MANIFEST.sha256`: release-file hashes.
- `supplement/verify_manifest.py`: portable release-manifest checker.
- `CITATION.cff`: citation metadata for the repository release.
- `LICENSE.md`: terms for the manuscript and verification software.
- `expert_audit_note.md`: two-page orientation for a subject-matter expert.
- `cover_letter.md`: neutral draft submission letter; no submission was made.
- `revision_log.md`: release history and material changes.

The top-level `src/`, `failed_approaches/`, and `phase2_trigger_drain/` through
`phase5_source_flag_closure/` directories record the research path.  Phases
II--IV are superseded approaches, and Phase V is the immediate predecessor of
the current proof.  They are retained as provenance, but neither their old
manuscripts nor their certificates are the release's canonical theorem or
verification result.  Version 0.3 repairs a few archived execution paths and
regenerates the Phase-V certificate deterministically; Git history preserves
the earlier states.

## Build the manuscript

```bash
cd manuscript
./build.sh
```

The reference toolchain is Tectonic 0.16.9.  `build.sh` performs dependency
preflight, uses Tectonic when available, and also supports a traditional
`pdflatex`/BibTeX installation by setting `TEX_ENGINE=pdflatex`.  It sets
`SOURCE_DATE_EPOCH` and suppresses variable PDF metadata where the engine
supports doing so.  The repository does not claim byte-identical PDFs across
different TeX engines, distributions, font bundles, or operating systems;
compare mathematical content and rendering when using a different toolchain.

The `main_jap` wrapper intentionally uses a standard article class for initial submission. Current Applied Probability Trust instructions state that the APT class is encouraged but not a condition of initial submission; an accepted manuscript would be moved to the official class during production.

## Run the standalone verifier

```bash
cd code
./reproduce.sh
```

Python 3.11 or newer is required; the package has no runtime third-party
dependencies and the reproduction command is installation-free.  The verifier
has been exercised under Python 3.11 and 3.14.
The reproduction script runs the tests, generates the normalized mathematical
report twice, requires byte-for-byte equality, and prints its SHA-256 digest.
Environment provenance is recorded separately so that interpreter metadata
does not masquerade as mathematical output.

The finite atlas and fixed-seed tests are adversarial calibration. The universal theorem is proved in the manuscript, not by enumeration.

## Verify the release manifest

From this directory, run:

```bash
python supplement/verify_manifest.py
```

The check covers every durable release file, reports missing or unexpected
files as well as changed hashes, and is portable to platforms without the GNU
`sha256sum` utility.

## Author metadata

Alec Kriebel
Independent researcher
Correspondence: me@aleckriebel.com
ORCID: https://orcid.org/0009-0001-9320-500X

## AI disclosure

Generative-AI systems were used substantively throughout the research workflow.
The complete disclosure—including systems, access routes, dates, and uses—is
in `supplement/ai_use_statement.md` and in the manuscript declaration.  The
author determined the released scope and claims, curated the package, and
assumes responsibility for the submitted manuscript and public verification
materials.  No claim of prior independent expert human verification is made.
