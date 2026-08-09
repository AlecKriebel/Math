# Source-author review packet

This is a technical comparison document, not an email or request for
endorsement.

## One-page theorem comparison

| Topic | Originating paper (arXiv:2606.21362v3) | Merged conclusion |
|---|---|---|
| First reduced operator | Defined; canonical strategy and lower bound | Same operator convention |
| First exact value | Conjectured (2\csc(\pi/(2d))) | Proved for (q,qa,qc) |
| First augmentation | Defined; printed conjecture has a localized normalization discrepancy | Operator-defined value (2\csc(\pi/(2d))+1) |
| Second reduced operator | Defined and SOS-proved with value (d) | SOS rechecked; commuting reading made explicit |
| Second augmentation | Defined, with convention variations between main text and appendix | Hermitian main-SOS convention; dagger version handled by Bob inversion |
| Canonical strategies | Supplied | Reverified exactly; full-behavior numerics not challenged |
| Equality/uniqueness | Symmetry and selected self-testing arguments | Sufficient paired phase-permutation family; no full-face classification |
| Maximal randomness | Numerical analysis fixes the canonical full distribution; maximal-violation interpretation also discussed | Scalar maximum alone is insufficient for (d\ge4); fixed canonical behavior remains a different question |

## Normalization convention

The merged paper treats the displayed Hermitian operator definitions as
authoritative. For the first family this gives reduced value
(M_d=2\csc(\pi/(2d))) and augmented value (M_d+1), consistent with the
source's reduced equation and stated (d=3) augmented value. The isolated
extra (d) in the printed augmented conjecture is described neutrally as a
normalization/typographical inconsistency.

For the second family, the merged paper follows the main-text/SOS convention
with (B_y) and the corrected v3 prefactor (1/(2d)). The appendix convention
with (B_y^\dagger) is exactly Bob outcome inversion and preserves the
maximum and guessing probability.

## Bell value versus full behavior

The full-behavior numerical program constrains every canonical probability
before optimizing Eve. The counterexample constrains only the scalar Bell
maximum (indeed it preserves the full first-harmonic correlator matrix), but
has different higher Fourier data. It is therefore consistent for the
canonical full-behavior problem to return (1/d^2) while the worst case over
the scalar maximizing face is larger.

## Three proof points most worth checking

1. **Polar support and commuting model.** Verify that
   (P=|C^\dagger|^{1/2}-V|C|^{1/2}B) expands to the stated gap for the
   canonical partial isometry, and that (V\in W^*(C)) preserves
   cross-party commutation.
2. **Paired phase admissibility.** Verify the two product-one identities and
   that the same permutation must be applied to the relative roots and every
   polar-phase row. Mismatched permutations fail the hostile control.
3. **Second-family Fourier compression.** Verify
   (\widehat B_\ell=d\lambda_\ell D_\ell), (D_\ell^d=I), Alice's
   conjugation, and annihilation of every corrected source SOS factor.

## Source claim to merged conclusion

| Source item | Merged treatment |
|---|---|
| Family definitions | Adopted and credited |
| Canonical lower strategies | Adopted, credited, exactly rechecked |
| First-value conjecture | Proved, including (qc) |
| Second-family SOS | Adopted with corrected v3 normalization and credited |
| Fixed-canonical-behavior numerical randomness | Explicitly not contradicted |
| Uniqueness-based scalar interpretation | Obstructed by exact alternate maximizers for (d\ge4) |
| (d=3) second-family self-test | Explicitly outside the counterexample dimension |

## Possible collaborative extensions

- Classify the complete maximizing faces, including reducible and
  commuting-operator representations.
- Determine the exact worst-case guessing probability at the scalar maximum.
- Resolve (d=2,3) for the first augmented family.
- Classify permutation orders up to local isometries and output relabelings.
- Add a small set of higher Fourier terms that restores value rigidity.
- Prove robust self-testing or randomness for a modified low-setting family.

## Shortest exact replay

```sh
cd cyclic_bell_exact_values_and_randomness
python3 verification/verify_merged.py
python3 ../cyclic_randomness_counterexample/verify_exact.py
python3 ../minimum_bell_randomness/verify_second_family_d4_exact.py
```

The theorem-to-artifact map gives precise manuscript and verifier locations.
