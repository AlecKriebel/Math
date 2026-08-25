# Exact signed two-minor certificates

This package closes twelve of the residual one-active wrong-split directions
in the strong cross-bridge calculation:

`108, 110, 113, 114, 116, 120, 128, 175, 178, 180, 181, 184`.

For each target, the package rebuilds the K3P Fourier map directly from the
frozen graph-derived switching signatures.  It selects two (2\times2)
minors from the character-sum 0 and character-sum 1 blocks.  The exact signed
combination

\[
M_0+\varepsilon M_1=mR,\qquad \varepsilon\in\{-1,+1\},
\]

has a strictly positive monomial factor (m).  Every tensor-Bernstein
coefficient of (R) on the closed unit cube is nonnegative and at least one
is positive.  Since every Bernstein basis function is positive in the open
cube, (R>0) there.  A bridge cut would make every Fourier character block
rank one, forcing both (M_0) and (M_1) to vanish, which contradicts the
strict positivity of their signed combination.  The certificate holds on the
full strict edge-spectrum cube and therefore on the K3P principal domain
\(\mathcal D_{3,+}\).

The producer searches a fixed finite family in a stated lexicographic order;
it does not hard-code the selected polynomial.  The verifier independently
rebuilds the 204-direction target universe and all Fourier polynomials.  It
does not import the producer, exploratory scripts, or the frozen K3P compiler.

## Artifacts

- `SIGNED_PAIR_CERTIFICATES.json`: theorem-facing exact manifest, including
  explicit reduced polynomials and nonzero Bernstein coefficients.
- `VERIFICATION_REPORT.json`: independent exact replay result.
- `ADVERSARIAL_MUTATION_REPORT.json`: 33 verifier mutations, all rejected.
- `build_signed_pair_certificates.py`: deterministic certificate producer.
- `verify_signed_pair_certificates.py`: independent exact verifier.
- `run_adversarial_mutations.py`: subprocess-isolated mutation suite.

## Replay

No third-party Python package is required.

```sh
python3 build_signed_pair_certificates.py
python3 verify_signed_pair_certificates.py
python3 run_adversarial_mutations.py
```

All proof arithmetic is over Python integers and exact rational numbers.  The
package proves precisely the twelve exclusions above; it does not by itself
assert closure of the other residual directions or the global containment
theorem.
