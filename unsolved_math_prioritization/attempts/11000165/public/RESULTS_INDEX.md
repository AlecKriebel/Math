# Results and evidence index

## Complete proofs

- [Closed genus-two generators](pass1_genus_two/GENUS_TWO_GENERATORS.md): theta system, unimodular section, ordinary-generation proof.
- [Closed higher-genus Johnson generators](pass1_constructive/CONSTRUCTIVE_JOHNSON_GENERATORS.md): ambient alphabet, all monomial lifts, primitive quotient basis, unrestricted family, telescoping proof.
- [Outer-action obstruction](pass1_johnson_obstruction/PROOF.md): explicit free-group commutator, all-power non-innerness, infinite-index strengthening.

## Acceptance reports

- [Final combined adversarial audit](pass1_audit/AUDIT.md) and [branch verdicts](pass1_audit/RESULT.json).
- [Closed transfer and source acceptance](pass1_closed_transfer/SOURCE_ACCEPTANCE_REPORT.md) and [verdict](pass1_closed_transfer/RESULT.json).
- [Independent exact-formula audit](pass1_exact_validation/AUDIT.md) and [original acceptance manifest, public projection](pass1_exact_validation/MANIFEST.json).

## Executable evidence

- [Principal exact checker](pass1_exact_validation/verify_exact_formulas.py): 62,840 checks; universal genus-two polynomial identities, free-word checks through rank 13 and powers ±20, quotient/monomial checks through genus 10.
- [Constructive checker](pass1_constructive/verify_lattice.py): all lift identities, integer reduction, and elementary parabolic preservation for genera 3–8.
- [Genus-two checker](pass1_genus_two/verify_homology.py): standard-library universal identities and 121 integer samples.
- [Free-group checker](pass1_johnson_obstruction/verify_free_group.py): ranks 3–12 and powers ±12.
- [Independent outer-commutator checker](pass1_audit/check_outer_commutator.py): a second partial-conjugation pair, ranks 3,4,8 and positive powers 1–19.
- [Independent lattice checker](pass1_audit/check_integral_lattice.py): exterior lifts and unit-pivot structure for genera 3–8.
- [Independent quotient checker](pass1_closed_transfer/verify_integral_quotient.py): integral quotient structure for genera 2–12; genus-two arithmetic does not transfer Omori's theorem to g=2.

## Integrity and replay

- [File identities](ORIGINAL_IDENTITIES.json), [acceptance bindings](AUDIT_BINDINGS.json), [exact public manifest](MANIFEST.json).
- [Replay receipt](CHECK_REPLAY.json), [negative/tamper receipt](TAMPER_CONTROLS.json).
- [Verification instructions and trust limits](REPRODUCIBILITY.md).
