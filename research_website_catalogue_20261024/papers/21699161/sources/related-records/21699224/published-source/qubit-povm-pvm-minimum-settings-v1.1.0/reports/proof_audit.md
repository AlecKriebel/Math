# End-to-end proof audit

**Audit date:** 2026-07-29
**Audited target:** the current manuscript and exact artifacts in this package

## Verdict

**PASS. No blocking mathematical issue remains in the stated theorem chain.**

The current manuscript proves, at full manuscript-proof level:

1. for every finite, input-dependent output architecture with two inputs per
   party,
   \[
   \overline{\mathsf Q}^{\mathrm{POVM}}_2(\mathbf A,\mathbf B)
   =
   \overline{\mathsf Q}^{\mathrm{PVM}}_2(\mathbf A,\mathbf B),
   \]
   with shared-randomness convexification, zero projectors, and classical
   output postprocessing on the PVM side; and
2. an explicit rational \(3\times2\) Bell functional has an attained qubit-POVM
   value strictly above a global upper bound for every fixed-qubit PVM
   strategy. Hence \(3\times2\), up to exchanging the parties, is the minimum
   input architecture for such a separation.

The formerly compressed proof bridges C--K have now been incorporated into
`paper/main.tex` and `paper/appendices.tex`. I rechecked those bridges against
the end-to-end dependency chain and found no remaining missing case or
unjustified implication that blocks either theorem.

This verdict is not a claim of formal verification or independent expert peer
review. The universal parts are mathematical arguments in the manuscript. The programs
check finite exact data and algebraic identities and serve as a
certificate/regression layer.

## Certification vocabulary

- **Manuscript proof** means the manuscript gives a quantified mathematical
  argument covering the full claimed class.
- **Exact finite check** means a script verifies specified data or symbolic
  identities with exact arithmetic. It does not automatically establish the
  surrounding quantified argument.
- **Exact regression instance** means a general identity is proved in the
  manuscript and independently tested on a nontrivial exact instance.
- **Illustrative construction** means an executable demonstrates one instance;
  generality still comes from the written proof.

The detailed theorem-to-file boundary is recorded in
`review_packet/theorem_to_artifact_map.md`.

## Audit basis

The primary proof sources are:

- `paper/main.tex`, especially the labeled results
  `lem:convexification`, `lem:nearest`, `prop:support-functions`,
  `thm:separation`, `lem:lorentz-circuit`, `thm:binary-party`,
  `lem:extreme-hull`, `lem:common-span`, `thm:residual-reduction`,
  `lem:lorentz-representation`, `thm:physical-completeness`, `prop:smooth`,
  `lem:povm-duality`, `lem:determinant-pullback`,
  `prop:positive-multipliers`, `prop:second-form`, `prop:fiber`,
  `prop:rank-zero`, `thm:two-input-equality`, and `cor:minimality`;
- `paper/appendices.tex`, especially `app:separation-algebra`,
  `app:strengthened`, `app:binary-degeneracies`, `app:extremal-povm`,
  `app:duality`, `app:square-completion`, `app:fibers`, and `app:transport`;
- the exact files under `artifacts/`, whose scope is described below.

On the audited checkout, `./run_all.sh` passed with Python 3.14.6 and
SymPy 1.14.0. It verified the hashes of all eight exact artifacts, all exact
\(3\times2\) certificate checks, all 39 reported closure checks, and the
symmetric-trine rank-zero construction.

## Expanded bridges C--K

