# Verification record

**Recorded:** 2026-07-25T07:18:00Z.

The theorem is encoded independently in SymPy and PARI/GP.

## Commands

```text
/usr/bin/python3 -u verify_unmarked_infinity_sympy.py
./verify_unmarked_infinity_pari_strict.sh
./test_fail_closed.sh
./audit_hostile/verify_hostile_strict.sh
./audit_hostile/test_hostile_fail_closed.sh
```

## Exact checks

The SymPy certificate reconstructs:

- \(\operatorname{Jac}(P,Q,R)=0\);
- the compact degree-seven identity;
- raw \(E_7\) rank \(18\) and constant maximal minor
  \(1709960483517235200\);
- the complete eight-dimensional kernel, independence minor \(-8\), and the
  third-translation relation;
- the \(28\times10\) degree-six system, its constant forcing minor
  \(4831838208\), its unique zero solution, and the converse substitution;
- four exact degree-five coefficients forcing the last two columns of \(L\)
  to vanish.

PARI/GP rebuilds the same objects directly from the full Jacobian determinant.
The strict wrapper accepts only its exact success sentinel.

The fail-closed harness verifies:

- optimized Python is rejected;
- a forged SymPy maximal minor is rejected;
- a forged PARI forcing minor is rejected;
- the strict baseline succeeds; and
- a forged extra PARI diagnostic is rejected.

## Hostile reconstruction

At 2026-07-25T10:00:00Z, the dependency-free verifier in
`audit_hostile/` independently rebuilt sparse polynomial arithmetic over
`fractions.Fraction`. It confirmed the full determinant, the raw
rank-\(18\)/nullity-\(8\) sandwich, all kernel and gauge directions, the
constant rank-ten \(E_6\) system and converse, and the full specialized
\(E_5\) exit. It imports neither SymPy nor PARI/GP.

The hostile strict runner whitelists its complete transcript. Mutations of
the raw minor, \(E_6\) minor, \(E_5\) literal, and completion marker are all
rejected, and the verifier remains active under optimized Python.

## Independence and limitations

SymPy and PARI/GP are independent implementations, but both use exact
coefficient matrices. They are not methodologically independent mathematical
proofs. The human-readable proof in `NOTE.md` supplies the structural kernel
and gauge argument.

The artifacts were developed with AI assistance. They have not been peer
reviewed. Exact execution is evidence about the encoded identities and is not
peer review.
