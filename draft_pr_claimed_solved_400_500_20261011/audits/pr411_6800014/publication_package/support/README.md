# Ricci-pinching verification and selected supporting material

This support package accompanies Alec Kriebel's note
Local Ricci-pinching maxima on an almost-abelian group.
The mathematical claim is the non-strict, all-nearby-metrics local maximum
for 0<u<1/2 on the fixed group, with F=1/3 and failure of that group's
solvsoliton equation. The metric is geometrically a Ricci soliton.
Lauret–Will's known family/value and Lauret's exact 23 July 2018 existence
announcement have priority. No new family, first assertion, first proof,
novelty, present community-open status, or inaccessible final-journal text is
certified. Primary PDFs and raw search material remain outside this archive.

## Contents and custody

- [verification_v2/README.md](verification_v2/README.md): intact accepted
  component, 71 positive payloads plus its authentic whitelist and final seal.
  No files were inserted or altered inside it. Its final seal SHA-256 is
  6fb571bf3f2e8c36cdea70832efcdab15a48bab75db40e67a9ebce496390e7fb;
  whitelist SHA-256 is
  6ea7bf4432ef4659340a94b1077fc804b1203d141fbf4231868f8844644fddf1.
- [acceptance/SOFTWARE_GATE_ACCEPTANCE_V2.json](acceptance/SOFTWARE_GATE_ACCEPTANCE_V2.json)
  and [acceptance/ROOT_V2_FINAL_REPLAY.json](acceptance/ROOT_V2_FINAL_REPLAY.json):
  later parent acceptance and actual final normal/optimized replay. Authentic
  component-review prose inside the core remains historical; this
  separate gate applies to its actual final 71/73-file state.
- [acceptance/MATH_GATE_ACCEPTANCE.json](acceptance/MATH_GATE_ACCEPTANCE.json)
  and [acceptance/PRIORITY_GATE_ACCEPTANCE.json](acceptance/PRIORITY_GATE_ACCEPTANCE.json):
  mathematical and qualified priority acceptance, with their limitations.
- [reviews/algebra_reproduction/VERDICT.md](reviews/algebra_reproduction/VERDICT.md),
  [reviews/geometry_adversary/GEOMETRIC_AUDIT.md](reviews/geometry_adversary/GEOMETRIC_AUDIT.md),
  and [reviews/priority_classification_adversary/ADVERSARIAL_REPORT.md](reviews/priority_classification_adversary/ADVERSARIAL_REPORT.md):
  complete individual reports with selected criteria, reconstructions, and
  native verdicts. The core also contains its complete software-adversary report.
- [root_checks/exact_boundary_koszul.py](root_checks/exact_boundary_koszul.py)
  and [root_checks/primary_Et_formula_check.py](root_checks/primary_Et_formula_check.py):
  exact, separately reviewed standard-library checks, kept together unchanged.
  Their normal/optimized native JSON results and root replay receipts are
  alongside them. PRIORITY_FORMULA_NORMAL_NATIVE.json is additional authored
  symbolic output, not a claim that its separate checker is bundled.
- [SUPPORT_MANIFEST.json](SUPPORT_MANIFEST.json): positive member manifest
  excluding itself; the external assembly/delivery record pins its actual hash.

Outside verification_v2 this is explicitly a PARTIAL selection of complete
authored artifacts, not a full sealed review corpus. Copied reports and
acceptances retain their original case-relative references and authentic
custody hashes. Referenced source PDFs, raw responses, complete reviewer file
sets, and private fixtures are not included; their presence or replay is not
attested by this archive. The core's own positive inventory is complete.
Whole-package acceptance and release status are tracked separately from
the historical component reviews and assembly records.

## Reproduce the accepted core

Authenticate the actual core seal hash above through a trusted independent
delivery record before executing code. A replacement of all code, manifests,
and custody together is outside this unkeyed-integrity check. Hashes bind
reviewed bytes, not arbitrary prose semantics.
Use Python with SymPy 1.14.0, preferably a private venv outside this extraction.
For example, from the extracted archive root:

    python -m venv "/path/to/private venv"
    "/path/to/private venv/bin/python" -m pip install sympy==1.14.0
    "/path/to/private venv/bin/python" -B verification_v2/run_all.py
    "/path/to/private venv/bin/python" -B -O verification_v2/run_all.py

Both top-level core runs must return PASS with 54 mandatory evaluations of
39 original predicates and 71 positive whitelist payloads. Do not place venvs,
caches, logs, or extra files inside verification_v2; its exact inventory is
checked. Do not use -I, which removes the script's sibling-module import path.
Do not resolve the venv interpreter symlink to its base interpreter.
The optional 38-control harness writes only private fixtures/logs:

    "/path/to/private venv/bin/python" -B verification_v2/reproduce_controls.py --private-log-dir "/path/to/private raw logs"

The current guarded normal/-O runs certify their checks and byte bindings.
Original historical optimized assertion output is NOT CERTIFIED validation.
The missing historical standalone source-manifest bytes with SHA-256
f5446c816081c5322e4279bcd9a61dca5bfb63cfacf69d105d1587ed9d93b7fb
and pre-layout checker bytes with SHA-256
eccde3c2a903b1fca0f232e7e392d537479ddd3936281a37e87c4f7e7047be97
remain UNATTESTED. No substitute objects or fabricated self-hashes are supplied.

## Reproduce the standard-library supplementary checks

From the extraction root, with any compatible Python 3:

    python3 -B root_checks/exact_boundary_koszul.py
    python3 -B -O root_checks/exact_boundary_koszul.py
    python3 -B root_checks/primary_Et_formula_check.py
    python3 -B -O root_checks/primary_Et_formula_check.py

Each prints a PASS JSON record. These finite exact computations supplement the
written uniform-neighborhood proof; they do not replace its analytic coverage.
The second script locates the first by its own directory, so keep both together.
It checks the old displayed E_t matrix directly: its actual ratio is
25t^4/(59t^4+32t^2), differing from the inspected preprint's printed formula.
No claim is made about whether the inaccessible journal corrected that formula.
The note's 9/17 comparison is independent of this peripheral source correction.

AI tools were used extensively in solving, symbolic computation, source review,
writing, and adversarial verification. Machine agents are not independent
human referees; the work is unrefereed and no external human peer review is
certified. The author retains responsibility. Status remains claimed_solved,
2/5 author proof-search turns, with zero new assembly/proof-search turns.
