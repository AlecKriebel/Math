# Response to the independent Lean referee

The substantive manuscript issue is corrected. The principal Lean results remain valid and the production proof sources are unchanged. The accompanying report is preserved as [received_report.md](received_report.md); its recommendations were assessed rather than treated as instructions to execute.

## R1 — Strict residual domain: corrected

Definition 5.1 in [the manuscript](../paper/main.tex) now explicitly requires signature `(1,3)` separately from positivity of distinct-ray pairings, and orients the common future cone to contain `u`. The text no longer suggests that the scalar inequalities imply Lorentz signature.

The referee's rational example was rechecked by Lean. It has all five rays null, all distinct-ray pairings positive, `uᵀgu=1`, `uᵀgv=0`, and `vᵀgv=12/5`. In particular its quadratic form is positive definite on a two-dimensional subspace, ruling out signature `(1,3)`. The independent [mathematical review](math_review.md) checks the correction and its downstream uses. This is a defect in the unqualified scalar characterization, not a counterexample to the main equality: the physical closure retains invertible frames and `g=EᵀJE`.

## R2 — Literal whole-paper coverage: clarified

The certificate and [coverage map](../bell_lean/docs/CERTIFIED_COVERAGE.md#auxiliary-mathematics-outside-the-certified-scope) now list the specific general or auxiliary statements that are specialized, replaced, or absent: the general SDP/KKT package, full smooth-manifold/Hessian/inertia statements, general cone/filter/rank inequalities, the original scalar bound route, auxiliary discrimination and Appendix B optimization details, and generic representation bridges.

The accurate claim is that the principal behavior-set equality, finite projective simulation, minimum-setting classification, explicit separation and strengthened attained value are formalized. We do not claim that every mathematical statement in the paper is formalized. The referee found no required repair to those production endpoints; this response does not add unnecessary proof assumptions or attempt to pass off an attained value as an optimality theorem.

## R3 — Trust and provenance: retained and made more precise

The certificate explicitly retains trust in the pinned Lean compiler/kernel/runtime and Mathlib cache producer. Its evidence links now point directly to the immutable original successful run, so pre-existing later changes to the top-level convenience receipts cannot silently change which run the certificate describes. Those pre-existing user changes have not been overwritten or included in this response's commit.

All 88 original protected proof/verifier inputs and all 123 original command-log hashes were rechecked. Both the standalone strict-domain counterexample and the independent explicit complex-matrix equality contract were executed again with pinned Lean 4.19.0 and passed with only `propext`, `Classical.choice`, and `Quot.sound`. No complete 675-theorem audit is newly claimed here: the unchanged production sources retain their complete earlier build and dependency evidence.

## Artifact validation

- The existing exact manuscript artifact suite passed.
- Publication and line-numbered review PDFs rebuilt warning-free, remaining 34 pages each. Revised definition and following-page layout were rendered and visually inspected in both versions.
- The active submission source archive was refreshed and rebuilt independently. Its extracted PDF text matches the publication PDF exactly.
- Current corrected manuscript/PDF/archive fingerprints and verification log hashes are in [verification.json](evidence/verification.json).
- Historical bundled source PDFs, the original referee evidence, and immutable Zenodo release packages remain unchanged. Their original fingerprints identify the earlier manuscript version.

To rerun the additional Lean checks, from `bell_lean`:

```sh
lake env lean ../referee_2026-09-11/computations/StrictDomainCounterexample.lean
lake env lean ../referee_2026-09-11/contracts/MatrixModelContract.lean
```

From the program directory, run `./run_all.sh` for exact artifact arithmetic and `./paper/build.sh` for both PDFs. `python3 referee_response_20260911/verify_evidence.py` verifies the recorded response evidence and the unchanged original certified inputs. The full original proof verification remains reproducible with `bash scripts/check.sh --serial` from `bell_lean`.

No outside individual was contacted. No new immutable GitHub/Zenodo release was created.
