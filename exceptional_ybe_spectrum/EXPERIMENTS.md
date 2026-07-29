# Experiment ledger

All new computations must record the exact command, seed, environment, raw
output location, interpretation, and commit identifier.  The original
\(d=4\) discovery search was not preserved and is not described as
reproducible; only its final exact witness is reproducible.

## Environment E0

- Recorded: 2026-07-28 21:34 PDT
- Machine: Apple M1 Pro, arm64, 16 GiB physical RAM
- OS: macOS 26.5.2 (build 25F84)
- Python: 3.9.6
- SymPy: 1.14.0
- NumPy: 2.0.2
- SciPy: 1.13.1
- Repository baseline: `ed87345d726da7c542df833089c7b08b64c4fc32`
- Branch: `main`
- Remote: `https://github.com/AlecKriebel/Math.git`

## Planned experiments

| ID | Purpose | Exactness | Seed | Status |
|---|---|---|---|---|
| E1 | Re-run the published \(d=4\) exact verifier suite. | Exact symbolic | N/A | PASSED |
| E2 | Independently verify the abstract two-projection normal form. | Exact symbolic + proof | N/A | PASSED |
| E3 | Enumerate admissible Hecke simples, branching, and central multiplicities through high levels. | Exact integer/rational | N/A | PASSED |
| E4 | Unrestricted and structured \(d=6\) Grassmann and shifted-\(K\) searches. | Numerical discovery only, plus exact finite subfamilies | `results/d6_seed_manifest.json` | COMPLETED: no candidate |
| E5 | Independent exact verification of any \(d=6\) candidate. | Exact algebraic | N/A | CONDITIONAL |
| E6 | Exhaust the cyclic Gaussian functional ansatz at \(d=6\). | Exact cyclotomic | N/A | PASSED: zero candidates |
| E7 | Controlled-reflection/face-model search, calibrated at \(d=4\) and then tested at \(d=6\). | Numerical discovery only; superseded by E9 | Predeclared in `results/d6_face_seed_manifest.json` | STOPPED: exact no-go superseded remaining seeds |
| E8 | Equal-sector and crossed operator-valued color/face models. | Exact reduction and \(d=4\) family; numerical \(d=6\) search | Recorded in raw JSONL logs | COMPLETED: no \(d=6\) candidate |
| E9 | Exclude every rank-one Bloch-controlled reflection at \(d=6\). | Human proof + exact symbolic orientation verifier | N/A | PASSED |
| E10 | Derive and audit the invariant one-leg-commutant divisibility theorem. | Human proof + exact orientation/sector verifier | N/A | PASSED |
| E11 | Exhaust the cyclic three-color low-Schmidt family and pure-product boundary. | Human proof + exact symbolic verifier | N/A | PASSED: zero \(d=6\) candidates |
| E12 | Reconstruct the Evans--Pugh \(D^{(6)}\) connection from published cell data and test ordinary completions. | Two independent exact algebraic implementations | N/A | PASSED: generalized path operator only |
| E13 | Search and then exactly classify the diagonal-regular group-relative branch at \(d=6\). | Numerical discovery plus two exact no-go routes | Predeclared in `results/d6_group_relative_seed_manifest.json` | PASSED: exact no-go |
| E14 | Derive canonical-channel constraints and test their \(d=6\) arithmetic strength. | Exact matrix, channel, and Weyl arithmetic | N/A | PASSED: exact countermodel to channel-only obstruction |

## E1 — published \(d=4\) exact verifier suite

- Start: 2026-07-28 21:36 PDT
- End: 2026-07-28 21:37 PDT
- Command:
  `YBE_SYMPY_PYTHON=/Users/alec/Documents/Math/.venv/bin/python ./run_all.sh`
- Working directory:
  `/Users/alec/Documents/Math-kissing5/exceptional_ybe_d4`
- Seed: N/A
- Result: all three exact verification routes passed.
- Raw transcript:
  `results/e1_d4_reproduction.txt`
