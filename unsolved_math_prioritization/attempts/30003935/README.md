# 30003935: a bounded-forward strong EKI theorem

[The partial result](PARTIAL.md) proves strong convergence with the time supremum inside the \(L^q\) norm for the exact stochastic EKI scheme with a bounded, locally Lipschitz nonlinear forward map. It also exhibits a smooth globally Lipschitz forward map for which uniform quadratic generator and one-step moment estimates fail.

The general nonlinear source problem remains **unsolved, 2/5**. The quadratic obstruction is not a counterexample to convergence. Finite ensemble, fixed time interval, Brownian coupling, forward-map restrictions, and initial-moment assumptions are explicit. Published probability/conditional-moment results and the standard localization method are credited. No priority claim is made. Separate adversarial review passed without mathematical corrections; see [the independent report](review/REVIEW.md). The frozen proof retains its historical pending-review sentence. The 3,270 independent exact controls also pass.

- [Exact verifier](verify.py) and [receipt](verification.json): 1,954 assertions with SymPy 1.14.0
- [Sources](source_manifest.json), [readiness](readiness.json), [research log](RESEARCH_LOG.md)
- [Frozen hashes](frozen_artifacts.json)

The original does not specify a strong-moment exponent or the location of the time supremum; the theorem does. Source PDFs are not redistributed. Run the verifier beside PARTIAL.md; finite algebraic controls do not certify a stochastic convergence theorem.

