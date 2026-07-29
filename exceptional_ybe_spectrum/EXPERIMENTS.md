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

## E25 — fusion anomaly and projective-\(A_4\) parity audit

- Run: 2026-07-29
- Exact fusion result:
  the neutral \(SU(3)_3\) component is \(R(A_4)\), while the degree-one
  component has the nontrivial projective \(A_4\) module rules.
- Exact algebra:
  the corresponding twisted algebra is
  \[
  \mathbb C^\alpha[A_4]\cong M_2(\mathbb C)^{\oplus3},
  \]
  verified through the binary tetrahedral quotient by a direct
  \(12\times12\) map of determinant \(6^6\).
- Conditional parity:
  a unital action on a space of dimension \(s=d/2\) would force \(s\)
  even. The natural projective action instead exists on
  \(\mathbb C^2\otimes\mathbb C^s\) for every \(s\), so it recovers only
  evenness of \(d\).
- Exact assumption guards:
  the generator is non-self-dual; determinant blocks have rank \(s^3\)
  and scalar braid action; tensor reversal maps \(P\) to \(FPF\). For the
  published \(d=4\) witness,
  \(\|P-FPF\|_2^2=8\) and the three-site determinant projection has
  reversal-defect norm squared \(14\).
- Interpretation:
  a new projective-descent theorem to an invariant \(s\)-dimensional
  multiplicity space would prove \(4\mid d\), but it is not supplied by
  the fusion tower, grading, FS data, determinant channels, or reversal.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_fusion_anomaly_parity.py`.
- Raw output:
  `results/fusion_anomaly_parity_exact.txt`.

## E26 — four-strand obstruction to square restrictions

- Run: 2026-07-29
- Exact algebra:
  constructed the \(24\)-element permutation basis of \(H_4(q)\) and
  checked the \(q\)-symmetrizer \(e_+\) and \(q\)-antisymmetrizer
  \(e_-\), including their idempotence and generator eigenrelations.
- Exact Markov traces:
  \[
  \begin{array}{c|cc}
  \eta&\mu_\eta(e_+)&\mu_\eta(e_-)\\ \hline
  0&1&0\\
  1/3&1/9&0\\
  1/2&0&0\\
  2/3&0&1/9\\
  1&0&1
  \end{array}
  \]
- Theorem:
  if \(R(W^{\otimes2})\subseteq W^{\otimes2}\), the restricted tower
  inherits the ambient annihilation of both idempotents. Their
  arbitrary-\(\eta\) trace polynomials have the unique common zero
  \(\eta_W=1/2\), without needing the discrete positive-trace
  classification; therefore \(\dim W\) is even.
- Consequences:
  a least-dimensional \(d\equiv2\pmod4\) witness must be
  non-restrictable, and no restrictable \(d=6\) witness exists.
- Assumption guard:
  the proof never assumes separate preservation of the mixed cells
  \(A\otimes B\) and \(B\otimes A\). The replay also derives all nine
  operator-valued mixed-color braid equations with unrestricted mixing.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_restrictable_four_strand_obstruction.py`.
- Raw output:
  `results/restrictable_four_strand_exact.txt`.

## E27 — determinant boundary-corner factorization

- Run: 2026-07-29
- Exact all-boundary theorem:
  for either three-site common-one/common-zero determinant projection
  \(a\),
  \[
  (a\otimes I)\mathcal A_{m+3}(a\otimes I)
  =a\otimes\mathcal A_m
  \qquad(m\ge0).
  \]
  The proof uses the invertible fusion endpoints and equality of exact
  path-corner dimensions with the injective disjoint \(\mathcal A_m\)
  copy.
- Consequence:
  every boundary word closed back onto the determinant block is the
  identity on its rank-\(s^3\) multiplicity. Endpoint traces and matrix
  coefficients therefore yield only scalars there.
- Exact low-level replay:
  four-site scalar compression, the five-site identity
  \(e h_3h_4h_3e=-e h_4/3\), and the six-site \(M_2\) Clifford block.
  The latter acts on the added three-site path factor with multiplicity
  \(3s^6\), not on the determinant multiplicity.
- Limitation model:
  an exact \(d=6\) abstract four-strand representation satisfies all
  cubic, far-commutation, rank, shifted-angle, boundary-compression, and
  opposite-sign identities used in this route.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_determinant_boundary_corner_factorization.py`.
- Raw output:
  `results/determinant_boundary_corner_exact.txt`.

### E25--E27 exact-run provenance

- Parent commit:
  `03fe7083c280aef5e202f31ad1c326b5bca70540`.
- Machine:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`.
- Runtime:
  Python `3.9.6`, SymPy `1.14.0`.
- Randomness:
  none; all three replays are deterministic exact calculations.
- SHA-256:
  - `notes/fusion_anomaly_parity_audit.md`:
    `979cd06d20f0cb4c260979b5e3dd3948c672de403b43bfc5f83d0e78a35e4ab8`;
  - `verifiers/verify_fusion_anomaly_parity.py`:
    `1deb45cbd0c6c5a182f88ac642483d0a4ca3f7318732de0b216507134c9677c0`;
  - `results/fusion_anomaly_parity_exact.txt`:
    `dbf2365c9be68dc7ef63ac3193f5af4a20e09eaeac3002ab053bffd54e6b4209`;
  - `notes/restrictable_four_strand_obstruction.md`:
    `8280ad7b68ef98832466c12bad25d9fb7186f82309d0d3d6c1bfee67079f6285`;
  - `verifiers/verify_restrictable_four_strand_obstruction.py`:
    `7e51b5bcc4e5e337e8358a6af6bbf0c29fc1f8ab691c5681311af447ad9677d7`;
  - `results/restrictable_four_strand_exact.txt`:
    `34f37e4180707d74e51d0dcd9e69402ba2a0963bf6d111407fddcd3ebe88effc`;
  - `notes/determinant_boundary_corner_factorization.md`:
    `cdc874fd274a8c7b90c07d95032924b1f7549556f694c8bcf7e7b5c716c0fd0a`;
  - `verifiers/verify_determinant_boundary_corner_factorization.py`:
    `071929457023770685052304636300cbb32b0862f3715bbc9a61de4c2f8c8cc7`;
  - `results/determinant_boundary_corner_exact.txt`:
    `d578c3722253638a291ddb55c0553469b058b8566ad654a79e2c7958ba5dabad`.

## E28 — one-sided square-invariance reduction

- Run: 2026-07-29.
- Exact reduction:
  for \(U=W^\perp\), complementary square invariance is equivalent to
  \[
  \delta=\frac{(\dim U)^2}{2}-\operatorname{Tr}(K^2)=0,
  \qquad K=P_{U\otimes U}PP_{U\otimes U}.
  \]
  Projection block multiplication also gives
  \[
  \delta
  =\|P_{\rm mixed}PP_{U\otimes U}\|_{\rm HS}^2
  =\frac12\|[P,P_{U\otimes U}]\|_{\rm HS}^2.
  \]
- Exact limitation model:
  a rank-18 projection in \(d=6\) has both partial traces \(3I_6\), an
  exact published exceptional \(d=4\) restriction, and
  \(\delta=1/2\), but fails the ambient cubic at the exact matrix
  coefficient \(-\sqrt2/48\).
- Interpretation:
  every two-site positivity and marginal argument is insufficient;
  proving \(\delta=0\) must use the mixed-sector ambient cubic.
