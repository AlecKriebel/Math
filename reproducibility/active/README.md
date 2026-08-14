# Active reproducibility package

The active mathematical package is rooted at
`s_tc_jc_landmark_closure/`, with the independently audited triangle-free
sharpness input at `omega_audit/` and the frozen triangle-containing
sharpness input at `s_tc_jc_sharp_boundary/`.

The only supported entry points are:

```bash
bash reproducibility/verify_quick.sh
bash reproducibility/verify_full.sh
bash reproducibility/verify_regenerate_all.sh
```

The active status, outcome, dependency graph, crosswalk, and release metadata
are the five authoritative files in `s_tc_jc_landmark_closure/`. All rejected
or superseded release surfaces are excluded from active verifier inputs.
