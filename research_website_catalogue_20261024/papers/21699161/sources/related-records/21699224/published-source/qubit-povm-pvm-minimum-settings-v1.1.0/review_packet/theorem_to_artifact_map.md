# Theorem-to-artifact map

All paths below are relative to the package root. Manuscript labels are more
stable than page or theorem numbers and should be used during review.

## How to read this map

The manuscript is the proof. The executable artifacts provide exact checks of
finite data, displayed algebraic identities, and selected constructions. A
passing verifier is corroborating evidence within its stated boundary; it is
not a formal proof of the universal theorem.

The evidence classes used below are:

- **Manuscript:** general proof in `paper/main.tex` or `paper/appendices.tex`.
- **Exact data/symbolic:** exact arithmetic on supplied data or symbolic
  identities.
- **Exact regression:** a general written identity tested on a nontrivial exact
  instance.
- **Example:** an executable construction for one instance.

## Main theorem and load-bearing results

| Result or dependency | Manuscript-proof location | Verifier scripts and data | What the artifact certifies | What the artifact does not certify |
|---|---|---|---|---|
| **Fixed-qubit model and convexified sets** | `paper/main.tex`, `sec:model`, including `lem:convexification`, `lem:nearest`, and `prop:support-functions` | None | Not applicable. | Compactness, separation, support-function equivalence, and the distinction between raw and convexified sets are manuscript proofs. |
| **Exact \(3\times2\) separation** (`thm:separation`) | `paper/main.tex`, `sec:separation`; `paper/appendices.tex`, `app:separation-algebra` and `app:strengthened` | `artifacts/three_by_two_separation/verify_exact.py`; `artifacts/three_by_two_separation/bell_coefficients_dense.csv`; `artifacts/three_by_two_separation/bell_coefficients_sparse.csv`; `artifacts/three_by_two_separation/strategy_simple_qsqrt2.json`; `artifacts/three_by_two_separation/strategy_strengthened_algebraic.json` | **Exact data/symbolic:** coefficient-table agreement; POVM/PVM normalization checks; projectors and rank-one factorizations; exact \(L_0,L_1,U\); discrimination dual certificates; determinant and discriminant identities; robust square-root comparison; CHSH scalar identities; six rank patterns; complete square; both exact gaps. | It does not numerically or symbolically optimize over all continuous PVM strategies. The pure-state/Schmidt reduction, deficit estimates as inequalities with valid sign domains, support exhaustion in the Bell problem, and assembly of the global bound are the manuscript proof. It also does not show that \(L_0,L_1\), or \(U\) are exact global optima. |
| **Heterogeneous \((2,2,3)\)-by-\((2,2)\) interpretation of the witness** | `paper/main.tex`, opening of `sec:separation` | `artifacts/three_by_two_separation/bell_coefficients_dense.csv` and `artifacts/three_by_two_separation/bell_coefficients_sparse.csv` encode a common three-label Alice table; `artifacts/three_by_two_separation/strategy_simple_qsqrt2.json` uses zero effects on the first two Alice inputs. | **Exact data:** the zero-label embedding used by the checked strategy and coefficient table is internally consistent. | Equivalence to the heterogeneous declared-output formulation uses the manuscript's deterministic coarse-graining argument. |
| **Three-dimensional cone circuit lemma** (`lem:lorentz-circuit`) | `paper/main.tex`, `sec:reductions` | None | Not applicable. | Minimal dependence, sign-pattern exclusion, and the two-versus-two conclusion are entirely manuscript linear/convex geometry. |
| **One-binary-party simulation** (`thm:binary-party`) | `paper/main.tex`, `sec:reductions`; `paper/appendices.tex`, `app:binary-degeneracies` | None | Not applicable. | No script proves the binary-POVM spectral mixture, cone-image classification, circuit elimination, canonical-purification lift, rank-one-\(\Omega\) construction, label bookkeeping, or the existence of one common shared-randomness decomposition of the complete behavior. |
| **Extreme raw realization** (`lem:extreme-hull`) | `paper/main.tex`, `sec:reductions` | None | Not applicable. | The fact that an extreme point of a compact hull lies in the compact generating set is a manuscript finite-dimensional proof. |
| **Common-span filtering** (`lem:common-span`) | `paper/main.tex`, `sec:reductions` | None | Not applicable. | Positivity of the filtered effects, exact behavior decomposition, and the scalar-intersection consequence are manuscript operator arguments. |
| **Residual-architecture reduction** (`thm:residual-reduction`) | `paper/main.tex`, `sec:reductions`; `paper/appendices.tex`, `app:extremal-povm` | None | Not applicable. | Selection of a pure entangled state and extremal POVMs, zero-effect handling, stochastic-to-deterministic PVM replacement, preservation of the span condition, and exclusion of four-outcome extrema are manuscript proofs. |
| **Lorentz representation of a residual strategy** (`lem:lorentz-representation`) | `paper/main.tex`, `sec:incidence` | `artifacts/two_by_two_closure/verify_exact.py`; `artifacts/two_by_two_closure/closure_formulas.json` | **Exact symbolic:** metric null rays, normalization, and the metric differential formula. **Exact regression:** the conformal-Lorentz relation on an exact algebraic trine instance. `closure_formulas.json` records the intended formulas in machine-readable form. | The JSON is a summary, not a proof certificate. The general trace-pairing factors, determinant polarization, frame invertibility, and identity \(P^Tg^{-1}P=4|\det\Xi|^2h\) are proved in the manuscript; one regression instance does not establish them universally. |
| **Local physical completeness** (`thm:physical-completeness`) | `paper/main.tex`, `sec:physical` | `artifacts/two_by_two_closure/verify_exact.py` | **Exact symbolic:** independence witnesses for the five matrices \(r_jr_j^T\), used in the smoothness calculation. | The verifier does not construct smooth Lorentz frames in general, prove time orientation and full rank remain open, reconstruct every nearby strategy, or integrate every tangent to a two-sided physical curve. |
| **Smooth incidence manifold** (`prop:smooth`) | `paper/main.tex`, `sec:physical` | `artifacts/two_by_two_closure/verify_exact.py` | **Exact symbolic:** the fixed coefficient-ray independence witnesses. | The open-stratum hypotheses, independence of normalization, regular-level-set conclusion, and 14-dimensional count as a statement about the manifold are manuscript arguments. |
| **Finite POVM duality** (`lem:povm-duality`) | `paper/main.tex`, `sec:multipliers`; `paper/appendices.tex`, `app:duality` | None | Not applicable. | Closedness, separation, dual attainment, and complementary slackness are manuscript proofs. |
| **Determinant pullback and strict multipliers** (`lem:determinant-pullback`, `prop:positive-multipliers`) | `paper/main.tex`, `sec:multipliers` | The conformal-Lorentz regression in `artifacts/two_by_two_closure/verify_exact.py` checks one upstream scaling identity only. | **Exact regression:** catches a possible factor error in one exact upstream Lorentz instance. | No executable proves the effect-level KKT pullback, identifies the two per-input dual operators, proves \(\lambda_j\ge0\), or proves that a zero multiplier yields a local/PVM behavior. |
| **Weighted second form and inertia** (`prop:second-form`) | `paper/main.tex`, `sec:second-variation`; `paper/appendices.tex`, `app:square-completion` | `artifacts/two_by_two_closure/verify_exact.py` | **Exact regression:** the Hessian square completion on a nontrivial exact \(4\times4\) instance. **Exact symbolic:** injectivity witnesses for \(\mu\mapsto\Lambda_\mu\). | The script does not prove the general first-variation/Fredholm condition, \(\dim\mathcal H_K=16-k\), inertia \((4,12)\) for all strict residual points, radial normalization, or the existence of a positive physical direction. |
| **Rank-\(\ge2\) obstruction** | `paper/main.tex`, `sec:closure`, subsection “Rank at least two” | Upstream Hessian checks in `artifacts/two_by_two_closure/verify_exact.py` | It checks the algebraic square-completion layer used upstream. | The dimension bound on nonpositive subspaces and its integration into an uphill physical curve are manuscript proofs. |
| **Projective fiber theorem and rank-one obstruction** (`prop:fiber`) | `paper/main.tex`, `sec:closure`; `paper/appendices.tex`, `app:fibers` | `artifacts/two_by_two_closure/verify_exact.py` | **Exact symbolic:** quadratic map, generic inverse, minor identity, direct/cross exceptional factors, two resultants, base-root factors, and the displayed degeneracy factorization. | A computer-checked resultant is not the full injectivity theorem. The strict-inequality sign arguments, zero-coordinate cases, nonvanishing alternatives, intersection exhaustion, and conversion to the positive-multiplier contradiction are human. |
| **Rank-zero deterministic simulation** (`prop:rank-zero`) | `paper/main.tex`, `sec:closure`; `paper/appendices.tex`, `app:transport` | `artifacts/two_by_two_closure/verify_exact.py`; `artifacts/two_by_two_closure/rank_zero_simulator.py` | **Exact symbolic:** flow row and column identities and the trine-cycle identities. **Example:** the simulator decomposes the symmetric trine table into six rational deterministic components and checks all four blocks. | The base-ray permutation/common-scale argument and the interval-intersection proof of a feasible bounded flow for every admissible table are human. The one trine run is not a universal enumeration. |
| **Universal two-input equality** (`thm:two-input-equality`) | `paper/main.tex`, `sec:closure`, subsection “Equality” | All closure artifacts above; `artifacts/two_by_two_closure/closure_formulas.json` names the intended outcome | The artifacts corroborate several exact identities used along the residual branch. | No script enumerates arbitrary finite output alphabets or proves convex-set equality. Compact separation, arbitrary-output reduction, physical exactness, multiplier positivity, and rank exhaustion are manuscript proofs. |
| **Minimum input architecture** (`cor:minimality`) | `paper/main.tex`, end of `sec:closure` | All \(3\times2\) separation artifacts plus the closure artifacts | The artifacts certify the exact witness data and the finite algebraic layers of the closure proof. | The logical combination “one input is local + two inputs are equal + \(3\times2\) separates” is the manuscript proof. Novelty or priority is outside these artifacts. |

