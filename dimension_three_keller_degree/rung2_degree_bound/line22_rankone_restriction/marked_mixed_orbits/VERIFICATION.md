# Verification

Run:

```text
/usr/bin/python3 -u verify_marked_mixed_sympy.py
cd audit_hostile
./verify_marked_mixed_pari_strict.sh
./test_fail_closed.sh
```

The script reconstructs both raw coefficient systems, complete kernels and
legal gauges, parameter-free lower maximal minors, exact row reductions,
full converses, and the singular-linear exits.

This exact check is evidence about the encoded algebra, not peer review.
The independent hostile reconstruction passed, including explicit \(d=0\)
reruns.
