# Assumptions ledger

## Bell-model assumptions

| Assumption | Status and use |
|---|---|
| Hilbert spaces are finite-dimensional complex spaces. | Assumed for the counterexample and the structural appendix. |
| Alice and Bob observables are unitary and satisfy `A_x^d=B_y^d=I`. | Assumed for admissible strategies and proved for every constructed observable. The unaugmented upper bound uses only unitarity. |
| Alice and Bob act on separate tensor factors. | Assumed by the stated Bell model. |
| Outputs are the spectral labels `omega^a` and `omega^b`. | Assumed exactly as in the originating functional and used in the projector/Fourier calculation. |
| Exact augmented maximality holds in the structural appendix. | Assumed there; proved for the explicit counterexample family. |
| Eve may hold arbitrary finite-dimensional quantum side information. | Part of the conjectured statement. The counterexample takes `dim H_E=1`. |

## Proved rather than assumed

- No local dimension is fixed in the upper-bound or equality analysis.
- The general equality argument does not assume full Schmidt rank; every
  operator conclusion is restricted to `K=supp(rho_A)`.
- The state is not assumed maximally entangled in the structural appendix.
- Weyl commutation, mutual unbiasedness, irreducibility, and uniqueness are
  never assumed.
- The explicit family uses `Phi_d` as a construction, not a
  without-loss-of-generality step.
- Singular polar factors are handled using canonical partial isometries. The
  structural proof cancels a positive factor only after proving that the
  relevant vector lies in its support range.
- The designated target formula follows from explicit eigenvectors and the
  transpose convention for measurements on `Phi_d`.
- Nonuniformity is exact: it follows from a nonzero autocorrelation, not a
  numerical optimizer.
- The explicit guessing lower bound includes the justification
  `sum |x_m| = 2 sum_{x_m>0} x_m <= 2(d-1) max x_m`.
- Both local marginals are uniform.

## Computational assumptions and boundaries

- `verify_exact.py` relies on Python integer and `fractions.Fraction`
  arithmetic. It uses no floating-point equality and no external algebra
  system.
- Strict positivity of the two exact `d=4` polar lengths uses the elementary
  real inequalities `2*cos(pi/8)>0` and `2*cos(3*pi/8)>0`; the verifier
  checks their exact field expressions.
- `cycle_family.py`, `test_cases.py`, and `discovery_search.py` use floating
  point. They are secondary checks or historical discovery tools.
- `family_certificate.json` records all-dimensional symbolic formulas but is
  not a formal proof object. The all-dimensional result rests on the
  manuscript.
- PDF compilation and rendering are presentation checks only.
