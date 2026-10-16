# Review03 reproduction and custody

Read REPORT.md and VERDICT.json for the exact finding and remaining scope. SIX_IDENTITIES.json binds the six frozen candidate files; FINAL_SIX_PRESERVATION.json rechecks them after substantive review. PRIMARY_RETRIEVALS.json, VERSION_RETRIEVALS.json and SOURCE_READING.md identify actual primary bytes/pages without redistributing third-party bodies. ALL_MEMBERS.json and CONTENT_INSPECTION_LEDGER.json cover all123source members.

This packet's custody is portable. Supply the final manifest SHA256 from the handoff outside the packet:

    python3 -B verify_custody.py --manifest-sha256 EXTERNAL_SHA256
    python3 -B -O verify_custody.py --manifest-sha256 EXTERNAL_SHA256

The verifier checks every recursive file, including hidden files, except only root MANIFEST.json. Symlinks, special files, missing/extra/altered files and empty directories fail. It requires neither original absolute paths nor file mtimes. The external digest authenticates the manifest; a freely rewritten self-manifest is not authentication. Run with-B to prevent new bytecode files.

The independent finite checks are standalone, standard-library Python:

    python3 -B independent_math.py
    python3 -B -O independent_math.py

They reproduce the48/16/32counts,32symmetry transforms,32shuffled separated-start controls n2–9 and the explicit event transport. Compare output to INDEPENDENT_MATH.json; INDEPENDENT_MATH_OPTIMIZED.json is byte-identical. Finite controls do not replace the all-n proof or source interpretation.

To reproduce this packet's physical custody self-controls, provide an owned scratch directory in TMPDIR on a POSIX filesystem supporting symlinks and FIFOs:

    python3 -B custody_controls.py
    python3 -B -O custody_controls.py

These controls create and remove only their TemporaryDirectory fixture. The captured normal/optimized results are in CUSTODY_CONTROLS_NORMAL.json and CUSTODY_CONTROLS_OPTIMIZED.json. Final actual manifest verification results are reported externally after sealing, avoiding circular self-inventory.

For full candidate replay, extract the exact released source-and-verification.zip into an empty directory and follow its README with the exact released PDF. Four complete execution outputs, actual runtime versions/commands and hashes are preserved here. PHYSICAL_AND_REBUILD_RESULTS.json records four same-six portable relocated rebuilds and64physical negatives. ORIGINAL_PUBLICATION_CONTROLS.json records the additionally run36original wrapper controls in each outer mode.

run_replays.py and package_controls.py preserve the exact environment-specific harnesses used in this review. They expect their canonical position under review_preprint03 within the audit root, the pre-existing root-owned RAM mount at preprint/tmp, and this review's own extracted source at preprint/tmp/review03-work/extracted. They are execution evidence, not standalone portable-source verifiers. No mounted image should be created, detached or reformatted to run the portable custody/finite checks above.

Only authored compact review evidence is included. Full primary bodies, page images, extracted candidate files and physical test fixtures are transient and excluded. No frozen candidate/history file, Git state, PR, release, DOI, external account or individual was changed or contacted by this reviewer.
