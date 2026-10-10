# Truncated Hadamard simplices: prior-proof audit

Read `AUDIT.md` for the mathematical conclusion: credited partial prior resolution, with the full normality classification retained. The audit accepts the seventeen written arguments, including the affine-lattice conventions and smoothness resonance correction. It makes no novelty or Lean-build claim.

- `SOURCE_METADATA.json`: primary-source identifiers, public URLs, hashes, byte counts and inspection history. No source bodies.
- `STATIC_FORMAL_INSPECTION.json`: official ancillary provenance, declaration locations, dependency pins and static hypothesis/target checks. No downloaded code is included or executed.
- `independent_exact_checks.py` and `EXACT_CHECK_RESULTS.json`: independently authored standard-library exact finite diagnostics. Every condition remains enforced under Python optimization. These tests do not prove the infinite-parameter theorems.
- `AUDIT_MANIFEST.json`: hashes and sizes of the seven stable authored payload files. The manifest excludes itself and the subsequently generated receipt, avoiding circular hashes.
- `verify_audit_packet.py`: validates the manifest, replays the finite checks under normal Python, `-O`, and `-OO`, tests deliberately failing controls, performs actual non-root read-only probes, and confirms the payload is unchanged. Run it on a copy with directory mode `0555` and file modes `0444`, redirecting stdout outside that copy.
- `VERIFICATION_RECEIPT.json`: the observed replay result, bound to the exact manifest hash. This receipt is integrity and diagnostic evidence, not a substitute for the proof audit.

A suitable replay is `python3 -B -O verify_audit_packet.py > ../replay-receipt.json` from the read-only packet as a non-root user. Python 3.10 or later is required. No network, third-party package, compiler, author script or external source archive is needed for this replay.
