# Known risks and publication conditions

## Summary

No located risk presently invalidates the mathematical theorem chain. The
self-contained manuscript, bibliography, and reproducibility package now
close the internal release conditions identified during the audit. The
highest remaining risk is external: the proof has not yet received expert
human peer review. Priority language also remains qualified and should be
rechecked immediately before journal or arXiv submission.

## Risk register

| Risk | Severity | Status | Required treatment |
|---|---:|---|---|
| Full human D1–D3 proofs originally came from a frozen Phase-I manuscript outside the publication folder | High | RESOLVED | The required D1–D3 arguments are incorporated into `paper/main.tex` and `paper/appendices.tex`; exact data are copied and hashed under `artifacts/three_by_two_separation/`. |
| Closure bundle originally contained only hashes of D2–D3 checkpoint files | High | REPAIRED mathematically | Exact preimages were recovered in `two_setting_qubit_checkpoint.zip`, and the full proofs occur in Phase-I §10. The publication bundle must include the proofs, not only hashes. |
| PVM convention could be misunderstood | High | REPAIRED wording | State the formal definition from `proof_audit.md`, including branchwise dimension, zero projections, postprocessing, and shared randomness. |
| D3 is theorem-sized and highly load-bearing | High | PASS, referee focus | Include the full common-span filtering and behavior-extremality proof in the paper. Do not summarize D3 as a frozen black box. |
| Positive incidence multipliers are load-bearing | High | REPAIRED wording | Derive the pullback separately for the binary and ternary Bob inputs, with distinct \(\Gamma_y\), complementary slackness, uniqueness, and the zero-slack deterministic tie. |
| Boundary and arbitrary-output completion could appear assumed | High | REPAIRED organization | Place D2 and D3 before the residual closure and explicitly state that repeated rays, zero effects, product states, and four-outcome extrema have already been removed. |
| Literature novelty and priority | High | READY with qualification | `priority_audit.md` and `equivalence_audit.md` document a current primary-source search. The \(3\times2\) phenomenon is prior art; only the arbitrary-output \(2\times2\) closure and minimum-setting classification are positioned as plausibly original, using “to our knowledge.” Repeat the search immediately before submission. |
| Phase-I manuscript says the residual case is unresolved | Medium | REPAIRED historically | Label it as a frozen earlier phase and explain that the later Lorentz-incidence theorem resolves its stated remaining obstruction. Do not present both status statements without chronology. |
| Legacy `PHASE1_SHA256SUMS.txt` names `verify_exact.py`, while the download was named `verify_exact(1).py` | Low | RESOLVED in publication suite | The publication artifact has the canonical name `verify_exact.py`, preserves the expected hash, and is covered by the new artifact manifest. |
| Legacy outer checkpoint manifest references an absent `discovery_code/` directory | Low | RESOLVED for release | Exact preimages verify inside the checkpoint ZIP. Exploratory code is deliberately excluded from the proof-critical publication runner. |
| Duplicate numbered strategy JSON | Low | RESOLVED in publication suite | Only canonical `strategy_strengthened_algebraic.json` is included in the exact artifact directory. |
| Duplicate sparse coefficient CSV under a legacy name | Low | RESOLVED in publication suite | The publication suite contains canonical dense and sparse files only. |
| Legacy proof has malformed control-character LaTeX | Medium | RESOLVED | The malformed legacy file is excluded. The consolidated paper compiles without LaTeX warnings. |
| Reproducible Python environment | Medium | RESOLVED | `requirements.txt` pins SymPy 1.14.0, `run_all.sh` checks the version and artifact hashes, and the recorded clean run passed from `/tmp`. |
| Exploratory checkpoint code has hard-coded `/mnt/data` paths and a missing exploratory import | Low | ACCEPTED, nonproof | Label it exploratory and exclude it from the proof-critical execution path, or make it portable separately. |
| Exact verifiers may be mistaken for full formal proofs | Medium | REPAIRED wording | State their precise coverage. D2, D3, compactness, sign implications, and quantified geometric conclusions remain human proofs. |
| Closure Hessian verifier uses an exact test instance | Medium | PASS with disclosure | Retain the human general derivation; describe the executable as a regression check for order, transpose, and sign errors. |
| Closure pure-state Lorentz verifier uses one exact algebraic example | Low | PASS with disclosure | Retain the determinant/polarization proof in the paper. |
| Rank-zero simulator tests one symmetric trine | Low | PASS with disclosure | Retain the general interval-intersection proof; present the simulator as an example constructor. |
| Exceptional-fiber proof omits two zero-coordinate sentences | Medium | REPAIRED wording | Insert the two base-ray checks from `proof_audit.md` before scaling the exceptional planes. |
| “Every tangent integrates” is asserted tersely | Medium | REPAIRED wording | Invoke the submanifold theorem and openness of the physical strict stratum; state that the curve exists for both signs of \(t\). |
| Zero joint probabilities could look like a positivity boundary gap | Medium | REPAIRED wording | Emphasize reconstruction as traces of positive operators, so incidence curves remain physical without entrywise strict positivity. |
| “Residual dimension \(14\)” can conflate incidence and projected dimensions | Medium | RESOLVED wording | The paper states only that the normalized incidence manifold has dimension \(14\) and explicitly says the projected behavior image has dimension at most \(14\). |
| D2 repeated-ray and rank-one-\(\Omega\) bookkeeping is terse | Medium | REPAIRED wording | Insert the circuit paragraph supplied in `proof_audit.md`. |
| D3 deterministic-postprocessing replacement may appear to lose the span-intersection property | Medium | REPAIRED wording | Reapply the filtering lemma after retaining the behavior-extreme deterministic component. |
| D3 treatment of zero effects is implicit | Low | REPAIRED wording | Delete zero effects before span/rank and positive-marginal arguments, then reinsert zero output labels at the end. |
| Exact global D1 PVM optimum is unknown | Low | ACCEPTED scope | State only \(\beta_{\rm PVM}\le U\). Do not call \(U\) the exact optimum. |
| Exact global D1 POVM optimum is unknown | Low | ACCEPTED scope | State only \(\beta_{\rm POVM}\ge L_1\). The strict separation does not require equality. |
| Strengthened strategy is optimal only in a one-parameter family | Low | PASS with disclosure | Preserve the limitation stated in Phase-I §§4 and 11. |
| Equality cases and maximizers of locking bounds are unclassified | Low | ACCEPTED scope | List as future work, not as part of the theorem. |
| No bibliography in the frozen mathematical sources | High | RESOLVED | `paper/references.bib` contains audited primary-source records; every manuscript citation resolves and the BibTeX build passes. |
| Independent peer review has not occurred | Medium | UNRESOLVED process | Seek mathematical referee review, focusing on D2, D3, and the positive-multiplier bridge. The independent-research policy forbids Codex from initiating contact. |

