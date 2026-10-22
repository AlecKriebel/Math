# Bounded-delta acceptance of the repaired parameter-hair proof

Problem 5300062 / AMR-052-0062. Date: 2026-10-05.

## Current verdict

**ACCEPT_SCOPED_PARTIAL_V2.** The actual v2 freeze incorporates exactly the
three mandatory mathematical replacements requested by the original independent
audit. The repaired proof establishes the scoped C-infinity interior conclusion,
relative to its explicitly credited dynamic-ray construction, simple-root and
nonvanishing-derivative inputs.

The complete problem remains **UNSOLVED, 5/5 approaches**. This acceptance does
not assert geometric real analyticity, endpoint regularity, landing of all rays,
a transfer of fixed-map dynamic nonanalyticity to parameter hairs, novelty, or
human peer review.

Acceptance applies to this exact tuple:

- Author v2 ZIP SHA256: ae94bc32d7727c371299ceefaeea99652ffb0dbee8897af386d1e51cd3012d49
- Author v2 ZIP bytes: 19,862
- Author v2 manifest SHA256: 850d3808cbe93e1c5ef2442cc4cafd60c9bec9bf586a2bee07c28553729d1ec8
- Revised REPORT.md SHA256: 6cdd4a0449328a245e4e210d765823366cca908aa2460c74dd028431e8bc81ae

The complete original independent audit remains part of the evidence. Its
historical REPAIR_REQUIRED_V1 verdict is not rewritten. This separately dated
acceptance closes that repair for the exact v2 identified above.

## Mathematical delta

The only mathematical-text changes are the mandatory replacements on REPORT.md
lines 68, 75 and 146. The complete report matches the previously supplied target
hash, and the included patch is byte-identical to the original audit's patch.

1. The working tail now satisfies

       a>max{x_0+2 log(K+3),K+6}, b+eta<F(a).

   Since the address bound gives t_s^*<=x_0, this explicitly meets the threshold
   t>t_s^*+2 log(K+3) used in [Foerster-Schleicher, Lemma 4.4](https://arxiv.org/abs/math/0505097).
   That resolves the missing identification hypothesis. Strengthening a does
   not impair the subsequent right-half-plane, shrinking-disk, branch or
   all-order summability estimates.

2. The approximant-identification sentence now states that implication and
   cites Lemma 4.4 specifically. It no longer invokes that convergence input
   without meeting its stated sufficient condition.

3. The low-potential step now chooses N with

       F^N(inf J)>max{F^N(u)+2 log(K+3),K+6}, F^N(u)>=2.

   Here inf J>u>0. Both iterates eventually exceed 2, after which their
   difference grows at least geometrically because F'>2 there. Consequently
   the additional fixed gap 2 log(K+3) can always be obtained. With
   x_0=F^N(u) and a=F^N(inf J), the repaired tail assumptions hold. Subsequent
   shrinking of J preserves those strict inequalities, and its width can
   still be chosen to satisfy b+eta<F(a).

The shift still works for every exponentially bounded address, including
unbounded ones, because the original proof uses a strict interior potential
margin and an eventual bound for every subsequent address entry. The finite
inverse pullback and smooth implicit-function step are unchanged. No new
claim about t=t_s or a common complex-potential disk has been introduced.

## Exact scope and replay results

Of the original archive's files, only REPORT.md and the regenerated manifest
changed. All six other original payload files are byte-identical: README.md,
RESULTS.json, SOURCE_VERIFICATION.json, code/check_controls.py,
results/controls.json and verify.py. The only additions are the exact mandatory
patch and DELTA_PROVENANCE.json. The latter's original bindings, corrected
report binding, three line changes and unchanged-file metadata were checked.

The original author, actual v2 and original audit ZIPs were each authenticated
against their independently supplied byte counts and SHA256 hashes, inspected
against their strict manifests, extracted into separate disposable directories,
and replayed with their external manifest anchors. All passed. The original
and v2 author controls reproduced exact retained bytes; the prior audit's
independent 480 exact-jet checks, 297 numerical controls and 12 branch traps
also reproduced exact retained bytes. These finite controls are not a formal
proof of the analytic theorem.

The author v2 intentionally preserves historical pending-audit labels and the
original source metadata's unperformed-review-hash flag. They describe the
author freeze's history; they are not this acceptance's current verdict. The
original independent audit separately records the successful full corpus and
review-hash recomputation. No historical file needs to be edited to reconcile
these distinct stages.

Both historical freezes and their safe directories were preserved. This
acceptance contains no source PDFs, source extracts, page images, raw corpus
records, raw repository snapshots or private coordination files. No remote
write was performed. See results/delta_checks.json and the replay instructions
in README.md for the exact machine-readable bindings.
