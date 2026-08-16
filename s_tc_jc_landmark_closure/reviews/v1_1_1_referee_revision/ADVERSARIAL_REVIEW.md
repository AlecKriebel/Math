# Adversarial review of the v1.1.1 targeted revision

Status: **VERIFIED AFTER CORRECTION — clean replay required by the release gate**

Two separately run read-only reviews attacked different failure modes after
the first revision pass.  Neither found a counterexample to the central
classification theorem.

## Mathematical review

The reviewer confirmed that componentwise normalization excludes the extra
constant scalar orbit and that the finite target-type selection, physical
sections, triangle contextual gluing, Omega rank argument, and Theta
positive-branch argument are coherent.  It found one literal overstatement in
the generalized finite-cover lemma: a covering set may have ambient dimension
greater than the source germ.  The manuscript now states the precise fact

```text
dim(U intersect Y_tau) = dim(U),
```

and concludes that this intersection has relative interior in `U`.  The same
review requested—and the manuscript now supplies—a smooth-image preimage
condition and the generic-rank formulation for the marginal map.  It also
caused the complete-factor definition to move before first use and clarified
the pendant-one Omega gauge.

## Release and mutation review

The release reviewer confirmed that the new title is synchronized, the two
PDFs render cleanly, and Figure 2 has visible clearance.  It correctly found
that the first review snapshot still had stale v1.1.0 hashes, envelope,
transcripts, PDF audit, and source ZIP.  Those are release-order findings, not
mathematical failures: v1.1.1 is sealed only after the final source rebuild,
two-renderer audit, metadata reseal, immutable commit, and three clean replay
commands.

The reviewer also broke the first syntactic regression by moving a graph node
while leaving the theta label fixed and by hiding a required phrase in a TeX
comment.  The active regression now strips comments, measures actual
node-to-label clearance, reads both embedded PDF titles, checks bioRxiv and
JSON titles, and rejects eight targeted mutations.  It is invoked by both the
quick and all-record-regeneration entry points.

## Final mathematical disposition

- **No central falsification found.**
- **Bridge normalization:** verified after correction.
- **Finite-union handoff:** verified after correction.
- **Marginal smooth-stratum rank:** verified after correction.
- **Triangle contextual gluing:** verified after correction.
- **Genericity handoff:** verified after correction.
- **Figure 2:** corrected and subjected to geometric regression.

The immutable release status is determined separately by the clean replay
transcripts and external release envelope; this report does not substitute
for those machine gates and does not claim independent human review.

After the corrections above, the mathematical reviewer performed a bounded
recheck of exactly the finite-cover, smooth-stratum, complete-factor, and
Omega-gauge edits and returned **PASS with no remaining defect**.
