# Verification

Run the strict independent PARI/GP reconstruction:

```sh
./verify_aopen_pari_strict.sh
```

It reconstructs the weighted Jacobian determinant directly in PARI/GP,
checks the \(A\mapsto1\) scalar normalization, derives the four-factor
cover, recomputes every displayed open chart and rank drop, and requires
all six success markers with no PARI diagnostic.

Run the fail-closed injections:

```sh
./test_fail_closed.sh
```

The guard corrupts the \(s=0\) residual, corrupts both minus-resonance
residuals, and deletes the final completion marker.  All three altered
certificates must be rejected.

The PARI/GP implementation does not import or call the exploratory SymPy
program.  It is therefore a methodologically separate computer-algebra
backend, although both systems verify the same mathematical identities.

These checks are exact evidence about the encoded polynomial algebra.
They are not peer review.