- Interpretation: independently reproduces the final \(d=4\) witness,
  partial traces, exact Yang--Baxter and Hecke identities, and the sitewise
  \((3,2)\)-generalized factorization.  It does not reproduce the historical
  discovery search and does not imply the same structure for arbitrary
  solutions.

## E2 — abstract two-projection and Clifford blocks

- Run: 2026-07-28 21:43 PDT
- Command:
  `/Users/alec/Documents/Math/.venv/bin/python scripts/verify_two_projection_blocks.py`
- Seed: N/A
- Result: exact block, trace, and Clifford checks passed.
- Raw output:
  `results/two_projection_blocks_exact_20260728.txt`
- Independent implementation:
  `verifiers/verify_two_projection_blocks.py`
- Interpretation: verifies the finite block arithmetic supporting the
  human proof.  The theorem itself follows algebraically and is not based
  on enumeration.
- Environment note: an initial replay with the system `python3` failed
  before execution because SymPy was unavailable.  The recorded project
  environment was then used successfully; this was a dependency issue, not
  a failed mathematical check.

## E3 — complete Hecke-tower multiplicity arithmetic

- Run: 2026-07-28 21:44 PDT
- Commands:
  - `python3 scripts/hecke_multiplicity_spectrum.py --max-strand 18 --test-d-through 40`
  - `python3 scripts/hecke_fusion_graph_crosscheck.py --max-strand 60 --test-d-through 100`
  - `python3 verifiers/verify_fusion_arithmetic_independent.py`
- Seed: N/A
- Exact arithmetic: Python integers and `fractions.Fraction`.
- Raw output:
  `results/hecke_multiplicity_low_strands.txt`
- Result: all implementations passed.  The simple multiplicity formula is
  \(m_{\lambda,n}=D_\lambda(d/2)^n\); integrality at every level is
  equivalent to even \(d\).
- Interpretation: this closes the proposed central-idempotent arithmetic
  route.  It does not construct a local \(R\)-matrix for any new dimension.

## E6 — cyclic Gaussian functional ansatz

- Run: 2026-07-28 22:04 PDT
- Command:
  `/Users/alec/Documents/Math/.venv/bin/python scripts/search_gaussian_functional_d6.py`
- Seed: N/A
- Exact search space: all 20 trace-zero Hermitian involutions \(H=f(U)\)
  for the order-six Gaussian generator.
- Arithmetic: exact coefficients in \(\mathbb Q(i\sqrt3)\), reduced in the
  36-dimensional twisted group algebra.
- Result: no survivors.
- Raw output:
  `results/gaussian_functional_d6_exact.txt`
- Interpretation: exact no-go for this finite ansatz only.

## E4 — adversarial dimension-six falsifier

- Runs: 2026-07-28
- Search spaces:
  - the full real and complex Grassmannians of signature-\((18,18)\)
    involutions in \(M_{36}\);
  - five independently defined symmetry families;
  - a reduced heterogeneous signature-\((6,6)\) search in \(M_{12}\);
  - a finite majority/transposition ansatz.
- Seeds and commands:
  `results/d6_seed_manifest.json` and
  `notes/track_d6_falsifier.md`.
- Raw output:
  `results/d6_riemannian_runs.jsonl`,
  `results/d6_shifted_runs.jsonl`, and
  `results/d6_majority_transposition_exact.json`.
- Calibration:
  the full \(d=4\) search reached residual \(8.73\times10^{-11}\), and
  direct insertion of the published active \(K_8\) gave residual
  \(6.89\times10^{-16}\).
- Result:
  no \(d=6\) run approached zero.  The finite
  majority/transposition search exhausted 291,840 signed candidates and
  found zero exact solutions.
- Interpretation:
  the finite ansatz exclusion is exact at its stated scope.  All other
  failures are only numerical landscape information and do not support a
  global nonexistence claim.
- Independent audit:
  `notes/checkpoint2_independent_audit.md` replayed every exact certificate,
  both analytic gradients, the calibrations, and the raw summaries.

## E8 — operator-valued color/face models

- Runs: 2026-07-28
- Exact component:
  reduced three-site equations were derived for equal-sector mixed colors
  and crossed local factors.  The symbolic verifier proves an exact
  one-parameter \(d=4\) family.
