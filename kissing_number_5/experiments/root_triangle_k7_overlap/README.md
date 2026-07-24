# Root-triangle K7 overlap audit

This interrupted lane tested whether a degree-three rooted-triangle moment
inequality could turn local rank-five `K7` data into a global obstruction.

## What is exact

- `root_triangle_degree3_catalog_dual.json` and
  `verify_exact_catalog_dual.py` certify an exact dual on one finite
  1,782-atom catalog.
- `catalog_dual_counteratom.json` and `verify_dual_counteratom.py` certify an
  exact rank-five quarter-grid `K7` atom outside that catalog with negative
  dual slack.  Thus the finite-catalog dual is not universal.
- `centered_degree3_radical.json` and
  `verify_centered_degree3_radical_symbolic.py` certify the completed part of
  the centered radical calculation.

Run from `kissing_number_5/`:

```sh
python3 experiments/root_triangle_k7_overlap/verify_exact_catalog_dual.py
python3 experiments/root_triangle_k7_overlap/independent_catalog_dual_audit.py
python3 experiments/root_triangle_k7_overlap/verify_dual_counteratom.py
python3 experiments/root_triangle_k7_overlap/test_centered_degree3_radical.py
```

## What is not proved

The catalog is not a complete classification of continuous rank-five `K7`
atoms, and this directory proves no kissing-number upper bound.  The
degree-three radical reduction was incomplete when the workstream paused.

Large `.npz` moment tables are regenerable discovery caches and are excluded
from Git.  They remain in the local safety archive described in
`../../RESUME.md`; the generators and the smaller exact artifacts are kept
here.
