# Independent referee report: qubit POVM–PVM Lean formalization

Review date: 11 September 2026, America/Los_Angeles (12 September UTC).

## Final disposition

The **unconditional universal two-input convex-hull equality is certified in the intended complex-qubit matrix model**, under the explicit standard Lean/compiler/dependency trust assumptions below. The fresh project-source build, both production statement contracts, all 675 public theorem dependency audits, and the independent expanded matrix contract passed. No fatal defect in the equality proof was found by the six source-review assignments.

The stronger assertion that **every mathematical statement in the primary paper is formalized is false**. The development proves the principal conclusions by a partly different route, and specializes or omits several auxiliary statements. This is already acknowledged in `bell_lean/docs/CERTIFIED_COVERAGE.md`; the present review verifies the distinction independently.

There is also a manuscript correction: the scalar characterization of the strict residual domain is false if read as dispensing with the Lorentz-signature hypothesis. An exact counterexample is supplied below. The Lean main proof explicitly retains a physical Gram frame and avoids this problem.

No changes to the mathematical production sources are proposed as necessary for the main equality on the evidence obtained. This report is a referee assessment, not a claim of novelty verification or an independent implementation of Lean's kernel.

## Scope and evidence

The objects reviewed are `paper/main.tex`, `paper/appendices.tex`, and the production `bell_lean/` sources and verification scripts. The paper's `main.pdf` and `bell_lean/source/paper_july2026_library.pdf` are byte-identical; the provenance details and complete claim matrix are in [coverage.md](reviews/coverage.md). Input hashes and the original commit are recorded in [input.json](evidence/input.json).

Six independent reviews covered materially different responsibilities:

- [Physical model and theorem semantics](reviews/model.md): actual complex matrices, mixed states, projection conventions, arbitrary outputs, finite common mixtures, and boundary cases.
- [Compactness and reductions](reviews/reductions.md): cone circuits, extreme measurements, filtering, steering and residual encoding.
- [Incidence geometry and rank closure](reviews/incidence.md): physical reconstruction, optimization bridge, stationarity, multipliers, and all ranks.
- [Separation and exact certificates](reviews/separation.md): Bell coefficients, full PVM cases, both attained witnesses and the stronger SOS upper bound.
- [Complete manuscript coverage](reviews/coverage.md): all 21 numbered theorem/lemma/proposition/corollary statements, the main theorem, definitions, substantive unnumbered claims, and every appendix.
- [Adversarial final review](reviews/adversarial.md): attempted falsification of the emerging verdict, signature counterexample, and environment/provenance checks.

These are independent source reviews with different assignments; they are not six independent reimplementations of the entire proof. The original production report files already had uncommitted changes before this review. They were not used as a substitute for a new run and were not modified or committed by this review.

## Exact meaning of the certified target

The production endpoint is `Bell.two_input_convex_equality` in `Bell/Assembly.lean:77`, whose only arguments are `AO BO : Fin 2 → ℕ`:

```lean
theorem two_input_convex_equality (AO BO : Fin 2 → ℕ) :
    convexPOVM ⟨2,2,AO,BO⟩ = convexPVM ⟨2,2,AO,BO⟩
```

Its definitions use a positive semidefinite trace-one complex 4×4 density matrix, positive semidefinite complex 2×2 measurement effects summing to the identity, and the tensor-product Born rule. A PVM additionally has idempotent, mutually orthogonal effects. The two sets are ordinary real convex hulls of the corresponding actual strategy images. Zero projectors, identity projectors, mixed states and unused outcome labels are allowed. Each output count is arbitrary and depends on its input. No extremality, full-rank, residual-geometry, stationarity or positivity-of-multipliers assumption survives in the theorem statement.

The independently written [MatrixModelContract.lean](contracts/MatrixModelContract.lean) defines both behavior sets directly by existential quantification over matrices, without using Bell's strategy/image definitions. It identifies those sets with the production model and derives their convex-hull equality. This checks the meaning of the theorem beyond simply printing a named proposition.

`finite_projective_simulation` in `Bell/SimulationCorollaries.lean:24` further supplies one finite random index with nonnegative weights summing to one, selecting a **complete** state-and-measurement projective strategy in each branch. Equality holds for the entire behavior table simultaneously. The theorem permits a different state in each branch. It does not claim raw-image equality or same-state measurement simulation.

