# Reproducibility

Python 3.10 or newer; standard library only; no network or external datasets are needed. Run from this public directory:

    python3 -I -B verify_package.py
    python3 -I -B run_checks.py
    python3 -I -B check_tamper_controls.py

The first command is a strict inventory, byte-identity, scope, local-link, and acceptance-binding check. The second replays every included finite mathematical checker under normal, `-O`, and `-OO` Python in disposable copies, compares its exact stdout with its checked-in fixture, and runs both explicit-guard probes and mathematical mutation controls. The third tests file integrity and scope rejection, including mutations whose modified JSON is deliberately rehashed into the manifest. No script updates the public package during these replay commands.

## Mathematical checkers

- `checks/exact/finite_solver.py` contains exact integer column-transfer optimization, exact optimum counting, the separate D≤1 recurrence, exhaustive small-subset search, edge branching, and all-optima backtracking.
- `checks/exact/verify_exact.py` recomputes all 200 smooth-prefix minima and constrained values. It checks witnesses, optimum counts, smooth ordering, increments, adjusted colors, exceptional patches, the 25-value numeric-cutoff table, and the index-45 unique optimum. Twelve separately invoked mutation controls must reject altered minima, witnesses, cutoffs, counts, increments, q0/q1 values, color counts, patch identity, prefix length, and provenance.
- `checks/check_crosslinks.py` directly checks all 200 sets of stored witnesses, compares the 77 independently generated minima and counts with the main certificate, compares all 200 overlapping q1 values with the 280-base certificate, and checks the arithmetic input and checker-to-fixture identities. The wrapper regenerates each underlying fixture output separately; this comparison is not another optimization algorithm. Four cross-link corruptions are separately rejected.
- `checks/check_structure.py` exhausts the 16 four-bit exact-one stencils, eleven small cases, and the four normalized terminal profiles used in the all-scale exact-one proof. It also tests the exceptional patch, its excluded endpoint, disjoint anchor-color matchings, and explicit negative controls.
- `checks/check_arithmetic.py` validates the exact finite input and rational constants, the nine-breakpoint candidate increment partition at endpoints and interior points, and the exceptional/isolated correction boundaries. It does not independently optimize the input tau values or prove actual output is binary.
- `checks/check_independently.py` imports none of the above mathematical implementation. It transposes the transfer direction, checking minima and counts through index 77. A separate vertex include/exclude search checks smooth minima through index 45 and directly optimizes the full integer interval for N≤80. Its component-decomposition check includes every integer N in that range.

- `checks/check_single_defect.py` exhausts three impossible interior stencils, nine left classifications, all 24 normalized suffix phase cases, and the 280 smooth base cutoffs below 3^18. Its default output is the full certificate; `--check fixtures/check_single_defect.json` additionally compares an existing certificate without changing it. Four built-in certificate corruptions must reject.
- `checks/check_local_independently.py` independently evaluates the affine stencil recurrence by a closed-form integer binomial formula. It compares every one of the 173 feasible suffix configurations and six left configurations, and checks all three interior impossibilities.
- `checks/check_tail.py` compares the exact reciprocal-tail formula with an independently summed complement at 70 exact cutoffs and one-sided rational neighbors. Its finite tests do not prove unboundedness of the remainder.

The single-defect finite certificate proves q1 only in combination with the full written all-scale reduction. It does not prove unrestricted tau=q1.

The exact solver uses integer powers and bit operations; no floating-point logarithm determines a combinatorial boundary. The arithmetic checker uses `Fraction`. All active verification guards are explicit exceptions, not `assert`, and the wrapper scans the checker sources for optimization-sensitive assertions.

## Fixtures and negative controls

All JSON mathematical fixtures are generated from the definitions in these authored checkers. They are synthetic mathematical data, not downloaded datasets. The five exact packet files are under `fixtures/exact/`; each executable checker's exact stdout is under `fixtures/`.

A fixture equality verifies reproducibility, not independence. Independent algorithms and direct witness checks supply separate comparisons. A manifest identity verifies bytes, not a theorem. The reader and supplements explicitly distinguish finite certificate results from written all-scale proofs and analytic reasoning.

Semantic controls corrupt the recurrence, the rational constant, the candidate color increment, independently optimized tau, and the actual numeric input; they also remove the single-defect exceptional saving or shift its color. Every mutation must fail through its intended guard. Explicit-guard probes must fail in all three interpreter modes. Integrity controls cover altered, missing, unlisted, and symbolic-link files; malformed JSON; unsafe manifest paths; unauthorized solution or completed-checkpoint claims; removed acceptance; and incomplete proof bindings.

Replay records are stored as `CHECK_REPLAY.json` and `TAMPER_CONTROLS.json` only after a successful final-edition run. Any later change requires a new manifest and replay. A checker is not a formal proof assistant, and the analytic arguments are not represented as mechanically verified.
