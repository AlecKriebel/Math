# Verification

The supplied checks and independent hostile audit passed at
2026-07-25T07:01:00Z.

Run from this directory:

```sh
/usr/bin/python3 verify_line22_outer_infinity_remaining_sympy.py
./verify_line22_outer_infinity_remaining_pari_strict.sh
./test_fail_closed.sh
```

The SymPy certificate reconstructs the raw \(E_7\) coefficient matrices,
their exact maximal minors and kernels, and the complete lower
coefficient reductions.  The PARI/GP certificate instead expands the
single generating determinant
\[
\det(L+T\,JH_2+T^2JH_3+T^3JH_4)
\]
for each solved normal form and checks the relevant \(T\)-coefficients
directly.

The strict wrapper fails on GP diagnostics, a nonzero process status, or
any output other than the exact success sentinel.  The guard test also
confirms that the Python verifier refuses optimized mode.
