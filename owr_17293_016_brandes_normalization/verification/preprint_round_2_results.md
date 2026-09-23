# Additional exact checks from fresh review round 2

Run `python3 verification/preprint_round_2_checks.py` to reproduce this output. The supplementary coefficient typo was corrected before this run.

```text
nonconvex delta=1e-1 PASS 5 classes, 3 slices
nonconvex delta=1e-8 PASS 5 classes, 3 slices
nonconvex delta=1e-80 PASS 5 classes, 3 slices
degenerate minimum lambda=0 PASS 5 classes, 3 slices
degenerate minimum lambda=1/10000000000000000000000000000000000000000 PASS 5 classes, 3 slices
degenerate minimum lambda=10000000000000000000000000000000000000000 PASS 5 classes, 3 slices
anisotropic quadratic lambda=1e80 PASS 3 classes, 1 slices
fixed-perturbation negative controls PASS
excluded nonnegative endpoint PASS
```