- Numerical component:
  39 complex \(d=6\) runs across the two ansätze; all seeds, options,
  versions, and outputs are retained in `results/color_face_*.jsonl`.
- Calibration:
  both implementations recovered \(d=4\) points below residual
  \(1.1\times10^{-10}\).
- Result:
  the best \(d=6\) residual was \(4.958747221723511\); no candidate was
  found.
- Scope:
  neither continuous ansatz was exhausted.  The numerical failures are not
  nonexistence evidence, even within the ansätze.
- Details:
  `notes/track_color_face_search.md` and
  `results/color_face_hashes.txt`.

## E7/E9 — rank-one Bloch-controlled face model

- Runs: 2026-07-28
- Numerical ansatz:
  \(V=\mathbb C^2\otimes\mathbb C^m\) and
  \(H=\sum_j((n_j\cdot\sigma)\otimes I_m)\otimes
  |\psi_j\rangle\langle\psi_j|\).
- Calibration:
  \(d=4\) seed `26073101` reached residual
  \(7.476389109123043\times10^{-10}\).
- \(d=6\) numerical component:
  four complete predeclared seeds gave residuals between
  \(11.872182248785922\) and \(13.654978496715914\). A fifth run was
  interrupted before completion.
- Exact result:
  E9 proves that this entire ansatz contains no \(d=6\) solution. The
  remaining predeclared numerical seeds were therefore not run.
- Proof mechanism:
  compression of the cubic relation gives exact scalar and Pauli-vector
  equations. The vector equation forces the Bloch vectors to span
  \(\mathbb R^3\); the scalar equation then forces a maximally entangled
  control basis and pairwise Bloch inner products \(-1/3\). Six such
  vectors have an indefinite Gram matrix.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_face_rank_one_control_no_go.py`.
- Details:
  `notes/face_rank_one_control_no_go_d6.md`,
  `results/face_rank_one_control_no_go_exact.txt`, and
  `results/d6_face_search_summary.md`.

## E10 — invariant controlled-leg divisibility

- Run: 2026-07-28
- Exact theorem:
  if a rank-\(r\) projection belongs to either one-leg commutant, then
  restricting the three-site pair to that spectator sector gives
  common-one and common-zero multiplicities \(rd^2/8\). Thus
  \(8\mid rd^2\).
- Consequence:
  for \(d\equiv2\pmod4\), every such projection has even rank; a
  rank-one-controlled solution or a leg-commutant MASA is impossible.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_controlled_leg_divisibility.py`.
- Raw output:
  `results/controlled_leg_divisibility_exact.txt`.
- Scope:
  this does not exclude a solution whose two one-leg commutants have only
  even-rank projections, including the scalar-commutant case.

## E11 — cyclic low-Schmidt color family

- Run: 2026-07-28
- Search space:
  the complete three-color cyclic Fourier mixed family and its
  pure-product boundary defined in
  `notes/track_color_low_schmidt_exact.md`.
- Result:
  no \(d=6\) solution; the two-color specialization retains the exact
  \(d=4\) family.
