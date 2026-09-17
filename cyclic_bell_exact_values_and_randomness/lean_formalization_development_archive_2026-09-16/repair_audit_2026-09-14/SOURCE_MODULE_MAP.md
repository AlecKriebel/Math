# Checked source and polar theorem map

Import `CyclicBell.GeneralCoverageSourceStrategy` to obtain the entire source
coefficient, canonical polar, PVM, and attainment chain below. Every listed
module passed `lake build CyclicBell.<module>`. Standard axiom dependencies for
the central endpoints are recorded in `source_endpoint_axioms.log`.

| Manuscript claim | Checked Lean endpoint |
| --- | --- |
| Literal source coefficients and their DFT | `source_coefficient_DFT` / existing `GeneralSourceFourier` DFT endpoints |
| Equation source-fourier, both sums | `source_fourier_zero`, `source_fourier_one` |
| Source positive clock / forward shift Weyl signs | `source_clock_shift`, `source_relative_weights` |
| W_y^d=(-1)^(d−1)I | `source_relative_power` |
| Literal coefficients equal conjugate polar scalar function | `sourceBob_transpose_finiteCalc`, `sourceLiteralInversePolar_quotient` |
| Source Bob matrices are unitary | `sourceBob_unitary` |
| Source Bob matrices have order dividing d | `sourceBob_order` |
| Positive invertible H_y | `sourceModulus_positive`, `sourceModulus_inverse` |
| H_y is the actual modulus of L_y and 1+W_y | `sourceModulus_eq_canonical`, `sourceModulus_eq_relative_modulus` |
| Q_y=H_y⁻¹(1+W_y†)Z† | `sourceBob_transpose_inverse_formula` |
| Literal source B_y is conjugate of unitary canonical polar factor | `sourceBob_canonical_polar` |
| Actual source d-outcome PVM | `sourceBobMeasurement`, `sourceBobMeasurement_encoding` |
| Source Z/X, B_y and extra Z† in a physical strategy | `sourcePhysicalStrategy`, `sourcePhysicalStrategy_encodings` |
| Actual source reduced expectation equals M_d | `source_reduced_expectation` |
| Actual source augmented physical first value equals M_d+1 | `sourcePhysicalStrategy_attains` |
| Arbitrary-Hilbert canonical positive polar identity | `Coverage.canonical_polar_hilbert_positive_factor_identity` |

The exact full simple spectra of W_y and B_y now pass a normal build in
`GeneralCoverageSourceSpectrum`, independently reviewed here. Endpoints are
`source_relative_full_simple_spectrum` and `sourceBob_full_simple_spectrum`.
The source result chain does not require its simple-spectrum theorem: actual
order-d unitarity already supplies a legitimate d-outcome PVM, while full
simple spectrum supplies the additional manuscript spectral claim.

No target endpoint was used as a premise. The generic helper
`finiteOrderMeasurement` assumes unitarity and order as its mathematical input;
the source strategy supplies the independently checked `sourceBob_unitary` and
`sourceBob_order`, rather than recording them as an unproved validity field.