- Independent numerical falsifier:
  nine seeded searches over the complete 20-dimensional orthogonal
  complement of a fixed \(d=4\) square found no witness.  The smallest
  cubic Frobenius residual was \(6.0108585346\ldots\).  This is negative
  numerical evidence only.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_one_sided_square_invariance.py`.
- Artifacts:
  `notes/one_sided_square_invariance_audit.md`,
  `results/one_sided_square_invariance_exact.txt`,
  `results/d6_one_sided_4plus2_gradient_check.txt`,
  `results/d6_one_sided_4plus2_runs.jsonl`, and
  `results/d6_one_sided_4plus2_pt10_runs.jsonl`.

## E29 — codimension-two cuts of the identity amplification

- Run: 2026-07-29.
- Predeclared Grassmann calibration:
  four rank-four runs, seeds \(26072980,\ldots,26072983\), reached
  normalized squared commutators between
  \(6.70\cdot10^{-23}\) and \(1.47\cdot10^{-22}\).  The analytic
  gradient check had relative error \(5.04\cdot10^{-11}\).
- Predeclared production:
  all 32 rank-six runs, seeds \(26072984,\ldots,26073015\), ended within
  \(9.58\cdot10^{-15}\) of
  \[
  \frac{23}{96}=0.239583333333\ldots.
  \]
  No candidate approached zero.  Apparent optimality and the rational
  value are not claimed.
- Exact theorem discovered from the endpoint:
  for every \(m\ge2\),
  \[
  [H^{(4)}\boxtimes I_m,Q\otimes Q]=0
  \quad\Longrightarrow\quad
  \operatorname{rank}Q\ne4m-2.
  \]
  The proof uses a three-coefficient Schmidt form, the exact six-line
  rank-at-most-two Bell-pencil cone, and generation of
  \(M_4(\mathbb C)\) on the active pair.
- Independent audit:
  the second verifier recovers the Schmidt coefficients by partial
  contraction and obtains active-commutant equation rank \(15\), rather
  than reusing the primary word-closure implementation.
- Replays:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_no_rank_six_subspace_of_d8.py` and
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_no_rank_six_subspace_of_d8_independent.py`.
- Raw numerical output:
  `results/d6_subspace_of_d8_calibration.jsonl` and
  `results/d6_subspace_of_d8_production.jsonl`.
- Seed manifest and aggregate:
  `results/d6_subspace_of_d8_seed_manifest.json` and
  `results/d6_subspace_of_d8_search_summary.json`.

### E28--E29 provenance

- Parent commit:
  `41b74cab`.
- Machine:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`.
- Runtime:
  Python `3.9.6`, NumPy `2.0.2`, SciPy `1.13.1`, SymPy `1.14.0`.
- New-search source SHA-256:
  `1eb40dc66b34e2f5b5d88a325f23f97b0147aa7fd70e85d022a21b25b2da6db0`.
- Exact artifact SHA-256:
  - `notes/one_sided_square_invariance_audit.md`:
    `ca2c18296c46d4a997edd9892f2a3ffdae505571270e671b78294d8a21418327`;
  - `verifiers/verify_one_sided_square_invariance.py`:
    `2bf2b4cf68755d81a03542a4e9efedf418b6c74fdfea9f6333452d2f13620a7c`;
  - `results/one_sided_square_invariance_exact.txt`:
    `1e48b4fbb264815fcaec8dd8cf5976f4ed5280eefb6b82c67f55c8a097823539`;
  - `notes/no_rank_six_subspace_of_d8_amplification.md`:
    `e8d45ae5ecc26556bda479b6adb606822c839a150ace4c1728ba3a0c5985e178`;
  - `notes/no_rank_six_subspace_of_d8_amplification_audit.md`:
    `ab8d8874e6edf80aa5dccf04e156d478bbd67d0ed66ae5169dcbb6476dd3e0d9`;
  - `verifiers/verify_no_rank_six_subspace_of_d8.py`:
    `cfbac4d195f6ef58555e5d0b56120fea2797919d1624a61054686b02028d2145`;
  - `results/no_rank_six_subspace_of_d8_exact.txt`:
    `cdf09475855627e1a054701478ae51579c0467be78ea964097e29be87d3a4ee5`;
  - `verifiers/verify_no_rank_six_subspace_of_d8_independent.py`:
    `db35ceca9f6363e6894baaf8cf33e0f7941032396fa76d59f227a7a79ce24f29`;
  - `results/no_rank_six_subspace_of_d8_independent_exact.txt`:
    `65d2eaecd100351de8462cffcf87016d65fe2f71fd7a7864fc1db15cdfe4e33e`.

## E30 — full-cubic one-sided color compression

- Run: 2026-07-29 03:06 PDT.
- Exact universal identities:
  with \(A=P_{12}\), \(B=P_{23}\),
  \(G_L=e_1e_2f_3\), and \(G_R=f_1e_2e_3\),
  \[
  \|G_LBA\|_{\rm HS}^2
  =\|G_RAB\|_{\rm HS}^2
  =\frac{r^2u}{4}.
  \]
  The complete \(G_L\)-corner is
  \[
  sTs-TsT-L^*A_\perp L=\frac13(s-T),
  \qquad T^2+L^*L=T,
  \]
  so it controls an \(A_\perp\)-weighted leakage rather than the
  zero-variance target \(L^*L=0\).
- Exact limitation model:
  a \(216\)-dimensional abstract \(H_3\) representation has the balanced
  \(d=6\) multiplicities \(27,27,81\), contains the balanced \(d=4\)
  multiplicities \(8,8,24\), and admits three commuting color projections
  with joint ranks
  \(64,32,32,32,16,16,16,8\).
  All one-color \(A/B\) traces are \(72\), and all color-level locality
  commutators vanish, while
  \[
  \frac12\|[A,F_{12}]\|_{\rm HS}^2
  =\frac12\|[B,F_{23}]\|_{\rm HS}^2
  =\frac{16}{9}.
  \]
- Scope:
  this is an abstract three-strand limitation theorem, not a local
  \(d=6\) witness.  It does not provide
  \(A=P\otimes I_6,\ B=I_6\otimes P\) for a common two-site \(P\).
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `971f58d8`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_one_sided_cubic_abstract_countermodel.py`.
- SHA-256:
  - `notes/one_sided_full_cubic_color_compression.md`:
    `0f78b8fce8183b152d1e86432fa8eb1de758ec44d223ea9c1ac8067c3b11d965`;
  - `verifiers/verify_one_sided_cubic_abstract_countermodel.py`:
    `f858cecea8a61bc88bd30b6fca38b63a9d38638ec2dd2cd5c9d3d383bfa99dbb`;
  - `results/one_sided_cubic_abstract_exact.txt`:
    `18e7daa9b14977764a367b33c39475a14d5be7e756d6ed044237bade394bf560`.

## E31 — exact balanced Manin super-Hecke audit

- Run: 2026-07-29 03:16 PDT.
- Object:
  the standard \(GL(3|3)\) Manin Hecke symmetry, multiplied by
  \(t=e^{i\pi/6}\) so that its two eigenvalues are
  \(q=t^2=e^{i\pi/3}\) and \(-1\).
- Exact direct checks:
  the \(36\times36\) matrix obeys
  \((T+I)(T-qI)=0\), and ordinary Kronecker placements obey the complete
  \(216\times216\) braid identity.  Both eigenspaces have dimension
  \(18\), and \(\operatorname{Tr}T=18(q-1)\).
- Exact unitarity audit:
  the standard-metric defect has squared Frobenius norm \(45\).
  More strongly, the human proof excludes every positive local metric
  \(G\): diagonal even/odd eigenvectors force \(G_{ia}=0\), after which
  the mixed \(q\)- and \((-1)\)-eigenvectors have inner product
  \((\bar t-t)G_{ii}G_{aa}=-iG_{ii}G_{aa}\ne0\).
- Scope:
  this is a proved no-go only for the standard one-parameter Manin family
  and its local-basis conjugates, not for arbitrary \(d=6\) solutions or
  multiparameter super-Hecke symmetries.
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `eac05ca0`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_manin_super_hecke_d6.py`.
- SHA-256:
  - `notes/manin_super_hecke_unitarity_no_go.md`:
    `4b7f90210f1e5bcfc680dea8182dc7af5a96b3596fa6c00c9d75ccaa7f68def4`;
  - `verifiers/verify_manin_super_hecke_d6.py`:
    `c99c457a28395dc4ba58d49380a1ac740b9051f533254718b2e21e0ed3862922`;
  - `results/manin_super_hecke_d6_exact.txt`:
    `af637465e3c5f38fc09fba110ff1c392125eaccf005aac986912004e2b2b884a`.

## E32 — exact completion of the \(S_4\)-equivariant rank-six branch

