# Consistent Noisy Single-Index Regression

Problem 30003790 / OWR-16161-003; rank 618 at intake.

**Disposition: unsolved.** This packet preserves a scope distinction rather
than claiming the source's high-dimensional objective has been settled.

`RESULT.md` proves a sample-split, vanishing-Euclidean-guard modification is
consistent at fixed ambient dimension under an explicit lower-mass design
condition and Hölder regularity. Its statistical bound depends adversely on
dimension. It also gives exact raw-slice tangent-error floors, a known-noise
deconvolution result and a pilot-localization lemma. Five distinct routes and
their remaining gaps are recorded in `APPROACH_LOG.md` and `turns.json`.

The inspected August 2026 JMLR follow-up still retains a geometry/noise
saturation term. Neither that upper bound nor our restricted tangent lower
bound is a general impossibility theorem. No global literature-completeness
or novelty claim is made.

Run `python3 verification/check.py` to reproduce the deterministic controls;
compare its JSON output with `verification/result.json`. These controls do not
certify the unresolved high-dimensional statement. The author packet is frozen
for independent review. Full source documents are not included.
