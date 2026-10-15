# Verification package: a minimal-surface Seshadri counterexample

The paper proves an upper Seshadri bound at a special point on each of a varying
family of smooth minimal complex projective surfaces. It refutes the precise
Szemberg2007/2008 / OWR2009Conjecture2 / Primer-v2Question6.1.6 bound
`epsilon >= 1/(2+|K^2|^(1/4))`. It asserts no exact epsilon, fixed-surface
vanishing, Picard-rank-one or very-general-point counterexample.

Miranda's integral pencil and polarization are credited through
Ein-Lazarsfeld1993Example3.1, Bauer1999Prop3.3 and Bauer-Szemberg2010v1Prop2.1.
The cover theory is classical. Historical priority is explicitly incomplete;
the unread full2025survey and other precise gaps are recorded in
CURRENT_PRIORITY_ASSESSMENT.json and the two primary-source priority reports.
No firstness, new-method or verified present-open assertion is made.

AI tools were used extensively in solving, research, writing, reproduction and
adversarial verification. These are internal AI reviews, not human peer review.
This is an unrefereed preprint without proof-assistant certification.

## Contents and replay

Extract the ZIP into a fresh directory. It contains authored evidence only:
18 exact original inputs from PR585 head0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27,
four closed review families and their unmodified seals, root derivations/source
receipts, the TeX source, exact recorded outputs, and the scripts and inventories.
Raw third-party PDFs, extractions, rendered source pages, private account data
and dependency environments are excluded. The paper PDF is deposited separately.
Dated pending/candidate wording in preserved evidence is historical; the paper,
CURRENT_CORRECTIONS.md and CURRENT_PRIORITY_ASSESSMENT.json govern the current
scope and disposition. Final package reviews and publication receipts are linked
from the repository acceptance guide after acceptance; they are not included in
their own reviewed ZIP.

Use Python3.9 or later, with assertions enabled, without `PYTHONOPTIMIZE`.
SymPy1.14.0 and mpmath1.3.0 are required and are not bundled. Install dependencies
in an environment **beside the extracted directory**, while network access is
available, or use an already prepared environment with these exact versions:

```
python3 -m venv ../seshadri-env
../seshadri-env/bin/python -m pip install -r requirements.txt
../seshadri-env/bin/python -B run_all.py
```

The install step can require network access. Once those dependencies are
installed, replay makes no network requests. The driver does not itself enforce
network denial; the recorded audit executions were additionally run under OS
network denial. Do not place the environment, output files or bytecode caches
inside the exact extracted inventory. Run with `-B` as shown.

The driver verifies the exact outer inventory, every registered nested seal,
and a literal acquisition-pinned snapshot of all18 originals, including their
manifests. It actually runs all nine registered jobs in separate disposable
copies and compares each complete JSON result with its recorded result, without
normalizing fields. The original release job itself reruns three original math
programs, so these replays overlap; they are not nine independent proofs. The
original integrity job executes eight actual copied mutations. The new strict
gate regression executes four actual copied mutations, including a changed input
and self-resealed snapshot. The pencil family's ten false-formula controls are
unit comparisons, not ten process mutations.

The first replay of the exact package should leave its contents unchanged. Each
job's writable copy is discarded. `JOBS.json` identifies all actual scripts and
recorded outputs. The finite symbolic controls supplement the geometric proof;
they do not prove Bertini, Nakai-Moishezon, complex existence or priority.
Integrity is not authenticity, semantic authorship or mathematical certification.

## Rebuilding

The PDF was built with Tectonic0.16.9 and `SOURCE_DATE_EPOCH=1792022400`:

```
SOURCE_DATE_EPOCH=1792022400 tectonic --only-cached seshadri_counterexample.tex
```

This requires the TeX resources already cached; it is separate from the nine
mathematical/integrity jobs. `BUILD.json` and `PDF_QA.json` identify the exact
build and inspected PDF. The fixed epoch is a reproducibility setting, not a
discovery timestamp.

`make_package.py` is the repository producer: run it from its audit checkout
layout, not from the extracted flat archive. It selects explicit authored files,
checks all seals and the snapshot, and writes a deterministic ZIP. Its path
guards examine lexical, resolved and archive paths relative to this audit;
unrelated external checkout ancestors named cache/scratch are allowed. Literal
parent segments in the lexical audit-relative source path are rejected before
selection, even if resolution would stay inside the audit. Sources
outside the audit, leaf symlinks, duplicates, traversal and audit-relative
`.cache`, `sources`, `scratch`, `qa`, `.secrets` and `.private` components are
rejected case-insensitively, including resolved ancestor aliases on a
case-insensitive filesystem. `MANIFEST.json` inventories all other archive members; the outer
manifest does not self-hash. Public deposit hashes supply its external binding.

The first fresh full-package review found a missing lexical source-alias guard
(F01) and then an exclusion bypass through uppercase directory aliases (F02).
Both guards were repaired; real copied-process regressions now reject the
lexical alias and all six case-alias redirects. The current ZIP was regenerated.
The historical ZIP was not alleged to contain unsafe members; the findings
concerned the source-selection contract. The mathematical paper, metadata and
all18 originals were unchanged.
