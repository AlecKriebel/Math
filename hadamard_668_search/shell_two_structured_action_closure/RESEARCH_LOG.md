# Research log: shell-two structured action closure

## 2026-07-24

### Scope defect identified

An adversarial audit found that the structured family laws depend on the
chosen class coordinates, while the earlier certificate evaluated only one
canonical representative from each of the five shell-two profile orbits.
The 24-element profile action therefore could not be used to claim that the
families had been tested on every labelled image.

The exact action expansion contains 84 images with source-orbit sizes
`24, 12, 12, 12, 24`.  A new folder was created so that the frozen v1
auditors and their existing certificates remained untouched.

### V1 diagnostic interrupted

The first implementation began an 84-image run and exposed digit-two hits
on noncanonical images.  During review, the aggregation was strengthened
to retain both raw occurrence counts and safe equivalence-class counts,
and to report witness-level multiplier-supergroup membership.  That run
was stopped after 47 complete images.  Its ignored `output/production`
directory is a superseded diagnostic and is not evidence for the final
claim.

No old result was deleted or silently overwritten.

### V2 certificate design

The v2 schema pins:

- the sorted 84-image action manifest and its semantic digest;
- the exact action element attached to every image;
- a transitive closure of 22 local Python sources, including the runner and
  verifier themselves;
- one atomic semantic record per image;
- exact coverage histograms and retained survivor records;
- direct replay through lambda digit three for every digit-two survivor.

The three structured families call the frozen
`verify_structured_phase_families.py` implementation directly.  The F27
lane calls the frozen 56-submodule construction and all 3,136 asymmetric
submodule pairs per image directly.

Only the proved common `C6` class-rotation action is used for lifted-witness
deduplication.  All six rotations are replayed exactly.  Independent star
images are not collapsed because a full labelled-placement action
compatible with the fixed zero-column slice was not established here.

### Authoritative run completed

At 2026-07-24 23:34 PDT, the single-process v2 run completed all 84 images.
It enumerated 5,900,019 attained first-digit placements across the four
families:

- 72,900 in `opposite_planar_c3_envelope`;
- 3,542,940 in `opposite_twisted_c6`;
- 2,278,854 in `opposite_helical_c4`;
- 5,325 in the F27 minimal-submodule union.

The exact result was five raw digit-two survivors, all in
`opposite_helical_c4`.  They are also five distinct `C6` rotation classes.
Their digit-three defect counts are `5, 6, 7, 8, 12`.  All five are fixed
by minimal proper multiplier supergroup `8`; none is
proper-supergroup-free.  No F27, planar, or twisted survivor reached digit
two.

No digit-two survivor reached lambda digit three.  The consecutive-lift
gate therefore failed, and the five digit-two witnesses are explicitly not
counted as gate progress.

The production run consumed 555.84 summed image seconds.  Median image time
was 6.28 seconds, the slowest image was 17.22 seconds under concurrent
machine load, and peak resident memory was approximately 36.4 MB.

### Independent verification

Both strict verification modes passed:

```text
images=84 d2_raw=5 d2_c6_unique=5 d3=0
semantic_sha256=e5a27d107a5e2f140feabb3a69a02c16044980a05baaa1523fafff3ef9d0d802
status=PASS
```

The default verifier reconstructed the manifest and source closure,
validated the embedded certificate and every retained survivor, and
reaggregated all counts.  The live verifier additionally required the
exact 84-file production output set and compared it with the tracked
certificate.  The full verifier then recomputed every family enumeration
on all 84 images and matched every semantic record; all 84 full-replay
checkpoints passed.

### Interpretation

The action closure corrects a real scope gap and gives an exact negative
result for four structured lanes.  The five helical digit-two points show
that representative-only testing can miss structured hits, but their
proper-supergroup fixation and immediate digit-three failure make them
poor evidence of convergence.  This milestone is useful as a rigorous
appendix or supporting computational result, not as a standalone
Hadamard-order breakthrough.
