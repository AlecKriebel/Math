# Narrow release rereview: 10400067

**Disposition: PASS.** This approves the additive release projection only as
an explicitly unresolved five-attempt partial-results packet. It does not
approve a complete solution, a realized knot counterexample, a global
Kricker–Lescop calibration, or a novelty claim.

## Exact projection reviewed

- Directory: `release-projection`, exactly 28 regular files, no symlinks.
- RELEASE_MANIFEST SHA256:
  `e20120caa544e6ca1d9e5b10294f479faff7dde1ec89ec9352b9e61bdaee2573`.
- RELEASE_CHANGE_MAP SHA256:
  `4dcb535d2669c9998d699a8d1f82d08a6edb928783ecca8816f54abededbb5d2`.
- All 27 manifest-listed hashes pass; the manifest's own hash also matches.
- All 18 author files match the frozen packet byte-for-byte.
- All four copied independent-review files match the original audit
  artifacts byte-for-byte.
- The change map accurately describes the six additive release files and
  reports no modifications to frozen files.

## Faithfulness of clarifications

The addendum and reviewed summary correctly distinguish A_n(H)=0 from the
generally false A_n(H/Q_Delta)=0. They retain the exact trefoil-denominator
negative control A_5(H/Q_Delta)=12 and use Q_Delta H^[J] as the numerator
perturbation for the unrestricted fixed-denominator extension. They
explicitly preserve the growing-degree and no-knot-realization limitations.

The PBW/wheeling explanation faithfully includes the zero-framed,
strut-free hypotheses, the connected-output first-Betti-number count, and
the separate sum-versus-average scalar. It does not claim a Lescop scalar
calibration or determine the integral-Blanchfield-class constants.

The reviewed outcome, addendum, guide, and machine-readable manifests all
retain the original unresolved 5/5 disposition. The additions are identified
as review clarifications and packaging, not a sixth substantive attempt.
The exact problem-page access limitation and non-exhaustive interpretation
of literature status remain visible. No new result beyond the earlier
audit's approved clarifications is promoted.

## Portable replay

I copied the entire projection to a fresh temporary directory and ran all
three advertised programs from outside that directory. They reproduced
their expected receipts **byte-for-byte**:

- `verify_core.py`: 1,127 exact assertions.
- `verify_reconstruction.py`: 1,372 exact assertions.
- `replay_independent.py`: 1,513 exact assertions.

The wrapper copies exactly the 18 frozen author files and the unchanged
independent checker into the latter's expected temporary layout. It does
not rely on the original workspace, a source PDF, the omitted raw remote
snapshot, network access, or third-party packages. All eight relative
Markdown links in the three new release documents resolve. The projection
remained unchanged after replay.

## Remaining action

No repair is required by this narrow rereview. The previously stated
restrictions on complete-solution and global-comparison claims continue
to apply. This rereview involved no remote writes and no new source or
construction search.

This is independent AI checking, not human peer review.
