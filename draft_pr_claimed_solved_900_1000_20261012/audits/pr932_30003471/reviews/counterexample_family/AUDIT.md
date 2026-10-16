# Direct counterexample audit: PR932 / 30003471

Final UTC: 2026-10-15T07:38:21.698020+00:00. Family audit complete; completion estimate 100%. Overall discovery completion is not estimated by this finite falsification family. Status: **CONDITIONAL — no certified counterexample found; no universal theorem inferred**. Original author proof-search budget remains **1/5**; this audit adds zero new positive author turns. No new positive-proof route was initiated.

## Exact object and independence

The full charter, complete private source record, and full original proof were read before `INITIAL_RECONSTRUCTION.md` was written. No historical audit/acceptance verdict, other current family output, original control program, or outside input was consulted. All new files are confined to this family directory. No outside individual was contacted and no outreach was prepared. No Git write, publication, service write, or tracker change was performed.

Pinned original head: `c09ef9df8b1f4642be0396ba6343344be8fa25b0`. Proof SHA256: `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`. Original outer publication manifest SHA256: `d1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd`.

`authenticate.py` independently compared the actual Git blobs at that exact head with all 29 assigned original disk files and expected byte lengths/digests, both before and after the mathematical work. Both checks passed. Start UTC 2026-10-15T07:28:40.479424+00:00; end UTC 2026-10-15T07:36:30.955640+00:00. Actual workspace head at both checks was `fa24428a4fa6930fd3df9dc1b2feb0f7c72885c9`. Original object identity is separate from the current workspace head. `AUTH_START.json` and `AUTH_END.json` contain every actual file digest.

## Claim, sign, and success criterion

For each corresponding adjacent facet pair, write `D_ij = m_i dot m_j - n_i dot n_j`. Since the interior angle is `theta=pi-acos(normal dot normal)`, `D_ij >= 0` means the second polytope has at least as large an interior angle. Strict positivity at every edge would refute the exact original target after reversing the ordered pair. Weak nonnegativity at every edge together with a changed entry of the complete normal Gram matrix would refute the author's stronger theorem. This includes the possibility that all adjacent entries are equal but some nonadjacent entry changes.

Every optimization required squared Frobenius separation of complete Gram matrices at least 0.01. This excludes similarities and complete-Gram equality without assuming that adjacent entries must change. Strict numerical candidate threshold was `min(D)>1e-7`; weak candidate screening threshold was `min(D)>=-1e-9`, in the presence of the verified Gram separation. These are screening thresholds, not mathematical certificates. Every found candidate would have needed exact rational or validated interval evidence for full dimensionality, convexity, face lattice, edge correspondence, and every inequality. None reached screening, so no counterexample certificate is asserted.

## Direct geometric search mechanisms

The primary seed is 93230003471. There were five bounded SLSQP starts each for tetrahedron, triangular prism, cube, pentagonal prism, truncated cube, and pyramids with 4, 5, and 8 base sides: 40 endpoints. The extended seed is 93230003472. Two starts each were run for independently perturbed asymmetric instances of the five simple types, affine-distorted pyramid bases with noncentral apexes, and regular/asymmetric octahedra: 20 more endpoints. All six vertices of an octahedron are nonsimple; the pyramid apexes have incidence 4, 5, or 8.

Simple models vary each facet normal in its two tangent coordinates and renormalize it, keeping positive support values fixed. The coordinate bounds are [-0.65,0.65], initial random coordinates [-0.24,0.24], and all nonincident vertex-plane slacks are constrained to at least 1e-4. The normal parameterization is an open local chart; it is not every possible normal fan. Pyramid models vary the convex planar polygon and apex horizontal position, with apex height fixed at one. Parameter displacement is bounded by 0.65 and initial displacement by 0.2. All side planes remain concurrent by construction; polygon convexity is constrained by signed areas at least 1e-4. Octahedral models vary six vertices independently, displacement bounded by 0.5 and initial displacement by 0.15, while retaining eight oriented triangular supporting facets. Every nonincident supporting-plane slack must be at least 1e-4.

