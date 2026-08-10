> **Superseded semantic wording.** This point-in-time review is preserved
> verbatim below except for this notice. A later clean-room review showed that
> its phrase “matches direct graph `S_TC`” is valid only for retention of the
> original primitive core. It is not an intrinsic `S_TC` test after arbitrary
> `red_*`; omitting a cycle sink can reduce to a strong tree. The active v2
> certificate and `SELECTED_STRENGTH_CORRECTION.md` enforce the narrower claim.

**Ranked Findings**

1. **High: corrected certificate artifacts are not present in current `certificates/`.**  
   [certificates/manifest.json](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/certificates/manifest.json:19) still has manifest hash `16e151...f333`, the hash identified as pre-correction in [SELECTED_STRENGTH_CORRECTION.md](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/SELECTED_STRENGTH_CORRECTION.md:7). It has no `selected_restriction_audit` or `preserved_selected_strength_failure`, and no `certificates/*selected*` files are readable. This contradicts the preservation path claimed in [PRECORRECTION_FAILURE.md](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/PRECORRECTION_FAILURE.md:18). Source regeneration code would write the right artifacts at [build_atlas.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/build_atlas.py:163), but the present certificate directory is stale.

2. **Low: count table is target-row convention, not all repair-choice rows or full decorated relations.**  
   The published totals match the cycle-collapsed completion target convention in [selected_restrictions.py](/Users/alec/Documents/Math-stc-jc-final-repair/s_tc_jc_landmark_closure/independent/decorated_atlas/selected_restrictions.py:324). If every minimum repair choice were counted separately, totals would be `838, 1992, 4166, 7922`, not `831, 1983, 4155, 7909`. This is not a counterexample, but the row type should stay explicit.

**Independent Audit Results**

I did not import or execute `selected_restrictions.py`. A stdlib-only scratch enumeration found exactly five contracted cores: one cycle and four theta. Minimum repair-size multiset: `1, 1, 2, 2, 2`.

The selected-strength predicate matches direct graph `S_TC`: all sink ports selected plus selected ordinary occupancy containing a minimum repair. Mismatches found: `0`. False-strong under the dummy rule: `0`.

The dummy counterexample is real: theta core, selected sink mask `1`, selected ordinary counts `(0,0,1,0,1)`, chosen repair `(2,3)`, dummy segment `3`, while selected occupancy already contains repair `(2,4)`.

Completion buckets confirmed:

| selected | total | old strong | new strong | promoted | new weak |
|---:|---:|---:|---:|---:|---:|
| 3 | 831 | 9 | 15 | 6 | 816 |
| 4 | 1983 | 40 | 78 | 38 | 1905 |
| 5 | 4155 | 131 | 257 | 126 | 3898 |
| 6 | 7909 | 342 | 652 | 310 | 7257 |

Fully selected primitive ordinary-`T` relation counts remain `18, 192, 1800, 17280` for ports `4..7`; I found no reason for them to change.

**Verdict: ACCEPT_WITH_LIMITATION**

I accept the mathematical/source-level correction. I do not accept the current `certificates/` directory as a corrected release artifact until it is regenerated and bound to the selected audit and preserved-failure files.
