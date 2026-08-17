# Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks

## Version 1.2.1 submission candidate

This directory is the unrefereed Version 1.2.1 submission candidate frozen on
16 August 2026. It is prepared first for possible deposit in bioRxiv Systems
Biology as a New Result and, later, for journal submission. No preprint upload,
journal submission, DOI registration, or external contact is performed by the
release process.

Version 1.2.1 is a separate, superseding patch release. Versions 0.3, 1.0,
1.1, and 1.2 and their Git history remain unchanged. The Version 1.2-to-1.2.1
relationship is recorded in `preservation/VERSION_1.2_PROVENANCE.md`.

## Exact result and scope

Weak reversibility alone gives an elementary state-space fact. If an enabled
reaction takes $x=\rho+y$ to $x'=\rho+y'$, a directed complex path from $y'$ back to
$y$ lifts, with the same residual $\rho\geq0$, to enabled population transitions
from $x'$ back to $x$. Accessibility is therefore symmetric, and the set
reachable from every initial population is a closed communicating class.

Under the additional assumptions of one linkage class and molecularity at
most two, every nonabsorbing reachable class is nonexplosive and positive
recurrent for every positive rate vector. An absorbing singleton carries its
point-mass law. Thus every initial population has a unique stationary
probability law on its reachable class.

The theorem does not cover multiple linkage classes or molecularity above two.
It gives no product-form stationary law, moment or tail bound, mixing rate,
exponential ergodicity, bounded-path guarantee, or useful uniform bound on the
finite Foster set. Positive recurrence supplies long-run state frequencies and
expectations of bounded observables; unbounded molecule-count moments require
separate integrability.

The theorem removes the pure unary/pure-double-complex hypothesis from the
binary one-linkage positive-recurrence result of Anderson, Cappelletti, and Kim
(2020). The new mechanism retains the target of the most recently fired
labelled reaction channel and applies a residual log-factorial potential after
subtracting that target. Its increment is exactly a target/source
falling-factorial ratio. Finite target-following paths, a scalar-envelope
induction, and a normalized-log top-complex alternative yield the qualitative
recurrence criterion.

## Submission files

- `manuscript/main_biorxiv.pdf`: bioRxiv preprint PDF.
- `manuscript/main_jap.pdf`: Applied Probability initial-submission PDF.
- `manuscript/main_arxiv.pdf`: arXiv fallback PDF; do not use concurrently
  with bioRxiv.
- `manuscript/supplementary_note.pdf`: optional bioRxiv/archival technical note;
  the later JAP submission should omit it unless an editor requests it.
- `manuscript/paper_content.tex`: canonical mathematical content shared by the
  three manuscript wrappers.
- `submission/biorxiv_metadata.md`: submission-day bioRxiv field sheet.
- `submission/journal_route.md`: journal recommendation and SPA fallback gaps.
- `submission/zenodo_deposit_checklist.md`: optional manual preservation route
  that avoids archiving unrelated monorepo content.
- `submission/journal_cover_letter.md`: draft Applied Probability cover letter;
  update the bioRxiv status before later journal submission.

The supplementary note records trace-chain, physical-time, stationary-cycle,
and computational-boundary details. The main paper remains self-contained.

## Verification and reproducibility

The universal theorem is analytic. The finite atlases, exact-identity checks,
calibration chains, and fixed-seed tests are falsification aids; they neither
prove recurrence nor enumerate the analytic Foster set.

From this directory:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./reproduce.sh
```

The unchanged standalone verifier remains Version 1.2.0. It runs 57
mathematical and calibration tests, generates the
canonical report twice, and requires byte-identical outputs. Four additional
release-tool tests reject cross-platform unsafe paths and unignored symbolic
links while permitting a documented virtual environment. The
stable report is copied identically to `code/`, `supplement/`, and
`validation/`. It is tested on CPython 3.11 through 3.14; no claim is made
about future interpreter versions until they join the matrix.

Verify every durable package file with:

```bash
python3 supplement/verify_manifest.py
```

Build all four PDFs with the canonical Tectonic 0.16.9 toolchain and pinned
bundle recorded in `REPRODUCIBILITY.env`:

```bash
manuscript/build.sh
```

Build or verify the deterministic release archive with:

```bash
python3 supplement/build_release_archive.py
python3 supplement/build_release_archive.py --check
```

`validation/replay_release.sh` performs the complete release replay from a
clean checkout. The Git tag is the immutable commit identifier; the replay
prints the resolved commit, tool versions, report/PDF/archive digests, and
requires a clean package tree.

## Package map

- `audit/`: preserved earlier audits and the Version 1.2.1 feedback audit.
- `code/`: dependency-free verifier, exact tests, and deterministic regular-
  wheel backend. Editable wheels are ephemeral and contain a checkout path.
- `manuscript/`: shared source, submission wrappers, four canonical PDFs, and
  the PDF builder.
- `preservation/`: immutable provenance for earlier versions.
- `submission/`: unsent preprint and journal metadata and checklists.
- `supplement/`: AI-use record, limitations, historical audits, manifest, and
  deterministic archive tools.
- `validation/`: stable report, manifest copy, tag instructions, release
  record, and complete replay script.

Historical filenames such as `publication_v1_1_calibrations.py` and the dated
Version 1.1 audit records are intentionally preserved: they identify when
those checks and audits were introduced, not the current package version.

## Author, declarations, and rights

- **Author:** Alec Kriebel
- **Affiliation:** Independent researcher
- **Correspondence:** <me@aleckriebel.com>
- **ORCID:** <https://orcid.org/0009-0001-9320-500X>

The research received no specific grant. The author declares no competing
interests. No empirical or third-party dataset was used.

Generative-AI systems were used materially from 5--16 August 2026. The
manuscript contains the journal-facing declaration, and
`supplement/ai_use_full_statement.md` provides the system-by-system record.
The author directed the research, verified retained outputs, determined the
released claims, and assumes responsibility. No AI system is an author, and no
independent expert human validation is claimed.

The standalone software in `code/` is MIT-licensed. Rights in the manuscript
and other materials are governed by `LICENSE.md`. The release makes no
Creative Commons selection on the author's behalf.