The objective maximizes the smallest corresponding normal-dot increase, with the Gram separation constraint. SLSQP stops at ftol 1e-10 or 180 iterations for simple models / 200 for pyramid and octahedral models. The exact input normals/supports/vertices, final coordinates, objective values, edge differences, stop messages, iterations, seeds, all parameters and constraints are in `SEARCH_RESULTS.json` and `EXTENDED_SEARCH_RESULTS.json`. No unbounded sampling or huge exhaustive search was used.

Each base and endpoint was checked independently from its halfspaces: enumerate every feasible triple-plane intersection; deduplicate; recover every vertex's entire facet-incidence set; require each facet to have at least three vertices; recover all ridge pairs; check positive three-dimensional hull volume; and check that zero is strictly inside the convex hull of the unit normals, which numerically tests boundedness. Final incidence and edge lists must exactly match the base's labels. All 60 endpoints passed these numerical checks and their optimization feasibility conditions; all 60 optimizers reported successful stopping. `verify_artifacts.py` independently re-enumerated the stored halfspaces, topology and edge differences instead of trusting search flags.

| Family | Starts | Best minimum D |
| --- | ---: | ---: |
| cube | 5 | -0.01164971365 |
| pentagonal_prism | 5 | -0.009372586369 |
| pyramid_4 | 5 | -0.007267829358 |
| pyramid_5 | 5 | -0.004080509815 |
| pyramid_8 | 5 | -0.001152159904 |
| tetrahedron | 5 | -0.01254787813 |
| triangular_prism | 5 | -0.01166194025 |
| truncated_cube | 5 | -0.006168635765 |
| asymmetric_cube | 2 | -0.01115412973 |
| asymmetric_octahedron | 2 | -0.004109259071 |
| asymmetric_pentagonal_prism | 2 | -0.008981347395 |
| asymmetric_pyramid_4 | 2 | -0.007355676046 |
| asymmetric_pyramid_5 | 2 | -0.003699807065 |
| asymmetric_pyramid_8 | 2 | -0.000986142134 |
| asymmetric_tetrahedron | 2 | -0.01243616632 |
| asymmetric_triangular_prism | 2 | -0.01048142644 |
| asymmetric_truncated_cube | 2 | -0.00428341207 |
| octahedron | 2 | -0.004362542452 |

There were zero strict or weak screening candidates. The largest of the 60 minimum edge differences was approximately -0.000986142134, so even the closest endpoint had a clearly decreasing edge. This is bounded falsification evidence only; local optimization failure does not prove nonexistence anywhere else.

## Exact and limiting controls

`CONSTRUCTIVE_CONTROLS.json` records exact SymPy identities independently implemented here. A rational orientation-reversing orthogonal map preserves the complete normal Gram matrix. Translation and positive scaling preserve outward normal directions. Boxes with different support values have identical complete normal Gram matrices even when their side ratios differ. Thus a conclusion about normals does not silently assert similarity of the primal shapes.

A rational cube shear produces both positive and negative edge-normal-dot changes, including exact values `1/sqrt(10)` and `-1/sqrt(10)` (with zero changes at other edges), checking the interior/exterior sign and all-edge comparison. At the regular tetrahedron and cube normal systems, the exact sum of all edge normal-dot first variations is zero for arbitrary tangent normal perturbations. These positive-weight local identities obstruct strictly positive first variations and force all first variations to vanish if all are nonnegative. They establish only those infinitesimal controls, not a global comparison theorem.

Exact Pauli anticommutators were checked with `c(e_j)=-i sigma_j`, and the commutant of all three Clifford matrices was computed to consist exactly of scalar matrices. This verifies the final finite-dimensional algebra conditional on a nonzero intertwiner with spanning target normals. It does not construct the analytic field or prove that its limiting mass survives.