For the paper's “dimension at most two” and stochastic-postprocessing conventions, the mathematical equivalences are valid, but their general bridges are not separate Lean endpoints. The model review gives explicit proofs: embed smaller spaces isometrically and put the unused orthogonal complement into one outcome; decompose each stochastic response channel into a finite distribution over complete deterministic output maps. The resulting convexified behavior sets are the same. Thus these conventions do not furnish a counterexample to the central result; a demand to formalize every identification step would require additional statements.

## Why the central proof is not merely conditional assembly

The final equality does not use the historical `main_claims_of_missing_theorems` as an assumption. A putative behavior outside the PVM hull gives an extreme maximizing physical POVM strategy through proved finite-dimensional compactness and separation. The reduction chain handles singular/product states and deterministic measurements, obtains a full-pure representative, and reduces active outcomes. The binary-party case is handled by actual finite cone simulation. The remaining binary–ternary case produces actual invertible physical frames.

`no_strict_residual_maximum` in `Bell/ResidualClosure.lean:54` receives this concrete geometry and proves the required contradiction. The local maximum on the incidence constraints is derived from a physical realization map. Stationarity is derived using the implicit-function/Lagrange machinery. Strict positivity of multipliers is derived from a deterministic-replacement score identity. Rank zero is simulated by a finite PVM mixture, rank one is incompatible with stationarity and positive multipliers, and rank at least two has a feasible improving direction. These intermediate hypotheses are discharged by the calling chain. An acyclic import graph alone would not establish this; the reviews traced the actual applications and their physical premises.

The separation route is also physical. A ternary qubit PVM must have a zero effect; all three zero positions, deterministic cases and mixed states are covered. An exact operator SOS proves the stronger PVM upper bound `289/10`, from which the paper's bound

\[
U=20\sqrt2+\frac35+\frac{4+3\sqrt2}{250}
\]

follows. The physical simple witness attains `20√2 + 16/25` and the Appendix B witness attains `(16+8√7813)/25`. The exact inequalities, finite-hull extension, strict separation, one-input equality and minimum-input classification are formal endpoints. No global optimality claim for either attained POVM value is certified or needed.

## Findings requiring correction or qualification

### R1 — Correct or qualify the strict-domain equivalence in the paper

At `paper/main.tex:1036–1049`, the definition first requires signature `(1,3)`, then says equivalently that all distinct-ray products are positive. If the signature requirement is retained in the background, this can be read correctly as a statement about common time orientation. If the second sentence is intended as a standalone characterization of the first, it is false.

Take

\[
a=d=\frac6{25},\qquad b=c=\frac3{100},\qquad
 e=a+b+c+d-\frac12=\frac1{25}.
\]

All four displayed pair sums are `27/100 < 1/2`. All five coefficient rays are null; every distinct-ray pairing is positive, including the four pairings with the fifth ray, each `23/100`. Nevertheless for

\[
u=(1,1,0,0),\qquad v=(2,-2,5,-5)
\]

one obtains

\[
u^Tgu=1,\qquad u^Tgv=0,\qquad v^Tgv=\frac{12}{5}.
\]

Their span is positive definite, so this metric cannot have signature `(1,3)`; in fact it has signature `(2,2)`. This is a rational certificate, not a floating-point eigenvalue observation. See [the independent exact calculation](evidence/independent_domain_counterexample.json), [the Lean probe](computations/StrictDomainCounterexample.lean), and the incidence review.

Suggested manuscript correction: “For a metric of this normal form **already assumed to have signature `(1,3)`**, the distinct null rays lie in one time cone exactly when all distinct-ray products are positive.” Explicitly retain the signature condition throughout the definition.

This does **not** refute the Lean equality: `Lorentz.StrictParameters` deliberately records only the scalar inequalities, and the final physical closure separately assumes and constructs `g = EᵀJE` with invertible `E`. The actual source does not infer Lorentz signature from the false scalar criterion.

### R2 — Do not claim literal formalization of all mathematics in the paper

The [complete matrix](reviews/coverage.md) distinguishes proved endpoints, specializations, alternative proof routes and missing auxiliary statements. Principal examples of mathematics not present in full claimed generality as production Lean theorems are:

