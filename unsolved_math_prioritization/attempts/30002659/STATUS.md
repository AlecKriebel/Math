# Status and verification scope

- Exact source target: every shortest Euclidean billiard orbit in every constant-width body is period 2.
- Result: **unsolved, 5/5 substantive author attempts**.
- Full-dimensional nonplanar orbits with low total turn and non-antipodally-symmetric normal measure remain unexcluded.
- No counterexample of length <=2 has been certified.
- 156 exact symbolic controls pass. They check finite examples, identities, constants, an infeasible negative control and a smooth counterexample to a failed proof shortcut. They do not prove the universal conjecture.
- An 80-start four-orbit numerical exploration is retained separately. It is not an exact optimization bound, interval certificate or full-dimensional search.
- Classical inputs are credited in SOURCE_GATE.md and ATTEMPT_2.md. The partial derivations are independently checkable but no historical novelty is asserted.
- Independent adversarial review: pending.

## Reproduction

Run `python verify_exact.py` (SymPy 1.14.0 in the recorded run). Its output is `verify_exact_results.json`.

Optionally rerun `python search_four.py` with NumPy and SciPy versions given in `search_four_results.json`. Numerical optimizers may produce platform-dependent near-feasibility residuals; the complete per-run residuals and status flags are part of the recorded diagnostic. No theorem depends on them.

The SHA256SUMS manifest freezes the author packet for review and excludes itself. Source papers, renders, full imported corpora and private workflow records are outside the public packet.
