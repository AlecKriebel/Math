# Partial classification of globally periodic positive rational recurrences

**Status: partial. The arbitrary-order classification remains unresolved.**

This manuscript concerns nonnegative-coefficient linear-fractional recurrences on independent positive initial data. Global period means the least common order of the shift map; individual initial conditions may have shorter periods.

The proofs establish:

- Complete classifications in orders 6, 13, and 15, allowing arbitrary nonnegative real coefficients.
- In every order, only the classical families when the reduced numerator has at most two active variable terms.
- A finite cyclotomic-factor reduction for every odd order, together with arithmetic filters and a finite per-order period bound.
- A uniform exclusion for orders congruent to 2 modulo 4 when the midpoint is the only active odd lag and some even lag is active.
- Further parity, algebraic-unit, lag-gap, and cubic resonance obstructions, and finite exact procedures in the explicitly stated rationally scaled subclasses.

These results do not prove that the five classical families exhaust all orders, and do not supply a new periodic example. Novelty relative to all earlier literature has not been established.

## Reading order

1. `turn01_reduction.md`: surjectivity reduction, coefficient symmetry, rational-ratio and odd-order two-cycle results.
2. `turn02_order_six.md`: complete order-six proof with exact tropical certificates.
3. `turn03_odd_spectral_factors.md`: finite odd-order reduction and exact classifications in orders 13 and 15.
4. `turn04_uniform_sparse_and_resonance.md`: all-order sparse classification and spectral/arithmetic constraints.
5. `turn05_mixed_lags_and_arithmetic.md`: uniform larger-support exclusion, quantitative arithmetic reductions, and the precise remaining gap.

`SOURCES.md` records source scope and method credit. The manuscript reproduces no third-party source documents or dataset contents.

## Exact checks

Run `python verify_turn01.py` through `python verify_turn05.py`. The scripts require Python 3 and SymPy; the recorded run used SymPy 1.14.0. Each script writes its corresponding `turnNN_verification.json` beside itself.

The scripts use exact arithmetic for retained certificates. Finite consistency checks supplement general proofs and are explicitly distinguished from exhaustive finite classifications. Numerical exploratory searches are not included in this packet and are not used as arbitrary-order proofs.

`MANIFEST.json` pins every included file except itself by byte count and SHA-256. This packet contains only authored proofs, exact checks, verification results, and public-source credit.
