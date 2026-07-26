# Verification

## Current status

The full frozen row is certified excluded.  Its strict aggregate combines
the fixed-divisor verticality theorem, all-vertical top obstruction,
marked-equal lower packages, the frozen thirteen-stratum marked-distinct
taxonomy, uniform and endpoint checks, both discrete `CO` calculations, and
the clean-room post-freeze bridge.

Run

```sh
./verify_full_row_strict.sh
```

The unique final marker is

```text
Q2_E2_A2_B1_D1_N1_FULL_ROW_STRICT_PASS_4D95A1
```

The clean-room bridge has its own dependency-free exact engine and ends
with

```text
AUDIT_BRIDGE_Q2_E2_STRICT_PASS_D9347B
```

These exact checks establish facts about the encoded algebra and coverage
ledger.  They are not peer review.

## Exact SymPy certificate

Run

```sh
/usr/bin/python3 verify_mixed_orbits_sympy.py
```

The script checks:

1. both raw \(36\times26\) degree-seven matrices;
2. explicit nonzero rank minors and complete twelve-vector kernels;
3. the five legal gauge directions and seven normal directions;
4. both degree-six compatibility systems;
5. polynomial left-syzygy certificates for the cube obstructions;
6. the exact resultant \(-250C^9\);
7. every rank-one zero-normal specialization, including
   \(w_4=w_5=0\) and \(w_2=w_3\);
8. the two degree-four product identities on the remaining
   \(w_2-w_3\ne0\) chart; and
9. \(\det L=0\) in every surviving leaf.

Assertions are required.  Running under `python -O` exits with failure.

## Independent hostile backend

Run

```sh
cd audit_hostile
./verify_mixed_orbits_pari_strict.sh
./test_fail_closed.sh
```

The PARI program reconstructs the monomial bases, weighted determinants,
raw kernels, constant-pivot \(E_6\) reductions, polynomial left syzygies,
resultant, specialization charts, and determinant exits without importing
SymPy matrices.  It explicitly clears and retests the apparent
\((C-w_4)^{-1}\) kernel-basis artifact at \(w_4=C\); the two
cross-multiplied residuals there are \(2C^4\) and \(-6C^4\).

The hostile report audits gauge legality, scope, circularity, and every
rank-drop leaf.  The injection tests reject a corrupted raw maximal minor
and a missing terminal attestation.

## Complete row replay

The two triple companions are verified in the sibling packages:

```sh
cd ranktwo_triple
/usr/bin/python3 -u verify_ranktwo_triple_sympy.py
./audit_hostile/verify_ranktwo_triple_pari_strict.sh
./audit_hostile/test_fail_closed.sh

cd ../rankone_triple
./verify_all_strict.sh
```

The rank-one aggregate runs the primary SymPy certificate, two independent
PARI/GP reconstructions, the external hostile \(A=0\) replay, and every
fault-injection guard.  Its hostile audit found a hidden
\(D\ne0,a_3=0\) pivot drop, rebuilt that leaf with an
\(s^8\)-supported pivot, and returned PASS.

Together with the mixed-companion checks above, these commands cover the
two companion orbits for both canonical fixed-divisor pencils.  They
verify the encoded algebra and branch ledger; they are not peer review.
