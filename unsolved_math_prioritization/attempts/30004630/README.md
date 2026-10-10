# 30004630 — quadratic growth without quadratic control cost

**Unreviewed first-turn negative candidate.** Read COUNTEREXAMPLE.md. A zero control is proved to be the unique global optimizer for small constant admissible radius, with the source's critical cone equal to zero. Its strict critical-cone positivity condition is therefore satisfied, but concentrating controls converge in L^infinity with objective gap smaller than any fixed multiple of their squared L^2 distance. Terminal-target perturbations also violate a natural Lipschitz L^2-control estimate.

The exact source's vacuous critical cone, PDE, sparsity/state penalties, optional velocity term and neighborhood topology are explicit. Stronger structural hypotheses and weaker growth or stability notions are outside this counterexample. No novelty or human peer-review claim is made.

Run `python verify_algebra.py` with SymPy1.14.0 to reproduce exact_receipt.json. These are finite exact algebra controls, not a PDE simulation or proof of the infinite-dimensional estimates. All analytic arguments are written in the proof and require separate review.
