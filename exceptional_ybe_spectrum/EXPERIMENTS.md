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
| E7 | Controlled-reflection/face-model search, calibrated at \(d=4\) and then tested at \(d=6\). | Numerical discovery only | Predeclared in `results/d6_face_seed_manifest.json` | IN PROGRESS |
| E8 | Equal-sector and crossed operator-valued color/face models. | Exact reduction and \(d=4\) family; numerical \(d=6\) search | Recorded in raw JSONL logs | COMPLETED: no \(d=6\) candidate |

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
