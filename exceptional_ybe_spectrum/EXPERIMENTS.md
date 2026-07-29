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
