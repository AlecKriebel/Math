# Verification

Run:

```text
/usr/bin/python3 -u verify_unmarked_triple_sympy.py
cd audit_hostile
./verify_hostile_pari_strict.sh
```

The script reconstructs all coefficient matrices from the full Jacobian
determinant.  It checks the complete raw kernel and legal gauges, exact
left-kernel compatibility, constant maximal minors, complete lower solves,
converses, and the singular-linear exit.

This is exact evidence about the encoded algebra, not peer review.
The independent hostile reconstruction passed.
