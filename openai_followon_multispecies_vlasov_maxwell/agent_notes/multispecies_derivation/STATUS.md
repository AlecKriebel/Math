# Multispecies derivation checkpoint

Timestamp: 2026-10-06T21:26:50-07:00 (America/Los_Angeles).

Best estimate toward the original targets: mathematics 25%; publication
package 3%. These estimates may change after adversarial upstream review.

The dedicated subtask's artifacts are:

- `derivations/multispecies_derivation/PAIR_IDENTITY.md`: exact normalization,
  constraints, mass-weighted energy/cone flux, pair field coefficients, signed
  cancellation proof and degenerate cases.
- `derivations/multispecies_derivation/TRANSFER_LEMMA.md`: parameter-robust
  transfer proof, simultaneous bootstrap quantifiers, source/receiver cutoff
  factors, direction and enhanced occupation dependence, pure selected-bin
  coefficients and exact upstream dependency table.
- `derivations/multispecies_derivation/verify_pair_identity.py`: reproducible
  generic cleared-denominator polynomial check using only Python standard
  library. No numerical tolerance or external dependency.
- `derivations/multispecies_derivation/pair_identity_certificate.json`: output
  with zero residuals, Python version and exact script hash.
- `agent_notes/multispecies_derivation/source_manifest.json`: hashes and byte
  sizes of source files actually used from pinned family 362.

The algebraic normalization and source/receiver identity are proved. In
particular the common physical pair prefactor is `c_ab=(e_a/m_a)e_b`, while
source cutoff/acceleration terms carry `c_ab(e_b/m_b)` and receiver terms
carry `c_ab` with the full normalized receiver derivative `K_a`.

Under a simultaneous signed bootstrap, stable-cell occupation is proved
specieswise with positive energy bounds `H_0/m_b`. The full analytic transfer
is conditional on the actual upstream scalar dyadic arguments, which have
been read but are being independently audited by the parent research effort.
Nothing in the extension step requires equal acceleration coefficients,
equal masses, same-sign charges, neutrality, a positive lower charge, or
smallness of fixed charges. Constants need not be uniform as a mass tends
to zero or the number of species tends to infinity.

The exact remaining proof dependency is the independent certification of
the upstream direct/direction/selection chain and the exact multispecies
local/continuation theorem. No unconditional full-resolution claim, full
PDE formalization claim or publication-ready claim follows from these notes.

Focused internal adversarial pass:

- Rechecked the momentum Jacobian and the distinction between `e_b` in
  Maxwell sources and `e_b/m_b` in source acceleration.
- Rechecked the two-species +/- transport and source-acceleration coefficient
  matrices; the source-acceleration coefficients are not the same sign
  matrix as the transport coefficients.
- Rechecked that `alpha_t=(I-alpha tensor alpha)K_a/q_X` adds no second
  receiver charge factor and never divides by charge.
- Rechecked direction/occupation dependency order: direct and baseline
  occupation -> projected signed direction estimate -> enhanced occupation
  -> final pure selection -> weighted signed strict improvement. This is
  conditional on the intended bootstrap, not an additional unsupported
  global estimate.
- Rechecked that source-specific `C(M,A)` in enhanced occupation is absorbed
  only into a common lower threshold for `P`, leaving the selected coefficient
  constants independent of `M,A`.
- Rechecked that finite species sums and the finite disjoint union of compact
  initial supports make all bootstrap constants/continuity quantifiers
  uniform over source and receiver species.

This focused pass is self-review of an extension proof. It does not replace
a fresh independent complete-package adversarial review or the upstream
audit required by the research protocol.
