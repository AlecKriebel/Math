# Independent v1.0.8 core-control results

These controls import no project helper or stored certificate.  The source is
`independent_v108_core_controls.py`.

## Exact reconstruction run

Command:

```text
/Users/alec/Documents/Math/.venv/bin/python independent_v108_core_controls.py
```

Outcome: exit 0 in 0.99 s (Python 3.9.6, SymPy 1.14.0).

- The indexed reactions were rebuilt into `Y`, `Gamma`, and
  `A=Gamma*diag(flux)*Y.T`.
- Every induced principal set of size below `m` was enumerated for
  `m=3,...,8`, both at `(a,b)=(3,5)` and on `b=2a` at `(3,6)`.  Counts per
  parameter case were 10, 25, 56, 119, 246, and 501; no unclassified SCC was
  found.
- For `m=3,...,8`, the exact core Schur complement was

```text
[ -(a+b)   -a       -b      ]
[ -a       -a        2a     ]
[ 2a-b      2a      -(4a+b) ]
```

  and its determinant was `2*a**2*b`.  For `m>=4`, the eliminated block had
  determinant `(-a)**(m-3)` and inverse bottom-left entry `-1/a`; `m=3` was
  checked directly.
- The mass-action Hessian was reconstructed reaction by reaction.  Exact
  linear solves for the gauge-fixed `w_0` and unique `w_2` matched the claimed
  numerator `R_m+C_m*hfrak_m` for `m=3,4,5,8,12`; every numerator was positive,
  every `ell.T*r` was negative, and every resulting cubic coefficient was
  negative.
- A separate symbolic calculation verified the four-factor `w_2` recurrence
  and the dimension-dependent interior product sum as identities in formal
  `m`.
- Independently shifting `Q_m`, `P_R`, `P_C`, and the cleared lower-bound
  polynomial `L_m` by `m=u+3` reproduced strictly positive coefficient lists.
  The harmonic upper bound also reduced the numerator proving `ell.T*r<0` to a
  shifted polynomial with positive coefficients.  This completes the
  all-dimensional sign check rather than inferring it from the five direct
  dimensions.

## New author verifier

Command:

```text
/Users/alec/Documents/Math/.venv/bin/python independent_verifier/verify_generic_cubic_recurrence.py
```

Outcome: exit 0 in 0.66 s with `GENERIC_CUBIC_RECURRENCE_PASS`.

The default `/opt/homebrew/bin/python3` is Python 3.14.6 without SymPy and
failed with `ModuleNotFoundError`; this is an environment-selection issue, not
a mathematical failure.  The following fail-closed control exited 1 with the
advertised assertion-mode message:

```text
/Users/alec/Documents/Math/.venv/bin/python -O independent_verifier/verify_generic_cubic_recurrence.py
```

Replacing the terminal closed-form function in memory by its value plus one
caused an `AssertionError`, reported as `MUTATED_CLOSED_FORM_REJECTED`.

## Tag and theorem controls

- SHA-256 hashes of snapshot `main.tex`, `supplement.tex`,
  `verify_generic_cubic_recurrence.py`, and
  `proof_audit/all_spectrum_localization.tex` exactly matched their v1.0.8 tag
  blobs.
- Extracting every proposition, lemma, theorem, and corollary environment from
  v1.0.7 and v1.0.8 and comparing them produced no difference (exit 0).
- `git diff --check` on the load-bearing changed files produced no error.