- Proof mechanism:
  one-qubit and first/third-qubit contractions, a nonvanishing Fourier
  lemma, an anticommuting-branch reduction, and a terminal negative-square
  contradiction.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_color_low_schmidt_no_go.py`.
- Raw output:
  `results/color_low_schmidt_exact_no_go.txt`.

## E12 — \(D^{(6)}\) Ocneanu-cell audit

- Run: 2026-07-28
- Inputs:
  the specialized \(D^{(6)}\) Ocneanu cells and Perron--Frobenius data
  recorded from Evans--Pugh.
- Independent exact implementations:
  `scripts/audit_evans_pugh_d6_connection.py` and
  `verifiers/verify_evans_pugh_d6_from_cells.py`.
- Result:
  the reconstructed operator is unitary and satisfies the Hecke, projection
  cubic, and braid identities on the 20-dimensional composable two-edge
  path space; the corresponding three-path space has dimension 48.
- Ordinary-locality audit:
  the graph has six vertices but ten directed edges with multiplicity.
  Its connection space is not \(\mathbb C^6\otimes\mathbb C^6\).
  Zero extension to the 100-dimensional edge square is singular, and both
  scalar Hecke completions fail the braid relation exactly.
- Raw outputs:
  `results/evans_pugh_d6_connection_audit.txt` and
  `results/evans_pugh_d6_from_cells_verifier.txt`.
- Scope:
  this does not exclude a new nontrivial vertex--face intertwiner or
  all-strand conversion.

## E13 — diagonal-regular group-relative branch

- Runs: 2026-07-28
- Numerical search:
  arbitrary trace-zero Hermitian involutions \(h\) for \(C_6\), \(S_3\),
  and \(V_4\), with commands and seeds in
  `results/d6_group_relative_seed_manifest.json`.
- Calibration:
  three \(V_4\) seeds converged below \(1.1\times10^{-10}\) and were
  exactified as \(h=iC/\sqrt3\) for an integer skew-conference matrix
  \(C^2=-3I\).
- Exact result:
  E10 excludes the full arbitrary-\(h\) branch for every
  \(d\equiv2\pmod4\). A logically independent dual-Fourier support
  exhaustion also excludes all \(C_6\) choices.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_group_relative_exact.py`.
- Raw output:
  `results/group_relative_exact.txt`.
- Interpretation:
  the failed \(d=6\) numerical runs are superseded by exact theorems and are
  not used as evidence.

## E14 — canonical channels and the exact \(d=6\) countermodel

- Runs: 2026-07-28
- Universal exact output:
  the canonical channels are positive self-adjoint bistochastic CP maps,
  their fixed algebras are the one-leg commutants, their supertraces are
  \(d^2/2\), their Schmidt supports lie at eigenvalue \(1/3\), and
  \(2\mathcal E-I\) is CP with traceless Hermitian Kraus directions.
- Exact \(d=4\) checks:
  the published witness and full color/face circle have commuting,
  isospectral channels and satisfy the observed paired polynomial.
  A rational standard non-YBE guard proves these facts do not follow from
  standardness alone.
- Exact \(d=6\) countermodel:
  a Weyl-diagonal channel has spectrum
  \(\{1,(2/3)^{16},(1/3)^{19}\}\) and satisfies all currently isolated
  channel-level and affine-CP constraints.
- New cubic point:
  identity-pairing its 19 Schmidt directions gives a Hermitian traceless
  cubic solution \(H_0\) with spectrum
  \(\{(-\sqrt3)^9,(1/\sqrt3)^{27}\}\). It fails involutivity, and its
  affine involution has trace \(18\).
- Replays:
  `verifiers/verify_channel_identities_d4.py`,
  `verifiers/verify_channel_color_family.py`, and
  `verifiers/verify_channel_d6_abstract_model.py`.
- Interpretation:
  channel spectra and positivity cannot prove divisibility by four without
  using the shared involutive three-site realization.

## E15 — Weyl cubic deformations and full-color equivariance

- Runs: 2026-07-28
- Exact cubic point:
  \[
  H_0=\frac{YY\otimes I_9+(XX+ZZ)\otimes F_3}{\sqrt3}
  \]
  satisfies the full cubic relation and has minimal polynomial
  \(3x^2+2\sqrt3x-3\), hence is not an involution.
- Exact equivariant theorem:
  every diagonally \(U(m)\)-equivariant exceptional candidate on
  \(\mathbb C^2\otimes\mathbb C^m\) is excluded when \(m\) is odd.
  The final \(m=3\) signatures reduce to a rank-one two-qubit projection;
  tensor overlap gives determinant at most \(1/16\), whereas the cubic
  requires at least \(1/9\).
- Exact pairing theorem:
  all signed, permutation, and orthogonal pairings that preserve the two
  nine-dimensional Weyl blocks, including a whole-block interchange, fail
  involutivity.
