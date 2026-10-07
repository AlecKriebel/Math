# Pure-loss bosonic dynamic capacities

Publication candidate: **Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting**. Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X . No affiliation or coauthors claimed. Production publication is conditional on final independent reviews; no deposit has yet been made.

The quantum C/Q/E formula is a consequence of the externally attributed OpenAI finite-energy multimode EPnI and established dynamic coding. The literal private coding source is refuted at zero energy. A positive public/private/key formula is proved under the explicitly corrected generated-secret convention. This is not success for the unchanged stronger secrecy target. See CURRENT_THEOREM.md and manuscript/main.tex for precise hypotheses, DEPENDENCY_LEDGER.md for external inputs and APPROACH_TABLE.md for route status.

The formulas and conditional reductions were already public in WHG arxiv1105.0119v1/v2 (2011). We do not claim independent discovery of EPnI, these formulas or known coding machinery. The note adds an explicit consequence, boundary obstruction and carefully stated operational repair. Priority search limits and exact chronology are recorded in notes/alternate_priority/PRIORITY_AND_ROUTES.md and SECURITY_CRITERION_PRIORITY.md.

## Build and reproduce

The standalone manuscript has an embedded bibliography. From this directory run `tectonic --keep-logs --outdir manuscript manuscript/main.tex` (tested Tectonic0.16.9). The desktop built-in LaTeX compiler also accepted the source. Any standard LaTeX distribution with article, lmodern, microtype, amsmath, amssymb, amsthm, geometry and hyperref can instead compile it with PDFLaTeX twice. No executable Python dependencies beyond the standard library are needed for the exact checks:

```
python3 code/verify_certificates.py
python3 notes/alternate_priority/repair_identity_audit/symbolic_checks.py
python3 notes/upstream_proof/check_interpolation.py
```

Tested Python3.14.6. The first checks exact rational finite OTP distances and conversion vectors; the second checks five exact entropy chain identities. The final seeded floating-point experiment is exploratory falsification evidence, not proof or validated interval computation. The universal analytical arguments are in the manuscript and proof supplements. Code and prose licenses are in LICENSES.md.

For optional selected-module Lean reproduction, first obtain a read-only clone of https://github.com/openai/math at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a, then run `python3 notes/formal_scope/create_harness.py --upstream /path/to/math --output /path/to/isolated-output`. In its generated pinned_build directory, install Lean4.34.1 and clone Mathlib at d13f23b723b8a846827a245b89c10fc7d3f11612 into .lake/packages/mathlib, initialize that dependency's own pinned dependencies, then run `lake update`, `lake build OAI.InformationTheory.PhotonNumber.Inequality`, and `lake env lean CheckAxioms.lean`. Adequate disk space is necessary. These commands are proposed reproduction steps, **not completed checks**: our setup failed under disk pressure before compilation, cache completion or axiom printing. Formal-source semantic and hash checks are recorded separately; no formal verification of this follow-on note is asserted. The analytical upstream proof audit is the decisive validation basis.

## Package and review

`python3 code/build_package.py` creates publication/paper.pdf, the source/proof verification zip and a SHA256 inventory from an explicit owned-file allowlist. It does not include third-party downloads, caches, credentials or unrelated projects. `zenodo-deposit.json` is the exact intended production manifest. Reproduction from a clean extracted directory checks certificate outputs and recompiles the PDF; bytewise PDF identity is not expected because PDF timestamps differ.

Subtask audits and full-package review records are retained under notes/ and reviews/ in the research repository https://github.com/AlecKriebel/Math/tree/main/openai_followon_bosonic_capacity . AI tools were used extensively in research, drafting and verification. Automated adversarial reviews are not human peer review. This preprint has not undergone conventional human refereeing. Full-package review status and exact reviewed hashes are recorded in publication/REVIEW_STATUS.md; receipts and the verified tracker row will be recorded separately after publication.