## Reproducibility and integrity layer

| File | Role | Boundary |
|---|---|---|
| `run_all.sh` | Checks the SymPy version, verifies artifact hashes, and runs both verifiers and the rank-zero simulator offline. | It orchestrates existing checks; a successful run is not a formal proof of claims outside those checks. |
| `artifacts/SHA256SUMS.txt` | Freezes the eight exact artifact files consumed or distributed by the runner. | It certifies byte identity only, not mathematical correctness. It does not freeze the entire manuscript or submission package. |
| `requirements.txt` | Pins the required SymPy version. | Environment specification is not mathematical evidence. |
| `reports/verifier_report.txt` | Records a prior clean execution and its disclosed verification boundary. | It is a historical run log; rerunning `./run_all.sh` is the live check. |
| `artifacts/two_by_two_closure/closure_formulas.json` | Machine-readable summary of the closure coordinates, second form, and rank cases. | It is not parsed as a proof by the closure verifier and must not be cited as independent certification of the universal theorem. |

## Reviewer-critical manuscript-only steps

The following steps have no finite executable substitute and deserve direct
line-by-line review:

1. the cone-circuit decomposition and simultaneous PVM lift;
2. the extreme-point/common-span reduction for arbitrary finite outputs;
3. local physical reconstruction and two-sided tangent integration;
4. the per-input KKT pullback and strict positivity of all five multipliers;
5. the dimension argument for rank at least two;
6. exceptional-fiber exhaustion beyond the checked identities;
7. general bounded transportation and simultaneous reconstruction of all four
   rank-zero setting blocks; and
8. assembly of the continuous global PVM upper bound for the \(3\times2\)
   functional.
