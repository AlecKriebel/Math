# Verification

Run:

```text
/usr/bin/python3 verify_top_obstruction_sympy.py
cd audit_hostile
./audit_exact_pari_strict.sh
/usr/bin/python3 -u audit_reconstruct_mod101.py
./test_audit_guards.sh
```

The exact SymPy and PARI reconstructions check the determinant reductions,
normal forms, canonical kernels, zero-kernel samples, and sharpness
witnesses.  The dependency-free modular implementation supplies independent
rank-minor evidence in characteristic \(101\); its exhaustive samples are
stress tests and are not the universal proof.

The audit rejected characteristics \(5\) and \(11\), where inseparability
or accidental rank drops produce spurious kernels.  All retained runners
fail closed under the injected faults.

These checks are evidence about the encoded algebra, not peer review.
