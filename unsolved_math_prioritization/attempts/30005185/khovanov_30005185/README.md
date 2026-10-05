# Modulo-four reduced Khovanov rank of ribbon knots

Target: **30005185 / OWR-11101915-009**. Checked 2026-10-05 UTC.

**Outcome: unresolved.** This package does not prove or refute the universal conjecture. Five bounded approaches recover a useful exact obstruction: in characteristic different from two, the missing condition is an even number of even-exponent elementary torsion factors in the lifted Lee complex of a ribbon knot. Neither a split unknot summand nor the determinant-square condition forces this parity.

- [Proofs and precise gap](PROOFS.md)
- [Five approaches and stopping conditions](APPROACHES.md)
- [Source metadata and inspection scope](SOURCE_VERIFICATION.json)
- [Limitations](LIMITATIONS.md)
- [Exact knot rank controls](KNOT_CHECKS.json)
- [Algebra regression controls](ALGEBRA_CHECKS.json)

Run with Python 3's standard library:

    python cube_verify.py
    python verify_algebra.py
    python verify_manifest.py

The cube calculation recomputes total reduced ranks over Q, F2, F3 and F5 for six explicit examples: unknot 1, two trefoil chiralities 3, stevedore 9, square knot 9, and the nonslice negative control 6_2 of rank 11. It checks the integral identity d²=0 before taking ranks. It does not decide ribbonness. Algebra checks cover 37,449 graded normal forms, 20,736 universal-coefficient cases, and 500 odd squares; they support separately supplied proofs and are not a finite-census argument.

No novelty is claimed. Published and preprint theorems retain their attribution. A separate, previously uninvolved audit is required before publication; this authored freeze does not itself provide one.