The spherical interpolation singular values `t` and `sin(t theta)/sin(theta)` were sampled on 15,150 hemisphere parameter points, with maximum at most one to numerical tolerance. An explicit point outside the hemisphere, theta=2.8 and t=0.7, has azimuthal derivative greater than one. The exact planar-sector logarithmic annulus integral is `1/abs(log(delta))`; reported positive delta values demonstrate decay. This exact planar calculation does not establish all uniform boundary transports or Sobolev constants for arbitrary smoothed polytopes.

Positive-thickness rational boxes down to thickness 2^-20 retain volume, incidence, and right angles. Flattened square pyramids of heights 1, 0.1, 0.01, 0.001 retain the nonsimple apex while their minimum interior angles tend toward zero and maximum toward pi. Zero height, collapsed volume, merged facets and unbounded polytopes are excluded. Shape-dependent constants are not asserted uniform along such degenerating families. Opposite cube facets have total slack two and cannot both be active for lambda>2; nonsimple apex incidence was rechecked for 4, 5 and 8 sides. These are selected active-set controls, not universal localization proofs.

## Honest numerical limitations

All 18 finite-difference primal angle-Jacobian LP optima were within about 2.4e-11 of zero. The exact-equality dual stress LP returned positive weights for 14 families and failed for four, including the original 8-gonal pyramid. The original failure is preserved verbatim in its raw result: `positive_stress_success=false`, no returned weights or exact stress certificate. These failures may reflect finite-difference/equality tolerances; no rigorous conclusion is drawn from that explanation.

A separately labeled tolerance stress diagnostic for the original 8-gonal pyramid reported solver success but its independently recomputed residual is approximately 5.08e-8, exceeding the requested 1e-8. It is explicitly marked `residual_within_allowed=false` and `exact_certificate=false`. It is not a verified approximate certificate, much less an exact obstruction. This illustrates why solver status is not a substitute for postchecking feasibility. Exact cube/tetrahedron identities remain valid independently of all these LP receipts.

Searches are local, finite, and bounded. Most simple models hold support values fixed. Pyramid base coordinates and octahedral vertices are confined to recorded boxes. Only 18 base realizations were used, with no exhaustive treatment of combinatorial types, arbitrary pair geometries or near-degenerate moduli. Floating-point hull tests and Jacobians are empirical checks. No universal index, compactness, homotopy, or rigidity statement can follow from these data.

## Reproducibility and conclusion

Run `verify_artifacts.py --reproduce` in the recorded NumPy/SciPy/SymPy environment. It checks all stored coordinates, then reruns both deterministic search programs and exact controls in the excluded `tmp/reproduction` directory. The receipt compares every output datum except timestamps and elapsed times, using 1e-9 numerical tolerance. Exact environment versions are preserved in the primary search record; runtime was reused, not installed or altered. The primary and extended run receipts record clean completion. The final stored-coordinate and deterministic replay verdicts are both PASS for their stated finite scopes in `VERIFICATION_RECEIPT.json`.

No direct defect or counterexample to the author's theorem was found in this bounded family. There are no required mathematical issues identified by this family. The strongest checkable results are the exact finite-dimensional sign/invariance/Clifford/local-stress identities and the reproducible absence of screened dominance in these 60 explicitly listed topology-preserving endpoints. The exact remaining gap is universal: this method has neither a certified counterexample nor a complete proof excluding all global dominance pairs, and it does not discharge the smooth Dirac/topological/compactness hypotheses. The candidate must remain conditional on the independent analytic/geometric/source audits. Replacing this gap by an unsupported global angle-rigidity theorem would be blocked; that route was not pursued.

The curated public `MANIFEST.json` lists only the intended audit artifacts with bytes and SHA256. It excludes itself, the external digest receipt `VERIFY.json`, all `private/`, `tmp/`, `__pycache__/`, cached source documents, renders, and unrelated directories. `VERIFY.json` records the manifest's external digest and byte verification. No publication action is implied by the word public.