| Bridge | Status | Manuscript-proof finding | Executable boundary |
|---|---|---|---|
| **C. Three-dimensional cone circuits and the one-binary-party theorem** | **PASS** | `lem:lorentz-circuit` now proves the support bound and the two-versus-two sign pattern. `thm:binary-party` explicitly treats terminating circuit extraction, retained labels, unique rank-one lifts, the full-rank canonical purification with the required transpose, rank-one \(\Omega\), zero and repeated rays, and one shared variable for the complete behavior. `app:binary-degeneracies` covers lower-dimensional cone images. | No script proves the cone decomposition or simultaneous behavioral reconstruction. These are manuscript proofs. |
| **D. Extreme residual architecture** | **PASS** | `lem:extreme-hull` closes the raw-realization selection step. `thm:residual-reduction` now spells out pure-state and extremal-measurement selection, deletion and reinsertion of zero effects, scalar-only common spans, the spectral-PVM postprocessing representation, reselection of a deterministic extreme component, reapplication of common-span filtering, and the rank-square exclusion of four-outcome extrema. | No finite verifier quantifies over all POVMs or exposed faces. `app:extremal-povm` is a manuscript support-perturbation proof. |
| **E. Lorentz conventions and representation** | **PASS** | `sec:incidence` fixes \(\det X=x^TJx\) and \(\operatorname{Tr}(XY)=2x^Ty\), proves that the selected four effects form a basis, defines the strict residual domain, and derives \(P=2\mathsf E_A^TL_\Xi\mathsf E_B\), \(L_\Xi^TJL_\Xi=|\det\Xi|^2J\), and \(P^Tg^{-1}P=4|\det\Xi|^2h\) with all factors accounted for. | The closure verifier checks the metric identities symbolically and the conformal-Lorentz relation on one exact trine instance. The general determinant/polarization proof is the manuscript's. |
| **F. Physical exactness and tangent integration** | **PASS** | `thm:physical-completeness` constructs a smooth Lorentz frame, reconstructs both parties' effects and the normalized full-rank state, explains the factor \(1/2\), proves nonnegative Born probabilities even at zero joint entries, and integrates every tangent through a regular-level-set chart on both sides. `prop:smooth` proves the six differentials independent on the stated open stratum. | The verifier checks finite independence witnesses, not the smooth reconstruction, openness, or integration theorem. |
| **G. KKT pullback and strict multiplier positivity** | **PASS** | `lem:povm-duality` and `app:duality` prove finite POVM duality. `lem:determinant-pullback` derives the effect-level stationarity equation separately for each input. `prop:positive-multipliers` identifies the KKT normalization multiplier with the per-input dual operator, obtains nonnegative multipliers, and gives an explicit hidden-variable/PVM model after a zero multiplier, proving strict positivity. | No script certifies dual attainment, multiplier identification, or the zero-multiplier locality implication. These are manuscript proofs. |
| **H. Compatibility, second variation, and rank at least two** | **PASS** | `sec:second-variation` now derives the first variation, the Fredholm compatibility condition, independence of the \(k\) compatibility functionals, and \(\dim\mathcal H_K=16-k\). `prop:second-form` proves square completion, inertia \((4,12)\), radial normalization without changing \(q\), and the maximum-sign convention. The rank-\(\ge2\) dimension contradiction then follows. | The closure verifier checks square completion on a nontrivial exact matrix instance and checks the \(\mu\mapsto\Lambda_\mu\) independence witnesses. The general differential, inertia, dimension, and physical-uphill arguments are manuscript proofs. |
| **I. Projective fibers and rank one** | **PASS** | `prop:fiber` and `app:fibers` give the base locus, generic inverse, all four exceptional divisors, direct and cross branches, permissible scalings, zero target coordinates, resultant degeneracies, strict-inequality exclusions, and exceptional intersections. This is sufficient for the rank-one multiplier contradiction. | The closure verifier reproduces the inverse identity, resultants, and listed factorizations exactly. It does not by itself prove the quantified injectivity or exhaustion; those use the written case analysis. |
| **J. Rank-zero simulation** | **PASS** | `sec:closure` proves that the transformed pentad preserves the binary/ternary partition, has a common scale, and normalizes to \(P=g\). `prop:rank-zero` defines the table entries and checks all four setting blocks. `app:transport` proves the bounded flow exists for every allowed table, including zero-capacity endpoints. | The closure verifier checks the flow row/column identities. `rank_zero_simulator.py` constructs one symmetric-trine instance. General feasibility and simultaneous reconstruction come from the interval proof. |
| **K. Exact \(3\times2\) separation** | **PASS** | `thm:separation` uses the simple attained value \(L_0\), not an asserted optimum. The manuscript separately proves POVM positivity and normalization, derives both CHSH deficit bounds, identifies the three score operators, lists all six ternary-PVM supports, proves the robust auxiliary bound, and completes the square to the global PVM bound \(U\). `app:strengthened` correctly presents \(L_1\) as an optional stronger attained lower bound, with one-parameter optimality confined to a remark. | The separation verifier checks the coefficient files, both strategies, dual factorizations, support patterns, algebraic bound identities, and exact gaps. The reduction from an arbitrary continuous PVM strategy to those inequalities remains the manuscript proof. |

