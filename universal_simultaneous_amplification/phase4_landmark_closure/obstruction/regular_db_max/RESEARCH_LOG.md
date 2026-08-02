# Research log

## 2026-08-02 06:33 PDT -- initialization and regular-polytope search

- Parameterized every symmetric stochastic zero-diagonal kernel as an affine
  point in the nullspace of the unsigned incidence matrix.
- Constrained searches through orders four to nine found no dB fixation value
  above the complete baseline at fitness two.  In orders four through eight,
  every polished start returned to the uniform complete kernel.
- Random midpoint tests and line scans found positive concavity slack.  This
  is **NUMERICAL ONLY**.
- Subtask completion estimate: **35%**.  The universal theorem remained open.

## 2026-08-02 06:55 PDT -- exact order-four closure

- **PROVED** the exact formula `rho=4A/(4+5A)` for every regular weighted
  four-vertex graph, with `A=sum 4x/(4+x)` over the three opposite-edge
  weights.
- **PROVED** the strict complete-graph comparison by an exact sum of three
  rational squares.  The independent verifier checks all fourteen labelled
  transient equations before checking the sign identity.
- Found the key `r=2` hypercube identity: the two opposing rates on each
  configuration edge sum to one.  This fixes the symmetric part of the
  generator but has not yet yielded the required nonreversible capacity
  comparison.
- Subtask completion estimate: **62%**.  The finite exact theorem and search
  package are closed; global regular-kernel concavity remains **OPEN**.

## 2026-08-02 07:04 PDT -- sharpened marginal target

- The componentwise complete-matching odds coefficient is false for regular
  kernels from order five onward.
- The aggregate inequality (5) in the README survived reproducible random
  tests through order nine.  Together with Jensen it would prove the exact
  finite complete baseline, rather than merely the half-density bound.
- No proof of (5), no proof of global concavity, and no regular counterexample
  is claimed.  Subtask completion estimate: **68%**.

## 2026-08-02 07:14 PDT -- global concavity exactly falsified

- Boundary-focused sampling found a negative Jensen slack at order seven,
  between weak complete-support perturbations of a seven-cycle and of a
  disconnected `C_3+K_2+K_2` extreme kernel.
- **EXACTLY FALSIFIED** global concavity using
  `epsilon=1/200000` and `lambda=1/2000`.  Three independently built
  126-state rational absorbing solves give slack
  `-0.0000900610858953220657...`; its reduced numerator and denominator have
  6,857 and 6,871 bits.  All three kernels are positive and regular.
- All three fixation probabilities remain strictly below the complete
  baseline, so the complete-maximizer conjecture survives.  The exact
  counterexample closes permutation averaging and any proof based solely on
  global concavity.
- The aggregate stationary-odds inequality (5) is now the cleanest surviving
  regular-only target.  Subtask completion estimate: **73%**.