## Load-bearing proof risks

### 1. D3 residual reduction

**Status: PASS, but highest referee priority.**

D3 is indispensable: without it, the Lorentz-incidence closure proves only the
genuine \((2,3)\)-by-\((2,3)\) architecture. The recovered Phase-I manuscript
contains a real proof rather than merely a checkpoint assertion. The proof was
rederived successfully:

- compactness and behavior extremality produce an unrandomized realization;
- state and measurement decompositions give a pure entangled state and
  extremal POVMs;
- common-span filtering forces scalar-only intersection;
- dimension and support-perturbation bounds yield binary-plus-ternary
  architecture;
- D2 removes the case of two binary inputs on one party.

The paper should give this proof in full.

### 2. Positive determinant multipliers

**Status: PASS after exposition repair.**

The closure's inertia argument requires \(\Lambda>0\). Equality-constraint
multipliers do not have a sign by themselves; the sign comes from the separate
local POVM dual problems. The corrected pullback/uniqueness proof in
`proof_audit.md` must appear verbatim or at equivalent rigor.

### 3. Physical completeness of incidence tangents

**Status: PASS after exposition repair.**

An uphill direction on an algebraic variety is useful only if it is a physical
two-sided curve. The reconstruction proof supplies positive rank-one effects,
the reduced state, the other party's POVMs, and a pure state at every nearby
strict incidence point. The paper should connect this explicitly to the
submanifold theorem.

### 4. Singular rank strata

**Status: PASS.**

The generic curvature argument does not cover ranks zero and one.

- Rank one is removed by projective injectivity of the quadratic null-ray map.
- Rank zero is not discarded by curvature; it is explicitly decomposed into
  deterministic local behaviors.

Both branches are essential and must remain in the main proof rather than an
informal appendix summary.

## Claims that must not be made

- Do not call \(L_1\) the exact global POVM optimum.
- Do not call \(U\) the exact global PVM optimum.
- Do not say the exact verifier proves D2, D3, compactness, or every quantified
  inequality.
- Do not call the historical Phase-I manuscript a proof of two-setting equality;
  it deliberately stopped at the residual architecture.
- Do not claim a \(7,7\) intrinsic Hessian signature; that exploratory
  conjecture was false and was replaced by the correct ambient inertia
  \((4,12)\).
- Do not claim literature priority without the separate novelty record.
- Do not state “PVM” without the fixed-dimension and postprocessing convention.

## Remaining release and submission conditions

The internal self-contained-release conditions are satisfied. Before claiming
independent verification or journal readiness:

1. Obtain expert human scrutiny focused on D2, D3, the physical incidence
   reconstruction, and the multiplier-sign bridge.
2. Repeat the 2025--2026 preprint and citation search immediately before
   submission.
3. Recheck the selected journal's current board, disclosure, source-archive,
   and conflict requirements.
4. Keep the final release manifest and clean-room verifier report synchronized
   with any later source change.

Subject to those external checks, the proof audit supports the final theorem
and its minimum-setting corollary.