- Run: 2026-07-29 03:20 PDT.
- Exact search space:
  \[
  V_2\otimes V_3\otimes V_2
  \cong 2V_3\oplus2V_{3'},
  \qquad
  \operatorname{End}_{S_4}\cong M_2(\mathbb C)\oplus M_2(\mathbb C).
  \]
  After the two central choices already checked earlier, every remaining
  trace-zero Hermitian involution is exactly a point of
  \(S^2\times S^2\).
- Certificate:
  an exact rational model of \(V_2,V_3\) constructs metric-Hermitian
  Pauli triples in both multiplicity summands. Twenty sparse cubic
  coordinates imply seven branch relations by exact Gröbner reduction.
  Three additional coordinates exclude all real branches. Independently,
  the two sphere equations and all 23 coordinates generate the unit ideal
  over \(\mathbb Q\).
- Conclusion:
  the complete \(S_4\)-equivariant heterogeneous \((2,3,2)\) rank-six
  branch is empty. This is not an unrestricted \(d=6\) theorem.
- Randomness:
  none in the final certificate. The retained derivation helpers are
  deterministic exact computations.
- Parent commit:
  `eac05ca0`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`, NumPy `2.0.2`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_s4_equivariant_noncentral_no_go.py`.
- SHA-256:
  - `notes/s4_equivariant_exact_no_go.md`:
    `a8c14f5f4e2b4f173499f01eb3007883cddf98fd2b92b67c39d535198c43424a`;
  - `verifiers/verify_s4_equivariant_noncentral_no_go.py`:
    `ad2fadf138809a126459cf64ec160f8785df5338c6eb46504b31f2d66436954e`;
  - `results/s4_equivariant_exact_no_go.txt`:
    `b835e7732e26ffffe37cfc9de2cdc577f18e606efe500521613240ac8aa12562`;
  - `scripts/derive_s4_equivariant_certificate.py`:
    `ab0bb3b00c4e30b8c4c69a8edfd2e1aa7223863e3b6394482923215780db6bae`;
  - `scripts/derive_s4_equivariant_objective.py`:
    `5f1a59ff04bbf09d9103c70e69c382c913f33b5111353bbaf45779bb7ebee71c`.

## E33 — exact completion of the binary-tetrahedral \(\mathbb{CP}^2\) branch

- Run: 2026-07-29 03:02--03:24 PDT.
- Exact search space:
  \(A=\mathbb C^2\) is the defining \(2T\)-module and
  \(B=\mathbb C^3\) its tetrahedral rotation module. Exact intertwiners for
  all 24 Hurwitz units give
  \[
  A\otimes B\otimes A
  \cong1\oplus1'\oplus1''\oplus3\oplus3\oplus3,
  \qquad
  \dim\operatorname{End}_{2T}=12.
  \]
  Balanced equivariant signatures are only \((s,r)=(3,1)\) and its
  complement \((0,2)\). Thus \(K\mapsto-K\) reduces the complete branch to
  one multiplicity line \([z]\in\mathbb{CP}^2\).
- Predeclared falsifier:
  all 64 full-complex seeds `26074001`--`26074064` were recorded before
  objective evaluation; the analytic-gradient check had relative error
  \(1.1647\cdot10^{-9}\). No candidate occurred. The smallest observed
  normalized squared residual was \(16/9\), but no global-minimum claim is
  based on this search.
- Exact certificate:
  with \(z=(a,b+ic,d+ie)\), normalization and two residual entries force
  \(a^2=1/3\) and \(bd+ce=0\). Writing the two orthogonal real vectors as
  \((b,c)=r(x,y)\) and \((d,e)=\varepsilon s(-y,x)\), a third residual
  entry satisfies
  \[
  |F_{57,20}|^2=16/729.
  \]
  Hence the complete balanced \(2T\)-equivariant branch is empty.
- Scope:
  this is an exact symmetry-scoped no-go, not an unrestricted
  \(d=6\) theorem.
- Randomness:
  only the retained numerical falsifier uses the predeclared seeds. The
  decomposition and no-go certificates are deterministic exact SymPy
  arithmetic.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`, NumPy `2.0.2`, SciPy `1.13.1`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  scripts/verify_binary_tetrahedral_cp2_ansatz.py` and
  `/Users/alec/Documents/Math/.venv/bin/python
  scripts/verify_binary_tetrahedral_cp2_no_go.py`.
- SHA-256:
  - `notes/binary_tetrahedral_cp2_no_go.md`:
    `405cbac7ec9584df48b4d52d9fb65a6393a2bdf190091a98c62e274779af9269`;
  - `scripts/verify_binary_tetrahedral_cp2_ansatz.py`:
    `5064ea7b04eb231a9cb2239cff8afd0242909e124dcdedddced596130efd0133`;
  - `scripts/verify_binary_tetrahedral_cp2_no_go.py`:
    `cc0dc8795bdac0d0843eeedde05c19e4e15b28dfa72fa8a180edf6a8d1e2090f`;
  - `scripts/d6_binary_tetrahedral_cp2_search.py`:
    `3b7e4dc657983fba1888ae9879be9820eb70056355f02d4bbfbd083110881640`;
  - `results/d6_binary_tetrahedral_cp2_runs.jsonl`:
    `32340c32e710911ee36e3747cb76d204e27b3faf889b09de74257e964eb5f8b4`;
  - `results/d6_binary_tetrahedral_cp2_seed_manifest.json`:
    `98ff739b5208bd6086f44628ef5afe05c00117b57e016afd41efecfacbfda8d2`;
  - `results/d6_binary_tetrahedral_decomposition_exact.txt`:
    `2d169f71396f445b7676b4c7502c14f62f8c21120cb9157ec610c4c50fe8e079`;
  - `results/d6_binary_tetrahedral_cp2_no_go_exact.txt`:
    `8166b2267c16a2f4731f386581d27f69befe4024f07411da5f5fc2743103a4cf`.

## E34 — finite-image fixed-point implication audit

- Run: 2026-07-29 03:27 PDT.
- Primary-source result:
  Rowell's main theorem proves that the canonical braid group generated
  inside \(H_n(3,6)\) is finite for every fixed \(n\). Every exceptional
  tensor representation therefore has finite finite-strand braid image.
  Conti--Lechner Proposition 7.12 and automatic standardness give
  \(\|\phi_R(R)\|_2^2=1/4\ne1/d^2\), so every exceptional \(d>2\)
  endomorphism is nonergodic.
- Exact limitation family:
  for \(d=2m\), \(m\ge2\), set
  \[
  S_m=(q-1)(I_m\boxplus I_m).
  \]
  The human proof gives
  \[
  |\rho_{S_m}(B_n)|\le3n!,\qquad
  S_m^6=I,\qquad
  d^{-1}\operatorname{Tr}_1S_m
  =d^{-1}\operatorname{Tr}_2S_m
  =\frac{q-1}{2}I_d.
  \]
  Both one-leg commutants are scalar. Conti--Lechner Proposition 7.10
  then rules out all nontrivial algebraic fixed points, while Proposition
  7.12 makes the von Neumann fixed algebra nontrivial.
- Exact replay:
  all basis states satisfy involutivity and the braid equation for
  \(m=2,3\); both rational commutant systems have nullity one; the
  normalized partial-trace norm squared is exactly \(1/4\).
- Scope:
  this disproves only an inference from finite image plus the listed
  trace/locality data. The countermodel spectrum
  \(\{q-1,1-q\}\) is antipodal, so it does not settle the sharpened route
  using no-opposite-spectrum and horizontal braid-subfactor
  irreducibility.
- Randomness:
  none.
- Parent commit:
  `eac05ca0`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_finite_braid_image_fixedpoint_countermodel.py`.
- SHA-256:
  - `notes/finite_braid_image_fixed_point_audit.md`:
    `b1f79f224fb44dca707cc63013d0359c85a005e7b8a0066322a7037813b1e14d`;
  - `verifiers/verify_finite_braid_image_fixedpoint_countermodel.py`:
    `60162c9eddd8adb9d47cb331221ff9f51fada79c519e5f9548638105c0349cba`;
  - `results/finite_braid_image_fixedpoint_countermodel_exact.txt`:
    `10269895bf258544562a38df4fe67cdf4c629bd1eda2885316f75eda1cd1af00`.

## E35 — unrestricted Grassmann search from the orthogonalized Manin point

- Run: 2026-07-29 03:23--03:33 PDT.
- Search space:
  the full complex Grassmannian of rank-eighteen projections in
  \(\mathbb C^{36}\), with no imposed symmetry. The initializer is the
  orthogonal projection onto the standard balanced \(GL(3|3)\) Manin
  \((-1)\)-eigenspace plus a seed-dependent small tangent perturbation.
- Predeclaration:
  seeds `26074101`--`26074108` used 500 iterations and no marginal
  penalty; seeds `26074111`--`26074118` used 750 iterations and unit
  penalty on both partial-trace scalar deviations. All seeds and settings
  were written to the manifest before objective evaluation.
- Numerical outcome:
  all eight unpenalized runs returned to cubic squared residual
  \(140/3\), and all eight penalized runs returned to objective
  \(176/3\), to the displayed precision. The two marginal squared
  deviations were \(6\) each.
- Exact identification:
  the unperturbed orthogonalized eigenspace projection has rank \(18\).
  Its associated \(H\) is a trace-zero Hermitian involution, with cubic
  residual squared norm \(140/3\) and both marginal squared deviations
  exactly \(6\).
- Scope:
  this is a calibrated failed-construction certificate. It neither proves
  the exact point is a local minimum nor supports unrestricted
  nonexistence in \(d=6\).
- Parent commit:
  `eac05ca0`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  NumPy `2.0.2`, SciPy `1.13.1`, SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_orthogonalized_manin_near_miss.py`.
- SHA-256:
  - `scripts/d6_riemannian_search.py`:
    `bc26c7b2d61ca5e3e94ce09c777c8e3faa77461fd7091399849ee0d84cd68b55`;
  - `results/d6_manin_orthogonalized_seed_manifest.json`:
    `4473d8cbcf7f3388f2965421107743db4d5a4dba0e07d1f8ef8b738442b56f1d`;
  - `results/d6_manin_orthogonalized_runs.jsonl`:
    `84c1f9e04583685289779da18056c2a9e394780f8fcd32c68b5770dce7bfa3f7`;
  - `results/d6_manin_orthogonalized_penalty_runs.jsonl`:
    `fd97394c7472bb383b7e7bd488b74cb401f3be262d4860837f2c82fd9693ec1b`;
  - `verifiers/verify_orthogonalized_manin_near_miss.py`:
    `b62a8e98b8c609affa00d741086644762eda4d0c730beb23c0002f76e85c76e0`;
  - `results/orthogonalized_manin_d6_exact.txt`:
    `0f58d8d722255813ebb91b591f425dc7dc5bae3c2975f7759ff3690e2a9ccd38`.

## E36 — exact overlap-space Kramers parity audit

- Run: 2026-07-29 03:36--03:44 PDT.
- Universal generic-block calculation:
  on the generic sector,
  \[
  C^*(P_{12},P_{23})=M_2(\mathbb C)\otimes I_k,\qquad
  k=3(d/2)^3.
  \]
  Every antiunitary commuting with both projections is
  \((I_2\otimes u)C_0\), and its square is
  \(I_2\otimes u\bar u\). Thus square \(-1\) exists exactly when \(k\)
  is even; the determinant argument is the parity to be proved, not an
  independent source of it. The same classification holds for
  antiunitaries interchanging the projections.
- Canonical-complex-structure audit:
  \[
  \mathcal J=
  \frac{P_{12}P_{23}-P_{23}P_{12}}{\sqrt2/3},
  \qquad \mathcal J^2=-I
  \]
  on the full generic sector, but \(\mathcal J\) exchanges its two
  \(k\)-dimensional halves. It does not act on the \(1/3\)-eigenspace
  whose parity is needed.
- Exact odd-multiplicity limitation:
  \(27\) common-one blocks, \(27\) common-zero blocks, and \(81\)
  generic blocks give an exact balanced \(216\)-dimensional abstract
  \(H_3\) model with ranks \(108\), overlap trace \(54\), and odd
  \(1/3\)-multiplicity \(81\).
- Bytsko/cyclic stress test:
  for cyclic rotation \(L\), the characteristic compression
  \(W=P_{12}LP_{12}\) has
  \(W^*W=P_{12}P_{23}P_{12}\), while \(WW^*\) uses the opposite cyclic
  neighbor. On the exact published \(d=4\) witness, the two
  \(1/3\)-singular projections have ranks \(24\), trace overlap \(18\),
  squared distance \(12\), and
  \[
  \|WW^*-W^*W\|_{\rm HS}^2=16/3.
  \]
  The same witness has exact flip/adjoint defect \(8\), overlap-space
  outer-reversal defect \(30\), and only a real antiunitary of square
  \(+1\).
- Scope:
  this proves that the abstract pair, cyclic polar overlap, conjugation,
  adjoint/transpose, and bare tensor reversal do not supply the proposed
  Kramers parity. The odd-\(81\) model is not of the tensor-local form
  \(P\otimes I_6,I_6\otimes P\). A deeper tensor-local alternating-form
  theorem remains possible.
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `ab8fe351`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_overlap_kramers_parity.py`.
- SHA-256:
  - `notes/overlap_kramers_parity_audit.md`:
    `7c092537b8cccf9c39afd5d9f4156d96901180faa3c8e0a0f37f1f07f3e3c15f`;
  - `verifiers/verify_overlap_kramers_parity.py`:
    `52117bec29cbdfefa2581248fbd0345181b84af73ebf1b758489110646da7d1b`;
  - `results/overlap_kramers_parity_exact.txt`:
    `089f81051c99e0f7483169097e904d3d08890f158c41538ead7cb843820049d9`.

## E37 — exact commuting-square/projective-descent limitation

- Run: 2026-07-29 03:35--03:48 PDT.
- Universal finite-tower theorem:
  if \(\mathcal A_n=C^*(P_1,\ldots,P_{n-1})\), the Hecke
  double-coset decomposition and automatic scalar partial traces give
  \[
  E_n(\mathcal A_{n+1})=\mathcal A_n.
  \]
  Combining this with Conti--Lechner Theorem 3.8 proves
  \[
  \mathcal L_{R,n}=\mathcal A_n
  \]
  for every exceptional localizer and every \(n\). Thus the finite
  horizontal relative-commutant tower contains no extra parity-bearing
  blocks beyond \(H_n(3,6)\).
- Exact first-cell limitation:
  constructed rank-four projections \(p,q\in M_8\) over
  \(\mathbb Q(\sqrt2,\sqrt3,i)\) with
  \[
  pqp-qpq=\frac13(p-q),\qquad
  \dim\operatorname{alg}(p,q)=6.
  \]
  Here \(p=p_0\otimes I_2\), normalized last-qubit partial trace maps
  \(\operatorname{alg}(p,q)\) onto
  \(\operatorname{alg}(p_0)\), and
  \(pqp\) has spectrum
  \(0^{(4)},(1/3)^{(3)},1^{(1)}\).
- Tensor-locality guard:
  \[
  \|q-I_2\otimes p_0\|_{\rm HS}^2=4.
  \]
  Hence this is an exact first Markov commuting square at formal
  \(d=2\), not an ordinary \(d=2\) localizer. Spectator amplification
  gives
  \(Gm_3=(2s)m_2\) for every \(s\ge1\), including odd \(s\), but still
  does not supply all-level same-\(P\) tensor placement.
- Interpretation:
  inclusion matrices, finite image, indices, and the first connection
  cell cannot canonically descend
  \(\mathbb C^\alpha[A_4]\) to an \(s\)-dimensional multiplicity space.
  A global flatness/module-extension theorem using repeated tensor
  placement remains possible and unproved.
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `ab8fe351`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_d2_commuting_square_limitation.py`.
- SHA-256:
  - `notes/commuting_square_projective_descent_audit.md`:
    `2ab68e2e9e1b0ef446ec4d321c2405d7b10e0b23a9e2679c2042f61b488e8666`;
  - `verifiers/verify_d2_commuting_square_limitation.py`:
    `f1210a674adc10f6711ea0e3027bd32a94ff4c54ef7f127efd4a3f15193cc105`;
  - `results/d2_commuting_square_limitation_exact.txt`:
    `9d35b97ad0075b0037734d484c6bb4dc2da3a392593c7a7323640372b60b3457`.

## E38 — numerical codimension-two cuts of amplified \(d=4\) family points

- Run: 2026-07-29 03:58--04:06 PDT.
- Search space:
  rank-six local projections \(Q\in M_8\), minimizing
  \[
  64^{-1}\|[H_4(s,t)\boxtimes I_2,Q\otimes Q]\|_{\rm HS}^2
  \]
  without symmetry constraints.
- Exact source points:
  three points on the C15 circle \(s^2+2t^2=1\):
  \((1,0)\), \((0,1/\sqrt2)\), and \((1/\sqrt2,1/2)\).
  The script checks the \(d=4\) involution and cubic before amplification.
- Interrupted protocol:
  a predeclared 24-run, 2000-iteration sweep was stopped during its
  second seed for excessive runtime. Its one completed seed and the
  interruption are retained explicitly.
- Reduced predeclaration:
  four new seeds per family point, `26074301`--`26074312`, with 400
  iterations per seed.
- Outcome:
  all twelve reduced runs ended at normalized squared commutator
  \(0.22729901088344\) to the displayed precision. No invariant
  rank-six subspace was found.
- Scope:
  this is only a numerical falsifier for a construction mechanism.
  It proves neither a positive lower bound nor the equivalence of the
  three landscapes, covers only three points of the C15 circle, and
  does not extend the exact C40 theorem.
- Parent commit:
  `ab8fe351`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  NumPy `2.0.2`, SciPy `1.13.1`.
- Replay:
  see `notes/d4_family_amplification_cut_falsifier.md` and
  `results/d6_cut_from_color_face_d4_reduced_seed_manifest.json`.
- SHA-256:
  - `notes/d4_family_amplification_cut_falsifier.md`:
    `7c4ff5ab93a0447aeec1f444063947b790775a81b41fecb759535a29245aaa88`;
  - `scripts/search_d6_cut_from_color_face_d4.py`:
    `8ec0e990c6cf91afeba7bfd577a1785a49efd76e8d595943b2612ee67eec7812`;
  - `results/d6_cut_from_color_face_d4_seed_manifest.json`:
    `38333d91274e2192acf3b87e09af89ca26715f1293572024e7b30ab283e4bb81`;
  - `results/d6_cut_from_color_face_d4_aborted_calibration.jsonl`:
    `c4f9c55e83a34e675c3b523f0327b115a2f806444d5e9e448d8b0dadc8afafc3`;
  - `results/d6_cut_from_color_face_d4_reduced_seed_manifest.json`:
    `8860a3e6c546fcdce4738e51e0f13ef4c9bd2e5e9277a8c431f70195fcf15a4e`;
  - `results/d6_cut_from_color_face_d4_axis_s_reduced_runs.jsonl`:
    `21a163a62b17479502c9dd4f1e4730125c867994b4e479a3cb7119c6837efb91`;
  - `results/d6_cut_from_color_face_d4_axis_t_reduced_runs.jsonl`:
    `3e22d3e774a0f9d1d9c7dc37c6ea5dc355078e00e76e1af8d0deb2ac1c164c04`;
  - `results/d6_cut_from_color_face_d4_interior_reduced_runs.jsonl`:
    `0751036f72bac96cc3cc555f53f1aa8b8e0886363c73ec9e660bea03539c4762`.

## E39 — exact quadratic-subproduct Hilbert and divisibility audit

- Run: 2026-07-29 04:02--04:15 PDT.
- Question:
  whether the exceptional common-one/common-zero subproduct ranks,
  quadratic-algebra associativity, Koszulity, Frobeniusity, or termination
  at degree four force \(2\mid s=d/2\).
- Universal exact result:
  \[
  \dim E_n=\dim F_n=(1,2s,2s^2,s^3,0,\ldots),
  \]
  and the \(1/3\)-angle multiplicity is \(3s^3\).  The exact outer
  partial traces were collected, while the middle marginal was retained
  as a nonscalar positive operator with fixed scalar marginals.
- One-sided-standard limitation model:
  the rank-two projection onto
  \[
  \operatorname{span}\{|0\rangle|1\rangle,\ |+\rangle|0\rangle\}
  \]
  has common-one dimensions \(1,2,2,1,0,\ldots\), one scalar partial
  trace, and cubic residual squared \(13/36\).  Spectator amplification
  gives \(1,2s,2s^2,s^3,0,\ldots\) for every \(s\), including odd \(s\).
- Fully standard limitation model:
  an exact color-controlled rank-eight projection on
  \(\mathbb C^4\otimes\mathbb C^4\) has both partial traces \(2I_4\),
  \(\dim E_3=2\not\equiv0\pmod4\), \(E_4=0\), and cubic residual squared
  \(95/36\).
- Koszul audit:
  \[
  \frac1{1-2st+2s^2t^2-s^3t^3}
  =1+2st+2s^2t^2+s^3t^3+0t^4+0t^5+s^6t^6+\cdots.
  \]
  A degree-one-generated quadratic dual cannot vanish in degree four
  and reappear in degree six, so the exceptional quadratic algebra is
  never Koszul. Ordinary connected graded Frobeniusity is likewise not
  automatic and is already incompatible with the known \(s=2\) Hilbert
  function.
- Scope:
  neither limitation projection satisfies the exceptional cubic.  The
  result closes rank/Hilbert/Koszul/ordinary-Frobenius arguments, not a
  proof that full exceptional tensor locality permits odd \(s\).
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `33e4cb30`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_subproduct_hilbert_parity_audit.py`.
- SHA-256:
  - `notes/subproduct_hilbert_parity_audit.md`:
    `f3e4d6d8d5da4d4b81c234a0a83dd15818a0bfe70ecfff1b14a0b494db2f6375`;
  - `verifiers/verify_subproduct_hilbert_parity_audit.py`:
    `a25b5a3292953c33d9000da2bce1f72deecc8b2ff870a5b89e0b35ea21fc54a3`;
  - `results/subproduct_hilbert_parity_audit_exact.txt`:
    `888e2b47bac05335b3714c9ffe29cf53f5870dfd5f7345823858ca023f3f56a6`.

## E40 — exact orbit and amplification-cut theorem for the C15 circle

- Run: 2026-07-29 04:07--04:13 PDT.
- Question:
  whether the exact C15 color/face family shares a common structural
  form and whether any identity amplification admits a codimension-two
  square-invariant local subspace.
- Method:
  exact Pauli coefficient extraction, polynomial reduction modulo
  \(a^2+b^2-1\), tetrahedral joint-spectrum arithmetic, active-algebra
  closure, and an independent exact sitewise rotation check.
- Outcome:
  \[
  H_{a,b}=\sum_{i=1}^3 A_i\otimes B_i(a,b),
  \]
  where the \(A_i\) are a Clifford triple and the commuting
  \(\sqrt3B_i\) have four one-dimensional joint eigenspaces with
  tetrahedral sign vectors. The rank-at-most-two pencil is exactly six
  lines and contains no plane. The active coefficient algebra is
  \(M_4(\mathbb C)\), uniformly in \((a,b)\).
- Exact orbit:
  \(e^{i\theta(X\otimes U_-)/2}\) fixes every \(A_i\) and rotates
  \((a,b)\), proving that the full circle is one sitewise-unitary orbit.
- Orbit separation:
  the exact fourth flip moments are \(-16/3\) on the color/face orbit
  and \(16\) on the published witness, so the two are not
  sitewise-unitarily equivalent. This is a statement under the finer
  sitewise-unitary relation only. Since both witnesses have the same
  \([q,\eta,d]\), Lechner's two-eigenvalue classification identifies
  them under his broader braid-representation equivalence.
- Theorem:
  every commuting local projection in an identity amplification has
  rank divisible by four; in particular rank \(4m-2\) is impossible.
- Relation to E38:
  the equivalence of its three sampled landscapes is now proved. Its
  positive optimizer endpoint remains numerical and no global lower
  bound is claimed.
- Scope:
  this excludes amplification-and-cut constructions from the complete
  C15 family. It neither classifies all \(d=4\) solutions nor excludes
  a genuinely new \(d=6\) solution.
- Randomness:
  none; deterministic exact SymPy arithmetic.
- Parent commit:
  `33e4cb30`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_no_codimension_two_cut_color_face_family.py`.
- SHA-256:
  - `notes/no_codimension_two_cut_color_face_family.md`:
    `98e083e3fd92568d154baf9300e0868e8928ea0b2ab99fc64f689a7097eeec70`;
  - `verifiers/verify_no_codimension_two_cut_color_face_family.py`:
    `c78f158f8672208a6226849bdef723bebad5876c821fcd6a0e36baceeb77e670`;
  - `results/no_codimension_two_cut_color_face_family_exact.txt`:
    `b7e713bce4be061639ab985094a073d780241fc2696da2525297e2a17c9c420a`.

## E41 — exact reversed \(S_4\)-equivariant heterogeneous no-go

- Run: 2026-07-29 03:51--04:18 PDT.
- Question:
  whether the reversed heterogeneous factorization
  \(A=V_3,\ B=V_2\) contains a diagonal-\(S_4\)-equivariant rank-nine
  solution on \(A\otimes B\otimes A\).
- Exact representation reduction:
  \[
  V_3\otimes V_2\otimes V_3
  \cong1\oplus\epsilon\oplus2V_2\oplus2V_3\oplus2V_3',
  \]
  so the full equivariant commutant is
  \(\mathbb C\oplus\mathbb C\oplus M_2(\mathbb C)^{\oplus3}\), of
  dimension \(14\).
- Complete half-rank coverage:
  the rank-nine equation has exactly ten multiplicity signatures. They
  pair into five representatives under complementation \(H\mapsto-H\).
  Exact group-averaged intertwiners give a full Pauli-sphere
  parametrization for every noncentral multiplicity-two block.
- Exact cubic certificate:
  after scaling each commutant generator by \(24\), the residual lies in
  \(\mathbb Z[\sqrt3,i]\). For the five representatives, respectively
  8, 8, 10, 59, and 10 selected real-rational residual coordinates have
  coefficient row spaces containing the constant monomial \(1\).
  Therefore no parameters, even complex and off the involution spheres,
  can make all selected residual coordinates vanish.
- Scope:
  this closes the complete diagonal-\(S_4\)-equivariant reversed
  \((3,2,3)\) heterogeneous branch. It does not exclude arbitrary
  heterogeneous \(18\times18\) operators or arbitrary \(d=6\) solutions.
- Discovery trace:
  two ephemeral, non-evidentiary scratch probes used deterministic seeds
  `123` and `26072901` to identify the branch as a likely no-go before
  the exact coordinate reduction. Their optimizer output was not used
  in any claim; the retained result is entirely deterministic and exact.
- Randomness in retained certificate:
  none.
- Parent commit:
  `a27246cc`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`, NumPy `2.0.2`.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_s4_reversed_equivariant_no_go.py`.
- SHA-256:
  - `scripts/derive_s4_reversed_heterogeneous.py`:
    `81253c0be3a711c4f61031cb738dd482365681c24c354c6b6c8b54cc9e6bc9a7`;
  - `scripts/derive_s4_reversed_coordinate_ideals.py`:
    `b04abdd497ca37830bd6242574fe566e66c78afdec76d76d640ce1a340f5cd07`;
  - `notes/s4_reversed_equivariant_no_go.md`:
    `e5e37b3c970a24729ba6fd0c9607f0c16357c72572af9d309b9325f39e0e18e1`;
  - `verifiers/verify_s4_reversed_equivariant_no_go.py`:
    `b688de1375f162debd0dbe4af67ebca68510eb0430cfd287e5108ee6a624c1c0`;
  - `results/s4_reversed_equivariant_no_go_exact.txt`:
    `cd925350f08cdfae630faee1d2c9b4608f5f94ab259c67633e346823d90c6db5`.

## E42 — exact low-operator-Schmidt obstruction

- Run: 2026-07-29 04:10--05:40 PDT.
- Question:
  whether arbitrary exceptional Hermitian involutions of low
  operator-Schmidt rank force \(4\mid d\), without assuming that the
  independent local pre/post unitaries in a controlled-equivalence theorem
  preserve Yang--Baxter locality.
- Primary inputs:
  Cohen--Yu Theorem 6 proves that every bipartite Schmidt-rank-two unitary
  is locally equivalent to a controlled unitary; Chen--Yu Theorem 11 proves
  the same for Schmidt rank three. Their equivalence permits four
  independent local unitaries and is not itself inserted into the cubic.
- Exact structural theorem:
  one valid same-site conjugacy converts
  \[
  (Q\otimes S)\left(\sum_iE_i\otimes U_i\right)(R\otimes T)
  \]
  to
  \[
  \sum_iE_i(RQ)\otimes(Q^*SU_iTQ).
  \]
  Hermiticity makes the support graph of \(RQ\) undirected. A
  nonbipartite component is a product block and supplies a genuine
  rank-one projection in the full control-leg commutant, even when its
  target unitary does not commute with targets from the other components.
  If every component is bipartite, the same operator has a
  fixed-point-free form
  \[
  H=\sum_x|\bar x\rangle\langle x|\otimes U_x.
  \]
  Its \(\langle\bar x|\,\cdot\,|x\rangle\) cubic coefficient would force
  \[
  -H(U_x\otimes I)H=\frac13(U_x\otimes I),
  \]
  contradicting operator norms.
- Arithmetic conclusion:
  C17 applies to the true rank-one leg projection, so every exceptional
  solution of operator-Schmidt rank at most three has \(4\mid d\).
  Conversely the published \(d=4\) rank-three witness and identity
  stabilization give rank-three solutions for every \(d\in4\mathbb N\).
  Thus any unresolved \(d=4m+2\) witness must have operator-Schmidt rank
  at least four.
- Independent exact replay:
  the verifier checks the four-unitary normalization, a mixed
  nonbipartite/bipartite stress test with noncommuting target unitaries,
  all six off-diagonal coefficient orientations in a balanced fully
  standard \(d=6\) fixed-point-free limitation model, and both tensor
  orientations of the published and C15 exact \(d=4\) rank-three
  witnesses. The limitation model has exact cubic residual squared norm
  \(512\). The published right coefficient algebra is verified as a
  rank-one MASA, separately from its left \(M_2\)-factor commutant.
- Scope:
  the result does not claim that arbitrary higher-Schmidt-rank unitaries
  are locally equivalent to controlled gates. It therefore narrows but
  does not settle the unrestricted dimension spectrum.
- Randomness:
  none.
- Parent commit:
  `9a90756b`.
- Machine/runtime:
  Apple arm64, `macOS-26.5.2-arm64-arm-64bit`; Python `3.9.6`,
  SymPy `1.14.0`; exact replay wall time approximately \(9.2\) seconds.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_low_schmidt_control_obstruction.py`.
- Raw output:
  `results/low_schmidt_control_obstruction_exact.txt`.
- SHA-256:
  - `notes/low_schmidt_control_obstruction.md`:
    `c17378bac6808907921148604e743f89641aa149ada47a6f9ec24d3c5c4d3f8d`;
  - `verifiers/verify_low_schmidt_control_obstruction.py`:
    `ff650548358bc07d49ff2e012d5aa45aba71503a77aea57ce16253d0464a083d`;
  - `results/low_schmidt_control_obstruction_exact.txt`:
    `03c44cc6cfd58bea9cbe7ba6ef5f5cd61019904a12f4b24fc24fe7f2d8f5010b`.

## E43 — exact determinant-transport and spatial-pairing parity audit

- Run: 2026-07-29 05:17--05:19 PDT.
- Question:
  whether the rank-\(s^3\) common-one determinant space acquires a
  canonical nondegenerate alternating or square-\(-1\) antiunitary form
  from shifted tensor locality.
- Universal theorem:
  if \(e\) is the common-one three-site projection and
  \(E=e_{123},F=e_{234}\), then \(EFE=E/4\) produces the unitary
  \[
  U=2(I_V\otimes i)^*(i\otimes I_V):
  W\otimes V\longrightarrow V\otimes W.
  \]
  After the target flip, the \(V\)-partial transpose factors through
  two copies of the original two-site projection. It has rank
  \(d^2/2\), and every nonzero singular value equals \(d/2\).
- Exact \(d=4\) spatial falsifier:
  for all six \(\pi\in S_3\), the compressions \(eJ_\pi e\) have ranks
  \(8\), \(4\), or \(2\) according as \(\pi\) is the identity, a
  transposition, or a three-cycle. The two cycle compressions coincide,
  so the only real skew-adjoint direction in \(\mathbb R[S_3]\)
  compresses to zero. Coordinate conjugation alone squares to \(+I\);
  every nonidentity permutation/conjugation compression is degenerate.
- Odd-\(s\) limitation:
  at \(s=3\), \(\dim W=27\), \(\dim(W\otimes V)=162\), and the
  partial-transpose support rank is \(18\), with squared nonzero singular
  value \(9\). An assumed antiunitary of square \(-1\) on \(W\) would
  already encode the desired parity and cannot be imported from the
  scalar abstract Hecke block.
- Interpretation:
  the canonical polar unitary acts between two \(2s^2\)-dimensional
  support spaces, not on \(W\). Closed four- and five-site Hecke boundary
  words act scalarly on the determinant multiplicity by C39. This closes
  the audited transport/spatial-pairing route, not the arbitrary
  same-\(P\) tensor-local problem.
- Randomness:
  none.
- Parent commit:
  `553574d7`.
- Machine/runtime:
  Apple arm64, macOS 26.5.2 (25F84); Python 3.9.6, SymPy 1.14.0;
  exact replay wall time \(62.99\) seconds.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_determinant_transport_parity_limitation.py`.
- Raw output:
  `results/determinant_transport_parity_limitation_exact.txt`.
- SHA-256:
  - `notes/determinant_transport_parity_limitation.md`:
    `79ec2758f32c65027cedcb51d986018b0328ba2550b346d96b3f72b618e29fd9`;
  - `verifiers/verify_determinant_transport_parity_limitation.py`:
    `498ae15ee531cbf9ad844dff194aba79a2f810bd6941c214038703363d5d0225`;
  - `results/determinant_transport_parity_limitation_exact.txt`:
    `8f1281ae47bf1d842c86e2558c24560df7ed6f0e63673bc64f37940019bc516e`.

## E46 — exact two-site flip-kernel parity reduction

- Run: 2026-07-29 05:16 PDT.
- Question:
  whether the two-site flip product
  \(K=H\mathsf F\) gives a parity obstruction independent of the desired
  conclusion \(2\mid s=d/2\).
- Universal kernel theorem:
  \[
  \ker(K+I)
  =(\operatorname{ran}P\cap\operatorname{Sym}^2V)
   \oplus(\ker P\cap\Lambda^2V)
  \]
  without any assumption that \(H\) commutes with the flip. If the two
  summand dimensions are \(a,b\), Grassmann's formula gives
  \[
  a-b=s,\qquad
  \dim\ker(K+I)=a+b=s+2b.
  \]
- Determinant cross-check:
  \(\mathsf F K\mathsf F=K^*\), so nonreal eigenvalues occur in
  conjugate pairs and
  \[
  \det K=(-1)^{\dim\ker(K+I)}.
  \]
  Balance gives \(\det H=1\), while
  \(\det\mathsf F=(-1)^s\). Therefore the determinant reproduces the
  same parity and does not prove that the nullity is even.
- Exact \(d=4\) calibration:
  the published witness has
  \(\operatorname{rank}[H,\mathsf F]=8\), so the kernel theorem does not
  depend on flip invariance. Its summand dimensions are \(3\) and \(1\),
  and
  \[
  \chi_K(x)=(x-1)^4(x+1)^4(x^2+1)^4.
  \]
- Exact limitation model:
  the balanced fully standard projection
  \(P_{\rm eq}=|00\rangle\langle00|+|11\rangle\langle11|\) in
  \(d=2\) has summand dimensions \(2+1\) and odd nullity three. It is
  not exceptional: its cubic residual has squared Hilbert--Schmidt norm
  \(4/9\).
- Interpretation:
  even flip-kernel nullity is exactly equivalent to \(s\) even. Any
  proof of it must use the exceptional cubic in a new operator-valued
  way; balance, standardness, Grassmann arithmetic, and the determinant
  do not advance the missing parity.
- Randomness:
  none.
- Parent commit:
  `553574d7`.
- Machine/runtime:
  Apple arm64, macOS 26.5.2 (25F84); Python 3.9.6, SymPy 1.14.0;
  exact replay wall time \(9.81\) seconds.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_two_site_flip_parity_reduction.py`.
- Raw output:
  `results/two_site_flip_parity_reduction_exact.txt`.
- SHA-256:
  - `notes/determinant_transport_parity_limitation.md`:
    `79ec2758f32c65027cedcb51d986018b0328ba2550b346d96b3f72b618e29fd9`;
  - `verifiers/verify_two_site_flip_parity_reduction.py`:
    `55b60226f20908dffa04b0cb3947941063910da3eb1f06f175e5c1dda1ebaf48`;
  - `results/two_site_flip_parity_reduction_exact.txt`:
    `9955756a1d9a64eebdc3d39f8f89e6d7f6402593ab79681e99df4e2562fc2df4`.

## E45 — exact Majid--Markl gluing unitarity audit

- Run: 2026-07-29 05:00--05:31 PDT.
- Question:
  whether the associative Hecke gluing of Majid--Markl, or its complete
  operator-valued Theorem 2.7 form, can provide a hidden
  \(4+2\to6\) exceptional unitary construction.
- Primary-source normalization:
  multiplying the exceptional roots
  \(\{-1,e^{i\pi/3}\}\) by \(e^{-i\pi/6}\) gives
  \(\{\mathfrak q,-\mathfrak q^{-1}\}\) with
  \(\mathfrak q=e^{i\pi/6}\).
- Canonical exact no-go:
  the mixed block is
  \(\left(\begin{smallmatrix}0&1\\1&i\end{smallmatrix}\right)\).
  For every positive one-site metric, the two mixed simple tensors have
  equal norm and real cross inner product, so the second column doubles
  squared norm.
- Operator-valued exact no-go:
  on orthogonal mixed-color sectors the full Theorem 2.7 block is
  \(\left(\begin{smallmatrix}0&S\\U&T\end{smallmatrix}\right)\).
  Its two-root polynomial forces
  \(T=(\lambda+\mu)I\) and \(SU=US=-\lambda\mu I\).
  Unitarity forces \(T=0\), so only opposite roots are possible.
- Interpretation:
  the named associative construction is excluded for every positive
  local metric, and the complete operator-valued architecture is
  excluded for orthogonal color summands. Arbitrary colored mixed
  blocks outside that triangular geometry, and a nonorthogonal
  algebraic color splitting, remain outside the theorem.
- Randomness:
  none.
- Parent commit:
  `553574d7`.
- Machine/runtime:
  Apple arm64, macOS 26.5.2 (25F84); Python 3.9.6, SymPy 1.14.0;
  exact replay wall time \(0.56\) seconds.
- Replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_majid_markl_gluing_no_go.py`.
- Raw output:
  `results/majid_markl_gluing_no_go_exact.txt`.
- SHA-256:
  - `notes/majid_markl_gluing_unitarity_no_go.md`:
    `457fd6aadc50f10f9dcbd858c7e1d24370296c510119c1c9a1198398ef9082d6`;
  - `verifiers/verify_majid_markl_gluing_no_go.py`:
    `72240c78ce7082ea202700ee139fa6f7bb11f636e01c1c09b2b56975447f0331`;
  - `results/majid_markl_gluing_no_go_exact.txt`:
    `513bc6b8f2c7e56efa28ddf9b7c42396c31fb491e6cd332978bfe506d07aa823`.

## E47 — Weyl--Bell-diagonal divisibility and exact \(d=4\) exhaustion

- Run: 2026-07-29 05:24--05:41 PDT.
- Question:
  whether a rank-\(18\) projection diagonal in the generalized Bell
  basis of \(\mathbb Z_6^2\) can satisfy the exceptional cubic, and
  whether the analogous \(d=4\) symmetry class contains a calibration
  witness.
- Exact reduction:
  every Bell-diagonal \(H\) commutes with \(X\otimes X\) and
  \(Z^{-1}\otimes Z\). Thus \(U=H_{12}H_{23}\) commutes with the
  primitive three-site Weyl pair
  \[
  X_1X_2X_3,\qquad Z_1^{-1}Z_2Z_3^{-1}.
  \]
  Its generated algebra is \(M_d\), represented with multiplicity
  \(d^2\), so every \(U\)-eigenvalue multiplicity is divisible by \(d\).
  The cubic polynomial, inverse pairing, and exact zero Bell marginals
  force the multiplicities
  \[
  \left(\frac{d^3}{4},\frac{3d^3}{8},\frac{3d^3}{8}\right).
  \]
  Divisibility of the latter by \(d\) gives \(8\mid3d^2\), hence
  \(4\mid d\).
- \(d=6\) conclusion:
  the forced triple is \((54,81,81)\), contradicting
  \(6\mid81\). This uniformly excludes every one of the
  \(\binom{36}{18}\) balanced sign tables; no enumeration is used in
  the proof.
- \(d=4\) exact calibration:
  all \(\binom{16}{8}=12{,}870\) balanced sign tables were evaluated
  over the Gaussian integers after clearing the cubic denominator.
  A direct \(64\times64\) tensor-matrix replay first checked every
  reduced coefficient and the translation coverage. Exact survivor
  count: zero.
- Preliminary Boolean search:
  before the multiplicity proof was recognized, the full \(d=6\)
  coefficient system was expanded to \(2{,}460\) integer equations in
  36 sign variables and 7,140 exact cubic-parity variables. The
  equation digest is
  `21ed429bd4af28337132be68bc9b520aa637e7ed5a47060a95cac7b9a07e2410`.
  Deterministic 5-second and 120-second CP-SAT limits both returned
  `UNKNOWN`; they are retained only as discovery provenance and are
  not evidence for the theorem. One earlier terminal-transport dry run
  did not retain its final stdout and is likewise not used.
- Randomness:
  no theorem computation uses randomness. The unused CP-SAT driver
  fixed seed `20260729` and one search worker.
- Parent commit:
  `553574d7`.
- Machine/dependencies:
  Apple arm64, macOS 26.5.2 (25F84); Python 3.9.6; SymPy 1.14.0;
  OR-Tools 9.14.6206.
- Exact replays:
  - `/Users/alec/Documents/Math/.venv/bin/python
    verifiers/verify_weyl_bell_diagonal_divisibility.py`
    (wall \(30.95\) seconds, peak RSS \(59{,}818{,}368\) bytes);
  - `/Users/alec/Documents/Math/.venv/bin/python
    verifiers/verify_d4_bell_diagonal_exhaustive.py`
    (wall \(0.96\) seconds, peak RSS \(43{,}745{,}640\) bytes).
- Raw outputs:
  - `results/weyl_bell_diagonal_divisibility_exact.txt`;
  - `results/d4_bell_diagonal_exhaustive_exact.txt`;
  - `results/d6_bell_diagonal_cpsat_5s.json`;
  - `results/d6_bell_diagonal_cpsat_120s.json`.
- SHA-256:
  - `notes/weyl_bell_diagonal_divisibility.md`:
    `41dcd73aa12f1d7f2cc4e562ed52056c9b81832c742c52bb78266c0404cebdb1`;
  - `verifiers/verify_weyl_bell_diagonal_divisibility.py`:
    `f7c5051985c5539f343af434fc7c221b39b3f8b249acff090af502ed5ffc9312`;
  - `results/weyl_bell_diagonal_divisibility_exact.txt`:
    `44d89c894393b689084793cb362d2fa22540acb6a4cf000543f08594edc9911d`;
  - `verifiers/verify_d4_bell_diagonal_exhaustive.py`:
    `f5b87f68489c7d0b772dbfc9be638bf9499a717f4e9ac93052569fa419285a0c`;
  - `results/d4_bell_diagonal_exhaustive_exact.txt`:
    `9928c6ebfb4c576d22ee02fb570c1abcfcd4191ea1c998cffedeee6b65719c4d`;
  - `scripts/search_d6_bell_diagonal_cpsat.py`:
    `e22cc2c0c8a8540dde786137a940b95da7bf9576e5a8f32f6f5df9836a457a51`;
  - `results/d6_bell_diagonal_cpsat_5s.json`:
    `9565936c73b202c60c7cc9eb5c53963ec3aec14814609cac516e47b03c7eee9a`;
  - `results/d6_bell_diagonal_cpsat_120s.json`:
    `c993a5f49516e6a566fe2e1c85ad52242eb42168edf45d592d5652f23997a0a1`.

## E48 — operator-Schmidt-rank-four Clifford-frame parity audit

- Run: 2026-07-29 05:41--05:47 PDT.
- Question:
  whether the rank-three controlled-unitary mechanism extends to arbitrary
  operator-Schmidt rank four, and whether a broad exact rank-four branch
  nevertheless forces \(4\mid d\).
- Literature/assumption audit:
  - Chen--Yu's rank-three theorem uses four independent local input/output
    unitaries and has no rank-four extension.
  - The two-qubit swap is an exact Hermitian involutive OSR-four unitary
    with scalar leg commutants, so rank four is the sharp failure point of
    controlled structure.
  - Neither local equivalence nor the swap was treated as a Yang--Baxter
    equivalence or an exceptional witness.
- Exact theorem:
  for a four-product Clifford frame
  \[
  H=\sum_{j=1}^4c_jA_j\otimes B_j
  \]
  with traceless Hermitian involutory local factors and pairwise-
  anticommuting product terms, the local binary commutation graphs are
  complementary.  If \(d=2s\), \(s\) odd, Clifford representation
  divisibility forces both graph ranks to be two.  The four-vertex
  complement lemma gives an isolated generator on one leg.  It commutes
  with an anticommuting pair, so it has form \(I_2\otimes L\); odd \(s\)
  makes its trace nonzero.  Thus \(4\mid d\).
- Independent exact graph replay:
  all 64 four-vertex graphs were enumerated; all 20 rank-two/rank-two
  complementary cases have an isolated vertex on at least one side.
- Exact limitation calibration:
  \[
  H_\star=\frac12(XI\otimes XI+IX\otimes ZI+ZI\otimes XZ+XZ\otimes ZY)
  \]
  is a \(d=4\) Hermitian trace-zero involution with both partial traces
  zero, OSR four, and scalar leg commutants.  Its exceptional cubic
  residual contains 38 Pauli words and has squared Hilbert--Schmidt norm
  \(1376/9\).  Hence the two-site hypotheses do not supply a nontrivial
  true one-leg control projection or the cubic; no four-local-equivalence
  claim about this calibration is used.
- Scope:
  C61 excludes only the precisely defined four-product Clifford-frame
  branch.  An arbitrary OSR-four Schmidt decomposition need not have
  involutory local factors or pairwise-anticommuting product terms.  The
  unrestricted OSR-four exceptional branch remains open.
- Randomness:
  none.
- Initial parent commit:
  `553574d7`; the shared branch advanced independently during the run.
- Machine/dependencies:
  Apple arm64, macOS 26.5.2; Python 3.9.6.  The verifier uses only the
  Python standard library; SymPy 1.14.0 was present but unused.
- Exact replay:
  `/Users/alec/Documents/Math/.venv/bin/python
  verifiers/verify_osr4_clifford_frame_parity.py`
  (wall \(0.05\) seconds, maximum resident set size \(11{,}370{,}496\)
  bytes).
- Raw output:
  `results/osr4_clifford_frame_parity_exact.txt` (byte-identical on replay).
- SHA-256:
  - `notes/osr4_clifford_frame_parity_audit.md`:
    `53a320f62ec689c29dae3fec14a256f03451d3baa66277b6b4373ec598ab6fb3`;
  - `verifiers/verify_osr4_clifford_frame_parity.py`:
    `661fdfd3efb72066c9218df556076c4282e28e5128de0669a61ef3bc19d1c5a9`;
  - `results/osr4_clifford_frame_parity_exact.txt`:
    `0ad7720f6f7f8c51fd1b44e27235c30415977e9454766b9b6103d5a6410da190`.
