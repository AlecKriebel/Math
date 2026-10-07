# Reproduction and evidence scope

All finite algebra checks use Python's standard library and exact `fractions.Fraction` arithmetic. The checked research environment used Python 3.14.6. The scripts require Python 3.10 or newer. They use a fixed pseudorandom seed `20261006`; they perform no network or publication operations.

## Extracted public archive

Extract `source-and-verification.zip` into a fresh directory and run from its root:

```sh
python3 verification/reproduce.py
```

The script verifies every byte-size/SHA-256 entry in `PACKAGE_CONTENTS.json`, checks author/title/date/license and exact upload filenames against `zenodo-deposit.json`, and confirms the TeX source is standalone with an embedded bibliography. It then runs:

- `agent_notes/upstream_audit_tensor_certificate.py`: 200 exact rational tensor cases, dimensions 1–5, including indefinite symmetric Hessian inputs.
- `agent_notes/moment_dependencies_tensor_check.py`: 250 separately implemented exact rational tensor cases, dimensions 1–5.
- 200 exact rational local endpoint-identity cases, tangent dimensions 1–5, including ambient `n=2`.
- Equal-volume box-measure and rational-scaling checks in ambient dimensions 2–8. These check the signed-normal L0 atom `V/2`, cone-volume atom `V/(2n)`, the positive-p strict-Jensen comparison, and the scaling exponent `n-p`.

The tensor programs test their independently derived contraction formulas and the nonnegative sum-of-squares remainder. The endpoint tests impose the first logarithmic derivative and check the algebra of the second derivative. No program solves the global geometric PDE. Finite passing cases are reproducible regression/falsification evidence, not a proof in every dimension. The all-dimensional deductions are the arguments in `main.tex` and the analytic reports.

## Standalone PDF compilation

The source requires the standard LaTeX packages `fontenc`, `lmodern`, `microtype`, `amsmath`, `amssymb`, `amsthm`, `geometry` and `hyperref`. It includes the complete bibliography inline, so no BibTeX run or additional project file is necessary. Use a current Tectonic or pdfLaTeX installation:

```sh
python3 verification/reproduce.py --compile --tex-engine /ABSOLUTE/PATH/TO/tectonic
```

The reproduction script creates a fresh project-local temporary directory, copies only `main.tex`, builds an actual PDF, checks common fatal/undefined-reference diagnostics and records the engine version and output/log hashes. With pdfLaTeX it runs twice to resolve references. This checks compilation, not the formulas' mathematical validity or visual page layout. The released `paper.pdf` is separately exported and visually inspected. The publication export used Tectonic 0.16.9; PDF inspection used Poppler 26.08.0. The recorded export was five pages with embedded fonts, and the final build log had no warnings; exact hashes and the final QA record are in `verification/PDF_QA.json`. Native editor preview/compilation success alone is not evidence of an exported downloadable PDF. Different engine versions, PDF timestamps and font tooling may produce different PDF bytes; no cross-environment byte-identical PDF claim is made.

## Pinned upstream source audit

The source repository is https://github.com/openai/math, at exact commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. `sources/UPSTREAM_INVENTORY.json` records every actually used upstream file, its byte size and SHA-256. The October 6, 2026 public release was checked; September 23 in the upstream manuscript name is an internal manuscript date, not an independently established September public disclosure.

The public archive intentionally does not redistribute the upstream manuscript, Lean solution, cloned dependencies or downloaded journal/arXiv PDFs. Obtain the upstream source separately and verify its bytes without changing it:

```sh
python3 verification/reproduce.py --upstream /PATH/TO/SEPARATE/PINNED/OPENAI-MATH-CHECKOUT
```

This command checks `git rev-parse HEAD` and the source inventory, and does not run a build in that checkout. External PDFs inspected in the audits are identified by primary URLs, versions and hashes in the reports and downloaded-source inventory. An unavailable or changed remote copy must not silently replace a recorded version. The source-hash inventory is an evidence identifier, not a redistribution license.

The analytic dependency reports are `agent_notes/upstream_proof_audit.md`, `agent_notes/moment_dependencies.md`, `agent_notes/smooth_transfer.md` and `agent_notes/mixed_strictness.md`. The priority/citation report is `agent_notes/priority_audit.md`. Reports were independent in scope; a favorable narrow audit does not certify the full follow-on package. Final complete-package reviews, their exact reviewed hashes and responses are included by explicit path in the package inventory.

## What was checked formally, and what was not

The actual upstream theorem is `OAI.LogBrunnMinkowski.main` in `lean/OAI/Geometry/LogVolume/BrunnMinkowski.lean`. It states the full-dimensional origin-symmetric Wulff-volume inequality with the intended hypotheses. Source definitions, statement semantics and selected actual proof declarations were inspected. The distinct comparator challenge intentionally contains `sorry`; it was not treated as a proof.

The exact upstream source SHA-256 is `bb798d24c3506422bc6ebdf064b71e3a1cf0f5f77835dd1985da2ff18a2c43a5`. Lexical checking found no local prohibited proof placeholders, but this does not establish imported-axiom closure. Formal provenance JSON identifies the exact Lean toolchain `leanprover/lean4:v4.34.1`, Mathlib revision `d13f23b723b8a846827a245b89c10fc7d3f11612` and eight matching transitive pins. Toolchain installation/version checking succeeded. Kernel compilation, `#print axioms OAI.LogBrunnMinkowski.main`, Comparator reproduction and an independent-kernel run **did not complete** because available disk space interrupted dependency installation. The compiled theorem's axiom set therefore remains unverified in this project. No follow-on theorem is formalized.

`verification/LEAN_SCOPE_AUDIT.md` is a public excerpt of the original formal-scope report. It records the original SHA-256 and removes only the unrelated operational incident section. Every mathematical/formal-check limitation remains. The JSON inventory/check reports under `verification/lean_pinned/` are metadata-only audit records; source copies and generated dependency/build instructions are omitted.

A reader wishing to extend the formal evidence should create a separate pinned build copy with adequate disk space, follow the upstream Lean build instructions, compile the actual solution, and execute a file importing that solution and printing the actual theorem's axioms. Record all logs/exit statuses, then compare the axiom list to the comparator's permitted `propext`, `Quot.sound`, `Classical.choice`. Any unexplained axiom or `sorryAx` must be reported. Compilation and axiom extraction alone would still not constitute an independent Comparator/kernel audit. Do not claim this future work already passed.

## Package construction

`publication/build_package.py` uses an explicit payload allowlist plus explicitly supplied review/response paths. It copies only owned documentation/proofs/code and source-hash metadata. It fixes ZIP entry order, timestamps and permissions and writes an internal payload hash inventory. The final receipt records Python/zlib versions and hashes of the three uploaded files. No secret is read. It performs no Zenodo operation and no Git action.

Run the exact final command recorded in `publication/package-inventory.json` to recreate the archive in the same environment. `--check` compares with the existing upload kit without mutating it. `--final` is a packaging assertion by the lead after the mathematical and two distinct complete-package reviews have passed; the builder is not a proof validator. Any changed manuscript, metadata or evidence must be reviewed appropriately before publication. DOI and spreadsheet receipts are separate verification of external state and are never inferred from successful local tests.
