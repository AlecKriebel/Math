# Release-lane cross-review of the root referee report

Date: 2026-09-07T04:02:14.451556+00:00

Reviewed root report SHA-256: `c0f6a30dfe4a38a52ef7d1afbf2469253484dcb31e567bf78627ad41a27f779f`.

**No required substantive correction within the release-audit scope.** The final report accurately distinguishes correct canonical preprint artifacts from the journal layout/build-gate defect, and it does not turn the journal finding into a theorem or physical-page-clipping claim.

Checked against retained evidence, without rerunning broad suites:

- The target commit and remote annotated-tag dereference agree. All nine downloaded assets passed both comparisons stated in the report.
- The source inventory contains 1,651 files totaling 22,425,118 bytes. The report's archive SHA-256 agrees with the independently created release-lane git archive. Manifest counts 1,650, 214, and 216 are correct and refer to distinct scopes.
- The 39 tests, 39 normal verifiers, 39 optimized rejections, complete symbolic suite, minimal replay, full portable replay, seven byte-identical regenerated ZIPs, three detached builds, and six matching PDF text streams are accurately reported. Compilation success is appropriately qualified by J1.
- All five journal warning magnitudes, source locations, and page numbers agree with the actual clean-build logs. The four large margin incursions are supported by the preserved word coordinates. The 1.66727-point case is properly qualified as small, and the contrast-table inclusion line 1101 is correct.
- Canonical bioRxiv and arXiv final logs have zero occurrences of the selected warning pattern. The journal-only synthetic failure control supplements, rather than replaces, evidence of the five shipped warnings.
- The canonical-only log-check limitation and proposed shared checks before copying journal/cover PDFs accurately reflect the scripts. The current cover is not alleged to have an observed warning.
- The wrong-toolchain, poisoned-PDF regeneration, and two manifest negative-control outcomes are stated fairly. The unavailable five-archive route is expressly not counted as a completed replay, and its preserved log sentinel is described correctly.
- No claim is made that Google Drive, submission portals, or server-side TeX environments were checked.

One optional wording precision: in the release-verification paragraph, replace **“forged replacement manifest”** with **“forged self-consistency manifest”**. The retained control forged the replay-side manifest and showed it cannot override the unchanged shipped baseline. It did not demonstrate authentication of an attacker-replaced baseline manifest. Other paragraphs already make the immutable-baseline boundary clear, so this is a precision edit rather than a change to the verdict.

This cross-review does not independently certify the other lanes' mathematical counts or the DataCite lookup; those lie outside the assigned release-evidence check. No source or Git changes were made.
