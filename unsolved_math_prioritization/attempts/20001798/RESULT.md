# First-turn candidate: an explicit Airy relationship

The literal original problem requests a description connecting WKB, EO recursion, DM recursion and the (wild) nonabelian Hodge correspondence in at least one example. `PROOF.md` gives a proposed complete worked example for that source reading, pending independent mathematical and source-scope review.

- Classical input: the global radial harmonic metric for the degree-one polynomial rank-two Higgs field.
- Proved scaling deduction: its flat twistor family with zeta=hbar R converges in the displayed fixed frame to the Airy oper in every compact C-infinity seminorm, at rate O(R^(4/3)) for fixed nonzero hbar.
- Classical all-order input, with matching normalizations: the Airy oper's WKB expansion equals the principal specialization of both EO and DM recursion on the same normalized spectral curve.
- Explicit domain: the plane, with its ramified irregular end at infinity, arbitrary R>0 and hbar in C*. WKB expansions are formal on a chosen sheet away from the turning point; actual Airy functions have the classical sectorial expansions.

This is one substantive author turn. Source triage, source recovery and finite checks are not separate proof turns. If independent source review requires a stronger global-end statement for the original request, this remains a partial first-turn result and the remaining four substantive turns must be used before unresolved finalization.

The proof does not assert that the metrics themselves converge, that the two limits R->0 and hbar->0 can be exchanged, that compact connection convergence implies Stokes-coordinate convergence, or that a general wild conformal-limit conjecture is solved. All classical inputs are credited, and no historical novelty is certified.

Reproduction: run `python verify.py` from this directory with SymPy installed. Its deterministic receipt has 103 exact finite controls, including frame/adjoint/curvature constants, the ramified Gram matrix, EO residues and 20 Riccati orders. These controls supplement the analytic proof and cited all-order theorem; they do not replace either.
