# Verification

Run from the repository root:

```sh
python3 dimension_three_keller_degree/monodromy_realizability/verify_status_table.py
```

The dependency-free checker:

1. verifies the preserved SHA-256 of the independent GAP census;
2. checks all 165 action IDs, orbit-stabilizer orders, and the equivalence
   `regular <=> stabilizer order 1 <=> group order equals degree`;
3. checks that the excluded IDs are exactly the regular IDs;
4. checks the symmetric realization in every degree \(3\) through \(10\);
5. checks the additional \(9T31=S_3\wr S_3\) realization, including order
   \(1296\) and point-stabilizer order \(144\); and
6. parses the compact table in `NOTE.md` and verifies every excluded,
   realized, and open entry and count.

The underlying census was independently reproduced with GAP 4.16.0 /
TransGrp 3.6.5 and a separate GAP 4.15.1 build. See
`regular_obstruction/INDEPENDENT_AUDIT.md` and
`regular_obstruction/enumerate_regular_actions_independent.g`.

This is a consistency check for the encoded finite-group ledger. It does not
replace the classical Galois-case theorem, the field-theoretic proof, or peer
review of the cited realization theorems.
