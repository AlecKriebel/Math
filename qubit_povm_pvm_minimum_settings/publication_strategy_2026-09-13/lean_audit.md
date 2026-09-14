# Lean scope and publication audit

Audit checkpoint: 2026-09-13 PDT (2026-09-14 UTC). Completion estimate: **100% of this bounded Lean/readiness assessment**. This is not a claim to have newly rebuilt the entire development or checked every prose lemma. No production source, prior receipt, manuscript, or release was changed; no external communication was initiated.

## Recommendation

**The principal results are already formally proved in Lean. Do not allocate resources to a second broad formalization before sharing/submission.** The immediate return is from making the existing proof package easy to find and reproducing it against the corrected manuscript. Lean materially strengthens confidence in this unusually long, delicate equality proof, but does not establish novelty, physical importance, exposition quality, or journal suitability. The existing checks are not external human peer review.

The highest-value next step is a consistent public revision: retain the September 11 Lorentz-signature correction, add an accurate manuscript paragraph linking the Lean theorem map/certificate/reproduction instructions, and make clear that the principal conclusions have formal proofs while selected auxiliary statements use specialized or alternative arguments. The current verification section still discusses only finite algebraic scripts and says the geometric arguments remain explicit manuscript proofs (`paper/main.tex:1747–1755`); it never mentions Lean. The project README already advertises it (`README.md:59–67`). This is a communication gap, not a missing proof campaign.

## What was independently checked now

- Rehashed all **88 protected proof/verifier inputs** and all **123 executed-command logs** against the fixed successful run `20260911T022153Z-2ea5f99b`: zero mismatches. Record: `lean_checks/receipt_rehash.json`.
- Checked all **675 public declaration dependency entries** in that run: every axiom list is contained in `{propext, Classical.choice, Quot.sound}`. The retained receipt records 58 rebuilt mathematical modules, the umbrella module, and 25 expanded contracts. This is retained full-build evidence, not a fresh 675-theorem rerun.
- Freshly executed `lake env lean ../referee_2026-09-11/contracts/MatrixModelContract.lean`: exit 0; its explicit complex-matrix equality reports only those standard axioms. This contract independently states PSD density/effect matrices, normalization, PVM idempotence/orthogonality, and the tensor Born formula before proving the hull equality (`MatrixModelContract.lean:15–36,74–80`). Log: `lean_checks/matrix_contract.log`.
- Freshly executed the strict-domain counterexample: exit 0; all five axiom queries use only standard axioms. Log: `lean_checks/strict_domain_counterexample.log`. A small manifest with hashes is `lean_checks/targeted_checks.json`.
- Read the actual model, unconditional assembly, finite-simulation statement, physical residual closure, bound transfer, corrected manuscript definition, certificate, coverage map, and prior correspondence/referee findings. No new added premise or false endpoint was identified in this bounded audit.

## Statement fidelity

`bell_lean/Bell/Quantum.lean:19–86` models genuine complex qubits, arbitrary PSD trace-one two-qubit states, normalized PSD measurements, and PVMs with idempotence and orthogonality. Zero/identity projectors and zero effects are permitted. It uses actual trace Born probabilities and separately defines the raw strategy ranges and their ordinary real convex hulls. No ambient extra quantum ancilla is introduced.

`Bell/Assembly.lean:75–85` proves arbitrary finite input-dependent-output two-input equality without geometric or optimization assumptions in the endpoint. The reductions discharge the pure-state, active-support and residual-frame premises internally. `Assembly.lean:100–134` supplies at-most-two equality, minimum inputs and attained 3×2 separation. `Bell/SimulationCorollaries.lean:24–37` uses one finite weight distribution selecting a complete projective strategy in each branch; its table equality is simultaneous for every input/output. It allows the branch state to change. This is not same-state simulation or equality of raw strategy images.

`Bell/ProjectiveBound.lean:153–200` proves a physical PVM bound of **289/10**, stronger than the manuscript's bound, via exact SOS; it is not merely a scalar feasible-region calculation. The strengthened POVM value is an attained value, not a global optimum. `ProjectiveBound.lean:203–209` proves the simple witness exceeds every projective behavior by more than 1/50. Promoting the useful stronger certificate as supplementary verification is preferable to claiming the original projective derivation itself was formalized.

## Corrected counterexample and remaining coverage limits

The scalar strict inequalities alone admit signature (2,2); this is a real error in the former unqualified domain characterization. Current `paper/main.tex:1036–1054` explicitly requires signature (1,3) separately. The production closure already requires an invertible physical frame and `frameGram E = metric ...` (`Bell/ResidualClosure.lean:54–60`), and hence does not infer physical signature from `StrictParameters`. Future orientation is explicitly used at `ResidualClosure.lean:43–50,98–105`. The freshly checked scalar counterexample therefore does not refute the main physical equality.

The exact scope omissions are documented at `bell_lean/docs/CERTIFIED_COVERAGE.md:29–40`: the full general SDP/KKT package, full 14-dimensional smooth-manifold and (4,12)-inertia statements, some general cone/extremality/common-span results, the original projective scalar-bound route, and individual Appendix B optimality/coordinate claims are not all standalone formal endpoints. Some are replaced by specialized sufficient arguments. They should not be described as a formalization of every mathematical statement in the paper.

Two small interpretation bridges remain outside named Lean endpoints: generic finite stochastic output-channel decomposition and embedding dimensions at most two into the fixed qubit carrier. The manuscript supplies the deterministic-mixture postprocessing argument (`paper/main.tex:295–314`), and fixed-dimension embedding is standard. If a reviewer specifically requests tighter model matching, these two explicit bridge theorems would be the best bounded next Lean task; they are not evidence that the present central theorem is conditional or that a new large formalization is necessary.

Some old module comments still say proofs await compilation, e.g. `Bell/SimulationCorollaries.lean:9`. The authoritative certificate labels the historical material and has successful receipts. A future documentation cleanup should align such stale comments with that status and refresh manifests as needed.

## Publication consequence and trust limit

A compact artifact panel should give: exact theorem scope, one-command pinned reproduction, theorem-to-paper map, fixed successful build receipt, standard-axiom dependency audit, September 11 correction, and precise unformalized auxiliary scope. A clean-environment rerun by a reviewer would be especially valuable independent validation. Normal trust remains in Lean's kernel/compiler/runtime, platform, and pinned Mathlib cache; the package does not bootstrap every external dependency (`bell_lean/CERTIFICATION.md:60–74`). None of this certifies literature priority or substitutes for a quantum-information expert assessing the contribution.

**Decision for the paper's Lean column:** “Already completed for principal physical claims; high value already realized. No major additional Lean spend before dissemination/submission. Package and disclose current certification; optional small postprocessing/embedding bridges if requested.”
