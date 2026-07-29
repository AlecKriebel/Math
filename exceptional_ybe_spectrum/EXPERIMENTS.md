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
| E4 | Structured \(d=6\) search, first ansatz family. | Numerical discovery only | To be recorded before run | PLANNED |
| E5 | Independent exact verification of any \(d=6\) candidate. | Exact algebraic | N/A | CONDITIONAL |

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
