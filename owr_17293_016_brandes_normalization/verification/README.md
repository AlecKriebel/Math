# Exact verification companion

Run `python3 verification/verify.py` from the project folder. Python 3.9+; standard library only. The run exits nonzero on failure. The checked-in `results.json` is reproducible by redirecting stdout.

The script checks 12 rational basis certificates, covering 120 symmetric coefficient classes. It independently checks 110 of those entries by inclusion-exclusion polarization. It also checks the quadratic coefficient identity symbol by symbol for degrees 2 through 24, and rejects a basis violating the bound and a singular basis. The universal identity is proved algebraically in the paper; finite runs are diagnostics, not a proof for all degrees.

The examples include dimensions 1–4, degrees 2–8, a positive nonconvex quartic, and a quartic that violates the desired bound in its original coordinates. The radial examples are positive definite because they are the Euclidean norm to degree d plus nonnegative even powers. The nonconvex quartic is (x^2-y^2)^2+x^2*y^2, which is positive away from zero. The last quartic is x^4+12*x^2*y^2+y^4, also positive definite.

For a supplied rational form and basis, run:

```
python3 verification/verify.py --input verification/examples/nonconvex-quartic.json
```

JSON uses `dimension`, positive even `degree`, a `monomials` list with integer `powers` and rational-string `coefficient`, and `basis_rows` (matrix rows, with the basis in its columns). The script verifies the stronger conclusion: all ordered entries positive, all mixed inequalities strict, pure equality, and a nonsingular basis. It expands p(S t), then divides each ordinary monomial coefficient by the multinomial multiplicity. Every inequality is checked in rational arithmetic after raising to the even power d; there are no floating-point tolerances.

This script does **not** decide positive definiteness of an arbitrary supplied polynomial, find a sphere minimizer, certify a universal epsilon, or formally prove the general existence theorem. Those are analytic parts of the paper. It verifies the requested coefficient property of a proposed rational basis even if the input's positivity is not supplied. Large degrees or dimensions can require substantial time, especially for the independent polarization checks (enabled through degree 6).

## Additional fresh-review checks

Run `python3 verification/preprint_round_2_checks.py` for seven independently implemented rational examples (33 coefficient classes and 19 positive definite bilinear slices), two expected fixed-perturbation failures, and the excluded nonnegative endpoint. These use signed polarization without importing the main verifier. The negative-control formulas are also checked against direct polynomial evaluation and polarization. The integration correction to their original handwritten coefficient is documented in audit/preprint-round-2.md.