## End-to-end dependency check

| Dependency | Status | Audit conclusion |
|---|---|---|
| Fixed-qubit model, convexification, and output postprocessing | **PASS** | The paper distinguishes raw strategy images from shared-randomness convex hulls, permits zero projectors, and forbids dimension-increasing dilation. |
| Compactness and support-function separation | **PASS** | Compactness, nearest-point separation, and equivalence between convex-set equality and equality of Bell support functions are explicit. |
| One-binary-party boundary cases | **PASS** | Binary POVMs, degenerate observables, repeated rays, zero effects, and rank-deficient circuit totals are all handled before the residual stratum. |
| Arbitrary-output reduction | **PASS** | Every hypothetical strict separator reduces to a pure full-Schmidt-rank \((2,3)\)-by-\((2,3)\) residual realization. |
| Incidence model is physically exact | **PASS** | The incidence equations are not used as an algebraic relaxation; nearby solutions reconstruct genuine strategies and tangents integrate physically. |
| Strictly positive multiplier matrix | **PASS** | The sign comes from local POVM duality and the explicit zero-slack contradiction, not from equality-constraint KKT conditions alone. |
| Exhaustive rank trichotomy | **PASS** | Ranks \(2,3,4\), rank \(1\), and rank \(0\) are respectively excluded by curvature, projective fibers, and explicit PVM simulation. |
| Universal two-input equality | **PASS** | Every putative separating functional is contradicted after the residual reduction. |
| Minimum input architecture | **PASS** | One-input scenarios are local, \(2\times2\) is closed by the equality theorem, and the exact \(3\times2\) witness supplies attainability. |

No circular dependency was found: the \(3\times2\) witness is not used to prove
the two-input equality; it is combined with that equality only for the final
minimality corollary.

## Verifier boundary

The exact runner establishes all of the following about the checked files:

- their bytes match `artifacts/SHA256SUMS.txt`;
- the dense and sparse Bell coefficient tables agree;
- both supplied strategies are normalized and attain their stated exact
  values, with the listed rank-one and dual factorizations;
- the determinant, discriminant, robust comparison, CHSH scalar, complete
  square, and exact gap identities used for the \(3\times2\) witness hold;
- the local metric, null-ray map, generic inverse, exceptional resultants,
  listed factorizations, and flow identities hold;
- a conformal-Lorentz identity and the Hessian square completion survive
  nontrivial exact regression instances; and
- the symmetric-trine rank-zero table is decomposed into six deterministic
  components.

The runner does **not** prove compactness, convex separation, cone-circuit
termination, extremal selection, common-span filtering, the general Lorentz
reconstruction, smooth tangent integration, dual multiplier signs, the
dimension obstruction, exceptional-case exhaustion, the general bounded-flow
existence theorem, or the universal equality. Those are supplied by the
manuscript and were audited as manuscript proofs.

## Nonblocking limitations and remaining review needs

- No independent expert human referee has yet certified the combined proof.
  The highest-value review targets remain the one-binary-party circuit lift,
  residual reduction, physical reconstruction, multiplier positivity, and
  exceptional-fiber exhaustion.
- The audit does not establish literature novelty or absolute priority.
- The exact global POVM and PVM optima of the \(3\times2\) functional are not
  known. The theorem needs only an attained lower bound above a global upper
  bound.
- The theorem is convexified behavior-set equality. It does not claim raw-set
  equality, same-state simulation, or operator-level simulability of every
  POVM.
- After any manuscript revision, the compiled PDFs, submission archive, and
  package-level freeze manifests should be regenerated before release. This is
  release engineering, not a mathematical gap.
