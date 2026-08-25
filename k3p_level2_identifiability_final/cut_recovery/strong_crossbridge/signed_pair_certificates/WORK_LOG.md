# Work log

## 2026-08-25 07:57 PDT — independent compilation and deterministic search

- Implemented a standalone compiler from the frozen switching-mask records to
  all 64 four-port K3P Fourier coordinate polynomials.
- Searched the prescribed signed-pair family using exact integer polynomial
  arithmetic and exact rational tensor-Bernstein conversion.
- Recovered the expected twelve certificates, with operators `-1` for targets
  `108, 110, 113, 114, 116, 120` and `+1` for targets
  `128, 175, 178, 180, 181, 184`.
- The reduced-polynomial hashes agree with the prior discovery values.
- Completion estimate for this bounded twelve-target certification task: 60%.

## 2026-08-25 08:00 PDT — independent exact verification

- Added a verifier that does not import the producer, exploratory
  cross-bridge scripts, or the frozen K3P compiler.
- Independently rebuilt all 204 normalized target directions, the selected
  block minors, the signed combinations, the positive monomial factors, and
  every Bernstein coefficient.
- Exact replay passed for all twelve records.
- Completion estimate for this bounded twelve-target certification task: 85%.

## 2026-08-25 08:02 PDT — adversarial closure

- Ran 33 subprocess-isolated adversarial mutations covering every signed
  operator and the input, target, descriptor, minor, reduced-polynomial,
  Bernstein, ordering, and aggregate-hash bindings.
- The independent verifier rejected all 33 mutations.
- Added a theorem-facing proof explanation and reproducibility instructions.
- Completion estimate for this bounded twelve-target certification task: 100%.
