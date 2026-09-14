# Independent finite arithmetic and domain audit

Final audit checkpoint: 2026-09-14 15:03 UTC. Reviewer responsibility: the actual
finite phase margin definitions, arithmetic certificates, endpoint conventions,
and denominator domains. This reviewer did not implement the small-order scalar
systems or the physical active-chain identification. This report is a statement
audit in addition to kernel checking, not an alternative mathematical checker.

## Definition and range correspondence

I compared `Margins.lean` directly with Appendix A (A.20), (A.27), (A.30),
and (A.32), without treating the Python verifier as an authority.

* `t N 0 = 0` is an auxiliary convention. The first recurrence step is
  exactly `2N/(2N-1)`, and the step from `k` to `k+1` has numerator
  `2N+k*t(N,k)` and denominator `2N-(k+1)`. This is the printed recurrence
  after the single index shift; the physical ranks are `1,...,N-1`.
* `lowerEll N j` is exactly `(3Nj+3N-8j-10)/(3Nj(j+1))`.
  All arithmetic subtractions in this expression and in `c`, `epsilon`,
  and `betaTerm` occur in the rational numbers, not truncated naturals.
* `c N=(2N-5)/(2N(N-2))` and
  `epsilon N=(25/11)*c N/(1-c N)` retain both normalization factors.
* `beta` takes the maximum of the actual `betaTerm N j` values over
  `Finset.Icc 1 (N-2)`. Removing duplicate values through `image` changes
  no maximum. On the claimed domain the index set is nonempty. Its fallback
  value at an empty rank set is irrelevant to every finite theorem.
* The interval contains exactly 248 orders: `40,...,287`. The later-order
  bound covers exactly 247 orders: `41,...,287`. Neither the omitted top
  a rank `j=N-1` nor an extra rank zero is included in the maximum.

## Certificate mechanism and trust path

The external generator supplies an integer list `w` of length `N`, starting
at zero. Successive entries are rounded down using denominator 10000. Lean
does not trust this description: `MarginCertificate` directly checks the
initial equality, every one-step rational recurrence inequality through
rank `N-1`, strict positivity of every witness and occupation factor used,
and each physical-rank reciprocal inequality. The recurrence checker has one
extra positive rank beyond the maximum's domain, which is harmless.

`gridValue_le_t` uses induction and a strictly positive recurrence denominator
to compare the witness with the actual recursive `t`. `betaTerm_le_grid`
uses positive lower denominator and positive occupation factor to justify
the reciprocal inequality in the correct direction. The theorem
`beta_add_epsilon_le_of_certificate` then passes the bounds to the actual
finite maximum. A false external witness therefore cannot establish the
theorem; its Lean check fails.

Each of the 248 order certificates uses `decide +kernel`. There is no
`native_decide`, compiler evaluator, asserted answer axiom, or imported
solver-correctness assumption in this path. One serially dependent module
per order bounds peak build memory. These imports do not introduce any
mathematical hypothesis. Regeneration was independently checked to preserve
all 248 files byte for byte and cover exactly the intended order interval.

## Exact minimum and independent numerical falsification attempt

I separately reconstructed the exact recurrence and every maximum using
Python `Fraction`. All 248 actual margins are positive. The minimum is

`639304267467075678841 / 115369588296792467144716`,

at `N=40`, where the maximum occurs at `j=20`. The second-smallest actual
margin is at `N=41`, rank `j=21`, and equals
`242900113925751690729 / 21341223935004904893304`.
Every later margin is greater than `1/100`. These computations are independent
corroboration only and are not used as proof inputs.

Lean's `exact_margin_40` computes the actual rational recurrence and maximum,
not the grid bound. The grid proves margin at least `1/200` at `N=40`
and at least `1/100` at every later finite order. Because the exact printed
fraction is strictly smaller than `1/100`, the final minimum proof identifies
the unique minimizing order without trusting an external maximizing-rank
assertion.

## Denominators and exceptional orders

The generic theorems `c_den_pos` and `one_sub_c_pos` establish the denominator
domains for `c` and `epsilon` for every `N≥3`. `RankBounds.lean` proves:

* `t_step_den_pos`: `2N-j>0` through physical rank `j=N-1`;
* `lowerEll_den_pos`: `3Nj(j+1)>0` for `N≥3`, `j≥1`;
* `beta_numerator_den_pos`: `3(j+1)(N-2)>0` for `N≥3`;
* `beta_den_pos`: `(11/25)*lowerEll N j*t N j>0` for
  `N≥4`, `1≤j≤N-2`.

The separate checked identity `lowerEll_three_one` proves that the occupation
lower bound is zero at `N=3,j=1`. This does not contradict the manuscript's
large-order phase argument; it prevents extending that argument's positivity
assumptions to the small-order endpoint. The actual `S_3` must be handled by
its linear-system certificate. At population `n=3`, `N=2`, the balanced
symmetric sector is absent and none of the finite phase claims applies.

## Build and axiom status

The full 248-order serial build completed successfully with
`lake build SymmetricSector.FiniteMargins`, followed by a successful
`lake build SymmetricSector.PhaseMargins`. The exact N=40 computation,
all generated certificates, all four finite wrapper theorems, and the
extended `RankBounds` have compiled. `all_phase_margin` now combines these
certificates with the actual analytic tail to establish `beta N + epsilon N < 1`
for every integer N≥40.

The independent query `lake env lean reports/FiniteMarginAxioms.lean`
completed successfully; its full statement and dependency output is retained
in `reports/FiniteMarginAxioms.log`. The representative endpoint grid
certificates `cert40` and `cert287` use only `propext`. The generic certificate
interpretation, exact minimum, complete quantified finite bounds, actual
all-order phase margin, and queried denominator/boundary results use only
`propext`, `Classical.choice`, and `Quot.sound`. No computed-answer,
compiler-trust, or project-specific axiom appears. The complete project
clean build is a separate final audit and is not inferred from these
component build commands.

## Scope boundary

This component concerns the actual finite `beta+epsilon` inequalities and
the printed minimum. It neither identifies the reduced scalar with an
active-chain expression nor supplies the Schur/barrier argument needed to
deduce its positivity from these margins. The all-order scalar and physical
quadratic-form obligations remain separate. No finite-definition mismatch,
finite arithmetic counterexample, or paper gap was found in this audit.

Completion estimate for this review's finite-margin component: 100%.
All statements, complete certificate range, build results, and final axiom
dependencies are checked. This is not an estimate of the whole three-stage
project.