- Numerical deformation:
  the cubic tangent Jacobian at \(H_0\) has numerical rank \(90\) and
  nullity \(81\), matching a realified \(\mathfrak u(9)\) space. Seeded
  optimization found no simultaneous cubic/involution point. These tangent
  and optimization statements remain numerical only.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_weyl_h0_and_swap_block_no_go.py`.
- Raw exact output:
  `results/weyl_h0_swap_block_exact.txt`.

## E16 — complete endpoint-commutant arithmetic audit

- Run: 2026-07-28
- Exact all-level result:
  for \(d=2s\), minimal left/right leg atoms of ranks \(2a_\alpha\) and
  \(2b_\beta\) admit the nonnegative integral endpoint multiplicities
  \[
  k_{\alpha\beta,\lambda,n}
  =a_\alpha b_\beta D_\lambda s^{n-2}.
  \]
  They satisfy every row, column, total-dimension, and branching equation.
- \(d=6\) exhaustion:
  precisely five represented \(C^*\)-algebra types have only even-rank
  minimal projections; all \(25\) ordered left/right pairs pass.
- Assumption guards:
  exact standard \(d=6\) reflections were built with scalar and
  \(M_3\otimes I_2\) leg commutants. Exact nonzero cubic entries confirm
  that neither guard is a Yang--Baxter witness.
- Operator-algebra audit:
  Conti--Lechner ergodicity is strictly stronger than having scalar
  algebraic one-leg fixed points. The exceptional partial trace violates
  their necessary ergodicity norm condition for every \(d>2\), but their
  examples show that this does not force a finite-level fixed projection.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_leg_commutant_obstruction_audit.py`.
- Raw output:
  `results/leg_commutant_obstruction_audit_exact.txt`.

## E17 — canonical intersection projections on four sites

- Run: 2026-07-28
- Universal theorem:
  for the common-one projections \(E=e_{123}\) and \(F=e_{234}\),
  \[
  E P_{34}E=\frac12E,\qquad EFE=\frac14E,\qquad FEF=\frac14F.
  \]
  Common-zero projections satisfy the complementary formulas, and shifted
  opposite signs are orthogonal.
- Exact marginals:
  \(\operatorname{Tr}_3e=dP_{12}/4\), the reversed formula holds on the
  other endpoint, and every one-site marginal of \(e\) is \(d^2I/8\).
  The uncontracted middle marginal remains generally nonscalar.
- Arithmetic:
  \(E,F\) have \(d^4/8\) generic angle-\(1/4\) blocks and a
  \(3d^4/4\)-dimensional common kernel. At \(d=6\), the counts are \(162\)
  and \(972\), so no new factor of two appears.
- Hostile audit:
  the canonical partial isometry has no intrinsic determinant or QCA index;
  its full-space direct rotation has order three and determinant one on
  every block. No Frobenius--Schur parity follows.
- Limitation countermodel:
  an exact GHZ-qubit construction stabilized by \(\mathbb C^3\) satisfies
  the complete derived marginal and four-site angle package at \(d=6\)
  while failing the original cubic/full-intersection condition.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_intersection_projection_structure.py`.
- Raw output:
  `results/intersection_projection_structure_exact.txt`.

## E18 — tensor-product spectrum audit

- Run: 2026-07-29
- Source:
  the tensor-product definition immediately before Lechner,
  Proposition 3.6, checked by extraction and visual rendering of pages
  15--16.
- Exact result:
  the only unitary scalar \(\mu\) satisfying
  \[
  \mu\{-1,e^{i\pi/3}\}
  =\{-1,e^{i\pi/3}\}
  \]
  is \(\mu=1\). Hence a tensor-product factor preserving the exceptional
  class must be an identity matrix.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_tensor_product_extension_no_go.py`.
- Interpretation:
  the standard operation gives exactly identity stabilization and cannot
  turn the \(d=4\) witness into a \(d=6\) witness.

## E19 — factor-leg no-go and full rank-two bookkeeping

- Run: 2026-07-29
- Exact theorem:
  for \(d=2m\) with \(m\) odd, a unital
  \(M_m(\mathbb C)\otimes I_2\) factor in either one-leg commutant is
  impossible. Commutant reduction and standardness leave three Pauli
  coefficients; involutivity makes them commute, producing rank-one
  projections in the opposite leg commutant and contradicting
  \(8\mid d^2\).