- General finite-POVM SDP dual attainment and complementary slackness; the determinant pullback/KKT package. The main proof instead derives the multipliers by physical deterministic replacements.
- The full smooth 14-dimensional incidence-manifold statement and the paper's full inverse-metric Hessian formula and inertia `(4,12)`. The main proof uses surjectivity, differentiable feasible curves and an exact score-gap argument sufficient for rank closure.
- The arbitrary pointed-cone circuit lemma, general mixed-state common-span statement, and arbitrary extremal-POVM rank-square inequality. The proof implements the specializations required by its qubit reduction.
- The paper's original physical-to-scalar projective-bound derivation. Selected scalar algebra is formalized, but the end-to-end bound uses the stronger SOS argument.
- The ideal auxiliary PVM discrimination bound `3/5`, Appendix B's specific dual slacks, differentiation and unique-critical-point assertions, and some individual spectral/coordinate identities. These are independently checked or explained where appropriate in the separation review; an attained-value theorem is not itself a proof of all those statements.
- General stochastic-postprocessing and smaller-dimension embedding bridges as standalone formal statements.

These are coverage findings, not claims that the listed mathematics is false. Alternative proofs legitimately certify their final conclusions. The recommended description is: “The principal behavior-set equality, finite projective simulation, minimum-setting classification, explicit separation and strengthened attained value are formalized; selected auxiliary arguments are specialized or replaced.”

### R3 — State the verification trust boundary accurately

A fresh build of all project modules checks their proof terms using the installed pinned Lean toolchain and imported dependency artifacts. It does not rebuild all Mathlib from source or independently validate the compiler binary's implementation. Standard theorem dependencies `propext`, `Classical.choice` and `Quot.sound` are permitted; project-specific axioms and `sorryAx` are not. The axiom audit is transitive, so an unqueried private helper cannot conceal a nonstandard axiom from an audited endpoint.

The adversarial provenance check found the expected compiler version/hash, all nine dependency revisions matching the manifest, clean tracked dependency sources, no untracked Lean-source shadowing outside build directories, and no inherited Lean path override. The binary hash and details are retained in [adversarial_provenance.json](evidence/adversarial_provenance.json). Reusing the pinned dependency cache is an explicit trust assumption, not a defect unique to this development.

## Fresh validation receipt

**PASS.** Run `20260912T035656Z-0dca7f1e` started at 03:56:56 UTC and finished at 04:10:34 UTC on 12 September 2026. The isolated work copy began without Bell build products.

| Check | Result |
|---|---|
| All 58 production mathematical modules and aggregate `Bell` rebuilt | Passed |
| Valid proof accepted; deliberately invalid proof rejected for the expected reason | Passed |
| Both production statement-contract files | Passed |
| All 675 public theorem transitive dependency reports | Passed; only `propext`, `Classical.choice`, `Quot.sound` |
| Source/configuration snapshot unchanged within the run; dependency source pins rechecked | Passed |
| Original production Lean sources and primary TeX unchanged across this referee run | Passed |
| Independent explicit complex-matrix set equality contract | Passed at 04:11:03 UTC, with only the same three standard axioms |
| Eight supplementary harness / exact-algebra suites | Passed after the two documented copy-preparation fixes |
| Standalone Mathlib-only strict-domain rational counterexample | Passed |

See [fresh build receipt](evidence/kernel_report.json), [full axiom audit](evidence/axiom_audit.json), [independent matrix contract receipt](evidence/matrix_contract.json), and [evidence guide](evidence/README.md). These were produced in this referee assignment and are independent of the older production receipts. Supporting source reviews were completed before the final build receipt; their conditional verification language is resolved by these results.

Supplementary evidence already completed includes the direct-source rational SOS replay in [separation_exact.py](computations/separation_exact.py), all 144 LDL entries, 12 positive pivots, the full noncommutative operator identity, and a corruption rejection test. Harness tests and finite algebra checks are additional evidence, not substitutes for Lean validation.

## Reproduction and preserved scope

Run `python3 reproduce.py` from a fresh copy of this audit folder after removing or archiving an existing ignored `work/` directory. It requires the pinned environment already present in the adjacent `bell_lean/`. The script deliberately refuses to overwrite an existing work copy. Then run `python3 verify_contract.py` to check the independent matrix contract against that fresh build. The two additional referee probes are reproducible with `python3 computations/separation_exact.py` and, from the isolated project, `lake env lean` on the absolute path to `computations/StrictDomainCounterexample.lean`.

The first minimal copy omitted a historical ZIP required by the runner and failed before Lean was invoked; it was corrected without changing any production source. Two supplementary scripts initially lacked a copied reference PDF or output directory; their errors and corrected reruns are preserved and do not count as successful checks. The final evidence must be assessed from successful complete runs, not from these preparation failures or historical receipts.

All review work remains in this dedicated directory, with dated checkpoints in [RESEARCH_LOG.md](RESEARCH_LOG.md). Production mathematical sources, manuscript text and pre-existing user changes were preserved. No individual was contacted, and no immutable GitHub/Zenodo release was created.
