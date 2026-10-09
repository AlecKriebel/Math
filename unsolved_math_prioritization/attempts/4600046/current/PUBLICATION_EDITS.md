# Public proof preparation

The current REPORT.md preserves every mathematical definition, theorem, proof, qualification and residual gap from the corrected restricted-results report. The empty-routing-set convention is the sole mathematical repair, shown in CORRECTION.patch.

Publication-only prose edits remove nonmathematical authoring and bookkeeping details, replace pre-audit status language with the recorded restricted acceptance, and identify the original author diagnostic as historical and excluded. Those edits do not consume a proof-search route. The omitted details are not repeated in a public deletion diff. The complete independent AUDIT_REPORT.md is byte-preserved.

The exact mathematical correction patch was applied to a local staging copy with zero fuzz and no offset before these editorial edits. The public correction verifier independently checks the unique seven-line mathematical context within the current proof, reverses and reapplies its one radius substitution in memory, and requires exact recovery of the current proof. It performs no source-file writes and does not require or replay the omitted full original report. Historical line numbers in CORRECTION.patch refer to the pre-editorial report.

The two verifier adaptation patches document public-path/pin and correction-replay adaptations. They contain authored verification code and generic historical packet filenames only; they do not contain excluded input manifests, source bodies, dataset contents, private source names, or coordination material. No mathematical solver in verify_partials.py was changed.