- Exact assumption audit at \(d=6\):
  the three-rank-two-atom branch admits 217 labelled cell-rank tables and
  1540 labelled endpoint common-rank tables. Uniform ranks are therefore
  not automatic. Exact cellwise-standard and abstract angle-\(1/3\) guards
  exercise the nonuniform cases.
- Exact shared-atom theorem:
  the left and right three-atom color algebras cannot share even one
  rank-two atom. A shared cell reduces to the base-\(2\) problem, becomes
  scalar, propagates across its row, and contradicts the scalar partial
  trace. Thus any surviving \(\mathbb C^3/\mathbb C^3\) branch has
  genuinely transverse relative position in \(U(6)\).
- Numerical falsifier:
  a new all-rank-two-cell search allows the relative color decompositions
  to vary over all of \(U(6)\), rather than only \(U(3)\otimes I_2\).
  Four declared seeds had best residual \(6.010858542676606\). This is
  negative evidence only and does not cover nonuniform cell ranks.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_factor_m3_opposite_control_no_go.py`.
- Raw exact output:
  `results/factor_m3_opposite_control_no_go_exact.txt`.

## E20 — all nine three-color cell-rank orbits

- Run: 2026-07-29
- Scope:
  the \(d=6\) branch in which both one-leg commutants contain three
  rank-two central atoms.  The relative color position varies over all of
  \(U(6)\), every four-dimensional cell is an arbitrary reflection of its
  prescribed signature, and the nine canonical rank tables cover all
  \(217\) labelled possibilities modulo the proved discrete symmetries.
- Predeclaration:
  `results/d6_threecolor_rankpattern_seed_manifest.json` fixes one seed
  and 800 iterations for each of the nine rank-pattern orbits.
- Gradient guard:
  the combined cell-block/\(U(6)\) descent direction agrees with an
  independently assembled central difference to relative error
  \(7.013199327717132\times10^{-9}\).
- Numerical outcome:
  no run found a candidate.  The final cubic residuals ranged from
  \(6.000000000000004\) to \(16.552374914369093\).
- Interpretation:
  NUMERICAL_EVIDENCE only.  One seed per orbit is not exhaustive and
  proves no nonexistence statement, even inside this branch.
- Replay:
  `scripts/d6_threecolor_rankpattern_search.py` and
  `scripts/check_d6_threecolor_rankpattern_gradient.py`.
- Raw output:
  `results/d6_threecolor_rankpattern_runs.jsonl`,
  `results/d6_threecolor_rankpattern_summary.txt`, and
  `results/d6_threecolor_rankpattern_gradient_check.txt`.

## E21 — common-leg and two-block audit at \(d=6\)

- Run: 2026-07-29
- Universal exact theorem:
  every hypothetical \(d=6\) exceptional projection satisfies
  \[
  \mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb C I_6.
  \]
  A common rank-two subspace gives a base-\(2\) cubic cell; all non-scalar
  ranks are excluded, scalar propagation then contradicts the vanishing
  partial trace.  C17 turns every nontrivial common projection into a
  rank-two one by complementation.
- Consequences:
  aligned and tensor-flip-symmetric realizations of
  \(\mathbb C I_4\oplus\mathbb C I_2\) and
  \((M_2\otimes I_2)\oplus\mathbb C I_2\) are impossible.
- Hostile audit:
  exact permutation conjugates put every ordered pair of those algebra
  types in scalar relative intersection, and exact abstract
  \(216\)-dimensional cubic blocks realize all endpoint multiplicities.
  Thus neither algebra type is excluded in arbitrary transverse position.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_d6_two_block_leg_types.py`.
- Raw output:
  `results/d6_two_block_leg_types_exact.txt`.

## E22 — common-reduction descent in every unresolved dimension

- Run: 2026-07-29
- Universal exact theorem:
  if \(z\) is a nonzero proper projection common to both one-leg
  commutants, the diagonal cells on \(zV\otimes zV\) and
  \(z^\perp V\otimes z^\perp V\) are non-scalar cubic involutions.
  Their normalized negative ranks are either both \(1/2\), or both
  \(1/3\) with equal cell dimensions, or both \(2/3\) with equal cell
  dimensions.
- Unresolved congruence:
  for \(d\equiv2\pmod4\), C17 excludes both unbalanced equal-dimension
  branches.  The common reduction therefore yields two smaller balanced
  exceptional solutions, one again in a \(2\bmod4\) dimension.
- Consequences:
  every least-dimensional \(2\bmod4\) solution is common-leg-irreducible;
  the \(d=6\) scalar-intersection theorem is recovered; a common reduction
  at \(d=10\) would imply a \(d=6\) solution.
- Exact guard:
  a dimension-three Gaussian projection and its complement verify that
  the \(1/3\) and \(2/3\) diagonal alternatives are genuine and must not
  be silently discarded.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_common_reduction_general.py`.
- Raw output:
  `results/common_reduction_general_exact.txt`.

## E23 — permutation and partial-transpose contraction exhaustion

- Run: 2026-07-29
- Universal exact audit:
  four of the six \(S_3\) scalar closures of the three-site cubic are
  tautologies, while the remaining two are scalar functionals of the
  already-known outer channel contractions.
- New operator identity:
  the middle contraction
  \[
  M=\operatorname{Tr}_2(P_{12}P_{23}P_{12})
   =\operatorname{Tr}_2(P_{23}P_{12}P_{23})
  \]
  obeys \(dI/6\le M\le dI/2\), has trace \(d^3/4\), and has both
  one-site marginals \(d^2I/4\).
- Exact limitation:
  \(M=(3/2)I_{36}\) satisfies all of these data at \(d=6\). Moreover,
  \(H=(Z\otimes I_3)\otimes(X\otimes I_3)\) is a standard rank-half
  involution for which every one of the 48 partially-transposed
  permutation pairings vanishes exactly, although the cubic residual has
  squared Hilbert--Schmidt norm \(192\).
- Interpretation:
  permutation/Brauer scalar shadows are exhausted and cannot prove
  \(4\mid d\); a successful obstruction must retain operator-valued
  overlap information.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_permutation_contraction_audit.py`.
- Raw output:
  `results/permutation_contraction_audit_exact.txt`.

## E24 — full retained Weyl coefficient search at \(d=6\)

- Run: 2026-07-29
- Scope:
  all \(361\) real coefficients in
  \[
  H(C)=\sum_{i,j=1}^{19}C_{ij}A_i\otimes A_j
  \]
  for the retained traceless-Hermitian qubit--qutrit Weyl frame. Unlike
  the earlier deformation, no Schmidt values, frames, rank, block
  support, or finite symmetry were fixed.
- Predeclaration:
  forty random, direct-joint, continuation, bidirectional, and
  mixed-strata runs were fixed in
  `results/d6_weyl_full_coeff_seed_manifest.json`.
- Gradient guard:
  the analytic gradient agrees with centered finite differences with
  maximum relative error \(1.38\times10^{-9}\).
- Numerical outcome:
  no candidate was found. The best final residual pair was
  \((3.5886268615,0.9034063467)\) for involutivity and the cubic.
  Twenty-nine endpoints normalize to adjacent-anticommuting involutions;
  eleven normalize to the Weyl cubic with its known wrong quadratic.
- Exact branch theorem:
  \(K^2=I\) and
  \(\{K_{12},K_{23}\}=0\) imply
  \[
  K_{12}K_{23}K_{12}-K_{23}K_{12}K_{23}=K_{12}-K_{23},
  \]
  so this branch has coefficient \(1\), not \(1/3\).
- Interpretation:
  numerical evidence only for the \(361\)-parameter search; the
  anticommuting-branch identity is exact. This proves neither
  nonexistence inside the frame nor global \(d=6\) nonexistence.
- Artifacts:
  `notes/d6_weyl_full_coefficient_search.md`,
  `results/d6_weyl_full_coeff_runs.jsonl`,
  `results/d6_weyl_full_coeff_analysis.json`, and
  `results/weyl_anticommuting_branch_exact.txt`.
